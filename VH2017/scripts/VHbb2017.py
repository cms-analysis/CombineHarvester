#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.VH2017.systematics as systs
import ROOT as R
import glob
import numpy as np
import os
import sys
import argparse

def adjust_shape(proc,nbins):
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1-nbins):
    new_hist.SetBinContent(i,0.)
  proc.set_shape(new_hist,True)


parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='Zll', help="""Which channels to run? Supported options: 'all', 'Znn', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhbb2017', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--auto_rebin', action='store_true', help="""Rebin automatically?""")
parser.add_argument(
 '--bbb_mode', default=1, type=int, help="""Sets the type of bbb uncertainty setup. 0: no bin-by-bins, 1: autoMCStats""")
parser.add_argument(
 '--zero_out_low', action='store_true', help="""Zero-out lowest SR bins (purely for the purpose of making yield tables""")
parser.add_argument(
 '--Zmm_fwk', default='Xbb', help="""Framework the Zmm inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Zee_fwk', default='Xbb', help="""Framework the Zee inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wmn_fwk', default='AT', help="""Framework the Wmn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wen_fwk', default='AT', help="""Framework the Wen inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Znn_fwk', default='AT', help="""Framework the Znn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--year', default='2017', help="""Year to produce datacards for (2017 or 2016)""")


args = parser.parse_args()

cb = ch.CombineHarvester()

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/VH2017/shapes/'

mass = ['125']

chns = []

if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']
if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel  or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel:
  chns.append('Wen')
if 'Znn' in args.channel:
  chns.append('Znn')

year = args.year
if year is not "2016" and not "2017":
  print "Year ", year, " not supported! Choose from: '2016', '2017'"
  sys.exit()

input_fwks = {
  'Wen' : args.Wen_fwk, 
  'Wmn' : args.Wmn_fwk,
  'Zee' : args.Zee_fwk,
  'Zmm' : args.Zmm_fwk,
  'Znn' : args.Znn_fwk
}

for chn in chns:
  if not input_fwks[chn]=='Xbb' and not input_fwks[chn]=='AT':
    print "Framework ", input_fwks[chn], "not supported! Choose from: 'Xbb','AT'"
    sys.exit()

folder_map = {
  'Xbb' : 'Xbb',
  'AT'  : 'AT'
}

input_folders = {
  'Wen' : folder_map[input_fwks['Wen']],
  'Wmn' : folder_map[input_fwks['Wmn']],
  'Zee' : folder_map[input_fwks['Zee']],
  'Zmm' : folder_map[input_fwks['Zmm']],
  'Znn' : folder_map[input_fwks['Znn']] 
}

bkg_procs = {
  'Wen' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Wmn' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Zmm' : ['s_Top','TT','VV','Zj0b','Zj1b','Zj2b'],
  'Zee' : ['s_Top','TT','VV','Zj0b','Zj1b','Zj2b'],
  'Znn' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']
}

sig_procs = {
  'Wen' : ['WH_hbb','ZH_hbb'],
  'Wmn' : ['WH_hbb','ZH_hbb'],
  'Zmm' : ['ZH_hbb','ggZH_hbb'],
  'Zee' : ['ZH_hbb','ggZH_hbb'],
  'Znn' : ['ZH_hbb','WH_hbb']
  #'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb']
}

sig_procs_ren = {
  'Wen' : ['WH_lep','ZH_hbb'],
  'Wmn' : ['WH_lep','ZH_hbb'],
  'Zmm' : ['ZH_hbb','ggZH_hbb'],
  'Zee' : ['ZH_hbb','ggZH_hbb'],
  'Znn' : ['ZH_hbb','ggZH_hbb','WH_lep']
}

cats = {
  'Zee' : [
    (1, 'Zee_BDT_highpt'), (2, 'Zee_BDT_lowpt'), (3, 'Zee_CRZlight_highpt'), (4,'Zee_CRZlight_lowpt'),
    (5, 'Zee_CRZb_highpt'), (6, 'Zee_CRZb_lowpt'), (7,'Zee_CRttbar_highpt'), (8,'Zee_CRttbar_lowpt')
  ],
  'Zmm' : [
    (1, 'Zuu_BDT_highpt'), (2, 'Zuu_BDT_lowpt'), (3, 'Zuu_CRZlight_highpt'), (4,'Zuu_CRZlight_lowpt'),
    (5, 'Zuu_CRZb_highpt'), (6, 'Zuu_CRZb_lowpt'), (7,'Zuu_CRttbar_highpt'), (8,'Zuu_CRttbar_lowpt')
  ],
  'Znn' : [
    (1, 'Znn_13TeV_SIG'), (3, 'Znn_13TeV_ZLF'), (5, 'Znn_13TeV_ZHF'), (7,'Znn_13TeV_TT')
  ],
 'Wen' : [
    (1, 'WenHighPt'), (3,'wlfWen'), (5,'whfWenHigh'), (6,'whfWenLow'), (7,'ttWen')
  ],
 'Wmn' : [
    (1, 'WmnHighPt'), (3,'wlfWmn'), (5,'whfWmnHigh'), (6,'whfWmnLow'), (7,'ttWmn')
  ]

}

