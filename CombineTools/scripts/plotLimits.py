#!/usr/bin/env python
import sys
import ROOT
import math
# from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
# import os.path
from array import array
import CombineHarvester.CombineTools.maketable as maketable

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='named input file')
parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
args = parser.parse_args()


def LimitTGraphFromJSON(js, label):
    xvals = []
    yvals = []
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][label])
    graph = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    graph.Sort()
    return graph

def LimitBandTGraphFromJSON(js, central, lo, hi):
    xvals = []
    yvals = []
    yvals_lo = []
    yvals_hi = []
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][central])
        yvals_lo.append(js[key][central] - js[key][lo])
        yvals_hi.append(js[key][hi] - js[key][central])
    graph = ROOT.TGraphAsymmErrors(len(xvals), array('d', xvals), array('d', yvals), array('d', [0]), array('d', [0]), array('d', yvals_lo), array('d', yvals_hi))
    graph.Sort()
    return graph


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# plot.ModTDRStyle(width=700, l = 0.13)
plot.ModTDRStyle()
# ROOT.gStyle.SetNdivisions(510, "XYZ")
# ROOT.gStyle.SetMarkerSize(0.7)

canv = ROOT.TCanvas('limit', 'limit')
pads = plot.OnePad()

data = {}
with open(args.file) as jsonfile:
    data = json.load(jsonfile)

g_obs = LimitTGraphFromJSON(data, 'observed')
g_obs.SetLineWidth(2)
axishist = plot.CreateAxisHist(g_obs, True)

g_exp = LimitTGraphFromJSON(data, 'expected')
g_exp.SetLineWidth(2)
g_exp.SetLineColor(ROOT.kRed)
# g_exp.SetLineStyle(9)
g_exp1 = LimitBandTGraphFromJSON(data, 'expected', '-1', '+1')
g_exp1.SetFillColor(ROOT.kGreen)
g_exp2 = LimitBandTGraphFromJSON(data, 'expected', '-2', '+2')
g_exp2.SetFillColor(ROOT.kYellow)
# print ROOT.gPad

pads[0].cd()
axishist.Draw()
axishist.SetMinimum(0.1)
axishist.SetMaximum(3)
axishist.GetYaxis().SetTitle('95% CL limit on #sigma/#sigma_{SM}')
axishist.GetXaxis().SetTitle('m_{H} (GeV)')
g_exp2.Draw('3SAME')
g_exp1.Draw('3SAME')

line = ROOT.TLine()
line.SetLineColor(ROOT.kBlue)
line.SetLineWidth(2)

plot.DrawHorizontalLine(pads[0], line, 1)

g_exp.Draw('LSAME')
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()
g_obs.Draw('PLSAME')


legend = ROOT.TLegend(0.64, 0.71, 0.93, 0.90, '', 'NBNDC')
legend.AddEntry(g_obs, 'Observed', 'LP')
legend.AddEntry(g_exp, 'Expected', 'L')
legend.AddEntry(g_exp1, '#pm1#sigma Expected', 'F')
legend.AddEntry(g_exp2, '#pm2#sigma Expected', 'F')
legend.Draw()


plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.0)
plot.DrawTitle(pads[0], '4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV)', 3)
plot.DrawTitle(pads[0], 'H#rightarrow#tau#tau', 1)



# outfile.Close()
canv.Print('.pdf')
canv.Print('.png')
# canv.Print('.C')
maketable.TablefromJson(args.table_vals, args.file, "TablefromJson.txt")
