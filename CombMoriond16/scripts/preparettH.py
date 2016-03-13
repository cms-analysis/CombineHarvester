import CombineHarvester.CombineTools.ch as ch
import ROOT
import os
import pprint
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', help='path to directory containing the moriond2016 directory', default='.')

args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')


cb = ch.CombineHarvester()
cb.SetFlag('workspace-uuid-recycle', False)
cb.SetFlag('workspaces-use-clone', True)
cb.SetFlag('import-parameter-err', False)
cb.SetFlag('filters-use-regex', True)

# cb.SetVerbosity(3)
l_pre = os.path.join(
    args.i, 'moriond2016/couplings/ttH/splitted_decay_channels/')
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
    'CMS-HGG_mva_13TeV_datacard.txt'
]

for card in l_cards:
    cb.ParseDatacard(l_pre + card, analysis='ttH', channel='leptons', mass='*')

for card in b_cards:
    cb.ParseDatacard(b_pre + card, analysis='ttH', channel='bb', mass='*')

for card in g_cards:
    cb.ParseDatacard(g_pre + card, analysis='ttH', channel='gg', mass='*')

# Temporarily using inclusive hgg card so filter everything that's not
# TTH
cb.FilterAll(lambda x:
             x.channel() == 'gg' and not x.bin().startswith('TTH'))

# cb.SetGroup('blah1', ['.*'])
# cb.SetGroup('blah2', ['.*_norm'])
# cb.RemoveGroup('blah1', ['.*tau.*', '.*qcd.*'])
# cb.RenameGroup('blah1', 'blah3')
# cb.PrintAll()

# cb.syst_name(['blah'], False)

modify_systs = True

def Set_QCDscale_ttH(sys):
    sys.set_asymm(True)
    sys.set_value_u(1.058)
    sys.set_value_d(0.908)

if modify_systs:
    cb.cp().channel(['gg']).signals().ForEachProc(
        lambda x: x.set_process(x.process() + '_hgg'))
    cb.cp().channel(['gg']).signals().ForEachSyst(
        lambda x: x.set_process(x.process() + '_hgg'))

    cb.cp().channel(['gg']).process(['ggH.*']).syst_name(
        ['QCDscale_gg']).ForEachSyst(lambda x: x.set_name('QCDscale_ggH'))
    cb.cp().channel(['gg']).process(['ttH.*']).syst_name(
        ['QCDscale_gg']).ForEachSyst(lambda x: x.set_name('QCDscale_ttH'))
    cb.cp().channel(['gg']).process(['WH.*', 'ZH.*']).syst_name(
        ['QCDscale_qqbar']).ForEachSyst(lambda x: x.set_name('QCDscale_VH'))
    cb.cp().channel(['gg']).process(['qqH.*']).syst_name(
        ['QCDscale_qqbar']).ForEachSyst(lambda x: x.set_name('QCDscale_qqH'))

    cb.cp().channel(['gg']).process(['ggH.*']).syst_name(
        ['pdf_alphaS_gg']).ForEachSyst(lambda x: x.set_name('pdf_Higgs_gg'))
    cb.cp().channel(['gg']).process(['ttH.*']).syst_name(
        ['pdf_alphaS_gg']).ForEachSyst(lambda x: x.set_name('pdf_Higgs_ttH'))
    cb.cp().channel(['gg']).signals().syst_name(
        ['pdf_alphaS_qqbar']).ForEachSyst(lambda x: x.set_name('pdf_Higgs_qq'))

    cb.cp().channel(['bb']).process(['ttH.*']).syst_name(
        ['pdf_gg_ttH']).ForEachSyst(lambda x: x.set_name('pdf_Higgs_ttH'))

    # gg has 0.964 for pdf_Higgs_ttH, to give anti-correlation with ggH,
    # but since LHC comb treat these as decorrelated, so set to 1.036 instead
    # to be in-line with other channels
    cb.cp().channel(['gg']).process(['ttH.*']).syst_name(
        ['pdf_Higgs_ttH']).ForEachSyst(lambda x: x.set_value_u(1.036))

    cb.cp().process(['ttH.*']).syst_name(
        ['QCDscale_ttH']).ForEachSyst(lambda x: Set_QCDscale_ttH(x))



sig_procs_in_bins = defaultdict(set)


print '>> Signal processes: '
pprint.pprint(cb.cp().signals().process_set(), indent=4)

for p in cb.cp().signals().process_set():
    for b in cb.cp().process([p]).SetFromProcs(lambda x: (x.channel(), x.bin())):
        sig_procs_in_bins[p].add(b)

print '>> Signal processes in bins: '
pprint.pprint(dict(sig_procs_in_bins), indent=4)

sig_systs_in_chns = defaultdict(set)

for syst in cb.cp().signals().syst_name_set():
    sig_systs_in_chns[syst] = cb.cp().syst_name(
        [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

print '>> Signal systematics in channels: '
pprint.pprint(dict(sig_systs_in_chns), indent=4)

correlated_systs = defaultdict(set)
for syst in cb.cp().syst_name_set():
    if len(cb.cp().syst_name([syst]).SetFromSysts(lambda x: x.channel())) > 1:
        correlated_systs[syst] = cb.cp().syst_name(
            [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

print '>> Correlated systematics in channels: '
pprint.pprint(dict(correlated_systs), indent=4)

cb.cp().syst_name(['pdf_Higgs_ttH']).PrintSysts()
cb.cp().syst_name(['QCDscale_ttH']).PrintSysts()
cb.cp().syst_name(['lumi_13TeV']).PrintSysts()

# cb.WriteDatacard('ttH_hgg.txt', 'ttH_hgg.root')
cb.WriteDatacard('ttH_comb.txt', 'ttH_comb.inputs.root')

# Also write per-analysis cards for cross-checking
for chn in cb.channel_set():
    cb.cp().channel([chn]).WriteDatacard(
        'ttH_%s.txt' % chn, 'ttH_%s.inputs.root' % chn)

cards = ' '.join(
    [x.replace('.txt', '=') + b_pre + x for x in b_cards] +
    [x.replace('.txt', '=').replace('ttH', 'ttH_hww') + l_pre + x for x in l_cards] +
    [x.replace('.txt', '=').replace('TTH', 'ttH_hgg') + g_pre + x for x in g_cards])
print 'combineCards.py %s &> ttH_comb_def.txt' % cards

os.system('combineCards.py %s &> ttH_comb_def.txt' % cards)

cards_b = ' '.join(
    [x.replace('.txt', '=') + b_pre + x for x in b_cards])

cards_l = ' '.join(
    [x.replace('.txt', '=').replace('ttH', 'ttH_hww') + l_pre + x for x in l_cards])

cards_g = ' '.join(
    [x.replace('.txt', '=').replace('TTH', 'ttH_hgg') + g_pre + x for x in g_cards])

os.system('combineCards.py %s &> ttH_leptons_def.txt' % cards_l)
os.system('combineCards.py %s &> ttH_bb_def.txt' % cards_b)
os.system('combineCards.py %s &> ttH_gg_def.txt' % cards_g)

# cb.process(['wmu'], False)

# cb.WriteDatacard('test.txt')
