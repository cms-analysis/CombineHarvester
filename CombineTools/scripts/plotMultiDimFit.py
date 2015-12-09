import CombineHarvester.CombineTools.plotting as plot 
import ROOT
import math
import argparse
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f', help='named input files')
args = parser.parse_args()

ROOT.gROOT.ProcessLine(
    "struct staff_t {\
    Float_t quantileExpected;\
    Float_t mh;\
    Double_t limit;\
    }" )

graph = ROOT.TGraph2D()
xvals = [] #ggH
yvals = [] #bbH
zvals = []

file = ROOT.TFile(args.files, 'r')
tree = file.Get('limit')
for evt in tree:
#    skip=0
#    if (float(evt.deltaNLL) in zvals): # Avoid inserting the same point twice
#        if (float(evt.r_ggH) == xvals[zvals.index(float(evt.deltaNLL))]) and (float(evt.r_bbH) == yvals[zvals.index(float(evt.deltaNLL))]):
#            print "Found duplicate point at (ggH,bbH) = ("+str(xvals[zvals.index(float(evt.deltaNLL))])+","+str(yvals[zvals.index(float(evt.deltaNLL))])+")"
#            continue
#        else:
#            for i in xrange(len(zvals)):
#                if (float(evt.r_ggH) == xvals[i]) and (float(evt.r_bbH) == yvals[i]):
#                    print "Found duplicate point at (ggH,bbH) = ("+str(xvals[i])+","+str(yvals[i])+")"
#                    skip=1
#                    break
#    if (skip==1): continue
    xvals.append(float(evt.r_ggH))
    yvals.append(float(evt.r_bbH))
    zvals.append(float(evt.deltaNLL))
graph = ROOT.TGraph2D(len(zvals), array('d', xvals), array('d', yvals), array('d', zvals))
fout = ROOT.TFile('multidimfit.root', 'RECREATE')
fout.WriteTObject(graph, 'Graph')
#graph.SaveAs("graph.root")

ggH_list=[]
bbH_list=[]
for i in xrange(graph.GetN()) :
    ggH_list.append(float(graph.GetX()[i]))
    bbH_list.append(float(graph.GetY()[i]))
ggH_list = sorted(set(ggH_list))
bbH_list = sorted(set(bbH_list))
ggH_bins=len(ggH_list)
bbH_bins=len(bbH_list)
print "r_ggH_list: ", ggH_list, "Total number: ", ggH_bins 
print "r_bbH_list: ", bbH_list, "Total number: ", bbH_bins

#Create canvas and TH2D for each component
plot.ModTDRStyle(width=600, l=0.12)
#Slightly thicker frame to ensure contour edges dont overlay the axis
ROOT.gStyle.SetFrameLineWidth(3)
c1=ROOT.TCanvas()
axis = plot.makeVarBinHist2D('hist2d', ggH_list, bbH_list)
axis.GetXaxis().SetTitle("#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]")
axis.GetYaxis().SetTitle("#sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]")
#Create two pads, one is just for the Legend
pad1 = ROOT.TPad("pad1","pad1",0,0.5,1,1)
pad1.SetFillStyle(4000)
pad1.Draw()
pad2 = ROOT.TPad("pad2","pad2",0,0,1,1)
pad2.SetFillStyle(4000)
pad2.Draw()
pads=[pad1,pad2]
pads[1].cd()

bfit = plot.bestFit(tree, "r_ggH", "r_bbH", "")
#Note the binning of the TH2D for the interpolation should ~ match the initial input grid
#Could in future implement variable binning here
h2d = plot.treeToHist2D(tree, "r_ggH", "r_bbH", "h2d", "", ggH_list[0], ggH_list[-1], bbH_list[0], bbH_list[-1], ggH_bins-1, bbH_bins-1)
#h2d = plot.makeVarBinHist2D("h2d", ggH_list, bbH_list)
#plot.fillTH2(h2d, graph)
#h2d.SaveAs("heatmap.root")
axis.Draw()

cont_1sigma = plot.contourFromTH2(h2d, 2.30, 20) #0.68
cont_2sigma = plot.contourFromTH2(h2d, 5.99, 20) #0.95

for i, p in enumerate(cont_2sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-10)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    p.Draw("CONT SAME")

for i, p in enumerate(cont_1sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-8)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")
    p.Draw("CONT SAME")

bfit.Draw("P SAME")

scenario_label="Multi-dimensional Fit"

pads[0].cd()
legend = ROOT.TLegend(0.65, 0.35, 1.05, 0.85, '', 'NBNDC')
legend.SetNColumns(1)
legend.SetFillStyle(1001)
legend.SetTextSize(0.08)
legend.SetTextFont(62)

hmass=""
if (args.files.find(".mH") != -1):
    hmass = args.files[args.files.find(".mH")+3:args.files.find(".root")]
    legend.SetHeader("m_{#phi} = "+hmass+" GeV")
if cont_1sigma[0] : legend.AddEntry(cont_1sigma[0], "68% CL", "F")
if cont_2sigma[0] : legend.AddEntry(cont_2sigma[0], "95% CL", "F")
legend.AddEntry(bfit, "Best fit", "P")
legend.Draw("same")

plot.DrawCMSLogo(pads[1], 'Combine Harvester', scenario_label, 11, 0.045, 0.035, 1.2)
plot.DrawTitle(pads[1], '19.7 fb^{-1} (8 TeV)', 3);
plot.FixOverlay()
if (hmass == ""):
    c1.SaveAs("mssm_multidimfit.pdf")
    c1.SaveAs("mssm_multidimfit.png")
else:
    c1.SaveAs("mssm_multidimfit_mH"+hmass+".pdf")
    c1.SaveAs("mssm_multidimfit_mH"+hmass+".png")
