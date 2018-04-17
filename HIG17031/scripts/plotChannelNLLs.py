import ROOT
# import json
# import argparse
# import pprint
import os
from collections import defaultdict
import CombineHarvester.CombineTools.plotting as plot



ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# parser = argparse.ArgumentParser()
# parser.add_argument( '-i', '--input', help='Input workspace')
# parser.add_argument( '--json', help='json file containing the impacts')
# parser.add_argument( '-o', '--output', help='output json file')

# args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

# impacts = {}
# with open(args.json) as jsonfile:
#     impacts = json.load(jsonfile)

# # print impacts


channel_bin_dict_all = {   'ggHbb': set([   'cat1_fail_cat1',
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
    'constraintPdf': set([   'constraintPdf'])
    }



channel_bin_dict_hgg = {
    'hgg_untagged': set([
                   'UntaggedTag_0_13TeV',
                   'UntaggedTag_1_13TeV',
                   'UntaggedTag_2_13TeV',
                   'UntaggedTag_3_13TeV']),
     'hgg_tth_had': set([
                   'TTHHadronicTag_13TeV']),
     'hgg_tth_lep': set([
                   'TTHLeptonicTag_13TeV']),
     'hgg_vbf': set([
                   'VBFTag_0_13TeV',
                   'VBFTag_1_13TeV',
                   'VBFTag_2_13TeV']),
     'hgg_vh': set([
                   'VHHadronicTag_13TeV',
                   'VHLeptonicLooseTag_13TeV',
                   'VHMetTag_13TeV',
                   'WHLeptonicTag_13TeV',
                   'ZHLeptonicTag_13TeV']),
    }


channel_bin_dict_tth_hbb_leptonic = {
    'dl_ge4j3t_both': set(['ttH_hbb_13TeV_dl_ge4j3t_both']),
    'dl_ge4jge4t_high': set([
        'ttH_hbb_13TeV_dl_ge4jge4t_high'
        ]),
    'dl_ge4jge4t_low': set([
        'ttH_hbb_13TeV_dl_ge4jge4t_low'
        ]),
    'sl_eq4j_ge3b': set([
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
        'ttH_hbb_13TeV_sl_eq4j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b'
        ]),
    'sl_eq5j_ge3b': set([
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
        'ttH_hbb_13TeV_sl_eq5j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b'
        ]),
    'sl_ge6j_ge3b': set([
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttH125_bb__MVA_cc_dnn_ttH_SL_v6b',
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_2b__MVA_cc_dnn_tt2b_SL_v6b',
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_b__MVA_cc_dnn_ttb_SL_v6b',
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_bb__MVA_cc_dnn_ttbb_SL_v6b',
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_cc__MVA_cc_dnn_ttcc_SL_v6b',
        'ttH_hbb_13TeV_sl_ge6j_ge3b_cc_v6b_ttJets_lf__MVA_cc_dnn_ttlf_SL_v6b'
        ])
    }



channel_bin_dict = channel_bin_dict_tth_hbb_leptonic

def runCmd(cmd):
    print cmd
    os.system(cmd)


for channel in channel_bin_dict:
    nll_str = '+'.join(['deltaNLL_' + x for x in channel_bin_dict[channel]])
    runCmd("""python scripts/plot1DScan.py -o scan_channelnll_%s --POI kappa_W \
                 -m Comb_Mar26/scan.K2.observed.nominal.kappa_W.channelnll.root \
                 --translate pois.json --remove-near-min 0.8 --chop 2 --y-max 4 \
                 --no-input-label --pub --nll-branch "(%s)"\
                 """ % (channel, nll_str))

plot.ModTDRStyle(width=700, l=0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)


canv = ROOT.TCanvas('channelnll_comp', 'channelnll_comp')
pads = plot.OnePad()

f = ROOT.TFile('scan_channelnll.root')
g = f.Get('main').Clone()
g.SetLineWidth(3)
f.Close()

g.Draw('APC')
deltamin = g.Eval(-1.132) - g.Eval(+1.120)


axishist = plot.GetAxisHist(pads[0])
axishist.GetXaxis().SetTitle('#kappa_{W}')
y_max = axishist.GetMaximum()


vline = ROOT.TLine()
plot.Set(vline, LineColor=16, LineWidth=1, LineStyle=7)
for linex in [-1.132, +1.120]:
    plot.DrawVerticalLine(pads[0], vline, linex)



legend = ROOT.TLegend(0.15, 0.75, 0.9, 0.94, '', 'NBNDC')
legend.SetNColumns(3)
legend.AddEntry(g, 'full scan (%+.2f)' % deltamin, 'L')
# legend.SetNColumns(1)

graphs = []
cols = [2, 3, 4, 5, 6, 7, 8, 9, 13, 17, 28, 32, 38, 40, 46, 49]

for i, draw in enumerate(channel_bin_dict.keys()):
    f = ROOT.TFile('scan_channelnll_%s.root' % draw)
    graphs.append(f.Get('main').Clone())
    graphs[-1].SetLineWidth(2)
    graphs[-1].SetLineColor(cols[i])
    graphs[-1].SetMarkerColor(cols[i])
    graphs[-1].SetMarkerSize(0.5)
    graphs[-1].Draw('PLSAME')
    deltamin = graphs[-1].Eval(-1.132) - graphs[-1].Eval(+1.120)
    legend.AddEntry(graphs[-1], '%s (%+.2f)' % (draw, deltamin), 'L')



box = ROOT.TBox(axishist.GetXaxis().GetXmin(), 0.7, axishist.GetXaxis().GetXmax(), y_max)
box2 = ROOT.TBox(-0.5, axishist.GetMinimum(), 0.5, y_max)
box.Draw()
box2.SetFillColor(19)
box2.Draw()

legend.Draw()

pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

canv.Print('.pdf')
canv.Print('.png')


