import CombineHarvester.CombineTools.plotting as plot 
import CombineHarvester.CombineTools.maketable as maketable
import ROOT
import math
import argparse
import json
import sys

ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='named input file')
parser.add_argument('--labels', help='Labels for legend')
parser.add_argument('--process', help='The process on which a limit has been calculated. [gg#phi, bb#phi]', default="gg#phi")
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
parser.add_argument('--relative',help='Relative difference in limit',action='store_true', default=False)
parser.add_argument('--title',help='Plot label', default='2.2 fb^{-1} (13 TeV)')
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
#parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
args = parser.parse_args()


colourlist=[ROOT.kGreen+3,ROOT.kRed,ROOT.kBlue,ROOT.kBlack,ROOT.kYellow+2,ROOT.kOrange+10,ROOT.kCyan+3,ROOT.kMagenta+2,ROOT.kViolet-5,ROOT.kGray]
files = (args.file).split(',')
if args.labels:
  labels = (args.labels).split(',')
else:
  labels =[]
outname = args.outname

if args.relative and len(files)!=2:
  print 'Provide exactly 2 input files to plot the relative difference in limit'

if len(colourlist) < len(files):
  print 'Too many input files! Maximum supported is %d'%len(colourlist)
  sys.exit(1)

if len(labels) < len(files) and not args.relative:
  print 'Provide at least as many legend labels as files'
  sys.exit(1)


exp_graph_list = [ROOT.TGraph() for i in range(len(files))]
if args.relative:
  obs_graph_list = [ROOT.TGraph() for i in range(len(files))]
for i in range(len(files)):
  if ".root" in files[i]:
    exp_graph_list[i] = plot.SortGraph((ROOT.TFile(files[i],'r')).Get('expected'))
    if args.relative:
     obs_graph_list[i] = plot.SortGraph((ROOT.TFile(files[i],'r')).Get('observed'))
  else:
    data = {}
    with open(files[i]) as jsonfile:
      data = json.load(jsonfile)
    exp_graph_list[i] = plot.LimitTGraphFromJSON(data, 'expected')
    if args.relative:
     obs_graph_list[i] = plot.LimitTGraphFromJSON(data, 'observed')

parton_lumis = [2.149018,2.197008,2.241856,2.28606,2.33067,2.37202,2.45378,2.53216,2.60917,2.79534,2.97773,3.15818,3.33910,3.52189,3.70655,4.09093,4.49192,4.92356,5.38754,5.887]
#yvalues = exp_graph_list[0].GetY();
#print yvalues
#xvalues = exp_graph_list[0].GetX();
#print xvalues
yval, xval = ROOT.Double(0), ROOT.Double(0)
for i in range((exp_graph_list[0].GetN())):
  exp_graph_list[0].GetPoint(i,xval,yval)
  print xval
  print yval
  print yval*parton_lumis[i]
  exp_graph_list[0].SetPoint(i,xval,(yval)*parton_lumis[i])

max_vals = []
for i in range(len(exp_graph_list)):
  max_vals.append(ROOT.TMath.MaxElement(exp_graph_list[i].GetN(),exp_graph_list[i].GetY()))

if args.relative:
  relative_exp_graph = plot.GraphDifference(exp_graph_list[0],exp_graph_list[1]) 
  relative_obs_graph = plot.GraphDifference(obs_graph_list[0],obs_graph_list[1])
  del max_vals[:]
  max_vals.append(ROOT.TMath.MaxElement(relative_exp_graph.GetN(),relative_exp_graph.GetY()))
  if not args.expected_only:
    max_vals.append(ROOT.TMath.MaxElement(relative_obs_graph.GetN(),relative_obs_graph.GetY()))

process_label=args.process

mass_list=[]
for i in range(exp_graph_list[0].GetN()) :
    mass_list.append(float(exp_graph_list[0].GetX()[i]))
mass_list = sorted(set(mass_list))
mass_bins=len(mass_list)
if int(args.verbosity) > 0 :
    print "mass_list: ", mass_list, "Total number: ", mass_bins 

#Create canvas and TH1D

plot.ModTDRStyle(r=0.06, l=0.12)
axis = plot.makeHist1D('hist1d', mass_bins, exp_graph_list[0])
ROOT.gStyle.SetFrameLineWidth(2)
c1=ROOT.TCanvas()
pads = plot.TwoPadSplit(0.8, 0, 0)
pads[1].cd()
axis.GetYaxis().SetRangeUser(0,1.2*float(max(max_vals)))  
if args.log:
  axis.GetYaxis().SetRangeUser(0.001,1.2*float(max(max_vals)))
