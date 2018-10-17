#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(width=750, height=600, l = 0.17, b = 0.15, r = 0.23, t=0.08)
plot.SetCorrMatrixPalette()
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPaintTextFormat('.2f')


def ColorLabels(text):
    # text = text.replace('#tau#tau', '#color[2]{#tau#tau}')
    # text = text.replace('WW', '#color[8]{WW}')
    # text = text.replace('ZZ', '#color[9]{ZZ}')
    # text = text.replace('bb', '#color[6]{bb}')
    # text = text.replace('#gamma#gamma', '#color[43]{#gamma#gamma}')
    return text


parser = argparse.ArgumentParser(
    prog='plot1DScan.py',
    )


parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--input', '-i', help='Main input file')
parser.add_argument('--POIs', help='List of POIs')
parser.add_argument('--label', '-l', help='Main input file')
parser.add_argument('--translate', default='texName.json', help='json file with POI name translation')
parser.add_argument('--cov', action='store_true', help='plot the covariance instead')
parser.add_argument('--label-size', type=float, default=0.04)
parser.add_argument('--marker-size', type=float, default=1.5)
parser.add_argument('--print-twiki', action='store_true')
parser.add_argument(
    '--subline', default='Projection', help='text to add next to cms logo')
parser.add_argument(
    '--postfix', default='', help='output postfix')

args = parser.parse_args()

POIs = args.POIs.split(',')

if args.cov:
    ROOT.gStyle.SetPaintTextFormat('.3f')


if args.translate is not None:
    with open(args.translate) as jsonfile:
        name_translate = json.load(jsonfile)


inputs = args.input.split(':')
fin = ROOT.TFile(inputs[0])
rfr = fin.Get(inputs[1])

hist = ROOT.TH2F('cor', '', len(POIs), 0, len(POIs), len(POIs), 0, len(POIs))

for i, ip in enumerate(POIs):
    hist.GetXaxis().SetBinLabel(i + 1, ip)
    hist.GetYaxis().SetBinLabel(len(POIs) - i, ip)
    for j, jp in enumerate(POIs):
        hist.SetBinContent(i + 1, len(POIs) - j, rfr.correlation(ip, jp))

for i in xrange(1,hist.GetXaxis().GetNbins()+1):
    new_name = hist.GetXaxis().GetBinLabel(i)
    if new_name in name_translate:
        new_name = name_translate[new_name]
        new_name = ColorLabels(new_name)
    hist.GetXaxis().SetBinLabel(i, new_name)

for i in xrange(1,hist.GetYaxis().GetNbins()+1):
    new_name = hist.GetYaxis().GetBinLabel(i)
    if new_name in name_translate:
        new_name = name_translate[new_name]
        new_name = ColorLabels(new_name)
    hist.GetYaxis().SetBinLabel(i, new_name)

if args.print_twiki:
    for i in reversed(range(1, hist.GetYaxis().GetNbins()+1)):
        line = ''
        line += '| *$%-60s$* | ' % hist.GetYaxis().GetBinLabel(i)
        for j in range(1, hist.GetXaxis().GetNbins()+1):
            line += ' %.2f |' % hist.GetBinContent(j, i)
        print line
    line = '| |'
    for j in range(1, hist.GetXaxis().GetNbins()+1):
        line += ' *$%-30s$* | ' % hist.GetXaxis().GetBinLabel(j)
    print line
# hist.GetXaxis().LabelsOption('v')
hist.GetXaxis().SetLabelFont(42)
hist.GetYaxis().SetLabelFont(42)
hist.GetXaxis().SetTickLength(0)
hist.GetYaxis().SetTickLength(0)
hist.GetXaxis().SetLabelSize(args.label_size)
hist.GetYaxis().SetLabelSize(args.label_size)
hist.GetZaxis().SetLabelSize(0.03)
hist.GetZaxis().SetTitle('#rho')
if not args.cov:
    hist.SetMinimum(-1)
    hist.SetMaximum(+1)
hist.SetContour(255)

canv = ROOT.TCanvas(args.output + args.postfix, args.output + args.postfix)
pads = plot.OnePad()


ROOT.gStyle.SetTextFont(42)
hist.SetMarkerSize(args.marker_size)
hist.Draw('COLZTEXT')

plot.DrawCMSLogo(pads[0], 'CMS', args.subline, 0, 0.15, 0.035, 1.2)
if args.label is not None: plot.DrawTitle(pads[0], args.label, 3)


canv.Print('.pdf')
canv.Print('.png')
# canv.Print('.C')
