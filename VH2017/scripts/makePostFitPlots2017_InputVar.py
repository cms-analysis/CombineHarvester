import os

CHN_DICT_SR = {
    #"Znn": [["vhbb_Znn_1_13TeV2017","0-lepton","Mjj"],["vhbb_Znn_2_13TeV2017","0-lepton","Max DeepCSV"],["vhbb_Znn_3_13TeV2017","0-lepton","Min DeepCSV"],["vhbb_Znn_4_13TeV2017","0-lepton","VPT"],["vhbb_Znn_5_13TeV2017","0-leptoni SR","DNN"]],
    "Znn": [["vhbb_Znn_1_13TeV2017","0-lepton SR","Mjj"],["vhbb_Znn_2_13TeV2017","0-lepton SR","Max DeepCSV"],["vhbb_Znn_3_13TeV2017","0-lepton SR","Min DeepCSV"],["vhbb_Znn_4_13TeV2017 SR","0-lepton","VPT"],["vhbb_Znn_6_13TeV2017","0-lepton, TT CR","ZnnTTBtag2"],["vhbb_Znn_7_13TeV2017","0-lepton, HF CR","ZnnZbbBtag2"],["vhbb_Znn_8_13TeV2017","0-lepton, LF CR","ZnnZLFBtag2"],["vhbb_Znn_9_13TeV2017","0-lepton, TT CR","ZnnTTBtag1"],["vhbb_Znn_10_13TeV2017","0-lepton, HF CR","ZnnZbbBtag1"],["vhbb_Znn_11_13TeV2017","0-lepton, LF CR","ZnnZLFBtag1"]],
    "Zee": [["vhbb_Zee_5_13TeV2017","2e,High VPT","Min DeepCSV"],["vhbb_Zee_7_13TeV2017","2e,High VPT","VPT"],["vhbb_Zee_9_13TeV2017","2e,High VPT","DNN"],["vhbb_Zee_10_13TeV2017","2e,Low VPT","DNN"]],
    "Zmm": [["vhbb_Zmm_5_13TeV2017","2m,High VPT","Min DeepCSV"],["vhbb_Zmm_6_13TeV2017","2m,Low VPT","Min DeepCSV"],["vhbb_Zmm_7_13TeV2017","2m,High VPT","VPT"],["vhbb_Zmm_8_13TeV2017","2m,Low VPT","VPT"],["vhbb_Zmm_9_13TeV2017","2m,High VPT","DNN"]],
    #"Wen": [["vhbb_Wen_1_13TeV2017","1e","Mjj"],["vhbb_Wen_3_13TeV2017","1e","Min DeepCSV"],["vhbb_Wen_5_13TeV2017","1e","DNN"]],
    #"Wmn": [["vhbb_Wmn_1_13TeV2017","1m","Mjj"],["vhbb_Wmn_3_13TeV2017","1m","Min DeepCSV"],["vhbb_Wmn_5_13TeV2017","1m","DNN"]]
    "Wen": [["vhbb_Wen_1_13TeV2017","1e SR","Mjj"],["vhbb_Wen_2_13TeV2017","1e SR","Max DeepCSV"],["vhbb_Wen_3_13TeV2017","1e SR","Min DeepCSV"],["vhbb_Wen_10_13TeV2017","1m TT CR","ttWenBtag1"],["vhbb_Wen_11_13TeV2017","1m HF low mjj CR","whfWenLowBtag1"],["vhbb_Wen_12_13TeV2017","1m HF high mjj CR","whfWenHighBtag1"],["vhbb_Wen_13_13TeV2017","1m LF CR","wlfWenBtag1"],["vhbb_Wen_14_13TeV2017","1m TT CR","ttWenBtag2"],["vhbb_Wen_15_13TeV2017","1m HF low mjj CR","whfWenLowBtag2"],["vhbb_Wen_16_13TeV2017","1m HF high mjj CR","whfWenHighBtag2"],["vhbb_Wen_17_13TeV2017","1m LF CR","wlfWenBtag2"],["vhbb_Wen_18_13TeV2017","1m TT CR","ttWenMjj"],["vhbb_Wen_19_13TeV2017","1m HF low mjj CR","whfWenLowMjj"],["vhbb_Wen_20_13TeV2017","1m HF high mjj CR","whfWenHighMjj"],["vhbb_Wen_21_13TeV2017","1m LF CR","wlfWenMjj"],["vhbb_Wen_22_13TeV2017","1m TT CR","ttWenVPT"],["vhbb_Wen_23_13TeV2017","1m HF Low mjj CR","whfWenLowVPT"],["vhbb_Wen_24_13TeV2017","1m HF High mjj CR","whfWenHighVPT"],["vhbb_Wen_25_13TeV2017","1m LF CR","wlfWenVPT"]],
    "Wmn": [["vhbb_Wmn_1_13TeV2017","1m SR","Mjj"],["vhbb_Wmn_2_13TeV2017","1m SR","Max DeepCSV"],["vhbb_Wmn_3_13TeV2017","1m SR","Min DeepCSV"],["vhbb_Wmn_10_13TeV2017","1m TT CR","ttWmnBtag1"],["vhbb_Wmn_11_13TeV2017","1m HF low mjj CR","whfWmnLowBtag1"],["vhbb_Wmn_12_13TeV2017","1m HF high mjj CR","whfWmnHighBtag1"],["vhbb_Wmn_13_13TeV2017","1m LF CR","wlfWmnBtag1"],["vhbb_Wmn_14_13TeV2017","1m TT CR","ttWmnBtag2"],["vhbb_Wmn_15_13TeV2017","1m HF low mjj CR","whfWmnLowBtag2"],["vhbb_Wmn_16_13TeV2017","1m HF high mjj CR","whfWmnHighBtag2"],["vhbb_Wmn_17_13TeV2017","1m LF CR","wlfWmnBtag2"],["vhbb_Wmn_18_13TeV2017","1m TT CR","ttWmnMjj"],["vhbb_Wmn_19_13TeV2017","1m HF low mjj CR","whfWmnLowMjj"],["vhbb_Wmn_20_13TeV2017","1m HF high mjj CR","whfWmnHighMjj"],["vhbb_Wmn_21_13TeV2017","1m LF CR","wlfWmnMjj"],["vhbb_Wmn_22_13TeV2017","1m TT CR","ttWmnVPT"],["vhbb_Wmn_23_13TeV2017","1m HF Low mjj CR","whfWmnLowVPT"],["vhbb_Wmn_24_13TeV2017","1m HF High mjj CR","whfWmnHighVPT"],["vhbb_Wmn_25_13TeV2017","1m LF CR","wlfWmnVPT"]]
}


