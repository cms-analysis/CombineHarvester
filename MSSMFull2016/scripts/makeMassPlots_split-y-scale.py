import os

CHN_DICT = {
    "zmm": "Z#rightarrow#mu#mu CR",
    "ttbar": "t#bar{t} CR",
    "et": "e_{}#tau_{h}",
    "mt": "#mu_{}#tau_{h}",
    "em": "e#mu",
    "tt": "#tau_{h}#tau_{h}"
}

CAT_DICT_EMT = {
    "8": "No B-tag Tight-^{}m_{T}",
    "9": "B-tag Tight-^{}m_{T}",
    "10": "No B-tag Loose-^{}m_{T}",
    "11": "B-tag Loose-^{}m_{T}"
}

CAT_DICT_TT = {
    "8": "No B-tag",
    "9": "B-tag"
}

CAT_DICT_EM = {
    "8": "No B-tag Low-^{}D_{#zeta}",
    "9": "B-tag Low-^{}D_{#zeta}",
    "10": "No B-tag Medium-^{}D_{#zeta}",
    "11": "B-tag Medium-^{}D_{#zeta}",
    "12": "No B-tag High-^{}D_{#zeta}",
    "13": "B-tag High-^{}D_{#zeta}"
}


RANGE_DICT = {
    "em" : 1E-5 ,
    "et" : 5E-7 ,
    "mt" : 1E-7 , 
    "tt" : 1E-7 ,
    "zmm" : 1E-3 
}

PAD_DICT = {
    "em" : 0.42 ,
    "et" : 0.45 ,
    "mt" : 0.45 , 
    "tt" : 0.5 
}

CAT_SPLIT_DICT_EMT = {
    "mt" : {
        "8": 200,
        "9": 1,
        "10": 200,
        "11": 1
    },
    "et" : {
        "8": 50,
        "9": 1,
        "10": 50,
        "11": 1
    }
}

CAT_SPLIT_DICT_EM = {
    "8": 200,
    "9": 1,
    "10": 100,
    "11": 1,
    "12": 20,
    "13": 1
}

CAT_SPLIT_DICT_TT = {
    "8": 100,
    "9": 1
}

CAT_RATIO_RANGE_DICT_EMT = {
    "mt" : {
        "8": "0.4,1.6",
        "9": "0.4,1.6",
        "10": "0.4,1.6",
        "11": "0.4,1.6"
    },
    "et" : {
        "8": "0.4,1.6",
        "9": "0.4,1.6",
        "10": "0.4,1.6",
        "11": "0.4,1.6"
    }
}

CAT_RATIO_RANGE_DICT_TT = {
    "8": "0.4,1.6",
    "9": "0.4,1.6"
}

# post-fit plots with split y scale

for MODE in ['postfit']:
    for CHN in ['mt','et']:
        for CAT in CAT_DICT_EMT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EMT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EMT[CHN][CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_EMT[CHN][CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s --split_y_scale %(SPLIT)s --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E15' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['postfit']:
    for CHN in ['em']:
        for CAT in CAT_DICT_EM:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EM[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EM[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=0.4,1.6 --split_y_scale %(SPLIT)s --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['postfit']:
    for CHN in ['tt']:
        for CAT in CAT_DICT_TT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_TT[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_TT[CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s --split_y_scale %(SPLIT)s --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))


# pre-fit plots with split y scale
for MODE in ['prefit']:
    for CHN in ['mt','et']:
        for CAT in CAT_DICT_EMT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EMT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EMT[CHN][CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_EMT[CHN][CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s --split_y_scale %(SPLIT)s' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E15' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['prefit']:
    for CHN in ['em']:
        for CAT in CAT_DICT_EM:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EM[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EM[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=0.4,1.6 --split_y_scale %(SPLIT)s' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['prefit']:
    for CHN in ['tt']:
        for CAT in CAT_DICT_TT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_TT[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_TT[CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s --split_y_scale %(SPLIT)s' \
                  ' --outname htt_%(CHN)s_%(CAT)s_split_y_scale --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['prefit']:
    for CHN in ['zmm']:
        for CAT in CAT_DICT_TT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT["tt"]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --no_signal' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_y' \
                  ' --ratio_range=0.92,1.08 --channel zmm --x_title "counting experiment" --y_title "Events" ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s"' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

# standard plots
for MODE in ['postfit']:
    for CHN in ['mt','et']:
        for CAT in CAT_DICT_EMT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EMT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EMT[CHN][CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_EMT[CHN][CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s  --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E15' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['postfit']:
    for CHN in ['em']:
        for CAT in CAT_DICT_EM:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_EM[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_EM[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=0.4,1.6 --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

for MODE in ['postfit']:
    for CHN in ['tt']:
        for CAT in CAT_DICT_TT:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT_TT[CAT])
            SPLIT = "%s" % CAT_SPLIT_DICT_TT[CAT]
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            RRANGE = "%s" % CAT_RATIO_RANGE_DICT_TT[CAT]
            os.system(('python scripts/postFitPlotJetFakes.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --model_dep --mA 700 --tanb 20' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --log_x --log_y' \
                  ' --ratio_range=%(RRANGE)s --sb_vs_b_ratio' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --custom_y_range --y_axis_min "%(YMIN)s" --y_axis_max 1E20' \
                  ' --channel_label "%(LABEL)s" --empty_bin_error' % vars()))

