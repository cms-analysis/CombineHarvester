import os

CHN_DICT_SR = {
    "Wen": [["WenHighPt","1-lepton (e)"]],
    "Wmn": [["WmnHighPt","1-lepton (#mu)"]],
    "Zee": [["ZeeHighPt_13TeV","2-lepton (e), High p_{T} (V)"],["ZeeLowPt_13TeV","2-lepton (e), Low p_{T} (V)"]],
    "Zmm": [["ZuuHighPt_13TeV","2-lepton (#mu), High p_{T} (V)"],["ZuuLowPt_13TeV","2-lepton (#mu), Low p_{T} (V)"]],
    "Znn": [["Znn_13TeV_Signal","0-lepton"]]
}



for MODE in ['prefit','postfit']:
    for CHN in ['Wen','Wmn','Zee','Zmm','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes_vhbb_2011.root --ratio --extra_pad=0.53 --file_dir=%(OUTNAME)s ' \
                  ' --ratio_range 0.4,1.6 --empty_bin_error --channel=%(CHN)s ' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --log_y --custom_y_range --y_axis_min "1E-2" '\
                  ' --channel_label "%(LABEL)s"' % vars()))

#for MODE in ['prefit', 'postfit']:
#    for CHN in ['et', 'mt', 'em', 'tt']:
#        for CAT in ['8', '9']:
#            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
#            YMIN = "%s" % RANGE_DICT[CHN]
#            PAD = "%s" % PAD_DICT[CHN]
#            os.system(('python scripts/postFitPlot.py' \
#                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --mA=1000 --tanb=50 --model_dep' \
#                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
#                  ' --ratio_range 0.4,1.6 --empty_bin_error' \
#                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min "%(YMIN)s" ' \
#                  ' --channel_label "%(LABEL)s"' % vars()))

#for MODE in ['prefit', 'postfit']:
#    for CHN in ['et', 'mt', 'em', 'tt']:
#        for CAT in ['8', '9']:
#            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
#            os.system(('python scripts/postFitPlot.py' \
#                  ' --file=shapes.root --ratio --extra_pad=0.6 --mA=1000 --tanb=50 --model_dep --no_signal' \
#                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
#                  ' --ratio_range 0.4,1.6 ' \
#                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
#                  ' --channel_label "%(LABEL)s"' % vars()))
