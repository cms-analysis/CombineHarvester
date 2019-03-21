import ROOT
import json
import argparse
import pprint
import re
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input workspace')
parser.add_argument('--attributes', default=None, help='json file containing the attributes')
parser.add_argument('--ignore', default=None, help='Ignore any parameter matching one of these groups')
parser.add_argument('--dump', action='store_true', help='dump channel/attrib assignments')
parser.add_argument('--prefix', default='', help='prefix for the output file')

args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

attributes = {}
with open(args.attributes) as jsonfile:
    attributes = json.load(jsonfile)
att_labels = [x for x in attributes.keys() if x.startswith('p')]
print att_labels

reject_patterns = []
if args.ignore is not None:
    for grp in args.ignore.split(','):
        reject_patterns.extend(attributes[grp])

channel_bin_dict = {   'ggHbb': set([   'cat1_fail_cat1',
                     'cat1_pass_cat1',
                     'cat2_fail_cat2',
                     'cat2_pass_cat2',
                     'cat3_fail_cat3',
                     'cat3_pass_cat3',
                     'cat4_fail_cat4',
                     'cat4_pass_cat4',
                     'cat5_fail_cat5',
                     'cat5_pass_cat5',
                     'cat6_fail_cat6',
                     'cat6_pass_cat6',
                     'muonCR_fail_muonCR',
                     'muonCR_pass_muonCR']),
    'hgg': set([   'TTHHadronicTag_13TeV',
                   'TTHLeptonicTag_13TeV',
                   'UntaggedTag_0_13TeV',
                   'UntaggedTag_1_13TeV',
                   'UntaggedTag_2_13TeV',
                   'UntaggedTag_3_13TeV',
                   'VBFTag_0_13TeV',
                   'VBFTag_1_13TeV',
                   'VBFTag_2_13TeV',
                   'VHHadronicTag_13TeV',
                   'VHLeptonicLooseTag_13TeV',
                   'VHMetTag_13TeV',
                   'WHLeptonicTag_13TeV',
                   'ZHLeptonicTag_13TeV']),
    'hinv': set([   'VH_hinv_ch1',
                    'VH_hinv_ch2',
                    'VH_hinv_ch3',
                    'VH_hinv_ch4',
                    'VH_hinv_ch5',
                    'VH_hinv_ch6',
                    'ZH_hinv_ch1_ch1',
                    'ZH_hinv_ch1_ch10',
                    'ZH_hinv_ch1_ch11',
                    'ZH_hinv_ch1_ch12',
                    'ZH_hinv_ch1_ch2',
                    'ZH_hinv_ch1_ch3',
                    'ZH_hinv_ch1_ch4',
                    'ZH_hinv_ch1_ch5',
                    'ZH_hinv_ch1_ch6',
                    'ZH_hinv_ch1_ch7',
                    'ZH_hinv_ch1_ch8',
                    'ZH_hinv_ch1_ch9',
                    'ZH_hinv_ch2_ch1',
                    'ZH_hinv_ch2_ch10',
                    'ZH_hinv_ch2_ch11',
                    'ZH_hinv_ch2_ch2',
                    'ZH_hinv_ch2_ch3',
                    'ZH_hinv_ch2_ch4',
                    'ZH_hinv_ch2_ch5',
                    'ZH_hinv_ch2_ch6',
                    'ZH_hinv_ch2_ch7',
                    'ZH_hinv_ch2_ch8',
                    'ZH_hinv_ch2_ch9',
                    'ZH_hinv_ch3_ch1',
                    'ZH_hinv_ch3_ch10',
                    'ZH_hinv_ch3_ch11',
                    'ZH_hinv_ch3_ch2',
                    'ZH_hinv_ch3_ch3',
                    'ZH_hinv_ch3_ch4',
                    'ZH_hinv_ch3_ch5',
                    'ZH_hinv_ch3_ch6',
                    'ZH_hinv_ch3_ch7',
                    'ZH_hinv_ch3_ch8',
                    'ZH_hinv_ch3_ch9',
                    'ggH_hinv_ch1',
                    'ggH_hinv_ch2',
                    'ggH_hinv_ch3',
                    'ggH_hinv_ch4',
                    'ggH_hinv_ch5',
                    'ggH_hinv_ch6',
                    'qqH_hinv_vbf_dielec',
                    'qqH_hinv_vbf_dimuon',
                    'qqH_hinv_vbf_signal',
                    'qqH_hinv_vbf_singleel',
                    'qqH_hinv_vbf_singlemu']),
    'hmm': set([   'hmm_13TeV_cat0',
                   'hmm_13TeV_cat1',
                   'hmm_13TeV_cat10',
                   'hmm_13TeV_cat11',
                   'hmm_13TeV_cat12',
                   'hmm_13TeV_cat13',
                   'hmm_13TeV_cat14',
                   'hmm_13TeV_cat2',
                   'hmm_13TeV_cat3',
                   'hmm_13TeV_cat4',
                   'hmm_13TeV_cat5',
                   'hmm_13TeV_cat6',
                   'hmm_13TeV_cat7',
                   'hmm_13TeV_cat8',
                   'hmm_13TeV_cat9']),
    'htt': set([   'htt_em_1_13TeV',
                   'htt_em_2_13TeV',
                   'htt_em_3_13TeV',
                   'htt_et_10_13TeV',
                   'htt_et_11_13TeV',
                   'htt_et_13_13TeV',
                   'htt_et_14_13TeV',
                   'htt_et_1_13TeV',
                   'htt_et_2_13TeV',
                   'htt_et_3_13TeV',
                   'htt_mt_10_13TeV',
                   'htt_mt_11_13TeV',
                   'htt_mt_13_13TeV',
                   'htt_mt_14_13TeV',
                   'htt_mt_1_13TeV',
                   'htt_mt_2_13TeV',
                   'htt_mt_3_13TeV',
                   'htt_tt_10_13TeV',
                   'htt_tt_11_13TeV',
                   'htt_tt_12_13TeV',
                   'htt_tt_1_13TeV',
                   'htt_tt_2_13TeV',
                   'htt_tt_3_13TeV',
                   'htt_ttbar_1_13TeV']),
    'hww': set([   'ggHtag_of0j_em_mp_0j_pt2ge20',
                   'ggHtag_of0j_em_mp_0j_pt2lt20',
                   'ggHtag_of0j_em_pm_0j_pt2ge20',
                   'ggHtag_of0j_em_pm_0j_pt2lt20',
                   'ggHtag_of0j_me_mp_0j_pt2ge20',
                   'ggHtag_of0j_me_mp_0j_pt2lt20',
                   'ggHtag_of0j_me_pm_0j_pt2ge20',
                   'ggHtag_of0j_me_pm_0j_pt2lt20',
                   'ggHtag_of0j_of0j_DYtt',
                   'ggHtag_of0j_of0j_Top',
                   'ggHtag_of1j_em_mp_1j_pt2ge20',
                   'ggHtag_of1j_em_mp_1j_pt2lt20',
                   'ggHtag_of1j_em_pm_1j_pt2ge20',
                   'ggHtag_of1j_em_pm_1j_pt2lt20',
                   'ggHtag_of1j_me_mp_1j_pt2ge20',
                   'ggHtag_of1j_me_mp_1j_pt2lt20',
                   'ggHtag_of1j_me_pm_1j_pt2ge20',
                   'ggHtag_of1j_me_pm_1j_pt2lt20',
                   'ggHtag_of1j_of1j_DYtt',
                   'ggHtag_of1j_of1j_Top',
                   'ggHtag_of2j_of2j_DYtt',
                   'ggHtag_of2j_of2j_Top',
                   'ggHtag_of2j_of_2j',
                   'ggHtag_sf0j_sf_0j_ee_Top',
                   'ggHtag_sf0j_sf_0j_ee_WW',
                   'ggHtag_sf0j_sf_0j_ee_pt2ge20',
                   'ggHtag_sf0j_sf_0j_ee_pt2lt20',
                   'ggHtag_sf0j_sf_0j_mm_Top',
                   'ggHtag_sf0j_sf_0j_mm_WW',
                   'ggHtag_sf0j_sf_0j_mm_pt2ge20',
                   'ggHtag_sf0j_sf_0j_mm_pt2lt20',
                   'ggHtag_sf1j_sf_1j_Top',
                   'ggHtag_sf1j_sf_1j_ee',
                   'ggHtag_sf1j_sf_1j_ee_WW',
                   'ggHtag_sf1j_sf_1j_mm',
                   'ggHtag_sf1j_sf_1j_mm_WW',
                   'vbftag_of2j_vbf_2j_DYtt',
                   'vbftag_of2j_vbf_2j_Top',
                   'vbftag_of2j_vbf_2j_highmjj',
                   'vbftag_of2j_vbf_2j_lowmjj',
                   'vhtag_of2j_vh2j_DYtt',
                   'vhtag_of2j_vh2j_Top',
                   'vhtag_of2j_vh_2j',
                   'wh3ltag_wh3l_13TeV_ossf',
                   'wh3ltag_wh3l_sssf',
                   'wh3ltag_wh3l_wz_13TeV',
                   'wh3ltag_wh3l_zg_13TeV',
                   'zh4ltag_zh4l_XDF_13TeV',
                   'zh4ltag_zh4l_XSF_13TeV',
                   'zh4ltag_zh4l_ZZ_13TeV']),
    'hzz4l': set([   'cat_hzz_13TeV_2e2mu_Untagged',
                     'cat_hzz_13TeV_2e2mu_VBF1JetTagged',
                     'cat_hzz_13TeV_2e2mu_VBF2JetTagged',
                     'cat_hzz_13TeV_2e2mu_VHHadrTagged',
                     'cat_hzz_13TeV_2e2mu_VHLeptTagged',
                     'cat_hzz_13TeV_2e2mu_VHMETtagged',
                     'cat_hzz_13TeV_2e2mu_ttHTagged',
                     'cat_hzz_13TeV_4e_UnTagged',
                     'cat_hzz_13TeV_4e_VBF1JetTagged',
                     'cat_hzz_13TeV_4e_VBF2JetTagged',
                     'cat_hzz_13TeV_4e_VHHadrTagged',
                     'cat_hzz_13TeV_4e_VHLeptTagged',
                     'cat_hzz_13TeV_4e_VHMETTagged',
                     'cat_hzz_13TeV_4e_ttHTagged',
                     'cat_hzz_13TeV_4mu_UnTagged',
                     'cat_hzz_13TeV_4mu_VBF1JetTagged',
                     'cat_hzz_13TeV_4mu_VBF2JetTagged',
                     'cat_hzz_13TeV_4mu_VHHadrTagged',
                     'cat_hzz_13TeV_4mu_VHLeptTagged',
                     'cat_hzz_13TeV_4mu_VHMETTagged',
                     'cat_hzz_13TeV_4mu_ttHTagged']),
    'tth_hbb_hadronic': set([   'tth_hbb_fh_j7_t3__mem_FH_4w2h1t',
                                'tth_hbb_fh_j7_t4__mem_FH_3w2h2t',
                                'tth_hbb_fh_j8_t3__mem_FH_4w2h1t',
                                'tth_hbb_fh_j8_t4__mem_FH_3w2h2t',
                                'tth_hbb_fh_j9_t3__mem_FH_4w2h1t',
                                'tth_hbb_fh_j9_t4__mem_FH_4w2h2t']),
    'tth_hbb_leptonic': set([   'ttH_hbb_13TeV_dl_ge4j3t_both',
                                'ttH_hbb_13TeV_dl_ge4jge4t_high',
                                'ttH_hbb_13TeV_dl_ge4jge4t_low',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
                                'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
                                'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b']),
    'tth_htt': set([   'ttH_1l_2tau',
                       'ttH_2lss_1tau_MEM_missing',
                       'ttH_2lss_1tau_MEM_nomiss',
                       'ttH_3l_1tau']),
    'tth_multilepton': set([   'ttH_2lss_ee_neg',
                               'ttH_2lss_ee_pos',
                               'ttH_2lss_em_bl_neg',
                               'ttH_2lss_em_bl_pos',
                               'ttH_2lss_em_bt_neg',
                               'ttH_2lss_em_bt_pos',
                               'ttH_2lss_mm_bl_neg',
                               'ttH_2lss_mm_bl_pos',
                               'ttH_2lss_mm_bt_neg',
                               'ttH_2lss_mm_bt_pos',
                               'ttH_3l_bl_neg',
                               'ttH_3l_bl_pos',
                               'ttH_3l_bt_neg',
                               'ttH_3l_bt_pos',
                               'ttH_4l']),
    'vhbb': set([   'WlnHbb_Wen_SR',
                    'WlnHbb_Wen_TTCR',
                    'WlnHbb_Wen_WHFCRhigh',
                    'WlnHbb_Wen_WHFCRlow',
                    'WlnHbb_Wen_WLFCR',
                    'WlnHbb_Wmn_SR',
                    'WlnHbb_Wmn_TTCR',
                    'WlnHbb_Wmn_WHFCRhigh',
                    'WlnHbb_Wmn_WHFCRlow',
                    'WlnHbb_Wmn_WLFCR',
                    'ZllHbb_ch1_Zmm_SIG_low',
                    'ZllHbb_ch1_Zmm_TT_low',
                    'ZllHbb_ch1_Zmm_Zhf_low',
                    'ZllHbb_ch1_Zmm_Zlf_low',
                    'ZllHbb_ch2_Zee_SIG_low',
                    'ZllHbb_ch2_Zee_TT_low',
                    'ZllHbb_ch2_Zee_Zhf_low',
                    'ZllHbb_ch2_Zee_Zlf_low',
                    'ZllHbb_ch3_Zmm_SIG_high',
                    'ZllHbb_ch3_Zmm_TT_high',
                    'ZllHbb_ch3_Zmm_Zhf_high',
                    'ZllHbb_ch3_Zmm_Zlf_high',
                    'ZllHbb_ch4_Zee_SIG_high',
                    'ZllHbb_ch4_Zee_TT_high',
                    'ZllHbb_ch4_Zee_Zhf_high',
                    'ZllHbb_ch4_Zee_Zlf_high',
                    'ZnnHbb_ZnnHbb_Signal',
                    'ZnnHbb_ZnnHbb_TT',
                    'ZnnHbb_ZnnHbb_Zbb',
                    'ZnnHbb_ZnnHbb_Zlight']),
    
    
    'tth_run1': set([   'hgg_card_7TeV_tth',
      'hgg_card_8TeV_tth_ch1_cat11_8TeV',
      'hgg_card_8TeV_tth_ch1_cat12_8TeV',
      'ttH_2lss_eeBCat_MVA_neg_8TeV',
      'ttH_2lss_eeBCat_MVA_pos_8TeV',
      'ttH_2lss_emBCat_MVA_neg_8TeV',
      'ttH_2lss_emBCat_MVA_pos_8TeV',
      'ttH_2lss_mumuBCat_MVA_neg_8TeV',
      'ttH_2lss_mumuBCat_MVA_pos_8TeV',
      'ttH_3lBCat_MVA_neg_8TeV',
      'ttH_3lBCat_MVA_pos_8TeV',
      'ttH_4l_nJet_8TeV',
      'ttH_7TeV_e2je2t',
      'ttH_7TeV_ge3t',
      'ttH_7TeV_ljets_j4_t3',
      'ttH_7TeV_ljets_j4_t4',
      'ttH_7TeV_ljets_j5_t3',
      'ttH_7TeV_ljets_j5_tge4',
      'ttH_7TeV_ljets_jge6_t2',
      'ttH_7TeV_ljets_jge6_t3',
      'ttH_7TeV_ljets_jge6_tge4',
      'ttH_hbb_8TeV_e3je2t',
      'ttH_hbb_8TeV_ge3t',
      'ttH_hbb_8TeV_ge4je2t',
      'ttH_hbb_8TeV_ljets_j4_t3',
      'ttH_hbb_8TeV_ljets_j4_t4',
      'ttH_hbb_8TeV_ljets_j5_t3',
      'ttH_hbb_8TeV_ljets_j5_tge4',
      'ttH_hbb_8TeV_ljets_jge6_t2',
      'ttH_hbb_8TeV_ljets_jge6_t3',
      'ttH_hbb_8TeV_ljets_jge6_tge4',
      'ttH_htt_8TeV_TTL_1b_1nb',
      'ttH_htt_8TeV_TTL_1b_2nb',
      'ttH_htt_8TeV_TTL_1b_3+nb',
      'ttH_htt_8TeV_TTL_2b_0nb',
      'ttH_htt_8TeV_TTL_2b_1nb',
      'ttH_htt_8TeV_TTL_2b_2+nb'])}


