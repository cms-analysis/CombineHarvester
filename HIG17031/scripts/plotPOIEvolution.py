#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()


parser = argparse.ArgumentParser()

parser.add_argument(
    '--json-files', default='impacts_%(LUMI)s.json', help='JSON filenames, including a %(LUMI)s string')
parser.add_argument(
    '--lumi', default='35.9,100,300,1000,3000', help='list of lumi points')
parser.add_argument(
    '--model', default='A1_5D', help='model identifier')
parser.add_argument(
    '--scenario', default='S1', help='scenario identifier')
parser.add_argument(
    '--subline', default='Projection', help='text to add next to cms logo')
parser.add_argument(
    '--postfix', default='', help='output postfix')
parser.add_argument(
    '--y-max', default=0.3, type=float, help='Attempt to use this max for all plots')
parser.add_argument('--translate', default='texName.json', help='json file with POI name translation')

args = parser.parse_args()

if args.translate is not None:
    with open(args.translate) as jsonfile:
        name_translate = json.load(jsonfile)

lumi_vals = args.lumi.split(',')

jsons = []

for l in lumi_vals:
    with open(args.json_files % {'LUMI': l}) as jsonfile:
        jsons.append(json.load(jsonfile)[args.model])

POIs = [str(x) for x in jsons[0].keys()]

print POIs

for POI in POIs:
    texname = name_translate.get(POI, POI)
    xvals = []
    yvals = []
    yvals_stat = []
    yvals_sigth = []
    yvals_bkgth = []
    yvals_exp = []
    yvals_pred = []
    for i, l in enumerate(lumi_vals):
        errSym = (jsons[i][POI]['ErrorHi'] - jsons[i][POI]['ErrorLo']) / 2.
        errStatSym = (jsons[i][POI]['StatHi'] - jsons[i][POI]['StatLo']) / 2.
        errSigThSym = (jsons[i][POI]['SigThHi'] - jsons[i][POI]['SigThLo']) / 2.
        errBkgThSym = (jsons[i][POI]['BkgThHi'] - jsons[i][POI]['BkgThLo']) / 2.
        errExpSym = (jsons[i][POI]['ExpHi'] - jsons[i][POI]['ExpLo']) / 2.
        xvals.append(float(l))
        yvals.append(errSym)
        yvals_stat.append(errStatSym)
        yvals_sigth.append(errSigThSym)
        yvals_bkgth.append(errBkgThSym)
        yvals_exp.append(errExpSym)
        if i == 0:
            yvals_pred.append(errSym)
        else:
            yvals_pred.append(yvals[0] * math.sqrt(float(lumi_vals[0]) / float(l)))
        print '%-10s %-10s %-10.3f' % (POI, l, errSym)
    gr = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    gr_pred = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_pred))
    gr_stat = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_stat))
    gr_sigth = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_sigth))
    gr_bkgth = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_bkgth))
    gr_exp = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_exp))
    plot.Set(gr, LineColor=1, MarkerColor=1, LineWidth=3)
    plot.Set(gr_pred, LineColor=1, MarkerColor=1, LineWidth=1, LineStyle=2, MarkerSize=0.5)
    plot.Set(gr_stat, LineColor=2, MarkerColor=2, LineWidth=2)
    plot.Set(gr_sigth, LineColor=4, MarkerColor=4, LineWidth=2)
    plot.Set(gr_bkgth, LineColor=28, MarkerColor=28, LineWidth=2)
    plot.Set(gr_exp, LineColor=8, MarkerColor=8, LineWidth=2)


    gr.Print()

    canv = ROOT.TCanvas('%s_%s_%s_evolution%s' % (args.scenario, args.model, POI, args.postfix), '')
    pads = plot.OnePad()
    pads[0].SetLogx(True)
    pads[0].SetGrid(3, 1)
    gr.Draw('APL')
    axishist = plot.GetAxisHist(pads[0])
    axishist.SetMinimum(0)
    gr_max = plot.GetPadYMax(pads[0])
    if gr_max < args.y_max:
        axishist.SetMaximum(args.y_max)
    print texname
    plot.Set(axishist.GetXaxis(), Title='Integrated luminosity (fb^{-1})')
    plot.Set(axishist.GetYaxis(), Title='Expected uncertainty on %s' % texname)

    gr_pred.Draw('PLSAME')
    gr_stat.Draw('PLSAME')
    gr_sigth.Draw('PLSAME')
    gr_bkgth.Draw('PLSAME')
    gr_exp.Draw('PLSAME')

    legend = ROOT.TLegend(0.75, 0.7, 0.9, 0.93, '', 'NBNDC')
    legend.AddEntry(gr, 'Total', 'L')
    legend.AddEntry(gr_pred, '1/sqrt(L)', 'L')
    legend.AddEntry(gr_stat, 'Stat', 'L')
    legend.AddEntry(gr_sigth, 'SigTh', 'L')
    legend.AddEntry(gr_bkgth, 'BkgTh', 'L')
    legend.AddEntry(gr_exp, 'Expt', 'L')
    legend.Draw()

    box = ROOT.TPaveText(0.4, 0.8, 0.65, 0.9, 'NDCNB')
    plot.Set(box, TextFont=42, TextAlign=11)
    box.AddText('#bf{Scenario: %s}' % args.scenario)
    box.AddText('Parameter: %s' % texname)
    box.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.subline, 0, 0.14, 0.035, 1.2)
    canv.Print('.pdf')
    canv.Print('.png')
    # plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)

