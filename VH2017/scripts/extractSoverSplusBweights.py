#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.ch as ch
import glob
import ROOT
import math
import argparse
import json
import sys
import os
import fnmatch
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = argparse.ArgumentParser()
parser.add_argument('--workspace','-w', help='Input workspace')
parser.add_argument('--fitresult','-f', help='RooFit result file')
parser.add_argument('--datacard','-d', help='Input datacard corresponding to workspace')

args = parser.parse_args()

cb = ch.CombineHarvester()

#Create a CH instance that we are going to manipulate:
cb_man = ch.CombineHarvester()
cb_man.SetFlag('workspaces-use-clone', True)

cb_prefit = ch.CombineHarvester()
cb_prefit.SetFlag('workspaces-use-clone', True)


f_wsp = ROOT.TFile(args.workspace)
ws = f_wsp.Get('w')
ch.ParseCombineWorkspace(cb_man, ws, "ModelConfig", "data_obs", True)
ch.ParseCombineWorkspace(cb_prefit, ws, "ModelConfig", "data_obs", True)
#We are going to update the contents of cb_man to do the S/S+B weighting:


f_fit = ROOT.TFile(args.fitresult)
fitresult = f_fit.Get('fit_s')

cb_man.UpdateParameters(fitresult)
cb_man.bin(['vhbb_Wen_1_13TeV','vhbb_Wmn_1_13TeV','vhbb_Zee_1_13TeV','vhbb_Zee_2_13TeV','vhbb_Zmm_1_13TeV','vhbb_Zmm_2_13TeV','vhbb_Znn_1_13TeV']) #Only keep the SR bins

bin_dict={}
sig_dict={} #Need to keep track of signal as total norm should be preserved
bkg_hist =  ROOT.TH1F()
sig_hist = ROOT.TH1F()

for b in cb_man.bin_set():
  cb_man_bin = cb_man.cp().bin([b])
  bkg_hist = cb_man.cp().bin([b]).backgrounds().GetShape()
  sig_hist = cb_prefit.cp().bin([b]).signals().GetShape()
  bin_dict[b] = {}
  sig_dict[b] = {}
  for i in range(1,bkg_hist.GetNbinsX()+1):
    c_sig = sig_hist.GetBinContent(i)
    c_bkg = bkg_hist.GetBinContent(i)
    c_splusb = c_sig/(c_bkg+c_sig)
    bin_dict[b][i] = c_splusb ##Note: we'll end up with weights even for the bins with which the distributions are padded. This is fixed in the next step
    sig_dict[b][i] = c_sig 


#Now let's parse the original full combined datacard so we can extract the bin boundaries used
cb.ParseDatacard(args.datacard,"vhbb","13TeV","")
cb.bin(['vhbb_Wen_1_13TeV','vhbb_Wmn_1_13TeV','vhbb_Zee_1_13TeV','vhbb_Zee_2_13TeV','vhbb_Zmm_1_13TeV','vhbb_Zmm_2_13TeV','vhbb_Znn_1_13TeV']) #Only keep the SR bins

tot_sig=0.
tot_wt_sig=0.
for b in cb.bin_set():
  bkg_hist = cb.cp().bin([b]).backgrounds().GetShape()
  for i in range(1,bkg_hist.GetNbinsX()+1):
    tot_sig+=sig_dict[b][i]
    tot_wt_sig+=(sig_dict[b][i]*bin_dict[b][i])

sf=tot_sig/tot_wt_sig #Scale factor needed to be applied to all weights to preserve total signal norm

outfile = ROOT.TFile.Open("store_ssplusbweights.root","RECREATE")
for b in cb.bin_set():
  bkg_hist = cb.cp().bin([b]).backgrounds().GetShape()
  current_wts = bkg_hist.Clone(b)
  for i in range(1,bkg_hist.GetNbinsX()+1):
    current_wts.SetBinContent(i,bin_dict[b][i]*sf)
  current_wts.Write() 

outfile.Close()  
    


