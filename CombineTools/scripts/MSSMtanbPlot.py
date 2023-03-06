from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.plotting as plot
import ROOT
import math
import argparse
from six.moves import range


col_store = []
def CreateTransparentColor(color, alpha):
    adapt   = ROOT.gROOT.GetColor(color)
    new_idx = ROOT.gROOT.GetListOfColors().GetSize() + 1
    trans = ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
    col_store.append(trans)
    trans.SetName('userColor%i' % new_idx)
    return new_idx


ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='named input file')
parser.add_argument('--scenario', '-s', help='scenario for plot label e.g. [mhmax,mhmodp,mhmodm,low-tb-high]')
parser.add_argument('--custom_y_range', help='Fix y axis range', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=0.0)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=60.0)
parser.add_argument('--custom_x_range', help='Fix x axis range', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=90.0)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=1000.0)
parser.add_argument('--verbosity', '-v', help='verbosity', default=0)
parser.add_argument('--expected_only', help='Do not plot observed', default=False)
parser.add_argument('--lumi_label', '-l', help='lumi label e.g. 19.7 fb^{-1} (8TeV)', default='19.7 fb^{-1} (8TeV)')
parser.add_argument('--ana_label', '-a', help='analysis label (for now just for filename but can also include label on plot) e.g. Hhh, AZh, mssm', default='mssm')
args = parser.parse_args()


#Store the mA and tanb list being used for the interpolation
file = ROOT.TFile(args.file, 'r')
print(args.file)
graph_obs         = file.Get("obs")
graph_minus2sigma = file.Get("exp-2")
graph_minus1sigma = file.Get("exp-1")
graph_exp         = file.Get("exp0")
graph_plus1sigma  = file.Get("exp+1")
graph_plus2sigma  = file.Get("exp+2")

mA_list=[]
tanb_list=[]
for i in range(graph_exp.GetN()) :
    mA_list.append(float(graph_exp.GetX()[i]))
    tanb_list.append(float(graph_exp.GetY()[i]))
tanb_list = sorted(set(tanb_list))
mA_list = sorted(set(mA_list))
tanb_bins=len(tanb_list)
mA_bins=len(mA_list)
if int(args.verbosity) > 0 :
    print("mA_list: ", mA_list, "Total number: ", mA_bins)
    print("tanb_list: ", tanb_list, "Total number: ", tanb_bins)

#Create canvas and TH2D for each component
plot.ModTDRStyle(width=600, l=0.12)
#Slightly thicker frame to ensure contour edges dont overlay the axis
ROOT.gStyle.SetFrameLineWidth(2)
c1=ROOT.TCanvas()
#axis = plot.makeHist2D('hist2d', mA_bins, tanb_bins, graph_exp)
axis = plot.makeVarBinHist2D('hist2d', mA_list, tanb_list)
axis.GetYaxis().SetTitle("tan#beta")
axis.GetXaxis().SetTitle("m_{A} (GeV)")
#Create two pads, one is just for the Legend
pad1 = ROOT.TPad("pad1","pad1",0,0.82,1,1)
pad1.SetFillStyle(4000)
pad1.Draw()
pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.82)
pad2.SetFillStyle(4000)
pad2.Draw()
pads=[pad1,pad2]
pads[1].cd()

