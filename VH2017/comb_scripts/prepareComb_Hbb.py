import CombineHarvester.CombineTools.ch as ch
import ROOT
import os
import pprint
import argparse
from collections import defaultdict
# import sys
import re

from subprocess import *
def processCmd(cmd, quiet = 0):
    output = ''
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
    p.stdout.close()
    return output

def ForEachProcAndSyst(cb, func):
    cb.ForEachProc(func)
    cb.ForEachSyst(func)

def drop_zero_procs(chob,proc):
  null_yield = not (proc.rate() > 0.)
  if(null_yield):
    print 'dropping process ', proc,' and associated systematics' 
    chob.FilterSysts(lambda sys: matching_proc(proc,sys))
  return null_yield

def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal())
         and (p.analysis()==s.analysis()) and  (p.era()==s.era())
         and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))

parser = argparse.ArgumentParser()
parser.add_argument( '-i', help='path to cadi directory in cmshcg svn', default='./')
parser.add_argument( '--ttH', help='only run ttH channels', action='store_true', default=False)
parser.add_argument( '--stats-mode', help='which type of autoMCStats card to produce', default=2, type=int)
parser.add_argument( '--diagnostics', help='Print diagnostic info about the model', action='store_true')
parser.add_argument( '--postfix', help='Postfix string for output', default='')

args = parser.parse_args()
postfix = args.postfix
ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

cb = ch.CombineHarvester()
cb.SetFlag('workspace-uuid-recycle', True)
cb.SetFlag('workspaces-use-clone', True)
cb.SetFlag('import-parameter-err', False)
cb.SetFlag('filters-use-regex', True)
cb.SetFlag("zero-negative-bins-on-import", False)
cb.SetFlag("check-negative-bins-on-import", False)

cb.SetVerbosity(0)

vhbb_pre = os.path.join(
    args.i, 'vhbb/125/forSTXS_Stage0/')
vhbb_cards = {
'vhbb_2016_13TeV_STXSStage0.txt':'cat_vhbb_13TeV'
}

vhbb_2017_pre = os.path.join(
    args.i, 'vhbb_2017/')
vhbb_2017_cards = {
'combined.txt.cmb':'cat_vhbb_13TeV_2017'
}

vhbb_run1_pre = os.path.join(
    args.i, 'vhbb_run1/')
vhbb_run1_cards = {
'vhbb_7plus8TeV.txt':'cat_vhbb_7TeV8TeV'
}

tth_hbb_leptonic_pre = os.path.join(
    # args.i, 'tth_hbb_leptonic/125/')
    args.i, 'tth_hbb_leptonic/125/cards_ttH_hbb_leptonic_with_tHW_tHq_SM/')
tth_hbb_leptonic_cards = {
    'combined_ttH_hbb_13TeV.txt':'cat_ttH_hbb_leptonic',
}

tth_hbb_hadronic_pre = os.path.join(
    args.i, 'tth_hbb_hadronic/125/tHW_SMxsec/')
tth_hbb_hadronic_cards = {
    'shapes_group_group_fh_forcomb.txt':'cat_ttH_hbb_hadronic',
}

tth_run1_pre = os.path.join(
    args.i, 'tth_run1/')
tth_run1_cards = {
#    'combined.txt':'cat_ttH_run1',
    'test.txt':'cat_ttH_run1',
}

ggHbb_pre = os.path.join(
    args.i, 'ggHbb/125/v2/')
ggHbb_cards = {
    'card_rhalphabet_muonCR.txt':'cat_boosted_hbb',
}

vbfbb_run1_pre = os.path.join(
    args.i, 'vbfbb_run1/125/')
vbfbb_run1_cards = {
'vbfbb_8TeV.txt':'cat_vbfbb_8TeV'
}


print "All Cards: "
cards = ' '.join(
    [vhbb_pre + card + '\n' for card,cat in vhbb_cards.iteritems()] +
    [vhbb_2017_pre + card + '\n' for card,cat in vhbb_2017_cards.iteritems()] +
    [vhbb_run1_pre + card + '\n' for card,cat in vhbb_run1_cards.iteritems()] +
    [tth_hbb_leptonic_pre + card + '\n' for card,cat in tth_hbb_leptonic_cards.iteritems()] +
    [tth_hbb_hadronic_pre + card + '\n' for card,cat in tth_hbb_hadronic_cards.iteritems()] +
    [tth_run1_pre + card + '\n' for card,cat in tth_run1_cards.iteritems()] +
    [ggHbb_pre + card + '\n' for card,cat in ggHbb_cards.iteritems()] +
    [vbfbb_run1_pre + card + '\n' for card,cat in vbfbb_run1_cards.iteritems()] 
)
print cards

print '>> Parsing tth_hbb_leptonic cards'
for card,cat in tth_hbb_leptonic_cards.iteritems():
    cb.ParseDatacard(tth_hbb_leptonic_pre + card, analysis='comb', channel='tth_hbb_leptonic', mass='125')

print '>> Parsing tth_hbb_hadronic cards'
for card,cat in tth_hbb_hadronic_cards.iteritems():
    cb.ParseDatacard(tth_hbb_hadronic_pre + card, analysis='comb', channel='tth_hbb_hadronic', mass='125')

print '>> Parsing vhbb cards'
for card,cat in vhbb_cards.iteritems():
    cb.ParseDatacard(vhbb_pre + card, analysis='comb', channel='vhbb', mass='125')

print '>> Parsing vhbb_2017 cards'
for card,cat in vhbb_2017_cards.iteritems():
    cb.ParseDatacard(vhbb_2017_pre + card, analysis='comb', channel='vhbb_2017', mass='125')

print '>> Parsing vhbb_run1 cards'
for card,cat in vhbb_run1_cards.iteritems():
    cb.ParseDatacard(vhbb_run1_pre + card, analysis='comb', channel='vhbb_run1', mass='125')

print '>> Parsing ggHbb cards'
for card,cat in ggHbb_cards.iteritems():
    cb.ParseDatacard(ggHbb_pre + card, analysis='comb', channel='ggHbb', mass='125')

print '>> Parsing tth_run1 cards'
for card,cat in tth_run1_cards.iteritems():
    # Need to take the cards with mass 125.1 GeV
    cb.ParseDatacard(tth_run1_pre + card, analysis='comb', channel='tth_run1', mass='125.1')

print '>> Parsing vbfbb_run1 cards'
for card,cat in vbfbb_run1_cards.iteritems():
    # Need to take the cards with mass 125.1 GeV
    cb.ParseDatacard(vbfbb_run1_pre + card, analysis='comb', channel='vbfbb_run1', mass='125')

# Only ttHbb categories
print '>> Dropping tth_run1 bins that are not h->bb:'
pprint.pprint(cb.cp().channel(['tth_run1']).bin_set(), indent=4)
cb.FilterAll(lambda x: x.channel() == 'tth_run1' and not ('ttH_7TeV' in x.bin() or 'ttH_hbb_8TeV' in x.bin()))
pprint.pprint(cb.cp().channel(['tth_run1']).bin_set(), indent=4)

# Fix process names for tHq and tHW in tth_hbb_leptonic
ForEachProcAndSyst(cb.cp().channel(['tth_hbb_leptonic']).process(['^tH(q|W)_hbb$']), lambda x: x.set_signal(True))

