from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch

def AddSystematics_ee_mm(cb):
    src = cb.cp()
    src.channel(['ee', 'mm'])

    # This regular expression will match any Higgs signal process.
    # It's useful for catching all these processes when we don't know
    # which of them will be signal or background
    higgs_rgx = '^(qq|gg|[WZV])H.*$'

    signal = src.cp().signals().process_set()

    # Lumi not added for ggH_hww125 type processes
    src.cp().process(['qqH', 'ggH', 'WH', 'ZH', 'Dibosons', 'WJets']).AddSyst(
        cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.022)
          (['8TeV'], 1.026))

    src.cp().channel(['ee']).process_rgx([higgs_rgx, 'ZTT', 'TTJ', 'WJets', 'Dibosons']).AddSyst(
        cb, 'CMS_eff_e', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.04)
          (['8TeV'], 1.06))

    src.cp().channel(['mm']).process_rgx([higgs_rgx, 'ZTT', 'TTJ', 'WJets', 'Dibosons']).AddSyst(
        cb, 'CMS_eff_m', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.04)
          (['8TeV'], 1.04))

    src.cp().channel(['ee']).process_rgx([higgs_rgx, 'ZTT', 'TTJ', 'Dibosons']).AddSyst(
        cb, 'CMS_scale_e_$ERA', 'shape', ch.SystMap()(0.50))

    src.cp().process_rgx([higgs_rgx, 'TTJ', 'Dibosons']).AddSyst(
        cb, 'CMS_scale_j_$ERA', 'shape', ch.SystMap()(0.50))

    src.cp().channel(['ee']).process_rgx([higgs_rgx, 'TTJ', 'Dibosons']).bin_id([4]).AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'shape', ch.SystMap()(0.50))

    src.cp().channel(['mm']).process_rgx([higgs_rgx, 'Dibosons']).bin_id([4]).AddSyst(
        cb, 'CMS_htt_scale_met_SignalDibosonWjets_$ERA', 'shape', ch.SystMap()(0.50))

    src.cp().channel(['mm']).process(['TTJ']).bin_id([4]).AddSyst(
        cb, 'CMS_htt_scale_met_TTJ_$ERA', 'shape', ch.SystMap()(0.50))

    src.cp().process(['TTJ']).AddSyst(
        cb, 'CMS_eff_b_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'],  [0, 1],     0.96)
          (['7TeV'],  [2, 3, 4],  0.95)
          (['8TeV'],  [2, 3],     0.97)
          (['8TeV'],  [4],        0.99))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'pdf_gg', 'lnN', ch.SystMap()(1.097))

    src.cp().process(['ggH']).bin_id([4]).AddSyst(
        cb, 'pdf_gg_Shape', 'shape', ch.SystMap()(1.0))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap()(1.036))
    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap('channel', 'bin_id')
          (['ee', 'mm'],  [0, 1, 2, 3],   1.01)
          (['ee'],        [4],            1.01)
          (['mm'],        [4],            1.04))

    src.cp().process(['qqH']).bin_id([4]).AddSyst(
        cb, 'pdf_qqbar_Shape', 'shape', ch.SystMap()(1.0))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH', 'lnN', ch.SystMap('bin_id')
          ([0], 1.103)
          ([1], 1.100))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH1in', 'lnN', ch.SystMap('bin_id')
          ([2], 1.109)
          ([3], 1.107))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH2in', 'lnN', ch.SystMap('bin_id')
          ([4], 1.182))

    src.cp().process(['ggH']).bin_id([4]).AddSyst(
        cb, 'QCDscale_ggH2in_Shape', 'shape', ch.SystMap()(1.0))

    src.cp().process_rgx(['^qqH.*$']).AddSyst(
        cb, 'QCDscale_qqH', 'lnN', ch.SystMap('bin_id')
          ([0], 1.034)
          ([1], 1.028)
          ([2], 1.008)
          ([3], 1.013)
          ([4], 1.009))

    src.cp().process(['qqH']).bin_id([4]).AddSyst(
        cb, 'QCDscale_qqH_Shape', 'shape', ch.SystMap()(1.0))

    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'QCDscale_VH', 'lnN', ch.SystMap()(1.04))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 1.035)
          ([1], 1.042)
          ([2], 0.984)
          ([3], 0.978)
          ([4], 0.926))
    src.cp().process_rgx(['^qqH.*$', 'WH', 'ZH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 1.089)
          ([1], 1.063)
          ([2], 1.000)
          ([3], 1.004)
          ([4], 0.986))

    src.cp().process(['ZTT']).AddSyst(
        cb, 'CMS_htt_zttNorm_$ERA', 'lnN', ch.SystMap()(1.03))

    src.cp().channel(['ee']).process(['ZTT']).AddSyst(
        cb, 'CMS_htt_ee_ztt_extrap_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [1, 2],  1.07)
          (['7TeV'], [3],     1.06)
          (['7TeV'], [4],     1.09)
          (['8TeV'], [1],     1.09)
          (['8TeV'], [2, 3],  1.07)
          (['8TeV'], [4],     1.09))

    src.cp().channel(['mm']).process(['ZTT']).AddSyst(
        cb, 'CMS_htt_mm_zttLnN_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [1, 2],  1.07)
          (['7TeV'], [3],     1.06)
          (['7TeV'], [4],     1.08)
          (['8TeV'], [1],     1.09)
          (['8TeV'], [2, 3],  1.07)
          (['8TeV'], [4],     1.08))

    src.cp().process(['TTJ']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$ERA', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.08)
          (['8TeV'], 1.10))

    src.cp().process(['Dibosons']).AddSyst(
        cb,
        'CMS_htt_$CHANNEL_DiBosonNorm_$ERA', 'lnN', ch.SystMap()(1.30))

    src.cp().process(['ZEE', 'ZMM']).AddSyst(
        cb, 'CMS_htt_$CHANNEL_z$CHANNELNorm_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [0], 1.01)
          (['7TeV'], [1], 1.0045)
          (['7TeV'], [2], 1.01)
          (['7TeV'], [3], 1.007)
          (['7TeV'], [4], 1.02)
          (['8TeV'], [0], 1.01)
          (['8TeV'], [1], 1.001)
          (['8TeV'], [2], 1.01)
          (['8TeV'], [3], 1.007)
          (['8TeV'], [4], 1.015))

    src.cp().process(['QCD']).AddSyst(
        cb, 'CMS_htt_$CHANNEL_QCDNorm_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['ee'], ['7TeV'], [0], 1.19)
          (['ee'], ['7TeV'], [1], 1.50)
          (['ee'], ['7TeV'], [2], 1.35)
          (['ee'], ['7TeV'], [3], 1.34)
          (['ee'], ['7TeV'], [4], 1.70)
          (['ee'], ['8TeV'], [0], 1.11)
          (['ee'], ['8TeV'], [1], 1.09)
          (['ee'], ['8TeV'], [2], 1.16)
          (['ee'], ['8TeV'], [3], 1.14)
          (['ee'], ['8TeV'], [4], 1.55)
          (['mm'], ['7TeV'], [0], 1.11)
          (['mm'], ['7TeV'], [1], 1.11)
          (['mm'], ['7TeV'], [2], 1.25)
          (['mm'], ['7TeV'], [3], 1.09)
          (['mm'], ['7TeV'], [4], 2.00)
          (['mm'], ['8TeV'], [0], 1.10)
          (['mm'], ['8TeV'], [1], 1.08)
          (['mm'], ['8TeV'], [2], 1.12)
          (['mm'], ['8TeV'], [3], 1.09)
          (['mm'], ['8TeV'], [4], 1.70))

    for b in src.cp().channel(['ee']).bin_set():
        clip = b.replace('ee_', '')
        for i in ['0', '1', '2']:
            src.cp().process(['ZEE']).bin([b]).AddSyst(
                cb, 'CMS_htt_$CHANNEL_z$CHANNELShape_' + clip + '_mass' + i + '_$ERA', 'shape', ch.SystMap()(1.0))

    for b in src.cp().channel(['mm']).bin_set():
        clip = b.replace('mumu_', '')
        for i in ['0', '1', '2']:
            src.cp().process(['ZMM']).bin([b]).AddSyst(
                cb, 'CMS_htt_$CHANNEL_z$CHANNELShape_' + clip + '_mass' + i + '_$ERA', 'shape', ch.SystMap()(1.0))


def AddSystematics_em(cb):
    src = cb.cp()
    src.channel(['em'])

    # This regular expression will match any Higgs signal process.
    # It's useful for catching all these processes when we don't know
    # which of them will be signal or background
    higgs_rgx = '^(qq|gg|[WZV])H.*$'

    ggH = ['ggH', 'ggH_hww125']
    qqH = ['qqH', 'qqH_hww125']

    signal = src.cp().signals().process_set()

    src.cp().process_rgx([higgs_rgx, 'EWK']).AddSyst(
        cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.022)
          (['8TeV'], 1.026))

    src.cp().AddSyst(cb, 'CMS_eff_e', 'lnN', ch.SystMap()(1.02))
    src.cp().AddSyst(cb, 'CMS_eff_m', 'lnN', ch.SystMap()(1.02))

    src.cp().process_rgx([higgs_rgx, 'Ztt']).bin_id([0, 2, 4, 5]).AddSyst(
        cb, 'CMS_scale_e_$ERA', 'shape', ch.SystMap()(1.00))
    src.cp().process_rgx([higgs_rgx, 'Ztt']).bin_id([1, 3]).AddSyst(
        cb, 'CMS_scale_e_highpt_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().AddSyst(
        cb, 'CMS_scale_j_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['7TeV'], [0, 1],   ggH,                0.98)
          (['7TeV'], [0, 1],   qqH,                0.90)
          (['7TeV'], [0, 1],   ['WH', 'ZH'],       0.98)
          (['7TeV'], [0, 1],   ['EWK', 'ttbar'],   0.99)
          (['7TeV'], [2, 3],   ggH,                1.05)
          (['7TeV'], [2, 3],   ['EWK', 'ttbar'],   1.05)
          (['7TeV'], [4],      ggH,                1.15)
          (['7TeV'], [4],      qqH,                1.05)
          (['7TeV'], [4],      ['WH', 'ZH'],       1.15)
          (['7TeV'], [4],      ['EWK', 'ttbar'],   1.20)
          (['8TeV'], [0],      ggH,                0.98)
          (['8TeV'], [0],      qqH,                0.90)
          (['8TeV'], [0],      ['WH', 'ZH'],       0.95)
          (['8TeV'], [0],      ['ttbar'],          0.91)
          (['8TeV'], [0],      ['EWK'],            0.98)
          (['8TeV'], [1],      ggH,                0.98)
          (['8TeV'], [1],      qqH,                0.89)
          (['8TeV'], [1],      ['WH', 'ZH'],       0.95)
          (['8TeV'], [1],      ['ttbar'],          0.90)
          (['8TeV'], [1],      ['EWK'],            0.98)
          (['8TeV'], [2],      ggH,                1.03)
          (['8TeV'], [2],      qqH,                0.99)
          (['8TeV'], [2],      ['WH', 'ZH'],       1.02)
          (['8TeV'], [2],      ['ttbar'],          1.03)
          (['8TeV'], [2],      ['EWK'],            0.98)
          (['8TeV'], [3],      ggH,                1.02)
          (['8TeV'], [3],      qqH,                0.99)
          (['8TeV'], [3],      ['WH', 'ZH'],       1.01)
          (['8TeV'], [3],      ['ttbar'],          1.02)
          (['8TeV'], [3],      ['EWK'],            0.99)
          (['8TeV'], [4],      ggH,                1.10)
          (['8TeV'], [4],      qqH,                1.05)
          (['8TeV'], [4],      ['WH', 'ZH'],       1.05)
          (['8TeV'], [4],      ['ttbar'],          1.22)
          (['8TeV'], [4],      ['EWK'],            1.21)
          (['8TeV'], [5],      ggH,                1.14)
          (['8TeV'], [5],      qqH,                1.04)
          (['8TeV'], [5],      ['WH', 'ZH'],       1.04)
          (['8TeV'], [5],      ['ttbar'],          1.08)
          (['8TeV'], [5],      ['EWK'],            1.08))

    src.cp().era(['7TeV']).process_rgx([higgs_rgx, 'EWK', 'ttbar']).AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'lnN', ch.SystMap('bin_id')
          ([0, 1, 2, 3, 4], 1.05))

    src.cp().era(['8TeV']).process_rgx([higgs_rgx]).AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'lnN', ch.SystMap('bin_id')
          ([0],     0.98)
          ([2],     1.01)
          ([1, 3],  0.99)
          ([4, 5],  0.98))

    src.cp().era(['8TeV']).process(['EWK', 'ttbar']).AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'lnN', ch.SystMap('bin_id', 'process')
          ([0],   ['ttbar'],            1.01)
          ([1],   ['ttbar'],            0.99)
          ([4],   ['ttbar'],            1.00)
          ([4],   ['EWK'],              0.98)
          ([5],   ['EWK', 'ttbar'],     1.10))

    src.cp().process(['ttbar']).AddSyst(
        cb, 'CMS_eff_b_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'],  [0, 1],         0.96)
          (['7TeV'],  [2, 3, 4],      0.95)
          (['8TeV'],  [2, 3, 4, 5],   0.97))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'pdf_gg', 'lnN', ch.SystMap()(1.097))

    src.cp().process_rgx(['^qqH.*$']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap()(1.036))

    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap('bin_id')
          ([0, 1],            1.01)
          ([2, 3, 4, 5],      1.02))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH', 'lnN', ch.SystMap('bin_id')
          ([0, 1], 1.08))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH1in', 'lnN', ch.SystMap('bin_id')
          ([2], 1.105)
          ([3], 1.125))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'QCDscale_ggH2in', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [4], 1.274)
          (['8TeV'], [4], 1.228)
          (['8TeV'], [5], 1.307))

    src.cp().process_rgx(['^qqH.*$']).AddSyst(
        cb, 'QCDscale_qqH', 'lnN', ch.SystMap('bin_id')
          ([0], 1.034)
          ([1], 1.028)
          ([2], 1.008)
          ([3], 1.013)
          ([4], 1.019))

    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'QCDscale_VH', 'lnN', ch.SystMap()(1.04))

    src.cp().process_rgx(['^ggH.*$']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 1.035)
          ([1], 1.042)
          ([2], 0.984)
          ([3], 0.978)
          ([4], 0.890)
          ([5], 0.881))

    src.cp().process_rgx(['^qqH.*$', 'WH', 'ZH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 1.089)
          ([1], 1.063)
          ([4], 0.988)
          ([5], 0.986))

    src.cp().process(['Ztt']).AddSyst(
        cb, 'CMS_htt_zttNorm_$ERA', 'lnN', ch.SystMap()(1.03))

    src.cp().process(['Ztt']).AddSyst(
        cb, 'CMS_htt_extrap_ztt_$BIN_$ERA', 'lnN',
          ch.SystMap('bin_id')
          ([1, 2],  1.03)
          ([3],     1.05)
          ([4, 5],  1.10))

    src.cp().process(['ttbar']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [0, 1, 4],       1.08)
          (['7TeV'], [2, 3],          1.10)
          (['8TeV'], [0, 1, 2, 3],    1.10)
          (['8TeV'], [4, 5],          1.08))

    src.cp().process(['ttbar']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$BIN_$ERA', 'lnN',
          ch.SystMap('era', 'bin_id')
          (['7TeV'],  [4],       1.05)
          (['8TeV'],  [4, 5],    1.10))

    src.cp().process(['EWK']).AddSyst(
        cb, 'CMS_htt_DiBosonNorm_$ERA', 'lnN', ch.SystMap()(1.15))

    src.cp().process(['Fakes']).AddSyst(
        cb, 'CMS_htt_fakes_em_$ERA', 'lnN', ch.SystMap()(1.30))

    src.cp().process(['Fakes']).AddSyst(
        cb, 'CMS_htt_fakes_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'],  [1],          1.30)
          (['7TeV'],  [2],          1.11)
          (['7TeV'],  [3],          1.05)
          (['7TeV'],  [4],          1.09)
          (['8TeV'],  [1],          1.10)
          (['8TeV'],  [2, 3, 4, 5], 1.05))

    for b in src.cp().bin_id([0, 1, 2]).bin_set():
        clip = b.replace('emu_', 'em_')
        src.cp().process(['Fakes']).bin([b]).AddSyst(
          cb, 'CMS_htt_FakeShape_' + clip + '_$ERA', 'shape', ch.SystMap()(1.00))