#Note the binning of the TH2D for the interpolation should ~ match the initial input grid
#Could in future implement variable binning here
#h_exp = plot.makeVarBinHist2D("h_exp", mA_list, tanb_list)
#h_obs = plot.makeVarBinHist2D("h_obs", mA_list, tanb_list)
#h_minus1sigma = plot.makeVarBinHist2D("h_minus1sigma", mA_list, tanb_list)
#h_plus1sigma = plot.makeVarBinHist2D("h_plus1sigma", mA_list, tanb_list)
#h_minus2sigma = plot.makeVarBinHist2D("h_minus2sigma", mA_list, tanb_list)
#h_plus2sigma = plot.makeVarBinHist2D("h_plus2sigma", mA_list, tanb_list)
h_exp = plot.makeHist2D("h_exp", mA_bins, tanb_bins, graph_exp)
h_obs = plot.makeHist2D("h_obs", mA_bins, tanb_bins, graph_obs)
h_minus1sigma = plot.makeHist2D("h_minus1sigma", mA_bins, tanb_bins, graph_minus1sigma)
h_plus1sigma = plot.makeHist2D("h_plus1sigma", mA_bins, tanb_bins, graph_plus1sigma)
h_minus2sigma = plot.makeHist2D("h_minus2sigma", mA_bins, tanb_bins, graph_minus2sigma)
h_plus2sigma = plot.makeHist2D("h_plus2sigma", mA_bins, tanb_bins, graph_plus2sigma)
plot.fillTH2(h_exp, graph_exp)
plot.fillTH2(h_obs, graph_obs)
plot.fillTH2(h_minus1sigma, graph_minus1sigma)
plot.fillTH2(h_plus1sigma, graph_plus1sigma)
plot.fillTH2(h_minus2sigma, graph_minus2sigma)
plot.fillTH2(h_plus2sigma, graph_plus2sigma)
axis.Draw()
#Possibility to draw CLs heat map, would be a useful option, using e.g.
#h_exp.Draw("colzsame")

#Extract exclusion contours from the TH2Ds, use threshold 1.0 for limit and 0.05 for CLs
threshold=0.05
#threshold=1
cont_exp = plot.contourFromTH2(h_exp, threshold, 20)
cont_obs = plot.contourFromTH2(h_obs, threshold, 5)
cont_minus1sigma = plot.contourFromTH2(h_minus1sigma, threshold, 20)
cont_plus1sigma = plot.contourFromTH2(h_plus1sigma, threshold, 20)
cont_minus2sigma = plot.contourFromTH2(h_minus2sigma, threshold, 20)
cont_plus2sigma = plot.contourFromTH2(h_plus2sigma, threshold, 20)

#if args.scenario != "hMSSM" and "2HDM" not in args.scenario :
#    graph_higgshBand = plot.higgsConstraint(args.scenario, "h")
#    plane_higgshBand = plot.makeHist2D('plane_higgshBand', 36, 91, graph_higgshBand)
#    plot.fillTH2(plane_higgshBand, graph_higgshBand)
#    cont_higgshlow = plot.contourFromTH2(plane_higgshBand, 122, 5)
#    cont_higgshhigh = plot.contourFromTH2(plane_higgshBand, 128, 5)
#    cont_higgsh = plot.contourFromTH2(plane_higgshBand, 125, 5)

if int(args.verbosity) > 0 : outf = ROOT.TFile('plotting_debug.root', 'RECREATE')
if int(args.verbosity) > 0 : outf.WriteTObject(h_minus2sigma, 'h_minus2sigma')
for i, p in enumerate(cont_minus2sigma):
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_minus2sigma_%i'%i)

if int(args.verbosity) > 0 : outf.WriteTObject(h_minus1sigma, 'h_minus1sigma')
for i, p in enumerate(cont_minus1sigma):
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+2)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_minus1sigma_%i'%i)

if int(args.verbosity) > 0 : outf.WriteTObject(h_plus1sigma, 'h_plus1sigma')
for i, p in enumerate(cont_plus1sigma):
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_plus1sigma_%i'%i)

if int(args.verbosity) > 0 : outf.WriteTObject(h_plus2sigma, 'h_plus2sigma')
for i, p in enumerate(cont_plus2sigma):
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kWhite)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_plus2sigma_%i'%i)

