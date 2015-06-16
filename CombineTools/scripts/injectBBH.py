#!/usr/bin/env python

import combineharvester as ch
import ROOT as R
import glob

SCALES = {
  ('mt', 1) : 1.12, #0jet-low
  ('mt', 2) : 1.13, #0jet-high
  ('mt', 3) : 0.39, #1jet-low
  ('mt', 4) : 0.39, #1jet-high (low boost)
  ('mt', 5) : 0.08, #1jet-high (med boost)
  ('mt', 6) : 0.23, #vbf loose
  ('mt', 7) : 0.23, #vbf tight
  ('et', 1) : 1.12, #0jet-low
  ('et', 2) : 1.13, #0jet-high
  ('et', 3) : 0.39, #1jet-low
  ('et', 4) : 0.39, #1jet-high (low boost)
  ('et', 5) : 0.08, #1jet-high (med boost)
  ('et', 6) : 0.23, #vbf loose
  ('et', 7) : 0.23, #vbf tight
  ('em', 0) : 1.12, #0jet-low
  ('em', 1) : 1.13, #0jet-high
  ('em', 2) : 0.39, #1jet-low
  ('em', 3) : 0.31, #1jet-high
  ('em', 4) : 0.23, #vbf loose
  ('em', 5) : 0.23, #vbf tight
  ('ee', 0) : 1.12, #0jet-low
  ('ee', 1) : 1.13, #0jet-high
  ('ee', 2) : 0.39, #1jet-low
  ('ee', 3) : 0.31, #1jet-high
  ('ee', 4) : 0.23, #vbf
  ('mm', 0) : 1.12, #0jet-low
  ('mm', 1) : 1.13, #0jet-high
  ('mm', 2) : 0.39, #1jet-low
  ('mm', 3) : 0.31, #1jet-high
  ('mm', 4) : 0.23, #vbf
  ('tt', 0) : 0.08, #1jet-high (med boost)
  ('tt', 1) : 0.08, #1jet-high (high boost)
  ('tt', 2) : 0.23 #vbf
}

def CustomizeProcs(p):
  p.set_process('bbH')
  if p.era() == '8TeV':
    p.set_rate(p.rate() * (0.2030/18.94) * SCALES[(p.channel(), p.bin_id())]) # ratio of YR3 bbH/ggH @ 125.1
  elif p.era() == '7TeV':
    p.set_rate(p.rate() * (0.1555/15.11) * SCALES[(p.channel(), p.bin_id())]) # ratio of YR3 bbH/ggH @ 125.1
  else:
    print "Don't know how to scale for " + p.era()

def CustomizeSysts(p):
  p.set_process('bbH')

cmb = ch.CombineHarvester()

for card in glob.glob('output/htt-YR3-hpt/*/htt*.txt'):
  cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

for card in glob.glob('output/htt-YR3-hpt/*/vhtt*.txt'):
  cmb.QuickParseDatacard(card, "$MASS/$ANALYSIS_$BINID_$ERA.txt")

ch.CloneProcs(cmb.cp().process(['ggH']), cmb, lambda p : CustomizeProcs(p))
ch.CloneSysts(cmb.cp().process(['ggH']), cmb, lambda p : CustomizeSysts(p))

# Now we drop QCDscale and pdf:
sys_init = set(cmb.cp().process(['bbH']).syst_name_set())
cmb.FilterSysts(lambda sys : 
    sys.process() == 'bbH' and 
    (
      sys.name().startswith('QCDscale') or 
      sys.name().startswith('pdf')
    )
  )
sys_final = set(cmb.cp().process(['bbH']).syst_name_set())
print sys_init - sys_final

# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt8TeV#bbH_Process
# +7.2  -7.8  +7.5  -6.9 (ggH 8TeV: scale, pdf)
# +10.3 -14.8 +6.2  -6.2 (bbH 8TeV, scale, pdf)
# +7.1  -7.8  +7.6  -7.1 (ggH 7TeV, scale, pdf)
# +10.4 -14.6 +6.1  -6.1 (bbH 7TeV, scale, pdf)

## Add new YR3 inclusive-only systematics
cmb.cp().process(['bbH']).AddSyst(
  cmb, 'QCDscale_bbH', 'lnN', ch.SystMap('era')
    (['7TeV'], (0.854, 1.104))
    (['8TeV'], (0.852, 1.103)))

cmb.cp().process(['bbH']).AddSyst(
  cmb, 'pdf_gg', 'lnN', ch.SystMap('era')
    (['7TeV'], 1.061)
    (['8TeV'], 1.062))

cmb.cp().process(['bbH']).PrintAll()

def FixMe(sys):
  if sys.process().startswith('ggH_hww') and sys.name() == 'pdf_qqbar':
    print sys
    sys.set_process(sys.process().replace('ggH','qqH'))
    print sys

cmb.ForEachSyst(FixMe)

writer_htt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           '$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA_lhchcg.root')
writer_htt.SetVerbosity(1)
writer_htt.WriteCards('output/htt-YR3-hpt-bbH', cmb.cp().analysis(['htt']))

writer_vhtt = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$BINID_$ERA.txt',
                            '$TAG/common/$ANALYSIS.input_$ERA_lhchcg.root')
writer_vhtt.SetVerbosity(1)
writer_vhtt.WriteCards('output/htt-YR3-hpt-bbH', cmb.cp().analysis(['vhtt']))
