#!/usr/bin/env python
import ROOT
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()
# plot.SetCorrMatrixPalette()
# ROOT.gStyle.SetNdivisions(510, "XYZ")
# ROOT.gStyle.SetMarkerSize(1.4)
# ROOT.gStyle.SetPaintTextFormat('.2f')


parser = argparse.ArgumentParser()


parser.add_argument('--input', '-i', help='input name')
parser.add_argument('--output', '-o', help='output name')
# parser.add_argument('--input', '-i', help='Main input file')
# parser.add_argument('--label', '-l', help='Main input file')
# parser.add_argument('--translate', default='texName.json', help='json file with POI name translation')
# parser.add_argument('--cov', action='store_true', help='json file with POI name translation')

args = parser.parse_args()


do_ratio = True
# inputs = args.input.split(':')
fin = ROOT.TFile(args.input)
h_bkg = fin.Get('h_bkg')

h_sig = fin.Get('h_sig')
h_sig_mu1 = fin.Get('h_sig_mu1')
h_dat = fin.Get('h_dat')
h_err = h_bkg.Clone()

axes = [h_bkg.Clone('axis'), h_bkg.Clone('axis')]


canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()

# sb_sig.SetBinContent(17, 0.);
# sb_bkg.SetBinContent(17, 0.);
# sb_obs.SetBinContent(17, 0.);

h_bkg.SetFillColor(18)
h_sig.SetFillColor(ROOT.kRed)
h_sig.SetFillStyle(3004)
h_sig.SetLineColor(ROOT.kRed)
h_sig_mu1.SetFillColor(ROOT.kOrange-2)
h_sig_mu1.SetFillStyle(3004)
h_sig_mu1.SetLineColor(ROOT.kOrange-2)

new_idx = plot.CreateTransparentColor(12, 0.4)
h_err.SetFillColor(new_idx)
h_err.SetMarkerSize(0)

h_sig_num = h_sig.Clone()
h_sig_num.Add(h_bkg)
h_sig_r = plot.MakeRatioHist(h_sig_num, h_bkg, False, False)
blank_r = h_bkg.Clone()
for i in xrange(1, blank_r.GetNbinsX()+1):
    blank_r.SetBinContent(i, 1.)

blank_r.SetFillColor(10)
blank_r.SetFillStyle(1001)

h_sig_mu1_num = h_sig_mu1.Clone()
h_sig_mu1_num.Add(h_bkg)
h_sig_mu1_r = plot.MakeRatioHist(h_sig_mu1_num, h_bkg, False, False)
# h_sig_mu1_r.SetFillStyle(0)

h_dat_r = plot.MakeRatioHist(h_dat, h_bkg, True, False)
h_err_r = plot.MakeRatioHist(h_err, h_bkg, True, False)

stack = ROOT.THStack("stack", "stack")
stack.Add(h_bkg, "hist")
stack.Add(h_sig, "hist")
stack2 = ROOT.THStack("stack2", "stack2")
stack2.Add(h_bkg, "hist")
stack2.Add(h_sig_mu1, "hist")


if do_ratio:
    pads = plot.TwoPadSplit(0.35, 0.005, 0.005)
else:
    pads = plot.OnePad()

pads[0].SetLogy(True)

if do_ratio:
    plot.SetupTwoPadSplitAsRatio(pads, axes[0], axes[1], "Obs. / Bkg.", True, 0.8, 2.9)
    axes[1].GetXaxis().SetTitle("log_{10}(S/B)")
    axes[0].GetYaxis().SetTitle("Events")
else:
    axes[0].GetXaxis().SetTitle("log_{10}(S/B)")
    axes[0].GetYaxis().SetTitle("Events")


axes[0].Draw("axis")
axes[0].SetMinimum(1.0)

stack.Draw("samenoclear")
stack2.Draw("samenoclear")
h_err.Draw('e2same')
h_dat.Draw("esamex0")


pads[1].cd()
axes[1].Draw("axis")
axes[1].GetYaxis().SetDecimals(True)
axes[1].GetXaxis().SetDecimals(True)

line = ROOT.TLine()
plot.DrawHorizontalLine(pads[1], line, 1)

h_sig_r.Draw('samehist')
h_sig_mu1_r.Draw('samehist')
blank_r.Draw('samehist')
blank_r.Print('range')
h_err_r.Draw('e2same')
h_dat_r.Draw('esamex0')

pads[0].cd()


axes[0].SetMaximum(8E6)
# plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.3)

legend = plot.PositionedLegend(0.30, 0.20, 3, 0.03)
legend.AddEntry(h_dat, "Observed", "pe")
legend.AddEntry(h_bkg, "Background", "f")
legend.AddEntry(h_err, "Uncertainty", "f")
legend.AddEntry(h_sig, "t#bar{t}H (#mu=1.26)", "f")
legend.AddEntry(h_sig_mu1, "t#bar{t}H (#mu=1.00)", "f")
# // legend->AddEntry(&sb_err, "Bkg. Uncertainty", "f");
legend.Draw()

for pad in pads:
    pad.cd()
    plot.FixOverlay()


# plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 0, 0.12, 0.035, 1.2)
plot.DrawCMSLogo(pads[0], 'CMS', 'Supplementary', 11, 0.045, 0.035, 1.2, '', 0.9)
plot.DrawTitle(pads[0], '5.1 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 35.9 fb^{-1} (13 TeV)' , 3)


canv.Print('.pdf')
canv.Print('.png')
# canv.Print('.C')
