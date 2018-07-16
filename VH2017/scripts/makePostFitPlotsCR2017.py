import os

CHN_DICT_SR = {
    "Wen": [["vhbb_Wen_7_13TeV2017","1-lepton (e),t#bar{t} enriched",0.,1.],["vhbb_Wen_6_13TeV2017","1-lepton (e), W+b#bar{b} enr.",0.,5.],["vhbb_Wen_3_13TeV2017","1-lepton (e),W+udcsg enr.",0.,0.5]],
    "Wmn": [["vhbb_Wmn_7_13TeV2017","1-lepton (#mu),t#bar{t} enriched",0.,1.],["vhbb_Wmn_6_13TeV2017","1-lepton (#mu), W+b#bar{b} enr.",0.,5.],["vhbb_Wmn_3_13TeV2017","1-lepton (#mu),W+udcsg enr.",0.,0.5]],
    #"Wen": [["vhbb_Wen_7_13TeV2017","1-lepton (e),t#bar{t} enriched",0.,1.],["vhbb_Wen_5_13TeV2017","1-lepton (e), high Mjj W+b#bar{b} enr.",0.,1.],["vhbb_Wen_6_13TeV2017","1-lepton (e), low Mjj, W+b#bar{b} enr.",0.,1.],["vhbb_Wen_3_13TeV2017","1-lepton (e),W+udcsg enr.",0.,0.5]],
    #"Wmn": [["vhbb_Wmn_7_13TeV2017","1-lepton (#mu),t#bar{t} enriched",0.,1.],["vhbb_Wmn_5_13TeV2017","1-lepton (#mu), high Mjj W+b#bar{b} enr.",0.,1.],["vhbb_Wmn_6_13TeV2017","1-lepton (#mu), low Mjj, W+b#bar{b} enr.",0.,1.],["vhbb_Wmn_3_13TeV2017","1-lepton (#mu),W+udcsg enr.",0.,0.5]],
    "Zee": [["vhbb_Zee_7_13TeV2017","2-lepton (e), High p_{T} (V), t#bar{t} enr.",0.14,1.],["vhbb_Zee_5_13TeV2017","2-lepton (e), High p_{T} (V),Z+b#bar{b} enr.",0.14,1.],["vhbb_Zee_3_13TeV2017","2-lepton (e), High p_{T} (V), Z+udcsg enr.",0.,0.2],["vhbb_Zee_8_13TeV2017","2-lepton (e), Low p_{T} (V), t#bar{t} enr.",0.14,1.],["vhbb_Zee_6_13TeV2017","2-lepton (e), Low p_{T} (V), Z+b#bar{b} enr.",0.14,1.],["vhbb_Zee_4_13TeV2017","2-lepton (e), Low p_{T} (V), Z+udcsg enr.",0,0.2]],
    "Zmm": [["vhbb_Zmm_7_13TeV2017","2-lepton (#mu), High p_{T} (V), t#bar{t} enr.",0.14,1.],["vhbb_Zmm_5_13TeV2017","2-lepton (#mu), High p_{T} (V),Z+b#bar{b} enr.",0.14,1.],["vhbb_Zmm_3_13TeV2017","2-lepton (#mu), High p_{T} (V), Z+udcsg enr.",0,0.2],["vhbb_Zmm_8_13TeV2017","2-lepton (#mu), Low p_{T} (V), t#bar{t} enr.",0.14,1.],["vhbb_Zmm_6_13TeV2017","2-lepton (#mu), Low p_{T} (V), Z+b#bar{b} enr.",0.14,1.],["vhbb_Zmm_4_13TeV2017","2-lepton (#mu), Low p_{T} (V), Z+udcsg enr.",0,0.2]],
    #"Znn": [["vhbb_Znn_5_13TeV","0-lepton, Z+b#bar{b} enr.",0.,5.]]
    "Znn": [["vhbb_Znn_7_13TeV2017","0-lepton, t#bar{t} enr.",0.14,1.],["vhbb_Znn_5_13TeV2017","0-lepton, Z+b#bar{b} enr.",0.,5.],["vhbb_Znn_3_13TeV2017","0-lepton, Z+udcsg enr.",0.14,0.52]]
    #"Znn": [["vhbb_Znn_7_13TeV2017","0-lepton, t#bar{t} enr.",0.14,1.],["vhbb_Znn_5_13TeV2017","0-lepton, Z+b#bar{b} enr.",0.14,1.],["vhbb_Znn_3_13TeV2017","0-lepton, Z+udcsg enr.",0.14,0.52]]
}



for MODE in ['prefit','postfit']:
#for MODE in ['postfit']:
    for CHN in ['Wmn','Wen','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              print CHN_DICT_SR[CHN][i]
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              XLOW = CHN_DICT_SR[CHN][i][2]
              XHIGH = CHN_DICT_SR[CHN][i][3]
              os.system(('./scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal ' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --cr ' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="DeepCSV_{min}" '\
                  ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range '\
                  ' --channel_label "%(LABEL)s"' % vars()))

