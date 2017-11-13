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
#Ingredients when output of PostFitShapes is already provided
parser.add_argument('--file', '-f',help='Input file if shape file has already been created')
parser.add_argument('--mA',default='700',help='Signal m_A to plot for model dep')
parser.add_argument('--tanb',default='30',help='Signal tanb to plot for model dep')
parser.add_argument('--mPhi',default='700',help='Signal m_Phi to plot for model indep')
parser.add_argument('--r_ggH',default='0.1',help='Signal ggH XS*BR for model indep')
parser.add_argument('--r_bbH',default='0.1',help='Signal bbH XS*BR for model indep')
parser.add_argument('--channel',default='',help='Option to specify channel in case it is not obtainable from the shape file name')
parser.add_argument('--file_dir',default='',help='Name of TDirectory inside shape file')
#Ingredients to internally call PostFitShapes
parser.add_argument('--dir', '-d', help='Directory for plot (channel-category containing the datacard and workspace)')
parser.add_argument('--postfitshapes',default=False,action='store_true',help='Run PostFitShapesFromWorkspace')
parser.add_argument('--workspace',default='mhmodp',help='Part of workspace filename right before .root')
parser.add_argument('--fitresult',help='Full path to fit result for making post fit plots')
parser.add_argument('--model_dep',action='store_true',default=False,help='Make plots for full model dependent signal h,H,A')
parser.add_argument('--mode',default='prefit',help='Prefit or postfit')
#Blinding options
parser.add_argument('--manual_blind', action='store_true',default=False,help='Blind data with hand chosen range')
parser.add_argument('--auto_blind',action='store_true',default=False,help='Blind data automatically based on s/root b')
parser.add_argument('--auto_blind_check_only',action='store_true',default=False,help='Only print blinding recommendation but still blind data using manual blinding')
parser.add_argument('--soverb_plot', action='store_true',default=False,help='Make plot with s/root b instead of ratio plot to test what it would blind')
parser.add_argument('--x_blind_min',default=10000,help='Minimum x for manual blinding')
parser.add_argument('--x_blind_max',default=4000,help='Maximum x for manual blinding')
parser.add_argument('--empty_bin_error',action='store_true',default=False, help='Draw error bars for empty bins')
#General plotting options
parser.add_argument('--channel_label',default='#mu#tau_{h} no b-tag',help='Channel - category label')
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
parser.add_argument('--bkg_fractions', default=False, action='store_true', help='Instead of yields for each process plot fraction of total bkg in each bin')
parser.add_argument('--bkg_frac_ratios', default=False, action='store_true', help='Instead of yields for each process plot fraction of total bkg in each bin')
parser.add_argument('--uniform_binning', default=False, action='store_true', help='Make plots in which each bin has the same width') 
parser.add_argument('--ratio_range',  help='y-axis range for ratio plot in format MIN,MAX', default="0.7,1.3")
parser.add_argument('--no_signal', action='store_true',help='Do not draw signal')
parser.add_argument('--split_y_scale', default=0.0,type=float,help='Use split y axis with linear scale at top and log scale at bottom. Cannot be used together with bkg_frac_ratios')
parser.add_argument('--sb_vs_b_ratio', action='store_true',help='Draw a Signal + Background / Background into the ratio plot')
parser.add_argument('--x_title', default='m_{T}^{tot} (GeV)',help='Title for the x-axis')
parser.add_argument('--y_title', default='dN/dm_{T}^{tot} (1/GeV)',help='Title for the y-axis')
parser.add_argument('--lumi', default='35.9 fb^{-1} (13 TeV)',help='Lumi label')


args = parser.parse_args()

mA = args.mA
mPhi = args.mPhi
tb = args.tanb
r_ggH = args.r_ggH
r_bbH = args.r_bbH
workspace = args.workspace
channel_label = args.channel_label
file_dir = args.file_dir
fitresult = args.fitresult
mode = args.mode
manual_blind = args.manual_blind
auto_blind = args.auto_blind
soverb_plot = args.soverb_plot
auto_blind_check_only = args.auto_blind_check_only
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
model_dep = args.model_dep
log_y=args.log_y
log_x=args.log_x
fractions=args.bkg_fractions
frac_ratios=args.bkg_frac_ratios
split_y_scale=args.split_y_scale
sb_vs_b_ratio = args.sb_vs_b_ratio
uniform=args.uniform_binning
#If plotting bkg fractions don't want to use log scale on y axis
if fractions:
  log_y = False
