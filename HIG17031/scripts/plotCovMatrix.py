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

plot.ModTDRStyle(width=750, height=600, l = 0.18, b = 0.18, r = 0.23)
plot.SetCorrMatrixPalette()
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPaintTextFormat('.2f')


def ColorLabels(text):
    return text


parser = argparse.ArgumentParser(
    prog='plot1DScan.py',
    )


parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--input', '-i', help='Main input file')
parser.add_argument('--label', '-l', help='Main input file')
parser.add_argument('--translate', default='texName.json', help='json file with POI name translation')
parser.add_argument('--cov', action='store_true', help='json file with POI name translation')
parser.add_argument('--label-size', type=float, default=0.04)
parser.add_argument('--reorder', default=None)
parser.add_argument('--special', default=None)
parser.add_argument('--subline', default='Internal')
parser.add_argument('--x-label-option', default='h')
parser.add_argument('--marker-size', default=0.7, type=float)
parser.add_argument('--rounding', action='store_true')

args = parser.parse_args()

if args.cov:
    ROOT.gStyle.SetPaintTextFormat('.3f')


if args.translate is not None:
    with open(args.translate) as jsonfile:
            name_translate = json.load(jsonfile)


inputs = args.input.split(':')
fin = ROOT.TFile(inputs[0])
hist = fin.Get(inputs[1])

if args.reorder is not None:
    new_order = args.reorder.split(',')
    curr_idx = {}
    for i in xrange(1, hist.GetXaxis().GetNbins() + 1):
        curr_idx[hist.GetXaxis().GetBinLabel(i)] = i
    hnew = hist.Clone()
    for i in xrange(1, hist.GetXaxis().GetNbins() + 1):
        for j in xrange(1, hist.GetYaxis().GetNbins() + 1):
            new_x = new_order[i - 1]
            new_y = new_order[len(new_order) - j]
            hnew.SetBinContent(i, j, hist.GetBinContent(curr_idx[new_x], len(new_order) - curr_idx[new_y] + 1))
    for i in xrange(1, hist.GetXaxis().GetNbins() + 1):
        hnew.GetXaxis().SetBinLabel(i, new_order[i - 1])
    for i in xrange(1, hist.GetYaxis().GetNbins() + 1):
        hnew.GetYaxis().SetBinLabel(i, new_order[len(new_order) - i])

    hist = hnew

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

if args.rounding:
    for i in xrange(1, hist.GetXaxis().GetNbins() + 1):
        for j in xrange(1, hist.GetYaxis().GetNbins() + 1):
            content = hist.GetBinContent(i, j)
            if abs(content) < 0.005:
                content = 0.000001
            elif abs(content) < 0.015:
                content = 0.000001
            hist.SetBinContent(i, j, content)


hist.GetXaxis().LabelsOption(args.x_label_option)
hist.GetXaxis().SetLabelFont(42)
hist.GetXaxis().SetTickLength(0)
hist.GetYaxis().SetTickLength(0)
hist.GetYaxis().SetLabelFont(42)
hist.GetXaxis().SetLabelSize(args.label_size)
hist.GetYaxis().SetLabelSize(args.label_size)
hist.GetZaxis().SetLabelSize(0.03)
hist.GetZaxis().SetTitle('#rho')

if not args.cov:
    hist.SetMinimum(-1)
    hist.SetMaximum(+1)
hist.SetContour(255)


canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()


ROOT.gStyle.SetTextFont(42)
hist.SetMarkerSize(args.marker_size)
hist.Draw('COLZTEXT')

if args.special == 'A1_5PD':
    line = ROOT.TLine()
    plot.Set(line, LineStyle=2)
    line.DrawLine(6, -3, 6, 24)
    line.DrawLine(11, -3, 11, 24)
    line.DrawLine(15, -3, 15, 24)
    line.DrawLine(19, -3, 19, 24)
    line.DrawLine(-3, 5, 24, 5)
    line.DrawLine(-3, 9, 24, 9)
    line.DrawLine(-3, 13, 24, 13)
    line.DrawLine(-3, 18, 24, 18)
    latex = ROOT.TLatex()
    plot.Set(latex, TextSize=0.03, TextAlign=22)
    latex.DrawLatex(3, -2.0, 'ggH')
    latex.DrawLatex(8.5, -2.0, 'VBF')
    latex.DrawLatex(13, -2.0, 'WH')
    latex.DrawLatex(17, -2.0, 'ZH')
    latex.DrawLatex(21.5, -2.0, 'ttH')
    plot.Set(latex, TextAngle=90)
    latex.DrawLatex(-2.5, 2.5, 'ttH')
    latex.DrawLatex(-2.5, 7, 'ZH')
    latex.DrawLatex(-2.5, 11, 'WH')
    latex.DrawLatex(-2.5, 15.5, 'VBF')
    latex.DrawLatex(-2.5, 21, 'ggH')
    plot.Set(latex, TextAngle=0, TextSize=0.05)
    latex.DrawLatex(23.5, -4.0, '#mu_{i}^{f}')
    latex.DrawLatex(-4.2, 23.5, '#mu_{i}^{f}')

plot.FixOverlay()

plot.DrawCMSLogo(pads[0], 'CMS', args.subline, 0, 0.12, 0.035, 1.2)
if args.label is not None: plot.DrawTitle(pads[0], args.label, 3)


canv.Print('.pdf')
canv.Print('.png')
# canv.Print('.C')
