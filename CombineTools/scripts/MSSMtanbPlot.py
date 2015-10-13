import CombineHarvester.CombineTools.plotting as plot 
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

# Should find another location for this function, and make more general. Ideally use the model files rather than the .dat files too
def higgsConstraint(model, higgstype) :
    higgsBand=ROOT.TGraph2D()
    masslow = 150
    masshigh = 500
    massstep = 10
    n=0
    for mass in range (masslow, masshigh, massstep):
        myfile = open("../../HiggsAnalysis/HiggsToTauTau/data/Higgs125/"+model+"/higgs_"+str(mass)+".dat", 'r')
        for line in myfile:
            tanb = (line.split())[0]
            mh = float((line.split())[1])
            mH = float((line.split())[3])
            if higgstype=="h" :
                 higgsBand.SetPoint(n, mass, float(tanb), mh)
            elif higgstype=="H" :
                 higgsBand.SetPoint(n, mass, float(tanb), mH)
            n=n+1 
        myfile.close()    
    return higgsBand

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
parser.add_argument('--files', '-f', help='named input files')
parser.add_argument('--scenario', '-s', help='scenario for plot label e.g. [mhmax,mhmodp,mhmodm,low-tb-high]')
parser.add_argument('--custom_y_range', help='Fix y axis range', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=0.0)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=60.0)
parser.add_argument('--custom_x_range', help='Fix x axis range', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=90.0)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=1000.0)
parser.add_argument('--verbosity', '-v', help='verbosity', default=0)
args = parser.parse_args()

myfile = open(args.files, 'r')
filestring = ''
for line in myfile:
    filestring += line
 
infiles = filestring.split(',')

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
#Store the mA and tanb list being used for the interpolation
tanb_list=[]
mA_list=[]
for f in infiles:
    if plot.TFileIsGood(f) :
        # Extract the relevant values from the file. This implementation is lifted from HiggsAnalysis/HiggsToTauTau/scripts/extractSignificanceStats.py
        file = ROOT.TFile(f, 'r')
        if file.GetListOfKeys().Contains("limit") :
            #First find the mA and tanb value indicated by the filename
            mA = plot.ParamFromFilename(f, "mA")
            tanb = plot.ParamFromFilename(f, "tanb")
            mA_list.append(mA)
            tanb_list.append(tanb)
            tree = file.Get("limit")
            staff = ROOT.staff_t()
            tree.SetBranchAddress("quantileExpected",ROOT.AddressOf(staff,"quantileExpected"))
            tree.SetBranchAddress("mh",ROOT.AddressOf(staff,"mh"))
            tree.SetBranchAddress("limit",ROOT.AddressOf(staff,"limit"))
            #Set not excluded by default in case a fit fails
            minus2sigma=1000
            minus1sigma=1000
            exp=1000
            plus1sigma=1000
            plus2sigma=1000
            obs=1000
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
        ROOT.TFile.Close(file)

tanb_list = sorted(set(tanb_list))
mA_list = sorted(set(mA_list))
tanb_bins=len(tanb_list)
mA_bins=len(mA_list)
if int(args.verbosity) > 0 :
    print "mA_list: ", mA_list, "Total number: ", mA_bins 
    print "tanb_list: ", tanb_list, "Total number: ", tanb_bins

#Create canvas and TH2D for each component
plot.ModTDRStyle(width=600, l=0.12)
#Slightly thicker frame to ensure contour edges dont overlay the axis
ROOT.gStyle.SetFrameLineWidth(2)
c1=ROOT.TCanvas()
axis = makeHist('hist2d', mA_bins, tanb_bins, graph_exp)
axis.GetYaxis().SetTitle("tan#beta")
if args.custom_y_range : axis.GetYaxis().SetRangeUser(float(args.y_axis_min), float(args.y_axis_max))
axis.GetXaxis().SetTitle("m_{A} (GeV)")
if args.custom_x_range : axis.GetXaxis().SetRangeUser(float(args.x_axis_min), float(args.x_axis_max))
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
h_exp = makeHist("h_exp", mA_bins, tanb_bins, graph_exp)
h_obs = makeHist("h_obs", mA_bins, tanb_bins, graph_obs)
h_minus1sigma = makeHist("h_minus1sigma", mA_bins, tanb_bins, graph_minus1sigma)
h_plus1sigma = makeHist("h_plus1sigma", mA_bins, tanb_bins, graph_plus1sigma)
h_minus2sigma = makeHist("h_minus2sigma", mA_bins, tanb_bins, graph_minus2sigma)
h_plus2sigma = makeHist("h_plus2sigma", mA_bins, tanb_bins, graph_plus2sigma)
fillTH2(h_exp, graph_exp)
fillTH2(h_obs, graph_obs)
fillTH2(h_minus1sigma, graph_minus1sigma)
fillTH2(h_plus1sigma, graph_plus1sigma)
fillTH2(h_minus2sigma, graph_minus2sigma)
fillTH2(h_plus2sigma, graph_plus2sigma)
axis.Draw()
#Possibility to draw CLs heat map, would be a useful option, using e.g.
#h_obs.Draw("colzsame")


