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

def signalComp(leg,plots,colour,stacked):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour),('in_stack',stacked)])

def backgroundComp(leg,plots,colour):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour)])

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
  

plot.ModTDRStyle(r=0.04, l=0.14)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',help='Input file if shape file has already been created')
parser.add_argument('--channel',default='',help='Option to specify channel in case it is not obtainable from the shape file name')
parser.add_argument('--file_dir',default='',help='Name of TDirectory inside shape file')
parser.add_argument('--mode',default='prefit',help='Prefit or postfit')
#Blinding options
parser.add_argument('--blind', action='store_true',default=False,help='Blind data in x_blind_min,x_blind_max range')
parser.add_argument('--x_blind_min',default=0,help='Minimum x for manual blinding')
parser.add_argument('--x_blind_max',default=1,help='Maximum x for manual blinding')
parser.add_argument('--empty_bin_error',action='store_true',default=False, help='Draw error bars for empty bins')
#General plotting options
parser.add_argument('--channel_label',default='0-lepton',help='Channel label')
parser.add_argument('--ratio', default=False,action='store_true',help='Draw ratio plot')
parser.add_argument('--custom_x_range', help='Fix x axis range', action='store_true', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=0.0)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=1000.0)
parser.add_argument('--custom_y_range', help='Fix y axis range', action='store_true', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=0.001)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=100.0)
parser.add_argument('--log_y', action='store_true',help='Use log for y axis')
parser.add_argument('--log_x', action='store_true',help='Use log for x axis')
parser.add_argument('--extra_pad', help='Fraction of extra whitespace at top of plot',default=0.0)
parser.add_argument('--outname',default='',help='Optional string for start of output filename')
parser.add_argument('--ratio_range',  help='y-axis range for ratio plot in format MIN,MAX', default="0.7,1.3")
parser.add_argument('--no_signal', action='store_true',help='Do not draw signal')
parser.add_argument('--x_title', default='BDT output',help='Title for the x-axis')
parser.add_argument('--y_title', default='Entries',help='Title for the y-axis')
parser.add_argument('--lumi', default='35.9 fb^{-1} (13 TeV)',help='Lumi label')
parser.add_argument('--cr', default=False, action='store_true', help='Plot CRs? (Important for QCD in 0-lep')


args = parser.parse_args()

channel_label = args.channel_label
file_dir = args.file_dir
blind = args.blind
x_blind_min = args.x_blind_min
x_blind_max = args.x_blind_max
empty_bin_error = args.empty_bin_error
extra_pad = float(args.extra_pad)
custom_x_range = args.custom_x_range
custom_y_range = args.custom_y_range
x_axis_min = float(args.x_axis_min)
x_axis_max = float(args.x_axis_max)
y_axis_min = float(args.y_axis_min)
y_axis_max = float(args.y_axis_max)
mode=args.mode
log_y=args.log_y
log_x=args.log_x

if(args.outname != ''):
  outname=args.outname + '_'
else:
  outname=''

if not args.file:
  print 'Provide a filename'
  sys.exit(1)

print "Using shape file ", args.file, ", with specified subdir name: ", file_dir
shape_file=args.file
shape_file_name=args.file

histo_file = ROOT.TFile(shape_file)

#Store plotting information for different backgrounds 
background_schemes = {'Wen':[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("WHb#bar{b}",["WH_hbb"],634)],
'Wmn':[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("WHb#bar{b}",["WH_hbb"],634)],
'Zee':[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625)],
'Zmm':[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625)],
'Znn':[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625),backgroundComp("WHb#bar{b}",["WH_hbb"],634)]}

if args.cr:
  background_schemes['Znn']=[backgroundComp("Single top",["s_Top"],70),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("QCD",["QCD"],613),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625),backgroundComp("WHb#bar{b}",["WH_hbb"],634)]

#Extract relevant histograms from shape file
[sighist,binname] = getHistogram(histo_file,'TotalSig', file_dir, mode, args.no_signal, log_x)
for i in range(0,sighist.GetNbinsX()):
  if sighist.GetBinContent(i) < y_axis_min: sighist.SetBinContent(i,y_axis_min)
bkghist = getHistogram(histo_file,'TotalBkg',file_dir, mode, logx=log_x)[0]
splusbhist = getHistogram(histo_file,'TotalProcs',file_dir, mode, logx=log_x)[0]

total_datahist = getHistogram(histo_file,"data_obs",file_dir, mode, logx=log_x)[0]
binerror_datahist = total_datahist.Clone()
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)
blind_datahist.SetLineColor(1)

