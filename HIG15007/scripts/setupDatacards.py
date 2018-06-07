#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import argparse
import os


# Need this later
def RenameSyst(cmb, syst, old, new):
    if old in syst.name():
        oldname = syst.name()
        syst.set_name(new)
        # Should change the ch::Parameter names too
        cmb.RenameParameter(oldname, new)


parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='./output/LIMITS', help="""
    Output directory""")
parser.add_argument('--constrain-tau-eff', action='store_true', help="""
    The tau efficiency will be a constrained nuisance parameter""")
parser.add_argument('--constrain-tau-scale', action='store_true', help="""
    The tau energy scale will be a constrained nuisance parameter""")
parser.add_argument('--variable', choices=['svfit', 'mvis'],
                    default='svfit', help="""
    Choice of input variable shape files""")

args = parser.parse_args()

shapes_dir = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG15007/shapes'

cb = ch.CombineHarvester()

##########################################################################
# Set the processes and categories
##########################################################################
sig_procs = ['ZTT']

bkg_procs = {
    'et': ['W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
    'mt': ['W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
    'em': ['W', 'QCD', 'ZLL', 'TT', 'VV'],
    'tt': ['W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
    'mm': ['W', 'QCD', 'ZLL', 'TT', 'VV']
}

bins = {
    'et': [(0, 'et_inclusive')],
    'mt': [(0, 'mt_inclusive')],
    'em': [(0, 'em_inclusive')],
    'tt': [(0, 'tt_inclusive')],
    'mm': [(0, 'mm_inclusive')]
}

channels = ['et', 'mt', 'em', 'tt', 'mm']

##########################################################################
# Set input shape files
##########################################################################
files = {
    'et': {
        'KIT': {
            'mvis': 'ztt_et.inputs-sm-13TeV-mvis_fall15.root',
            'svfit': 'ztt_et.inputs-sm-13TeV-svfit_fall15.root'
        },
        'DESY': {
            'mvis': 'ztt_et.inputs-sm-13TeV-mvis_fall15.root',
            'svfit': 'ztt_et.inputs-sm-13TeV-svfit_fall15.root'
        }
    },
    'mt': {
        'KIT': {
            'mvis': 'ztt_mt.inputs-sm-13TeV-mvis_fall15.root',
            'svfit': 'ztt_mt.inputs-sm-13TeV-svfit_fall15.root'
        },
        'DESY': {
            'mvis': 'ztt_mt.inputs-sm-13TeV-mvis_fall15.root',
            'svfit': 'ztt_mt.inputs-sm-13TeV-svfit_fall15.root'
        }
    },
    'em': {
        'DESY': {
            'mvis': 'ztt_em.inputs-sm-13TeV_mvis.root',
            'svfit': 'ztt_em.inputs-sm-13TeV_msv.root'
        },
        'KIT': {
            'mvis': 'ztt_em.inputs-sm-13TeV-mvis_pzeta_fall15.root',
            'svfit': 'ztt_em.inputs-sm-13TeV-svfit_pzeta_fall15.root'
        }
    },
    'tt': {
        'Wisconsin': {
            'mvis': 'htt_tt.inputs-sm-13TeV.root',
            'svfit': 'htt_tt.inputs-sm-13TeV_svFit.root'
        }
    },
    'mm': {
        'DESY': {
            'mvis': 'ztt_mm.inputs-sm-13TeV_mvis.root',
            'svfit': 'ztt_mm.inputs-sm-13TeV_msv.root'
        }
    }
}

inputs = {
    'et': 'KIT',
    'mt': 'KIT',
    'em': 'DESY',
    'tt': 'Wisconsin',
    'mm': 'DESY'
}

variable = args.variable

##########################################################################
# Create CH entries and load shapes
##########################################################################
for chn in channels:
    ana = ['ztt']
    era = ['13TeV']
    cb.AddObservations(['*'], ana, era, [chn], bins[chn])
    cb.AddProcesses(['*'], ana, era, [chn], bkg_procs[chn], bins[chn], False)
    cb.AddProcesses(['*'], ana, era, [chn], sig_procs, bins[chn], True)

##########################################################################
# Define systematic uncertainties
##########################################################################
# define some useful shortcuts
real_m = ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV']  # procs with a real muon
real_e = ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV']  # procs with a real electron

cb.cp().AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], real_m,                    1.03)
        (['em'], ['ZTT', 'TT', 'W', 'VV'],  1.03)
        (['mm'], ['ZTT', 'VV', 'ZLL'],      1.06)
        (['mm'], ['W'],                     1.03))

cb.cp().AddSyst(
    cb, 'CMS_eff_e', 'lnN', ch.SystMap('channel', 'process')
        (['et'], real_e, 1.04)
        (['em'], ['ZTT', 'TT', 'W', 'VV'], 1.04))

