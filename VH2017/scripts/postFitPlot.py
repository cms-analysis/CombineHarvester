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
from math import pow,sqrt

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
parser.add_argument('--channel_label',default='',help='Channel label')
parser.add_argument('--ratio', default=False,action='store_true',help='Draw ratio plot')
parser.add_argument('--ratio_justb', default=False,action='store_true',help='Draw ratio plot with respect to B-only')
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
parser.add_argument('--x_title', default='m(jj) [GeV]',help='Title for the x-axis. For bin labels give comma-separated string.')
parser.add_argument('--y_title', default='S/(S+B) weighted entries',help='Title for the y-axis')
parser.add_argument('--lumi', default='77.2 fb^{-1} (13 TeV)',help='Lumi label')
parser.add_argument('--cr', default=False, action='store_true', help='Plot CRs? (Important for QCD in 0-lep')
parser.add_argument('--weights', default="", help='weights')
parser.add_argument('--verbosity','-v', default=0, help='verbosity level (default 0)')
parser.add_argument('--subbkg',         default=0, help='subtract backgrounds (default 0)')
parser.add_argument('--extralabel',     default='', help='Extra label next to CMS')
args = parser.parse_args()


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

def getHistogram(fname, histname, dirnames='', postfitmode='prefit', allowEmpty=False, logx=False, inweight=1):
  if args.verbosity>2:
    print "called getHistogram: ",fname,histname,dirnames,postfitmode,allowEmpty,logx,inweight
    print "dirnames = ",dirnames
  returnName = fname.GetName()
  return_hist = ""
  for key in fname.GetListOfKeys():
    if histname.find("data")!=-1:
      if args.verbosity>2:
        print "key.GetName() = ",key.GetName()
    histo = fname.Get(key.GetName())
    for dirname in dirnames.split(','): 
        #print weights,dirname
        weight=inweight*(weights[dirname] if dirname in weights else 1)
        if weight==0 :
          print histname, dirname
        dircheck = False
        if histname.find("data")!=-1: 
          if args.verbosity>2:
            print "dirname now = ",dirname
        if dirname == '' : dircheck=True
        elif dirname in key.GetName(): dircheck=True
        if isinstance(histo,ROOT.TH1F) and key.GetName()==histname:
          histo.Scale(weight)
          #if (histname.find("data")==-1 and histname.find("hbb")==-1 and histname.find("VVHF")==-1):
          #  histo.Smooth(5)
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
          #return [histo,returnName]
          if not isinstance(return_hist,ROOT.TH1F):
            if histname.find("data")!=-1:
                print "non-recursive call, adding (first): ",histname
            return_hist = histo
          else: 
            if histname.find("data")!=-1:
              if args.verbosity>2:
                print "non-recursive call, adding: ",histname
            return_hist.Add(histo)
          if histname.find("data")!=-1:
            if args.verbosity>2:
              print "return_hist.Integral() = ",return_hist.Integral()
        elif isinstance(histo,ROOT.TDirectory) and postfitmode in key.GetName() and dircheck:
            #return getHistogram(histo,histname, allowEmpty=allowEmpty, logx=logx)
            hist_tmp = getHistogram(histo,histname, allowEmpty=allowEmpty, logx=logx,inweight=weight)
            if hist_tmp is not None:
              if not isinstance(return_hist,ROOT.TH1F):
                if histname.find("data")!=-1:
                  if args.verbosity>2:
                    print "first hist to return:",histo,histname
                return_hist = getHistogram(histo,histname, allowEmpty=allowEmpty, logx=logx,inweight=weight)[0]
              else: 
                if histname.find("data")!=-1:
                  if args.verbosity>2:
                    print "adding to return_hist: ",histo,histname
                return_hist.Add(getHistogram(histo,histname, allowEmpty=allowEmpty, logx=logx,inweight=weight)[0])
              if histname.find("data")!=-1:
                if args.verbosity>2:
                  print "total return_hist now: ",return_hist.Integral()  

  if not isinstance(return_hist,ROOT.TH1F):
    print 'Failed to find %(postfitmode)s histogram with name %(histname)s in file %(fname)s '%vars()
    if allowEmpty:
      return [ROOT.TH1F('empty', '', 1, 0, 1), returnName]
    else:
      return None
  return [return_hist,returnName]

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

weights={}
if args.weights != "" :
  for w,s in zip(args.weights.split(","),args.file_dir.split(",")):
    weights[s]=float(w)

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

if args.verbosity>0:
  print "Using shape file ", args.file, ", with specified subdir name(s): ", file_dir
shape_file_name=args.file

histo_file = ROOT.TFile(shape_file_name)