if uniform:
  log_y = False
  log_x = False
if(args.outname != ''):
  outname=args.outname + '_'
else:
  outname=''

if args.dir and args.file and not args.postfitshapes:
  print 'Provide either directory or filename, not both'
  sys.exit(1)

if not args.dir and not args.file and not args.postfitshapes:
  print 'Provide one of directory or filename'
  sys.exit(1)

if args.postfitshapes and not args.dir:
  print 'Provide directory when running with --postfitshapes option'
  sys.exit(1)

if manual_blind and auto_blind :
    print 'Pick only one option for blinding strategy out of --manual_blind and --auto_blind'
#For now, force that one type of blinding is always included! When unblinding the below line will need to be removed
if not manual_blind and not auto_blind: manual_blind=True    

if (args.auto_blind or args.auto_blind_check_only) and args.model_dep:
  print 'Automated blinding only supported for model independent plots, please use manual blinding'
  sys.exit(1)

if (args.auto_blind or args.auto_blind_check_only) and not args.postfitshapes:
  print 'Option --postfitshapes required when using auto-blinding, to ensure workspaces used for blinding exist in correct format'
  sys.exit(1)

#If call to PostFitWithShapes is requested, this is performed here
#if args.postfitshapes or soverb_plot:
if args.postfitshapes:
  print "Internally calling PostFitShapesFromWorkspace on directory ", args.dir
  for root,dirnames,filenames in os.walk(args.dir):
    for filename in fnmatch.filter(filenames, '*.txt.cmb'):
      datacard_file = os.path.join(root,filename) 
    for filename in fnmatch.filter(filenames, '*%(workspace)s.root'%vars()):
      workspace_file = os.path.join(root,filename)
      if model_dep :
          shape_file=workspace_file.replace('.root','_shapes_mA%(mA)s_tb%(tb)s.root'%vars())
          shape_file_name=filename.replace ('.root','_shapes_mA%(mA)s_tb%(tb)s.root'%vars())
      else : 
          shape_file=workspace_file.replace('.root','_shapes_mPhi%(mPhi)s_r_ggH%(r_ggH)s_r_bbH%(r_bbH)s.root'%vars())
          shape_file_name=filename.replace ('.root','_shapes_mPhi%(mPhi)s_r_ggH%(r_ggH)s_r_bbH%(r_bbH)s.root'%vars()) 
  
  if model_dep is True :
    print "using mA and tanb"
    freeze = 'mA='+mA+',tanb='+tb 
  else: 
    print "using MH="+mPhi+", r_ggH="+r_ggH+" and r_bbH="+r_bbH
    freeze = 'MH='+mPhi+',r_ggH='+r_ggH+',r_bbH='+r_bbH 
  if mode=="postfit": postfit_string = '--fitresult '+fitresult+':fit_s --postfit' 
  else: postfit_string = ''
  print 'PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s %(postfit_string)s --print --freeze %(freeze)s'%vars()
  os.system('PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s %(postfit_string)s --print --freeze %(freeze)s'%vars())


#Otherwise a shape file with a given naming convention is required
if not args.postfitshapes:
  if args.dir:
    for root,dirnames,filenames in os.walk(args.dir):
      if model_dep: filestring = '*_shapes_%(mA)s_%(tb)s.root'%vars()
      else: filestring = '*_shapes_mPhi%(mPhi)s_r_ggH%(r_ggH)s_r_bbH%(r_bbH)s.root'%vars()  
      for filename in fnmatch.filter(filenames, '*_shapes_%(mA)s_%(tb)s.root'%vars()):
        shape_file = os.path.join(root,filename)
  elif args.file:
    print "Providing shape file: ", args.file, ", with specified subdir name: ", file_dir
    shape_file=args.file
    shape_file_name=args.file

histo_file = ROOT.TFile(shape_file)

