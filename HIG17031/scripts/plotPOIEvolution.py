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
    yvals_exp = []
    yvals_pred = []
    for i, l in enumerate(lumi_vals):
        errSym = (jsons[i][POI]['ErrorHi'] - jsons[i][POI]['ErrorLo']) / 2.
        errStatSym = (jsons[i][POI]['StatHi'] - jsons[i][POI]['StatLo']) / 2.
        errSigThSym = (jsons[i][POI]['SigThHi'] - jsons[i][POI]['SigThLo']) / 2.
        errExpSym = (jsons[i][POI]['ExpHi'] - jsons[i][POI]['ExpLo']) / 2.
        xvals.append(float(l))
        yvals.append(errSym)
        yvals_stat.append(errStatSym)
        yvals_sigth.append(errSigThSym)
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
    gr_exp = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_exp))
    plot.Set(gr, LineColor=1, MarkerColor=1, LineWidth=3)
    plot.Set(gr_pred, LineColor=1, MarkerColor=1, LineWidth=1, LineStyle=2, MarkerSize=0.5)
    plot.Set(gr_stat, LineColor=2, MarkerColor=2, LineWidth=2)
    plot.Set(gr_sigth, LineColor=4, MarkerColor=4, LineWidth=2)
    plot.Set(gr_exp, LineColor=8, MarkerColor=8, LineWidth=2)


    gr.Print()

    canv = ROOT.TCanvas('%s_%s_evolution' % (args.model, POI), '')
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
    gr_exp.Draw('PLSAME')

    legend = ROOT.TLegend(0.75, 0.7, 0.9, 0.93, '', 'NBNDC')
    legend.AddEntry(gr, 'Total', 'L')
    legend.AddEntry(gr_pred, '1/sqrt(L)', 'L')
    legend.AddEntry(gr_stat, 'Stat', 'L')
    legend.AddEntry(gr_sigth, 'SigTh', 'L')
    legend.AddEntry(gr_exp, 'Other', 'L')
    legend.Draw()

    box = ROOT.TPaveText(0.4, 0.8, 0.65, 0.9, 'NDCNB')
    plot.Set(box, TextFont=42, TextAlign=11)
    box.AddText('#bf{Scenario 1}')
    box.AddText('Parameter: %s' % texname)
    box.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', 'Projection', 0, 0.14, 0.035, 1.2)
    canv.Print('.pdf')
    canv.Print('.png')
    # plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)

# print len(x1)
# print len(x2)

# h_abs_diff = ROOT.TH1F('abs_diff', '', 50, -0.2, 0.2)
# h_abs_diff.SetLineColor(ROOT.kRed)

# h_err_rel = ROOT.TH1F('err_rel', '', 50, 0.9, 1.1)
# h_err_rel.SetLineColor(ROOT.kBlue)

# h_err_abs = ROOT.TH1F('err_abs', '', 50, -0.1, 0.1)
# h_err_abs.SetLineColor(ROOT.kBlue)

# for i in range(len(x1)):
#     h_abs_diff.Fill(x2[i][0] - x1[i][0])
#     if (x1[i][1]+x1[i][2]) > 0.:
#         h_err_rel.Fill(((x2[i][1]+x2[i][2])/2.)/((x1[i][1]+x1[i][2])/2.))
#     h_err_abs.Fill(((x2[i][1]+x2[i][2])/2.) - ((x1[i][1]+x1[i][2])/2.))

# h_abs_diff.GetXaxis().SetTitle('#hat{#mu}_{%s} - #hat{#mu}_{%s}' % (mod2, mod1))
# h_abs_diff.GetYaxis().SetTitle('nToys')

# h_err_rel.GetXaxis().SetTitle('#sigma_{%s}/#sigma_{%s}' % (mod2, mod1))
# h_err_rel.GetYaxis().SetTitle('nToys')

# h_err_abs.GetXaxis().SetTitle('#sigma_{%s} - #sigma_{%s}' % (mod2, mod1))
# h_err_abs.GetYaxis().SetTitle('nToys')

# canv = ROOT.TCanvas('%s_%s_%s_abs_diff' % (mod1, mod2, toy), 'abs_diff')
# pads = plot.OnePad()
# h_abs_diff.Draw('HIST')

# mean = h_abs_diff.GetMean()
# stdv = h_abs_diff.GetStdDev()

# # mean = h_abs_diff.GetMean()
# stdverr = h_abs_diff.GetStdDevError()
# print 'stdv = %.3f +/- %.3f' % (stdv, stdverr)

# box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
# box.AddText('Mean = %.3f' % mean)
# box.AddText('StdDev = %.3f' % stdv)
# box.Draw()

# # plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
# plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)

# canv.Print('.pdf')
# canv.Print('.png')


# canv = ROOT.TCanvas('%s_%s_%s_err_rel' % (mod1, mod2, toy), 'err_rel')
# pads = plot.OnePad()
# h_err_rel.Draw('HIST')

# mean = h_err_rel.GetMean()
# stdv = h_err_rel.GetStdDev()

# box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
# box.AddText('Mean = %.3f' % mean)
# box.AddText('StdDev = %.3f' % stdv)
# box.Draw()

# # plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
# plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)


# canv.Print('.pdf')
# canv.Print('.png')


# canv = ROOT.TCanvas('%s_%s_%s_err_abs' % (mod1, mod2, toy), 'err_abs')
# pads = plot.OnePad()
# h_err_abs.Draw('HIST')

# mean = h_err_abs.GetMean()
# stdv = h_err_abs.GetStdDev()

# box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
# box.AddText('Mean = %.3f' % mean)
# box.AddText('StdDev = %.3f' % stdv)
# box.Draw()

# # plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
# plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)


# canv.Print('.pdf')
# canv.Print('.png')
