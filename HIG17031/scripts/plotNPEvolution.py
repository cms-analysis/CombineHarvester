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
    '--json-files', default='impacts_A1_5D_%(LUMI)s_extra.json', help='JSON filenames, including a %(LUMI)s string')
parser.add_argument(
    '--lumi', default='35.9,100,300,1000,3000', help='list of lumi points')
parser.add_argument(
    '--param', default='', help='model identifier')
parser.add_argument(
    '--model', default='', help='model identifier')
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
        jsonraw = json.load(jsonfile)['params']
        jsonproc = {}
        for X in jsonraw:
            jsonproc[X['name']] = X
        jsons.append(jsonproc)


params = [args.param]

print params

for param in params:
    # texname = name_translate.get(POI, POI)
    xvals = []
    yvals_In = []
    yvals = []
    yvals_In_pred = []
    for i, l in enumerate(lumi_vals):
        inSym = (jsons[i][param]['prefit'][2] - jsons[i][param]['prefit'][0]) / 2.
        fitSym = (jsons[i][param]['fit'][2] - jsons[i][param]['fit'][0]) / 2.
        xvals.append(float(l))
        yvals.append(fitSym)
        yvals_In.append(inSym)
        if i == 0:
            yvals_In_pred.append(inSym)
        else:
            yvals_In_pred.append(yvals_In[0] * math.sqrt(float(lumi_vals[0]) / float(l)))
    gr = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    gr_In = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_In))
    print yvals_In_pred
    gr_In_pred = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_In_pred))
    plot.Set(gr_In, LineColor=1, MarkerColor=1, LineWidth=3)
    plot.Set(gr_In_pred, LineColor=1, MarkerColor=1, LineWidth=1, LineStyle=2, MarkerSize=0.5)
    plot.Set(gr, LineColor=2, MarkerColor=2, LineWidth=2)


    gr.Print()

    canv = ROOT.TCanvas('%s_%s_evolution' % (args.model, param), '')
    pads = plot.OnePad()
    pads[0].SetLogx(True)
    pads[0].SetGrid(3, 1)
    gr.Draw('APL')
    axishist = plot.GetAxisHist(pads[0])
    axishist.SetMinimum(0)
    gr_max = plot.GetPadYMax(pads[0])
    if gr_max < args.y_max:
        axishist.SetMaximum(args.y_max)
    # print texname
    plot.Set(axishist.GetXaxis(), Title='Integrated luminosity (fb^{-1})')
    plot.Set(axishist.GetYaxis(), Title='Expected constraints on %s' % param)

    gr_In.Draw('PLSAME')
    gr_In_pred.Draw('PLSAME')

    legend = ROOT.TLegend(0.20, 0.15, 0.4, 0.35, '', 'NBNDC')
    legend.AddEntry(gr, 'Post-fit', 'L')
    legend.AddEntry(gr_In, 'Pre-fit', 'L')
    legend.AddEntry(gr_In_pred, 'Pre-fit * 1/sqrt(L)', 'L')
    legend.Draw()

    box = ROOT.TPaveText(0.43, 0.15, 0.64, 0.28, 'NDCNB')
    plot.Set(box, TextFont=42, TextAlign=11)
    box.AddText('#bf{Scenario 1}')
    box.AddText('Parameter: %s' % param)
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
