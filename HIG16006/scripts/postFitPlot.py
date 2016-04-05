import CombineHarvester.CombineTools.plotting as plot
import ROOT
import math
import argparse
import json
import sys
import os
import fnmatch

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getHistogram(fname,histname,dirname='',postfitmode='prefit'):
  outname = fname.GetName()
  for key in fname.GetListOfKeys():
    histo = fname.Get(key.GetName())
    dircheck = False
    if dirname == '' : dircheck=True
    elif dirname in key.GetName(): dircheck=True
    if isinstance(histo,ROOT.TH1F) and key.GetName()==histname:
      return [histo,outname]
    elif isinstance(histo,ROOT.TDirectory) and postfitmode in key.GetName() and dircheck:
      return getHistogram(histo,histname)
  print 'Failed to find %(postfitmode)s histogram with name %(histname)s in file %(fname)s '%vars()
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
parser.add_argument('--x_blind_min',default=200,help='Minimum x for manual blinding')
parser.add_argument('--x_blind_max',default=4000,help='Maximum x for manual blinding')
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
#If plotting bkg fractions don't want to use log scale on y axis
if fractions:
  log_y = False
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
if args.postfitshapes or soverb_plot:
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
background_schemes = {'mt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#mu#mu",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'et':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowee",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'tt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W","ZL","ZJ"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'em':[backgroundComp("Misidentified e/#mu", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZLL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))]}

#Extract relevent histograms from shape file
[sighist,binname] = getHistogram(histo_file,'TotalSig', file_dir, mode)
if not model_dep: sighist_ggH = getHistogram(histo_file,'ggH',file_dir, mode)[0]
if not model_dep: sighist_bbH = getHistogram(histo_file,'bbH',file_dir, mode)[0]
bkghist = getHistogram(histo_file,'TotalBkg',file_dir, mode)[0]

total_datahist = getHistogram(histo_file,"data_obs",file_dir, mode)[0]
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
    if ((low_edge > x_blind_min and low_edge < x_blind_max) or (high_edge > x_blind_min and high_edge<x_blind_max)):
      blind_datahist.SetBinContent(i+1,0)
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
          testsighist_ggH = getHistogram(testhisto_file,'ggH', file_dir,mode)[0]
          testsighist_bbH = getHistogram(testhisto_file,'bbH', file_dir,mode)[0]
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


#Normalise by bin width except in soverb_plot mode, where interpretation is easier without normalising
#Also don't normalise by bin width if plotting fractional bkg contribution
if not soverb_plot and not fractions:
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
for i,t in enumerate(background_schemes[channel]):
  plots = t['plot_list']
  h = ROOT.TH1F()
  for j,k in enumerate(plots):
    if h.GetEntries()==0 and getHistogram(histo_file,k, file_dir,mode) is not None:
      h = getHistogram(histo_file,k, file_dir,mode)[0]
      h.SetName(k)
    else:
      if getHistogram(histo_file,k, file_dir,mode) is not None:
        h.Add(getHistogram(histo_file,k, file_dir,mode)[0])
  h.SetFillColor(t['colour'])
  h.SetLineColor(ROOT.kBlack)
  h.SetMarkerSize(0)
  if not soverb_plot and not fractions : h.Scale(1.0,"width")
  if fractions:
    for i in range(1,h.GetNbinsX()+1) :
      h.SetBinContent(i,h.GetBinContent(i)/bkghist.GetBinContent(i))
  bkg_histos.append(h)

stack = ROOT.THStack("hs","")
for hists in bkg_histos:
  stack.Add(hists)


#Setup style related things
plot.ModTDRStyle(r=0.06, l=0.12)
c2 = ROOT.TCanvas()
c2.cd()
if args.ratio:
  pads=plot.TwoPadSplit(0.29,0.005,0.005)
else:
  pads=plot.OnePad()
pads[0].cd()
if(log_y): pads[0].SetLogy(1)
if(log_x): pads[0].SetLogx(1)
if args.ratio and not fractions:
  if(log_x): pads[1].SetLogx(1)
  axish = createAxisHists(2,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax())
  axish[1].GetXaxis().SetTitle("m_{T,#tau#tau} (GeV)")
  axish[1].GetYaxis().SetNdivisions(4)
  if not soverb_plot: axish[1].GetYaxis().SetTitle("Obs/Exp")
  else: axish[1].GetYaxis().SetTitle("S/#sqrt(B)")
  axish[0].GetXaxis().SetTitleSize(0)
  axish[0].GetXaxis().SetLabelSize(0)
  axish[0].GetYaxis().SetTitleOffset(1.4)
  axish[1].GetYaxis().SetTitleOffset(1.4)
  if custom_x_range:
    axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max)
    axish[1].GetXaxis().SetRangeUser(x_axis_min,x_axis_max)
  if custom_y_range:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
    axish[1].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
