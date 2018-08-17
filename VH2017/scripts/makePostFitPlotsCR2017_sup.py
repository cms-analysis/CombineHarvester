import os,sys

CHN_DICT_SR = {
    "Wen": [["vhbb_Wen_6_13TeV2017","1-lepton (e), W+b#bar{b} enr.",0.,5.,"W+b#bar{b},t#bar{t},#lower[0.2]{W+LF},#lower[0.2]{W+b},#lower[0.2]{Top}"]],
    "Wmn": [["vhbb_Wmn_6_13TeV2017","1-lepton (#mu), W+b#bar{b} enr.",0.,5.,"W+b#bar{b},t#bar{t},#lower[0.2]{W+LF},#lower[0.2]{W+b},#lower[0.2]{Top}"]],
    "Zee": [["vhbb_Zee_5_13TeV2017","2-e, High p_{T,V}, Z+b#bar{b} enr.",0.14,1.,"DeepCSV_{min}"],["vhbb_Zee_6_13TeV2017","2-e, Low p_{T,V}, Z+b#bar{b} enr.",0.14,1.,"DeepCSV_{min}"]],
    "Zmm": [["vhbb_Zmm_5_13TeV2017","2-#mu, High p_{T,V}, Z+b#bar{b} enr.",0.14,1.,"DeepCSV_{min}"],["vhbb_Zmm_6_13TeV2017","2-#mu, Low p_{T,V}, Z+b#bar{b} enr.",0.14,1.,"DeepCSV_{min}"]],
    "Znn": [["vhbb_Znn_5_13TeV2017","0-lepton, Z+b#bar{b} enr.",0.,5.,"V+b#bar{b},t#bar{t},#lower[0.2]{V+LF},#lower[0.2]{V+b},#lower[0.2]{Top}"]]
}


FILENAME=sys.argv[1]

#for MODE in ['prefit','postfit']:
for MODE in ['postfit']:
    for CHN in ['Wmn','Wen','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              print CHN_DICT_SR[CHN][i]
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              XLOW = CHN_DICT_SR[CHN][i][2]
              XHIGH = CHN_DICT_SR[CHN][i][3]
              XLABEL = CHN_DICT_SR[CHN][i][4]
              os.system(('./scripts/postFitPlot.py' \
                  ' --file=%(FILENAME)s --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s --no_signal '\
                  ' --ratio_range 0.92,1.08 --empty_bin_error --channel=%(CHN)s --cr  --extralabel="Supplementary" '\
                  ' --outname %(OUTNAME)s --mode %(MODE)s  --x_title=%(XLABEL)s  --y_title="Entries" '\
                  ' --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range  --lumi="41.3 fb^{-1} (13 TeV)" '\
                  ' --channel_label "%(LABEL)s"' % vars()))

