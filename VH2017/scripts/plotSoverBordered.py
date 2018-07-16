#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot
import ROOT
import math
import argparse
import json
import sys
import os
import fnmatch
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

def createAxisHists(n,src,xmin=0,xmax=499):
  result = []
  for i in range(0,n):
    res = src.Clone()
    res.Reset()
    res.SetTitle("")
    res.SetName("axis%(i)d"%vars())
    res.SetAxisRange(xmin,xmax)
    res.SetStats(0)
    result.append(res)
  return result

def getHistogram(fname, histname, dirname='', postfitmode='prefit', allowEmpty=False, logx=False):
  outname = fname.GetName()
  for key in fname.GetListOfKeys():
    histo = fname.Get(key.GetName())
    dircheck = False
    if dirname == '' : dircheck=True
    elif dirname in key.GetName(): dircheck=True
    if isinstance(histo,ROOT.TH1F) and key.GetName()==histname:
      if logx:
        bin_width = histo.GetBinWidth(1)
        xbins = []
        xbins.append(bin_width - 1)
        axis = histo.GetXaxis()
        for i in range(1,histo.GetNbinsX()+1):
         xbins.append(axis.GetBinUpEdge(i))
        rethist = ROOT.TH1F(histname,histname,histo.GetNbinsX(),array('d',xbins))
        rethist.SetBinContent(1,histo.GetBinContent(1)*(histo.GetBinWidth(1)-(bin_width - 1))/(histo.GetBinWidth(1)))
        rethist.SetBinError(1,histo.GetBinError(1)*(histo.GetBinWidth(1)-(bin_width - 1))/(histo.GetBinWidth(1)))
        for i in range(2,histo.GetNbinsX()+1):
          rethist.SetBinContent(i,histo.GetBinContent(i))
          rethist.SetBinError(i,histo.GetBinError(i))
        histo = rethist
      return [histo,outname]
    elif isinstance(histo,ROOT.TDirectory) and postfitmode in key.GetName() and dircheck:
      return getHistogram(histo,histname, allowEmpty=allowEmpty, logx=logx)
  print 'Failed to find %(postfitmode)s histogram with name %(histname)s in file %(fname)s '%vars()
  if allowEmpty:
    return [ROOT.TH1F('empty', '', 1, 0, 1), outname]
  else:
    return None

  

plot.ModTDRStyle(r=0.04, l=0.14)
ROOT.gStyle.SetHatchesLineWidth(1)
ROOT.gStyle.SetHatchesSpacing(0.2)


parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',help='Input file if shape file has already been created')
#General plotting options
parser.add_argument('--ratio', default=False,action='store_true',help='Draw ratio plot')
parser.add_argument('--custom_x_range', help='Fix x axis range', action='store_true', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=-2.)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=0.)
parser.add_argument('--custom_y_range', help='Fix y axis range', action='store_true', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=1)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=100000.0)
parser.add_argument('--log_y', action='store_true',help='Use log for y axis')
parser.add_argument('--log_x', action='store_true',help='Use log for x axis')
parser.add_argument('--extra_pad', help='Fraction of extra whitespace at top of plot',default=0.0)
parser.add_argument('--outname',default='sbordered',help='Output plot name')
parser.add_argument('--ratio_range',  help='y-axis range for ratio plot in format MIN,MAX', default="0.4,1.6")
parser.add_argument('--x_title', default='log_{10}(S/B)',help='Title for the x-axis')
parser.add_argument('--y_title', default='Entries',help='Title for the y-axis')
parser.add_argument('--lumi', default='41.3 fb^{-1} (13 TeV)',help='Lumi label')


args = parser.parse_args()
extra_pad = float(args.extra_pad)
custom_x_range = args.custom_x_range
custom_y_range = args.custom_y_range
x_axis_min = float(args.x_axis_min)
x_axis_max = float(args.x_axis_max)
y_axis_min = float(args.y_axis_min)
y_axis_max = float(args.y_axis_max)
log_y=args.log_y
log_x=args.log_x

histo_file = ROOT.TFile(args.file)


bkghist = getHistogram(histo_file,'TotalBkg','', 'postfit', logx=log_x)[0]
splusbhist = getHistogram(histo_file,'TotalProcs','','postfit',logx=log_x)[0]
total_datahist = getHistogram(histo_file,"data_obs",'','postfit', logx=log_x)[0]
sighist = getHistogram(histo_file,'TotalSig', '', 'postfit',logx=log_x)[0]
sighist_forratio = sighist.Clone()
sighist_forratio.SetName("sighist_forratio")

bkghist.SetFillColor(ROOT.kGray+1)
bkghist.SetLineColor(ROOT.kBlack)
bkghist.SetMarkerSize(0)

