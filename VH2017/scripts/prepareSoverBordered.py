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

def ReorderBin(proc,binorder,xbins):
  orig_hist = proc.ShapeAsTH1F()
  orig_hist.Scale(proc.rate())
  new_hist = ROOT.TH1F(orig_hist.GetName(),orig_hist.GetTitle(),len(xbins)-1,array('d',xbins))
  for i in range(1,orig_hist.GetNbinsX()+1):
    new_hist.SetBinContent(binorder[i],new_hist.GetBinContent(binorder[i])+orig_hist.GetBinContent(i))
  proc.set_shape(new_hist,False)

def ReorderBinSystematic(syst,binorder,xbins):
  orig_hist_u = syst.ShapeUAsTH1F()
  orig_hist_d = syst.ShapeDAsTH1F()
  new_hist_u = ROOT.TH1F(orig_hist_u.GetName(),orig_hist_u.GetTitle(),len(xbins)-1,array('d',xbins))
  new_hist_d = ROOT.TH1F(orig_hist_d.GetName(),orig_hist_d.GetTitle(),len(xbins)-1,array('d',xbins))
  for i in range(1,orig_hist_u.GetNbinsX()+1):
    new_hist_u.SetBinContent(binorder[i],new_hist_u.GetBinContent(binorder[i])+orig_hist_u.GetBinContent(i))
    new_hist_d.SetBinContent(binorder[i],new_hist_d.GetBinContent(binorder[i])+orig_hist_d.GetBinContent(i))
  syst.set_shapes(new_hist_u,new_hist_d,None)




parser = argparse.ArgumentParser()
parser.add_argument('--workspace','-w', help='Input workspace')
parser.add_argument('--fitresult','-f', help='RooFit result file')
parser.add_argument('--datacard','-d',help='Input datacard')

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
#We are going to update the contents of this workspace and use these updated inputs to do the S/B ordering

f_fit = ROOT.TFile(args.fitresult)
fitresult = f_fit.Get('fit_s')

cb_man.UpdateParameters(fitresult)
cb_man.GetParameter("r").set_val(1.0)
cb_man.bin(['vhbb_Wen_1_13TeV2017','vhbb_Wmn_1_13TeV2017','vhbb_Zee_1_13TeV2017','vhbb_Zee_2_13TeV2017','vhbb_Zmm_1_13TeV2017','vhbb_Zmm_2_13TeV2017','vhbb_Znn_1_13TeV2017']) #Only keep the SR bins
#cb_man.bin(['vhbb_Wen_1_13TeV','vhbb_Wmn_1_13TeV','vhbb_Zee_1_13TeV','vhbb_Zee_2_13TeV','vhbb_Zmm_1_13TeV','vhbb_Zmm_2_13TeV','vhbb_Znn_1_13TeV','vhbb_Wen_1_13TeV2017','vhbb_Wmn_1_13TeV2017','vhbb_Zee_1_13TeV2017','vhbb_Zee_2_13TeV2017','vhbb_Zmm_1_13TeV2017','vhbb_Zmm_2_13TeV2017','vhbb_Znn_1_13TeV2017']) #Only keep the SR bins
 
#Now let's parse the original full combined datacard that we want to manipulate
cb.ParseDatacard(args.datacard,"vhbb","13TeV","")
cb.bin(['vhbb_Wen_1_13TeV2017','vhbb_Wmn_1_13TeV2017','vhbb_Zee_1_13TeV2017','vhbb_Zee_2_13TeV2017','vhbb_Zmm_1_13TeV2017','vhbb_Zmm_2_13TeV2017','vhbb_Znn_1_13TeV2017']) #Only keep the SR bins
#cb.bin(['vhbb_Wen_1_13TeV','vhbb_Wmn_1_13TeV','vhbb_Zee_1_13TeV','vhbb_Zee_2_13TeV','vhbb_Zmm_1_13TeV','vhbb_Zmm_2_13TeV','vhbb_Znn_1_13TeV','vhbb_Wen_1_13TeV2017','vhbb_Wmn_1_13TeV2017','vhbb_Zee_1_13TeV2017','vhbb_Zee_2_13TeV2017','vhbb_Zmm_1_13TeV2017','vhbb_Zmm_2_13TeV2017','vhbb_Znn_1_13TeV2017']) #Only keep the SR bins

xbins = [-4,-2.25,-1.75,-1.5,-1.25,-1.0,-0.75,-0.5,0]
reorder_hist = ROOT.TH1F('reorder_hist','reorder_hist',8,array('d',xbins))
bin_dict={}
bkg_hist =  ROOT.TH1F()
sig_hist = ROOT.TH1F()

for b in cb_man.bin_set():
  print b
  cb_man_bin = cb_man.cp().bin([b])
  bkg_hist = cb_man.cp().bin([b]).backgrounds().GetShape()
  sig_hist = cb_man.cp().bin([b]).signals().GetShape()
  bin_dict[b] = {}
  for i in range(1,bkg_hist.GetNbinsX()+1):
    print i
    c_sig = sig_hist.GetBinContent(i)
    c_bkg = bkg_hist.GetBinContent(i)
    if c_sig==0 and c_bkg==0:
      c_sb=0
    else:
      c_sb = c_sig/c_bkg
    if c_sb == 0:
      bin_id = 0
    else :
      bin_id = reorder_hist.FindFixBin(math.log10(c_sb))
    if bin_id==0: bin_id=1
    bin_dict[b][i] = bin_id


for b in cb.bin_set():
  cb.cp().bin([b]).ForEachObs(lambda x : ReorderBin(x,bin_dict[b],xbins))
  cb.cp().bin([b]).ForEachProc(lambda x : ReorderBin(x,bin_dict[b],xbins))
  cb.cp().bin([b]).ForEachSyst(lambda x : ReorderBinSystematic(x,bin_dict[b],xbins))


output = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/VH2017/output/vhbb_sbordered_14jul/'
writer=ch.CardWriter(output+"vhbb_2017.txt",
                      output+ "vhbb_input.root")
writer.SetWildcardMasses([])
writer.SetVerbosity(1);

writer.WriteCards("cmb",cb);
