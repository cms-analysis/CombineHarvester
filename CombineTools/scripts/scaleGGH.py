#!/usr/bin/env python

import combineharvester as ch
import ROOT as R
import glob

# OLD inclusive distribution
# SCALES = {
#   ('mt', 1) : 1.029022621, #0jet-low
#   ('mt', 2) : 1.037426484, #0jet-high
#   ('mt', 3) : 1.005208333, #1jet-low
#   ('mt', 4) : 1.014984227, #1jet-high (low boost)
#   ('mt', 5) : 0.873225152, #1jet-high (med boost)
#   ('mt', 6) : 0.948453608, #vbf loose
#   ('mt', 7) : 0.896551724, #vbf tight
#   ('et', 1) : 1.029022621, #0jet-low
#   ('et', 2) : 1.037426484, #0jet-high
#   ('et', 3) : 1.005208333, #1jet-low
#   ('et', 4) : 1.014984227, #1jet-high (low boost)
#   ('et', 5) : 0.873225152, #1jet-high (med boost)
#   ('et', 6) : 0.948453608, #vbf loose
#   ('et', 7) : 0.896551724, #vbf tight
#   ('em', 0) : 1.029022621, #0jet-low
#   ('em', 1) : 1.037426484, #0jet-high
#   ('em', 2) : 1.005208333, #1jet-low
#   ('em', 3) : 0.975298126, #1jet-high
#   ('em', 4) : 0.948453608, #vbf loose
#   ('em', 5) : 0.896551724, #vbf tight
#   ('ee', 0) : 1.029022621, #0jet-low
#   ('ee', 1) : 1.037426484, #0jet-high
#   ('ee', 2) : 1.005208333, #1jet-low
#   ('ee', 3) : 0.975298126, #1jet-high
#   ('ee', 4) : 0.948453608, #vbf
#   ('mm', 0) : 1.029022621, #0jet-low
#   ('mm', 1) : 1.037426484, #0jet-high
#   ('mm', 2) : 1.005208333, #1jet-low
#   ('mm', 3) : 0.975298126, #1jet-high
#   ('mm', 4) : 0.948453608, #vbf
#   ('tt', 0) : 0.873225152, #1jet-high (med boost)
#   ('tt', 1) : 0.873225152, #1jet-high (high boost)
#   ('tt', 2) : 0.948453608 #vbf
# }

# 2D reweighting
SCALES_7TEV = {
  ('mt', 1) : 1.027, #0jet-low
  ('mt', 2) : 1.044, #0jet-high
  ('mt', 3) : 0.924, #1jet-low
  ('mt', 4) : 0.925, #1jet-high (low boost)
  ('mt', 5) : 0.782, #1jet-high (med boost)
  ('mt', 6) : 0.962, #vbf
  ('et', 1) : 1.027, #0jet-low
  ('et', 2) : 1.044, #0jet-high
  ('et', 3) : 0.924, #1jet-low
  ('et', 4) : 0.925, #1jet-high (low boost)
  ('et', 5) : 0.782, #1jet-high (med boost)
  ('et', 6) : 0.962, #vbf
  ('em', 0) : 1.027, #0jet-low
  ('em', 1) : 1.044, #0jet-high
  ('em', 2) : 0.924, #1jet-low
  ('em', 3) : 0.889, #1jet-high
  ('em', 4) : 0.962, #vbf
  ('ee', 0) : 1.027, #0jet-low
  ('ee', 1) : 1.044, #0jet-high
  ('ee', 2) : 0.924, #1jet-low
  ('ee', 3) : 0.889, #1jet-high
  ('ee', 4) : 0.962, #vbf
  ('mm', 0) : 1.027, #0jet-low
  ('mm', 1) : 1.044, #0jet-high
  ('mm', 2) : 0.924, #1jet-low
  ('mm', 3) : 0.889, #1jet-high
  ('mm', 4) : 0.962, #vbf
}

SCALES_8TEV = {
  ('mt', 1) : 1.051, #0jet-low
  ('mt', 2) : 1.061, #0jet-high
  ('mt', 3) : 0.955, #1jet-low
  ('mt', 4) : 0.961, #1jet-high (low boost)
  ('mt', 5) : 0.800, #1jet-high (med boost)
  ('mt', 6) : 1.103, #vbf loose
  ('mt', 7) : 1.069, #vbf tight
  ('et', 1) : 1.051, #0jet-low
  ('et', 2) : 1.061, #0jet-high
  ('et', 3) : 0.955, #1jet-low
  ('et', 4) : 0.961, #1jet-high (low boost)
  ('et', 5) : 0.800, #1jet-high (med boost)
  ('et', 6) : 1.103, #vbf loose
  ('et', 7) : 1.069, #vbf tight
  ('em', 0) : 1.051, #0jet-low
  ('em', 1) : 1.061, #0jet-high
  ('em', 2) : 0.955, #1jet-low
  ('em', 3) : 0.915, #1jet-high
  ('em', 4) : 1.103, #vbf loose
  ('em', 5) : 1.069, #vbf tight
  ('ee', 0) : 1.051, #0jet-low
  ('ee', 1) : 1.061, #0jet-high
  ('ee', 2) : 0.955, #1jet-low
  ('ee', 3) : 0.915, #1jet-high
  ('ee', 4) : 1.087, #vbf
  ('mm', 0) : 1.051, #0jet-low
  ('mm', 1) : 1.061, #0jet-high
  ('mm', 2) : 0.955, #1jet-low
  ('mm', 3) : 0.915, #1jet-high
  ('mm', 4) : 1.087, #vbf
  ('tt', 0) : 0.800, #1jet-high (med boost)
  ('tt', 1) : 0.798, #1jet-high (high boost)
  ('tt', 2) : 1.087 #vbf
}

def DoScales(cmb, scales):
  for key, val in scales.iteritems():
    print 'Scaling ' + str(key) + ' by ' + str(val)
    cmb.cp().process(["ggH"]).channel([key[0]]).bin_id([key[1]]).ForEachProc(lambda x : x.set_rate(x.rate() * val))
    cmb.cp().process(["ggH"]).channel([key[0]]).bin_id([key[1]]).PrintProcs()

cmb = ch.CombineHarvester()

for card in glob.glob('output/htt-YR3/*/htt*.txt'):
  cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

for card in glob.glob('output/htt-YR3/*/vhtt*.txt'):
  cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$BINID_$ERA.txt")

cmb_for_scaling = cmb.cp().analysis(['vhtt'], False)

DoScales(cmb_for_scaling.cp().era(['7TeV']), SCALES_7TEV)
DoScales(cmb_for_scaling.cp().era(['8TeV']), SCALES_8TEV)

writer_htt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           '$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root')
writer_htt.SetVerbosity(1)
writer_htt.WriteCards('output/htt-YR3-hpt', cmb.cp().analysis(['htt']))

writer_vhtt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$BINID_$ERA.txt',
                            '$TAG/common/$ANALYSIS.input_$ERA.root')
writer_vhtt.SetVerbosity(1)
writer_vhtt.WriteCards('output/htt-YR3-hpt', cmb.cp().analysis(['vhtt']))
