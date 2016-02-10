import CombineHarvester.CombineTools.plotting as plot
import ROOT
import math
import argparse
import json
import sys
import os
import fnmatch

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getHistogram(fname,histname,postfitmode='prefit'):
  outname = fname.GetName()
  for key in fname.GetListOfKeys():
    histo = fname.Get(key.GetName())
    if isinstance(histo,ROOT.TH1F) and key.GetName()==histname:
      return [histo,outname]
    elif isinstance(histo,ROOT.TDirectory) and postfitmode in key.GetName():
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
parser.add_argument('--dir', '-d', help='Directory for plot (channel-category containing the datacard and workspace)')
parser.add_argument('--file', '-f',help='Input file if shape file has already been created')
parser.add_argument('--mA',default='700',help='Signal m_A to plot for model dep')
parser.add_argument('--tanb',default='30',help='Signal tanb to plot for model dep')
parser.add_argument('--mPhi',default='700',help='Signal m_Phi to plot for model indep')
parser.add_argument('--r_ggH',default='0.1',help='Signal ggH XS*BR for model indep')
parser.add_argument('--r_bbH',default='0.1',help='Signal bbH XS*BR for model indep')
parser.add_argument('--postfitshapes',default=False,action='store_true',help='Run PostFitShapesFromWorkspace')
parser.add_argument('--workspace',default='mhmodp',help='Part of workspace filename right before .root')
parser.add_argument('--model_dep',action='store_true',default=False,help='Make plots for full model dependent signal h,H,A')
parser.add_argument('--mode',default='prefit',help='Prefit or postfit')
parser.add_argument('--manual_blind', action='store_true',default=False,help='Blind data with hand chosen range')
parser.add_argument('--auto_blind',action='store_true',default=False,help='Blind data automatically based on s/root b')
parser.add_argument('--auto_blind_check_only',action='store_true',default=False,help='Only print blinding recommendation but still blind data using manual blinding')
parser.add_argument('--soverb_plot', action='store_true',default=False,help='Make plot with s/root b instead of ratio plot to test what it would blind')
parser.add_argument('--x_blind_min',default=200,help='Minimum x for manual blinding')
parser.add_argument('--x_blind_max',default=4000,help='Maximum x for manual blinding')
parser.add_argument('--ratio', default=True,action='store_true',help='Draw ratio plot')
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


args = parser.parse_args()

mA = args.mA
mPhi = args.mPhi
tb = args.tanb
r_ggH = args.r_ggH
r_bbH = args.r_bbH
workspace = args.workspace
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
outname=args.outname + '_'

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
    print 'Pick one option for blinding strategy out of --manual_blind and --auto_blind'
#For now, force that one type of blinding is always included! When unblinding the below line will need to be removed
if not manual_blind and not auto_blind: manual_blind=True    

#If call to PostFitWithShapes is requested, this is performed here
if args.postfitshapes or soverb_plot:
  for root,dirnames,filenames in os.walk(args.dir):
    for filename in fnmatch.filter(filenames, '*.txt'):
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
    freeze = 'MH='+mPhi+',r_ggH='+r_ggH+',r_bbH='+r_bbH 
  print 'PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --print --freeze %(freeze)s'%vars()
  os.system('PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --print --freeze %(freeze)s'%vars())


#Otherwise a shape file with a given naming convention is required
if not args.postfitshapes:
  if args.dir:
    for root,dirnames,filenames in os.walk(args.dir):
      if model_dep: filestring = '*_shapes_%(mA)s_%(tb)s.root'%vars()
      else: filestring = '*_shapes_mPhi%(mPhi)s_r_ggH%(r_ggH)s_r_bbH%(r_bbH)s.root'%vars()  
      for filename in fnmatch.filter(filenames, '*_shapes_%(mA)s_%(tb)s.root'%vars()):
        shape_file = os.path.join(root,filename)
  elif args.file:
    shape_file=args.file

histo_file = ROOT.TFile(shape_file)

#Store plotting information for different backgrounds 
background_schemes = {'mt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#mu#mu",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'et':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowee",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'tt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#tau#tau",["ZTT","ZL","ZJ"],ROOT.TColor.GetColor(248,206,104))],
'em':[backgroundComp("Misidentified e/#mu", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))]}

#Extract relevent histograms from shape file
[sighist,binname] = getHistogram(histo_file,'TotalSig')
if not model_dep: sighist_ggH = getHistogram(histo_file,'ggH')[0]
if not model_dep: sighist_bbH = getHistogram(histo_file,'bbH')[0]
bkghist = getHistogram(histo_file,'TotalBkg')[0]

total_datahist = getHistogram(histo_file,"data_obs")[0]
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)

#If using in test automated blinding mode, build the s/root b histogram for the ratio 
sighist_forratio = sighist.Clone()
sighist_forratio.SetName("sighist_forratio")
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

