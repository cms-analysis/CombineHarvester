import CombineHarvester.CombineTools.ch as ch
import ROOT
import os
import pprint
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='path to directory containing the moriond2016 directory', default='.')

args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')



cb = ch.CombineHarvester()
cb.SetFlag('workspace-uuid-recycle', False)
cb.SetFlag('workspaces-use-clone', True)
cb.SetFlag('import-parameter-err', False)

# cb.SetVerbosity(3)

l_pre = os.path.join(args.i, 'moriond2016/couplings/ttH/')
l_cards = [
    'ttH_2lss_1tau.card.txt',
    'ttH_2lss_ee_0tau_neg.card.txt',
    'ttH_2lss_ee_0tau_pos.card.txt',
    'ttH_2lss_em_0tau_bl_neg.card.txt',
    'ttH_2lss_em_0tau_bl_pos.card.txt',
    'ttH_2lss_em_0tau_bt_neg.card.txt',
    'ttH_2lss_em_0tau_bt_pos.card.txt',
    'ttH_2lss_mm_0tau_bl_neg.card.txt',
    'ttH_2lss_mm_0tau_bl_pos.card.txt',
    'ttH_2lss_mm_0tau_bt_neg.card.txt',
    'ttH_2lss_mm_0tau_bt_pos.card.txt',
    'ttH_3l_bl_neg.card.txt',
    'ttH_3l_bl_pos.card.txt',
    'ttH_3l_bt_neg.card.txt',
    'ttH_3l_bt_pos.card.txt'
]

b_pre = os.path.join(args.i, 'moriond2016/couplings/ttH/')
b_cards = [
    'ttH_hbb_13TeV_dl_3j2t.txt',
    'ttH_hbb_13TeV_dl_3j3t.txt',
    'ttH_hbb_13TeV_dl_ge4j2t.txt',
    'ttH_hbb_13TeV_dl_ge4j3t.txt',
    'ttH_hbb_13TeV_dl_ge4jge4t.txt',
    'ttH_hbb_13TeV_sl_4j3t.txt',
    'ttH_hbb_13TeV_sl_4j4t_high.txt',
    'ttH_hbb_13TeV_sl_4j4t_low.txt',
    'ttH_hbb_13TeV_sl_5j3t.txt',
    'ttH_hbb_13TeV_sl_5jge4t_high.txt',
    'ttH_hbb_13TeV_sl_5jge4t_low.txt',
    'ttH_hbb_13TeV_sl_boost.txt',
    'ttH_hbb_13TeV_sl_ge6j2t.txt',
    'ttH_hbb_13TeV_sl_ge6j3t.txt',
    'ttH_hbb_13TeV_sl_ge6jge4t_high.txt',
    'ttH_hbb_13TeV_sl_ge6jge4t_low.txt'
]

g_pre = os.path.join(args.i, 'moriond2016/couplings/hgg/')
g_cards = [
    'Datacard_13TeV_HggAnalysis_290216_TTH.txt'
]

for card in l_cards:
    cb.ParseDatacard(l_pre + card, analysis='ttH', channel='leptons', mass='125')

for card in b_cards:
    cb.ParseDatacard(b_pre + card, analysis='ttH', channel='bb', mass='125')

for card in g_cards:
    cb.ParseDatacard(g_pre + card, analysis='ttH', channel='gg', mass='125')

# cb.SetGroup('blah1', ['.*'])
# cb.SetGroup('blah2', ['.*_norm'])
# cb.RemoveGroup('blah1', ['.*tau.*', '.*qcd.*'])
# cb.RenameGroup('blah1', 'blah3')
# cb.PrintAll()

# cb.syst_name(['blah'], False)


sig_procs_in_bins = defaultdict(set)

print '>> Signal processes: '
pprint.pprint(cb.cp().signals().process_set(), indent=4)

for p in cb.cp().signals().process_set():
    for b in cb.cp().process([p]).bin_set():
        sig_procs_in_bins[p].add(b)

# print '>> Signal processes in bins: '
# pprint.pprint(dict(sig_procs_in_bins), indent=4)


# cb.PrintObs()

# cb.WriteDatacard('ttH_hgg.txt', 'ttH_hgg.root')
cb.WriteDatacard('ttH_comb.txt', 'ttH_comb.inputs.root')

# Also write per-analysis cards for cross-checking
for chn in cb.channel_set():
    print chn
    cb.cp().channel([chn]).WriteDatacard(
        'ttH_%s.txt' % chn, 'ttH_%s.inputs.root' % chn)

cards = ' '.join(
    [x.replace('.txt', '=')+b_pre+x for x in b_cards] +
    [x.replace('.txt', '=').replace('ttH','ttH_hww')+l_pre+x for x in l_cards] +
    [x.replace('.txt', '=').replace('TTH','ttH_hgg')+g_pre+x for x in g_cards])
print 'combineCards.py %s &> ttH_comb_def.txt' % cards

os.system('combineCards.py %s &> ttH_comb_def.txt' % cards)

cards_b = ' '.join(
    [x.replace('.txt', '=')+b_pre+x for x in b_cards])

cards_l = ' '.join(
    [x.replace('.txt', '=').replace('ttH','ttH_hww')+l_pre+x for x in l_cards])

cards_g = ' '.join(
    [x.replace('.txt', '=').replace('TTH','ttH_hgg')+g_pre+x for x in g_cards])

os.system('combineCards.py %s &> ttH_leptons_def.txt' % cards_l)
os.system('combineCards.py %s &> ttH_bb_def.txt' % cards_b)
os.system('combineCards.py %s &> ttH_gg_def.txt' % cards_g)

# cb.process(['wmu'], False)

# cb.WriteDatacard('test.txt')