sighist.SetFillColor(ROOT.kRed)
sighist.SetLineColor(ROOT.kBlack)
sighist.SetMarkerSize(0)

stack = ROOT.THStack("hs","")
stack.Add(bkghist)
stack.Add(sighist)


c2 = ROOT.TCanvas()
c2.cd()
if args.ratio:
  pads=plot.TwoPadSplit(0.29,0.01,0.01)
else:
  pads=plot.OnePad()
pads[0].cd()
if(log_y): pads[0].SetLogy(1)
if(log_x): pads[0].SetLogx(1)
if custom_x_range:
    if x_axis_max > bkghist.GetXaxis().GetXmax(): x_axis_max = bkghist.GetXaxis().GetXmax()
if args.ratio:
  if(log_x): pads[1].SetLogx(1)
  axish = createAxisHists(2,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()-0.01)
  axish[1].GetXaxis().SetTitle(args.x_title)
  axish[1].GetYaxis().SetNdivisions(4)
  axish[1].GetYaxis().SetTitle("Obs/Exp")
  #axish[1].GetYaxis().SetTitleSize(0.04)
  #axish[1].GetYaxis().SetLabelSize(0.04)
  #axish[1].GetYaxis().SetTitleOffset(1.3)
  #axish[0].GetYaxis().SetTitleSize(0.04)
  #axish[0].GetYaxis().SetLabelSize(0.04)
  #axish[0].GetYaxis().SetTitleOffset(1.3)
  axish[0].GetXaxis().SetTitleSize(0)
  axish[0].GetXaxis().SetLabelSize(0)
  if custom_x_range:
    axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
    axish[1].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
  if custom_y_range:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
    axish[1].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
else:
  axish = createAxisHists(1,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()-0.01)
#  axish[0].GetYaxis().SetTitleOffset(1.4)
  if custom_x_range:
    axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
  if custom_y_range:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)

axish[0].GetYaxis().SetTitle(args.y_title)
axish[0].GetXaxis().SetTitle(args.x_title)
if not custom_y_range: axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
if not custom_y_range: 
  if(log_y): axish[0].SetMinimum(0.0009)
  else: axish[0].SetMinimum(0)
axish[0].Draw()

#Draw uncertainty band

stack.Draw("histsame")
#splusbhist.SetFillColor(plot.CreateTransparentColor(12,0.4))
splusbhist.SetFillColor(ROOT.kGray)
splusbhist.SetLineColor(0)
splusbhist.SetMarkerSize(0)
splusbhist.SetFillStyle(3994)
splusbhist.DrawCopy("e2same")
total_datahist.SetMarkerStyle(20)
total_datahist.Draw("PSAME")

#Setup legend
legend = plot.PositionedLegend(0.48,0.10,3,0.03)
plot.Set(legend, NColumns=2)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
legend.SetFillColor(0)
#legend.AddEntry(total_datahist,"Observation","PE")
legend.AddEntry(bkghist, "Background", "f")
legend.AddEntry(sighist, "VH(b#bar{b})","f")
legend.AddEntry(splusbhist, "S+B uncertainty","f")

legend.Draw("same")


#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.30)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.lumi, 3)



if args.ratio:
  ratio_bkghist = plot.MakeRatioHist(bkghist,bkghist,True,False)
  ratio_bkghist.SetFillColor(ROOT.kGray)
  ratio_bkghist.SetFillStyle(3944)
  ratio_splusbhist = plot.MakeRatioHist(splusbhist,splusbhist,True,False)
  ratio_splusbhist.SetFillColor(ROOT.kGray)
  ratio_splusbhist.SetFillStyle(3944)
  ratio_datahist = plot.MakeRatioHist(total_datahist,bkghist,True,False)
  ratio_sighist = plot.MakeRatioHist(sighist_forratio,bkghist,True,False)
  ratio_sighist.SetLineColor(ROOT.kRed)
  ratio_sighist.SetMarkerSize(0)
  for i in range(1,ratio_sighist.GetNbinsX()+1):
    ratio_sighist.SetBinContent(i,ratio_sighist.GetBinContent(i)+1)
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(float(args.ratio_range.split(',')[0]))
  axish[1].SetMaximum(float(args.ratio_range.split(',')[1]))
  ratio_bkghist.SetMarkerSize(0)
  ratio_bkghist.DrawCopy("e2same")
  ratio_datahist.Draw("e0same")
  ratio_sighist.Draw("histsame")
  pads[1].RedrawAxis("G")


pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()



c2.SaveAs("sbordered.png")
c2.SaveAs("sbordered.pdf")