#Store plotting information for different backgrounds 
background_schemes = {'mt':[backgroundComp("t#bar{t}",["TTT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VVT"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#mu#mu",["ZL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("jet#rightarrow#tau_{h} fakes",["jetFakes"],ROOT.TColor.GetColor(192,232,100)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'et':[backgroundComp("t#bar{t}",["TTT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VVT"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowee",["ZL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("jet#rightarrow#tau_{h} fakes",["jetFakes"],ROOT.TColor.GetColor(192,232,100)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'tt':[backgroundComp("t#bar{t}",["TTT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VVT","ZL"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("jet#rightarrow#tau_{h} fakes",["jetFakes"],ROOT.TColor.GetColor(192,232,100)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'em':[backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZLL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'ttbar':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZLL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204))],
'zmm':[backgroundComp("Misidentified #mu", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104)),backgroundComp("Z#rightarrow#mu#mu",["ZLL"],ROOT.TColor.GetColor(100,192,232))]}

#Extract relevent histograms from shape file
[sighist,binname] = getHistogram(histo_file,'TotalSig', file_dir, mode, args.no_signal, log_x)
if not model_dep: sighist_ggH = getHistogram(histo_file,'ggH',file_dir, mode, args.no_signal, log_x)[0]
if not model_dep: sighist_bbH = getHistogram(histo_file,'bbH',file_dir, mode, args.no_signal, log_x)[0]
if sb_vs_b_ratio:
    sbhist = getHistogram(histo_file,'TotalProcs',file_dir, mode, args.no_signal, log_x)[0]
    bkg_sb_vs_b_ratio_hist = getHistogram(histo_file,'TotalBkg',file_dir, mode, logx=log_x)[0]
for i in range(0,sighist.GetNbinsX()):
  if sighist.GetBinContent(i) < y_axis_min: sighist.SetBinContent(i,y_axis_min)
bkghist = getHistogram(histo_file,'TotalBkg',file_dir, mode, logx=log_x)[0]

total_datahist = getHistogram(histo_file,"data_obs",file_dir, mode, logx=log_x)[0]
binerror_datahist = total_datahist.Clone()
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)
blind_datahist.SetLineColor(1)

#If using in test automated blinding mode, build the s/root b histogram for the ratio 
if model_dep :
    sighist_forratio = sighist.Clone()
    sighist_forratio.SetName("sighist_forratio")
else:
    sighist_ggH_forratio = sighist_ggH.Clone()
    sighist_ggH_forratio.SetName("sighist_ggH_forratio")
    sighist_bbH_forratio = sighist_bbH.Clone()
    sighist_bbH_forratio.SetName("sighist_bbH_forratio")
if soverb_plot:
    for j in range(1,bkghist.GetNbinsX()+1):
        if model_dep:
            soverb = sighist.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
            sighist_forratio.SetBinContent(j,soverb)
            sighist_forratio.SetBinError(j,0)
        else: 
            soverb_ggH = sighist_ggH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
            soverb_bbH = sighist_bbH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
            sighist_ggH_forratio.SetBinContent(j,soverb_ggH)
            sighist_ggH_forratio.SetBinError(j,0)
            sighist_bbH_forratio.SetBinContent(j,soverb_bbH)
            sighist_bbH_forratio.SetBinError(j,0)


#Blinding by hand using requested range, set to 200-4000 by default
if manual_blind or auto_blind_check_only:
  for i in range(0,total_datahist.GetNbinsX()):
    low_edge = total_datahist.GetBinLowEdge(i+1)
    high_edge = low_edge+total_datahist.GetBinWidth(i+1)
    if ((low_edge > float(x_blind_min) and low_edge < float(x_blind_max)) or (high_edge > float(x_blind_min) and high_edge<float(x_blind_max))):
      blind_datahist.SetBinContent(i+1,-0.1)
      blind_datahist.SetBinError(i+1,0)

#Automated blinding based on s/root b on bin by bin basis - use with caution!! Run with "check_only" mode first
if auto_blind or auto_blind_check_only:
    #Points for testing added by hand and chosen cross-sections are the exclusion from HIG-14-029 scaled by parton lumi. Values above 1 TeV are
    #crudely extrapolated using the 1 TeV limit and a higher parton lumi factor. 
    points=[200,300,400,500,600,700,900,1100,1500,2000,2500,3200]
    ggH_sigmas=[0.69,0.27,0.25,0.12,0.081,0.067,0.044,0.06,0.08,0.1,0.2,0.3]
    bbH_sigmas=[0.54,0.23,0.21,0.12,0.097,0.088,0.059,0.08,0.08,0.1,0.2,0.3]
    for root,dirnames,filenames in os.walk(args.dir):
      for filename in fnmatch.filter(filenames, '*.txt.cmb'):
        datacard_file = os.path.join(root,filename) 
      for filename in fnmatch.filter(filenames, '*%(workspace)s.root'%vars()):
        workspace_file = os.path.join(root,filename)
        unblind_binlow_set=[]
        unblind_binhigh_set=[]
        for i,p in enumerate(points) :
          shape_file=workspace_file.replace('.root','_shapes_mPhi'+str(p)+'.root')
          freeze = 'MH='+str(p)+',r_ggH='+str(ggH_sigmas[i])+',r_bbH='+str(bbH_sigmas[i])
          print 'PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --freeze %(freeze)s'%vars()
          os.system('PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --freeze %(freeze)s'%vars())
    
          testhisto_file = ROOT.TFile(shape_file)
          testsighist_ggH = getHistogram(testhisto_file,'ggH', file_dir,mode,logx=log_x)[0]
          testsighist_bbH = getHistogram(testhisto_file,'bbH', file_dir,mode,logx=log_x)[0]
          for j in range(1,bkghist.GetNbinsX()):
              soverb_ggH = testsighist_ggH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
              soverb_bbH = testsighist_bbH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
              if auto_blind_check_only: 
                  print "mPhi=",str(p)," r_ggPhi=",str(ggH_sigmas[i])," r_bbPhi=",str(bbH_sigmas[i]), "BinLowEdge=", bkghist.GetBinLowEdge(j), "BinHighEdge=", bkghist.GetBinLowEdge(j+1), "ggH s/b:", soverb_ggH, "bbH s/b:", soverb_bbH
              if soverb_ggH > 0.5 or soverb_bbH > 0.5:
                  if not auto_blind_check_only: blind_datahist.SetBinContent(j,0)
                  if not auto_blind_check_only: blind_datahist.SetBinError(j,0)
                  unblind_binlow_set.append(blind_datahist.GetBinLowEdge(j))    
                  unblind_binhigh_set.append(blind_datahist.GetBinLowEdge(j+1))    
        if auto_blind_check_only:
            binlow_list = sorted(set(unblind_binlow_set))
            binhigh_list = sorted(set(unblind_binhigh_set))
            print "Auto blinding algorithm would blind the following bins: "
            for h in range(0,len(binlow_list)):
                print binlow_list[h], "-", binhigh_list[h]            
            print "For this pass, applying manual blinding. Disable option --auto_blind_check_only to apply this automatic blinding"

#Set bin errors for empty bins if required:
if empty_bin_error:
  for i in range (1,blind_datahist.GetNbinsX()+1):
    if blind_datahist.GetBinContent(i) == 0:
      blind_datahist.SetBinError(i,1.8)

if uniform:
  blind_datahist2 = ROOT.TH1F(blind_datahist.GetName(),blind_datahist.GetName(),blind_datahist.GetNbinsX(),0,blind_datahist.GetNbinsX())
  total_datahist2 = ROOT.TH1F(total_datahist.GetName(),total_datahist.GetName(),total_datahist.GetNbinsX(),0,total_datahist.GetNbinsX())
  bkghist2 = ROOT.TH1F(bkghist.GetName(),bkghist.GetName(),bkghist.GetNbinsX(),0,bkghist.GetNbinsX())
  for i in range(0,blind_datahist.GetNbinsX()):
    blind_datahist2.SetBinContent(i,blind_datahist.GetBinContent(i))
    blind_datahist2.SetBinError(i,blind_datahist.GetBinError(i))
    total_datahist2.SetBinContent(i,total_datahist.GetBinContent(i))
    total_datahist2.SetBinError(i,total_datahist.GetBinError(i))
  blind_datahist = blind_datahist2
  total_datahist = total_datahist2
  for i in range(0,bkghist.GetNbinsX()):
    bkghist2.SetBinContent(i,bkghist.GetBinContent(i))
    bkghist2.SetBinError(i,bkghist.GetBinError(i))
  bkghist = bkghist2

  

#Normalise by bin width except in soverb_plot mode, where interpretation is easier without normalising
#Also don't normalise by bin width if plotting fractional bkg contribution
if not soverb_plot and not fractions and not uniform:
    blind_datahist.Scale(1.0,"width")
    total_datahist.Scale(1.0,"width")
    sighist.Scale(1.0,"width")
    if not model_dep: sighist_ggH.Scale(1.0,"width")
    if not model_dep: sighist_bbH.Scale(1.0,"width")
    bkghist.Scale(1.0,"width")

channel = args.channel
if channel == '':  channel=binname[4:6]

#Create stacked plot for the backgrounds
bkg_histos = []
bkg_histos_fractions = []
for i,t in enumerate(background_schemes[channel]):
  plots = t['plot_list']
  h = ROOT.TH1F()
  for j,k in enumerate(plots):
    if h.GetEntries()==0 and getHistogram(histo_file,k, file_dir,mode,logx=log_x) is not None:
      if not uniform:
        h = getHistogram(histo_file,k, file_dir,mode, logx=log_x)[0]
      else :
        htemp = getHistogram(histo_file,k,file_dir, mode,logx=log_x)[0]
        h = ROOT.TH1F(k,k,htemp.GetNbinsX(),0,htemp.GetNbinsX())
        for bp in range(0,htemp.GetNbinsX()):
          h.SetBinContent(bp+1,htemp.GetBinContent(bp+1))
          h.SetBinError(bp+1,htemp.GetBinError(bp+1))
      h.SetName(k)
    else:
      if getHistogram(histo_file,k, file_dir,mode, logx=log_x) is not None:
        if not uniform:
          h.Add(getHistogram(histo_file,k, file_dir,mode,logx=log_x)[0])
        else :
          htemp = getHistogram(histo_file,k,file_dir, mode,logx=log_x)[0]
          htemp2 = ROOT.TH1F(k,k,htemp.GetNbinsX(),0,htemp.GetNbinsX())
          for bp in range(0,htemp.GetNbinsX()):
            htemp2.SetBinContent(bp+1,htemp.GetBinContent(bp+1))
            htemp2.SetBinError(bp+1,htemp.GetBinError(bp+1))
          h.Add(htemp2)
  h.SetFillColor(t['colour'])
  h.SetLineColor(ROOT.kBlack)
  h.SetMarkerSize(0)
  
  if not soverb_plot and not fractions and not uniform : h.Scale(1.0,"width")
  if fractions:
    for i in range(1,h.GetNbinsX()+1) :
      h.SetBinContent(i,h.GetBinContent(i)/bkghist.GetBinContent(i))
  if frac_ratios:
    h_frac = h.Clone()
    for i in range(1, h_frac.GetNbinsX()+1):
      h_frac.SetBinContent(i,h_frac.GetBinContent(i)/bkghist.GetBinContent(i))
    bkg_histos_fractions.append(h_frac)
  bkg_histos.append(h)

stack = ROOT.THStack("hs","")
for hists in bkg_histos:
  stack.Add(hists)

if frac_ratios:
  stack_frac = ROOT.THStack("hs_frac","")
  for hists in bkg_histos_fractions:
    stack_frac.Add(hists)


#Setup style related things
c2 = ROOT.TCanvas()
c2.cd()

if args.ratio:
  if frac_ratios:
    pads=plot.MultiRatioSplit([0.25,0.14],[0.01,0.01],[0.01,0.01])
  elif split_y_scale:
    pads=plot.ThreePadSplit(0.53,0.29,0.01,0.01)
  else:
    pads=plot.TwoPadSplit(0.29,0.01,0.01)
else:
  pads=plot.OnePad()
pads[0].cd()
if(log_y):
  if split_y_scale:
    pads[2].SetLogy(1)
  else:
    pads[0].SetLogy(1)
if(log_x):
  pads[0].SetLogx(1)
  if(split_y_scale):
    pads[2].SetLogx(1)

if custom_x_range:
    if x_axis_max > bkghist.GetXaxis().GetXmax(): x_axis_max = bkghist.GetXaxis().GetXmax()
if args.ratio and not fractions:
  if not frac_ratios:
    if(log_x): pads[1].SetLogx(1)
    axish = createAxisHists(2,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()-0.01)
    axish[1].GetXaxis().SetTitle(args.x_title)
    axish[1].GetYaxis().SetNdivisions(4)
    if soverb_plot: axish[1].GetYaxis().SetTitle("S/#sqrt(B)")
    elif split_y_scale or sb_vs_b_ratio: axish[1].GetYaxis().SetTitle("")
    else: axish[1].GetYaxis().SetTitle("Obs/Exp")
    #axish[1].GetYaxis().SetTitleSize(0.04)
    axish[1].GetYaxis().SetLabelSize(0.033)
    axish[1].GetXaxis().SetLabelSize(0.033)
    #axish[1].GetYaxis().SetTitleOffset(1.3)
    axish[0].GetYaxis().SetTitleSize(0.048)
    axish[0].GetYaxis().SetLabelSize(0.033)
    axish[0].GetYaxis().SetTitleOffset(1.44)
    axish[0].GetXaxis().SetTitleSize(0)
    axish[0].GetXaxis().SetLabelSize(0)
    axish[0].GetXaxis().SetRangeUser(x_axis_min,bkghist.GetXaxis().GetXmax()-0.01)
    axish[1].GetXaxis().SetRangeUser(x_axis_min,bkghist.GetXaxis().GetXmax()-0.01)
    axish[0].GetXaxis().SetMoreLogLabels()
    axish[0].GetXaxis().SetNoExponent()
    axish[1].GetXaxis().SetMoreLogLabels()
    axish[1].GetXaxis().SetNoExponent()

    if custom_x_range:
      axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
      axish[1].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
    if custom_y_range:
      axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
      axish[1].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
    if split_y_scale:
      axistransit=split_y_scale
      axish.append(axish[0].Clone())

      axish[0].SetMinimum(axistransit)
      axish[0].SetTickLength(0)

      axish[2].GetYaxis().SetRangeUser(y_axis_min, axistransit)
      axish[2].GetYaxis().SetTitle("")
      axish[2].GetYaxis().SetLabelSize(0.033)
      axish[2].GetYaxis().SetNdivisions(3)
      width_sf = ((1-pads[0].GetTopMargin())-pads[0].GetBottomMargin())/((1-pads[2].GetTopMargin())-pads[2].GetBottomMargin())
      axish[2].GetYaxis().SetTickLength(width_sf*axish[0].GetYaxis().GetTickLength())

  else :
    if(log_x):
      pads[1].SetLogx(1)
      pads[2].SetLogx(1) 
    axish = createAxisHists(3,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()-0.01)
    axish[1].GetXaxis().SetTitle(args.x_title)
    axish[1].GetYaxis().SetNdivisions(4)
    axish[2].GetXaxis().SetTitle(args.x_title)
    axish[2].GetYaxis().SetNdivisions(4)
    axish[1].GetYaxis().SetTitleSize(0.03)
    axish[1].GetYaxis().SetLabelSize(0.03)
    axish[1].GetYaxis().SetTitleOffset(1.7)
    axish[2].GetYaxis().SetTitleOffset(1.7)
    axish[2].GetYaxis().SetTitleSize(0.03)
    axish[2].GetYaxis().SetLabelSize(0.03)
    axish[1].GetYaxis().SetTitle("Bkg. frac.")
    axish[2].GetYaxis().SetTitle("Obs/Exp")
    axish[0].GetXaxis().SetTitleSize(0)
    axish[0].GetXaxis().SetLabelSize(0)
    axish[1].GetXaxis().SetTitleSize(0)
    axish[1].GetXaxis().SetLabelSize(0)
    axish[0].GetXaxis().SetRangeUser(x_axis_min,bkghist.GetXaxis().GetXmax()-0.01)
    axish[1].GetXaxis().SetRangeUser(x_axis_min,bkghist.GetXaxis().GetXmax()-0.01)
    if custom_x_range:
      axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
      axish[1].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
      axish[2].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
    if custom_y_range:
      axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
else:
  axish = createAxisHists(1,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()-0.01)
#  axish[0].GetYaxis().SetTitleOffset(1.4)
  if custom_x_range:
    axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max-0.01)
  if custom_y_range and not fractions:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
  elif fractions: axish[0].GetYaxis().SetRangeUser(0,1)
