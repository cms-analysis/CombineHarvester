from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch

def AddSystematics_hhh_et_mt(cb):
    src = cb.cp()
    src.channel(['et', 'mt'])

    # This regular expression will match any Higgs signal process.
    # It's useful for catching all these processes when we don't know
    # which of them will be signal or background
    higgs_rgx = '^(qq|gg|[WZV])H.*$'

    signal = src.cp().signals().process_set()

    src.cp().signals().AddSyst(
        cb, "lumi_8TeV", "lnN", ch.SystMap()(1.026))

    src.cp().process(signal + ['ZTT','ZJ','ZL','TT','VV']).channel(['et']).AddSyst(
        cb, "CMS_eff_e", "lnN", ch.SystMap()(1.02))

    src.cp().process(signal + ['ZTT','ZJ','ZL','TT','VV']).channel(['mt']).AddSyst(
        cb, "CMS_eff_m", "lnN", ch.SystMap()(1.01))

    src.cp().process(signal + ['ZTT','TT','VV']).channel(['et']).AddSyst(
        cb, "CMS_eff_t_etau_8TeV", "lnN", ch.SystMap('bin_id', 'process')
            ([0,1,2], signal+['ZTT','TT','VV'], 1.08))

    src.cp().process(signal+['ZTT','TT','VV']).channel(['mt']).AddSyst(
        cb, "CMS_eff_t_mutau_8TeV", "lnN", ch.SystMap('bin_id','process')
            ([0,1,2],signal+['ZTT','TT','VV'],1.08))

    src.cp().process(signal+['TT','ZL','ZJ','VV']).AddSyst(
        cb, "CMS_htt_scale_met_8TeV", "lnN", ch.SystMap('channel','bin_id','process')
            (['et'],[0],signal+['VV'],1.01)
            (['et'],[0],['TT'],0.97)
            (['et'],[0],['ZL'],0.98)
            (['et'],[1],signal,0.99)
            (['et'],[1],['TT'],0.98)
            (['et'],[1],['ZL','ZJ'],0.96)
            (['et'],[1],['VV'],0.97)
            (['et'],[2],signal,1.01)
            (['et'],[2],['TT'],0.96)
            (['mt'],[0],signal,1.01)
            (['mt'],[0],['TT'],0.97)
            (['mt'],[0],['ZL'],0.93)
            (['mt'],[0],['ZJ'],0.99)
            (['mt'],[0],['VV'],1.04)
            (['mt'],[1],signal,0.99)
            (['mt'],[1],['TT'],0.98)
            (['mt'],[1],['ZJ'],0.95)
            (['mt'],[1],['VV'],0.96)
            (['mt'],[2],signal,0.99)
            (['mt'],[2],['TT'],0.97)
            (['mt'],[2],['VV'],1.01))

    src.cp().process(signal+['ZTT']).channel(['et']).AddSyst(
        cb, "CMS_scale_t_etau_8TeV", "shape", ch.SystMap()(1.00))

    src.cp().process(signal+['ZTT']).channel(["mt"]).AddSyst(
        cb, "CMS_scale_t_mutau_8TeV", "shape", ch.SystMap()(1.00))

    src.cp().process(signal + ["ZTT","ZJ","ZL","TT","VV"]).AddSyst(
        cb, "CMS_scale_j_8TeV","shape", ch.SystMap()(1.00))

    src.cp().process(signal+['TT','W','VV','QCD','ZL','ZJ']).AddSyst(
        cb,"CMS_eff_b_8TeV","lnN",ch.SystMap('channel','bin_id','process')
            (['et','mt'],[0],['TT'], 0.95)
            (['et','mt'],[0],['W'], 1.01)
            (['et'],[0],signal,0.93)
            (['mt'],[0],signal,0.92)
            (['mt'],[0],['VV'],0.99)
            (['et'],[1],{"VV","QCD"},0.97)
            (['et'],[1],['W'],0.99)
            (['mt'],[1],signal+['ZJ'],0.99)
            (['mt'],[1],['VV'],1.02)
            (['mt'],[1],['W'],1.01)
            (['mt'],[1],['QCD'],0.98)
            (['mt'],[1],['ZL'],1.05)
            (['et'],[2],signal+['TT'],1.04)
            (['et'],[2],['VV'],1.13)
            (['et'],[2],['W'],0.68)
            (['et'],[2],['ZL'],1.07)
            (['mt'],[2],signal+['TT'],1.05)
            (['mt'],[2],['VV'],1.01)
            (['mt'],[2],['W'],0.28)
            (['mt'],[2],['ZJ'],1.41))

    src.cp().process(['ZTT','ZL','ZJ']).AddSyst(
        cb,"CMS_htt_zttNorm_8TeV","lnN",ch.SystMap()(1.03))

    src.cp().process(['TT','W']).AddSyst(
        cb,"CMS_htt_ttbarNorm_8TeV","lnN",ch.SystMap('bin_id','process')
            ([0,1,2],['TT'],1.10)
            ([1],['W'],0.75))

    src.cp().process(['VV']).AddSyst(
        cb,"CMS_htt_DiBosonNorm_8TeV","lnN",ch.SystMap()(1.15))

    src.cp().process(['ZL']).channel(['et']).AddSyst(
        cb,"CMS_htt_ZLeptonFakeTau_etau_8TeV","lnN",ch.SystMap('bin_id')
            ([0,1],1.20)
            ([2],1.40))

    src.cp().process(['ZL']).channel(['mt']).AddSyst(
        cb,"CMS_htt_ZLeptonFakeTau_mutau_8TeV","lnN",ch.SystMap('bin_id')
            ([0],1.30)
            ([1],1.60)
            ([2],1.40))

    src.cp().process(['ZL','ZJ','W','VV']).AddSyst(
        cb,"CMS_fake_b_8TeV","lnN",ch.SystMap('channel','bin_id','process')
            (['mt'],[0],['VV'],0.99)
            (['et'],[1],['ZL'],1.01)
            (['et'],[1],['ZJ'],1.04)
            (['mt'],[1],['VV'],1.03)
            (['mt'],[1],['ZL'],1.04)
            (['mt'],[1],['ZJ'],1.02)
            (['et'],[2],['W'],0.95)
            (['mt'],[2],['VV'],1.01)
            (['mt'],[2],['W'],0.96))

    src.cp().process(['W']).bin_id([0]).channel(['et']).AddSyst(
        cb,"CMS_htt_WNorm_etau_2jet0tag_8TeV","lnN",ch.SystMap()(1.10))

    src.cp().process(['ZTT']).bin_id([0]).channel(['et']).AddSyst(
        cb,"CMS_htt_extrap_ztt_etau_2jet0tag_8TeV","lnN",ch.SystMap()(1.05))

    src.cp().process(['QCD']).bin_id([0]).channel(['et']).AddSyst(
        cb,"CMS_htt_QCDSyst_etau_2jet0tag_8TeV","lnN", ch.SystMap()(1.20))

    src.cp().process(['ZJ']).bin_id([0]).channel(['et']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_etau_2jet0tag_8TeV","lnN",ch.SystMap()(1.20))

    src.cp().process(['W']).bin_id([0]).channel(['mt']).AddSyst(
        cb,"CMS_htt_WNorm_mutau_2jet0tag_8TeV","lnN",ch.SystMap()(1.10))

    src.cp().process(['ZTT']).bin_id([0]).channel(['mt']).AddSyst(
        cb,"CMS_htt_extrap_ztt_mutau_2jet0tag_8TeV","lnN",ch.SystMap()(1.05))

    src.cp().process(['QCD']).bin_id([0]).channel(['mt']).AddSyst(
        cb,"CMS_htt_QCDSyst_mutau_2jet0tag_8TeV","lnN", ch.SystMap()(1.20))

    src.cp().process(['ZJ']).bin_id([0]).channel(['mt']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_mutau_2jet0tag_8TeV","lnN",ch.SystMap()(1.20))


    src.cp().process(['W']).bin_id([1]).channel(['et']).AddSyst(
        cb,"CMS_htt_WNorm_etau_2jet1tag_8TeV","lnN",ch.SystMap()(1.30))

    src.cp().process(['ZTT']).bin_id([1]).channel(['et']).AddSyst(
        cb,"CMS_htt_extrap_ztt_etau_2jet1tag_8TeV","lnN",ch.SystMap()(1.05))

    src.cp().process(['ZTT']).channel(['mt']).AddSyst(
        cb,"CMS_htt_ttbar_emb_mutau_8TeV","lnN",ch.SystMap('bin_id')
            ([1],1.08)
            ([2],1.27))

    src.cp().process(['ZTT']).channel(['et']).AddSyst(
        cb,"CMS_htt_ttbar_emb_etau_8TeV","lnN",ch.SystMap('bin_id')
            ([1],1.08)
            ([2],1.32))

    src.cp().process(['QCD']).bin_id([1]).channel(['et']).AddSyst(
        cb,"CMS_htt_QCDSyst_etau_2jet1tag_8TeV","lnN",ch.SystMap()(1.40))

    src.cp().process(['ZJ']).bin_id([1]).channel(['et']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_etau_2jet1tag_8TeV","lnN",ch.SystMap()(1.25))

    src.cp().process(['W']).bin_id([1]).channel(['mt']).AddSyst(
        cb,"CMS_htt_WNorm_mutau_2jet1tag_8TeV","lnN",ch.SystMap()(1.30))

    src.cp().process(['ZTT']).bin_id([1]).channel(['mt']).AddSyst(
        cb,"CMS_htt_extrap_ztt_mutau_2jet1tag_8TeV","lnN",ch.SystMap()(1.05))

    src.cp().process(['QCD']).bin_id([1]).channel(['mt']).AddSyst(
        cb,"CMS_htt_QCDSyst_mutau_2jet1tag_8TeV","lnN",ch.SystMap()(1.40))

    src.cp().process(['ZJ']).bin_id([1]).channel(['mt']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_mutau_2jet1tag_8TeV","lnN",ch.SystMap()(1.20))

    src.cp().process(['W']).bin_id([2]).channel(['et']).AddSyst(
        cb,"CMS_htt_WNorm_etau_2jet2tag_8TeV","lnN",ch.SystMap()(2.00))

    src.cp().process(['ZTT']).bin_id([2]).channel(['et']).AddSyst(
        cb,"CMS_htt_extrap_ztt_etau_2jet2tag_8TeV","lnN",ch.SystMap()(1.06))

    src.cp().process(['QCD']).bin_id([2]).channel(['et']).AddSyst(
        cb,"CMS_htt_QCDSyst_etau_2jet2tag_8TeV","lnN",ch.SystMap()(2.00))

    src.cp().process(['ZJ']).bin_id([2]).channel(['et']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_etau_2jet2tag_8TeV","lnN",ch.SystMap()(1.70))

    src.cp().process(['W']).bin_id([2]).channel(['mt']).AddSyst(
        cb,"CMS_htt_WNorm_mutau_2jet2tag_8TeV","lnN",ch.SystMap()(2.00))

    src.cp().process(['ZTT']).bin_id([2]).channel(['mt']).AddSyst(
        cb,"CMS_htt_extrap_ztt_mutau_2jet2tag_8TeV","lnN",ch.SystMap()(1.06))

    src.cp().process(['QCD']).bin_id([2]).channel(['mt']).AddSyst(
        cb,"CMS_htt_QCDSyst_mutau_2jet2tag_8TeV","lnN",ch.SystMap()(1.60))

    src.cp().process(['ZJ']).bin_id([2]).channel(['mt']).AddSyst(
        cb,"CMS_htt_ZJetFakeTau_mutau_2jet2tag_8TeV","lnN",ch.SystMap()(1.90))

def AddSystematics_hhh_tt(cb):
    src = cb.cp()
    src.channel(['tt'])

    signal = cb.cp().signals().process_set()

    src.cp().signals().AddSyst(
        cb, "lumi_8TeV", "lnN", ch.SystMap()(1.026))

    src.cp().process(signal+['TT','VV','ZTT','W']).AddSyst(
        cb, "CMS_eff_t_tautau_8TeV", "lnN", ch.SystMap('process')
            (signal+['TT','VV','ZTT'],1.190)
            (['W'], 1.095))

    src.cp().process(signal+['ZTT','W']).AddSyst(
        cb, "CMS_scale_t_tautau_8TeV", "shape", ch.SystMap()(1.00))

    src.cp().process(signal+['TT','VV','W','ZLL','ZTT']).AddSyst(
        cb, "CMS_scale_j_8TeV", "shape", ch.SystMap()(1.00))

    src.cp().process(signal+['TT']).AddSyst(
        cb, "CMS_eff_b_8TeV", "lnN", ch.SystMap('bin_id','process')
            ([0], signal, 0.944)
            ([0], ['TT'], 0.949)
            ([1], signal, 0.980)
            ([2], ['TT'], 1.042)
            ([2], signal, 1.049))

    src.cp().process(['TT','ZTT']).AddSyst(
        cb, "CMS_htt_ttbarNorm_8TeV", "lnN", ch.SystMap('bin_id', 'process')
            ([0,1,2], ['TT'], 1.100)
            ([1], ['ZTT'], 0.949)
            ([2], ['ZTT'], 0.494))

    src.cp().process(['VV']).AddSyst(
        cb, "CMS_htt_DiBosonNorm_8TeV", "lnN", ch.SystMap()(1.150))

    src.cp().process(['W']).bin_id([0]).AddSyst(
        cb, "CMS_WNorm_tautau_8TeV", "lnN", ch.SystMap()(1.200))

    src.cp().process(['QCD']).bin_id([0]).AddSyst(
        cb, "CMS_htt_QCDSyst_tautau_2jet0tag_8TeV", "lnN", ch.SystMap()(1.100))

    src.cp().process(['QCD']).bin_id([1]).AddSyst(
        cb, "CMS_htt_QCDSyst_tautau_2jet1tag_8TeV", "lnN", ch.SystMap()(1.200))

    src.cp().process(['QCD']).bin_id([2]).AddSyst(
        cb, "CMS_htt_QCDSyst_tautau_2jet2tag_8TeV", "lnN", ch.SystMap()(1.400))

    src.cp().process(['ZTT','ZLL']).AddSyst(
        cb, "CMS_htt_zttNorm_8TeV", "lnN", ch.SystMap()(1.033))

    src.cp().process(['ZTT']).bin_id([0]).AddSyst(
        cb, "CMS_htt_extrap_ztt_tautau_2jet0tag_8TeV", "lnN", ch.SystMap()(1.057))

    src.cp().process(['ZTT']).bin_id([1]).AddSyst(
        cb, "CMS_htt_extrap_ztt_tautau_2jet1tag_8TeV", "lnN", ch.SystMap()(1.252))

    src.cp().process(['ZTT']).bin_id([2]).AddSyst(
        cb, "CMS_htt_extrap_ztt_tautau_2jet2tag_8TeV", "lnN", ch.SystMap()(2.749))

    src.cp().process(['ZLL']).bin_id([0]).AddSyst(
        cb, "CMS_htt_ZLL_FakeTau_tautau_2jet0tag_8TeV", "lnN", ch.SystMap()(1.301))

    src.cp().process(['ZLL']).bin_id([1]).AddSyst(
        cb, "CMS_htt_ZLL_FakeTau_tautau_2jet1tag_8TeV", "lnN", ch.SystMap()(1.515))

    src.cp().process(['ZLL']).bin_id([2]).AddSyst(
        cb, "CMS_htt_ZLL_FakeTau_tautau_2jet2tag_8TeV", "lnN", ch.SystMap()(1.671))


