#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

parser = argparse.ArgumentParser()
parser.add_argument('--input','-i',help = 'input json file')
parser.add_argument('--output','-o', help = 'Output filename')

args = parser.parse_args()

with open(args.input) as jsonfile:
  js = json.load(jsonfile)

canv = ROOT.TCanvas(args.output,args.output)
pads = plot.OnePad()
pads[0].SetTicks(1,-1)
pads[0].SetLeftMargin(0.3)

axis = ROOT.TH2F('axis', '',1,-1,3,7,0,7)
plot.Set(axis.GetYaxis(), LabelSize=0)
plot.Set(axis.GetXaxis(), Title = 'Best fit #mu')
axis.Draw()


cmb_band = ROOT.TBox()
plot.Set(cmb_band, FillColor=ROOT.kGreen)
plot.DrawVerticalBand(pads[0],cmb_band,1.2-0.4,1.2+0.4)

cmb_line = ROOT.TLine()
plot.Set(cmb_line,LineWidth=2)
plot.DrawVerticalLine(pads[0],cmb_line,1.2)


gr = ROOT.TGraphAsymmErrors(5)
plot.Set(gr, LineWidth=2, LineColor=ROOT.kRed)

y_pos = 5.5
x_text = -2.7
i=0
latex = ROOT.TLatex()
plot.Set(latex, TextAlign=12,TextSize=0.035)
order = ['r_ZH','r_WH','r_zerolep','r_onelep','r_twolep']
txt_dict = {
  'r_ZH': '#splitline{ZH(bb)}{#mu=%.1f#pm%.1f}'%(js['r_ZH']['val'],js['r_ZH']['ErrHi']),
  'r_WH': '#splitline{WH(bb)}{#mu=%.1f#pm%.1f}'%(js['r_WH']['val'],js['r_WH']['ErrHi']),
  'r_zerolep': '#splitline{0 lept.}{#mu=%.1f#pm%.1f}'%(js['r_zerolep']['val'],js['r_zerolep']['ErrHi']),
  'r_onelep': '#splitline{1 lept.}{#mu=%.1f#pm%.1f}'%(js['r_onelep']['val'],js['r_onelep']['ErrHi']),
  'r_twolep': '#splitline{2 lept.}{#mu=%.1f#pm%.1f}'%(js['r_twolep']['val'],js['r_twolep']['ErrHi'])
}

for stre in order:
  gr.SetPoint(i,js[stre]['val'],y_pos)
  gr.SetPointError(i,js[stre]['ErrLo'],js[stre]['ErrHi'],0,0)
  latex.DrawLatex(x_text,y_pos,txt_dict[stre])

  i+=1
  y_pos -= 1.

gr.Draw("SAMEP")

pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

plot.DrawCMSLogo(pads[0],'CMS','',11.,0.045,0.05,1.0,'',1.0)
plot.DrawTitle(pads[0],'35.9 fb^{-1} (13 TeV)',3)

canv.Print('.png')
canv.Print('.pdf')
