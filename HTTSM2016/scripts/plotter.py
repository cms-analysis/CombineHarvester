#!/usr/bin/env python
import ROOT
import re
from array import array
from collections import OrderedDict
import varCfgPlotter
import argparse
import os

parser = argparse.ArgumentParser(
    "Create pre/post-fit plots for SM HTT")
parser.add_argument(
    "--isLog",
    type=int,
    action="store",
    dest="isLog",
    default=1,
    help="Plot Log Y? (Integers 0, false, 1 true)")
parser.add_argument(
    "--channel",
    action="store",
    dest="channel",
    default="tt",
    help="Which channel to run over? (et, mt, em, tt)")
parser.add_argument(
    "--prefix",
    action="store",
    dest="prefix",
    default="",
    help="Provide prefix for TDirectory holding histograms such as 'prefit_' or postfin_'.  Default is '' and will search in CHANNEL_0jet, CHANNEL_boosted, CHANNEL_VBF")
parser.add_argument(
    "--higgsSF",
    type=int,
    action="store",
    dest="higgsSF",
    default=50,
    help="Provide the Scale Factor for the SM-Higgs signals.  100x is default")
parser.add_argument(
    "--inputFile",
    action="store",
    dest="inputFile",
    help="Provide the relative path to the target input file")
args = parser.parse_args()

channel = args.channel
isLog = args.isLog
prefix = args.prefix
categories = varCfgPlotter.getCategories( channel, prefix )
higgsSF = args.higgsSF
fileName = args.inputFile
if fileName == None :
    fileName = varCfgPlotter.getFile( channel )
assert (fileName != None), "Please provide a file name"

print "\nPlotting for:"
print " -- Channel:",channel
print " -- Plot", "Log" if isLog else "Linear"
print " -- Plotting for categories:"
for cat in categories :
    print "     -- ",cat
print " -- Using Higgs Scale Factor:",higgsSF
print " -- Target file:",fileName,"\n"



file = ROOT.TFile( fileName, "r" )
print file

# Category map for the LaTeX naming of histograms
catMap = {
    "em" : "e#mu",
    "et" : "e#tau_{h}",
    "mt" : "#mu#tau_{h}",
    "tt" : "#tau_{h}#tau_{h}",
}