FILENAME="shapes_FullTT.root"

for MODE in ['prefit','postfit']:
    #for CHN in ['Zee','Zmm','Znn','Wmn','Wen']:
    #for CHN in ['Znn','Wen','Wmn']:
    for CHN in ['Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              XAXIS = "%s" % CHN_DICT_SR[CHN][i][2]
              if (XAXIS.find("DNN")!=-1):
                  os.system(('./scripts/postFitPlot.py' \
                      ' --file=%(FILENAME)s --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s ' \
                      ' --ratio_range 0.7,1.3 --empty_bin_error --channel=%(CHN)s ' \
                      ' --outname %(OUTNAME)s --mode %(MODE)s  --custom_y_range --y_axis_min "1E-2" '\
                      ' --channel_label "%(LABEL)s"   --x_title "%(XAXIS)s"  ' % vars()))
              else:
                  os.system(('./scripts/postFitPlot.py' \
                      ' --file=%(FILENAME)s  --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s ' \
                      ' --ratio_range 0.7,1.3 --empty_bin_error --channel=%(CHN)s ' \
                      ' --outname %(OUTNAME)s --mode %(MODE)s --custom_y_range --y_axis_min "1E-2" '\
                      ' --channel_label "%(LABEL)s"  --x_title "%(XAXIS)s" ' % vars()))

