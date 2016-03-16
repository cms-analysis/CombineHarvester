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
parser.add_argument('--r',default='0.1',help='Signal XS*BR to scale QCD')
parser.add_argument('--mode',default='prefit',help='Prefit or postfit')
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


args = parser.parse_args()

r = args.r
mode = args.mode
extra_pad = float(args.extra_pad)
custom_x_range = args.custom_x_range
custom_y_range = args.custom_y_range
x_axis_min = float(args.x_axis_min)
x_axis_max = float(args.x_axis_max)
y_axis_min = float(args.y_axis_min)
y_axis_max = float(args.y_axis_max)
log_y=args.log_y
log_x=args.log_x
outname=args.outname + '_'

shape_file = args.file

histo_file = ROOT.TFile(shape_file)

#Store plotting information for different backgrounds 
background_schemes = {'mt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#mu#mu",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'et':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowee",["ZL","ZJ"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'tt':[backgroundComp("QCD", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W","ZL","ZJ"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))],
'em':[backgroundComp("Misidentified e/#mu", ["QCD"], ROOT.TColor.GetColor(250,202,255)),backgroundComp("t#bar{t}",["TT"],ROOT.TColor.GetColor(155,152,204)),backgroundComp("Electroweak",["VV","W"],ROOT.TColor.GetColor(222,90,106)),backgroundComp("Z#rightarrowll",["ZLL"],ROOT.TColor.GetColor(100,192,232)),backgroundComp("Z#rightarrow#tau#tau",["ZTT"],ROOT.TColor.GetColor(248,206,104))]}

bkghist = getHistogram(histo_file,'TotalProcs')[0]
#ztthist = getHistogram(histo_file,'ZTT')[0]
#bkghist = bkghist.Add(ztthist, 1)

total_datahist = getHistogram(histo_file,"data_obs")[0]
blind_datahist = total_datahist.Clone()
total_datahist.SetMarkerStyle(20)
blind_datahist.SetMarkerStyle(20)
blind_datahist.SetLineColor(1)

#channel=binname[4:6]
channel='mt'

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
  axish[1].GetXaxis().SetTitle("M_{#tau#tau}^{vis} (GeV)")
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
axish[0].GetYaxis().SetTitle("Events (1/GeV)")
axish[0].GetXaxis().SetTitle("M_{#tau#tau}^{vis} (GeV)")
axish[0].SetMaximum(extra_pad*bkghist.GetMaximum())
axish[0].SetMinimum(0.0009)
axish[0].Draw()

#Draw uncertainty band
bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
bkghist.SetMarkerSize(0)

stack.Draw("histsame")
bkghist.Draw("e2same")
blind_datahist.DrawCopy("psame")
axish[0].Draw("axissame")

#Setup legend
legend = plot.PositionedLegend(0.30,0.30,3,0.03)
legend.SetTextFont(42)
legend.SetTextSize(0.025)
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
#latex.DrawLatex(0.61,0.53,"m_{h}^{mod+}, m_{A}=%(mA)s GeV, tan#beta=%(tb)s"%vars())

#CMS and lumi labels
plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), extra_pad if extra_pad>0 else 0.15)
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], "2.3 fb^{-1} (13 TeV)", 3);

#Add ratio plot if required
if args.ratio:
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


pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()


#Save as png and pdf with some semi sensible filename
shape_file = shape_file.replace(".root","_%(mode)s"%vars())
shape_file = shape_file.replace("_shapes","")
outname += shape_file
if(log_y): outname+="_logy"
if(log_x): outname+="_logx"
c2.SaveAs("%(outname)s.png"%vars())
c2.SaveAs("%(outname)s.pdf"%vars())




