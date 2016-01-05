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

plot.ModTDRStyle(width=750, height=600, l = 0.15, b = 0.07, r = 0.17)
plot.SetBirdPalette()
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)
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
parser.add_argument('--label', '-l', help='Main input file')
parser.add_argument('--translate', default='texName.json', help='json file with POI name translation')
parser.add_argument('--cov', action='store_true', help='json file with POI name translation')

args = parser.parse_args()

if args.cov:
    ROOT.gStyle.SetPaintTextFormat('.3f')


if args.translate is not None:
    with open(args.translate) as jsonfile:    
        name_translate = json.load(jsonfile)


inputs = args.input.split(':')
fin = ROOT.TFile(inputs[0])
hist = fin.Get(inputs[1])

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

hist.GetXaxis().LabelsOption('h')
hist.GetXaxis().SetLabelFont(62)
hist.GetYaxis().SetLabelFont(62)
hist.GetXaxis().SetLabelSize(0.04)
hist.GetYaxis().SetLabelSize(0.041)
if not args.cov:
    hist.SetMinimum(-1)
    hist.SetMaximum(+1)
hist.SetContour(255)

canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()

hist.Draw('COLZTEXT')

plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', 'LHC Run 1 Internal', 0, 0.38, 0.035, 1.2)
if args.label is not None: plot.DrawTitle(pads[0], args.label, 3)


canv.Print('.pdf')
canv.Print('.png')
# canv.Print('.C')
