import os

CHN_DICT = {
    "et": "e_{}#tau_{h}",
    "mt": "#mu_{}#tau_{h}",
    "em": "e#mu",
    "tt": "#tau_{h}#tau_{h}"
}

CAT_DICT_EMT = {
    "8": "no b-tag tight",
    "9": "b-tag tight",
    "10": "no b-tag loose mT",
    "11": "b-tag loose mT"
}

CAT_DICT_TT = {
    "8": "no b-tag",
    "9": "b-tag"
}

CAT_DICT_EM = {
    "8": "no b-tag low D_{#zeta}",
    "9": "b-tag low D_{#zeta}",
    "10": "no b-tag medium D_{#zeta}",
    "11": "b-tag medium D_{#zeta}",
    "12": "no b-tag high D_{#zeta}",
    "13": "b-tag high D_{#zeta}"
}



RANGE_DICT = {
    "em" : 1E-5 ,
    "et" : 5E-7 ,
    "mt" : 1E-7 , 
    "tt" : 1E-7 
}

PAD_DICT = {
    "em" : 0.42 ,
    "et" : 0.45 ,
    "mt" : 0.45 , 
    "tt" : 0.5 
}


for MODE in ['prefit']:
    for CHN in ['mt','et']:
        for CAT in ['8', '9', '10', '11']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EMT[CAT])
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad="%(PAD)s" --mA 1000 --tanb 50 --model_dep ' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min "%(YMIN)s" ' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit']:
    for CHN in ['mt','et']:
        for CAT in ['8', '9', '10', '11']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EMT[CAT])
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad=0.6 --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
                  ' --channel_label "%(LABEL)s"' % vars()))



for MODE in ['prefit']:
    for CHN in ['em']:
        for CAT in ['8', '9', '10', '11','12','13']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EM[CAT])
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad="%(PAD)s" --mA 1000 --tanb 50 --model_dep ' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min "%(YMIN)s" ' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit']:
    for CHN in ['em']:
        for CAT in ['8', '9', '10', '11','12','13']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EM[CAT])
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad=0.6 --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit']:
    for CHN in ['tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad="%(PAD)s" --mA 1000 --tanb 50 --model_dep ' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min "%(YMIN)s" ' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit']:
    for CHN in ['tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes_test.root --ratio --extra_pad=0.6 --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
                  ' --ratio_range 0.4,1.6 --manual_blind --x_blind_min=100 --x_blind_max=4000 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
                  ' --channel_label "%(LABEL)s"' % vars()))