#Store plotting information for different backgrounds 
background_schemes = {
'Wen':[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("WHb#bar{b}",["WH_hbb"],634)],
'Wmn':[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("WHb#bar{b}",["WH_hbb"],634)],
'Zee':[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625)],
'Zmm':[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625)],
'Znn':[backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("Single top",["s_Top"],862),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625),backgroundComp("WHb#bar{b}",["WH_hbb"],634),backgroundComp("QCD",["QCD"],613)]}
#'Znn':[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("WHb#bar{b}",["WH_hbb"],634)],backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"])}

if args.cr:
  background_schemes['Znn']=[backgroundComp("Single top",["s_Top"],862),backgroundComp("VV+LF",["VVLF"], 13),backgroundComp("VV+HF",["VVHF"],17),backgroundComp("t#bar{t}",["TT"],4),backgroundComp("Z+udscg",["Zj0b"],402),backgroundComp("Z+b",["Zj1b"],397),backgroundComp("Z+b#bar{b}",["Zj2b"],5),backgroundComp("W+udscg",["Wj0b"],814),backgroundComp("W+b",["Wj1b"],815),backgroundComp("W+b#bar{b}",["Wj2b"],81),backgroundComp("QCD",["QCD"],613),backgroundComp("ZHb#bar{b}",["ZH_hbb"],2),backgroundComp("ggZHb#bar{b}",["ggZH_hbb"],625),backgroundComp("WHb#bar{b}",["WH_hbb"],634)]
#To be filled later depending on which histograms actually exist
plot_background_schemes = {'Wen':[],'Wmn':[],'Zee':[],'Zmm':[],'Znn':[]}

#Extract relevant histograms from shape file
[sighist,binname] = getHistogram(histo_file,'TotalSig', file_dir, mode, args.no_signal, log_x)
for i in range(0,sighist.GetNbinsX()):
  if sighist.GetBinContent(i) < y_axis_min: sighist.SetBinContent(i,y_axis_min)
bkghist = getHistogram(histo_file,'TotalBkg',file_dir, mode, logx=log_x)[0]
splusbhist = getHistogram(histo_file,'TotalProcs',file_dir, mode, logx=log_x)[0]
if args.subbkg!=0:
  splusbhist_total = getHistogram(histo_file,'TotalProcs',file_dir, mode, logx=log_x)[0]
  vvhist = getHistogram(histo_file,'VVHF',file_dir, mode, logx=log_x)[0]

if args.verbosity>1:
  print "grabbing data histogram"
  print "file_dir = ",file_dir
total_datahist = getHistogram(histo_file,"data_obs",file_dir, mode, logx=log_x)[0]
if args.subbkg!=0:
  total_datahist.Sumw2()
if args.verbosity>1:
  print "data integral = ",total_datahist.Integral()
binerror_datahist = total_datahist.Clone()
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)
if args.subbkg!=0:
  blind_datahist.SetLineWidth(2)
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
  if args.subbkg!=0:
    h.SetLineColor(ROOT.kBlack)
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
    plot_background_schemes[channel].append(t)

stack = ROOT.THStack("hs","")
for hists in bkg_histos:
  stack.Add(hists)