# Only create the eff_t lnN if we want this to be constrained,
# otherwise set a rateParam.
# Split tau ID efficiency uncertainty into part ("CMS_eff_t") that is correlated between channels
# and part ("CMS_eff_t_et", "CMS_eff_t_mt", "CMS_eff_t_tt") that is uncorrelated
if args.constrain_tau_eff:
    print '>> Info: Tau efficiency will be constrained'
    cb.cp().AddSyst(
        cb, 'CMS_eff_t', 'lnN', ch.SystMap('channel', 'process')
            (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.05)
            (['tt'],       ['ZTT', 'TT', 'VV'], 1.10))
else:
    print '>> Info: Tau efficiency will be unconstrained'
    cb.cp().AddSyst(
        cb, 'CMS_eff_t', 'rateParam', ch.SystMap('channel', 'process')
            (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.0)
            (['tt'],       ['ZTT', 'TT', 'VV'], 1.0))
    # We should set a sensible range for the resulting parameter
    cb.GetParameter('CMS_eff_t').set_range(0.0, 4.0)

# Always create the terms that decorrelate the channels
cb.cp().AddSyst(
    cb, 'CMS_eff_t_$CHANNEL', 'lnN', ch.SystMap('channel', 'process')
        (['et', 'mt'], ['ZTT', 'TT', 'VV'], 1.03)
        (['tt'],       ['ZTT', 'TT', 'VV'], 1.06))

# Split tau energy scale uncertainty into part ("CMS_scale_t") that is correlated between channels
# and part ("CMS_scale_t_et", "CMS_scale_t_mt", "CMS_scale_t_tt") that is uncorrelated
# cb.cp().AddSyst(
#     cb, 'CMS_scale_t_$ERA', 'shape', ch.SystMap('channel', 'process')
#         (['et', 'mt'], ['ZTT'], 0.833))
cb.cp().AddSyst(
    cb, 'CMS_scale_t_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['et', 'mt', 'tt'], ['ZTT'], 1.0))

cb.cp().AddSyst(
    cb, 'CMS_scale_e_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['em'], ['ZTT', 'TT', 'W', 'VV'], 1.0))
cb.cp().AddSyst(
    cb, 'CMS_scale_m_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['em'], ['ZTT', 'TT', 'W', 'VV'],      1.0))
cb.cp().AddSyst(
    cb, 'CMS_scale_m_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['mm'], ['ZTT', 'TT', 'VV', 'ZLL', 'W'],    1.0))
cb.cp().AddSyst(
    cb, 'CMS_htt_ttbarShape_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['em', 'mm'], ['TT'], 1.0))
cb.cp().AddSyst(
    cb, 'CMS_htt_em_qcdShape_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['em'], ['QCD'], 1.0))

cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_scale_met', 'lnN', ch.SystMap('channel', 'process')
        (['em', 'mt', 'et'], ['ZTT', 'W', 'ZL', 'ZJ', 'ZLL'], 1.02))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_reso_met', 'lnN', ch.SystMap('channel', 'process')
        (['em', 'mt', 'et'], ['ZTT', 'W', 'ZL', 'ZJ', 'ZLL'], 1.02))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_ewkTop_scale_met', 'lnN', ch.SystMap('channel', 'process')
        (['em', 'mt', 'et'], ['TT', 'VV'], 1.03))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_ewkTop_reso_met', 'lnN', ch.SystMap('channel', 'process')
        (['em', 'mt', 'et'], ['TT', 'VV'], 1.01))

cb.cp().process(['QCD']).AddSyst(
    cb, 'CMS_$ANALYSIS_qcdSyst_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt'],      1.10)
        (['em'],            1.15)
        (['mm'],            1.21)
        (['tt'],            1.06))  # From Tyler's studies

cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_$ANALYSIS_ttjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'em', 'tt', 'mm'],  1.06))
cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_$ANALYSIS_ttjExtrapol_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'em', 'tt', 'mm'],  1.10))

