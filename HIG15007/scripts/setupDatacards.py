#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import os


# Need this later
def RenameSyst(cmb, syst, old, new):
    if old in syst.name():
        oldname = syst.name()
        syst.set_name(new)
        # Should change the ch::Parameter names too
        cmb.RenameParameter(oldname, new)


shapes_dir = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG15007/shapes'

cb = ch.CombineHarvester()

#####################################################################################
# Set the processes and categories
#####################################################################################
sig_procs = ['ZTT']

bkg_procs = {
  'et': ['W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'mt': ['W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  # 'em': ['W', 'QCD', 'ZLL', 'TT', 'VV'], # Wisconsin should add ZLL
  'em': ['W', 'QCD', 'TT', 'VV'],
  'tt': ['W', 'QCD', 'TT', 'VV']
}

bins = {
  'et': [(0, 'et_inclusive')],
  'mt': [(0, 'mt_inclusive')],
  'em': [(0, 'em_inclusive')],
  'tt': [(0, 'tt_inclusive')]
}

channels = ['et', 'mt', 'em', 'tt']

#####################################################################################
# Set input shape files
#####################################################################################
files = {
    'et': {
        'KIT': 'ztt_et_et_inclusive_13TeV_fall15.root'
    },
    'mt': {
        'KIT': 'ztt_mt_mt_inclusive_13TeV_fall15.root'
    },
    'em': {
        'Wisconsin': 'htt_em.inputs-sm-13TeV.root',
        'DESY' : 'htt_em.inputs-sm-13TeV_pzeta.root'
    },
    'tt': {
        'Wisconsin': 'htt_tt.inputs-sm-13TeV.root'
    },
    ##'mm': {
    ##    'Florida': ''
    ##}
}

inputs = {
    'et': 'KIT',
    'mt': 'KIT',
    'em': 'DESY',
    'tt': 'Wisconsin',
    ##'mm': 'Florida'
}

#####################################################################################
# Create CH entries and load shapes
#####################################################################################
for chn in channels:
    ana = ['ztt']
    era = ['13TeV']
    cb.AddObservations(['*'], ana, era, [chn], bins[chn])
    cb.AddProcesses(['*'], ana, era, [chn], bkg_procs[chn], bins[chn], False)
    cb.AddProcesses(['*'], ana, era, [chn], sig_procs, bins[chn], True)

#####################################################################################
# Define systematic uncertainties
#####################################################################################
# define some useful shortcuts
real_m = ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV']  # procs with a real muon
real_e = ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV']  # procs with a real electron

constrain_eff_t = False

cb.cp().AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], real_m, 1.03)
        (['em'], real_m + ['W'], 1.03))

cb.cp().AddSyst(
    cb, 'CMS_eff_e', 'lnN', ch.SystMap('channel', 'process')
        (['et'], real_e, 1.03)
        (['em'], real_e + ['W'], 1.03))

# Only create the eff_t lnN if we want this to be constrained,
# otherwise set a rateParam.
# Split tau ID efficiency uncertainty into part ("CMS_eff_t") that is correlated between channels
# and part ("CMS_eff_t_et", "CMS_eff_t_mt", "CMS_eff_t_tt") that is uncorrelated
if constrain_eff_t:
    cb.cp().AddSyst(
        cb, 'CMS_eff_t', 'lnN', ch.SystMap('channel', 'process')
            (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.05)
            (['tt'],       ['ZTT', 'TT', 'VV'], 1.10))
    cb.cp().AddSyst(
        cb, 'CMS_eff_t_$CHANNEL', 'lnN', ch.SystMap('channel', 'process')
            (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.03)
            (['tt'],       ['ZTT', 'TT', 'VV'], 1.06))
else:
    cb.cp().AddSyst(
        cb, 'CMS_eff_t', 'rateParam', ch.SystMap('channel', 'process')
            (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.0)
            (['tt'],       ['ZTT', 'TT', 'VV'], 1.0))
    # We should set a sensible range for the resulting parameter
    cb.GetParameter('CMS_eff_t').set_range(0.5, 1.5)

