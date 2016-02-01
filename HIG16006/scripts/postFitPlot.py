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
parser.add_argument('--dir', '-d', help='Directory')
parser.add_argument('--file', '-f',help='Input file')
parser.add_argument('--mA',help='Signal m_A')
parser.add_argument('--tanb',help='Signal tanb')
parser.add_argument('--postfitshapes',default=False,action='store_true',help='Run PostFitShapesFromWorkspace')
parser.add_argument('--workspace',default='mhmodp',help='Part of workspace filename right before .root')
parser.add_argument('--mode',default='prefit',help='Prefit or postfit')
parser.add_argument('--blind', default=False,action='store_true',help='Blind data')
parser.add_argument('--ratio', default=False,action='store_true',help='Draw ratio')
parser.add_argument('--x_blind_min',default=100,help='Minimum x for blinding')
parser.add_argument('--x_blind_max',default=1000,help='Maximum x for blinding')


args = parser.parse_args()

mA = args.mA
tb = args.tanb
workspace = args.workspace
mode = args.mode
x_blind_min = args.x_blind_min
x_blind_max = args.x_blind_max

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
    for filename in fnmatch.filter(filenames, '*_mssm.txt'):
      datacard_file = os.path.join(root,filename) 
    for filename in fnmatch.filter(filenames, '*%(workspace)s.root'%vars()):
      workspace_file = os.path.join(root,filename)
      shape_file=workspace_file.replace('.root','_shapes_%(mA)s_%(tb)s.root'%vars())

  os.system('PostFitShapesFromWorkspace -d %(datacard_file)s -w %(workspace_file)s -o %(shape_file)s --print  --freeze mA=%(mA)s,tanb=%(tb)s'%vars())


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
bkghist = getHistogram(histo_file,'TotalBkg')[0]
sighist.Scale(1.0,"width")
bkghist.Scale(1.0,"width")

total_datahist = getHistogram(histo_file,"data_obs")[0]
blind_datahist = total_datahist.Clone()
blind_datahist.SetMarkerStyle(20)

if(args.blind):
  for i in range(0,total_datahist.GetNbinsX()):
    low_edge = total_datahist.GetBinLowEdge(i+1)
    high_edge = low_edge+total_datahist.GetBinWidth(i+1)
    if ((low_edge > x_blind_min and low_edge < x_blind_max) or (high_edge > x_blind_min and high_edge<x_blind_max)):
      blind_datahist.SetBinContent(i+1,0)
      blind_datahist.SetBinError(i+1,0)

blind_datahist.Scale(1.0,"width")


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



 
c2 = ROOT.TCanvas("c2","c2",0,0,800,800)
c2.cd()
if args.ratio:
  pads=plot.TwoPadSplit(0.29,0.005,0.005)
else:
  pads=plot.OnePad()
pads[0].cd()
pads[0].SetLogy(1)
if args.ratio:
  axish = createAxisHists(2,bkghist,0,999)
  axish[1].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
  axish[1].GetYaxis().SetNdivisions(4)
  axish[1].GetYaxis().SetTitle("Obs/Exp")
else:
  axish = createAxisHists(1,bkghist,0,999)
axish[0].GetYaxis().SetTitle("dN/dM_{#tau#tau} (1/GeV)")
axish[0].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
axish[0].SetMaximum(1.2*bkghist.GetMaximum())
axish[0].SetMinimum(0.0009)
axish[0].Draw()
bkghist.SetFillColor(plot.CreateTransparentColor(12,0.4))
bkghist.SetMarkerSize(0)

stack.Draw("histsame")
bkghist.Draw("e2same")
sighist.SetLineColor(ROOT.kRed)
sighist.Draw("histsame")
blind_datahist.DrawCopy("psame")
axish[0].Draw("axissame")

legend = plot.PositionedLegend(0.20,0.20,3,0.03)
legend.SetTextFont(42)
legend.AddEntry(sighist,"H,h,A#rightarrow#tau#tau"%vars(),"l")
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
latex.SetTextSize(0.023)
latex.DrawLatex(0.63,0.63,"m_{h}^{mod+}, m_{A}=%(mA)s GeV, tan#beta=%(tb)s"%vars())

if args.ratio:
  blind_datahist.Divide(bkghist)
  blind_datahist.SetFillColor(plot.CreateTransparentColor(12,0.4))
  pads[1].cd()
  pads[1].SetGrid(0,1)
  axish[1].Draw("axis")
  axish[1].SetMinimum(0.7)
  axish[1].SetMaximum(1.3)
  blind_datahist.Draw("e2psame")


outname = shape_file.replace(".root","_%(mode)s.pdf"%vars())
c2.SaveAs("%(outname)s"%vars())