else:
  axish = createAxisHists(1,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax())
  axish[0].GetYaxis().SetTitleOffset(1.4)
  if custom_x_range:
    axish[0].GetXaxis().SetRangeUser(x_axis_min,x_axis_max)
  if custom_y_range and not fractions:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
  elif fractions: axish[0].GetYaxis().SetRangeUser(0,1)
if not soverb_plot and not fractions: axish[0].GetYaxis().SetTitle("dN/dM_{T,#tau#tau} (1/GeV)")
elif soverb_plot: axish[0].GetYaxis().SetTitle("Events")
elif fractions: axish[0].GetYaxis().SetTitle("Fraction of total bkg")
axish[0].GetXaxis().SetTitle("m_{T,#tau#tau} (GeV)")
if not custom_y_range: axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
if not custom_y_range: 
  if(log_y): axish[0].SetMinimum(0.0009)
  else: axish[0].SetMinimum(0)
axish[0].Draw()

#Draw uncertainty band
bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
bkghist.SetLineColor(0)
bkghist.SetMarkerSize(0)

stack.Draw("histsame")
#Don't draw total bkgs/signal if plotting bkg fractions
if not fractions:
  bkghist.Draw("e2same")
  #Add signal, either model dependent or independent
  if model_dep is True: 
      sighist.SetLineColor(ROOT.kRed)
      sighist.Draw("histsame")
  else: 
      sighist_ggH.SetLineColor(ROOT.kBlue)
      sighist_bbH.SetLineColor(ROOT.kBlue + 3)
      sighist_ggH.Draw("histsame")
      sighist_bbH.Draw("histsame")
if not soverb_plot and not fractions: blind_datahist.DrawCopy("psame")
axish[0].Draw("axissame")

#Setup legend
legend = plot.PositionedLegend(0.30,0.30,3,0.03)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
legend.SetFillColor(0)
#Drawn on legend in reverse order looks better
bkg_histos.reverse()
background_schemes[channel].reverse()
for legi,hists in enumerate(bkg_histos):
  legend.AddEntry(hists,background_schemes[channel][legi]['leg_text'],"f")
legend.AddEntry(bkghist,"Background uncertainty","f")
if not fractions:
  if model_dep is True: 
      legend.AddEntry(sighist,"H,h,A#rightarrow#tau#tau"%vars(),"l")
  else: 
      legend.AddEntry(sighist_ggH,"gg#phi("+mPhi+")#rightarrow#tau#tau"%vars(),"l")
      legend.AddEntry(sighist_bbH,"bb#phi("+mPhi+")#rightarrow#tau#tau"%vars(),"l")
  if not soverb_plot: legend.AddEntry(blind_datahist,"Observation","P")
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)
  latex.SetTextSize(0.026)
  if model_dep is True: 
      latex.DrawLatex(0.61,0.53,"m_{h}^{mod+}, m_{A}=%(mA)s GeV, tan#beta=%(tb)s"%vars())
  else: 
      latex.DrawLatex(0.63,0.56,"#sigma(gg#phi)=%(r_ggH)s pb,"%vars())
      latex.DrawLatex(0.63,0.52,"#sigma(bb#phi)=%(r_bbH)s pb"%vars())
legend.Draw("same")
latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextAngle(0)
latex2.SetTextColor(ROOT.kBlack)
latex2.SetTextSize(0.028)
latex2.DrawLatex(0.125,0.96,channel_label)


#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.15)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], "2.3 fb^{-1} (13 TeV)", 3);

#Add ratio plot if required
if args.ratio and not soverb_plot and not fractions:
  ratio_bkghist = bkghist.Clone()
  ratio_bkghist.Divide(bkghist)
  blind_datahist.Divide(bkghist)
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(0.7)
  axish[1].SetMaximum(1.3)
  ratio_bkghist.SetMarkerSize(0)
  ratio_bkghist.Draw("e2same")
  blind_datahist.DrawCopy("psame")
  pads[1].RedrawAxis("G")

if soverb_plot:
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(0)
  axish[1].SetMaximum(2)
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
pads[0].RedrawAxis()


#Save as png and pdf with some semi sensible filename
shape_file_name = shape_file_name.replace(".root","_%(mode)s"%vars())
shape_file_name = shape_file_name.replace("_shapes","")
outname += shape_file_name
if soverb_plot : outname+="_soverb"
if(log_y): outname+="_logy"
if(log_x): outname+="_logx"
c2.SaveAs("%(outname)s.png"%vars())
c2.SaveAs("%(outname)s.pdf"%vars())