# Fix process names for tHq and tHW in tth_hbb_hadronic
ForEachProcAndSyst(cb.cp().channel(['tth_hbb_hadronic']).process(['^tH(q|W)$']), lambda x: x.set_signal(True))
ForEachProcAndSyst(cb.cp().channel(['tth_hbb_hadronic']).process(['^tH(q|W)$']), lambda x: x.set_process(x.process()+'_hbb'))

def FlipAsymLogNormal(x):
    if x.asymm():
        val_d = x.value_d()
        val_u = x.value_u()
        x.set_value_d(val_u)
        x.set_value_u(val_d)
    else:
        x.set_value_u(1./x.value_u())

cb_hbb_flip = cb.cp().channel(['tth_hbb_hadronic', 'tth_hbb_leptonic']).syst_name([
    'pdf_gg'
])
cb_hbb_flip.ForEachSyst(FlipAsymLogNormal)

# Fix pdf_Higgs_qg in tth_hbb_leptonic - FIXME
# cb.FilterSysts(lambda x: x.channel() == 'tth_hbb_leptonic' and x.name() == 'pdf_Higgs_qg')
# cb.cp().channel(['tth_hbb_leptonic']).process(['tHq_hbb']).AddSyst(cb, 'pdf_Higgs_tHq', 'lnN', ch.SystMap()(1.037))
# cb.cp().channel(['tth_hbb_leptonic']).process(['tHW_hbb']).AddSyst(cb, 'pdf_Higgs_tHW', 'lnN', ch.SystMap()(1.063))
# cb.cp().channel(['tth_hbb_leptonic']).process(['tHq_hbb']).AddSyst(cb, 'QCDscale_tHq', 'lnN', ch.SystMap()([0.851,1.065]))
# cb.cp().channel(['tth_hbb_leptonic']).process(['tHW_hbb']).AddSyst(cb, 'QCDscale_tHW', 'lnN', ch.SystMap()([0.933,1.049]))

# Fix pdf_Higgs_qqbar in vhbb
cb.FilterSysts(lambda x: x.channel() == 'vhbb' and x.name() == 'pdf_Higgs_qqbar')
cb.cp().channel(['vhbb']).process(['ZH_lep_hbb']).AddSyst(cb, 'pdf_Higgs_qqbar', 'lnN', ch.SystMap()(1.016))
cb.cp().channel(['vhbb']).process(['WH_lep_hbb']).AddSyst(cb, 'pdf_Higgs_qqbar', 'lnN', ch.SystMap()(1.019))

#Remove QCDScale_VV from  vhbb (double counting)
cb.FilterSysts(lambda x: x.channel() == 'vhbb' and x.name() == 'QCDscale_VV')

# Fix names in vhbb_run1
cb.cp().channel(['vhbb_run1']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^WH$","WH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_run1']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^WH$","WH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_run1']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^ZH$","ZH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_run1']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^ZH$","ZH_lep_hbb",x.process()))
    )

# Fix names in vbfbb_run1
cb.cp().channel(['vbfbb_run1']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^ggH$","ggH_hbb",x.process()))
    )
cb.cp().channel(['vbfbb_run1']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^ggH$","ggH_hbb",x.process()))
    )
cb.cp().channel(['vbfbb_run1']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^qqH$","qqH_hbb",x.process()))
    )
cb.cp().channel(['vbfbb_run1']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^qqH$","qqH_hbb",x.process()))
    )

# Fix names in vhbb_2017
cb.cp().channel(['vhbb_2017']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^WH_hbb$","WH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_2017']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^WH_hbb$","WH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_2017']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^ZH_hbb$","ZH_lep_hbb",x.process()))
    )
cb.cp().channel(['vhbb_2017']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^ZH_hbb$","ZH_lep_hbb",x.process()))
    )

