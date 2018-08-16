#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()
ROOT.gStyle.SetTickLength(0., "Y")

parser = argparse.ArgumentParser()
parser.add_argument('--input','-i',help = 'input json file')
parser.add_argument('--output','-o', help = 'Output filename')
parser.add_argument('--extralabel', default='',help = 'Additional CMS label')

args = parser.parse_args()

with open(args.input) as jsonfile:
  js = json.load(jsonfile)

canv = ROOT.TCanvas(args.output,args.output)
pads = plot.OnePad()
pads[0].SetTicks(1,-1)
pads[0].SetLeftMargin(0.23)
pads[0].SetTicky(0)

axis = ROOT.TH2F('axis', '',1,-2,2,7,0,7)
plot.Set(axis.GetYaxis(), LabelSize=0)
plot.Set(axis.GetXaxis(), Title = 'Best fit #mu')
axis.Draw()


cmb_band = ROOT.TBox()
plot.Set(cmb_band, FillColor=ROOT.kGreen)
plot.DrawVerticalBand(pads[0],cmb_band,js['r']['val']-js['r']['ErrLo'],js['r']['val']+js['r']['ErrHi'])

cmb_line = ROOT.TLine()
plot.Set(cmb_line,LineWidth=2)
plot.DrawVerticalLine(pads[0],cmb_line,js['r']['val'])

horizontal_line = ROOT.TLine()
plot.Set(horizontal_line,LineWidth=2,LineStyle=2)
plot.DrawHorizontalLine(pads[0],horizontal_line,3)


gr = ROOT.TGraphAsymmErrors(5)
plot.Set(gr, LineWidth=2, LineColor=ROOT.kRed)

y_pos = 4.5
x_text = -3.1
i=0
latex = ROOT.TLatex()
plot.Set(latex, TextAlign=12,TextSize=0.03)
latex.SetTextFont(42)
order = ['r_ZH','r_WH','r_zerolep','r_onelep','r_twolep']
txt_dict = {
  'r_ZH': '#splitline{ZH(bb)}{#mu = %.2f #pm %.2f}'%(js['r_ZH']['val'],(js['r_ZH']['ErrHi']+js['r_ZH']['ErrLo'])/2.),
  'r_WH': '#splitline{WH(bb)}{#mu = %.2f #pm %.2f}'%(js['r_WH']['val'],(js['r_WH']['ErrHi']+js['r_WH']['ErrLo'])/2.),
  'r_zerolep': '#splitline{0 lept.}{#mu = %.2f #pm %.2f}'%(js['r_zerolep']['val'],(js['r_zerolep']['ErrHi']+js['r_zerolep']['ErrLo'])/2.),
  'r_onelep': '#splitline{1 lept.}{#mu = %.2f #pm %.2f}'%(js['r_onelep']['val'],(js['r_onelep']['ErrHi']+js['r_onelep']['ErrLo'])/2.),
  'r_twolep': '#splitline{2 lept.}{#mu = %.2f #pm %.2f}'%(js['r_twolep']['val'],(js['r_twolep']['ErrHi']+js['r_twolep']['ErrLo'])/2.)
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

plot.DrawCMSLogo(pads[0],'CMS','%s'%args.extralabel,11,0.045,0.03,1.0,'',1.0)
plot.DrawTitle(pads[0],'41.3 fb^{-1} (13 TeV)',3)

latex.SetTextFont(42)
latex.SetTextSize(0.03)
#latex.DrawLatex(-0.82,6.1,"pp#rightarrow VH; H#rightarrow b#bar{b}")
#latex.DrawLatex(-0.82,5.7,"Combined #mu=%.1f#pm%.1f"%(js['r']['val'],js['r']['ErrHi']))
latex.DrawLatex(-1.82,5.6,"pp#rightarrow VH; H#rightarrow b#bar{b}")
latex.DrawLatex(-1.82,5.2,"#mu = %.2f #pm %.2f (stat.) #pm %.2f (syst.)"%(js['r']['val'],(js['r']['StatHi']+js['r']['StatLo'])/2.,(js['r']['SystHi']+js['r']['SystLo'])/2.))

canv.Print('.png')
canv.Print('.pdf')
