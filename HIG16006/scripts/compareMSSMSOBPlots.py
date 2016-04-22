#!/usr/bin/env python
import CombineHarvester.CombineTools.plotting as plot 
import CombineHarvester.CombineTools.maketable as maketable
import ROOT
import math
import argparse
import json
import sys


ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Input file(s)')
parser.add_argument('--labels', help='Labels for legend')
parser.add_argument('--mode', help='Plot mode', default='sob', choices=['sob','sosb'])
parser.add_argument('--custom_y_range', help='Fix y axis range', action='store_true', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=0.001)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=100.0)
parser.add_argument('--custom_x_range', help='Fix x axis range', action='store_true', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=90.0)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=1000.0)
parser.add_argument('--verbosity', '-v', help='verbosity', default=0)
parser.add_argument('--log', help='Set log range for x and y axis', action='store_true', default=False)
parser.add_argument('--expected_only', help='Plot expected limit difference only',action='store_true', default=False)
parser.add_argument('--outname','-o', help='Name of output plot', default='limit_comparison')
parser.add_argument('--title',help='Plot label', default='2.3 fb^{-1} (13 TeV)')
#parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
args = parser.parse_args()


colourlist=[ROOT.kGreen+3,ROOT.kRed,ROOT.kBlue,ROOT.kBlack,ROOT.kYellow+2,ROOT.kOrange+10,ROOT.kCyan+3,ROOT.kMagenta+2,ROOT.kViolet-5,ROOT.kGray]
files = (args.file).split(',')
outname = args.outname
if args.labels:
  labels = (args.labels).split(',')
else:
  labels =[]


if len(files) < 1 :
  print 'No input files!'
  sys.exit(1)

if len(colourlist) < len(files):
  print 'Too many input files! Maximum supported is %d'%len(colourlist)
  sys.exit(1)

if len(labels) < len(files) and not (args.relative or args.absolute) :
  print 'Provide at least as many legend labels as files'
  sys.exit(1)


graph_list = [ROOT.TGraph() for i in range(len(files))]
graph_name=""
if args.mode == 'sob' : graph_name='sob_graph'
if args.mode == 'sosb' : graph_name='sosb_graph'

  

for i in range(len(files)):
  if ".root" in files[i] :
    graph_list[i] = plot.SortGraph((ROOT.TFile(files[i],'r')).Get(graph_name)) 



max_vals = []
for i in range(len(graph_list)):
  max_vals.append(ROOT.TMath.MaxElement(graph_list[i].GetN(),graph_list[i].GetY()))


mass_list=[]
for i in range(graph_list[0].GetN()) :
    mass_list.append(float(graph_list[0].GetX()[i]))
mass_list = sorted(set(mass_list))
mass_bins=len(mass_list)
if int(args.verbosity) > 0 :
    print "mass_list: ", mass_list, "Total number: ", mass_bins 

# Setup the canvas: we'll use a two pad split, with a small top pad to contain
# the CMS logo and the legend
plot.ModTDRStyle(r=0.06, l=0.12)
axis = plot.makeHist1D('hist1d', mass_bins, graph_list[0])
ROOT.gStyle.SetFrameLineWidth(2)
c1=ROOT.TCanvas()
pads = plot.TwoPadSplit(0.8, 0, 0)
pads[1].cd()
axis.GetYaxis().SetRangeUser(0,1.2*float(max(max_vals)))  
if args.mode=='sob':
  axis.GetYaxis().SetTitle("S/#sqrt{B}")
if args.mode=='sosb':
  axis.GetYaxis().SetTitle("S/S+B")


if args.custom_y_range : axis.GetYaxis().SetRangeUser(float(args.y_axis_min), float(args.y_axis_max))
axis.GetXaxis().SetTitle("m_{H} [GeV]")
if args.custom_x_range : axis.GetXaxis().SetRangeUser(float(args.x_axis_min), float(args.x_axis_max))
axis.GetYaxis().SetTitleSize(0.040)    
axis.GetYaxis().SetTitleOffset(1.2)    
pads[1].SetTickx()
pads[1].SetTicky()
if args.log :
    pads[1].SetLogx(1);
    pads[1].SetLogy(1);
    axis.SetNdivisions(50005, "X");
    axis.GetXaxis().SetMoreLogLabels();
    axis.GetXaxis().SetNoExponent();
    axis.GetXaxis().SetLabelSize(0.040);
axis.Draw()


for i in range(len(files)):
  graph_list[i].SetLineColor(colourlist[i])
  graph_list[i].SetLineWidth(3)
  graph_list[i].SetMarkerStyle(20)
  graph_list[i].SetMarkerColor(colourlist[i])
  graph_list[i].SetLineStyle(2)
  graph_list[i].Draw("PL")


pads[0].cd()
h_top = axis.Clone()
#necessary in case chosen range surrounds 0 which will cause axis to contain a horizontal line at 0
h_top.GetYaxis().SetRangeUser(0.001,100)
plot.Set(h_top.GetXaxis(), LabelSize=0, TitleSize=0, TickLength=0)
plot.Set(h_top.GetYaxis(), LabelSize=0, TitleSize=0, TickLength=0)
h_top.Draw()


legend = plot.PositionedLegend(0.4, 0.11, 3, 0.015)
plot.Set(legend, NColumns=1, Header='')
for i in range(len(files)):
  legend.AddEntry(graph_list[i],labels[i],"PL")

legend.Draw()

#plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.15, 1.0, '', 1.0)
plot.DrawTitle(pads[0], '%s'%args.title, 3);
plot.FixOverlay()


pads[1].cd()
pads[1].GetFrame().Draw()
pads[1].RedrawAxis()

c1.SaveAs("%s.pdf"%outname)
c1.SaveAs("%s.png"%outname)
