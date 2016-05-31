#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.plotting as plot

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

cat = 'mt_nobtag'
fin = ROOT.TFile('WJetsFakeWeights_Debug.root')

nom = fin.Get(cat+'_Nominal')
shi = fin.Get(cat+'_Up')
slo = fin.Get(cat+'_Down')

canv = ROOT.TCanvas(cat, cat)
pads = plot.TwoPadSplit(0.30, 0.01, 0.01)

legend = ROOT.TLegend(0.50, 0.75, 0.93, 0.93, '', 'NBNDC')


plot.Set(nom, LineColor=ROOT.kBlack, LineWidth=3)
plot.Set(shi, LineColor=ROOT.kRed, LineWidth=3)
plot.Set(slo, LineColor=ROOT.kBlue, LineWidth=3)

nom.Draw('HIST')
shi.Draw('HISTSAME')
slo.Draw('HISTSAME')

axis = plot.GetAxisHist(pads[0])
axis.GetXaxis().SetRangeUser(0, 700)


legend.AddEntry(nom, 'Weighted (Nominal)', 'L')
legend.AddEntry(slo, 'Unweighted (Down)', 'L')
legend.AddEntry(shi, 'Weighted^2 (Up)', 'L')

plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.30)
legend.Draw()

plot.Set(axis.GetXaxis(), Title='m_{T,#tau#tau}')
plot.Set(axis.GetYaxis(), Title='Events')

pads[1].cd()

rhi = shi.Clone()
rlo = slo.Clone()

rhi.Divide(nom)
rlo.Divide(nom)
rhi.Draw('HIST')
rlo.Draw('HISTSAME')

plot.SetupTwoPadSplitAsRatio(
    pads, plot.GetAxisHist(
        pads[0]), plot.GetAxisHist(pads[1]), 'Ratio', True, 0.6, 1.4)

plot.GetAxisHist(pads[1]).GetXaxis().SetRangeUser(0, 700)

# plot.DrawTitle(pads[0], args.title_left, 1)
plot.DrawTitle(pads[0], cat + ' W+jets shape', 3)

canv.Print('.pdf')
canv.Print('.png')
