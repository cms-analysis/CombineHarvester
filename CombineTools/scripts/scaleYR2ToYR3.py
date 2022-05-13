#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import ROOT as R
import glob
import six

SCALES_XSEC_7TEV = {
  "^ggH(|_hww|_htt)$" : 15.13/15.31,
  "^qqH(|_hww|_htt)$" : 1.222/1.211,
  "^WH(|_hww|_htt)$" : 0.5785/0.5729,
  "^ZH(|_hww|_htt)$" : 0.3351/0.3158
}

SCALES_XSEC_8TEV = {
  "^ggH(|_hww|_htt)$" : 19.27/19.610579,
  "^qqH(|_hww|_htt)$" : 1.578/1.5511699,
  "^WH(|_hww|_htt)$" : 0.7046/0.73382761,
  "^ZH(|_hww|_htt)$" : 0.4153/0.40450822
}

SCALES_BR = {
  "^(ggH|qqH|WH|ZH)(|_htt)$" : 6.32E-02/6.37E-02,
  "^(ggH|qqH|WH|ZH)_hww$" :    2.15E-01/2.16E-01
}

def DoScales(cmb, scales):
    for key, val in six.iteritems(scales):
        print('Scaling ' + key + ' by ' + str(val))
        cmb.cp().process_rgx([key]).ForEachProc(lambda x : x.set_rate(x.rate() * val))
        cmb.cp().process_rgx([key]).PrintProcs()

cmb = ch.CombineHarvester()

for card in glob.glob('output/htt-YR2/125.1/htt*.txt'):
    cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

for card in glob.glob('output/htt-YR2/125.1/vhtt*.txt'):
    cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$BINID_$ERA.txt")

cmb_for_scaling = cmb.cp().analysis(['vhtt'], False)

DoScales(cmb_for_scaling.cp().era(['7TeV']), SCALES_XSEC_7TEV)
DoScales(cmb_for_scaling.cp().era(['8TeV']), SCALES_XSEC_8TEV)
DoScales(cmb_for_scaling, SCALES_BR)

writer_htt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           '$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root')
writer_htt.SetVerbosity(1)
writer_htt.WriteCards('output/htt-YR3', cmb.cp().analysis(['htt']))

writer_vhtt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$BINID_$ERA.txt',
                            '$TAG/common/$ANALYSIS.input_$ERA.root')
writer_vhtt.SetVerbosity(1)
writer_vhtt.WriteCards('output/htt-YR3', cmb.cp().analysis(['vhtt']))
