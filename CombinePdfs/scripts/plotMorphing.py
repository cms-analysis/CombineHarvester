#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import os.path
import bisect

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()

# real_points = [110., 115., 120., 125., 130., 135., 140., 145.]
real_points = [100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000]
# step = 1.
step = 10.
morph_points = []
m = real_points[0]
while m < real_points[-1]:
    morph_points.append(m)
    m += step
print(morph_points)

# file = 'htt_sm_morphing_debug_full.root'
# folder = 'htt_mt_1_8TeV_ggH_morph'

file = 'htt_mt_mssm_demo.root'
folder = 'htt_mt_8_8TeV_bbH_Htautau_morph'

fin = ROOT.TFile(file)
ROOT.gDirectory.cd(folder)

donescale = False

for p in morph_points:
    print('%g' % p)

    hmorph = ROOT.gDirectory.Get('morph_point_%g' % p)
    hmorph.Scale(1, 'width')
    hmorph.Scale(1/hmorph.Integral())
    canv = ROOT.TCanvas('%s_%g' % (folder, p), '')
    pads = plot.OnePad()
    hmorph.SetLineWidth(3)
    hmorph.GetXaxis().SetTitle('m_{#tau#tau}')
    hmorph.GetYaxis().SetTitle('PDF value')
    hmorph.Draw('HIST')
    upper = bisect.bisect_right(real_points, p)
    lower = upper - 1
    morph_pair = [real_points[upper], real_points[lower]]
    rhists = []
    for r in real_points:
        rhists.append(ROOT.gDirectory.Get('actual_point_%g' % r))
        if not donescale: rhists[-1].Scale(1, 'width')
        if not donescale: rhists[-1].Scale(1/rhists[-1].Integral())
        rhists[-1].SetLineWidth(2)
        if r in morph_pair:
            rhists[-1].SetLineColor(ROOT.kRed)
        else:
            rhists[-1].SetLineColor(16)
        rhists[-1].Draw('HISTSAME')
    donescale = True
    hmorph.Draw('HISTSAME')
    hmorph.SetMaximum(0.3)
    plot.DrawTitle(pads[0], 'RooMorphingPdf:%s' % folder, 3)
    legend = ROOT.TLegend(0.50, 0.7, 0.93, 0.93, '', 'NBNDC')
    legend.AddEntry(rhists[lower], 'Lower: m_{H} = %g GeV' % real_points[lower], 'L')
    legend.AddEntry(hmorph, 'Morph: m_{H} = %g GeV' % p, 'L')
    legend.AddEntry(rhists[upper], 'Upper: m_{H} = %g GeV' % real_points[upper], 'L')
    legend.Draw()

    canv.Print('.pdf')
    canv.Print('.png')