xLabelsPerBin=(len(args.x_title.split(","))>1)
if xLabelsPerBin:
    args.x_title=args.x_title.split(",")

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
  if xLabelsPerBin:
    axish[1].GetXaxis().SetLabelSize(0.06)
    axish[1].GetXaxis().RotateTitle(True)
    iBin=1
    for label in args.x_title:
      axish[1].GetXaxis().SetBinLabel(iBin,label)
      iBin=iBin+1
  else:
    axish[1].GetXaxis().SetTitle(args.x_title)
  axish[1].GetYaxis().SetNdivisions(4)
  axish[1].GetYaxis().SetTitle("Obs / Exp")
  if args.ratio_justb:
    axish[1].GetYaxis().SetTitle("Obs / Bkg")
  if args.subbkg==0:
    axish[1].GetXaxis().SetTitleOffset(1.2)
    axish[1].GetXaxis().SetTitleFont(42)
    axish[1].GetXaxis().SetLabelOffset(0.01)
    axish[1].GetXaxis().SetLabelFont(42)
    axish[1].GetYaxis().SetTitleOffset(1.85)
    axish[1].GetYaxis().SetTitleFont(42)
    axish[1].GetYaxis().SetLabelOffset(0.01)
    axish[1].GetYaxis().SetLabelFont(42)
    axish[1].GetYaxis().SetTitleSize(0.04)
    axish[1].GetXaxis().SetTitleSize(0.04)

    axish[0].GetXaxis().SetLabelOffset(0.01)
    axish[0].GetYaxis().SetTitleOffset(1.85)
    axish[0].GetYaxis().SetLabelOffset(0.01)
    axish[0].GetYaxis().SetTitleSize(0.04)
  else:
    axish[0].GetXaxis().SetLabelOffset(0.1)
    axish[0].GetYaxis().SetTitleOffset(1.2)
    axish[0].GetYaxis().SetLabelOffset(0.1)
  
  axish[0].GetXaxis().SetLabelSize(0)
  axish[0].GetXaxis().SetTitleOffset(1.2)
  axish[0].GetXaxis().SetTitleFont(42)
  axish[0].GetXaxis().SetLabelFont(42)
  axish[0].GetYaxis().SetTitleFont(42)
  axish[0].GetYaxis().SetLabelFont(42)
  axish[0].GetXaxis().SetTitleSize(0)


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
    if args.subbkg!=0:
      axish[0].GetXaxis().SetTitleOffset(1.2)
      axish[0].GetXaxis().SetTitleFont(42)
      axish[0].GetXaxis().SetLabelOffset(0.01)
      axish[0].GetXaxis().SetLabelFont(42)
      axish[0].GetXaxis().SetTitleSize(0.04)
      axish[0].GetYaxis().SetTitleOffset(1.75)
      axish[0].GetYaxis().SetTitleFont(42)
      axish[0].GetYaxis().SetLabelOffset(0.01)
      axish[0].GetYaxis().SetLabelFont(42)
      axish[0].GetYaxis().SetTitleSize(0.04)

axish[0].GetYaxis().SetTitle(args.y_title)
if not args.ratio:
  if xLabelsPerBin:
    axish[0].GetXaxis().SetLabelSize(0.06)
    iBin=1
    for label in args.x_title:
      axish[0].GetXaxis().SetBinLabel(iBin,label)
      iBin=iBin+1
  else:
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

if args.subbkg!=0:
  bkghist_noerr = bkghist.Clone("bkghist_noerr")
  splusbhist_total_noerr = splusbhist_total.Clone("splusbhist_total_noerr")

  for i in xrange(1,bkghist_noerr.GetNbinsX()+1):
  #  bkghist_noerr.Sumw2()
      bkghist_noerr.SetBinError(i,0.)
  for i in xrange(1,splusbhist_total_noerr.GetNbinsX()+1):
  #  bkghist_noerr.Sumw2()
      splusbhist_total_noerr.SetBinError(i,0.)
  
  vvhist_noerr = vvhist.Clone("vvhist_noerr")
  for i in xrange(1,bkghist_noerr.GetNbinsX()+1):
  #    vvhist_noerr.Sumw2()
      vvhist_noerr.SetBinError(i,0.)
  blind_datahist.Sumw2()
  blind_datahist.Add(bkghist_noerr,-1)
  splusbhist.Sumw2()
  splusbhist.Add(bkghist_noerr,-1)
  vvhist_noerr.Sumw2()
  blind_datahist.Add(vvhist_noerr)
  splusbhist.Add(vvhist_noerr)
  splusbhist_total.Sumw2()
  splusbhist_total.Add(splusbhist_total_noerr,-1)
else:
  stack.Draw("histsame")
  splusbhist.Draw("e2same")

#Add signal
if not args.no_signal:
  sighist.SetLineColor(ROOT.kRed)
  sighist.SetLineWidth(3)
  sighist.Draw("histsame")
  if args.subbkg!=0:
    vvhist.SetLineColor(ROOT.kBlack)
    vvhist.SetFillColor(17)
    sighist.SetLineColor(ROOT.kBlack)
    sighist.SetFillColor(ROOT.kRed)
    sigstack = ROOT.THStack()
    sigstack.Add(vvhist)
    sigstack.Add(sighist)
    sigstack.Draw("hist same")

if args.subbkg!=0:
  bkg_unc = bkghist.Clone("bkg_unc")
  bkg_unc_minus = bkghist.Clone("bkg_unc_minus")
  for i in xrange(1,bkghist.GetNbinsX()+1):
      e = sqrt(pow(bkghist.GetBinError(i),2) - pow(vvhist.GetBinError(i),2))
      bkg_unc.SetBinContent(i,e)
      bkg_unc_minus.SetBinContent(i,-1.0*e)
#  bkg_unc.SetLineColor(ROOT.kBlue)
#  bkg_unc.SetLineWidth(3)
#  bkg_unc_minus.SetLineColor(ROOT.kBlue)
#  bkg_unc_minus.SetLineWidth(3)
#  bkg_unc.SetFillStyle(0)
#  bkg_unc_minus.SetFillStyle(0)
#  bkg_unc.Draw("histsame")
#  bkg_unc_minus.Draw("histsame")