def AddSystematics_tt(cb):
    src = cb.cp()
    src.channel(['tt'])

    signal = cb.cp().signals().process_set()

    src.cp().signals().AddSyst(
        cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')
          (['8TeV'], 1.026))

    src.cp().process(['ggH']).AddSyst(
        cb, 'pdf_gg', 'lnN', ch.SystMap()(1.097))

    src.cp().process(['qqH', 'WH', 'ZH']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap('process')
          (['qqH'],       1.036)
          (['WH', 'ZH'],  1.020))

    src.cp().process(['ggH']).AddSyst(
        cb, 'QCDscale_ggH1in', 'lnN', ch.SystMap('bin_id')
          ([0], 1.205)
          ([1], 1.175))

    src.cp().process(['ggH']).AddSyst(
        cb, 'QCDscale_ggH2in', 'lnN', ch.SystMap('bin_id')
          ([2], 1.41))

    src.cp().process(['qqH']).AddSyst(
        cb, 'QCDscale_qqH', 'lnN', ch.SystMap('bin_id')
          ([0], 1.012)
          ([1], 1.014)
          ([2], 1.013))

    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'QCDscale_VH', 'lnN', ch.SystMap('bin_id')
          ([0, 1, 2],   1.04))

    src.cp().process(['qqH', 'WH', 'ZH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 1.025)
          ([1], 0.996))
    src.cp().process(['ggH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([0], 0.975)
          ([1], 0.993)
          ([2], 0.900))

    src.cp().process(signal + ['ZTT', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_t_$CHANNEL_$ERA', 'lnN', ch.SystMap()(1.19))

    src.cp().process(signal +['ZTT']).AddSyst(
        cb, 'CMS_scale_t_tautau_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().AddSyst(
        cb, 'CMS_scale_j_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['8TeV'], [0],     ['qqH'],        0.99)
          (['8TeV'], [1],     ['qqH'],        0.99)
          (['8TeV'], [2],     ['ggH'],        1.035)
          (['8TeV'], [2],     ['qqH'],        1.015)
          (['8TeV'], [2],     ['WH', 'ZH'],   1.015)
          (['8TeV'], [2],     ['ZL', 'ZJ'],   1.03)
          (['8TeV'], [2],     ['TT'],         1.02)
          (['8TeV'], [2],     ['VV'],         1.08))

    src.cp().AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['8TeV'], [0],     ['W'],          1.015)
          (['8TeV'], [0],     ['TT'],         1.02)
          (['8TeV'], [1],     ['TT'],         1.02)
          (['8TeV'], [1],     signal,         1.03)
          (['8TeV'], [2],     ['W'],          1.015))

    src.cp().AddSyst(
        cb, 'CMS_eff_b_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['8TeV'], [0],     ['TT'],         0.93)
          (['8TeV'], [1],     ['TT'],         0.83)
          (['8TeV'], [2],     ['TT'],         0.93))

    src.cp().AddSyst(
        cb, 'CMS_fake_b_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['8TeV'], [0],     ['TT'],         0.96)
          (['8TeV'], [1],     ['TT'],         0.83)
          (['8TeV'], [2],     ['TT'],         0.96))

    src.cp().AddSyst(
        cb, 'CMS_htt_zttNorm_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['8TeV'], [0, 1],  ['ZTT', 'ZL', 'ZJ'],  1.033)
          (['8TeV'], [2],     ['ZTT', 'ZJ'],        1.03))

    src.cp().process(['ZTT']).AddSyst(
        cb, 'CMS_htt_extrap_ztt_$BIN_$ERA', 'lnN', ch.SystMap('bin_id')
          ([0, 1],   1.03)
          ([2],      1.10))

    src.cp().process(['TT']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$ERA', 'lnN', ch.SystMap()(1.10))

    src.cp().process(['TT']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['8TeV'], [0, 1], 1.05)
          (['8TeV'], [2],    1.24))

    src.cp().process(['W']).AddSyst(
        cb, 'CMS_htt_WNorm_$BIN_$ERA', 'lnN', ch.SystMap()(1.30))

    src.cp().process(['VV']).AddSyst(
        cb, 'CMS_htt_DiBosonNorm_$ERA', 'lnN', ch.SystMap()(1.15))

    src.cp().process(['VV']).AddSyst(
        cb, 'CMS_htt_DiBosonNorm_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['8TeV'], [0, 1],   1.15)
          (['8TeV'], [2],      1.13))

    src.cp().process(['QCD']).AddSyst(
        cb, 'CMS_htt_QCDSyst_$BIN_$ERA', 'lnN', ch.SystMap()(1.35))

    src.cp().process(['ZJ']).AddSyst(
        cb, 'CMS_htt_ZJetFakeTau_$BIN_$ERA', 'lnN', ch.SystMap()(1.20))

    src.cp().process(['ZL']).bin_id([0, 1]).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$BIN_$ERA', 'lnN', ch.SystMap()(1.30))

def AddSystematics_et_mt(cb):
    src = cb.cp()
    src.channel(['et', 'mt'])

    signal = cb.cp().signals().process_set()

    src.cp().signals().AddSyst(
        cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')
          (['7TeV'], 1.022)
          (['8TeV'], 1.026))

    src.cp().process(['ggH']).AddSyst(
        cb, 'pdf_gg', 'lnN', ch.SystMap()
        (1.097))

    src.cp().process(['qqH', 'WH', 'ZH']).AddSyst(
        cb, 'pdf_qqbar', 'lnN', ch.SystMap('channel', 'era', 'process')
          (['et', 'mt'],  ['7TeV', '8TeV'], ['qqH'],       1.036)
          (['et'],        ['7TeV'],         ['WH', 'ZH'],  1.02)
          (['et'],        ['8TeV'],         ['WH', 'ZH'],  1.04)
          (['mt'],        ['7TeV', '8TeV'], ['WH', 'ZH'],  1.04))

    src.cp().process(['ggH']).AddSyst(
        cb, 'QCDscale_ggH', 'lnN', ch.SystMap('bin_id')
          ([1, 2], 1.08))

    src.cp().process(['ggH']).AddSyst(
        cb, 'QCDscale_ggH1in', 'lnN', ch.SystMap('channel', 'bin_id')
          (['mt'], [3], 1.105)
          (['mt'], [4], 1.095)
          (['mt'], [5], 1.195)
          (['et'], [3], 1.125)
          (['et'], [5], 1.175))

    src.cp().process(['ggH']).AddSyst(
        cb, 'QCDscale_ggH2in', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'], ['7TeV', '8TeV'],  [6], 1.228)
          (['mt'], ['7TeV', '8TeV'],  [7], 1.307)
          (['et'], ['7TeV'],          [6], 1.275)
          (['et'], ['8TeV'],          [6], 1.228)
          (['et'], ['8TeV'],          [7], 1.307))

    src.cp().process(['qqH']).AddSyst(
        cb, 'QCDscale_qqH', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['et', 'mt'], ['7TeV', '8TeV'], [1], 1.022)
          (['et', 'mt'], ['7TeV', '8TeV'], [2], 1.023)
          (['et', 'mt'], ['7TeV', '8TeV'], [3], 1.015)
          (['et', 'mt'], ['7TeV', '8TeV'], [4], 1.013)
          (['et', 'mt'], ['7TeV', '8TeV'], [5], 1.015)
          (['mt'],       ['7TeV', '8TeV'], [6], 1.018)
          (['et'],       ['7TeV'],         [6], 0.981)
          (['et'],       ['8TeV'],         [6], 1.018)
          (['et', 'mt'], ['7TeV', '8TeV'], [7], 1.031))

    src.cp().process(['WH', 'ZH']).AddSyst(
        cb, 'QCDscale_VH', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'], ['7TeV', '8TeV'],  [1, 2],               1.010)
          (['mt'], ['7TeV', '8TeV'],  [3, 4, 5, 6, 7],      1.040)
          (['et'], ['7TeV'],          [1, 2, 3, 5, 6, 7],   1.040)
          (['et'], ['8TeV'],          [1, 2],               1.010)
          (['et'], ['8TeV'],          [3, 5, 6, 7],         1.040))

    src.cp().process(['qqH', 'WH', 'ZH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([1], 1.050)
          ([2], 1.060)
          ([3], 1.007)
          ([4], 0.996)
          ([5], 1.006)
          ([6], 0.988)
          ([7], 0.986))
    src.cp().process(['ggH']).AddSyst(
        cb, 'UEPS', 'lnN', ch.SystMap('bin_id')
          ([1], 1.013)
          ([2], 1.028)
          ([3], 0.946)
          ([4], 0.954)
          ([5], 0.983)
          ([6], 0.893)
          ([7], 0.881))

    src.cp().channel(['mt']).process(signal + ['ZTT', 'ZL', 'ZJ', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_m', 'lnN', ch.SystMap()(1.02))

    src.cp().channel(['et']).process(signal + ['ZTT', 'ZL', 'ZJ', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_e', 'lnN', ch.SystMap()(1.02))

    src.cp().process(signal + ['ZTT', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_t_$CHANNEL_$ERA', 'lnN', ch.SystMap()(1.08))

    src.cp().process(signal + ['ZTT', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_t_$CHANNEL_medium_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'], ['7TeV', '8TeV'],  [1, 3],  1.03)
          (['mt'], ['7TeV', '8TeV'],  [6, 7],  1.01)
          (['et'], ['7TeV'],          [1],     1.03)
          (['et'], ['7TeV'],          [3],     1.08)
          (['et'], ['8TeV'],          [1, 3],  1.03)
          (['et'], ['7TeV', '8TeV'],  [6, 7],  1.01))

    src.cp().process(signal + ['ZTT', 'TT', 'VV']).AddSyst(
        cb, 'CMS_eff_t_$CHANNEL_high_$ERA', 'lnN', ch.SystMap('channel', 'bin_id')
          (['et', 'mt'],  [2, 4, 5],  1.030)
          (['et', 'mt'],  [6],        1.012)
          (['mt'],        [7],        1.015)
          (['et'],        [7],        1.012))

    src.cp().channel(['mt']).process(signal + ['ZTT']).AddSyst(
        cb, 'CMS_scale_t_mutau_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().channel(['et']).process(signal + ['ZTT']).AddSyst(
        cb, 'CMS_scale_t_etau_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().channel(['mt']).AddSyst(
        cb, 'CMS_scale_j_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['7TeV'], [1, 2],  ['ggH'],        0.98)
          (['7TeV'], [1, 2],  ['qqH'],        0.86)
          (['7TeV'], [1, 2],  ['WH', 'ZH'],   0.97)
          (['7TeV'], [1, 2],  ['TT'],         0.99)
          (['7TeV'], [1, 2],  ['VV'],         0.98)
          (['7TeV'], [3],     ['ggH'],        1.05)
          (['7TeV'], [3],     ['qqH'],        1.01)
          (['7TeV'], [3],     ['WH', 'ZH'],   1.05)
          (['7TeV'], [3],     ['VV'],         1.02)
          (['7TeV'], [4, 5],  ['ggH'],        1.03)
          (['7TeV'], [4, 5],  ['qqH'],        1.02)
          (['7TeV'], [4, 5],  ['WH', 'ZH'],   1.03)
          (['7TeV'], [4, 5],  ['TT'],         1.01)
          (['7TeV'], [4, 5],  ['VV'],         1.04)
          (['7TeV'], [6],     ['ggH'],        1.20)
          (['7TeV'], [6],     ['qqH'],        1.05)
          (['7TeV'], [6],     ['WH', 'ZH'],   1.20)
          (['7TeV'], [6],     ['TT'],         1.10)
          (['7TeV'], [6],     ['VV'],         1.15)
          (['8TeV'], [1],     ['ggH'],        0.98)
          (['8TeV'], [1],     ['qqH'],        0.92)
          (['8TeV'], [1],     ['WH', 'ZH'],   0.96)
          (['8TeV'], [1],     ['ZL'],         0.99)
          (['8TeV'], [1],     ['ZJ'],         0.98)
          (['8TeV'], [1],     ['TT'],         0.95)
          (['8TeV'], [1],     ['VV'],         0.98)
          (['8TeV'], [2],     ['ggH'],        0.98)
          (['8TeV'], [2],     ['qqH'],        0.92)
          (['8TeV'], [2],     ['WH', 'ZH'],   0.88)
          (['8TeV'], [2],     ['ZL'],         0.99)
          (['8TeV'], [2],     ['ZJ'],         0.97)
          (['8TeV'], [2],     ['TT'],         0.84)
          (['8TeV'], [2],     ['VV'],         0.97)
          (['8TeV'], [3],     ['ggH'],        1.04)
          (['8TeV'], [3],     ['qqH'],        0.99)
          (['8TeV'], [3],     ['WH', 'ZH'],   1.01)
          (['8TeV'], [3],     ['ZL', 'ZJ'],   1.02)
          (['8TeV'], [3],     ['VV'],         1.03)
          (['8TeV'], [4],     ['ggH'],        1.04)
          (['8TeV'], [4],     ['WH', 'ZH'],   1.03)
          (['8TeV'], [4],     ['ZL', 'ZJ'],   1.02)
          (['8TeV'], [4],     ['VV'],         1.02)
          (['8TeV'], [5],     ['ggH'],        1.02)
          (['8TeV'], [5],     ['WH', 'ZH'],   1.01)
          (['8TeV'], [5],     ['TT'],         0.97)
          (['8TeV'], [5],     ['VV'],         1.03)
          (['8TeV'], [6],     ['ggH'],        1.10)
          (['8TeV'], [6],     ['qqH'],        1.04)
          (['8TeV'], [6],     ['WH', 'ZH'],   1.15)
          (['8TeV'], [6],     ['ZL'],         1.05)
          (['8TeV'], [6],     ['ZJ'],         1.10)
          (['8TeV'], [6],     ['TT'],         1.05)
          (['8TeV'], [6],     ['VV'],         1.08)
          (['8TeV'], [7],     ['ggH'],        1.06)
          (['8TeV'], [7],     ['qqH'],        1.03)
          (['8TeV'], [7],     ['WH', 'ZH'],   1.15)
          (['8TeV'], [7],     ['ZL'],         1.05)
          (['8TeV'], [7],     ['TT'],         1.05)
          (['8TeV'], [7],     ['VV'],         1.10))

    src.cp().channel(['et']).AddSyst(
        cb, 'CMS_scale_j_$ERA', 'lnN', ch.SystMap('era', 'bin_id', 'process')
          (['7TeV'], [1, 2],  ['ggH'],        0.97)
          (['7TeV'], [1, 2],  ['qqH'],        0.85)
          (['7TeV'], [1, 2],  ['WH', 'ZH'],   0.95)
          (['7TeV'], [1, 2],  ['TT'],         0.98)
          (['7TeV'], [1, 2],  ['VV'],         0.97)
          (['7TeV'], [3],     ['ggH'],        1.02)
          (['7TeV'], [3],     ['qqH'],        1.03)
          (['7TeV'], [3],     ['WH', 'ZH'],   1.02)
          (['7TeV'], [3],     ['VV'],         1.01)
          (['7TeV'], [5],     ['ggH'],        1.06)
          (['7TeV'], [5],     ['qqH'],        1.02)
          (['7TeV'], [5],     ['WH', 'ZH'],   1.06)
          (['7TeV'], [5],     ['VV'],         1.02)
          (['7TeV'], [6],     ['ggH'],        1.20)
          (['7TeV'], [6],     ['qqH'],        1.07)
          (['7TeV'], [6],     ['WH', 'ZH'],   1.20)
          (['7TeV'], [6],     ['TT'],         1.10)
          (['7TeV'], [6],     ['VV'],         1.25)
          (['8TeV'], [1],     ['ggH'],        0.98)
          (['8TeV'], [1],     ['qqH'],        0.90)
          (['8TeV'], [1],     ['WH', 'ZH'],   0.96)
          (['8TeV'], [1],     ['ZL'],         0.99)
          (['8TeV'], [1],     ['ZJ'],         0.92)
          (['8TeV'], [1],     ['TT'],         0.95)
          (['8TeV'], [1],     ['VV'],         0.97)
          (['8TeV'], [2],     ['ggH'],        0.98)
          (['8TeV'], [2],     ['qqH'],        0.89)
          (['8TeV'], [2],     ['WH', 'ZH'],   0.95)
          (['8TeV'], [2],     ['ZL'],         0.99)
          (['8TeV'], [2],     ['ZJ'],         0.94)
          (['8TeV'], [2],     ['TT'],         0.84)
          (['8TeV'], [2],     ['VV'],         0.98)
          (['8TeV'], [3],     ['ggH'],        1.01)
          (['8TeV'], [3],     ['qqH'],        0.99)
          (['8TeV'], [3],     ['WH', 'ZH'],   1.01)
          (['8TeV'], [3],     ['VV'],         1.03)
          (['8TeV'], [5],     ['ggH'],        1.02)
          (['8TeV'], [5],     ['WH', 'ZH'],   1.01)
          (['8TeV'], [5],     ['TT'],         0.97)
          (['8TeV'], [5],     ['VV'],         1.03)
          (['8TeV'], [6],     ['ggH'],        1.10)
          (['8TeV'], [6],     ['qqH'],        1.05)
          (['8TeV'], [6],     ['WH', 'ZH'],   1.15)
          (['8TeV'], [6],     ['ZL'],         1.08)
          (['8TeV'], [6],     ['ZJ'],         1.08)
          (['8TeV'], [6],     ['TT'],         1.05)
          (['8TeV'], [6],     ['VV'],         1.10)
          (['8TeV'], [7],     ['ggH'],        1.06)
          (['8TeV'], [7],     ['qqH'],        1.03)
          (['8TeV'], [7],     ['WH', 'ZH'],   1.15)
          (['8TeV'], [7],     ['ZL'],         1.08)
          (['8TeV'], [7],     ['TT'],         1.05)
          (['8TeV'], [7],     ['VV'],         1.10))

    src.cp().AddSyst(
        cb, 'CMS_htt_scale_met_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id', 'process')
          (['et', 'mt'], ['7TeV'], [1, 2, 3, 4, 5, 6], signal,             1.05)
          (['mt'],       ['7TeV'], [1, 2, 3, 4, 5, 6], ['TT', 'W'],        1.07)
          (['et'],       ['7TeV'], [1, 2, 3, 4, 5, 6], ['TT', 'VV'],       1.07)
          (['et', 'mt'], ['7TeV'], [1, 2, 3, 4, 5, 6], ['ZL', 'ZJ'],       1.05)
          (['et', 'mt'], ['8TeV'], [1],                ['TT'],             1.05)
          (['et', 'mt'], ['8TeV'], [1],                ['W'],              1.01)
          (['et', 'mt'], ['8TeV'], [2],                signal,             1.01)
          (['et', 'mt'], ['8TeV'], [2],                ['TT'],             1.04)
          (['et', 'mt'], ['8TeV'], [2],                ['W'],              1.01)
          (['et', 'mt'], ['8TeV'], [2],                ['ZL'],             1.02)
          (['et', 'mt'], ['8TeV'], [3],                signal,             0.99)
          (['mt'],       ['8TeV'], [3],                ['TT'],             1.02)
          (['et'],       ['8TeV'], [3],                ['TT', 'VV', 'ZJ'], 1.01)
          (['et', 'mt'], ['8TeV'], [3],                ['W'],              1.01)
          (['et', 'mt'], ['8TeV'], [3],                ['ZL'],             1.02)
          (['et', 'mt'], ['8TeV'], [4],                signal,             0.99)
          (['et', 'mt'], ['8TeV'], [4],                ['TT'],             1.02)
          (['et', 'mt'], ['8TeV'], [4],                ['W'],              1.01)
          (['et', 'mt'], ['8TeV'], [4],                ['ZL'],             1.03)
          (['mt'],       ['8TeV'], [5],                signal,             0.99)
          (['et'],       ['8TeV'], [5],                signal,             0.98)
          (['et', 'mt'], ['8TeV'], [5],                ['TT'],             1.01)
          (['et', 'mt'], ['8TeV'], [5],                ['W'],              1.03)
          (['mt'],       ['8TeV'], [5],                ['ZL'],             1.02)
          (['et'],       ['8TeV'], [5],                ['ZL'],             1.12)
          (['mt'],       ['8TeV'], [5],                ['ZJ'],             0.98)
          (['et'],       ['8TeV'], [5],                ['ZJ'],             0.97)
          (['et', 'mt'], ['8TeV'], [6],                signal,             0.99)
          (['et', 'mt'], ['8TeV'], [6],                ['TT', 'W'],        1.04)
          (['et', 'mt'], ['8TeV'], [6],                ['ZL', 'ZJ'],       1.03)
          (['et', 'mt'], ['8TeV'], [7],                signal,             0.99)
          (['et', 'mt'], ['8TeV'], [7],                ['TT', 'W'],        1.03)
          (['et', 'mt'], ['8TeV'], [7],                ['ZL', 'ZJ'],       1.03))

    src.cp().AddSyst(
        cb, 'CMS_eff_b_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id', 'process')
          (['mt'],        ['7TeV'], [1, 2, 3, 4, 5, 6],  ['TT'],      0.90)
          (['mt'],        ['7TeV'], [3, 4, 5],           ['VV'],      0.98)
          (['et'],        ['7TeV'], [1],                 ['TT'],      0.97)
          (['et'],        ['7TeV'], [2, 3, 5, 6],        ['TT'],      0.94)
          (['et'],        ['7TeV'], [3, 5],              ['VV'],      0.97)
          (['et'],        ['7TeV'], [6],                 ['VV'],      0.85)
          (['mt'],        ['8TeV'], [1],                 ['TT'],      0.98)
          (['et'],        ['8TeV'], [1],                 ['TT'],      0.96)
          (['et', 'mt'],  ['8TeV'], [2, 3, 4],           ['TT'],      0.96)
          (['mt'],        ['8TeV'], [5, 6, 7],           ['TT'],      0.94)
          (['et'],        ['8TeV'], [5, 6, 7],           ['TT'],      0.96))

    src.cp().process(['ZTT', 'ZL', 'ZJ']).AddSyst(
        cb, 'CMS_htt_zttNorm_$ERA', 'lnN', ch.SystMap()(1.03))

    src.cp().process(['ZTT']).AddSyst(
        cb, 'CMS_htt_extrap_ztt_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'bin_id')
          (['et', 'mt'], [1, 2, 3, 4, 5],   1.05)
          (['et', 'mt'], [6],               1.10)
          (['mt'],       [7],               1.13)
          (['et'],       [7],               1.16))
    src.cp().channel(['et']).bin_id([6]).era(['7TeV']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_extrap_ztt_$BIN_$ERA', 'lnN', ch.SystMap()(1.10))

    src.cp().process(['TT']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [1, 2, 3, 4, 5, 6],    1.08)
          (['8TeV'], [1, 2, 3, 4, 5],       1.10)
          (['8TeV'], [6, 7],                1.08))

    src.cp().process(['TT']).AddSyst(
        cb, 'CMS_htt_ttbarNorm_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'],  ['7TeV'], [6],     1.20)
          (['mt'],  ['8TeV'], [6, 7],  1.33)
          (['et'],  ['7TeV'], [6],     1.23)
          (['et'],  ['8TeV'], [6, 7],  1.33))

    src.cp().process(['W']).AddSyst(
        cb, 'CMS_htt_WNorm_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt', 'et'], ['7TeV'], [1, 2],    1.20)
          (['mt', 'et'], ['7TeV'], [3, 4],    1.10)
          (['mt'],       ['7TeV'], [5],       1.12)
          (['et'],       ['7TeV'], [5],       1.10)
          (['mt'],       ['7TeV'], [6],       1.20)
          (['et'],       ['7TeV'], [6],       1.50)
          (['mt', 'et'], ['8TeV'], [1, 2],    1.20)
          (['mt'],       ['8TeV'], [3],       1.15)
          (['et'],       ['8TeV'], [3],       1.16)
          (['mt', 'et'], ['8TeV'], [4],       1.11)
          (['mt'],       ['8TeV'], [5],       1.16)
          (['et'],       ['8TeV'], [5],       1.17)
          (['mt'],       ['8TeV'], [6],       1.21)
          (['et'],       ['8TeV'], [6],       1.26)
          (['mt'],       ['8TeV'], [7],       1.51)
          (['et'],       ['8TeV'], [7],       1.56))

    src.cp().process(['VV']).AddSyst(
        cb, 'CMS_htt_DiBosonNorm_$ERA', 'lnN', ch.SystMap()(1.15))

    src.cp().process(['VV']).AddSyst(
        cb, 'CMS_htt_DiBosonNorm_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'],      ['7TeV'], [6],      1.37)
          (['et'],      ['7TeV'], [6],      1.40)
          (['mt'],      ['8TeV'], [6],      1.50)
          (['mt'],      ['8TeV'], [7],      1.45)
          (['et'],      ['8TeV'], [6],      1.39)
          (['et'],      ['8TeV'], [7],      1.33))

    src.cp().process(['QCD']).AddSyst(
        cb, 'CMS_htt_QCDSyst_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['mt'],      ['7TeV'], [1, 2, 3, 4, 5],   1.10)
          (['et'],      ['7TeV'], [1, 2],            1.20)
          (['et'],      ['7TeV'], [3, 5],            1.10)
          (['mt'],      ['7TeV'], [6],               1.22)
          (['et'],      ['7TeV'], [6],               1.40)
          (['mt'],      ['8TeV'], [1, 2],            1.06)
          (['mt'],      ['8TeV'], [3, 4, 5],         1.10)
          (['mt'],      ['8TeV'], [6],               1.30)
          (['mt'],      ['8TeV'], [7],               1.70)
          (['et'],      ['8TeV'], [1, 2, 3, 5],      1.10)
          (['et'],      ['8TeV'], [6],               1.30)
          (['et'],      ['8TeV'], [7],               2.00))

    src.cp().channel(['mt']).process(['QCD']).bin_id([3]).AddSyst(
        cb, 'CMS_htt_QCDShape_mutau_1jet_medium_$ERA', 'shape', ch.SystMap()(1.00))
    src.cp().channel(['et']).process(['QCD']).bin_id([3]).AddSyst(
        cb, 'CMS_htt_QCDShape_etau_1jet_medium_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().channel(['mt']).process(['QCD']).bin_id([4]).AddSyst(
        cb, 'CMS_htt_QCDShape_mutau_1jet_high_lowhiggs_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().channel(['mt']).process(['QCD']).bin_id([6]).era(['7TeV']).AddSyst(
        cb, 'CMS_htt_QCDShape_mutau_vbf_$ERA', 'shape', ch.SystMap()(1.00))
    src.cp().channel(['et']).process(['QCD']).bin_id([6]).era(['7TeV']).AddSyst(
        cb, 'CMS_htt_QCDShape_etau_vbf_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().channel(['mt']).process(['QCD']).bin_id([6]).era(['8TeV']).AddSyst(
        cb, 'CMS_htt_QCDShape_mutau_vbf_loose_$ERA', 'shape', ch.SystMap()(1.00))
    src.cp().channel(['et']).process(['QCD']).bin_id([6]).era(['8TeV']).AddSyst(
        cb, 'CMS_htt_QCDShape_etau_vbf_loose_$ERA', 'shape', ch.SystMap()(1.00))

    src.cp().process(['ZJ']).AddSyst(
        cb, 'CMS_htt_ZJetFakeTau_$BIN_$ERA', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
          (['et', 'mt'],  ['7TeV', '8TeV'], [1, 2, 3, 4, 5],   1.20)
          (['mt'],        ['7TeV', '8TeV'], [6],               1.30)
          (['et'],        ['7TeV'],         [6],               1.56)
          (['et'],        ['8TeV'],         [6],               1.20)
          (['mt'],        ['8TeV'],         [7],               1.80)
          (['et'],        ['8TeV'],         [7],               1.65))

    src.cp().channel(['mt']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_$ERA', 'lnN', ch.SystMap()(1.30))

    src.cp().channel(['et']).process(['ZL']).bin_id([3, 6, 7]).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_low_$ERA', 'lnN',
          ch.SystMap('bin_id')([3], 1.20)([6, 7], 1.06))
    src.cp().channel(['et']).process(['ZL']).bin_id([3, 5]).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_met_$ERA', 'lnN',
          ch.SystMap()(1.30))
    src.cp().channel(['et']).process(['ZL']).bin_id([1, 6, 7]).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_medium_$ERA', 'lnN',
          ch.SystMap('bin_id')([1], 1.20)([6, 7], 1.08))
    src.cp().channel(['et']).process(['ZL']).bin_id([3]).era(['8TeV']).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_medium_$ERA', 'lnN',
          ch.SystMap('bin_id')([3], 1.20))
    src.cp().channel(['et']).process(['ZL']).bin_id([2, 5, 6, 7]).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$CHANNEL_high_$ERA', 'lnN',
          ch.SystMap('bin_id')([2, 5], 1.20)([6, 7], 1.06))

    src.cp().channel(['mt']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['7TeV'], [6],       2.00)
          (['8TeV'], [5],       1.26)
          (['8TeV'], [6],       1.70))

    src.cp().channel(['et']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_ZLeptonFakeTau_$BIN_$ERA', 'lnN', ch.SystMap('era', 'bin_id')
          (['8TeV'], [5],       1.30)
          (['8TeV'], [6],       1.70)
          (['8TeV'], [7],       1.74))

    src.cp().channel(['mt']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_ZLScale_mutau_$ERA', 'shape', ch.SystMap()(1.00))
    src.cp().channel(['et']).process(['ZL']).AddSyst(
        cb, 'CMS_htt_ZLScale_etau_$ERA', 'shape', ch.SystMap()(1.00))
