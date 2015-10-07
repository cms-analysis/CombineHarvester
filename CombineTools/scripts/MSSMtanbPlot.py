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

def higgsConstraint(model, higgstype) :
    if model=="low-tb-high":
        massstep=10
        masslow=150
        masshigh=500
        nmass=int(((masshigh-masslow)/massstep-1))
        tanblow=0.5
        tanbhigh=9.5
        ntanb=int(((tanbhigh-tanblow)*10-1))

    higgsBand=ROOT.TH2D("higgsBand", "higgsBand", nmass, masslow, masshigh, ntanb, tanblow, tanbhigh)
    for mass in range (masslow, masshigh+1, massstep):
        myfile = open("../../HiggsAnalysis/HiggsToTauTau/data/Higgs125/"+model+"/higgs_"+str(mass)+".dat", 'r')
        for line in myfile:
            tanb = (line.split())[0]
            mh = float((line.split())[1])
            mH = float((line.split())[3])
            if higgstype=="h" :
                 higgsBand.SetBinContent(higgsBand.GetXaxis().FindBin(mass), higgsBand.GetYaxis().FindBin(tanb), mh);
            elif higgstype=="H" :
                higgsBand.SetBinContent(higgsBand.GetXaxis().FindBin(mass), higgsBand.GetYaxis().FindBin(tanb), mH);
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
parser.add_argument('--verbosity', '-v', help='verbosity')
parser.add_argument('--scenario', '-s', help='scenario for plot label e.g. [mhmax,mhmodp,mhmodm,low-tb-high]')
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
for f in infiles:
    if plot.TFileIsGood(f) :
        # Extract the relevant values from the file. This implementation is lifted from HiggsAnalysis/HiggsToTauTau/scripts/extractSignificanceStats.py
        file = ROOT.TFile(f, 'r')
        if file.GetListOfKeys().Contains("limit") :
            #First find the mA and tanb value indicated by the filename
            mA = plot.ParamFromFilename(f, "mA")
            tanb = plot.ParamFromFilename(f, "tanb")
            tree = file.Get("limit")
            staff = ROOT.staff_t()
            tree.SetBranchAddress("quantileExpected",ROOT.AddressOf(staff,"quantileExpected"))
            tree.SetBranchAddress("mh",ROOT.AddressOf(staff,"mh"))
            tree.SetBranchAddress("limit",ROOT.AddressOf(staff,"limit"))
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
                    #print minus2sigma
                if abs(staff.quantileExpected-0.160) < 0.01  :
                    minus1sigma=staff.limit
                    #print minus1sigma
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

#Create canvas and TH2D for each component
#Note the binning of the TH2D for the interpolation should match the initial input grid
plot.ModTDRStyle(width=800, l=0.13)
#plot.SetTDRStyle()
c1=ROOT.TCanvas()
axis = makeHist('hist2d', 16, 45, graph_exp)
axis.GetYaxis().SetTitle("tan#beta")
axis.GetXaxis().SetTitle("m_{A}")
pads = plot.OnePad()
pads[0].Draw()
h_exp = makeHist("h_exp", 16, 45, graph_exp)
h_obs = makeHist("h_obs", 16, 45, graph_obs)
h_minus1sigma = makeHist("h_minus1sigma", 16, 45, graph_minus1sigma)
h_plus1sigma = makeHist("h_plus1sigma", 16, 45, graph_plus1sigma)
h_minus2sigma = makeHist("h_minus2sigma", 16, 45, graph_minus2sigma)
h_plus2sigma = makeHist("h_plus2sigma", 16, 45, graph_plus2sigma)
fillTH2(h_exp, graph_exp)
fillTH2(h_obs, graph_obs)
fillTH2(h_minus1sigma, graph_minus1sigma)
fillTH2(h_plus1sigma, graph_plus1sigma)
fillTH2(h_minus2sigma, graph_minus2sigma)
fillTH2(h_plus2sigma, graph_plus2sigma)
axis.Draw()
#Possibility to draw CLs heat map, would be a useful option, using e.g.
#h_obs.Draw("colzsame")


#Extract exclusion contours from the TH2Ds
#cont_exp = plot.contourFromTH2(h_exp, 1.0, 20)
#cont_obs = plot.contourFromTH2(h_obs, 1.0, 5)
#cont_minus1sigma = plot.contourFromTH2(h_minus1sigma, 1.0, 20)
#cont_plus1sigma = plot.contourFromTH2(h_plus1sigma, 1.0, 20)
#cont_minus2sigma = plot.contourFromTH2(h_minus2sigma, 1.0, 20)
#cont_plus2sigma = plot.contourFromTH2(h_plus2sigma, 1.0, 20)
cont_exp = plot.contourFromTH2(h_exp, 0.05, 20)
cont_obs = plot.contourFromTH2(h_obs, 0.05, 5)
cont_minus1sigma = plot.contourFromTH2(h_minus1sigma, 0.05, 20)
cont_plus1sigma = plot.contourFromTH2(h_plus1sigma, 0.05, 20)
cont_minus2sigma = plot.contourFromTH2(h_minus2sigma, 0.05, 20)
cont_plus2sigma = plot.contourFromTH2(h_plus2sigma, 0.05, 20)

#if args.scenario == "low-tb-high":
#    plane_higgsHBand = higgsConstraint(args.scenario, "H")
#  plane_higgsBands.push_back(plane_higgsHBand);
#  //lower edge entry 2
#    cont_higgsHlow = plot.contourFromTH2(plane_higgsHBand, 260, 20)
#  STestFunctor higgsHband0 = std::for_each( iter_higgsHlow.Begin(), TIter::End(), STestFunctor() );
#  for(int i=0; i<higgsHband0.sum; i++) {gr_higgsHlow.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[1], 260, 20, false, 200))->At(i));}
#  gr_higgsBands.push_back(gr_higgsHlow);
#  //upper edge entry 3
#    cont_higgsHhigh = plot.contourFromTH2(plane_higgsHBand, 350, 20)
#  STestFunctor higgsHband1 = std::for_each( iter_higgsHhigh.Begin(), TIter::End(), STestFunctor() );
#  for(int i=0; i<higgsHband1.sum; i++) {gr_higgsHhigh.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[1], 350, 20, false, 200))->At(i));} 
#  gr_higgsBands.push_back(gr_higgsHhigh);
#}

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
    p.SetFillColor(CreateTransparentColor(ROOT.kAzure+6,0.5))
    pads[0].cd()
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

#Set some common scenario labels
scenario_label=""
if args.scenario == "mhmax":
    scenario_label="m_{h}^{max} scenario"
if args.scenario == "mhmodp":
    scenario_label="m_{h}^{mod+} scenario"
if args.scenario == "mhmodm":
    scenario_label="m_{h}^{mod-} scenario"
if args.scenario == "low-tb-high":
    scenario_label="low tan#beta scenario"


plot.DrawCMSLogo(pads[0], 'Combine Harvester', scenario_label, 11, 0.045, 0.035, 1.2)
plot.FixOverlay()
c1.SaveAs("mssm_"+args.scenario+".pdf")
c1.SaveAs("mssm_"+args.scenario+".png")

