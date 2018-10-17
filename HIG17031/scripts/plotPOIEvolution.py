#!/usr/bin/env python
# import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
# import os.path
from array import array


def ErrVal(poi_dict, error_label, warn=False, handleZero=False):
    err_hi = poi_dict['%sHi' % error_label]
    err_lo = poi_dict['%sLo' % error_label]
    if poi_dict['ValidErrorHi'] and poi_dict['ValidErrorLo']:
        if err_hi == 0.0:
            print '%sHi is exactly zero' % error_label
            if handleZero:
                print 'Replacing with %sLo = %.4f' % (error_label, err_lo * -1.)
                err_hi = err_lo * -1.
        if err_lo == 0.0:
            print '%sLo is exactly zero' % error_label
            if handleZero:
                print 'Replacing with %sHi = %.4f' % (error_label, err_hi * -1.)
                err_lo = err_hi * -1.
        err = (err_hi - err_lo) / 2.
    elif poi_dict['ValidErrorHi'] and not poi_dict['ValidErrorLo']:
        print 'ErrorLo is not valid!'
        err = err_hi
    elif not poi_dict['ValidErrorHi'] and poi_dict['ValidErrorLo']:
        print 'ErrorHi is not valid!'
        err = -1. * err_lo
    else:
        print 'Neither ErrorLo or ErrorHi is valid!'
        err = 0.
    return err


def FixGraph(gr):
    N = gr.GetN()
    for i in range(1, N - 1):
        xm1 = gr.GetX()[i - 1]
        ym1 = gr.GetY()[i - 1]
        x = gr.GetX()[i]
        y = gr.GetY()[i]
        xp1 = gr.GetX()[i + 1]
        yp1 = gr.GetY()[i + 1]
        m = (yp1 - ym1) / (math.log10(xp1) - math.log10(xm1))
        if y > ym1 and y > yp1:
            gr.GetY()[i] = ym1 + m * (math.log10(x) - math.log10(xm1))


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
    '--fix-fluctuations', action='store_true')
parser.add_argument(
    '--show', default='Error,Stat,SigTh,BkgTh,Exp')
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

show = args.show.split(',')

for POI in POIs:
    texname = name_translate.get(POI, POI)
    xvals = []
    yvals = []
    yvals_stat = []
    yvals_sigth = []
    yvals_siginc = []
    yvals_sigacc = []
    yvals_bkgth = []
    yvals_exp = []
    yvals_pred = []
    for i, l in enumerate(lumi_vals):
        errSym = ErrVal(jsons[i][POI], 'Error', warn=True, handleZero=True)
        errStatSym = ErrVal(jsons[i][POI], 'Stat', warn=True, handleZero=True)
        errSigThSym = 0.
        errSigIncSym = 0.
        errSigAccSym = 0.
        if 'SigTh' in show:
            errSigThSym = ErrVal(jsons[i][POI], 'SigTh', warn=True, handleZero=True)
        if 'SigInc' in show:
            errSigIncSym = ErrVal(jsons[i][POI], 'SigInc', warn=True, handleZero=True)
        if 'SigAcc' in show:
            errSigAccSym = ErrVal(jsons[i][POI], 'SigAcc', warn=True, handleZero=True)
        errBkgThSym = ErrVal(jsons[i][POI], 'BkgTh', warn=True, handleZero=True)
        errExpSym = ErrVal(jsons[i][POI], 'Exp', warn=True, handleZero=True)
        xvals.append(float(l))
        yvals.append(errSym)
        yvals_stat.append(errStatSym)
        yvals_sigth.append(errSigThSym)
        yvals_siginc.append(errSigIncSym)
        yvals_sigacc.append(errSigAccSym)
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
    gr_siginc = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_siginc))
    gr_sigacc = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_sigacc))
    gr_bkgth = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_bkgth))
    gr_exp = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_exp))

    if args.fix_fluctuations:
        for g in [gr, gr_pred, gr_stat, gr_sigth, gr_siginc, gr_sigacc, gr_bkgth, gr_exp]:
            g.SetMarkerSize(1.6)
            FixGraph(g)

    plot.Set(gr, LineColor=1, MarkerColor=1, LineWidth=4)
    plot.Set(gr_pred, LineColor=1, MarkerColor=1, LineWidth=1, LineStyle=2, MarkerSize=0.5)
    plot.Set(gr_stat, LineColor=2, MarkerColor=2, LineWidth=3, MarkerStyle=33)
    plot.Set(gr_sigth, LineColor=4, MarkerColor=4, LineWidth=3, MarkerStyle=22)
    plot.Set(gr_siginc, LineColor=4, MarkerColor=4, LineWidth=3, MarkerStyle=22)
    plot.Set(gr_sigacc, LineColor=ROOT.kAzure + 8, MarkerColor=ROOT.kAzure + 8, LineWidth=3, MarkerStyle=23)
    plot.Set(gr_bkgth, LineColor=28, MarkerColor=28, LineWidth=3, MarkerStyle=21)
    plot.Set(gr_exp, LineColor=8, MarkerColor=8, LineWidth=3, MarkerStyle=34)

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
    plot.Set(axishist.GetYaxis(), Title='Expected uncertainty')

    # gr_pred.Draw('PLSAME')
    gr_stat.Draw('PLSAME')
    if 'SigTh' in show:
        gr_sigth.Draw('PLSAME')
    if 'SigInc' in show:
        gr_siginc.Draw('PLSAME')
    if 'SigAcc' in show:
        gr_sigacc.Draw('PLSAME')
    gr_bkgth.Draw('PLSAME')
    gr_exp.Draw('PLSAME')

    legend = ROOT.TLegend(0.75, 0.7, 0.92, 0.93, '', 'NBNDC')
    legend.AddEntry(gr, 'Total', 'LP')
    # legend.AddEntry(gr_pred, '1/sqrt(L)', 'L')
    legend.AddEntry(gr_stat, 'Stat', 'LP')
    if 'SigTh' in show:
        legend.AddEntry(gr_sigth, 'SigTh', 'LP')
    if 'SigInc' in show:
        legend.AddEntry(gr_siginc, 'SigInc', 'LP')
    if 'SigAcc' in show:
        legend.AddEntry(gr_sigacc, 'SigAcc', 'LP')
    legend.AddEntry(gr_bkgth, 'BkgTh', 'LP')
    legend.AddEntry(gr_exp, 'Expt', 'LP')
    legend.Draw()

    # latex = ROOT.TLatex()
    # plot.Set(latex, TextFont=42, TextAlign=12, TextSize=0.05)
    # latex.DrawLatexNDC(0.50, 0.87, 'Parameter: #bf{%s}' % texname)

    box = ROOT.TPaveText(0.47, 0.77, 0.72, 0.93, 'NDCNB')
    plot.Set(box, TextFont=42, TextAlign=11)
    box.AddText('YR2018 %s' % args.scenario)
    box.AddText('Parameter: %s' % texname)
    box.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.subline, 0, 0.14, 0.035, 1.2)
    # plot.DrawTitle(pads[0], 'YR2018 %s' % args.scenario, 3)
    canv.Print('.pdf')
    canv.Print('.png')

