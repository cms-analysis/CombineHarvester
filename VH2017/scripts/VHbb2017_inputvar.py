#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.VH2017.systematics_inputVars as systs
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

def drop_zero_procs(chob,proc):
  null_yield = not (proc.rate() > 0.)
  if(null_yield):
    chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return null_yield

def drop_znnqcd(chob,proc):
  drop_process =  proc.process()=='QCD' and proc.channel()=='Znn' and proc.bin_id()==5
  if(drop_process):
    chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return drop_process


def drop_zero_systs(syst):
  null_yield = (not (syst.value_u() > 0. and syst.value_d()>0.) ) and syst.type() in 'shape'
  if(null_yield):
    print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. up norm is ', syst.value_u() , ' and down norm is ', syst.value_d()
    #chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return null_yield


def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal()) 
         and (p.analysis()==s.analysis()) and  (p.era()==s.era()) 
         and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))

def remove_norm_effect(syst):
  syst.set_value_u(1.0)
  syst.set_value_d(1.0)

def symm(syst,nominal):
  print 'Symmetrising systematic ', syst.name(), ' in region ', syst.bin(), ' for process ', syst.process()
  hist_u = syst.ShapeUAsTH1F()
  hist_u.Scale(nominal.Integral()*syst.value_u())
  hist_d = nominal.Clone()
  hist_d.Scale(2)
  hist_d.Add(hist_u,-1)
  syst.set_shapes(hist_u,hist_d,nominal)
  
  
def symmetrise_syst(chob,proc,sys_name):
  nom_hist = proc.ShapeAsTH1F()
  nom_hist.Scale(proc.rate())
  chob.ForEachSyst(lambda s: symm(s,nom_hist) if (s.name()==sys_name and matching_proc(proc,s)) else None)
  

parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='all', help="""Which channels to run? Supported options: 'all', 'Znn', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhbb2017', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--auto_rebin', action='store_true', help="""Rebin automatically?""")
parser.add_argument(
 '--bbb_mode', default=1, type=int, help="""Sets the type of bbb uncertainty setup. 0: no bin-by-bins, 1: autoMCStats""")
parser.add_argument(
 '--zero_out_low', action='store_true', help="""Zero-out lowest SR bins (purely for the purpose of making yield tables""")
parser.add_argument(
 '--Zmm_fwk', default='AT', help="""Framework the Zmm inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Zee_fwk', default='AT', help="""Framework the Zee inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wmn_fwk', default='AT', help="""Framework the Wmn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wen_fwk', default='AT', help="""Framework the Wen inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Znn_fwk', default='AT', help="""Framework the Znn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--year', default='2017', help="""Year to produce datacards for (2017 or 2016)""")
parser.add_argument(
 '--extra_folder', default='', help="""Additional folder where cards are""")
parser.add_argument(
 '--rebinning_scheme', default='', help="""Rebinning scheme for CR and SR distributions""")




args = parser.parse_args()

cb = ch.CombineHarvester()

# uncomment to play with negative bins or large error bins with bin.error > bin.content
# cb.SetFlag('zero-negative-bins-on-import', 1)
# cb.SetFlag('check-large-weights-bins-on-import', 1)
# cb.SetFlag('reduce-large-weights-bins-on-import', 1)

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/VH2017/shapes/'

mass = ['125']

chns = []

if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']
if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel  or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel:# or 'Znn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel:# or 'Znn' in args.channel:
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
  'Xbb' : 'Xbb/'+args.extra_folder,
  'AT'  : 'AT/'+args.extra_folder
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
  'Zmm' : ['s_Top','TT','VVLF','VVHF','Zj0b','Zj1b','Zj2b'],
  'Zee' : ['s_Top','TT','VVLF','VVHF','Zj0b','Zj1b','Zj2b'],
  'Znn' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']
}

sig_procs = {
  'Wen' : ['WH_hbb','ZH_hbb'],
  'Wmn' : ['WH_hbb','ZH_hbb'],
  'Zmm' : ['ZH_hbb','ggZH_hbb'],
  'Zee' : ['ZH_hbb','ggZH_hbb'],
  'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb']
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
    (1, 'SR_high_Zee'), (2, 'SR_low_Zee'), (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
    (5, 'Zhf_high_Zee'), (6, 'Zhf_low_Zee'), (7,'ttbar_high_Zee'), (8,'ttbar_low_Zee')
  ],
  'Zmm' : [
    (1, 'SR_high_Zuu'), (2, 'SR_low_Zuu'), (3, 'Zlf_high_Zuu'), (4,'Zlf_low_Zuu'),
    (5, 'Zhf_high_Zuu'), (6, 'Zhf_low_Zuu'), (7,'ttbar_high_Zuu'), (8,'ttbar_low_Zuu')
  ],
  'Znn' : [
    (1, 'Znn_13TeV_Signal'), (3, 'Znn_13TeV_Zlight'), (5, 'Znn_13TeV_Zbb'), (7,'Znn_13TeV_TT')
  ],
 'Wen' : [
    (1, 'WenHighPt'), (3,'wlfWen'), (5,'whfWenHigh'), (6,'whfWenLow'), (7,'ttWen')
  ],
 'Wmn' : [
    (1, 'WmnHighPt'), (3,'wlfWmn'), (5,'whfWmnHigh'), (6,'whfWmnLow'), (7,'ttWmn')
  ]

}