def add_lumi():
    lowX=0.7
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("2016, 35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.11
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.20
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
	if isLog:
	   output = ROOT.TLegend(0.12, 0.05, 0.92, 0.25, "", "brNDC")
           output.SetNColumns(5)
	else:
           output = ROOT.TLegend(0.55, 0.3, 0.92, 0.75, "", "brNDC")
	   output.SetNColumns(2)
        #output = ROOT.TLegend(0.2, 0.1, 0.47, 0.65, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        #output.SetFillStyle(0)
        output.SetFillColor(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output

# Can use to return all hists in a dir
def get_Keys_Of_Class( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys

binMap = varCfgPlotter.getBinMap()

ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

c=ROOT.TCanvas("canvas","",0,0,1800,1000)
c.cd()


adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

infoMap = varCfgPlotter.getInfoMap( higgsSF, channel )
bkgs = varCfgPlotter.getBackgrounds()
signals = varCfgPlotter.getSignals()


for cat in categories:
    print "Plotting for:",cat
    
    # Get list of the keys to hists in our category directory
    if channel == "tt" :
        histKeys = get_Keys_Of_Class( file, cat, "TH1F" )
    else :
        histKeys = get_Keys_Of_Class( file, cat, "TH1F" )
    
    # Get nominal shapes for all processes
    initHists = {}
    for key in histKeys :
        if "_CMS_" in key.GetName() : continue
        # skip the higgs mass +/-
        if "120" in key.GetName() or "130" in key.GetName() : continue
        initHists[ key.GetName() ] = key.ReadObj()
    
        # to merge later, we need clearly defined under and overflow bins
        #print initHists[ key.GetName() ]
        #initHists[ key.GetName() ].ClearUnderflowAndOverflow()
    

    # Check for a few fundamental histos
    assert (initHists["data_obs"] != None), "Where's your data hist?!"
    assert (initHists["ZTT"] != None), "Where's your ZTT hist?!"
    #for sig in signals :
    #    assert (initHists[sig] != None), "Where's your %s?!" % sig

    
    nBins = initHists["data_obs"].GetXaxis().GetNbins()
    binWidth = initHists["data_obs"].GetBinWidth(1)
    # FIXME, we could look at variable binning, but that ontop of
    # unrolled histograms would be a bit much

    
    # Make the final hists, some initial shapes need to be merged
    hists = {}
    for name, val in infoMap.iteritems() :
        hists[ name ] = ROOT.TH1F( name+cat, val[1], nBins, 0, nBins*binWidth )
        hists[ name ].Sumw2()
        for toAdd in val[0] :
            if not toAdd in initHists :
                print toAdd," not in your file: %s, directory, %s" % (file, cat)
                continue
            hists[ name ].Add( initHists[ toAdd ] )
    
        if name not in signals :
            hists[ name ].SetFillColor(ROOT.TColor.GetColor( val[3] ) )
            hists[ name ].SetLineColor(1)
        
    
    # Set aesthetics
    hists["data_obs"].GetXaxis().SetTitle("")
    hists["data_obs"].GetXaxis().SetTitleSize(0)
    hists["data_obs"].GetXaxis().SetNdivisions(505)
    hists["data_obs"].GetYaxis().SetLabelFont(42)
    hists["data_obs"].GetYaxis().SetLabelOffset(0.01)
    hists["data_obs"].GetYaxis().SetLabelSize(0.06)
    hists["data_obs"].GetYaxis().SetTitleSize(0.075)
    hists["data_obs"].GetYaxis().SetTitleOffset(0.56)
    hists["data_obs"].GetYaxis().SetTickLength(0.012)
    hists["data_obs"].SetTitle("")
    hists["data_obs"].GetYaxis().SetTitle("Events/bin")
    hists["data_obs"].SetMarkerStyle(20)
    hists["data_obs"].SetMarkerSize(2)
    hists["data_obs"].SetLineWidth(2)
    for sig in signals :
        hists[ sig ].SetLineColor(ROOT.TColor.GetColor( infoMap[ sig ][3] ))
        hists[ sig ].SetLineWidth(3)
    
    errorBand=hists["ZTT"].Clone()
    for bkg in bkgs :
        if bkg == "ZTT" : continue
        errorBand.Add(hists[bkg])
    
    # Build our stack
    stack=ROOT.THStack("stack","stack")
    for bkg in bkgs :
        stack.Add( hists[bkg] )
    
    errorBand.SetMarkerSize(0)
    errorBand.SetFillColor(new_idx)
    errorBand.SetFillStyle(3001)
    errorBand.SetLineWidth(1)
    
    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    pad1.Draw()
    pad1.cd()
    pad1.SetFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(10)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.SetLeftMargin(0.10)
    pad1.SetRightMargin(0.05)
    pad1.SetTopMargin(0.122)
    pad1.SetBottomMargin(0.026)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameLineStyle(0)
    pad1.SetFrameLineWidth(3)
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameBorderSize(10)
    if isLog:
        pad1.SetLogy()
    
    hists["data_obs"].GetXaxis().SetLabelSize(0)
    hists["data_obs"].SetMaximum(hists["data_obs"].GetMaximum()*1.35)
    hists["data_obs"].SetMinimum(0.0)
    if isLog:
        hists["data_obs"].SetMaximum(hists["data_obs"].GetMaximum()*5.35)
        hists["data_obs"].SetMinimum(0.01)
    for k in range(1,hists["data_obs"].GetSize()-1):
        s=0.0
        for sig in signals :
            s += hists[sig].GetBinContent(k)
        b=0.0
        for bkg in bkgs :
            b += hists[bkg].GetBinContent(k)
        if (b<0):
            b=0.000001
        #if (10*s/((b+0.09*b*0.09*b)**0.5) > 0.5):
        if (2*s/(0.0000001+s+b)**0.5 > 0.2):
           hists["data_obs"].SetBinContent(k,100000000)
           hists["data_obs"].SetBinError(k,0)
    hists["data_obs"].Draw("ep")
    stack.Draw("histsame")
    errorBand.Draw("e2same")
    for sig in signals :
        hists[ sig ].Scale(higgsSF)
        hists[ sig ].Draw("histsame")
    hists["data_obs"].Draw("epsame")
    
    
    # Add the nice pretty gray lines to deliniate
    # where out higgs_pt / mjj bins start/stop
    line=[]
    label=[]
    nx = binMap[channel][cat]["nx"]
    ny = binMap[channel][cat]["ny"]
    for z in range(1, nx+1):
        if channel == "tt" and (cat == "tt_0jet" or "_tt_1" in cat): continue # tt_0jet not unrolled!
        line.append(ROOT.TLine(z*ny,0,z*ny,hists["data_obs"].GetMaximum()))
        line[z-1].SetLineStyle(3)
        line[z-1].Draw("same")
        posx=0.11+0.85*(z-1)/nx
        label.append(ROOT.TPaveText(posx, 0.73, posx+0.15, 0.73+0.155, "NDC"))
        
        # Label each unrolled bin
        label[z-1].AddText(binMap[channel][cat]["name"]+" > "+str(binMap[channel][cat]["binning"][z-1])+" GeV")
        label[z-1].SetBorderSize(   0 )
        label[z-1].SetFillStyle(    0 )
        label[z-1].SetTextAlign(   12 )
        label[z-1].SetTextSize ( 0.04 )
        label[z-1].SetTextColor(    1 )
        label[z-1].SetTextFont (   42 )
        label[z-1].Draw("same")
    
    
    legend=make_legend()
    for name, val in infoMap.iteritems() :
        legend.AddEntry(hists[name], val[1], val[2])
    legend.AddEntry(errorBand,"Stat. uncertainty","f")
    legend.Draw()
    
    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")
    
    pad1.RedrawAxis()
    
    categ  = ROOT.TPaveText(0.45, 0.865, 0.60, 0.865+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.06 )
    categ.SetTextColor(    1 )
    categ.SetTextFont (   42 )
    if "0jet" in cat or "_1_" in cat: 
        categ.AddText(catMap[channel]+", 0 jet")
    elif "boosted" in cat or "_2_" in cat:
        categ.AddText(catMap[channel]+", Boosted")
    elif "VBF" in cat or "vbf" in cat or "_3_" in cat:
        categ.AddText(catMap[channel]+", VBF")
    categ.Draw("same")
    
    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.35);
    pad2.SetLeftMargin(0.10);
    pad2.SetRightMargin(0.05);
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetFrameLineWidth(3)
    #pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    h1=hists["data_obs"].Clone()
    h1.SetMaximum(1.8)#FIXME(1.5)
    h1.SetMinimum(0.2)#FIXME(0.5)
    h1.SetMarkerStyle(20)
    h3=errorBand.Clone()
    hwoE=errorBand.Clone()
    for iii in range (1,hwoE.GetSize()-2):
      hwoE.SetBinError(iii,0)
    h3.Sumw2()
    h1.Sumw2()
    h1.SetStats(0)
    h1.Divide(hwoE)
    h3.Divide(hwoE)
    h1.GetXaxis().SetTitle("2D bin number")
    if channel == "tt" and (cat == "tt_0jet" or "tt_1" in cat):
       h1.GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTickLength(0.012)
    h1.GetYaxis().SetTitle("Obs./Exp.")
    #h1.GetXaxis().SetNdivisions(505)
    h1.GetYaxis().SetNdivisions(5)
    
    h1.GetXaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleOffset(0.26)
    h1.GetXaxis().SetTitleOffset(1.04)
    h1.GetXaxis().SetLabelSize(0.11)
    h1.GetYaxis().SetLabelSize(0.11)
    h1.GetXaxis().SetTitleFont(42)
    h1.GetYaxis().SetTitleFont(42)
    
    h1.Draw("e0psame")
    h3.Draw("e2same")
    
    line2=[]
    for z in range(1,nx):
        line2.append(ROOT.TLine(z*ny,0.2,z*ny,1.8))
        line2[z-1].SetLineStyle(3)
        line2[z-1].Draw("same")
    
    
    c.cd()
    pad1.Draw()
    
    ROOT.gPad.RedrawAxis()
    
    c.Modified()
    if not os.path.exists( 'plots' ) : os.makedirs( 'plots' )
    if isLog:
       c.SaveAs("plots/unroll_log_"+cat+".pdf")
       c.SaveAs("plots/unroll_log_"+cat+".png")
    else:
       c.SaveAs("plots/unroll_"+cat+".pdf")
       c.SaveAs("plots/unroll_"+cat+".png")
    
    

