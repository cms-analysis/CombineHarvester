import os

CHN_DICT_SR = {
    "Wen": [["vhbb_Wen_1_13TeV2016","1-lepton (e)"]],
    "Wmn": [["vhbb_Wmn_1_13TeV2016","1-lepton (#mu)"]],
    "Zee": [["vhbb_Zee_1_13TeV2016","2-lepton (e), High p_{T} (V)"],["vhbb_Zee_2_13TeV2016","2-lepton (e), Low p_{T} (V)"]],
    "Zmm": [["vhbb_Zmm_1_13TeV2016","2-lepton (#mu), High p_{T} (V)"],["vhbb_Zmm_2_13TeV2016","2-lepton (#mu), Low p_{T} (V)"]],
    "Znn": [["vhbb_Znn_1_13TeV2016","0-lepton"]]
}



for MODE in ['prefit','postfit']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              os.system(('./scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s ' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s --blind' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "1E-2" '\
                  ' --channel_label "%(LABEL)s"' % vars()))