cats = {
  'Znn' : [
    #(1, 'Znn_mjj_Signal'),(2, 'Znn_btag1_Signal'),(3, 'Znn_btag2_Signal')
    (1, 'Znn_mjj_Signal'),(2, 'Znn_btag1_Signal'),(3, 'Znn_btag2_Signal'),(4, 'Znn_VPT_Signal'),#(5, 'Znn_DNN_Signal'),
    (6,'ZnnTTBtag2'), (7,'ZnnZbbBtag2'), (8,'ZnnZLFBtag2'), (9,'ZnnTTBtag1'), (10,'ZnnZbbBtag1'), (11,'ZnnZLFBtag1')
  ],
  'Zee' : [
    #(1,'SRHIZeeMjj'),(2,'SRLOZeeMjj'),(3,'SRHIZeeBtag1'),(4,'SRLOZeeBtag1'),
    #(4,'SRLOZeeBtag1'),
    (5,'SRHIZeeBtag2')#,(7,'SRHIZeeVPT'),(8,'SRLOZeeVPT'),(9,'SRHIZeeDNN'),(10,'SRLOZeeDNN') 
  ],
  'Zmm' : [
    #(1,'SRHIZmmMjj'),(2,'SRLOZmmMjj'),(3,'SRHIZmmBtag1'),(4,'SRLOZmmBtag1'),(5,'SRHIZmmBtag2'),
    #(6,'SRLOZmmBtag2'),(7,'SRHIZmmVPT'),(8,'SRLOZmmVPT'),(9,'SRHIZmmDNN'),(10,'SRLOZmmDNN') 
    (5,'SRHIZmmBtag2')#,(6,'SRLOZmmBtag2'),(7,'SRHIZmmVPT'),(8,'SRLOZmmVPT'),(9,'SRHIZmmDNN')
  ],
 'Wen' : [
    #(1,'WenHighPtMjj'),(2,'WenHighPtBtag1'),(3,'WenHighPtBtag2'),(4,'WenHighPtVPT'),(5,'WenHighPtDNN')
    (1,'WenHighPtMjj'),(2,'WenHighPtBtag1'),(3,'WenHighPtBtag2'),(10,'ttWenBtag1'),(11,'whfWenLowBtag1'),(12,'whfWenHighBtag1'),(13,'wlfWenBtag1'),(14,'ttWenBtag2'),(15,'whfWenLowBtag2'),(16,'whfWenHighBtag2'),(17,'wlfWenBtag2'),(18,'ttWenMjj'),(19,'whfWenLowMjj'),(20,'whfWenHighMjj'),(21,'wlfWenMjj'),(22,'ttWenVPT'),(23,'whfWenLowVPT'),(24,'whfWenHighVPT'),(25,'wlfWenVPT')#,(5,'WenHighPtDNN')
  ],
 'Wmn' : [
    #(1,'WmnHighPtMjj'),(2,'WmnHighPtBtag1'),(3,'WmnHighPtBtag2'),(4,'WmnHighPtVPT'),(5,'WmnHighPtDNN')
    (1,'WmnHighPtMjj'),(2,'WmnHighPtBtag1'),(3,'WmnHighPtBtag2'),(10,'ttWmnBtag1'),(11,'whfWmnLowBtag1'),(12,'whfWmnHighBtag1'),(13,'wlfWmnBtag1'),(14,'ttWmnBtag2'),(15,'whfWmnLowBtag2'),(16,'whfWmnHighBtag2'),(17,'wlfWmnBtag2'),(18,'ttWmnMjj'),(19,'whfWmnLowMjj'),(20,'whfWmnHighMjj'),(21,'wlfWmnMjj'),(22,'ttWmnVPT'),(23,'whfWmnLowVPT'),(24,'whfWmnHighVPT'),(25,'wlfWmnVPT')#,(5,'WmnHighPtDNN')
  ]
}