#Extract exclusion contours from the TH2Ds, use threshold 1.0 for limit and 0.05 for CLs
threshold=0.05
#threshold=1
cont_exp = plot.contourFromTH2(h_exp, threshold, 20)
cont_obs = plot.contourFromTH2(h_obs, threshold, 5)
cont_minus1sigma = plot.contourFromTH2(h_minus1sigma, threshold, 20)
cont_plus1sigma = plot.contourFromTH2(h_plus1sigma, threshold, 20)
cont_minus2sigma = plot.contourFromTH2(h_minus2sigma, threshold, 20)
cont_plus2sigma = plot.contourFromTH2(h_plus2sigma, threshold, 20)


if args.scenario == "low-tb-high":
    graph_higgshBand = higgsConstraint(args.scenario, "h")
    plane_higgshBand = makeHist('plane_higgshBand', 36, 91, graph_higgshBand)
    fillTH2(plane_higgshBand, graph_higgshBand)
    plane_higgshBand.SaveAs("plane_higgshBand.C")
    cont_higgshlow = plot.contourFromTH2(plane_higgshBand, 122, 5)
    cont_higgshhigh = plot.contourFromTH2(plane_higgshBand, 128, 5)
    cont_higgsh = plot.contourFromTH2(plane_higgshBand, 125, 5)

for p in cont_minus2sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")

for p in cont_minus1sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+2)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")

for p in cont_plus1sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kGray+1)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")

for p in cont_plus2sigma :
    p.SetLineColor(0)
    p.SetFillColor(ROOT.kWhite)
    p.SetFillStyle(1001)
    pads[1].cd()
    p.Draw("F SAME")

for p in cont_exp :
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetLineStyle(2)
    p.SetFillColor(100)
    pads[1].cd()
    p.Draw("L SAME")

for p in cont_obs :
    p.SetLineColor(ROOT.kBlack)
    p.SetLineWidth(2)
    p.SetMarkerStyle(20)
    p.SetMarkerSize(1.0)
    p.SetMarkerColor(ROOT.kBlack)
    p.SetFillStyle(1001)
    p.SetFillColor(CreateTransparentColor(ROOT.kAzure+6,0.5))
    pads[1].cd()
    p.Draw("F SAME")
    p.Draw("L SAME")

#for p in cont_higgsHlow:      
#    print "higgsHlow"
#    p.SetLineWidth(9902)
#    p.SetFillStyle(1001)
#    p.SetFillColor(ROOT.kGreen) 
#    p.SetLineColor(ROOT.kGreen+3)
#    p.SetLineStyle(3)
    #p.Draw("L SAME")
    #p.Draw("F SAME")

#for p in cont_higgsHhigh:      
#    print "higgsHhigh"
#    p.SetLineWidth(-9902)
#    p.SetFillStyle(1001)
#    p.SetFillColor(ROOT.kGreen) 
#    p.SetLineColor(ROOT.kGreen+3)
#    p.SetLineStyle(3)
    #p.Draw("L SAME")
    #p.Draw("F SAME")

for p in cont_higgshlow:
    p.SetLineWidth(-402)
    p.SetFillStyle(3005)
    p.SetFillColor(ROOT.kRed)
    p.SetLineColor(ROOT.kRed)
    pads[1].cd()
    p.Draw("L SAME")

for p in cont_higgshlow:
    p.SetLineWidth(402)
    p.SetFillStyle(3005)
    p.SetFillColor(ROOT.kRed)
    p.SetLineColor(ROOT.kRed)
    pads[1].cd()
    p.Draw("L SAME")

for p in cont_higgsh:
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kRed)
    p.SetLineStyle(7)
    pads[1].cd()
    p.Draw("L SAME")


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
if cont_obs[0] : 
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

plot.DrawCMSLogo(pads[1], 'Combine Harvester', scenario_label, 11, 0.045, 0.035, 1.2)
plot.DrawTitle(pads[1], '19.7 fb^{-1} (8 TeV)', 3);
plot.FixOverlay()
c1.SaveAs("mssm_"+args.scenario+".pdf")
c1.SaveAs("mssm_"+args.scenario+".png")

