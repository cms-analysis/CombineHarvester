#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import ROOT
import sys

args = sys.argv[1:]
assert (len(args) >= 2)


ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

cb = ch.CombineHarvester()

# this is a technical workaround needed when using ParseCombineWorkspace
cb.SetFlag('workspaces-use-clone', True)

f_wsp = ROOT.TFile(args[0])
workspace = f_wsp.Get('w')

ch.ParseCombineWorkspace(cb, workspace, "ModelConfig", "data_obs", True)

f_fit = ROOT.TFile(args[1])
fitresult = f_fit.Get('fit_s')

cb.UpdateParameters(fitresult)

# Print the full contents
cb.PrintAll()

# Print rate and uncertainty for each process in each category
for b in cb.bin_set():
    for p in cb.cp().bin([b]).process_set():
        print('%-20s %-20s %-12g %-12g' % (b, p, cb.cp().bin([b]).process([p]).GetRate(),
                                     cb.cp().bin([b]).process([p]).GetUncertainty(fitresult, 500)))
    # Total background yield in each category
    print('Total Background: %-12g %-12g' % (
          cb.cp().bin([b]).backgrounds().GetRate(),
          cb.cp().bin([b]).backgrounds().GetUncertainty(fitresult, 500)
    ))
    # Total signal yield in each category
    print('Total Signal:     %-12g %-12g' % (
          cb.cp().bin([b]).signals().GetRate(),
          cb.cp().bin([b]).signals().GetUncertainty(fitresult, 500)
    ))