if int(args.verbosity) > 0 : outf.WriteTObject(h_exp, 'h_exp')
for i, p in enumerate(cont_exp):
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetLineStyle(2)
    p.SetFillColor(100)
    pads[1].cd()
    p.Draw("L SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_exp_%i'%i)

if int(args.verbosity) > 0 : outf.WriteTObject(h_obs, 'h_obs')
for i,p in enumerate(cont_obs):
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetMarkerStyle(20)
    p.SetMarkerSize(1.0)
    p.SetMarkerColor(ROOT.kBlack)
    p.SetFillStyle(1001)
    p.SetFillColor(CreateTransparentColor(ROOT.kAzure+6,0.5))
    pads[1].cd()
    if not args.expected_only:
        p.Draw("F SAME")
        p.Draw("L SAME")
    if int(args.verbosity) > 0 : outf.WriteTObject(p, 'graph_obs_%i'%i)

if int(args.verbosity) > 0 : outf.Close()

#if args.scenario != "hMSSM" and "2HDM" not in args.scenario :
#    if cont_higgshhigh :
#        for p in cont_higgshhigh:
#            p.SetLineWidth(-402)
#            p.SetFillStyle(3005)
#            p.SetFillColor(ROOT.kRed)
#            p.SetLineColor(ROOT.kRed)
#            pads[1].cd()
#            p.Draw("L SAME")

#    if cont_higgshlow :
#        for p in cont_higgshlow:
#            p.SetLineWidth(402)
#            p.SetFillStyle(3005)
#            p.SetFillColor(ROOT.kRed)
#            p.SetLineColor(ROOT.kRed)
#            pads[1].cd()
#            p.Draw("L SAME")

#    if cont_higgsh :
#        for p in cont_higgsh:
#            p.SetLineWidth(2)
#            p.SetLineColor(ROOT.kRed)
#            p.SetLineStyle(7)
#            pads[1].cd()
#            p.Draw("L SAME")


#Set some common scenario labels
scenario_label=args.scenario
if args.scenario == "mhmax":
    scenario_label="m_{h}^{max} scenario"
if args.scenario == "mhmodp":
    scenario_label="m_{h}^{mod+} scenario"
if args.scenario == "mhmodm":
    scenario_label="m_{h}^{mod-} scenario"
if args.scenario == "low-tb-high":
    scenario_label="low tan#beta scenario"
if args.scenario == "hMSSM":
    scenario_label="hMSSM scenario"


pads[0].cd()
legend = plot.PositionedLegend(0.5,0.9,2,0.03)
legend.SetNColumns(2)
legend.SetFillStyle(1001)
legend.SetTextSize(0.15)
legend.SetTextFont(62)
legend.SetHeader("95% CL Excluded:")
# Stupid hack to get legend entry looking correct
if cont_obs[0] and not args.expected_only:
    alt_cont_obs = cont_obs[0].Clone()
    alt_cont_obs.SetLineColor(ROOT.kWhite)
    legend.AddEntry(alt_cont_obs,"Observed", "F")
if cont_minus1sigma[0] : legend.AddEntry(cont_minus1sigma[0], "#pm 1#sigma Expected", "F")
if cont_exp[0] : legend.AddEntry(cont_exp[0],"Expected", "L")
if cont_minus2sigma[0] : legend.AddEntry(cont_minus2sigma[0], "#pm 2#sigma Expected", "F")
legend.Draw("same")

# ROOT is just the worst - ARC requested the observed symbol in the legend be changed to this
if(cont_obs[0]) :
    legline = ROOT.TLine(605, 13, 680, 13)
    legline.SetLineWidth(3)
    legline.SetLineColor(ROOT.kBlack)
    legline.DrawLineNDC(legend.GetX1()+0.0106, legend.GetY2()-0.36, legend.GetX1()+0.0516, legend.GetY2()-0.36)

if args.custom_y_range : axis.GetYaxis().SetRangeUser(float(args.y_axis_min), float(args.y_axis_max))
axis.GetXaxis().SetTitle("m_{A} (GeV)")
if args.custom_x_range : axis.GetXaxis().SetRangeUser(float(args.x_axis_min), float(args.x_axis_max))
plot.DrawCMSLogo(pads[1], 'Combine Harvester', scenario_label, 11, 0.045, 0.035, 1.2)
plot.DrawTitle(pads[1], args.lumi_label, 3);
plot.FixOverlay()
c1.SaveAs(args.ana_label+"_"+args.scenario+".pdf")
c1.SaveAs(args.ana_label+"_"+args.scenario+".png")
c1.SaveAs(args.ana_label+"_"+args.scenario+".C")

