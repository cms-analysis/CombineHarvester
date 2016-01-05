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
    graph = plot.TGraph2DFromTree(limit, param_x, param_y, '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0 && deltaNLL < 100')
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

plot.ModTDRStyle(l=0.13, b=0.10)
# ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetNdivisions(506, "Y")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)


fin = ROOT.TFile('asymptotic_grid.root')
hist = fin.Get('h_observed')
axis = hist.Clone('axis')
axis.Reset()

# axis = None
axis.GetXaxis().SetTitle('m_{A} (GeV)')
axis.GetYaxis().SetTitle('tan#beta')

canv = ROOT.TCanvas('asymptotic_grid', 'asymptotic_grid')
pads = plot.OnePad()
pads[0].SetGridx(False)
pads[0].SetGridy(False)
pads[0].Draw()
axis.Draw()

hist.Draw('COLSAME')

conts = plot.contourFromTH2(hist, 0.05, mult = 4)
for i, c in enumerate(conts):
    c.SetFillColor(ROOT.kBlue)
    c.SetLineColor(ROOT.kBlack)
    c.SetLineWidth(3)
    pads[0].cd()
    # c.Draw('F SAME')
    c.Draw('L SAME')
    # c.Draw('P SAME')

# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1}', 11, 0.025, 0.035, 1.1, extraText2='#it{Preliminary}')
# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{+}CMS', '#it{LHC Run 1}', 11, 0.02, 0.035, 1.1, extraText2='#it{Internal}')
# pads[0].RedrawAxis()
canv.Print('.pdf')
canv.Print('.png')