cb.cp().process(['VV']).AddSyst(
    cb, 'CMS_$ANALYSIS_vvXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'em', 'tt'],  1.10))
cb.cp().process(['VV']).AddSyst(
    cb, 'CMS_$ANALYSIS_vvXSyst_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['mm'],  1.30))

cb.cp().channel(['mm']).process(['ZTT', 'ZLL']).AddSyst(
    cb, 'CMS_$ANALYSIS_mm_BDT_DY', 'lnN', ch.SystMap('process')
        (['ZTT'],  1.033)
        (['ZLL'],  1.052))

# W xsec uncertainty only applied to tt and em. et and mt use data-driven method
cb.cp().process(['W']).AddSyst(
    cb, 'CMS_$ANALYSIS_wjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['tt', 'em', 'mm'],  1.04))
# Give each channel an independent extrap uncertainty
cb.cp().process(['W']).AddSyst(
    cb, 'CMS_$ANALYSIS_wjExtrapol_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'tt', 'em'],  1.20))

cb.cp().process(['ZJ', 'ZJ', 'ZLL']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'tt', 'em', 'mm'],  1.04))

# KIT cards only have one zllFakeTau param, but need at least three:
#  - e->tau fake rate
#  - mu->tau fake rate (CV: use 100% uncertainty for now, as no measurement of mu->tau fake-rate in Run 2 data available yet)
#  - jet->tau fake rate
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_eFakeTau_loose_$ERA', 'lnN', ch.SystMap('channel')
        (['tt'],  1.10))
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_eFakeTau_tight_$ERA', 'lnN', ch.SystMap('channel')
        (['et'],  1.30))
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_mFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  2.00))
cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_$CHANNEL_zllNorm', 'lnN', ch.SystMap('channel')
        (['em'],  1.20))

cb.cp().process(['ZJ']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['et', 'mt', 'tt'],  1.30))

cb.cp().AddSyst(
    cb, 'lumi_$ERA', 'lnN', ch.SystMap('channel', 'process')
        (['et', 'mt'],  ['ZTT', 'ZL', 'ZJ', 'TT', 'VV'],        1.027)
        (['tt'],        ['ZTT', 'ZL', 'ZJ', 'TT', 'VV', 'W'],   1.027)
        (['em'],        ['ZTT', 'ZLL', 'TT', 'VV', 'W'],        1.027)
        (['mm'],        ['ZTT', 'ZLL', 'TT', 'VV', 'W'],        1.027))

# Signal acceptance
cb.cp().process(['ZTT']).AddSyst(
    cb, 'CMS_$ANALYSIS_pdf_$ERA', 'lnN', ch.SystMap()(1.015))
cb.cp().process(['ZTT']).AddSyst(
    cb, 'CMS_$ANALYSIS_QCDscale_$ERA', 'lnN', ch.SystMap()(1.005))
cb.cp().process(['ZTT']).channel(['tt']).AddSyst(
    cb, 'CMS_$ANALYSIS_QCDscale_$CHANNEL_$ERA', 'lnN', ch.SystMap()(1.06))


##########################################################################
# Load the shapes
##########################################################################
for chn in channels:
    cb.cp().channel([chn]).ExtractShapes(
        '%s/%s/%s' % (shapes_dir, inputs[chn], files[chn][inputs[chn]][variable]),
        '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

##########################################################################
# Tau ES modifcations
##########################################################################
# Now we manipulate the tau ES a bit
# First rename to a common 'CMS_scale_t'
cb.ForEachSyst(lambda sys: RenameSyst(cb, sys, 'CMS_scale_t', 'CMS_scale_t'))

# Then scale the constraint to 2.5%/3%:
tau_es_scaling = 2.5/3.0
# Unless the tau ES is going to be floating, in which case don't rescale
if not args.constrain_tau_scale:
    tau_es_scaling = 1.0

cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(lambda sys: sys.set_scale(tau_es_scaling))


def ChannelSpecificTauES(sys, scale=1.0):
    sys.set_name('CMS_scale_t_' + sys.channel())
    sys.set_scale(scale)

# Now clone back to a channel specific one scaled to 1.5%
ch.CloneSysts(cb.cp().syst_name(['CMS_scale_t']), cb,
              lambda sys: ChannelSpecificTauES(sys, 0.5))

if not args.constrain_tau_scale:
    print '>> Info: Tau energy scale will be unconstrained'
    cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(
        lambda sys: sys.set_type('shapeU'))
else:
    print '>> Info: Tau energy scale will be constrained'


##########################################################################
# Create bin-by-bin
##########################################################################
bbb = ch.BinByBinFactory()
bbb.SetPattern('CMS_$ANALYSIS_$BIN_$ERA_$PROCESS_bin_$#')
bbb.SetAddThreshold(0.1)
bbb.SetMergeThreshold(0.5)  # For now we merge, but to be checked
bbb.SetFixNorm(True)
bbb.MergeAndAdd(cb.cp().backgrounds(), cb)


##########################################################################
# Set nuisance parameter groups
##########################################################################
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


##########################################################################
# Write the cards
##########################################################################
writer = ch.CardWriter('$TAG/datacard.txt',
                       '$TAG/shapes.root')
writer.SetWildcardMasses([])  # We don't use the $MASS property here
writer.SetVerbosity(1)
x = writer.WriteCards('%s/cmb' % args.output, cb)  # All cards combined
print x
x['%s/cmb/datacard.txt' % args.output].PrintAll()
for chn in channels:  # plus a subdir per channel
    writer.WriteCards('%s/%s' % (args.output, chn), cb.cp().channel([chn]))