#Automated blinding based on s/root b on bin by bin basis
if auto_blind or auto_blind_check_only:
    #Points for testing added by hand and chosen cross-sections are the exclusion from HIG-14-029 scaled by parton lumi. Values above 1 TeV are
    #crudely extrapolated using the 1 TeV limit and a higher parton lumi factor
    points=[300,500,700,900,1100,1500,2000,3200]
    ggH_sigmas=[0.27,0.12,0.067,0.044,0.044,0.08,0.1,0.1]
    bbH_sigmas=[0.23,0.12,0.088,0.059,0.059,0.08,0.1,0.1]
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
          testsighist_ggH = getHistogram(testhisto_file,'ggH')[0]
          testsighist_bbH = getHistogram(testhisto_file,'bbH')[0]
          for j in range(1,bkghist.GetNbinsX()):
              soverb_ggH = testsighist_ggH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
              soverb_bbH = testsighist_bbH.GetBinContent(j)/math.sqrt(bkghist.GetBinContent(j))
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

#Normalise by bin width except in soverb_plot mode
if not soverb_plot:
    blind_datahist.Scale(1.0,"width")
    total_datahist.Scale(1.0,"width")
    sighist.Scale(1.0,"width")
    if not model_dep: sighist_ggH.Scale(1.0,"width")
    if not model_dep: sighist_bbH.Scale(1.0,"width")
    bkghist.Scale(1.0,"width")


channel=binname[4:6]

#Create stacked plot for the backgrounds
bkg_histos = []
for i,t in enumerate(background_schemes[channel]):
  plots = t['plot_list']
  h = ROOT.TH1F()
  for j,k in enumerate(plots):
    if h.GetEntries()==0 and getHistogram(histo_file,k) is not None:
      h = getHistogram(histo_file,k)[0]
      h.SetName(k)
    else:
      if getHistogram(histo_file,k) is not None:
        h.Add(getHistogram(histo_file,k)[0])
  h.SetFillColor(t['colour'])
  h.SetLineColor(ROOT.kBlack)
  h.SetMarkerSize(0)
  if not soverb_plot: h.Scale(1.0,"width")
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
if args.ratio:
  if(log_x): pads[1].SetLogx(1)
  axish = createAxisHists(2,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax())
  axish[1].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
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
  if custom_y_range:
    axish[0].GetYaxis().SetRangeUser(y_axis_min,y_axis_max)
if not soverb_plot: axish[0].GetYaxis().SetTitle("dN/dM_{#tau#tau} (1/GeV)")
else: axish[0].GetYaxis().SetTitle("Events")
axish[0].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
axish[0].SetMinimum(0.0009)
axish[0].Draw()

#Draw uncertainty band
bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
bkghist.SetMarkerSize(0)

stack.Draw("histsame")
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
if not soverb_plot: blind_datahist.DrawCopy("psame")
axish[0].Draw("axissame")

#Setup legend
legend = plot.PositionedLegend(0.30,0.30,3,0.03)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
if model_dep is True: 
    legend.AddEntry(sighist,"H,h,A#rightarrow#tau#tau"%vars(),"l")
else: 
    legend.AddEntry(sighist_ggH,"gg#phi#rightarrow#tau#tau"%vars(),"l")
    legend.AddEntry(sighist_bbH,"bb#phi#rightarrow#tau#tau"%vars(),"l")
legend.SetFillColor(0)
for legi,hists in enumerate(bkg_histos):
  legend.AddEntry(hists,background_schemes[channel][legi]['leg_text'],"f")
legend.AddEntry(bkghist,"Background uncertainty","f")
if not soverb_plot: legend.AddEntry(blind_datahist,"Observation","P")
legend.Draw("same")
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)
latex.SetTextSize(0.026)
if model_dep is True: 
    latex.DrawLatex(0.61,0.53,"m_{h}^{mod+}, m_{A}=%(mA)s GeV, tan#beta=%(tb)s"%vars())
else: 
    latex.DrawLatex(0.61,0.53,"#sigma(gg#phi)=%(r_ggH)s pb,#sigma(bb#phi)=%(r_bbH)s pb"%vars())

#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.15)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], "2.2 fb^{-1} (13 TeV)", 3);

#Add ratio plot if required
if args.ratio and not soverb_plot:
  total_datahist.Divide(bkghist)
  blind_datahist.Divide(bkghist)
  total_datahist.SetFillColor(plot.CreateTransparentColor(12,0.4))
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(0.7)
  axish[1].SetMaximum(1.3)
  total_datahist.SetMarkerSize(0)
  total_datahist.Draw("e2same")
  blind_datahist.DrawCopy("psame")

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
    sighist_ggH_forratio.SetLineColor(ROOT.kRed)
    sighist_ggH_forratio.Draw("same")
    sighist_bbH_forratio.SetLineColor(ROOT.kRed+3)
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




