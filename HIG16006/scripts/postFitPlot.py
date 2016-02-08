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
parser.add_argument('--blind', default=True,action='store_true',help='Blind data with hand chosen range')
parser.add_argument('--x_blind_min',default=100,help='Minimum x for blinding')
parser.add_argument('--x_blind_max',default=4000,help='Maximum x for blinding')
parser.add_argument('--ratio', default=True,action='store_true',help='Draw ratio plot')
parser.add_argument('--custom_x_range', help='Fix x axis range', action='store_true', default=False)
parser.add_argument('--x_axis_min',  help='Fix x axis minimum', default=90.0)
parser.add_argument('--x_axis_max',  help='Fix x axis maximum', default=1000.0)
parser.add_argument('--custom_y_range', help='Fix y axis range', action='store_true', default=False)
parser.add_argument('--y_axis_min',  help='Fix y axis minimum', default=0.001)
parser.add_argument('--y_axis_max',  help='Fix y axis maximum', default=100.0)
parser.add_argument('--extra_pad', help='Fraction of extra whitespace at top of plot',default=0.0)


args = parser.parse_args()

mA = args.mA
mPhi = args.mPhi
tb = args.tanb
r_ggH = args.r_ggH
r_bbH = args.r_bbH
workspace = args.workspace
mode = args.mode
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

if args.dir and args.file and not args.postfitshapes:
  print 'Provide either directory or filename, not both'
  sys.exit(1)


if not args.dir and not args.file and not args.postfitshapes:
  print 'Provide one of directory or filename'
  sys.exit(1)

if args.postfitshapes and not args.dir:
  print 'Provide directory when running with --postfitshapes option'
  sys.exit(1)


if args.postfitshapes:
  for root,dirnames,filenames in os.walk(args.dir):
    for filename in fnmatch.filter(filenames, '*.txt.cmb'):
      datacard_file = os.path.join(root,filename) 
    for filename in fnmatch.filter(filenames, '*%(workspace)s.root'%vars()):
      workspace_file = os.path.join(root,filename)
      print workspace_file
      shape_file=workspace_file.replace('.root','_shapes_%(mA)s_%(tb)s.root'%vars())
  
  if model_dep is True :
    print "using mA and tanb"
    freeze = 'mA='+mA+',tanb='+tb 
  else: 
    freeze = 'MH='+mPhi+',r_ggH='+r_ggH+',r_bbH='+r_bbH 
  print 'PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --print --freeze %(freeze)s'%vars()
  os.system('PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --print --freeze %(freeze)s'%vars())


if not args.postfitshapes:
  if args.dir:
    for root,dirnames,filenames in os.walk(args.dir):
      for filename in fnmatch.filter(filenames, '*_shapes_%(mA)s_%(tb)s.root'%vars()):
        shape_file = os.path.join(root,filename)
  elif args.file:
    shape_file=args.file

histo_file = ROOT.TFile(shape_file)

background_schemes = {'mt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#mu#mu",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'et':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowee",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'tt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#tau#tau",["ZTT","ZL","ZJ"],ROOT.TColor.GetColor(248,206,104))],
'em':[backgroundComp("Misidentified e/#mu", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))]}

[sighist,binname] = getHistogram(histo_file,'TotalSig')
if not model_dep: sighist_ggH = getHistogram(histo_file,'ggH')[0]
if not model_dep: sighist_bbH = getHistogram(histo_file,'bbH')[0]
bkghist = getHistogram(histo_file,'TotalBkg')[0]
sighist.Scale(1.0,"width")
if not model_dep: sighist_ggH.Scale(1.0,"width")
if not model_dep: sighist_bbH.Scale(1.0,"width")
bkghist.Scale(1.0,"width")

total_datahist = getHistogram(histo_file,"data_obs")[0]
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)

if(args.blind):
  for i in range(0,total_datahist.GetNbinsX()):
    low_edge = total_datahist.GetBinLowEdge(i+1)
    high_edge = low_edge+total_datahist.GetBinWidth(i+1)
    if ((low_edge > x_blind_min and low_edge < x_blind_max) or (high_edge > x_blind_min and high_edge<x_blind_max)):
      blind_datahist.SetBinContent(i+1,0)
      blind_datahist.SetBinError(i+1,0)

blind_datahist.Scale(1.0,"width")
total_datahist.Scale(1.0,"width")


channel=binname[4:6]


bkg_histos = []
for i,t in enumerate(background_schemes[channel]):
  plots = t['plot_list']
  h = ROOT.TH1F()
  for j,k in enumerate(plots):
    if j==0:
      h = getHistogram(histo_file,k)[0]
      h.SetName(k)
    else:
      h.Add(getHistogram(histo_file,k)[0])
  h.SetFillColor(t['colour'])
  h.SetLineColor(ROOT.kBlack)
  h.SetMarkerSize(0)
  h.Scale(1.0,"width")
  bkg_histos.append(h)

stack = ROOT.THStack("hs","")
for hists in bkg_histos:
  stack.Add(hists)


plot.ModTDRStyle(r=0.06, l=0.12)
c2 = ROOT.TCanvas()
c2.cd()
if args.ratio:
  pads=plot.TwoPadSplit(0.29,0.005,0.005)
else:
  pads=plot.OnePad()
pads[0].cd()
pads[0].SetLogy(1)
if args.ratio:
  axish = createAxisHists(2,bkghist,bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax())
  axish[1].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
  axish[1].GetYaxis().SetNdivisions(4)
  axish[1].GetYaxis().SetTitle("Obs/Exp")
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
axish[0].GetYaxis().SetTitle("dN/dM_{#tau#tau} (1/GeV)")
axish[0].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
axish[0].SetMinimum(0.0009)
axish[0].Draw()

bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
bkghist.SetMarkerSize(0)

stack.Draw("histsame")
bkghist.Draw("e2same")
if model_dep is True: 
    sighist.SetLineColor(ROOT.kRed)
    sighist.Draw("histsame")
else: 
    sighist_ggH.SetLineColor(ROOT.kBlue)
    sighist_bbH.SetLineColor(ROOT.kBlue + 3)
    sighist_ggH.Draw("histsame")
    sighist_bbH.Draw("histsame")
blind_datahist.DrawCopy("psame")
axish[0].Draw("axissame")

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
legend.AddEntry(blind_datahist,"Observation","P")
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

plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.15)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], "2.2 fb^{-1} (13 TeV)", 3);

if args.ratio:
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

pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

outname = shape_file.replace(".root","_%(mode)s.pdf"%vars())
c2.SaveAs("%(outname)s"%vars())
outname = shape_file.replace(".root","_%(mode)s.png"%vars())
c2.SaveAs("%(outname)s"%vars())




