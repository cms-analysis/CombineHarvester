import plotting as plot 
import ROOT
import math
import argparse

def fillTH2(hist2d, graph):
    for x in xrange(1, hist2d.GetNbinsX()+1):
        for y in xrange(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            val = graph.Interpolate(xc, yc)
            hist2d.SetBinContent(x, y, val)

def makeHist(name, xbins, ybins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(xbins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(ybins) - 1.)) - 1E-5
    hist = ROOT.TH2F(name, '', xbins, graph2d.GetXmin()-binw_x, graph2d.GetXmax()+binw_x, ybins, graph2d.GetYmin()-binw_y, graph2d.GetYmax()+binw_y)
    return hist

ROOT.gROOT.SetBatch(ROOT.kTRUE)
parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f', help='named input files')
parser.add_argument('--verbosity', '-v', help='verbosity')
args = parser.parse_args()

infiles = args.files.split(',')
goodfiles = [f for f in infiles if plot.TFileIsGood(f)]

ROOT.gROOT.ProcessLine(
    "struct staff_t {\
    Float_t quantileExpected;\
    Float_t mh;\
    Double_t limit;\
    }" )

n=0
graph_exp = ROOT.TGraph2D()
graph_minus2sigma = ROOT.TGraph2D()
graph_minus1sigma = ROOT.TGraph2D()
graph_plus2sigma = ROOT.TGraph2D()
graph_plus1sigma = ROOT.TGraph2D()
graph_obs = ROOT.TGraph2D()
for f in goodfiles:
    #First find the mA and tanb value indicated by the filename
    mA = plot.ParamFromFilename(f, "mA")
    tanb = plot.ParamFromFilename(f, "tanb")
    # Extract the relevant values from the file. This implementation is lifted from HiggsAnalysis/HiggsToTauTau/scripts/extractSignificanceStats.py
    file = ROOT.TFile(f, 'r')
    tree = file.Get("limit")
    staff = ROOT.staff_t()
    tree.SetBranchAddress("quantileExpected",ROOT.AddressOf(staff,"quantileExpected"))
    tree.SetBranchAddress("mh",ROOT.AddressOf(staff,"mh"))
    tree.SetBranchAddress("limit",ROOT.AddressOf(staff,"limit"))
    for i in range(tree.GetEntries()) :
        tree.GetEntry(i);
        if abs(staff.quantileExpected-0.025) < 0.01  :
            minus2sigma=staff.limit
        if abs(staff.quantileExpected-0.160) < 0.01  :
            minus1sigma=staff.limit
        if abs(staff.quantileExpected-0.500) < 0.01  :
            exp=staff.limit
        if abs(staff.quantileExpected-0.840) < 0.01  :
            plus1sigma=staff.limit
        if abs(staff.quantileExpected-0.975) < 0.01  :
            plus2sigma=staff.limit
        if abs(staff.quantileExpected+1.000) < 0.01  :
            obs=staff.limit           
    if int(args.verbosity) > 0 :
        print "Tested points: ", mA, tanb, minus2sigma, minus1sigma, exp, plus1sigma, plus2sigma, obs
    #Fill TGraphs with the values of each CLs
    graph_exp.SetPoint(n, mA, tanb, exp)
    graph_minus2sigma.SetPoint(n, mA, tanb, minus2sigma)
    graph_minus1sigma.SetPoint(n, mA, tanb, minus1sigma)
    graph_plus2sigma.SetPoint(n, mA, tanb, plus2sigma)
    graph_plus1sigma.SetPoint(n, mA, tanb, plus1sigma)
    graph_obs.SetPoint(n, mA, tanb, obs)
    n=n+1

#Create canvas and TH2D for each component
plot.ModTDRStyle(width=800, l=0.13)
c1=ROOT.TCanvas()
axis = makeHist('hist2d', 16, 60, graph_exp)
axis.GetYaxis().SetTitle("tan#beta")
axis.GetXaxis().SetTitle("m_{A}")
pads = plot.OnePad()
pads[0].Draw()
h_exp = makeHist("h_exp", 16, 60, graph_exp)
h_obs = makeHist("h_obs", 16, 60, graph_obs)
h_minus1sigma = makeHist("h_minus1sigma", 16, 60, graph_minus1sigma)
h_plus1sigma = makeHist("h_plus1sigma", 16, 60, graph_plus1sigma)
h_minus2sigma = makeHist("h_minus2sigma", 16, 60, graph_minus2sigma)
h_plus2sigma = makeHist("h_plus2sigma", 16, 60, graph_plus2sigma)
fillTH2(h_exp, graph_exp)
fillTH2(h_obs, graph_obs)
fillTH2(h_minus1sigma, graph_minus1sigma)
fillTH2(h_plus1sigma, graph_plus1sigma)
fillTH2(h_minus2sigma, graph_minus2sigma)
fillTH2(h_plus2sigma, graph_plus2sigma)
axis.Draw()
#Possibility to draw CLs heat map, would be a useful option, using e.g.
#h_exp.Draw("colzsame")


#Extract exclusion contours from the TH2Ds
cont_exp = plot.contourFromTH2(h_exp, 1.0, 20)
cont_obs = plot.contourFromTH2(h_obs, 1.0, 20)
cont_minus1sigma = plot.contourFromTH2(h_minus1sigma, 1.0, 20)
cont_plus1sigma = plot.contourFromTH2(h_plus1sigma, 1.0, 20)
cont_minus2sigma = plot.contourFromTH2(h_minus2sigma, 1.0, 20)
cont_plus2sigma = plot.contourFromTH2(h_plus2sigma, 1.0, 20)

for p in cont_minus2sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[0].cd()
    p.Draw("F SAME")

for p in cont_minus1sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+2)
    p.SetFillStyle(1001)
    pads[0].cd()
    p.Draw("F SAME")

for p in cont_plus1sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[0].cd()
    p.Draw("F SAME")

for p in cont_plus2sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kWhite)
    p.SetFillStyle(1001)
    pads[0].cd()
    p.Draw("F SAME")

for p in cont_exp :
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetLineStyle(2)
    p.SetFillColor(100)
    pads[0].cd()
    p.Draw("L SAME")

for p in cont_obs :
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetMarkerStyle(20)
    p.SetMarkerSize(1.0)
    p.SetMarkerColor(ROOT.kBlack)
    p.SetFillStyle(1001)
    #p.SetFillColor(plot.CreateTransparentColor(ROOT.kAzure-4,0.5))
    #p.SetFillColor(ROOT.TColor(1501, 0.463, 0.867, 0.957).GetNumber())
    p.SetFillColor(ROOT.kAzure+6)
    pads[0].cd()
    p.Draw("F SAME")
    p.Draw("L SAME")

plot.DrawCMSLogo(pads[0], 'Combine Harvester', 'm_{h}^{max} scenario', 11, 0.045, 0.035, 1.2)
plot.FixOverlay()
c1.SaveAs("mssm_mhmax.png")

