import os

CHN_DICT_SR = {
    "Wen": [["ttWen","1-lepton (e),t#bar{t} enriched"],["whfWenHigh","1-lepton (e), high Mjj W+b#bar{b} enr."],["whfWenLow","1-lepton (e), low Mjj, W+b#bar{b} enr."],["wlfWen","1-lepton (e),W+udcsg enr."]],
    "Wmn": [["ttWmn","1-lepton (#mu),t#bar{t} enriched"],["whfWmnHigh","1-lepton (#mu), high Mjj W+b#bar{b} enr."],["whfWmnLow","1-lepton (#mu), low Mjj, W+b#bar{b} enr."],["wlfWmn","1-lepton (#mu),W+udcsg enr."]],
    "Zee": [["ttbar_high_Zee","2-lepton (e), High p_{T} (V), t#bar{t} enr."],["Zhf_high_Zee","2-lepton (e), High p_{T} (V),Z+b#bar{b} enr."],["Zlf_high_Zee","2-lepton (e), High p_{T} (V), Z+udcsg enr."],["ttbar_low_Zee","2-lepton (e), Low p_{T} (V), t#bar{t} enr."],["Zhf_low_Zee","2-lepton (e), Low p_{T} (V), Z+b#bar{b} enr."],["Zlf_low_Zee","2-lepton (e), Low p_{T} (V), Z+udcsg enr."]],
    "Zmm": [["ttbar_high_Zuu","2-lepton (#mu), High p_{T} (V), t#bar{t} enr."],["Zhf_high_Zuu","2-lepton (#mu), High p_{T} (V),Z+b#bar{b} enr."],["Zlf_high_Zuu","2-lepton (#mu), High p_{T} (V), Z+udcsg enr."],["ttbar_low_Zuu","2-lepton (#mu), Low p_{T} (V), t#bar{t} enr."],["Zhf_low_Zuu","2-lepton (#mu), Low p_{T} (V), Z+b#bar{b} enr."],["Zlf_low_Zuu","2-lepton (#mu), Low p_{T} (V), Z+udcsg enr."]],
    "Znn": [["Znn_13TeV_TT","0-lepton, t#bar{t} enr."],["Znn_13TeV_Zbb","0-lepton, Z+b#bar{b} enr."],["Znn_13TeV_Zlight","0-lepton, Z+udcsg enr."]]
}



for MODE in ['prefit','postfit']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal ' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s ' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_title="CMVA_{min}" '\
                  ' --channel_label "%(LABEL)s"' % vars()))