sighist_forratio = sighist.Clone()
sighist_forratio.SetName("sighist_forratio")

#Blinding by hand using requested range, set to 200-4000 by default
if blind:
  for i in range(0,total_datahist.GetNbinsX()):
    low_edge = total_datahist.GetBinLowEdge(i+1)
    high_edge = low_edge+total_datahist.GetBinWidth(i+1)
    if ((low_edge > float(x_blind_min) and low_edge < float(x_blind_max)) or (high_edge > float(x_blind_min) and high_edge<float(x_blind_max))):
      blind_datahist.SetBinContent(i+1,0)
      blind_datahist.SetBinError(i+1,0)

#Set bin errors for empty bins if required:
if empty_bin_error:
  for i in range (1,blind_datahist.GetNbinsX()+1):
    if blind_datahist.GetBinContent(i) == 0:
      blind_datahist.SetBinError(i,1.8)

channel = args.channel

#Create stacked plot for the backgrounds
bkg_histos = []
for i,t in enumerate(background_schemes[channel]):
  plots = t['plot_list']
  h = ROOT.TH1F()
  for j,k in enumerate(plots):
    if h.GetEntries()==0 and getHistogram(histo_file,k, file_dir,mode,logx=log_x) is not None:
      h = getHistogram(histo_file,k, file_dir,mode,logx=log_x)[0]
      h.SetName(k)
    else:
      if getHistogram(histo_file,k, file_dir,mode,logx=log_x) is not None:
        h.Add(getHistogram(histo_file,k, file_dir,mode,logx=log_x)[0])
  if h.GetEntries()!=0:
    h.SetFillColor(t['colour'])
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerSize(0)
    bkg_histos.append(h)

stack = ROOT.THStack("hs","")
for hists in bkg_histos:
  stack.Add(hists)


#Setup style related things
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
ROOT.gStyle.SetHatchesSpacing(0.4)
ROOT.gStyle.SetHatchesLineWidth(1)
bkghist.SetFillColor(12)
bkghist.SetFillStyle(3944)
bkghist.SetLineColor(0)
bkghist.SetMarkerSize(0)
splusbhist.SetFillColor(12)
splusbhist.SetLineColor(0)
splusbhist.SetMarkerSize(0)
splusbhist.SetFillStyle(3944)


stack.Draw("histsame")
splusbhist.Draw("e2same")
#Add signal
if not args.no_signal:
  sighist.SetLineColor(ROOT.kRed)
  sighist.SetLineWidth(3)
  sighist.Draw("histsame")
blind_datahist.DrawCopy("e0psame")
axish[0].Draw("axissame")

#Setup legend
legend = plot.PositionedLegend(0.48,0.30,3,0.03)
plot.Set(legend, NColumns=2)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
legend.SetFillColor(0)
legend.AddEntry(total_datahist,"Observation","PE")
#Drawn on legend in reverse order looks better
bkg_histos.reverse()
background_schemes[channel].reverse()
for legi,hists in enumerate(bkg_histos):
  legend.AddEntry(hists,background_schemes[channel][legi]['leg_text'],"f")
legend.AddEntry(splusbhist,"S+B uncertainty","f")
if not args.no_signal:
  legend.AddEntry(sighist,"VH(b#bar{b})","l")
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)
latex.SetTextSize(0.026)
legend.Draw("same")
latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextAngle(0)
latex2.SetTextColor(ROOT.kBlack)
latex2.SetTextSize(0.028)
latex2.DrawLatex(0.145,0.955,channel_label)


#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.30)
plot.DrawCMSLogo(pads[0], 'CMS', '', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.lumi, 3)

#Add ratio plot if required
if args.ratio:
  ratio_bkghist = plot.MakeRatioHist(splusbhist,splusbhist,True,False)
  blind_datahist = plot.MakeRatioHist(blind_datahist,splusbhist,True,False)
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(float(args.ratio_range.split(',')[0]))
  axish[1].SetMaximum(float(args.ratio_range.split(',')[1]))
  ratio_bkghist.SetMarkerSize(0)
  ratio_bkghist.Draw("e2same")
  blind_datahist.DrawCopy("e0same")
  pads[1].RedrawAxis("G")


pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()


#Save as png and pdf with some semi sensible filename
shape_file_name = shape_file_name.replace(".root","_%(mode)s"%vars())
shape_file_name = shape_file_name.replace("_shapes","")
outname += shape_file_name
if(log_y): outname+="_logy"
if(log_x): outname+="_logx"
c2.SaveAs("%(outname)s.png"%vars())
c2.SaveAs("%(outname)s.pdf"%vars())




