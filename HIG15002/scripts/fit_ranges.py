#!/usr/bin/env python 
import sys

RANGES = {
  'A1_mu' : {
    'mu' : 0.111
  },
  'A1_4P' : {
    'mu_XS_ggFbbH'    : 0.163,
    'mu_XS_VBF'       : 0.252,
    'mu_XS_VH'        : 0.396,
    'mu_XS_ttHtH'     : 0.678
  },
  'A1_5P' : {
    'mu_XS_ggFbbH'    : 0.163,
    'mu_XS_VBF'       : 0.252,
    'mu_XS_WH'        : 0.396,
    'mu_XS_ZH'        : 0.387,
    'mu_XS_ttHtH'     : 0.678
  },
  'A1_5D' : {
    'mu_BR_gamgam'    :0.197,
    'mu_BR_ZZ'        :0.271,
    'mu_BR_WW'        :0.187,
    'mu_BR_tautau'    :0.244,
    'mu_BR_bb'        :0.301
  },
  'A1_6D' : {
    'mu_BR_gamgam'    :0.197,
    'mu_BR_ZZ'        :0.271,
    'mu_BR_WW'        :0.187,
    'mu_BR_tautau'    :0.244,
    'mu_BR_bb'        :0.301,
    'mu_BR_mumu'      :2.000
  },
  'A1_5PD_cms' : {
      'mu_XS_ggFbbH_BR_WW':     0.5,
      'mu_XS_VBF_BR_WW':        1.0,
      'mu_XS_WH_BR_WW':         2.5,
      'mu_XS_ZH_BR_WW':         5.0,
      'mu_XS_ttHtH_BR_WW':      5.0,
      'mu_XS_ggFbbH_BR_ZZ':     0.5,
      'mu_XS_VBF_BR_ZZ':        1.0,
      'mu_XS_WH_BR_ZZ':         5.0,
      'mu_XS_ZH_BR_ZZ':         50.0,
      'mu_XS_ttHtH_BR_ZZ':      50.0,
      'mu_XS_WH_BR_bb':         1.0,
      'mu_XS_ZH_BR_bb':         1.0,
      'mu_XS_ttHtH_BR_bb':      2.5,
      'mu_XS_ggFbbH_BR_gamgam': 0.5,
      'mu_XS_VBF_BR_gamgam':    1.0,
      'mu_XS_WH_BR_gamgam':     2.5,
      'mu_XS_ZH_BR_gamgam':     5.0,
      'mu_XS_ttHtH_BR_gamgam':  10.0,
      'mu_XS_ggFbbH_BR_tautau': 1.0,
      'mu_XS_VBF_BR_tautau':    1.0,
      'mu_XS_WH_BR_tautau':     2.5,
      'mu_XS_ZH_BR_tautau':     2.5,
      'mu_XS_ttHtH_BR_tautau':  10.0
  },
  'A1_muVmuF' : {
    'mu_V_gamgam'     :0.443,
    'mu_V_ZZ'         :1.367,
    'mu_V_WW'         :0.412,
    'mu_V_tautau'     :0.375,
    'mu_V_bb'         :0.300,
    'mu_F_gamgam'     :0.277,
    'mu_F_ZZ'         :0.380,
    'mu_F_WW'         :0.232,
    'mu_F_tautau'     :0.575,
    'mu_F_bb'         :0.937
  },
  'A2' : {
    'mu_V_r_F'        :0.356,
    'mu_F_gamgam'     :0.222,
    'mu_F_ZZ'         :0.269,
    'mu_F_WW'         :0.197,
    'mu_F_tautau'     :0.317,
    'mu_F_bb'         :0.370
  },
  'B1WW' : {
    'mu_XS_ggF_x_BR_WW'     :0.194,
    'mu_XS_VBF_r_XS_ggF'    :0.461,
    'mu_XS_WH_r_XS_ggF'     :0.822,
    'mu_XS_ZH_r_XS_ggF'     :1.931,
    'mu_XS_ttH_r_XS_ggF'    :1.314,
    'mu_BR_ZZ_r_BR_WW'      :0.297,
    'mu_BR_gamgam_r_BR_WW'  :0.218,
    'mu_BR_tautau_r_BR_WW'  :0.273,
    'mu_BR_bb_r_BR_WW'      :0.300
  },
  'B1ZZ' : {
    'mu_XS_ggF_x_BR_ZZ'     :0.255,
    'mu_BR_gamgam_r_BR_ZZ'  :0.222,
    'mu_BR_WW_r_BR_ZZ'      :0.208,
    'mu_BR_tautau_r_BR_ZZ'  :0.262,
    'mu_BR_bb_r_BR_ZZ'      :0.300,
    'mu_XS_VBF_r_XS_ggF'    :0.451,
    'mu_XS_WH_r_XS_ggF'     :0.799,
    'mu_XS_ZH_r_XS_ggF'     :1.906,
    'mu_XS_ttH_r_XS_ggF'    :1.224
  },
  'B1WW_P78' : {
    'mu_XS_ggF_x_BR_WW'     :0.194,
    'mu_XS_VBF_r_XS_ggF'    :0.461,
    'mu_XS_WH_r_XS_ggF'     :0.822,
    'mu_XS_ZH_r_XS_ggF'     :1.931,
    'mu_XS_ttH_r_XS_ggF'    :1.314,
    'mu_BR_ZZ_r_BR_WW'      :0.297,
    'mu_BR_gamgam_r_BR_WW'  :0.218,
    'mu_BR_tautau_r_BR_WW'  :0.273,
    'mu_BR_bb_r_BR_WW'      :0.248,
    'mu_XS7_r_XS8_VBF'      :1.000,
    'mu_XS7_r_XS8_WH'       :2.000,
    'mu_XS7_r_XS8_ZH'       :2.000,
    'mu_XS7_r_XS8_ggF'      :1.000,
    'mu_XS7_r_XS8_ttH'      :2.000
  },
  'B1ZZ_P78' : {
    'mu_XS_ggF_x_BR_ZZ'     :0.255,
    'mu_BR_gamgam_r_BR_ZZ'  :0.222,
    'mu_BR_WW_r_BR_ZZ'      :0.208,
    'mu_BR_tautau_r_BR_ZZ'  :0.262,
    'mu_BR_bb_r_BR_ZZ'      :0.210,
    'mu_XS_VBF_r_XS_ggF'    :0.451,
    'mu_XS_WH_r_XS_ggF'     :0.799,
    'mu_XS_ZH_r_XS_ggF'     :1.906,
    'mu_XS_ttH_r_XS_ggF'    :1.224,
    'mu_XS7_r_XS8_VBF'      :1.000,
    'mu_XS7_r_XS8_WH'       :2.000,
    'mu_XS7_r_XS8_ZH'       :2.000,
    'mu_XS7_r_XS8_ggF'      :1.000,
    'mu_XS7_r_XS8_ttH'      :2.000
  },
  'B1WW_TH' : {
    'mu_XS_ggF_x_BR_WW'     :0.194,
    'mu_XS_VBF_r_XS_ggF'    :0.461,
    'mu_XS_WH_r_XS_ggF'     :0.822,
    'mu_XS_ZH_r_XS_ggF'     :1.931,
    'mu_XS_ttH_r_XS_ggF'    :1.314,
    'mu_BR_ZZ_r_BR_WW'      :0.297,
    'mu_BR_gamgam_r_BR_WW'  :0.218,
    'mu_BR_tautau_r_BR_WW'  :0.273,
    'mu_BR_bb_r_BR_WW'      :0.300
  },
  'B1ZZ_TH' : {
    'mu_XS_ggF_x_BR_ZZ'     :0.255,
    'mu_BR_gamgam_r_BR_ZZ'  :0.222,
    'mu_BR_WW_r_BR_ZZ'      :0.208,
    'mu_BR_tautau_r_BR_ZZ'  :0.262,
    'mu_BR_bb_r_BR_ZZ'      :0.300,
    'mu_XS_VBF_r_XS_ggF'    :0.451,
    'mu_XS_WH_r_XS_ggF'     :0.799,
    'mu_XS_ZH_r_XS_ggF'     :1.906,
    'mu_XS_ttH_r_XS_ggF'    :1.224
  },
  'B2' : {
    'mu_XS_ggF_x_BR_WW'     :0.155,
    'mu_XS_VBF_x_BR_tautau' :0.261,
    'mu_XS_WH_r_XS_VBF'     :0.600,
    'mu_XS_ZH_r_XS_WH'      :3.000,
    'mu_XS_ttH_r_XS_ggF'    :1.114,
    'mu_BR_ZZ_r_BR_WW'      :0.280,
    'mu_BR_gamgam_r_BR_WW'  :0.208,
    'mu_BR_tautau_r_BR_WW'  :0.247,
    'mu_BR_bb_r_BR_tautau'  :0.296
  },
  'D1_general' : {
    'l_VBF_WW'          :1.0,
    'l_VBF_ZZ'          :1.0,
    'l_VBF_gamgam'      :1.0,
    'l_VBF_tautau'      :1.5,
    'l_WH_WW'           :2.0,
    'l_WH_ZZ'           :10.000,
    'l_WH_bb'           :2.0,
    'l_WH_gamgam'       :2.0,
    'l_WH_tautau'       :2.0,
    'l_ZH_WW'           :5.0,
    'l_ZH_ZZ'           :10.0,
    'l_ZH_bb'           :1.0,
    'l_ZH_gamgam'       :5.0,
    'l_ZH_tautau'       :7.0,
    'l_ttH_WW'          :2.0,
    'l_ttH_ZZ'          :10.0,
    'l_ttH_bb'          :2.0,
    'l_ttH_gamgam'      :2.0,
    'l_ttH_tautau'      :2.0,
    'mu_WW'             :0.2,
    'mu_ZZ'             :0.2,
    'mu_bb'             :0.2,
    'mu_gamgam'         :0.2,
    'mu_tautau'         :0.2
  },
  'D1_rank1' : {
    'mu_WW'     : 0.2,
    'mu_ZZ'     : 0.2,
    'mu_gamgam' : 0.2,
    'mu_tautau' : 0.2,
    'mu_bb'     : 0.2,
    'l_VBF'     : 0.5,
    'l_WH'      : 1.0,
    'l_ZH'      : 1.0,
    'l_ttH'     : 2.0
  },
  'K1' : {
    'kappa_Z'       :0.104,
    'kappa_W'       :0.094,
    'kappa_t'       :0.143,
    'kappa_tau'     :0.139,
    'kappa_b'       :0.209
  },
  'K1_mm' : {
    'kappa_Z'       :0.104,
    'kappa_W'       :0.094,
    'kappa_t'       :0.143,
    'kappa_tau'     :0.139,
    'kappa_b'       :0.209,
    'kappa_mu'      :1.500
  },
  'K2' : {
    'kappa_Z'       :0.109,
    'kappa_W'       :0.098,
    'kappa_t'       :0.226,
    'kappa_tau'     :0.124,
    'kappa_b'       :0.187,
    'kappa_g'       :0.115,
    'kappa_gam'     :0.107
  },
  'K2_BSM' : {
    'kappa_Z'       :0.109,
    'kappa_W'       :0.098,
    'kappa_t'       :0.226,
    'kappa_tau'     :0.124,
    'kappa_b'       :0.187,
    'kappa_g'       :0.115,
    'kappa_gam'     :0.107,
    'BRinv'         :0.100
  },
  'K3' : {
    'kappa_V'       :0.053,
    'kappa_F'       :0.109
  },
  'K3_5D' : {
    'kappa_F_WW'      :0.206628,
    'kappa_F_ZZ'      :0.546678,
    'kappa_F_bb'      :0.125614,
    'kappa_F_gamgam'  :0.186866,
    'kappa_F_tautau'  :0.142708,
    'kappa_V_WW'	    :0.0760111,
    'kappa_V_ZZ'      :0.152273,
    'kappa_V_bb'      :4.34253,
    'kappa_V_gamgam'  :0.0698755,
    'kappa_V_tautau'  :0.296897
  },
  'L1' : {
    'kappa_gZ'      :0.114,
    'lambda_WZ'     :0.097,
    'lambda_Zg'     :0.223,
    'lambda_bZ'     :0.162,
    'lambda_gamZ'   :0.112,
    'lambda_tauZ'   :0.137,
    'lambda_tg'     :0.313
  },
  'L2_ldu' : {
    'lambda_du'     :0.125,
    'lambda_Vu'     :0.133,
    'kappa_uu'      :0.221
  },
  'L2_lfv' : {
    'lambda_FV'     :0.096,
    'kappa_VV'      :0.098
  },
  'L2_llq' : {
    'lambda_lq'     :0.155,
    'lambda_Vq'     :0.137,
    'kappa_qq'      :0.166
  },
  'M1' : {
    'M'             :10.0,
    'eps'           :0.03
  }
}

assert(len(sys.argv) >= 3)

multiplier = 1.

if len(sys.argv) >= 4:
  multiplier = float(sys.argv[3])

sys.stdout.write(str(RANGES[sys.argv[1]][sys.argv[2]] * multiplier))

