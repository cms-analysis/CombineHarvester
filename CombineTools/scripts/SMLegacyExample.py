#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombineTools.systematics.SMLegacy as SMLegacySysts
import ROOT as R
import glob
import os

cb = ch.CombineHarvester()

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/auxiliaries/'
aux_shapes   = auxiliaries +'shapes/'
aux_pruning  = auxiliaries +'pruning/'
input_dir    = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/CombineTools/input';

chns = ['et', 'mt', 'em', 'ee', 'mm', 'tt']

input_folders = {
  'et' : 'Imperial',
  'mt' : 'Imperial',
  'em' : 'MIT',
  'ee' : 'DESY-KIT',
  'mm' : 'DESY-KIT',
  'tt' : 'CERN'
}

bkg_procs = {
  'et' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'mt' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'em' : ['Ztt', 'EWK', 'Fakes', 'ttbar', 'ggH_hww125', 'qqH_hww125'],
  'ee' : ['ZTT', 'WJets', 'QCD', 'ZEE', 'TTJ', 'Dibosons', 'ggH_hww125', 'qqH_hww125'],
  'mm' : ['ZTT', 'WJets', 'QCD', 'ZMM', 'TTJ', 'Dibosons', 'ggH_hww125', 'qqH_hww125'],
  'tt' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV']
}

sig_procs = ['ggH', 'qqH', 'WH', 'ZH']

cats = {
  'et_7TeV' : [
    (1, 'eleTau_0jet_medium'), (2, 'eleTau_0jet_high'),
    (3, 'eleTau_1jet_medium'), (5, 'eleTau_1jet_high_mediumhiggs'),
    (6, 'eleTau_vbf')
  ],
  'et_8TeV' : [
    (1, 'eleTau_0jet_medium'), (2, 'eleTau_0jet_high'),
    (3, 'eleTau_1jet_medium'), (5, 'eleTau_1jet_high_mediumhiggs'),
    (6, 'eleTau_vbf_loose'),   (7, 'eleTau_vbf_tight')
  ],
  'mt_7TeV' : [
    (1, 'muTau_0jet_medium'), (2, 'muTau_0jet_high'),
    (3, 'muTau_1jet_medium'), (4, 'muTau_1jet_high_lowhiggs'), (5, 'muTau_1jet_high_mediumhiggs'),
    (6, 'muTau_vbf')
  ],
  'mt_8TeV' : [
    (1, 'muTau_0jet_medium'), (2, 'muTau_0jet_high'),
    (3, 'muTau_1jet_medium'), (4, 'muTau_1jet_high_lowhiggs'), (5, 'muTau_1jet_high_mediumhiggs'),
    (6, 'muTau_vbf_loose'),   (7, 'muTau_vbf_tight')
  ],
  'em_7TeV' : [
    (0, 'emu_0jet_low'), (1, 'emu_0jet_high'),
    (2, 'emu_1jet_low'), (3, 'emu_1jet_high'),
    (4, 'emu_vbf_loose')
  ],
  'em_8TeV' : [
    (0, 'emu_0jet_low'),  (1, 'emu_0jet_high'),
    (2, 'emu_1jet_low'),  (3, 'emu_1jet_high'),
    (4, 'emu_vbf_loose'), (5, 'emu_vbf_tight')
  ],
  'ee_7TeV' : [
    (0, 'ee_0jet_low'), (1, 'ee_0jet_high'),
    (2, 'ee_1jet_low'), (3, 'ee_1jet_high'),
    (4, 'ee_vbf')
  ],
  'mm_7TeV' : [
    (0, 'mumu_0jet_low'), (1, 'mumu_0jet_high'),
    (2, 'mumu_1jet_low'), (3, 'mumu_1jet_high'),
    (4, 'mumu_vbf')
  ],
  'tt_7TeV' : [],
  'tt_8TeV' : [
    (0, 'tauTau_1jet_high_mediumhiggs'), (1, 'tauTau_1jet_high_highhiggs'),
    (2, 'tauTau_vbf')
  ]
}
cats['ee_8TeV'] = cats['ee_7TeV']
cats['mm_8TeV'] = cats['mm_7TeV']

masses = ch.ValsFromRange('110:145|5')

print('>> Creating processes and observations...')

for era in ['7TeV', '8TeV']:
    for chn in chns:
        cb.AddObservations(   ['*'], ['htt'], [era], [chn],                 cats[chn+"_"+era]         )
        cb.AddProcesses(      ['*'], ['htt'], [era], [chn], bkg_procs[chn], cats[chn+"_"+era], False  )
        cb.AddProcesses(     masses, ['htt'], [era], [chn], sig_procs,      cats[chn+"_"+era], True   )

#Have to drop ZL from tautau_vbf category
cb.FilterProcs(lambda p : p.bin() == 'tauTau_vbf' and p.process() == 'ZL')

print('>> Adding systematic uncertainties...')
SMLegacySysts.AddSystematics_et_mt(cb)
SMLegacySysts.AddSystematics_em(cb)
SMLegacySysts.AddSystematics_ee_mm(cb)
SMLegacySysts.AddSystematics_tt(cb)