if process_label == "gg#phi" :
    axis.GetYaxis().SetTitle("95% CL limit on #sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]")
elif process_label == "bb#phi" :
    axis.GetYaxis().SetTitle("95% CL limit on #sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]")
else:
    exit("Currently process is not supported")
if args.custom_y_range : axis.GetYaxis().SetRangeUser(float(args.y_axis_min), float(args.y_axis_max))
axis.GetXaxis().SetTitle("m_{#phi} [GeV]")
if args.custom_x_range : axis.GetXaxis().SetRangeUser(float(args.x_axis_min), float(args.x_axis_max))

axis.GetYaxis().SetTitleSize(0.040)    
axis.GetYaxis().SetTitleOffset(1.2)    
pads[1].SetTickx()
pads[1].SetTicky()
pads[1].cd()
if args.log :
    pads[1].SetLogx(1);
    pads[1].SetLogy(1);
    axis.SetNdivisions(50005, "X");
    axis.GetXaxis().SetMoreLogLabels();
    axis.GetXaxis().SetNoExponent();
    axis.GetXaxis().SetLabelSize(0.040);
axis.Draw()

if not args.relative:
  for i in range(len(files)):
    exp_graph_list[i].SetLineColor(colourlist[i])
    exp_graph_list[i].SetLineWidth(3)
    exp_graph_list[i].SetMarkerStyle(20)
    exp_graph_list[i].SetMarkerColor(colourlist[i])
    exp_graph_list[i].SetLineStyle(2)
    exp_graph_list[i].Draw("PL")
else:
  relative_exp_graph.SetLineColor(ROOT.kRed)
  relative_exp_graph.SetLineWidth(3)
  relative_exp_graph.SetMarkerStyle(20)
  relative_exp_graph.SetMarkerColor(ROOT.kRed)
  relative_exp_graph.SetLineStyle(1)
  relative_exp_graph.Draw("PL")
  if not args.expected_only:
    relative_obs_graph.SetLineColor(ROOT.kBlue)
    relative_obs_graph.SetMarkerColor(ROOT.kBlue)
    relative_obs_graph.SetLineWidth(3)
    relative_obs_graph.SetLineStyle(2)
    relative_obs_graph.SetMarkerStyle(20)
    relative_obs_graph.Draw("PL")

pads[0].cd()

h_top = axis.Clone()
#necessary in case chosen range surrounds 0 which will cause axis to contain a horizontal line at 0
h_top.GetYaxis().SetRangeUser(0.001,100)
plot.Set(h_top.GetXaxis(), LabelSize=0, TitleSize=0, TickLength=0)
plot.Set(h_top.GetYaxis(), LabelSize=0, TitleSize=0, TickLength=0)
h_top.Draw()

legend = plot.PositionedLegend(0.5 if args.relative else 0.4, 0.11, 3, 0.015)
plot.Set(legend, NColumns=1, Header='#bf{%.0f%% CL Excluded:}' % 95)
if not (args.relative):
  for i in range(len(files)):
    legend.AddEntry(exp_graph_list[i],labels[i],"PL")
elif args.relative:
  legend.SetTextSize(0.025)
  legend.AddEntry(relative_exp_graph,"Exp 2*|"+labels[0]+"-"+labels[1]+"|/("+labels[0]+"+"+labels[1]+")","PL")
  if not args.expected_only:
    legend.AddEntry(relative_obs_graph,"Obs 2*|"+labels[0]+"-"+labels[1]+"|/("+labels[0]+"+"+labels[1]+")","PL")
#elif args.absolute:
#  legend.SetTextSize(0.025)
#  legend.AddEntry(relative_exp_graph,"Exp 2*("+labels[0]+"-"+labels[1]+")/("+labels[0]+"+"+labels[1]+")","PL")
  if not args.expected_only:
    legend.AddEntry(relative_obs_graph,"Obs 2*("+labels[0]+"-"+labels[1]+")/("+labels[0]+"+"+labels[1]+")","PL")
legend.Draw()

plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.15, 1.0, '', 1.0)
plot.DrawTitle(pads[0], '%s'%args.title, 3);
plot.FixOverlay()

# Redraw the frame because it usually gets covered by the filled areas
pads[1].cd()
pads[1].GetFrame().Draw()
pads[1].RedrawAxis()

c1.SaveAs("%s.pdf"%outname)
c1.SaveAs("%s.png"%outname)
    
