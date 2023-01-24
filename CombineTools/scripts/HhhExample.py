#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombineTools.systematics.Hhh as HhhSysts
import ROOT as R
import glob
import os

cb = ch.CombineHarvester()

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/auxiliaries/'
aux_shapes   = auxiliaries +'shapes/'

chns = ['et', 'mt', 'tt']

input_folders = {
  'et' : 'Imperial',
  'mt' : 'Imperial',
  'tt' : 'Italians',
}

bkg_procs = {
  'et' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'mt' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'tt' : ['ZTT', 'W', 'QCD', 'ZLL', 'TT', 'VV'],
}

sig_procs = ['ggHTohhTo2Tau2B']

cats = {
  'et_8TeV' : [
    (0, 'eleTau_2jet0tag'),
    (1, 'eleTau_2jet1tag'),
    (2, 'eleTau_2jet2tag')
  ],
  'mt_8TeV' : [
    (0, 'muTau_2jet0tag'),
    (1, 'muTau_2jet1tag'),
    (2, 'muTau_2jet2tag')
  ],
  'tt_8TeV' : [
    (0, 'tauTau_2jet0tag'),
    (1, 'tauTau_2jet1tag'),
    (2, 'tauTau_2jet2tag')
  ]
}

masses = ch.ValsFromRange('260:350|10')

print('>> Creating processes and observations...')

for chn in chns:
    cb.AddObservations(  ['*'],  ['htt'], ['8TeV'], [chn],                 cats[chn+"_8TeV"]      )
    cb.AddProcesses(     ['*'],  ['htt'], ['8TeV'], [chn], bkg_procs[chn], cats[chn+"_8TeV"], False  )
    cb.AddProcesses(     masses, ['htt'], ['8TeV'], [chn], sig_procs,      cats[chn+"_8TeV"], True   )

#Remove W background from 2jet1tag and 2jet2tag categories for tt channel
cb.FilterProcs(lambda p : p.bin() == 'tauTau_2jet1tag' and p.process() == 'W')
cb.FilterProcs(lambda p : p.bin() == 'tauTau_2jet2tag' and p.process() == 'W')

print('>> Adding systematic uncertainties...')
HhhSysts.AddSystematics_hhh_et_mt(cb)
HhhSysts.AddSystematics_hhh_tt(cb)

print('>> Extracting histograms from input root files...')
for chn in chns:
    file = aux_shapes + input_folders[chn] + "/htt_" + chn + ".inputs-Hhh-8TeV.root"
    cb.cp().channel([chn]).era(['8TeV']).backgrounds().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).era(['8TeV']).signals().ExtractShapes(
        file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')

print('>> Merging bin errors and generating bbb uncertainties...')
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)

cb_et = cb.cp().channel(['et'])
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_mt = cb.cp().channel(['mt'])
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_tt = cb.cp().channel(['tt'])
bbb.MergeAndAdd(cb_tt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZLL','VV','ZTT','TT']), cb)

print('>> Setting standardised bin names...')
ch.SetStandardBinNames(cb)

writer = ch.CardWriter('LIMITS/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       'LIMITS/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
#writer.SetVerbosity(1)
writer.WriteCards('cmb', cb)
for chn in chns: writer.WriteCards(chn,cb.cp().channel([chn]))

print('>> Done!')
