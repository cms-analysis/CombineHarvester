#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import sys
import ROOT
import math
from functools import partial
import Tools.Plotting.plotting as plot
import os.path
import bisect
from six.moves import range

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

h1 = ROOT.TH1F('h1', '', 100, 0, 10)
for i in range(1, 101):
    h1.SetBinContent(i, float(i))
h2 = ROOT.TH1F('h2', '', 10, 0, 10)
for i in range(1, 11):
    h2.SetBinContent(i, float(i))

h1.Print('range')
h2.Print('range')

r1 = ROOT.RooRealVar('r1', 'r1', 0)

rdh1 = ROOT.RooDataHist('rdh1', 'rdh1', ROOT.RooArgList(r1), ROOT.RooFit.Import(h1))
rhf1 = ROOT.RooHistFunc('rhf1', 'rhf1', ROOT.RooArgSet(r1), rdh1)

wsp = ROOT.RooWorkspace('w', 'w')
getattr(wsp, 'import')(rhf1, ROOT.RooFit.RecycleConflictNodes())


rdh2 = ROOT.RooDataHist('rdh2', 'rdh2', ROOT.RooArgList(r1), ROOT.RooFit.Import(h2))
rhf2 = ROOT.RooHistFunc('rhf2', 'rhf2', ROOT.RooArgSet(r1), rdh2)

getattr(wsp, 'import')(rhf2, ROOT.RooFit.RecycleConflictNodes())

# r1.Print()

r1 = wsp.var('r1')
rhf1 = wsp.function('rhf1')
rhf2 = wsp.function('rhf2')

r1.setBins(10)

x = 0.05
while x <= 10.:
    r1.setVal(x)
    print('r1 = %f; rhf1 = %f; rhf2 = %f' % (x, rhf1.getVal(), rhf2.getVal()))
    x += 0.1
