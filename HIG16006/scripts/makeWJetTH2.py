#!/usr/bin/env python
import ROOT
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

fin = ROOT.TFile('WJets_mt.root')

tin = fin.Get('ntuple')

xarr = array('f', [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 3900])
yarr = array('f', [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 3900])

hist = ROOT.TH2F('hist', 'hist', len(xarr)-1, xarr, len(yarr)-1, yarr)
tin.Draw("mt_sv:nearjpt_1>>+hist", "(iso_1<0.1 && mva_olddm_tight_2>0.5 && antiele_2 && antimu_2 && !leptonveto)*wt")

# Now we need to normalise in columns
for i in range(1, hist.GetNbinsX()+1):
    col_sum = 0.
    for j in range(1, hist.GetNbinsY()+1):
        col_sum += hist.GetBinContent(i, j)
    if col_sum > 0.:
        for j in range(1, hist.GetNbinsY()+1):
            hist.SetBinContent(i, j, hist.GetBinContent(i, j) / col_sum)

hist.Print('range')
fout = ROOT.TFile('WJetsFakeWeights.root', 'RECREATE')
hist.Write()
fout.Close()