# Split tau energy scale uncertainty into part ("CMS_scale_t") that is correlated between channels
# and part ("CMS_scale_t_et", "CMS_scale_t_mt", "CMS_scale_t_tt") that is uncorrelated
cb.cp().AddSyst(
    cb, 'CMS_scale_t_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['et', 'mt'], ['ZTT'], 0.833))
cb.cp().AddSyst(
    cb, 'CMS_scale_t_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['et', 'mt'], ['ZTT'], 0.500))

cb.cp().process(['QCD']).AddSyst(
    cb, 'CMS_$ANALYSIS_qcdSyst_$BIN_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt'],  1.06)
        (['em'],  2.00) # FIXME!
        (['tt'],  1.20))  # Not in KIT datacards but should be added

cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_$ANALYSIS_ttjNorm_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt'],  1.10)
        (['em', 'tt'],  1.10))

cb.cp().process(['VV']).AddSyst(
    cb, 'CMS_$ANALYSIS_vvNorm_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt'],  1.15)
        (['em', 'tt'],  1.15))

cb.cp().process(['W']).AddSyst(
    cb, 'CMS_$ANALYSIS_wjNorm_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'tt'],  1.20))

# KIT cards only have one zllFakeTau param, but need at least three:
#  - e->tau fake rate 
#  - mu->tau fake rate (CV: use 100% uncertainty for now, as no measurement of mu->tau fake-rate in Run 2 data available yet)
#  - jet->tau fake rate
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_eFakeTau_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['et'],  1.30))
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_mFakeTau_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  2.00))

cb.cp().process(['ZJ']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt'],  1.30))

cb.cp().AddSyst(
    cb, 'lumi_$ERA', 'lnN', ch.SystMap('channel', 'process')
        (['et', 'mt'], ['ZTT', 'ZL', 'ZJ', 'TT', 'VV'], 1.027)
        (['em', 'tt'], ['ZTT', 'ZLL', 'TT', 'VV'],      1.027))


#####################################################################################
# Load the shapes
#####################################################################################
for chn in channels:
    cb.cp().channel([chn]).ExtractShapes(
        '%s/%s/%s' % (shapes_dir, inputs[chn], files[chn][inputs[chn]]),
        '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

# Want to treat scale_t as one parameter for now
cb.ForEachSyst(lambda sys: RenameSyst(cb, sys, 'CMS_scale_t', 'CMS_scale_t'))

constrain_scale_t = False
if not constrain_scale_t:
    cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(lambda sys: sys.set_type('shapeU'))


#####################################################################################
# Create bin-by-bin
#####################################################################################
bbb = ch.BinByBinFactory()
bbb.SetPattern('CMS_$ANALYSIS_$BIN_$ERA_$PROCESS_bin_$#')
bbb.SetAddThreshold(0.1)
bbb.SetMergeThreshold(0.5) # For now we merge, but to be checked
bbb.SetFixNorm(True)
bbb.MergeAndAdd(cb.cp().backgrounds(), cb)


#####################################################################################
# Set nuisance parameter groups
#####################################################################################
# Start by calling everything syst and allsyst
cb.SetGroup('allsyst', ['.*'])
cb.SetGroup('syst', ['.*'])

# Then set lumi, and remove from both of the above
cb.SetGroup('lumi', ['lumi_.*'])
cb.RemoveGroup('syst', ['lumi_.*'])
cb.RemoveGroup('allsyst', ['lumi_.*'])

# Then tauid, and remove it only from syst
cb.SetGroup('tauid', ['CMS_eff_t'])
cb.RemoveGroup('syst', ['CMS_eff_t'])

# Now we can split into:
#    - stat + syst + tauid + lumi   ..or..
#    - stat + allsyst + lumi

cb.PrintAll()


#####################################################################################
# Write the cards
#####################################################################################
writer = ch.CardWriter('$TAG/datacard.txt',
                       '$TAG/shapes.root')
writer.SetWildcardMasses([])  # We don't use the $MASS property here
writer.SetVerbosity(1)
x = writer.WriteCards('output/LIMITS/cmb', cb)  # All cards combined
print x
x['output/LIMITS/cmb/datacard.txt'].PrintAll()
for chn in channels:  # plus a subdir per channel
    writer.WriteCards('output/LIMITS/%s'%chn, cb.cp().channel([chn]))