bin_channel_dict = {}

for key, val in channel_bin_dict.iteritems():
    for binname in val:
        bin_channel_dict[binname] = key


fin = ROOT.TFile(args.input)
w = fin.Get('w')
dat = w.data('data_obs')

mc = w.genobj("ModelConfig")


pdf = mc.GetPdf()
# pdf.Print()
cat = pdf.indexCat()
ncats = cat.numBins('')

names = []
for i in range(ncats):
    cat.setBin(i)
    names.append(cat.getLabel())


param_dict = {}

all_pars = set()

for name in names:
    cat_pdf = w.pdf(pdf.getPdf(name).GetName() + '_nuis')
    # cat_pdf.Print()
    pdfvars = cat_pdf.getParameters(dat)
    chn = bin_channel_dict[name]
    if chn not in param_dict:
        param_dict[chn] = set()
    it = pdfvars.createIterator()
    var = it.Next()
    print '>> Doing bin %s' % name
    while var:
        if (not var.isConstant()) and var.InheritsFrom("RooRealVar"):
            param_dict[chn].add(var.GetName())
            skip = False
            for pattern in reject_patterns:
                if re.match(pattern + '$', var.GetName()):
                    print '>> Skipping %s' % var.GetName()
                    skip = True
                    break
            if not skip:
                all_pars.add(var.GetName())
        var = it.Next()