if args.rebinning_scheme == 'v2-wh-hf-dnn' or args.rebinning_scheme == 'v2-whznnh-hf-dnn':
    cats['Wen'] = [ (1, 'WenHighPt'), (3,'wlfWen'), (6,'whfWenLow'), (7,'ttWen') ]
    cats['Wmn'] = [ (1, 'WmnHighPt'), (3,'wlfWmn'), (6,'whfWmnLow'), (7,'ttWmn') ]

for chn in chns:
  cb.AddObservations( ['*'], ['vhbb'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

#cb.FilterProcs(lambda x: x.bin_id()==7 and x.channel()=='Znn' and x.process()=='Zj1b')
cb.FilterProcs(lambda x: x.bin_id()==1 and x.channel()=='Znn' and x.process()=='QCD')

systs.AddCommonSystematics(cb)
if year=='2016':
  systs.AddSystematics2016(cb)
if year=='2017':
  systs.AddSystematics2017(cb)


if args.bbb_mode==0:
  cb.AddDatacardLineAtEnd("* autoMCStats -1")
elif args.bbb_mode==1:
  cb.AddDatacardLineAtEnd("* autoMCStats 0")



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

# play with rebinning (and/or cutting) of the shapes
if args.rebinning_scheme == 'v1': # Zll only: 1bin in TT/LF, 2bins in HF
    binning=np.linspace(0.0,1.0,num=2)
    print 'binning in CR for LF,TT fitting variable:',binning,'for channels',['Zee','Zmm']
    cb.cp().channel(['Zee','Zmm']).bin_id([3,4,7,8]).VariableRebin(binning)
    binning=np.linspace(0.0,1.0,num=3)
    print 'binning in CR for HF fitting variable:',binning,'for channels',['Zee','Zmm']
    cb.cp().channel(['Zee','Zmm']).bin_id([5,6]).VariableRebin(binning)

elif args.rebinning_scheme == 'v2': # all channels: 1bin in TT/LF, 2bins in HF
    binning=np.linspace(0.0,1.0,num=2)
    print 'binning in CR for LF,TT fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([3,4,7,8]).VariableRebin(binning)
    binning=np.linspace(0.0,1.0,num=3)
    print 'binning in CR for HF fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([5,6]).VariableRebin(binning)
    
elif args.rebinning_scheme == 'v2-wh-hf-dnn': # all channels: 1bin in TT/LF, 2bins in HF
    binning=np.linspace(0.0,1.0,num=2)
    print 'binning in CR for LF,TT fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([3,4,7,8]).VariableRebin(binning)
    binning=np.linspace(0.0,1.0,num=3)
    print 'binning in CR for HF fitting variable:',binning,'for all Zll and Znn channels'
    cb.cp().channel(['Zee','Zmm','Znn']).bin_id([5,6]).VariableRebin(binning)
    binning=np.linspace(0.0,5.0,num=6)
    print 'binning in CR for HF fitting variable:',binning,'for all the channels'
    cb.cp().channel(['Wmn','Wen']).bin_id([5,6]).VariableRebin(binning) 
   
elif args.rebinning_scheme == 'v2-whznnh-hf-dnn': # all channels: 1bin in TT/LF, 2bins in HF
    binning=np.linspace(0.0,1.0,num=2)
    print 'binning in CR for LF,TT fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([3,4,7,8]).VariableRebin(binning)
    binning=np.linspace(0.0,1.0,num=3)
    print 'binning in CR for HF fitting variable:',binning,'for all Zll and Znn channels'
    cb.cp().channel(['Zee','Zmm']).bin_id([5,6]).VariableRebin(binning)
    binning=np.linspace(0.0,5.0,num=6)
    print 'binning in CR for HF fitting variable:',binning,'for all the channels'
    cb.cp().channel(['Wmn','Wen','Znn']).bin_id([5,6]).VariableRebin(binning) 
   
elif args.rebinning_scheme == 'v3': # all channels: 1bin in TT/LF, no rebin in HF
    binning=np.linspace(0.0,1.0,num=2)
    print 'binning in CR for LF,TT fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([3,4,7,8]).VariableRebin(binning)
    
elif args.rebinning_scheme == 'v4': # all channels: 1bin in TT/LF, no rebin in HF
    binning=np.linspace(0.0,1.0,num=3)
    print 'binning in CR for LF,TT fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([3,4,7,8]).VariableRebin(binning)
    binning=np.linspace(0.0,1.0,num=5)
    print 'binning in CR for HF fitting variable:',binning,'for all the channels'
    cb.cp().bin_id([5,6]).VariableRebin(binning)
    
elif args.rebinning_scheme == 'sr_mva_cut_2bins': # HIG-16-044 style
    binning=np.linspace(0.2,1.0,num=13)
    print 'binning in SR for fitting variable:',binning
    cb.cp().bin_id([1,2]).VariableRebin(binning)


cb.FilterProcs(lambda x: drop_zero_procs(cb,x))
cb.FilterSysts(lambda x: drop_zero_systs(x))
#Drop QCD in Z+HF CR
cb.FilterProcs(lambda x: drop_znnqcd(cb,x))

if year=='2016':
    cb.cp().syst_name(["CMS_res_j_13TeV_2016"]).ForEachProc(lambda x:symmetrise_syst(cb,x,'CMS_res_j_13TeV_2016'))


if year=='2017':
    cb.cp().ForEachSyst(lambda x: remove_norm_effect(x) if x.name()=='CMS_vhbb_puWeight' else None)

cb.SetGroup('signal_theory',['pdf_Higgs.*','BR_hbb','QCDscale_ggZH','QCDscale_VH','CMS_vhbb_boost.*','.*LHE_weights.*ZH.*','.*LHE_weights.*WH.*','.*LHE_weights.*ggZH.*'])
cb.SetGroup('bkg_theory',['pdf_qqbar','pdf_gg','CMS_vhbb_VV','CMS_vhbb_ST','.*LHE_weights.*TT.*','.*LHE_weights.*VV.*','.*LHE_weights.*Zj0b.*','LHE_weights.*Zj1b.*','LHE_weights.*Zj2b.*','LHE_weights.*Wj0b.*','LHE_weights.*Wj1b.*','LHE_weights.*Wj2b.*','LHE_weights.*s_Top.*','LHE_weights.*QCD.*'])
cb.SetGroup('sim_modelling',['CMS_vhbb_ptwweights.*'])
cb.SetGroup('jes',['CMS_scale_j.*'])
cb.SetGroup('jer',['CMS_res_j.*'])
cb.SetGroup('btag',['.*bTagWeight.*JES.*','.*bTagWeight.*HFStats.*','.*bTagWeight.*LF_.*','.*bTagWeight.*cErr.*'])
cb.SetGroup('mistag',['.*bTagWeight.*LFStats.*','.*bTagWeight.*HF_.*'])
cb.SetGroup('lumi',['lumi_13TeV','.*puWeight.*'])
cb.SetGroup('lep_eff',['.*eff_e.*','.*eff_m.*'])
cb.SetGroup('met',['.*MET.*'])



#To rename processes:
#cb.cp().ForEachObj(lambda x: x.set_process("WH_lep") if x.process()=='WH_hbb' else None)

rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(1.0).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

#binning=np.linspace(0.2,1.0,num=13)
#print binning


if args.auto_rebin:
  rebin.Rebin(cb, cb)

if args.zero_out_low:
  range_to_drop = {'Wen':[[1,0,0.5]],'Wmn':[[1,0,0.5]],'Znn':[[1,0,0.5]],'Zee':[[1,0,0.5],[2,0,0.5]],'Zmm':[[1,0,0.5],[2,0,0.5]]} #First number is bin_id, second number lower bound of range to drop, third number upper bound of range to drop
  for chn in chns:
    for i in range(len(range_to_drop[chn])):
      cb.cp().channel([chn]).bin_id([range_to_drop[chn][i][0]]).ZeroBins(range_to_drop[chn][i][1],range_to_drop[chn][i][2])

ch.SetStandardBinNames(cb)

writer=ch.CardWriter("output/" + args.output_folder + year + "/$TAG/$BIN"+year+".txt",
                      "output/" + args.output_folder + year +"/$TAG/vhbb_input_$BIN"+year+".root")
writer.SetWildcardMasses([])
writer.SetVerbosity(0);
                
#Combined:
writer.WriteCards("cmb",cb);
writer.WriteCards("cmb_CRonly",cb.cp().bin_id([3,4,5,6,7,8]));

#Per channel:
for chn in chns:
  writer.WriteCards(chn,cb.cp().channel([chn]))

if 'Znn' in chns:
  #writer.WriteCards("Znn",cb.cp().FilterAll(lambda x: not (x.channel()=='Znn' or ( (x.channel() in ['Wmn','Wen']) and x.bin_id() in [3,4,5,6,7,8]))))
  writer.WriteCards("Znn",cb.cp().channel(['Znn']))
  writer.WriteCards("Znn",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Wmn','Wen']))
  writer.WriteCards("Znn_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Znn','Wmn','Wen']))

#Zll and Wln:
if 'Wen' in chns and 'Wmn' in chns:
  writer.WriteCards("Wln",cb.cp().channel(['Wen','Wmn']))
  writer.WriteCards("Wln_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Wen','Wmn']))

if 'Zee' in chns and 'Zmm' in chns:
  writer.WriteCards("Zll",cb.cp().channel(['Zee','Zmm']))
  writer.WriteCards("Zll_CRonly",cb.cp().bin_id([3,4,5,6,7,8]).channel(['Zee','Zmm']))
