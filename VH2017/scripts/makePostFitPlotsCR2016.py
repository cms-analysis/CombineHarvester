import os

CHN_DICT_SR = {
    "Wen": [["vhbb_Wen_7_13TeV2016","1-lepton (e),t#bar{t} enriched"],["vhbb_Wen_5_13TeV2016","1-lepton (e), high Mjj W+b#bar{b} enr."],["vhbb_Wen_6_13TeV2016","1-lepton (e), low Mjj, W+b#bar{b} enr."],["vhbb_Wen_3_13TeV2016","1-lepton (e),W+udcsg enr."]],
    "Wmn": [["vhbb_Wmn_7_13TeV2016","1-lepton (#mu),t#bar{t} enriched"],["vhbb_Wmn_5_13TeV2016","1-lepton (#mu), high Mjj W+b#bar{b} enr."],["vhbb_Wmn_6_13TeV2016","1-lepton (#mu), low Mjj, W+b#bar{b} enr."],["vhbb_Wmn_3_13TeV2016","1-lepton (#mu),W+udcsg enr."]],
    "Zee": [["vhbb_Zee_7_13TeV2016","2-lepton (e), High p_{T} (V), t#bar{t} enr."],["vhbb_Zee_5_13TeV2016","2-lepton (e), High p_{T} (V),Z+b#bar{b} enr."],["vhbb_Zee_3_13TeV2016","2-lepton (e), High p_{T} (V), Z+udcsg enr."],["vhbb_Zee_8_13TeV2016","2-lepton (e), Low p_{T} (V), t#bar{t} enr."],["vhbb_Zee_6_13TeV2016","2-lepton (e), Low p_{T} (V), Z+b#bar{b} enr."],["vhbb_Zee_4_13TeV2016","2-lepton (e), Low p_{T} (V), Z+udcsg enr."]],
    "Zmm": [["vhbb_Zmm_7_13TeV2016","2-lepton (#mu), High p_{T} (V), t#bar{t} enr."],["vhbb_Zmm_5_13TeV2016","2-lepton (#mu), High p_{T} (V),Z+b#bar{b} enr."],["vhbb_Zmm_3_13TeV2016","2-lepton (#mu), High p_{T} (V), Z+udcsg enr."],["vhbb_Zmm_8_13TeV2016","2-lepton (#mu), Low p_{T} (V), t#bar{t} enr."],["vhbb_Zmm_6_13TeV2016","2-lepton (#mu), Low p_{T} (V), Z+b#bar{b} enr."],["vhbb_Zmm_4_13TeV2016","2-lepton (#mu), Low p_{T} (V), Z+udcsg enr."]],
    "Znn": [["vhbb_Znn_7_13TeV2016","0-lepton, t#bar{t} enr."],["vhbb_Znn_5_13TeV2016","0-lepton, Z+b#bar{b} enr."],["vhbb_Znn_3_13TeV2016","0-lepton, Z+udcsg enr."]]
}



for MODE in ['prefit','postfit']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              os.system(('./scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal ' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr ' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CMVA_{min}" '\
                  ' --channel_label "%(LABEL)s"' % vars()))