# pprint.pprint(param_dict, indent=4)

param_dict_rev = defaultdict(list)
for chn, pars in param_dict.iteritems():
    for par in pars:
        param_dict_rev[par].append(chn)


# pprint.pprint(dict(param_dict_rev), indent=4)

dump_dict = {}
dump_dict_all = defaultdict(list)
for ana in channel_bin_dict:
    dump_dict[ana] = defaultdict(list)


for name in all_pars:
    print '>> Doing %s' % name
    nassigned = 0
    for att in att_labels:
        for pattern in attributes[att]:
            if re.match(pattern + '$', name):
                for ana in param_dict_rev[name]:
                    dump_dict[ana][att].append(name)
                dump_dict_all[att].append(name)
                nassigned += 1
                break
    for oth_group in ['sigTheory', 'bkgTheory', 'sigInc']:
        for pattern in attributes[oth_group]:
            if re.match(pattern + '$', name):
                for ana in param_dict_rev[name]:
                    dump_dict[ana][oth_group].append(name)
                dump_dict_all[oth_group].append(name)
                nassigned += 1
                break
    if nassigned == 0:
        pdf = w.pdf(name + '_Pdf')
        if pdf != None and pdf.IsA().InheritsFrom(ROOT.RooGaussian.Class()):
            for ana in param_dict_rev[name]:
                dump_dict[ana]['unassigned'].append(name)
                dump_dict_all['pOther'].append(name)

if args.dump:
    for ana in dump_dict:
        for key in dump_dict[ana]:
            dump_dict[ana][key].sort()
        jsondata = json.dumps(
            dump_dict[ana], sort_keys=True, indent=2, separators=(',', ': '))
        with open('%sproj_np_groups_%s.json' % (args.prefix, ana), 'w') as out_file:
            out_file.write(jsondata)
        with open('%sproj_np_groups.txt' % args.prefix, 'w') as out_file:
            for grp in dump_dict_all:
                out_file.write('%s group = %s\n' % (grp, ' '.join(dump_dict_all[grp])))

