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

def Eval(obj, y, x, params):
    return obj.Interpolate(x[0], y)


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(l=0.13, b=0.10, r=0.15)
# plot.SetBirdPalette()

# # ROOT.gStyle.SetNdivisions(510, "XYZ")
# ROOT.gStyle.SetNdivisions(506, "Y")
# ROOT.gStyle.SetMarkerSize(1.0)
# ROOT.gStyle.SetPadTickX(1)
# ROOT.gStyle.SetPadTickY(1)

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--file', '-f', help='named input scans')
parser.add_argument('--x-range', default=None)
parser.add_argument('--x-axis', default='#kappa_{V}')
parser.add_argument('--y-axis', default='#kappa_{F}')
args = parser.parse_args()

infile = args.file

graph_test, best = read('test', args.x_axis, args.y_axis, infile)

y_vals = set()
x_vals = set()

for i in xrange(0, graph_test.GetN()):
    if graph_test.GetZ()[i] > 99: graph_test.GetZ()[i] = 99
    if graph_test.GetZ()[i] == 0.: graph_test.GetZ()[i] = 99
    y_vals.add(graph_test.GetY()[i])
    x_vals.add(graph_test.GetX()[i])

y_list = sorted(y_vals)
print y_list


fout = ROOT.TFile('%s.root' % (args.output), 'RECREATE')
tout = ROOT.TTree('limit', 'limit')
a_r = array( 'f', [ 0 ] )
a_deltaNLL = array( 'f', [ 0 ] )
a_quantileExpected = array( 'f', [ 1 ] )
tout.Branch( args.y_axis, a_r, '%s/f'%args.y_axis )
tout.Branch( 'deltaNLL', a_deltaNLL, 'deltaNLL/f' )
tout.Branch( 'quantileExpected', a_quantileExpected, 'quantileExpected/f' )

a_r[0] = best.GetY()[0]
tout.Fill()

for i, yval in enumerate(y_list):
    func = ROOT.TF1('fn', partial(Eval, graph_test, yval), min(x_vals), max(x_vals), 1)
    min_x = func.GetMinimumX(-20 if i <= 17 else -44, 44)
    min_y = func.Eval(min_x)
    print '[%i] %s = %f, -2lnL = %f at %s = %s' % (i, args.y_axis, yval, min_y, args.x_axis, min_x)
    if min_y > 0.:
        a_r[0] = yval
        a_deltaNLL[0] = min_y
        tout.Fill()

tout.Write()
fout.Close()
    # if i == 14:
    #     canv = ROOT.TCanvas(args.output, args.output)
    #     pads = plot.OnePad()
    #     func.Draw('L')
    #     canv.Print('.pdf')
    #     canv.Print('.png')





