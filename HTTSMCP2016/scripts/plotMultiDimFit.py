import CombineHarvester.CombineTools.plotting as plot 
import ROOT
import math
import argparse
from array import array

import sys
sys.setrecursionlimit(10000)

ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs="+", help='Input files')
parser.add_argument(
    '--output', '-o', default='limit', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--sm-exp', default=[], nargs="+", help="""Input files for the SM expectation""")
parser.add_argument(
    '--bg-exp', default=[], nargs="+", help="""Input files for the backgroud only expectation""")
parser.add_argument(
    '--cms-sub', default='Preliminary', help="""Text below the CMS logo""")
parser.add_argument(
    '--mass', default='', help="""Mass label on the plot""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--x-title', default='#alpha_{hgg} (#circ)', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='#mu_{ggH}^{#tau#tau}', help="""Title for the y-axis""")
parser.add_argument(
    '--x-min', default=None, help="minimum xaxis point")
parser.add_argument(
    '--x-max', default=None, help="maximum xaxis point")
parser.add_argument(
    '--y-min', default=None, help="minimum yaxis point")
parser.add_argument(
    '--y-max', default=None, help="maximum yaxis point")
parser.add_argument(
    '--debug-output', '-d', help="""If specified, write the contour TH2s and
    TGraphs into this output ROOT file""")
parser.add_argument('--kappa', action='store_true', help='Produce 2D plot for kappa parameterisation')
args = parser.parse_args()

#Create canvas and TH2D for each component
plot.ModTDRStyle(width=600, l=0.12)
ROOT.gStyle.SetNdivisions(510, 'XYZ')
plot.SetBirdPalette()
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()

if args.debug_output is not None:
    debug = ROOT.TFile(args.debug_output, 'RECREATE')
else:
    debug = None

limit = plot.MakeTChain(args.files, 'limit')
if args.kappa:
  args.x_title = '#kappa_{t}'
  args.y_title = '#tilde{#kappa}_{t}'
  graph = plot.TGraph2DFromTree(
      limit, "kh", "ka", '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0 && deltaNLL < 1000')
  best = plot.TGraphFromTree(
      limit, "kh", "ka", 'deltaNLL == 0')
 
else:
  graph = plot.TGraph2DFromTree(
      limit, "alpha", "muggH", '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0 && deltaNLL < 1000')

  best = plot.TGraphFromTree(
      limit, "alpha", "muggH", 'deltaNLL == 0')
plot.RemoveGraphXDuplicates(best)
hists = plot.TH2FromTGraph2D(graph, method='BinCenterAligned')
plot.fastFillTH2(hists, graph,interpolateMissing=True)
if args.bg_exp:
    limit_bg = plot.MakeTChain(args.bg_exp, 'limit')
    best_bg = plot.TGraphFromTree(
        limit_bg, "alpha", "muggH", 'deltaNLL == 0')
    plot.RemoveGraphXDuplicates(best_bg)

# If included just plot SM exp at 1,1
if args.sm_exp:
    limit_sm = plot.MakeTChain(args.sm_exp, 'limit')
    if args.kappa: best_sm = ROOT.TGraph( 1, array('d', [1,]), array('d', [0,]))
    else: best_sm = ROOT.TGraph( 1, array('d', [1,]), array('d', [1,]))
    plot.RemoveGraphXDuplicates(best_sm)
hists.SetMaximum(6)
hists.SetMinimum(0)
hists.SetContour(255)
# c2=ROOT.TCanvas()
# hists.Draw("COLZ")
# c2.SaveAs("heatmap.png")

if args.x_min is not None:
  x_min = float(args.x_min)
else: x_min = hists.GetXaxis().GetXmin()
if args.x_max is not None:
  x_max = float(args.x_max)
else: x_max = hists.GetXaxis().GetXmax()

if args.y_min is not None:
  y_min = float(args.y_min)
else: y_min = hists.GetYaxis().GetXmin()
if args.y_max is not None:
  y_max = float(args.y_max)
else: y_max = hists.GetYaxis().GetXmax()

axis = ROOT.TH2D(hists.GetName(),hists.GetName(),hists.GetXaxis().GetNbins(),x_min,x_max,hists.GetYaxis().GetNbins(),y_min,y_max)

axis.Reset()
axis.GetXaxis().SetTitleOffset(0.9)
axis.GetXaxis().SetTitle(args.x_title)
axis.GetXaxis().SetLabelSize(0.025)
axis.GetYaxis().SetLabelSize(0.025)
axis.GetYaxis().SetTitle(args.y_title)
cont_2sigma = None
cont_1sigma = plot.contourFromTH2(hists, ROOT.Math.chisquared_quantile_c(1 - 0.68, 2), 10, frameValue=20)
cont_2sigma = plot.contourFromTH2(hists, ROOT.Math.chisquared_quantile_c(1 - 0.95, 2), 10, frameValue=20)
if args.kappa: cont_2sigma = plot.contourFromTH2(hists, ROOT.Math.chisquared_quantile_c(1 - 0.95, 2), 1, frameValue=20)
#cont_1sigma = plot.contourFromTH2(hists, 1., 10, frameValue=20)
#cont_2sigma = plot.contourFromTH2(hists, 3.8415, 10, frameValue=20)
print cont_1sigma
for item in cont_1sigma :
    print item
print cont_2sigma
for item in cont_2sigma :
    print item

if debug is not None:
    debug.WriteTObject(hists, 'hist')
    for i, cont in enumerate(cont_1sigma):
        debug.WriteTObject(cont, 'cont_1sigma_%i' % i)
    for i, cont in enumerate(cont_2sigma):
        debug.WriteTObject(cont, 'cont_2sigma_%i' % i)

if args.sm_exp or args.bg_exp:
    legend = plot.PositionedLegend(0.3, 0.20, 3, 0.015)
else:
    legend = plot.PositionedLegend(0.3, 0.2, 3, 0.015)

pads[0].cd()
pads[0].SetTicks(1)
axis.Draw()
count1sigma=0
for i, p in enumerate(cont_2sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-10)
    p.SetFillStyle(1001)
    p.Draw("F SAME")
    p.Draw("L SAME")
    if i ==0: legend.AddEntry(cont_1sigma[0], "68% CL", "F")
    if args.kappa and i==1: p.SetFillColor(ROOT.kWhite)
    #break

for i, p in enumerate(cont_1sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-8)
    p.SetFillStyle(1001)
    #print i
    #if False or (args.kappa and i==1): 
    #  p.SetFillStyle(0)
    #  p.SetFillColor(ROOT.kWhite)
    if args.kappa and i==1: p.SetFillColor(ROOT.kBlue-10)
    p.Draw("F SAME")
    p.Draw("L SAME")
    if i ==0: legend.AddEntry(cont_2sigma[0], "95% CL", "F")
    #break

if args.kappa:
    cont_2sigma[len(cont_2sigma)-2].Draw("F SAME")
    cont_2sigma[len(cont_2sigma)-2].Draw("L SAME")

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(12)
    latex.DrawLatex(.75,.70,"#bf{#mu^{#tau#tau}=1}")


if not args.kappa:
  func = ROOT.TF1 ("func","cos(pi/2*x/90)*cos(pi/2*x/90) +sin(pi/2*x/90)*sin(pi/2*x/90)*2.25",-90,90)
  func.SetLineWidth(3)
  func.SetLineStyle(2)
#  func.Draw("same")

best.SetMarkerStyle(34)
best.SetMarkerSize(3)
best.Draw("P SAME")
legend.AddEntry(best, "Best fit", "P")
legend.SetFillStyle(0)
#if not args.kappa: legend.AddEntry(func, "Exp with #mu^{#tau#tau}=1, y_{t}=#tilde{y_{t}}", "L")

if args.sm_exp:
    best_sm.SetMarkerStyle(33)
    best_sm.SetMarkerColor(1)
    best_sm.SetMarkerSize(3.0)
    best_sm.Draw("P SAME")
    legend.AddEntry(best_sm, "SM Expected", "P")
if args.bg_exp:
    best_bg.SetMarkerStyle(33)
    best_bg.SetMarkerColor(46)
    best_bg.SetMarkerSize(3)
    best_bg.Draw("P SAME")
    legend.AddEntry(best_bg, "Expected for background only", "P")


#if args.mass:
#    legend.SetHeader("m_{#phi} = "+args.mass+" GeV")
legend.Draw("SAME")
if args.sm_exp:
    overlayLegend,overlayGraphs = plot.getOverlayMarkerAndLegend(legend, {legend.GetNRows()-1 : best_sm}, {legend.GetNRows()-1 : {"MarkerColor" : 2}}, markerStyle="P")

plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.035, 1.2, '', 1.0)
pads[0].cd()
lumi = ROOT.TLatex(.7,1.05,"X fb^{-1} (13 TeV)")
lumi.SetTextSize(0.03)
#lumi.DrawTextNDC(.7,.96,"35.9 / fb (13 TeV)" )

plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawTitle(pads[0], args.title_left, 1)
plot.FixOverlay()
if args.sm_exp:
    best_sm.Draw("P SAME")
    for overlayGraph in overlayGraphs:
        print "test"
        overlayGraph.Draw("P SAME")
    overlayLegend.Draw("SAME")
canv.Print('.pdf')
canv.Print('.png')
canv.Print('.C')
canv.Close()

if debug is not None:
    debug.Close()
