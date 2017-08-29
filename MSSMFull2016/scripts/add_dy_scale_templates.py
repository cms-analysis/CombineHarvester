import ROOT
import argparse
import os
import fnmatch

cmssw_base=os.environ['CMSSW_BASE']
up_name = 'ZTT_CMS_htt_QCDScale_13TeVUp' 
down_name = 'ZTT_CMS_htt_QCDScale_13TeVDown'

parser = argparse.ArgumentParser()
parser.add_argument('--groups', '-g', help= 'Names of groups where ZTT scale templates will be added (seperate by commas) e.g Imperial,KIT,Vienna,DESY')
args = parser.parse_args()
groups=args.groups.split(',')
chns = ['em', 'mt', 'tt', 'et']
cats = ['et_nobtag_tight','et_btag_tight','et_nobtag_loosemt','et_btag_loosemt','em_nobtag_lowPzeta','em_btag_lowPzeta','em_nobtag_mediumPzeta','em_btag_mediumPzeta','em_nobtag_highPzeta','em_btag_highPzeta','tt_nobtag','tt_btag','mt_nobtag_tight','mt_btag_tight','mt_nobtag_loosemt','mt_btag_loosemt']

datacard_files = []
# get all LO and NLO datacard files for all specified groups
for g in groups:
  lo_cards = os.listdir(cmssw_base+'/src/CombineHarvester/MSSMFull2016/shapes/'+g+'/')
  nlo_cards = os.listdir(cmssw_base+'/src/CombineHarvester/MSSMFull2016/shapes/'+g+'/NLO/')
  lo_matching = fnmatch.filter(lo_cards, 'htt_*.inputs-mssm-13TeV-mttot.root')  
  nlo_matching = fnmatch.filter(nlo_cards, 'htt_*.inputs-mssm-13TeV-mttot.root')
  for i in lo_matching: 
    if any('_'+c+'.' in i for c in chns): datacard_files.append(cmssw_base+'/src/CombineHarvester/MSSMFull2016/shapes/'+g+'/'+i)    
  for i in nlo_matching: 
    if any('_'+c+'.' in i for c in chns): datacard_files.append(cmssw_base+'/src/CombineHarvester/MSSMFull2016/shapes/'+g+'/NLO/'+i) 

infilename = cmssw_base+'/src/CombineHarvester/MSSMFull2016/input/ztt_scale_uncerts.root'
dy_systs_infile = ROOT.TFile(infilename)

for f in datacard_files:
  datacards_file = ROOT.TFile(f,"UPDATE")
  for c in cats:
     nom_hist = datacards_file.Get(c+'/ZTT')
     if not datacards_file.GetDirectory(c): continue
     # multiply nominal ZTT by relative uncertainties to get up and down templates
     h_up = dy_systs_infile.Get(c+'_up')
     h_down = dy_systs_infile.Get(c+'_down')
     h_up.Multiply(nom_hist)
     h_down.Multiply(nom_hist)
     # normalize up and down histogram to the nominal
     h_up.Scale(nom_hist.Integral(-1,-1)/h_up.Integral(-1,-1))
     h_down.Scale(nom_hist.Integral(-1,-1)/h_down.Integral(-1,-1))
     h_up.SetName(up_name);
     h_down.SetName(down_name);
     datacards_file.cd(c)
     h_up.Write('',ROOT.TObject.kOverwrite)
     h_down.Write('',ROOT.TObject.kOverwrite)
     datacards_file.cd()
  datacards_file.Close()
dy_systs_infile.Close()