print('>> Extracting histograms from input root files...')
for era in ['7TeV', '8TeV']:
    for chn in chns:
        if chn == 'tt' and era == '7TeV': continue
        file = aux_shapes + input_folders[chn] + "/htt_" + chn + ".inputs-sm-" + era + "-hcg.root"
        cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
            file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
            file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')

print('>> Scaling signal process rates...')
xs = { }
# Get the table of H->tau tau BRs vs mass
xs['htt'] = ch.TGraphFromTable(input_dir+'/xsecs_brs/htt_YR3.txt', 'mH', 'br')
for e in ['7TeV', '8TeV']:
    for p in sig_procs:
        # Get the table of xsecs vs mass for process 'p' and era 'e':
        xs[p+'_'+e] = ch.TGraphFromTable(input_dir+'/xsecs_brs/'+p+'_'+e+'_YR3.txt', 'mH', 'xsec')
        print('>>>> Scaling for process ' + p + ' and era ' + e)
        cb.cp().process([p]).era([e]).ForEachProc(
          lambda x : x.set_rate(
            x.rate() * xs[p+'_'+e].Eval(float(x.mass())) * xs['htt'].Eval(float(x.mass())))
        )
xs['hww_over_htt'] = ch.TGraphFromTable(input_dir+'/xsecs_brs/hww_over_htt.txt', 'mH', 'ratio')

for e in ['7TeV', '8TeV']:
    for p in sig_procs:
        cb.cp().channel(['em']).process([p+'_hww125']).era([e]).ForEachProc(
          lambda x : x.set_rate(
            x.rate() * xs[p+'_'+e].Eval(125.) * xs['htt'].Eval(125.) * xs['hww_over_htt'].Eval(125.))
        )

print('>> Merging bin errors and generating bbb uncertainties...')
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)

cb_et = cb.cp().channel(['et'])
bbb.MergeAndAdd(cb_et.cp().era(['7TeV']).bin_id([1, 2]).process(['ZL', 'ZJ', 'QCD', 'W']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['7TeV']).bin_id([3, 5]).process(['W']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([1, 2]).process(['ZL', 'ZJ', 'QCD', 'W']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([3, 5]).process(['W']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['7TeV']).bin_id([6]).process(['ZL', 'ZJ', 'W', 'ZTT']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([6]).process(['ZL', 'ZJ', 'W']), cb)
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([7]).process(['ZL', 'ZJ', 'W', 'ZTT']), cb)
cb_mt = cb.cp().channel(['mt'])
bbb.MergeAndAdd(cb_mt.cp().era(['7TeV']).bin_id([1, 2, 3, 4]).process(['W', 'QCD']), cb)
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([1, 2, 3, 4]).process(['W', 'QCD']), cb)
bbb.MergeAndAdd(cb_mt.cp().era(['7TeV']).bin_id([5]).process(['W']), cb)
bbb.MergeAndAdd(cb_mt.cp().era(['7TeV']).bin_id([6]).process(['W', 'ZTT']), cb)
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([5, 6]).process(['W']), cb)
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([7]).process(['W', 'ZTT']), cb)
cb_em = cb.cp().channel(['em'])
bbb.MergeAndAdd(cb_em.cp().era(['7TeV']).bin_id([1, 3]).process(['Fakes']), cb)
bbb.MergeAndAdd(cb_em.cp().era(['8TeV']).bin_id([1, 3]).process(['Fakes']), cb)
bbb.MergeAndAdd(cb_em.cp().era(['7TeV']).bin_id([4]).process(['Fakes', 'EWK', 'Ztt']), cb)
bbb.MergeAndAdd(cb_em.cp().era(['8TeV']).bin_id([5]).process(['Fakes', 'EWK', 'Ztt']), cb)
bbb.MergeAndAdd(cb_em.cp().era(['8TeV']).bin_id([4]).process(['Fakes', 'EWK']), cb)
cb_tt = cb.cp().channel(['tt'])
bbb.MergeAndAdd(cb_tt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['ZTT', 'QCD']), cb)
bbb.SetAddThreshold(0.)  # ee and mm use a different threshold
cb_ll = cb.cp().channel(['ee', 'mm'])
bbb.MergeAndAdd(cb_ll.cp().era(['7TeV']).bin_id([1, 3, 4]).process(['ZTT', 'ZEE', 'ZMM', 'TTJ']), cb)
bbb.MergeAndAdd(cb_ll.cp().era(['8TeV']).bin_id([1, 3, 4]).process(['ZTT', 'ZEE', 'ZMM', 'TTJ']), cb)

print('>> Setting standardised bin names...')
ch.SetStandardBinNames(cb)

to_drop = [line.rstrip('\n') for line in open(aux_pruning + 'uncertainty-pruning-drop-131128-sm.txt')]
print('>> Droplist contains ' + str(len(to_drop)) + ' entries')
pre_drop = cb.syst_name_set()
cb.syst_name(to_drop, False)
post_drop = cb.syst_name_set()
print('>> Systematics dropped: ' + str(len(pre_drop) - len(post_drop)))

writer = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       '$TAG/common/$ANALYSIS_$CHANNEL.input.root')
# writer.SetVerbosity(1)
writer.WriteCards('output/sm_cards/cmb', cb)
# Also create directory structure for per-channel cards
for chn in cb.channel_set():
    writer.WriteCards('output/sm_cards/'+chn, cb.cp().channel([chn]))

print('>> Done!')
