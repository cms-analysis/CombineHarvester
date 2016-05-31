import os

CHN_DICT = {
    "et": "e_{}#tau_{h}",
    "mt": "#mu_{}#tau_{h}",
    "em": "e#mu",
    "tt": "#tau_{h}#tau_{h}"
}

CAT_DICT = {
    "8": "no b-tag",
    "9": "b-tag"
}

RANGE_DICT = {
    "em" : 1E-3 ,
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


for MODE in ['prefit', 'postfit']:
    for CHN in ['et', 'mt', 'em', 'tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
            YMIN = "%s" % RANGE_DICT[CHN]
            PAD = "%s" % PAD_DICT[CHN]
            os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad="%(PAD)s" --r_ggH=0.1 --r_bbH=0.1 --mPhi=700' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
                  ' --ratio_range 0.4,1.6 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min "%(YMIN)s" ' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit', 'postfit']:
    for CHN in ['et', 'mt', 'em', 'tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
            os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.6 --r_ggH=0.1 --r_bbH=0.1 --mPhi=700' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
                  ' --ratio_range 0.4,1.6 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
                  ' --channel_label "%(LABEL)s"' % vars()))
