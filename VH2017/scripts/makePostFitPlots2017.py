import os,sys

CHN_DICT_SR = {
    "Wen": [["vhbb_Wen_1_13TeV2017","1-lepton (e)","DNN output"]],
    "Wmn": [["vhbb_Wmn_1_13TeV2017","1-lepton (#mu)","DNN output"]],
    "Zee": [["vhbb_Zee_1_13TeV2017","2-e, High p_{T,V}","DNN output"],["vhbb_Zee_2_13TeV2017","2-e, Low p_{T,V}","DNN output"]],
    "Zmm": [["vhbb_Zmm_1_13TeV2017","2-#mu, High p_{T,V}","DNN output"],["vhbb_Zmm_2_13TeV2017","2-#mu, Low p_{T,V}","DNN output"]],
    "Znn": [["vhbb_Znn_1_13TeV2017","0-lepton","DNN output"]]
}

CHN_MAX_RATIO = {
    "Wen": [5.0],
    "Wmn": [2.5],
    "Zee": [2.0, 1.5],
    "Zmm": [2.0, 2.0],
    "Znn": [1.5],
}

FILENAME=sys.argv[1]

#for MODE in ['prefit','postfit']:
for MODE in ['postfit']:
    for CHN in ['Zee','Zmm','Znn','Wmn','Wen']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              XAXIS = "%s" % CHN_DICT_SR[CHN][i][2]
              MAXRATIO = "%s" % CHN_MAX_RATIO[CHN][i]
              if (XAXIS.find("DNN")!=-1):
                  os.system(('./scripts/postFitPlot.py' \
                      ' --file=%(FILENAME)s --ratio --ratio_justb --extra_pad=0.53 --file_dir=%(OUTNAME)s --extralabel="Supplementary" ' \
                      ' --ratio_range 0.4,%(MAXRATIO)s --empty_bin_error --channel=%(CHN)s  --y_title="Entries" --lumi="41.3 fb^{-1} (13 TeV)" ' \
                      ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "1E-2" '\
                      ' --channel_label "%(LABEL)s" --x_title "%(XAXIS)s" --x_blind_min 0.5 ' % vars()))
              else:
                  os.system(('./scripts/postFitPlot.py' \
                      ' --file=%(FILENAME)s --ratio --ratio_justb --extra_pad=0.53 --file_dir=%(OUTNAME)s  --extralabel="Supplementary" ' \
                      ' --ratio_range 0.4,2.0 --empty_bin_error --channel=%(CHN)s  --y_title="Entries" --lumi="41.3 fb^{-1} (13 TeV)" ' \
                      ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "1E-2" '\
                      ' --channel_label "%(LABEL)s" --x_title "%(XAXIS)s" ' % vars()))

