#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path

def read(scan, param_x, param_y, file):
    # print files
    goodfiles = [f for f in [file] if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    graph = plot.TGraph2DFromTree(limit, param_x, param_y, '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0')
    best = plot.TGraphFromTree(limit, param_x, param_y, 'quantileExpected > -0.5 && deltaNLL == 0')
    plot.RemoveGraphXDuplicates(best)
    assert(best.GetN() == 1)
    graph.SetName(scan)
    best.SetName(scan+'_best')
    # graph.Print()
    return (graph, best)

def fillTH2(hist2d, graph):
    for x in xrange(1, hist2d.GetNbinsX()+1):
        for y in xrange(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            val = graph.Interpolate(xc, yc)
            hist2d.SetBinContent(x, y, val)

def fixZeros(hist2d):
    for x in xrange(1, hist2d.GetNbinsX()+1):
        for y in xrange(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            if hist2d.GetBinContent(x, y) == 0:
                # print 'Bin at (%f,%f) is zero!' % (xc, yc)
                hist2d.SetBinContent(x, y, 1000)

def makeHist(name, bins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(bins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(bins) - 1.)) - 1E-5
    hist = ROOT.TH2F(name, '', bins, graph2d.GetXmin()-binw_x, graph2d.GetXmax()+binw_x, bins, graph2d.GetYmin()-binw_y, graph2d.GetYmax()+binw_y)
    return hist

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(l=0.13, b=0.10, r=0.15)
plot.SetBirdPalette()

# ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetNdivisions(506, "Y")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--file', '-f', help='named input scans')
parser.add_argument('--multi', type=int, default=1, help='scale number of bins')
parser.add_argument('--thin', type=int, default=1, help='thin graph points')
parser.add_argument('--order', default='b,tau,Z,gam,W,comb')
parser.add_argument('--x-range', default=None)
parser.add_argument('--x-axis', default='#kappa_{V}')
parser.add_argument('--y-axis', default='#kappa_{F}')
parser.add_argument('--axis-hist', default=None)
parser.add_argument('--layout', type=int, default=1)
args = parser.parse_args()

infile = args.file

order = args.order.split(',')

graph_test = read('test', args.x_axis, args.y_axis, infile)[0]


if args.axis_hist is not None:
    hargs = args.axis_hist.split(',')
    axis = ROOT.TH2F('hist2d', '', int(hargs[0]), float(hargs[1]), float(hargs[2]), int(hargs[3]), float(hargs[4]), float(hargs[5]))
else:
    axis = makeHist('hist2d', 40 * args.multi, graph_test)

# axis = None
axis.GetXaxis().SetTitle(args.x_axis)
axis.GetYaxis().SetTitle(args.y_axis)

canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].SetGridx(False)
pads[0].SetGridy(False)
pads[0].Draw()
axis.Draw()
if args.x_range is not None:
    xranges = args.x_range.split(',')
    axis.GetXaxis().SetRangeUser(float(xranges[0]), float(xranges[1]))

if args.layout == 1:
    legend = ROOT.TLegend(0.14, 0.53, 0.35, 0.74, '', 'NBNDC')
if args.layout == 2:
    legend = ROOT.TLegend(0.15, 0.11, 0.46, 0.27, '', 'NBNDC')
    legend.SetNColumns(2)
if args.layout == 3:
    legend = ROOT.TLegend(0.14, 0.53, 0.35, 0.74, '', 'NBNDC')


graphs = {}
bestfits = {}
hists = {}
conts68 = {}
conts95 = {}

outfile = ROOT.TFile(args.output+'.root', 'RECREATE')
order = ['default']
for scan in order:
    graphs[scan], bestfits[scan] = read(scan, args.x_axis, args.y_axis, infile)
    outfile.WriteTObject(graphs[scan], scan+'_graph')
    outfile.WriteTObject(bestfits[scan])
    hists[scan] = makeHist(scan+'_hist', 40 * args.multi, graph_test)
    fillTH2(hists[scan], graphs[scan])
    outfile.WriteTObject(hists[scan], hists[scan].GetName()+'_input')
    fixZeros(hists[scan])
    hists[scan].Draw('COLZSAME')
    hists[scan].SetMinimum(0)
    hists[scan].SetMaximum(10)
    outfile.WriteTObject(hists[scan], hists[scan].GetName()+'_processed')
    conts68[scan] = plot.contourFromTH2(hists[scan], ROOT.Math.chisquared_quantile_c(1-0.68, 2))
    conts95[scan] = plot.contourFromTH2(hists[scan], ROOT.Math.chisquared_quantile_c(1-0.95, 2))
    for i, c in enumerate(conts68[scan]):
        if args.thin > 1:
            newgr = ROOT.TGraph(c.GetN() / args.thin)
            needLast = True
            for a,p in enumerate(range(0, c.GetN(), args.thin)):
                if p == c.GetN()-1: needLast = False
                newgr.SetPoint(a, c.GetX()[p], c.GetY()[p])
            if needLast: newgr.SetPoint(newgr.GetN(), c.GetX()[c.GetN()-1], c.GetY()[c.GetN()-1])
            conts68[scan][i] = newgr
            c = conts68[scan][i]
        c.SetLineWidth(3)
        pads[0].cd()
        c.Draw('L SAME')
        outfile.WriteTObject(c, 'graph68_%s_%i' % (scan, i))
    if scan in conts95:
        for i, c in enumerate(conts95[scan]):
            c.SetLineWidth(3)
            c.SetLineStyle(9)
            pads[0].cd()
            outfile.WriteTObject(c, 'graph95_%s_%i' % (scan, i))
    legend.AddEntry(conts68[scan][0], 'Scan', 'F')
for scan in order:
    for i, c in enumerate(conts68[scan]):
        c.Draw('L SAME')
    if scan in conts95:
        for i, c in enumerate(conts95[scan]):
            c.Draw('L SAME')

for scan in order:
    bestfits[scan].SetMarkerStyle(34)
    bestfits[scan].SetMarkerSize(1.2)
    if scan == 'comb': bestfits[scan].SetMarkerSize(1.5)
    bestfits[scan].Draw('PSAME')

sm_point = ROOT.TGraph()
sm_point.SetPoint(0, 1, 1)
# sm_point.SetMarkerColor(ROOT.TColor.GetColor(249, 71, 1))
sm_point.SetMarkerColor(ROOT.kBlack)
sm_point.SetMarkerStyle(33)
sm_point.SetMarkerSize(2)
sm_point.Draw('PSAME')
# sm_point.SetFillColor(ROOT.TColor.GetColor(248, 255, 1))

# legend.Draw()

if args.layout == 1:
    legend2 = ROOT.TLegend(0.15, 0.11, 0.94, 0.15, '', 'NBNDC')
    legend2.SetNColumns(4)
if args.layout == 2:
    legend2 = ROOT.TLegend(0.14, 0.53, 0.34, 0.74, '', 'NBNDC')
if args.layout == 3:
    legend2 = ROOT.TLegend(0.57, 0.7, 0.82, 0.9, '', 'NBNDC')
    # legend2.SetNColumns(2)
legend2.AddEntry(conts68['default'][0], '68% CL', 'L')
legend2.AddEntry(conts95['default'][0], '95% CL', 'L')
legend2.AddEntry(bestfits['default'], 'Best fit', 'P')
legend2.AddEntry(sm_point, 'SM expected', 'P')
legend2.SetMargin(0.4)
legend2.Draw()

box = ROOT.TPave(0.15, 0.82, 0.41, 0.92, 0, 'NBNDC')
# box.Draw()
plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1}', 11, 0.025, 0.035, 1.1, extraText2='#it{Internal}')

axis.SetMinimum(0)
axis.SetMaximum(6)
# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{+}CMS', '#it{LHC Run 1}', 11, 0.02, 0.035, 1.1, extraText2='#it{Internal}')
# pads[0].RedrawAxis()
canv.Print('.pdf')
canv.Print('.png')
outfile.Close()