if not soverb_plot and not fractions: axish[0].GetYaxis().SetTitle(args.y_title)
elif soverb_plot: axish[0].GetYaxis().SetTitle("Events")
elif fractions: axish[0].GetYaxis().SetTitle("Fraction of total bkg")
axish[0].GetXaxis().SetTitle(args.x_title)
if not custom_y_range: axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
if not custom_y_range: 
  if(log_y): axish[0].SetMinimum(0.0009)
  else: axish[0].SetMinimum(0)

hist_indices = [0,2] if split_y_scale else [0]
for i in hist_indices:
    pads[i].cd()
    axish[i].Draw("AXIS")

    #Draw uncertainty band
    bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
    bkghist.SetLineColor(0)
    bkghist.SetMarkerSize(0)

    stack.Draw("histsame")
    #Don't draw total bkgs/signal if plotting bkg fractions
    if not fractions and not uniform:
      bkghist.Draw("e2same")
      #Add signal, either model dependent or independent
      if not args.no_signal and ((split_y_scale and i == 2) or (not split_y_scale)):
        if model_dep is True: 
          sighist.SetLineColor(ROOT.kGreen+3)
          sighist.SetLineWidth(3)
          # A trick to remove vertical lines for the signal histogram at the borders while preventing the lines to end in the middle of the plot.
          for j in range(1,sighist.GetNbinsX()+1):
            entry = sighist.GetBinContent(j)
            if split_y_scale:
              if entry < axish[2].GetMinimum():
                sighist.SetBinContent(j,axish[2].GetMinimum()*1.00001)
            else:
              if entry < axish[0].GetMinimum():
                sighist.SetBinContent(j,axish[0].GetMinimum()*1.00001)
          sighist.Draw("histsame][") # removing vertical lines at the borders of the pad; possible with the trick above
        else: 
          sighist_ggH.SetLineColor(ROOT.kBlue)
          sighist_bbH.SetLineColor(ROOT.kBlue + 3)
          sighist_ggH.SetLineWidth(3)
          sighist_bbH.SetLineWidth(3)
          sighist_ggH.Draw("histsame")
          sighist_bbH.Draw("histsame")
    if not soverb_plot and not fractions: 
      blind_datahist.DrawCopy("e0x0same")
    axish[i].Draw("axissame")

