#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import os

cb = ch.CombineHarvester()

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/auxiliaries/'
aux_shapes   = auxiliaries +'shapes/'

procs = {
  'sig'  : ['tH_YtMinus', 'tHW'],
  'sim'  : ['WZ', 'ZZ', 'ttW', 'ttZ', 'ttH'],
  'bkg'  : ['WZ','ZZ','ttW','ttZ','ttH','reducible']
}

cats = [(0, 'emt'), (1, 'mmt')]

masses = ['125']

cb.AddObservations(   ['*'], ['htt'], ["8TeV"], ['th'],               cats         )
cb.AddProcesses(      ['*'], ['htt'], ["8TeV"], ['th'], procs['bkg'], cats, False  )
cb.AddProcesses(     masses, ['htt'], ["8TeV"], ['th'], procs['sig'], cats, True   )

print('>> Adding systematic uncertainties...')

cb.cp().process(procs['sig'] + procs['sim']).AddSyst(
    cb, 'lumi_$ERA', 'lnN', ch.SystMap()(1.026))

cb.cp().process(procs['sig']).AddSyst(
    cb, 'CMS_th_sig_trigger_$BIN_$ERA', 'lnN', ch.SystMap('bin')(['emt'], 1.05)(['mmt'], 1.06))

cb.cp().process(procs['sig'] + procs['sim']).AddSyst(
    cb, 'CMS_th_eff_e_$ERA', 'lnN', ch.SystMap('bin')(['emt'], 1.051))

cb.cp().process(procs['sig'] + procs['sim']).AddSyst(
    cb, 'CMS_th_eff_m_$ERA', 'lnN', ch.SystMap('bin')(['emt'], 1.051)(['mmt'], 1.102))

cb.cp().process(procs['sig'] + procs['sim']).AddSyst(
    cb, 'CMS_th_eff_t_$ERA', 'lnN', ch.SystMap()(1.06))

cb.cp().process(procs['sig'] + procs['sim']).AddSyst(
    cb, 'CMS_th_scale_t_$ERA', 'lnN', ch.SystMap()(1.03))

cb.cp().process(procs['sig'] + ['ttW', 'ttH', 'ZZ', 'WZ']).AddSyst(
    cb, 'CMS_scale_j_$ERA', 'lnN', ch.SystMap()(1.01))

cb.cp().AddSyst(
    cb, 'CMS_th_mc_stats_$PROCESS_$BIN_$ERA', 'lnN', ch.SystMap('bin', 'process')
      (['emt'], ['ttZ'], 1.18)
      (['emt'], ['ttW'], 1.14)
      (['emt'], ['ttH'], 1.06)
      (['emt'], ['ZZ'],  1.10)
      (['emt'], ['WZ'],  1.12)
      (['mmt'], ['ttZ'], 1.27)
      (['mmt'], ['ttW'], 1.18)
      (['mmt'], ['ttH'], 1.09)
      (['mmt'], ['ZZ'],  1.15)
      (['mmt'], ['WZ'],  1.18))

cb.cp().AddSyst(
    cb, 'CMS_eff_b_$ERA', 'lnN', ch.SystMap('process')
      (procs['sig'],           1.05)
      (['ttH', 'ttW', 'ttZ'],  1.03))

cb.cp().AddSyst(
    cb, 'CMS_fake_b_$ERA', 'lnN', ch.SystMap('process')
      (['WZ', 'ZZ'],           1.20))

cb.cp().process(['reducible']).AddSyst(
    cb, 'CMS_th_reducible_$BIN_$ERA', 'lnN', ch.SystMap('bin')
      (['emt'], 1.50)(['mmt'], 1.50))

cb.cp().process(procs['sig']).AddSyst(cb, 'QCDscale_tHq', 'lnN', ch.SystMap()(1.019))
cb.cp().process(['ttH']).AddSyst(cb, 'QCDscale_ttH', 'lnN', ch.SystMap()(1.067))
cb.cp().process(['ttW']).AddSyst(cb, 'QCDscale_ttW', 'lnN', ch.SystMap()(1.105))
cb.cp().process(['ttZ']).AddSyst(cb, 'QCDscale_ttW', 'lnN', ch.SystMap()(1.116))
cb.cp().process(['WW', 'ZZ']).AddSyst(cb, 'QCDscale_VV', 'lnN', ch.SystMap()(1.036))

cb.cp().AddSyst(
    cb, 'pdf_gg', 'lnN', ch.SystMap('process')
      (['ttZ'], 0.919)(['ttH'], 0.926))

cb.cp().AddSyst(
    cb, 'pdf_qqbar', 'lnN', ch.SystMap('process')
      (['tH_YtMinus'], 1.048)(['ttW'], 1.072)(['WZ','ZZ'], 1.040))

cb.cp().AddSyst(
    cb, 'pdf_qg', 'lnN', ch.SystMap('process')
      (['tHW'], 1.048))


print('>> Extracting histograms from input root files...')
file = aux_shapes + 'CERN/htt_th.inputs-sm-8TeV.root'
cb.cp().backgrounds().ExtractShapes(
    file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
cb.cp().signals().ExtractShapes(
    file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')


print('>> Generating bbb uncertainties...')
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetFixNorm(True)
bbb.AddBinByBin(cb.cp().process(['reducible']), cb)


print('>> Setting standardised bin names...')
ch.SetStandardBinNames(cb)
cb.PrintAll()

writer = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       '$TAG/common/$ANALYSIS_$CHANNEL.input.root')
writer.SetVerbosity(1)
writer.WriteCards('output/sm_cards/LIMITS', cb)

print('>> Done!')