for chn in chns:
  cb.AddObservations( ['*'], ['vhbb'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

cb.FilterProcs(lambda x: x.bin_id()==7 and x.channel()=='Znn' and x.process()=='Zj1b')

systs.AddCommonSystematics(cb)
if year=='2016':
  systs.AddSystematics2016(cb)
if year=='2017':
  systs.AddSystematics2017(cb)


if args.bbb_mode==0:
  cb.AddDatacardLineAtEnd("* autoMCStats -1")
elif args.bbb_mode==1:
  cb.AddDatacardLineAtEnd("* autoMCStats 0")


cb.SetGroup('allparams',['.*'])
cb.SetGroup('signal_xs',['pdf_Higgs.*','BR_hbb','QCDscale_ggZH','QCDscale_VH','CMS_vhbb_boost.*'])
cb.SetGroup('bkg_xs',['pdf_qqbar','pdf_gg','CMS_vhbb_VV','CMS_vhbb_ST'])
cb.SetGroup('sim_modelling',['.*LHE_weights.*','CMS_vhbb_ptwweights.*'])
cb.SetGroup('jes',['CMS_scale_j.*'])
cb.SetGroup('jer',['CMS_res_j.*'])
cb.SetGroup('b_eff',['.*bTagWeightJES','.*bTagWeightHFStats.*','.*bTagWeightLF'])
cb.SetGroup('b_fake',['.*bTagWeightLFStats.*','.*bTagWeightHF','.*bTagWeightcErr.*'])
cb.SetGroup('lumi',['lumi_13TeV'])
cb.SetGroup('rateparams',['SF.*'])
#cb.SetGroup('lep_eff',[''])
#cb.SetGroup('met_uncl',[''])

for chn in chns:
  file = shapes + input_folders[chn] + "/vhbb_"+chn+"-"+year+".root"
  if input_fwks[chn] == 'Xbb':
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
      file, '$BIN/$PROCESS', '$BIN/$PROCESS$SYSTEMATIC')
    cb.cp().channel([chn]).signals().ExtractShapes(
      file, '$BIN/$PROCESS', '$BIN/$PROCESS$SYSTEMATIC')
      #file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')
  elif input_fwks[chn] == 'AT':
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).signals().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')


#To rename processes:
#cb.cp().ForEachObj(lambda x: x.set_process("WH_lep") if x.process()=='WH_hbb' else None)

rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(1.0).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

if args.auto_rebin:
  rebin.Rebin(cb, cb)

if args.zero_out_low:
  nbins_to_keep = {'Wen':[[1,5]],'Wmn':[[1,5]],'Znn':[[1,5]],'Zee':[[1,5],[2,3]],'Zmm':[[1,5],[2,3]]}
  for chn in chns:
    for i in range(len(nbins_to_keep[chn])):
      print nbins_to_keep[chn][i]
      cb.cp().channel([chn]).bin_id([nbins_to_keep[chn][i][0]]).ForEachProc(lambda x: adjust_shape(x,nbins_to_keep[chn][i][1]))
      cb.cp().channel([chn]).bin_id([nbins_to_keep[chn][i][0]]).ForEachObs(lambda x: adjust_shape(x,nbins_to_keep[chn][i][1]))

ch.SetStandardBinNames(cb)

writer=ch.CardWriter("output/" + args.output_folder + year + "/$TAG/$BIN"+year+".txt",
                      "output/" + args.output_folder + year +"/$TAG/vhbb_input.root")
writer.SetWildcardMasses([])
writer.SetVerbosity(1);
                
#Combined:
writer.WriteCards("cmb",cb);
writer.WriteCards("cmb_CRonly",cb.cp().bin_id([3,4,5,6,7,8]));

#Per channel:
for chn in chns:
  writer.WriteCards(chn,cb.cp().channel([chn]))

if 'Znn' in chns:
  writer.WriteCards("Znn_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Znn']))

#Zll and Wln:
if 'Wen' in chns and 'Wmn' in chns:
  writer.WriteCards("Wln",cb.cp().channel(['Wen','Wmn']))
  writer.WriteCards("Wln_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Wen','Wmn']))

if 'Zee' in chns and 'Zmm' in chns:
  writer.WriteCards("Zll",cb.cp().channel(['Zee','Zmm']))
  writer.WriteCards("Zll_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Zee','Zmm']))