pads[0].cd()
#Setup legend
legend = plot.PositionedLegend(0.30,0.30,3,0.03)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
legend.SetFillStyle(0)

signal_legend = None
if not args.no_signal and model_dep:
    signal_legend = plot.PositionedLegend(0.16,0.04,2,0.03,0.07)
    signal_legend.SetTextFont(42)
    signal_legend.SetTextSize(0.025)
    signal_legend.SetFillStyle(0)

if not soverb_plot and not fractions: legend.AddEntry(total_datahist,"Observation","PE")
#Drawn on legend in reverse order looks better
bkg_histos.reverse()
background_schemes[channel].reverse()
for legi,hists in enumerate(bkg_histos):
  legend.AddEntry(hists,background_schemes[channel][legi]['leg_text'],"f")
legend.AddEntry(bkghist,"Background uncertainty","f")
if not fractions:
  if not args.no_signal:
    if model_dep is True: 
        signal_legend.AddEntry(sighist,"h,H,A#rightarrow#tau#tau"%vars(),"l")
    else: 
        legend.AddEntry(sighist_ggH,"gg#phi("+mPhi+")#rightarrow#tau#tau"%vars(),"l")
        legend.AddEntry(sighist_bbH,"bb#phi("+mPhi+")#rightarrow#tau#tau"%vars(),"l")
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextAlign(11)
  latex.SetTextFont(42)
  latex.SetTextSize(0.025)
  latex.SetTextColor(ROOT.kBlack)
  if not args.no_signal:
    if model_dep is True: 
        latex.DrawLatex(0.477,0.80,"#splitline{#splitline{m_{h}^{mod+}}{#mu = 200 GeV}}{#splitline{m_{A} = %(mA)s GeV}{tan#beta = %(tb)s}}"%vars())
    else: 
        latex.DrawLatex(0.65,0.56,"#sigma(gg#phi)=%(r_ggH)s pb,"%vars())
        latex.DrawLatex(0.65,0.52,"#sigma(bb#phi)=%(r_bbH)s pb"%vars())