# Fix names in ggHbb
cb.cp().channel(['ggHbb']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^hqq125$","ggH_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^hqq125$","ggH_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^vbfhqq125$","qqH_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^vbfhqq125$","qqH_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^whqq125$","WH_had_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^whqq125$","WH_had_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^zhqq125$","ZH_had_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^zhqq125$","ZH_had_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachProc(
    lambda x: x.set_process(re.sub("^tthqq125$","ttH_hbb",x.process()))
    )
cb.cp().channel(['ggHbb']).signals().ForEachSyst(
    lambda x: x.set_process(re.sub("^tthqq125$","ttH_hbb",x.process()))
    )

#scale 125.09/125.0
fxs = ROOT.TFile("$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/sm_yr4_13TeV.root","READ")
wxs = fxs.Get("xs_13TeV")
fbr = ROOT.TFile("$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/sm_br_yr4.root","READ")
wbr = fbr.Get("br")

mhscal_systmap = ch.SystMap('process')
# Define the processes we will add the rateParams to
mhscal_cb = cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1'], False).signals()
mhscal_sigs = mhscal_cb.process_set()

for sig in mhscal_sigs:
    xs = sig.split("_")[0]
    br = sig.split("_")[-1]
    if (xs=="qqH"): xs="vbfH"

    if (xs=="tHW" or xs=="tHq"):
        xsscal=1.0
    else:
        wxs.var("MH").setVal(125.0)
        xsden = wxs.function(xs + "_13TeV").getVal()
        wxs.var("MH").setVal(125.09)
        xsnum = wxs.function(xs + "_13TeV").getVal()
        xsscal = xsnum / xsden

    if (br=="hinv"):
        brscal=1.0
    else:
        print br
        wbr.var("MH").setVal(125.0)
        brden = wbr.function(br).getVal()
        wbr.var("MH").setVal(125.09)
        brnum = wbr.function(br).getVal()
        brscal = brnum / brden

    print sig, xsscal, brscal
    mhscal_systmap([sig], round(xsscal * brscal, 3))

mhscal_cb.AddSyst(cb, 'mhscal_$PROCESS', 'rateParam', mhscal_systmap)

for sig in mhscal_sigs:
    par = cb.GetParameter('mhscal_' + sig)
    par.set_frozen(True)
    par.set_range(par.val(), par.val())


# Drop systematics
drop = [
'CMS_ggH_PDF',
'CMS_qqH_PDF',
'CMS_qqH_QCDUnc',
]
for name in drop:
  cb.syst_name([name], False)


# Rename Systematics
rename = {
'CMS_vhbb_res_j_13TeV' : 'CMS_res_j_13TeV',
'CMS_scale_j_13TeV' : 'CMS_scale_j_13TeV',
'CMS_scaleAbsoluteMPFBias_j' : 'CMS_scale_j_AbsoluteMPFBias_13TeV',
'CMS_scaleAbsoluteScale_j' : 'CMS_scale_j_AbsoluteScale_13TeV',
'CMS_scaleAbsoluteStat_j' : 'CMS_scale_j_AbsoluteStat_13TeV',
'CMS_scaleFlavorQCD_j' : 'CMS_scale_j_FlavorQCD_13TeV',
'CMS_scaleFragmentation_j' : 'CMS_scale_j_Fragmentation_13TeV',
'CMS_scalePileUpDataMC_j' : 'CMS_scale_j_PileUpDataMC_13TeV',
'CMS_scalePileUpPtBB_j' : 'CMS_scale_j_PileUpPtBB_13TeV',
'CMS_scalePileUpPtEC1_j' : 'CMS_scale_j_PileUpPtEC1_13TeV',
'CMS_scalePileUpPtEC2_j' : 'CMS_scale_j_PileUpPtEC2_13TeV',
'CMS_scalePileUpPtHF_j' : 'CMS_scale_j_PileUpPtHF_13TeV',
'CMS_scalePileUpPtRef_j' : 'CMS_scale_j_PileUpPtRef_13TeV',
'CMS_scaleRelativeBal_j' : 'CMS_scale_j_RelativeBal_13TeV',
'CMS_scaleRelativeFSR_j' : 'CMS_scale_j_RelativeFSR_13TeV',
'CMS_scaleRelativeJEREC1_j' : 'CMS_scale_j_RelativeJEREC1_13TeV',
'CMS_scaleRelativeJEREC2_j' : 'CMS_scale_j_RelativeJEREC2_13TeV',
'CMS_scaleRelativeJERHF_j' : 'CMS_scale_j_RelativeJERHF_13TeV',
'CMS_scaleRelativePtBB_j' : 'CMS_scale_j_RelativePtBB_13TeV',
'CMS_scaleRelativePtEC1_j' : 'CMS_scale_j_RelativePtEC1_13TeV',
'CMS_scaleRelativePtEC2_j' : 'CMS_scale_j_RelativePtEC2_13TeV',
'CMS_scaleRelativePtHF_j' : 'CMS_scale_j_RelativePtHF_13TeV',
'CMS_scaleRelativeStatEC_j' : 'CMS_scale_j_RelativeStatEC_13TeV',
'CMS_scaleRelativeStatFSR_j' : 'CMS_scale_j_RelativeStatFSR_13TeV',
'CMS_scaleRelativeStatHF_j' : 'CMS_scale_j_RelativeStatHF_13TeV',
'CMS_scaleSinglePionECAL_j' : 'CMS_scale_j_SinglePionECAL_13TeV',
'CMS_scaleSinglePionHCAL_j' : 'CMS_scale_j_SinglePionHCAL_13TeV',
'CMS_scaleTimePtEta_j' : 'CMS_scale_j_TimePtEta_13TeV',
'CMS_vhbb_scale_j_AbsoluteMPFBias_13TeV' : 'CMS_scale_j_AbsoluteMPFBias_13TeV',
'CMS_vhbb_scale_j_AbsoluteScale_13TeV' : 'CMS_scale_j_AbsoluteScale_13TeV',
'CMS_vhbb_scale_j_AbsoluteStat_13TeV' : 'CMS_scale_j_AbsoluteStat_13TeV',
'CMS_vhbb_scale_j_FlavorQCD_13TeV' : 'CMS_scale_j_FlavorQCD_13TeV',
'CMS_vhbb_scale_j_Fragmentation_13TeV' : 'CMS_scale_j_Fragmentation_13TeV',
'CMS_vhbb_scale_j_PileUpDataMC_13TeV' : 'CMS_scale_j_PileUpDataMC_13TeV',
'CMS_vhbb_scale_j_PileUpPtBB_13TeV' : 'CMS_scale_j_PileUpPtBB_13TeV',
'CMS_vhbb_scale_j_PileUpPtEC1_13TeV' : 'CMS_scale_j_PileUpPtEC1_13TeV',
'CMS_vhbb_scale_j_PileUpPtEC2_13TeV' : 'CMS_scale_j_PileUpPtEC2_13TeV',
'CMS_vhbb_scale_j_PileUpPtRef_13TeV' : 'CMS_scale_j_PileUpPtRef_13TeV',
'CMS_vhbb_scale_j_RelativeFSR_13TeV' : 'CMS_scale_j_RelativeFSR_13TeV',
'CMS_vhbb_scale_j_RelativeJEREC1_13TeV' : 'CMS_scale_j_RelativeJEREC1_13TeV',
'CMS_vhbb_scale_j_RelativePtBB_13TeV' : 'CMS_scale_j_RelativePtBB_13TeV',
'CMS_vhbb_scale_j_RelativePtEC1_13TeV' : 'CMS_scale_j_RelativePtEC1_13TeV',
'CMS_vhbb_scale_j_RelativePtEC2_13TeV' : 'CMS_scale_j_RelativePtEC2_13TeV',
'CMS_vhbb_scale_j_RelativeStatEC_13TeV' : 'CMS_scale_j_RelativeStatEC_13TeV',
'CMS_vhbb_scale_j_RelativeStatFSR_13TeV' : 'CMS_scale_j_RelativeStatFSR_13TeV',
'CMS_vhbb_scale_j_SinglePionECAL_13TeV' : 'CMS_scale_j_SinglePionECAL_13TeV',
'CMS_vhbb_scale_j_SinglePionHCAL_13TeV' : 'CMS_scale_j_SinglePionHCAL_13TeV',
'CMS_vhbb_scale_j_TimePtEta_13TeV' : 'CMS_scale_j_TimePtEta_13TeV',
'CMS_scale_met_clustered_13TeV' : 'CMS_scale_met',
'CMS_THU_ggH_Mig01' : 'THU_ggH_Mig01',
'CMS_THU_ggH_Mig12' : 'THU_ggH_Mig12',
'CMS_THU_ggH_Mu' : 'THU_ggH_Mu',
'CMS_THU_ggH_PT120' : 'THU_ggH_PT120',
'CMS_THU_ggH_PT60' : 'THU_ggH_PT60',
'CMS_THU_ggH_Res' : 'THU_ggH_Res',
'CMS_THU_ggH_VBF2j' : 'THU_ggH_VBF2j',
'CMS_THU_ggH_VBF3j' : 'THU_ggH_VBF3j',
'CMS_THU_ggH_qmtop' : 'THU_ggH_qmtop',
'CMS_hgg_THU_ggH_Mig01' : 'THU_ggH_Mig01',
'CMS_hgg_THU_ggH_Mig12' : 'THU_ggH_Mig12',
'CMS_hgg_THU_ggH_Mu' : 'THU_ggH_Mu',
'CMS_hgg_THU_ggH_PT120' : 'THU_ggH_PT120',
'CMS_hgg_THU_ggH_PT60' : 'THU_ggH_PT60',
'CMS_hgg_THU_ggH_Res' : 'THU_ggH_Res',
'CMS_hgg_THU_ggH_VBF2j' : 'THU_ggH_VBF2j',
'CMS_hgg_THU_ggH_VBF3j' : 'THU_ggH_VBF3j',
'CMS_hgg_THU_ggH_qmtop' : 'THU_ggH_qmtop',
'THU_ggH_Mig01_13TeV' : 'THU_ggH_Mig01',
'THU_ggH_Mig12_13TeV' : 'THU_ggH_Mig12',
'THU_ggH_Mu_13TeV' : 'THU_ggH_Mu',
'THU_ggH_PT120_13TeV' : 'THU_ggH_PT120',
'THU_ggH_PT60_13TeV' : 'THU_ggH_PT60',
'THU_ggH_Res_13TeV' : 'THU_ggH_Res',
'THU_ggH_VBF2j_13TeV' : 'THU_ggH_VBF2j',
'THU_ggH_VBF3j_13TeV' : 'THU_ggH_VBF3j',
'THU_ggH_qmtop_13TeV' : 'THU_ggH_qmtop',
'QCDscale_ggH' : 'THU_ggH_Mu',
'QCDscale_WH' : 'QCDscale_VH',
'QCDscale_ZH' : 'QCDscale_VH',
'lumi_13TeV' : 'lumi_13TeV_2016',
'CMS_pu' : 'CMS_PU',
'CMS_ttH_PU' : 'CMS_PU',
'CMS_vhbb_puWeight' : 'CMS_PU',
'Pu':'CMS_PU',
'JES':'CMS_scale_j_13TeV',
'JER':'CMS_res_j_13TeV',
'lumi':'lumi_13TeV_2016',
'CMS_btag_heavy':'CMS_eff_b',
'CMS_btag_hf':'CMS_btag_CSV_HF',
'CMS_btag_hfstats1': 'CMS_btag_CSV_HF_stats1',
'CMS_btag_hfstats2':'CMS_btag_CSV_HF_stats2',
'CMS_btag_lf': 'CMS_btag_CSV_LF',
'CMS_btag_lfstats1':'CMS_btag_CSV_LF_stats1',
'CMS_btag_lfstats2':'CMS_btag_CSV_LF_stats2',
'CMS_btag_cferr1':'CMS_btag_CSV_Err1',
'CMS_btag_cferr2':'CMS_btag_CSV_Err2',
'CMS_ttH_CSVhf':'CMS_btag_CSV_HF',
'CMS_ttH_CSVhfstats1':'CMS_btag_CSV_HF_stats1',
'CMS_ttH_CSVhfstats2':'CMS_btag_CSV_HF_stats2',
'CMS_ttH_CSVlf':'CMS_btag_CSV_LF', 
'CMS_ttH_CSVlfstats1':'CMS_btag_CSV_LF_stats1',
'CMS_ttH_CSVlfstats2':'CMS_btag_CSV_LF_stats2',
'CMS_ttH_CSVcferr1':'CMS_btag_CSV_Err1', 
'CMS_ttH_CSVcferr2':'CMS_btag_CSV_Err2', 
'CMS_ttHl16_btag_HF':'CMS_btag_CSV_HF',
'CMS_ttHl16_btag_HFStats1':'CMS_btag_CSV_HF_stats1', 
'CMS_ttHl16_btag_HFStats2':'CMS_btag_CSV_HF_stats2', 
'CMS_ttHl16_btag_LF':'CMS_btag_CSV_LF', 
'CMS_ttHl16_btag_LFStats1':'CMS_btag_CSV_LF_stats1', 
'CMS_ttHl16_btag_LFStats2':'CMS_btag_CSV_LF_stats2',
'CMS_ttHl16_btag_cErr1':'CMS_btag_CSV_Err1',
'CMS_ttHl16_btag_cErr2':'CMS_btag_CSV_Err2', 
'CMS_ttH_CSVjes':'CMS_btag_CSV_JES',
'cms_ps':'CMS_PS',
'CMS_hgg_PS':'CMS_PS',
'CMS_hgg_UE':'CMS_UE',
'CMS_ggH_PS':'CMS_PS', #??? in the Htt analysis 
'CMS_qqH_PS':'CMS_PS', #??? in the Htt analysis 
#PS_wh3l ? in the HWW analysis
#PS_zh4l ? in the HWW analysis
#UE_wh3l ? in the HWW analysis
#UE_zh4l ? in the HWW analysis
'cms_eff_b':'CMS_eff_b',
'cms_pu':'CMS_PU',
'CMS_res_j':'CMS_res_j_13TeV',
'cms_res_j':'CMS_res_j_13TeV',
'cms_scale_j':'CMS_scale_j_13TeV',
'cms_tune':'CMS_PS',
'PS': 'CMS_PS',  # hww
'UE': 'CMS_UE',   # hww
'QCDscale_ggVH': 'QCDscale_ggZH',  # hinv
'pdf_Higgs_qq': 'pdf_Higgs_qqbar',  # hmm
'lumi_13TeV2016': 'lumi_13TeV_2016'  # hinv
#comb_2017_mu_hmm.txt:cms_fake_b
#comb_2017_mu_hmm.txt:cms_pdf
}

rename_2017 = {
'CMS_scale_j_AbsoluteStat_13TeV' : 'CMS_scale_j_AbsoluteStat_13TeV_2017',
'CMS_scale_j_RelativeJEREC1_13TeV' : 'CMS_scale_j_RelativeJEREC1_13TeV_2017',
'CMS_scale_j_RelativeJEREC2_13TeV' : 'CMS_scale_j_RelativeJEREC2_13TeV_2017',
'CMS_scale_j_RelativePtEC1_13TeV' : 'CMS_scale_j_RelativePtEC1_13TeV_2017',
'CMS_scale_j_RelativePtEC2_13TeV' : 'CMS_scale_j_RelativePtEC2_13TeV_2017',
'CMS_scale_j_RelativeStatEC_13TeV' : 'CMS_scale_j_RelativeStatEC_13TeV_2017',
'CMS_scale_j_RelativeStatFSR_13TeV' : 'CMS_scale_j_RelativeStatFSR_13TeV_2017',
'CMS_scale_j_RelativeStatHF_13TeV' : 'CMS_scale_j_RelativeStatHF_13TeV_2017',
'CMS_scale_j_TimePtEta_13TeV' : 'CMS_scale_j_TimePtEta_13TeV_2017',
'CMS_LHE_weights_scale_muR_ZH': 'CMS_vhbb_LHE_weights_scale_muR_ZH',
'CMS_LHE_weights_scale_muF_ZH': 'CMS_vhbb_LHE_weights_scale_muF_ZH',
'CMS_LHE_weights_scale_muR_ggZH': 'CMS_vhbb_LHE_weights_scale_muR_ggZH',
'CMS_LHE_weights_scale_muF_ggZH': 'CMS_vhbb_LHE_weights_scale_muF_ggZH',
'CMS_LHE_weights_scale_muR_WH': 'CMS_vhbb_LHE_weights_scale_muR_WH',
'CMS_LHE_weights_scale_muF_WH': 'CMS_vhbb_LHE_weights_scale_muF_WH',
'CMS_LHE_weights_scale_muR_Wj0b': 'CMS_vhbb_LHE_weights_scale_muR_Wj0b',
'CMS_LHE_weights_scale_muF_Wj0b': 'CMS_vhbb_LHE_weights_scale_muF_Wj0b',
'CMS_LHE_weights_scale_muR_Wj1b': 'CMS_vhbb_LHE_weights_scale_muR_Wj1b',
'CMS_LHE_weights_scale_muF_Wj1b': 'CMS_vhbb_LHE_weights_scale_muF_Wj1b',
'CMS_LHE_weights_scale_muR_Wj2b': 'CMS_vhbb_LHE_weights_scale_muR_Wj2b',
'CMS_LHE_weights_scale_muF_Wj2b': 'CMS_vhbb_LHE_weights_scale_muF_Wj2b',
'CMS_LHE_weights_scale_muR_Zj0b': 'CMS_vhbb_LHE_weights_scale_muR_Zj0b',
'CMS_LHE_weights_scale_muF_Zj0b': 'CMS_vhbb_LHE_weights_scale_muF_Zj0b',
'CMS_LHE_weights_scale_muR_Zj1b': 'CMS_vhbb_LHE_weights_scale_muR_Zj1b',
'CMS_LHE_weights_scale_muF_Zj1b': 'CMS_vhbb_LHE_weights_scale_muF_Zj1b',
'CMS_LHE_weights_scale_muR_Zj2b': 'CMS_vhbb_LHE_weights_scale_muR_Zj2b',
'CMS_LHE_weights_scale_muF_Zj2b': 'CMS_vhbb_LHE_weights_scale_muF_Zj2b',
'CMS_LHE_weights_scale_muR_TT': 'CMS_vhbb_LHE_weights_scale_muR_TT',
'CMS_LHE_weights_scale_muF_TT': 'CMS_vhbb_LHE_weights_scale_muF_TT',
'CMS_LHE_weights_scale_muR_VVHF': 'CMS_vhbb_LHE_weights_scale_muR_VVHF',
'CMS_LHE_weights_scale_muF_VVHF': 'CMS_vhbb_LHE_weights_scale_muF_VVHF',
'CMS_LHE_weights_scale_muR_VVLF': 'CMS_vhbb_LHE_weights_scale_muR_VVLF',
'CMS_LHE_weights_scale_muF_VVLF': 'CMS_vhbb_LHE_weights_scale_muF_VVLF',
'CMS_LHE_weights_scale_muR_s_Top': 'CMS_vhbb_LHE_weights_scale_muR_s_Top',
'CMS_LHE_weights_scale_muF_s_Top': 'CMS_vhbb_LHE_weights_scale_muF_s_Top',
}

for oldname, newname in rename.iteritems():
  # Do not rename run1 systs for now
  cb.cp().syst_name([oldname]).channel(['tth_run1','vbfbb_run1','vhbb_run1'], False).ForEachSyst(lambda x: x.set_name(newname))

for oldname, newname in rename_2017.iteritems():
  # Rename some of the 2017 JEC uncertainties to uncorrelate from 2016. Also rename the acceptance scale variations to correlate 2016&2017
  cb.cp().syst_name([oldname]).channel(['vhbb_2017']).ForEachSyst(lambda x: x.set_name(newname))


cb.cp().signals().ForEachSyst(
    lambda x: x.set_name(x.name().replace("pdf_qqbar","pdf_Higgs_qqbar").replace("pdf_gg","pdf_Higgs_gg"))
)


for chan in ['tth_hbb_leptonic']:
    cb.cp().channel([chan]).ForEachSyst(
        lambda x: x.set_name(re.sub("^CMS_eff_e$","CMS_"+chan+"_eff_e",x.name()))
        )
    cb.cp().channel([chan]).ForEachSyst(
        lambda x: x.set_name(re.sub("^CMS_eff_m$","CMS_"+chan+"_eff_m",x.name()))
        )

for chan in ['ggHbb']:
    cb.cp().channel([chan]).ForEachSyst(
        lambda x: x.set_name(re.sub("^CMS_scale_j$","CMS_"+chan+"_scale_j",x.name()))
        )
    cb.cp().channel([chan]).ForEachSyst(
        lambda x: x.set_name(re.sub("^CMS_res_j$","CMS_"+chan+"_res_j",x.name()))
        )

cb.cp().syst_name(['lumi_13TeV_2016']).ForEachSyst(lambda x: x.set_value_u(1.025))

for chan in ['vhbb_2017']:
    cb.cp().channel([chan]).ForEachSyst(
        lambda x: x.set_name(re.sub("^lumi_13TeV_2016$","lumi_13TeV_2017",x.name()))
        )

# Fix run1 ttH:
#ForEachProcAndSyst(cb.cp().channel(['tth_run1']).bin(['hgg_card_.*']).process(['(gg|qq|W|Z|tt)H', 'tH(q|W)']), lambda x: x.set_process(x.process() + '_hgg'))
ForEachProcAndSyst(cb.cp().channel(['tth_run1']).bin(['ttH_7TeV_.*']).process(['(gg|qq|W|Z|tt)H', 'tH(q|W)']), lambda x: x.set_process(x.process() + '_hbb'))
ForEachProcAndSyst(cb.cp().channel(['tth_run1']).mass(['125.1']), lambda x: x.set_mass('125'))

cb_tth_run1 = cb.cp().channel(['tth_run1'])
for proc, oldname, newname in [
    # ('(ggH|bbH)',           '^(pdf_gg)$',       'pdf_Higgs_gg'),
    ('(ttH)',               '^(pdf_gg)$',        'pdf_Higgs_ttH'),
    # ('(qqH|VBF|WH|^ZH)',    '^(pdf_qqbar)$',    'pdf_Higgs_qq'),
    ('^tHW_.*$',               '^(pdf_qg)$',        'pdf_Higgs_tHW'),
    ('^tHq_.*$',               '^(pdf_qg)$',        'pdf_Higgs_tHq'),
    ('^tHq_.*$',               '^(pdf_Higgs_qqbar)','pdf_Higgs_tHq'),
    ('^tHW_.*$',             '^(pdf_Higgs_gg)$',  'pdf_Higgs_tHW'),
    ('^tHq_.*$',             '^(pdf_Higgs_gg)$',  'pdf_Higgs_tHq'),
    # ('.*',                  '^(pdf_qqbar)$',     'pdf_qq'),
    # ('tHq_hbb',             '^(QCDscale_tHq)$',  'QCDscale_tHjb'),
    ('^(tHq)$',             '^(QCDscale_ttH)$',  'QCDscale_tHq'),
    ('^(tHW)$',             '^(QCDscale_ttH)$',  'QCDscale_tHW'),
    ('^(ttbarW)$',          'QCDscale_ttbar',    'QCDscale_ttW'),
    ('^(ttbarZ)$',          'QCDscale_ttbar',    'QCDscale_ttZ'),
    ('.*',          'QCDscale_WtH',    'QCDscale_tHW'),
    ('.*',          'QCDscale_tHjb',    'QCDscale_tHq'),
    ('^ttH_.*$',          'pdf_Higgs_gg',    'pdf_Higgs_ttH'),
    # ('.*', 'CMS_ttH_CSVCErr1',    'CMS_btag_CSV_Err1'),     # altE
    # ('.*', 'CMS_ttH_CSVCErr2',    'CMS_btag_CSV_Err2'),     # altE
    # ('.*', 'CMS_ttH_CSVHF',       'CMS_btag_CSV_HF'),     # altE
    # ('.*', 'CMS_ttH_CSVHFStats1', 'CMS_btag_CSV_HF_stats1'),     # altE
    # ('.*', 'CMS_ttH_CSVHFStats2', 'CMS_btag_CSV_HF_stats2'),     # altE
    # ('.*', 'CMS_ttH_CSVLF',       'CMS_btag_CSV_LF'),     # altE
    # ('.*', 'CMS_ttH_CSVLFStats1', 'CMS_btag_CSV_LF_stats1'),     # altE
    # ('.*', 'CMS_ttH_CSVLFStats2', 'CMS_btag_CSV_LF_stats2'),     # altE
    ('.*', 'CMS_eff_b', 'CMS_eff_b_run1'),     # altE
    ('.*', 'CMS_hgg_tth_parton_shower', 'CMS_hgg_tth_parton_shower_run1'),
    ('.*', 'CMS_hgg_tth_mc_low_stat', 'CMS_hgg_tth_mc_low_stat_run1'),
    ('.*', 'CMS_hgg_tth_gluon_splitting', 'CMS_hgg_tth_gluon_splitting_run1'),
    #('.*', 'CMS_ttHl_FRm_norm', 'CMS_ttHl16_FRm_norm'),   # altA
    #('.*', 'CMS_ttHl_FRe_norm', 'CMS_ttHl16_FRe_norm'),   # altA
    #don't do this for Hbb, renamed the 13 TeV ones#('.*', 'CMS_scale_j', 'CMS_scale_j_run1'),   # altC
    #('.*', 'CMS_ttH_QCDscale_ttbb', 'bgnorm_ttbarPlusBBbar'),   # altD
    ]:
    cb_tth_run1.cp().process([proc]).syst_name([oldname]).ForEachSyst(lambda x: x.set_name(newname))

def DoSwap(sys):
    print sys
    sys.SwapUpAndDown()

cb.cp().channel(['vhbb_2017']).syst_name(['CMS_vhbb_LHE_weights_scale_mu(R|F).*']).ForEachSyst(lambda x: DoSwap(x))

cb.cp().syst_name(['CMS_vhbb_LHE_weights_scale_muR_Zj2b']).PrintSysts()
#cb_vhbb_run1 = cb.cp().channel(['vhbb_run1'])
#for proc, oldname, newname in [
#    ('.*', 'CMS_scale_j', 'CMS_scale_j_run1'),  
#    ('.*', 'CMS_res_j', 'CMS_res_j_run1')  
#    ]:
#    cb_vhbb_run1.cp().process([proc]).syst_name([oldname]).ForEachSyst(lambda x: x.set_name(newname))

#cb_vbfbb_run1 = cb.cp().channel(['vbfbb_run1'])
#for proc, oldname, newname in [
#    ('.*', 'CMS_scale_j', 'CMS_scale_j_run1'),  
#    ('.*', 'CMS_res_j', 'CMS_res_j_run1')  
#    ]:
#    cb_vbfbb_run1.cp().process([proc]).syst_name([oldname]).ForEachSyst(lambda x: x.set_name(newname))


# Update tth_run1 to YR4 uncertainties
######################################################
def UpdateUncert(x, val_d, val_u=None):
    if x.type() != 'lnN':
        'Not a lnN:'
        x.PrintHeader()
        print x
        return
    if val_u is None:
        x.set_asymm(False)
        x.set_value_u(val_d)
    else:
        x.set_asymm(True)
        x.set_value_u(val_u)
        x.set_value_d(val_d)

cb_run1sig = cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1']).signals()

cb_run1sig.cp().process(['WH_.*']).syst_name(['QCDscale_VH']).ForEachSyst(lambda x: UpdateUncert(x, 0.992, 1.007))
cb_run1sig.cp().process(['ZH_.*']).syst_name(['QCDscale_VH']).ForEachSyst(lambda x: UpdateUncert(x, 0.976, 1.028))
cb_run1sig.cp().process(['ggH_.*']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: UpdateUncert(x, 0.931, 1.044))
cb_run1sig.cp().process(['qqH_.*']).syst_name(['QCDscale_qqH']).ForEachSyst(lambda x: UpdateUncert(x, 0.998, 1.003))
cb_run1sig.cp().process(['tHW_.*']).syst_name(['QCDscale_tHW']).ForEachSyst(lambda x: UpdateUncert(x, 0.943, 1.043))
cb_run1sig.cp().process(['tHq_.*']).syst_name(['QCDscale_tHq']).ForEachSyst(lambda x: UpdateUncert(x, 0.834, 1.073))
cb_run1sig.cp().process(['ttH_.*']).syst_name(['QCDscale_ttH']).ForEachSyst(lambda x: UpdateUncert(x, 0.908, 1.040))

cb_run1sig.cp().process(['ggH_.*']).syst_name(['pdf_Higgs_gg']).ForEachSyst(lambda x: UpdateUncert(x, 1.032))
cb_run1sig.cp().process(['qqH_.*']).syst_name(['pdf_Higgs_qqbar']).ForEachSyst(lambda x: UpdateUncert(x, 1.022))
cb_run1sig.cp().process(['WH_.*']).syst_name(['pdf_Higgs_qqbar']).ForEachSyst(lambda x: UpdateUncert(x, 1.02))
cb_run1sig.cp().process(['ZH_.*']).syst_name(['pdf_Higgs_qqbar']).ForEachSyst(lambda x: UpdateUncert(x, 1.017))
cb_run1sig.cp().process(['ttH_.*']).syst_name(['pdf_Higgs_ttH']).ForEachSyst(lambda x: UpdateUncert(x, 1.043))
cb_run1sig.cp().process(['tHW_.*']).syst_name(['pdf_Higgs_tHW']).ForEachSyst(lambda x: UpdateUncert(x, 1.079))
cb_run1sig.cp().process(['tHq_.*']).syst_name(['pdf_Higgs_tHq']).ForEachSyst(lambda x: UpdateUncert(x, 1.046))

# Also fix run 2:
cb.cp().channel(['tth_run1','vbfbb_run1','vhbb_run1'], False).signals().process(['tHW_.*']).syst_name(['QCDscale_tHW']).ForEachSyst(lambda x: UpdateUncert(x, 0.933, 1.049))
cb.cp().channel(['tth_run1','vbfbb_run1','vhbb_run1'], False).signals().process(['tHq_.*']).syst_name(['QCDscale_tHq']).ForEachSyst(lambda x: UpdateUncert(x, 0.853, 1.065))
######################################################


#scale YR4/YR3 for Run 1 ttH
wbr.var("MH").setVal(125.09)

xs_yr3_8TeV = {"ggH":19.24,"vbfH":1.579,"WH":0.7027,"ZH":0.4142,"ggZH":3.243E-02,"ttH":0.1290}
xs_yr3_7TeV = {"ggH":15.11,"vbfH":1.222,"WH":0.5770,"ZH":0.3341,"ggZH":2.275E-02,"ttH":0.08611}
xs_yr4_8TeV = {"ggH":2.139E+01,"vbfH":1.600E+00,"WH":7.009E-01,"ZH":4.199E-01,"ggZH":3.942E-02,"bbH":2.008E-01,"ttH":1.327E-01}
xs_yr4_7TeV = {"ggH":1.682E+01,"vbfH":1.240E+00,"WH":5.756E-01,"ZH":3.383E-01,"ggZH":2.789E-02,"bbH":1.547E-01,"ttH":8.873E-02}
br_yr3 = {"hbb":5.75E-01, "htt":6.30E-02, "hmm":2.19E-04, "hcc":2.90E-02, "hss":2.46E-04, "hgluglu":8.56E-02, "hgg":2.28E-03, "hzg":1.55E-03, "hww":2.16E-01, "hzz":2.67E-02}

yr4scal_7TeV_systmap = ch.SystMap('process')
yr4scal_7TeV_cb = cb.cp().channel(['tth_run1', 'vhbb_run1']).bin(['.*7TeV.*']).signals()
print '>> Adjusting to YR4 for signals in bins:'
pprint.pprint(yr4scal_7TeV_cb.bin_set(), indent=4)
yr4scal_7TeV_sigs = yr4scal_7TeV_cb.process_set()
print '>> Signal processes are:'
pprint.pprint(yr4scal_7TeV_sigs, indent=4)

for sig in yr4scal_7TeV_sigs:
    xs = sig.split("_")[0]
    br = sig.split("_")[-1]
    print sig,xs,br
    if (xs=="qqH"): xs="vbfH"
    if (xs=="tHW" or xs=="tHq" or xs=="bbH"):
        xsscal=1.0
    else:
        xsscal = xs_yr4_7TeV[xs]/xs_yr3_7TeV[xs]
    if (br=="hinv"):
        brscal=1.0
    else:
        brscal = wbr.function(br).getVal()/br_yr3[br]
    print sig, xsscal, brscal
    yr4scal_7TeV_systmap([sig], round(xsscal * brscal, 3))

yr4scal_7TeV_cb.AddSyst(cb, 'yr4scal_7TeV_$PROCESS', 'rateParam', yr4scal_7TeV_systmap)

for sig in yr4scal_7TeV_sigs:
    par = cb.GetParameter('yr4scal_7TeV_' + sig)
    par.set_frozen(True)
    par.set_range(par.val(), par.val())

yr4scal_8TeV_systmap = ch.SystMap('process')
yr4scal_8TeV_cb = cb.cp().channel(['tth_run1', 'vhbb_run1', 'vbfbb_run1']).bin(['.*8TeV.*','CAT.*']).signals()
print '>> Adjusting to YR4 for signals in bins:'
pprint.pprint(yr4scal_8TeV_cb.bin_set(), indent=4)
yr4scal_8TeV_sigs = yr4scal_8TeV_cb.process_set()
print '>> Signal processes are:'
pprint.pprint(yr4scal_8TeV_sigs, indent=4)

for sig in yr4scal_8TeV_sigs:
    xs = sig.split("_")[0]
    br = sig.split("_")[-1]
    print sig,xs,br
    if (xs=="qqH"): xs="vbfH"
    if (xs=="tHW" or xs=="tHq" or xs=="bbH"):
        xsscal=1.0
    else:
        xsscal = xs_yr4_8TeV[xs]/xs_yr3_8TeV[xs]
    if (br=="hinv"):
        brscal=1.0
    else:
        brscal = wbr.function(br).getVal()/br_yr3[br]
    print sig, xsscal, brscal
    yr4scal_8TeV_systmap([sig], round(xsscal * brscal, 3))

yr4scal_8TeV_cb.AddSyst(cb, 'yr4scal_8TeV_$PROCESS', 'rateParam', yr4scal_8TeV_systmap)

for sig in yr4scal_8TeV_sigs:
    par = cb.GetParameter('yr4scal_8TeV_' + sig)
    par.set_frozen(True)
    par.set_range(par.val(), par.val())

"""
#scale YR4/YR3 for Run 1 VHbb
wbr.var("MH").setVal(125.09)

yr4scal_7TeV_systmap_hbb = ch.SystMap('process')
yr4scal_7TeV_cb_hbb = cb.cp().channel(['vhbb_run1']).bin(['.*7TeV.*']).signals()
yr4scal_7TeV_sigs_hbb = yr4scal_7TeV_cb_hbb.process_set()

for sig in yr4scal_7TeV_sigs_hbb:
    xs = sig.split("_")[0]
    br = sig.split("_")[-1]
    print sig,xs,br
    if (xs=="qqH"): xs="vbfH"
    if (xs=="tHW" or xs=="tHq" or xs=="bbH"):
        xsscal=1.0
    else:
        xsscal = xs_yr4_7TeV[xs]/xs_yr3_7TeV[xs]
    if (br=="hinv"):
        brscal=1.0
    else:
        brscal = wbr.function(br).getVal()/br_yr3[br]
    print sig, xsscal, brscal
    yr4scal_7TeV_systmap_hbb([sig], round(xsscal * brscal, 3))

yr4scal_7TeV_cb_hbb.AddSyst(cb, 'yr4scal_7TeV_$PROCESS', 'rateParam', yr4scal_7TeV_systmap_hbb)

for sig in yr4scal_7TeV_sigs_hbb:
    par = cb.GetParameter('yr4scal_7TeV_' + sig)
    par.set_frozen(True)
    par.set_range(par.val(), par.val())

yr4scal_8TeV_systmap_hbb = ch.SystMap('process')
yr4scal_8TeV_cb_hbb = cb.cp().channel(['vhbb_run1']).bin(['.*7TeV.*']).signals()
yr4scal_8TeV_sigs_hbb = yr4scal_8TeV_cb_hbb.process_set()

for sig in yr4scal_8TeV_sigs_hbb:
    xs = sig.split("_")[0]
    br = sig.split("_")[-1]
    print sig,xs,br
    if (xs=="qqH"): xs="vbfH"
    if (xs=="tHW" or xs=="tHq" or xs=="bbH"):
        xsscal=1.0
    else:
        xsscal = xs_yr4_8TeV[xs]/xs_yr3_8TeV[xs]
    if (br=="hinv"):
        brscal=1.0
    else:
        brscal = wbr.function(br).getVal()/br_yr3[br]
    print sig, xsscal, brscal
    yr4scal_8TeV_systmap_hbb([sig], round(xsscal * brscal, 3))

yr4scal_8TeV_cb_hbb.AddSyst(cb, 'yr4scal_8TeV_$PROCESS', 'rateParam', yr4scal_8TeV_systmap_hbb)

for sig in yr4scal_8TeV_sigs_hbb:
    print sig 
    par = cb.GetParameter('yr4scal_8TeV_' + sig)
    par.set_frozen(True)
    par.set_range(par.val(), par.val())
"""

# Put "8TeV" in the bin names that don't already have 7 or 8 TeV
cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1']).bin(['.*(7|8)TeV.*'], False).ForEachObj(lambda x: x.set_bin(x.bin() + '_8TeV'))
# Also replace "7TeV" with "8TeV_7" 
cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1']).bin(['.*7TeV.*'], True).ForEachObj(lambda x: x.set_bin(x.bin().replace('7TeV', '8TeV_7')))



# Edits for MC stats
if args.stats_mode == 1:
    # Need to add '[bin] autoMCStats -1' for every binned category that
    # doesn't already use autoMCStats
    currentBins = list(cb.GetAutoMCStatsBins())
    target = cb.cp().channel(['ggHbb'], False).bin(currentBins, False)
    target.SetAutoMCStats(cb, -1.)

if args.stats_mode == 2:
    # First drop all existing stat uncertainties
    dropAll = list()

    for chn, pattern in [
      # ('htt',               '.*_bin_[0-9]*'),
      #('hww',               '.*_ibin_.*'),
      ('tth_hbb_hadronic',  '.*Bin[0-9].*'),
      #('tth_multilepton',   '.*_bin[0-9].*'),
      # ('tth_htt',           '.*_bin_[0-9].*'),
      #('vhbb',              '.*_bin[0-9].*')
      ]:
        drop = list(cb.cp().channel([chn]).syst_name([pattern]).syst_name_set())
        print '>> Dropping %i bin-by-bin parameters from channel %s' % (len(drop), chn)
        dropAll.extend(drop)

    cb.syst_name(dropAll, False)

    currentBins = list(cb.GetAutoMCStatsBins())
    target = cb.cp().channel(['tth_hbb_hadronic'], True).bin(currentBins, False)
    print '>> Enabling autoMCStats with threshold 0 for bins:'
    pprint.pprint(target.bin_set(), indent=4)
    target.SetAutoMCStats(cb, 0.0)
    target = cb.cp().channel(['htt', 'hww', 'tth_htt', 'vhbb', 'tth_multilepton'], True).bin(currentBins, False)
    print '>> Enabling autoMCStats with threshold -1 for bins:'
    pprint.pprint(target.bin_set(), indent=4)
    target.SetAutoMCStats(cb, -1.)

if args.diagnostics:
    sig_procs_in_bins = defaultdict(set)

    print 'Bins_in_channels =  '
    bins_in_channels = defaultdict(set)
    for chn in cb.cp().channel_set():
        bins_in_channels[chn] = set(cb.cp().channel([chn]).bin_set())
    pprint.pprint(dict(bins_in_channels), indent=4)
    print ' '

    print 'Signal_processes = '
    pprint.pprint(cb.cp().signals().process_set(), indent=4)

    for p in cb.cp().signals().process_set():
        for b in cb.cp().process([p]).SetFromProcs(lambda x: (x.channel(), x.bin())):
            sig_procs_in_bins[p].add(b)

    print 'Signal_processes_in_bins: '
    pprint.pprint(dict(sig_procs_in_bins), indent=4)
    print ' '

    sig_systs_in_chns = defaultdict(set)

    for syst in cb.cp().signals().syst_name_set():
        sig_systs_in_chns[syst] = cb.cp().syst_name(
            [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

    print 'Signal_systematics_in_channels = '
    pprint.pprint(dict(sig_systs_in_chns), indent=4)
    print ' '

    correlated_systs = defaultdict(set)
    for syst in cb.cp().syst_name_set():
        if len(cb.cp().syst_name([syst]).SetFromSysts(lambda x: x.channel())) > 1:
            correlated_systs[syst] = cb.cp().syst_name(
                [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

    print 'Correlated_systematics_in_channels = '
    pprint.pprint(dict(correlated_systs), indent=4)
    print ' '

    #for syst in cb.cp().syst_name_set():
    #    print '>> Implementation of syst ' + syst
    #    cb.cp().syst_name([syst]).PrintSysts()

    run1_systs = set(cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1'], True).syst_name_set())
    run2_systs = set(cb.cp().channel(['tth_run1','vhbb_run1','vbfbb_run1'], False).syst_name_set())
    print 'Correlated_between_run1_and_run2 = '
    pprint.pprint(run1_systs.intersection(run2_systs))

#cb.channel(['hmm'],False)

cb.FilterProcs(lambda x: drop_zero_procs(cb,x) if x.channel()=='vhbb_run1' else None )

print '>> Writing combined card'
cb.cp().channel(['tth_run1','vhbb_run1'], False).WriteDatacard('comb_2017_Hbb%s.txt' % postfix, 'comb_2017_Hbb%s.inputs.root' % postfix)
cb.cp().channel(['vhbb_2017'], False).WriteDatacard('comb_2017_Hbb_2016_plus_run1%s.txt' % postfix, 'comb_2017_Hbb_2016_plus_run1%s.inputs.root' % postfix)
cb.cp().channel(['vhbb_run1','vhbb','vhbb_2017']).WriteDatacard('comb_2017_Hbb_vhonly_plus_run1%s.txt' % postfix, 'comb_2017_Hbb_vhonly_plus_run1%s.inputs.root' % postfix)
cb.cp().channel(['vhbb','vhbb_2017']).WriteDatacard('comb_2017_Hbb_vhonly%s.txt' % postfix, 'comb_2017_Hbb_vhonly%s.inputs.root' % postfix)
cb.WriteDatacard('comb_2017_Hbb_plus_run1%s.txt' % postfix, 'comb_2017_Hbb_plus_run1%s.inputs.root' % postfix)
cb.cp().channel(['tth_hbb_leptonic', 'tth_hbb_hadronic']).WriteDatacard('comb_2017_Hbb_tth_hbb%s.txt' % postfix, 'comb_2017_Hbb_tth_hbb%s.inputs.root' % postfix)
#os.system('mkdir hbb_comb_split_cards')
#for chn in cb.channel_set():
#    for bin in cb.cp().channel([chn]).bin_set():
#        cardname = '%s_%s' % (chn, bin)
#        print '>> Writing %s card' % cardname
#        cb.cp().bin([bin]).WriteDatacard('hbb_comb_split_cards/%s.txt' % cardname, 'hbb_comb_split_cards/%s.input.root' % cardname)

# Also write per-analysis cards for cross-checking
for chn in cb.channel_set():
    print '>> Writing %s card' % chn
    cb.cp().channel([chn]).WriteDatacard(
        'comb_2017_Hbb_%s%s.txt' % (chn, postfix) , 'comb_2017_Hbb_%s%s.inputs.root' % (chn, postfix))


#processCmd('sed -i "1,5{s~imax [0-9]*~imax *~g}" comb*.txt')
#processCmd('sed -i "1,5{s~jmax [0-9]*~jmax *~g}" comb*.txt')
#processCmd('sed -i "1,5{s~kmax [0-9]*~kmax *~g}" comb*.txt')

# Make some edits to the cards:
cardlist = ['', '_plus_run1', '_vhbb', '_vhbb_2017', '_vhbb_run1', '_tth_run1', '_tth_hbb', '_hgg', '_tth_hbb_leptonic','_tth_hbb_hadronic','_2016_plus_run1', '_vhonly_plus_run1','_vhonly']

for card in cardlist:

  # BR uncertainties for mu based models
  processCmd('cp comb_2017_Hbb'+card+postfix+'.txt comb_2017_Hbb_mu'+card+postfix+'.txt')
  processCmd('cat brunc_mu.txt >> comb_2017_Hbb_mu'+card+postfix+'.txt')

  # BR uncertainties for kappa/lambda based models
  processCmd('cp comb_2017_Hbb'+card+postfix+'.txt comb_2017_Hbb_kappa'+card+postfix+'.txt')
  processCmd('cat brunc_kappa.txt >> comb_2017_Hbb_kappa'+card+postfix+'.txt')

  # other edits, like lumi scale
  processCmd('cat edits.txt >> comb_2017_Hbb_mu'+card+postfix+'.txt')
  processCmd('cat edits.txt >> comb_2017_Hbb_kappa'+card+postfix+'.txt')
