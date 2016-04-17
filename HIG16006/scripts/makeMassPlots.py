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

for MODE in ['prefit', 'postfit']:
    for CHN in ['et', 'mt', 'em', 'tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
            os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.4 --r_ggH=0.1 --r_bbH=0.1 --mPhi=700' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0.1 --x_axis_max 1E4' \
                  ' --ratio_range 0.4,1.6 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s --log_x --log_y --custom_y_range --y_axis_min 1E-4' \
                  ' --channel_label "%(LABEL)s"' % vars()))

for MODE in ['prefit', 'postfit']:
    for CHN in ['et', 'mt', 'em', 'tt']:
        for CAT in ['8', '9']:
            LABEL = "%s %s" % (CHN_DICT[CHN], CAT_DICT[CAT])
            os.system(('python scripts/postFitPlot.py' \
                  ' --file=shapes.root --ratio --extra_pad=0.4 --r_ggH=0.1 --r_bbH=0.1 --mPhi=700' \
                  ' --file_dir="htt_%(CHN)s_%(CAT)s" --custom_x_range --x_axis_min=0 --x_axis_max 200' \
                  ' --ratio_range 0.4,1.6 ' \
                  ' --outname htt_%(CHN)s_%(CAT)s --mode %(MODE)s' \
                  ' --channel_label "%(LABEL)s"' % vars()))