if not args.bkg_fractions: legend.Draw("same")
if not args.no_signal and model_dep: signal_legend.Draw("same")

# Channel & Category label
latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextAngle(0)
latex2.SetTextColor(ROOT.kBlack)
latex2.SetTextSize(0.04)
latex2.DrawLatex(0.145,0.955,channel_label)

#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.30)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.lumi, 3)

#Add ratio plot if required
if args.ratio and not soverb_plot and not fractions:
  ratio_bkghist = plot.MakeRatioHist(bkghist,bkghist,True,False)
  blind_datahist = plot.MakeRatioHist(blind_datahist,bkghist,True,False)
  if sb_vs_b_ratio:
    ratio_sbhist = plot.MakeRatioHist(sbhist,bkg_sb_vs_b_ratio_hist,True,False)
  if not frac_ratios:
    pads[1].cd()
    pads[1].SetGrid(0,1)
    axish[1].Draw("axis")
    axish[1].SetMinimum(float(args.ratio_range.split(',')[0]))
    axish[1].SetMaximum(float(args.ratio_range.split(',')[1]))
    ratio_bkghist.SetMarkerSize(0)
    ratio_bkghist.Draw("e2same")
    if sb_vs_b_ratio:
      ratio_sbhist.SetMarkerSize(0)
      ratio_sbhist.SetLineColor(ROOT.kGreen+3)
      ratio_sbhist.SetLineWidth(3)
      ratio_sbhist.Draw("histsame][")
    blind_datahist.DrawCopy("e0x0same")
    pads[1].RedrawAxis("G")
    if split_y_scale or sb_vs_b_ratio:
      # Add a ratio legend for y-splitted plots or plots with sb vs b ratios
      rlegend = plot.PositionedLegend(0.35,0.04,4,0.015,0.01)
      rlegend.SetTextFont(42)
      rlegend.SetTextSize(0.025)
      rlegend.SetFillStyle(1001)
      rlegend.SetFillColor(plot.CreateTransparentColor(3,0.2))
      rlegend.SetNColumns(2)
      rlegend.AddEntry(blind_datahist,"Obs/Bkg","PE")
      if sb_vs_b_ratio:
        rlegend.AddEntry(ratio_sbhist,"(Sig+Bkg)/Bkg","L")
      rlegend.Draw("same")
  else:
    pads[1].cd()
    axish[1].Draw("axis")
    axish[1].SetMinimum(0)
    axish[1].SetMaximum(1)
    stack_frac.Draw("histsame")
    pads[2].cd()
    pads[2].SetGrid(0,1)
    axish[2].Draw("axis")
    axish[2].SetMinimum(float(args.ratio_range.split(',')[0]))
    axish[2].SetMaximum(float(args.ratio_range.split(',')[1]))
    ratio_bkghist.SetMarkerSize(0)
    ratio_bkghist.Draw("e2same")
    blind_datahist.DrawCopy("e0same")
    pads[2].RedrawAxis("G")
    pads[1].RedrawAxis("G")