blind_datahist.DrawCopy("e0psame")
axish[0].Draw("axissame")

#Setup legend
if args.subbkg!=0:
  legend = plot.PositionedLegend(0.30,0.22,3,0.03)
  plot.Set(legend, NColumns=1)
else:
  legend = plot.PositionedLegend(0.47,0.30,3,0.03)
  plot.Set(legend, NColumns=2)
legend.SetTextFont(42)
legend.SetTextSize(0.032)
legend.SetFillColor(0)
legend.AddEntry(total_datahist,"Data","PE")
#Drawn on legend in reverse order looks better
bkg_histos.reverse()
plot_background_schemes[channel].reverse()
if args.subbkg==0:
  for legi,hists in enumerate(bkg_histos):
    legend.AddEntry(hists,plot_background_schemes[channel][legi]['leg_text'],"f")
if not args.no_signal:
  legend.AddEntry(splusbhist,"S+B uncertainty","f")
  if args.subbkg==0:
    legend.AddEntry(sighist,"VH,H#rightarrowb#bar{b}","l")
  else:
    legend.AddEntry(sighist,"VH,H#rightarrowb#bar{b}","f")
  if args.subbkg!=0:
    legend.AddEntry(vvhist,"VZ,Z#rightarrowb#bar{b}","f")
else:
  legend.AddEntry(splusbhist,"MC uncertainty","f")
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
if args.extralabel=="":
  setY=0.84
else:
  setY=0.78
setX=0.18

latex2.DrawLatex(setX,setY,channel_label)

if args.subbkg!=0:
  splusbhist_total.SetFillColor(ROOT.kGray+3)
  splusbhist_total.SetFillStyle(3013)
  splusbhist_total.SetMarkerSize(0)
  splusbhist_total.Draw('e2same')
  if not args.no_signal:
    legend.AddEntry(splusbhist_total,"S+B uncertainty","f")
  else:
    legend.AddEntry(splusbhist_total,"MC uncertainty","f")
  #theErrorGraph = ROOT.TGraphErrors(sigstack.GetStack().Last())
  #theErrorGraph.SetFillColor(ROOT.kGray+3)
  #theErrorGraph.SetFillStyle(3013)
  #theErrorGraph.Draw('SAME2')
  #legend.AddEntry(theErrorGraph,"VH+VZ uncert.","fl")

#CMS and lumi labels
if args.subbkg==0:
  ROOT.gStyle.SetTitleFont(42)
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.30)
plot.DrawCMSLogo(pads[0], 'CMS', args.extralabel, 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.lumi, 3)

#Add ratio plot if required
if args.ratio:
  if args.ratio_justb:
     # it's a bit silly to call getHistogram again but otherwise we pick up the style modifications to bkghist
    ratio_soverbhist = plot.MakeRatioHist(splusbhist,bkghist,False,False)
    ratio_bkghist = plot.MakeRatioHist(bkghist,bkghist,True,False)
    blind_datahist = plot.MakeRatioHist(blind_datahist,bkghist,True,False)
  else:
    ratio_bkghist = plot.MakeRatioHist(splusbhist,splusbhist,True,False)
    blind_datahist = plot.MakeRatioHist(blind_datahist,splusbhist,True,False)
  if args.subbkg!=0:
    ratio_bkghist = plot.MakeRatioHist(splusbhist,splusbhist,True,True)
    blind_datahist = plot.MakeRatioHist(blind_datahist,splusbhist,True,True)
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(float(args.ratio_range.split(',')[0]))
  axish[1].SetMaximum(float(args.ratio_range.split(',')[1]))
  if args.ratio_justb:
      ratio_soverbhist.SetLineColor(ROOT.kRed)
      ratio_soverbhist.SetFillColor(0)
      ratio_soverbhist.Draw("hist same")
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
outname += shape_file_name.split("/")[-1]
if(log_y): outname+="_logy"
if(log_x): outname+="_logx"
if args.subbkg==0:
  c2.SaveAs("%(outname)s.png"%vars())
  c2.SaveAs("%(outname)s.pdf"%vars())
else:
  c2.SaveAs("%(outname)s_unsub.png"%vars())
  c2.SaveAs("%(outname)s_unsub.pdf"%vars())

if args.verbosity>0:
  print splusbhist.Integral(),stack.GetStack().Last().Integral()


if args.subbkg==0:
  outfile = ROOT.TFile("mjj_withBkg.root","UPDATE")
else:
  outfile = ROOT.TFile("mjj_subtracted.root","UPDATE")
c2.Write()
outfile.Close()

