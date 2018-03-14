#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()


def readColumns(file, tree, columns):
    """Extracts the output from the MultiDimFit singles mode
    Note: relies on the list of parameters that were run (scanned) being correct"""
    res = {}
    f = ROOT.TFile(file)
    if f is None or f.IsZombie():
        return None
    t = f.Get(tree)
    res = []
    for evt in t:
        vals = tuple([getattr(evt, col) for col in columns])
        print vals
        res.append(vals)
    return res


mod1 = sys.argv[1]
mod2 = sys.argv[2]
toy = sys.argv[3]


x1 = readColumns('fitDiagnostics.ttH_plus_run1.A1_ttH.mod.%s.toy.%s.merged.root' % (mod1, toy), 'tree_fit_sb', ['mu_XS_ttH', 'mu_XS_ttHLoErr', 'mu_XS_ttHHiErr'])
x2 = readColumns('fitDiagnostics.ttH_plus_run1.A1_ttH.mod.%s.toy.%s.merged.root' % (mod2, toy), 'tree_fit_sb', ['mu_XS_ttH', 'mu_XS_ttHLoErr', 'mu_XS_ttHHiErr'])

print len(x1)
print len(x2)

h_abs_diff = ROOT.TH1F('abs_diff', '', 50, -0.2, 0.2)
h_abs_diff.SetLineColor(ROOT.kRed)

h_err_rel = ROOT.TH1F('err_rel', '', 50, 0.9, 1.1)
h_err_rel.SetLineColor(ROOT.kBlue)

h_err_abs = ROOT.TH1F('err_abs', '', 50, -0.1, 0.1)
h_err_abs.SetLineColor(ROOT.kBlue)

for i in range(len(x1)):
    h_abs_diff.Fill(x2[i][0] - x1[i][0])
    if (x1[i][1]+x1[i][2]) > 0.:
        h_err_rel.Fill(((x2[i][1]+x2[i][2])/2.)/((x1[i][1]+x1[i][2])/2.))
    h_err_abs.Fill(((x2[i][1]+x2[i][2])/2.) - ((x1[i][1]+x1[i][2])/2.))

h_abs_diff.GetXaxis().SetTitle('#hat{#mu}_{%s} - #hat{#mu}_{%s}' % (mod2, mod1))
h_abs_diff.GetYaxis().SetTitle('nToys')

h_err_rel.GetXaxis().SetTitle('#sigma_{%s}/#sigma_{%s}' % (mod2, mod1))
h_err_rel.GetYaxis().SetTitle('nToys')

h_err_abs.GetXaxis().SetTitle('#sigma_{%s} - #sigma_{%s}' % (mod2, mod1))
h_err_abs.GetYaxis().SetTitle('nToys')

canv = ROOT.TCanvas('%s_%s_%s_abs_diff' % (mod1, mod2, toy), 'abs_diff')
pads = plot.OnePad()
h_abs_diff.Draw('HIST')

mean = h_abs_diff.GetMean()
stdv = h_abs_diff.GetStdDev()

# mean = h_abs_diff.GetMean()
stdverr = h_abs_diff.GetStdDevError()
print 'stdv = %.3f +/- %.3f' % (stdv, stdverr)

box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
box.AddText('Mean = %.3f' % mean)
box.AddText('StdDev = %.3f' % stdv)
box.Draw()

# plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)

canv.Print('.pdf')
canv.Print('.png')


canv = ROOT.TCanvas('%s_%s_%s_err_rel' % (mod1, mod2, toy), 'err_rel')
pads = plot.OnePad()
h_err_rel.Draw('HIST')

mean = h_err_rel.GetMean()
stdv = h_err_rel.GetStdDev()

box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
box.AddText('Mean = %.3f' % mean)
box.AddText('StdDev = %.3f' % stdv)
box.Draw()

# plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)


canv.Print('.pdf')
canv.Print('.png')


canv = ROOT.TCanvas('%s_%s_%s_err_abs' % (mod1, mod2, toy), 'err_abs')
pads = plot.OnePad()
h_err_abs.Draw('HIST')

mean = h_err_abs.GetMean()
stdv = h_err_abs.GetStdDev()

box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, 'NDCNB')
box.AddText('Mean = %.3f' % mean)
box.AddText('StdDev = %.3f' % stdv)
box.Draw()

# plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.12, 0.035, 1.2)
plot.DrawTitle(pads[0], 'Toy data: %s' % toy, 3)


canv.Print('.pdf')
canv.Print('.png')