if soverb_plot:
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(0)
  axish[1].SetMaximum(10)
  if model_dep:
    sighist_forratio.SetLineColor(2)
    sighist_forratio.Draw("same")
  else:
    sighist_ggH_forratio.SetLineColor(ROOT.kBlue)
    sighist_ggH_forratio.Draw("same")
    sighist_bbH_forratio.SetLineColor(ROOT.kBlue+3)
    sighist_bbH_forratio.Draw("same")

pads[0].cd()
pads[0].GetFrame().Draw()
if not split_y_scale:
    pads[0].RedrawAxis()



if split_y_scale:
    pads[2].cd()
    pads[2].GetFrame().Draw()
    pads[2].RedrawAxis()

    pads[2].Update()
    x_min = axish[2].GetXaxis().GetXmin()
    x_max = axish[2].GetXaxis().GetXmax()
    splitline = ROOT.TLine(x_min*0.995,split_y_scale,x_max*1.5,split_y_scale)
    splitline.SetLineWidth(2)
    splitline.SetLineColor(ROOT.kGray+2)
    splitline.Draw()
    pads[0].cd()
    splitline.Draw()

    linear_latex = ROOT.TLatex()
    linear_latex.SetNDC()
    linear_latex.SetTextAngle(-90)
    linear_latex.SetTextColor(ROOT.kGray+2)
    linear_latex.SetTextSize(0.03)
    linear_latex.DrawLatex(0.973,0.70,"linear scale")


    log_latex = ROOT.TLatex()
    log_latex.SetNDC()
    log_latex.SetTextAngle(-90)
    log_latex.SetTextColor(ROOT.kGray+2)
    log_latex.SetTextSize(0.03)
    linear_latex.DrawLatex(0.973,0.51,"log scale")


#Save as png and pdf with some semi sensible filename
shape_file_name = shape_file_name.replace(".root","_%(mode)s"%vars())
shape_file_name = shape_file_name.replace("_shapes","")
outname += shape_file_name
if soverb_plot : outname+="_soverb"
if(log_y): outname+="_logy"
if(log_x): outname+="_logx"
c2.SaveAs("%(outname)s.png"%vars())
c2.SaveAs("%(outname)s.pdf"%vars())
