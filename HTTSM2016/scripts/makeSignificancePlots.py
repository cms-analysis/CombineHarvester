
# This code is taken from: https://github.com/cms-analysis/flashggFinalFit/blob/master/Plots/FinalResults/makeCombinePlots.py#L317-L424  and modified a bit for tautau channel
# Here is how the code runs:    python makeSignificancePlots.py -d Significance.dat


#!/usr/bin/env python

# Usual reasons to love python imports
import os
import sys
import shlex
import array 

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--datfile",dest="datfile",help="Read from datfile")
parser.add_option("-f","--file",dest="files",default=[],action="append",help="Add a file")
parser.add_option("-o","--outname",dest="outname",help="Name of output pdf/png/C")
parser.add_option("-c","--color",dest="colors",default=[],action="append",help="Set color")
parser.add_option("-s","--style",dest="styles",default=[],action="append",help="Set style")
parser.add_option("-w","--width",dest="widths",default=[],action="append",help="Set width")
parser.add_option("-n","--name",dest="names",default=[],action="append",help="Set name")
parser.add_option("-g","--gname",dest="groupnames",default=[],action="append",help="Set (group) name -for channel compat")
parser.add_option("","--groups",dest="groups",default=1,type="int",help="Set Number of groups")
parser.add_option("-t","--text",dest="text",type="string",default="",help="Add Text")
parser.add_option("","--MHtext",dest="MHtext",default=[],action='append',help="Add more text (eg mh=XXX for chan-compat plots etc). Modify NDC position by ruing  X:Y:text")
parser.add_option("","--blacklistMH",dest="blacklistMH",default=[],action='append',type='float',help="Kill an MH value (limits, pvals, Mu vs MH etc)")

parser.add_option("","--xlab",dest="xlab",type="string",default="",help="Label for x-axis")
parser.add_option("","--xvar",dest="xvar",type="string",default=[],action="append",help="Branch in TTree to pick up as 'x'")
parser.add_option("-e","--expected",dest="expected",default=False,action="store_true",help="Expected only")
parser.add_option("-m","--method",dest="method",type="string",help="Method to run")
parser.add_option("-l","--legend",dest="legend",type="string",help="Legend position - x1,y1,x2,y2")
parser.add_option("--box",dest="box",type="string",help="Legend position - x1,y1,x2,y2,TColor")
parser.add_option("-x","--xaxis",dest="xaxis",type="string",help="x-axis range - x1,x2")
parser.add_option("-y","--yaxis",dest="yaxis",type="string",help="y-axis range - y1,y2")
parser.add_option("","--xbinning",dest="xbinning",type="string",help="force x binning (b,l,h)")
parser.add_option("","--ybinning",dest="ybinning",type="string",help="force y binning (b,l,h)")
parser.add_option("","--groupentry",dest="groupentry",type="string",help="In ch compat, put per XXX (channel,group,etc)")
parser.add_option("","--canv",dest="canv",type="string",default="700,700",help="Canvas size x,y")
parser.add_option("","--chcompLine",dest="chcompLine",type="int",help="For ChannelComp plot put line here splitting two year")
parser.add_option("","--chcompShift",dest="chcompShift",type="float",help="For ChannelComp Asimov - shift to this value")
parser.add_option("","--do1sig",dest="do1sig",default=False,action="store_true",help="For ChannelComp plot only 1 sigma errors")
parser.add_option("","--noComb",dest="noComb",default=False,action="store_true",help="Don't assume the first line is the combined one")
parser.add_option("","--mhval",dest="mhval",default="125.09",help="Don't assume the first line is the combined one")
parser.add_option("","--smoothNLL",dest="smoothNLL",default=False,action="store_true",help="Smooth 1D likelihood scans")
parser.add_option("","--shiftNLL",dest="shiftNLL",type="float",help="Correct NLL to this value")
parser.add_option("","--correctNLL",dest="correctNLL",default=False,action="store_true",help="Correct NLL (occasionally required for failed jobs)")
parser.add_option("","--cleanNLL",dest="cleanNll",default=False,action="store_true",help="Try to remove pike from NLL curve")
parser.add_option("","--addSM",dest="addSM",default=False,action="store_true",help="Add SM Diamond to 2D plot")
parser.add_option("","--limit",dest="limit",default=False,action="store_true",help="Do limit plot")
parser.add_option("","--pval",dest="pval",default=False,action="store_true",help="Do p-value plot")
parser.add_option("","--maxlh",dest="maxlh",default=False,action="store_true",help="Do best fit mu plot")
parser.add_option("","--mh",dest="mh",default=False,action="store_true",help="Do NLL mass scan plot")
parser.add_option("","--mu",dest="mu",default=False,action="store_true",help="Do NLL mu scan plot")
parser.add_option("","--pdf",dest="pdf",default=False,action="store_true",help="Do NLL pdf scan plot")
parser.add_option("","--rv",dest="rv",default=False,action="store_true",help="Do NLL rv scan plot")
parser.add_option("","--rf",dest="rf",default=False,action="store_true",help="Do NLL rf scan plot")
parser.add_option("","--draw2dhist",dest="draw2dhist",default=False,action="store_true",help="Ue 2D hist drawing for the 2D NLL")
parser.add_option("","--get2dhist",dest="get2dhist",default="",help="Get a h2d from the file, separate with : for name of hist (default is h2d)")
parser.add_option("","--bf2d",dest="bf2d",default="",help="Put the best fit point here, dont read from ROOT file. use x,y")
parser.add_option("","--mumh",dest="mumh",default=False,action="store_true",help="Do NLL mu vs mh scan plot")
parser.add_option("","--rvrf",dest="rvrf",default=False,action="store_true",help="Do NLL rv vs rf scan plot")
parser.add_option("","--cvcf",dest="cvcf",default=False,action="store_true",help="Do NLL cv vs cf scan plot")
parser.add_option("","--kglukgam",dest="kglukgam",default=False,action="store_true",help="Do NLL kgluon vs kgamma scan plot")
parser.add_option("","--xdm",dest="xdm",default=False,action="store_true",help="Do NLL x vs delta(m) degenerate")
parser.add_option("","--zmax",dest="zmax",default=10.,type='float',help="Maximum on 2D plots for the Z axis")
parser.add_option("","--mpdfchcomp",dest="mpdfchcomp",default=False,action="store_true",help="Do MultiPdf channel compatbility plot")
parser.add_option("","--perprocchcomp",dest="perprocchcomp",default=False,action="store_true",help="Do PerProc channel compatbility plot")
parser.add_option("","--mpdfmaxlh",dest="mpdfmaxlh",default=False,action="store_true",help="Do MultiPdf best fit mu as a function of MH plot")
parser.add_option("-v","--verbose",dest="verbose",default=True,action="store_true")
parser.add_option("-b","--batch",dest="batch",default=False,action="store_true")
parser.add_option("--it",dest="it",type="string",help="if using superloop, index of iteration")
parser.add_option("--itLedger",dest="itLedger",type="string",help="ledger to keep track of values of each iteration if using superloop")
(options,args)=parser.parse_args()

print "[INFO] Processing Files :"
print " --> raw input :", options.files
if (len(options.files)==1) : options.files=options.files[0].split(",")
print " --> output  :", options.files

# Required for back compatbility and current compatibility it seems
if options.limit: options.method='limit'
if options.pval: options.method='pval'
if options.maxlh: options.method='maxlh'
if options.mh: options.method='mh'
if options.mu: options.method='mu'
if options.pdf: options.method='pdf'
if options.rv: options.method='rv'
if options.rf: options.method='rf'
if options.mumh: options.method='mumh'
if options.rvrf: options.method='rvrf'
if options.cvcf: options.method='cvcf'
if options.kglukgam: options.method='kglukgam'
if options.xdm: options.method='xdm'
if options.mpdfchcomp: options.method='mpdfchcomp'
if options.perprocchcomp: options.method='perprocchcomp'
if options.mpdfmaxlh: options.method='mpdfmaxlh'
if not options.outname: options.outname=options.method

allowed_methods=['pval','limit','maxlh','mh','mu','pdf','mumh','rv','rf','rvrf','cvcf','kglukgam','xdm','mpdfchcomp','perprocchcomp','mpdfmaxlh']
if not options.datfile and options.method not in allowed_methods:
  print 'Invalid method : ' , options.method , '. Must set one of: ', allowed_methods
  sys.exit()

import ROOT as r
outf = r.TFile('%s.root'%options.outname,'RECREATE')

# Load and use the Hgg Paper style
#r.gROOT.ProcessLine(".x hggPaperStyle.C")

if options.batch: r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)

def is_float_try(str):
    try:
      float(str)
      return True
    except ValueError:
      return False
# very fine-grained colour palettee
def set_palette(ncontours=999):
    style=2
    if (style==1):
     # default palette, looks cool
     stops = [0.00, 0.34, 0.61, 0.84, 1.00]
     red   = [0.00, 0.00, 0.77, 0.85, 0.90]
     green = [0.00, 0.81, 1.00, 0.20, 0.00]
     blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)
    elif (style==3):
     
     red   = [ 0.00, 0.90, 1.00] 
     blue  = [ 1.00, 0.50, 0.00] 
     green = [ 0.00, 0.00, 0.00] 
     stops = [ 0.00, 0.50, 1.00] 
     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    elif (style==2):
     # blue palette, looks cool
     #stops = [0.00, 0.14, 0.34, 0.61, 0.84, 1.00]
     #red   = [1.00, 1.00, 1.00, 1.00, 1.00, 1.00]
     #green = [1.00, 1.00, 1.00, 1.00, 1.00, 1.00]
     #blue  = [1.00, 0.80, 0.6, 0.4, 0.2, 1.0]
     stops = [0.00,1.00 ]
     red   = [1.00,0.220 ]
     green = [1.00,0.27 ]
     blue  = [1.00,0.57 ]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    npoints = len(st)
    r.TColor.CreateGradientColorTable(npoints, st, re, gr, bl, ncontours)
    r.gStyle.SetNumberContours(ncontours)

# set defaults for colors etc.
if len(options.colors):
  for i in range(len(options.colors)): 
  	if "r.k" not in options.colors[i]: options.colors[i]=int(options.colors[i])
	else :
	  lcolst = options.colors[i].split(".")[1]
	  add = 0
	  if "+" in lcolst: 
	  	add=int(lcolst.split("+")[1])
		lcolst = lcolst.split("+")[0]
	  if "-" in lcolst: 
	  	add=int(lcolst.split("-")[1])
		lcolst = lcolst.split("-")[0]
	  lcol = int(getattr(r,lcolst))
	  options.colors[i]=lcol+add
while len(options.files)>len(options.colors): options.colors.append(1)
while len(options.files)>len(options.styles): options.styles.append(1)
while len(options.files)>len(options.widths): options.widths.append(1)
while len(options.files)>len(options.names): options.names.append('')
while len(options.files)>len(options.xvar): options.xvar.append("")
while len(options.files)>len(options.groupnames): options.groupnames.append("")

# mh text options, this is just an excuse to dump some text somewhere
mhTextX = []
mhTextY = []
mhTextSize = []
MHtexts = []
for MH in options.MHtext:
  mhtextoptions = MH.split(":")
  MHtexts.append(mhtextoptions[2])
  mhTextX.append(float(mhtextoptions[0]))
  mhTextY.append(float(mhtextoptions[1]))
  if len(mhtextoptions)>3:
    mhTextSize.append(float(mhtextoptions[3]))
  else:
    mhTextSize.append(-1)

# make canvas and dummy hist
#canv = r.TCanvas("c","c",int(options.canv.split(',')[0]),int(options.canv.split(',')[1]))
canv = r.TCanvas("c","c",800,800) # use the default canvas style
#canv = r.TCanvas("c","c") # use the default canvas style
canv.SetTicks(1,1)

if options.xaxis :
  options.xaxis = options.xaxis.split(',')
if not options.xaxis: dummyHist = r.TH1D("dummy","",1,105,145)
else: 
  dummyHist =  r.TH1D("dummy","",1,float(options.xaxis[0]),float(options.xaxis[1]))
  print "====>, ", float(options.xaxis[0]),"   ",float(options.xaxis[1])
dummyHist.GetXaxis().SetTitle('m_{H} (GeV)')
dummyHist.GetXaxis().SetTitleSize(0.05)
dummyHist.GetXaxis().SetTitleOffset(0.9)

# make a helful TLatex box
lat = r.TLatex()
lat.SetTextFont(42)
lat.SetTextSize(0.045)
lat.SetLineWidth(2)
lat.SetTextAlign(11)
lat.SetNDC()
##########################

# Draw the usual propaganda 
def drawGlobals(canv,shifted="False"):

  # draw text 
  
  if (shifted=="True"):
   #print "AM I SHIFTED ? YES"
   #lat.DrawLatex(0.129+0.03,0.93,"CMS Unpublished H#rightarrow#tau#tau")
   #lat.DrawLatex(0.129+0.03,0.93,"CMS H#rightarrow#tau#tau")
   #lat.SetTextSize(0.07)
   lat.DrawLatex(0.129+0.085,0.93,"#bf{CMS} #scale[0.75]{#it{Preliminary}}")
   lat.SetTextSize(0.045)
#   lat.DrawLatex(0.129+0.085+0.04,0.85,"H#rightarrow#tau#tau")
   #lat.DrawLatex(0.71,0.92,options.text)
   lat.DrawLatex(0.7,0.93,options.text)

  elif shifted=="2D":
   #print "AM I SHIFTED ? 2D"
   lat.SetTextSize(0.05)
   lat.DrawLatex(0.1,0.92,"#bf{CMS} #scale[0.75]{#it{Preliminary}}")
   #lat.DrawLatex(0.129+0.04,0.85,"H#rightarrow#tau#tau")
   #lat.DrawLatex(0.13,0.85,"H#rightarrow#tau#tau")
   #lat.SetTextSize(0.07)
   lat.SetTextSize(0.045)
   lat.DrawLatex(0.61,0.92,options.text)

  else:
   #print "AM I SHIFTED ? NO"
   #lat.DrawLatex(0.129,0.93,"CMS Unpublished H#rightarrow#tau#tau")
   #lat.DrawLatex(0.129,0.93,"CMS H#rightarrow#tau#tau")
   #lat.DrawLatex(0.173,0.85,"#splitline{#bf{CMS}}{#it{Preliminary}}")
   #lat.DrawLatex(0.129,0.93,"#bf{CMS} #scale[0.75]{#it{Preliminary}}")
   lat.SetTextSize(0.05)
   lat.DrawLatex(0.1,0.92,"#bf{CMS} #scale[0.75]{#it{Preliminary}}")
   #lat.DrawLatex(0.129+0.04,0.85,"H#rightarrow#tau#tau")
#   lat.DrawLatex(0.13,0.83,"H#rightarrow#tau#tau")
   #lat.SetTextSize(0.07)
   lat.SetTextSize(0.045)
   lat.DrawLatex(0.6,0.92,options.text)

  for mi,MH in enumerate(MHtexts):
    if mhTextSize[mi]>0:
      lat.SetTextSize(mhTextSize[mi])
    lat.DrawLatex(mhTextX[mi],mhTextY[mi],MH)

def cleanSpikes1D(rfix):

 # cindex is where deltaNLL = 0 (pre anything)
 MAXDER = 1.0
 for i,r,m in enumerate(rfix):
   if abs(r[1]) <0.001: cindex = i

 lhs = rfix[0:cindex]; lhs.reverse()
 rhs= rfix[cindex:-1]
 keeplhs = []
 keeprhs = []

 for i,lr,m in enumerate(lhs): 
   if i==0: 
   	prev = lr[1]
	idiff = 1
   if abs(lr[1]-prev) > MAXDER :
   	idiff+=1
   	continue 
   keeplhs.append(lr)
   prev = lr[1]
   idiff=1
 keeplhs.reverse()

 for i,rr,m in enumerate(rhs):
   if i==0: 
   	prev = rr[1]
	idiff = 1
   if abs(rr[1]-prev) > MAXDER : 
   	idiff+=1
   	continue 
   keeprhs.append(rr)
   prev = rr[1]
   idiff=1
 
 rfix = keeplhs+keeprhs
 
 rkeep = []
 #now try to remove small jagged spikes
 for i,r,m in enumerate(rfix):
   if i==0 or i==len(rfix)-1: 
   	rkeep.append(r)
   	continue
   tres = [rfix[i-1][1],r[1],rfix[i+1][1]]
   mean = float(sum(tres))/3.
   mdiff = abs(max(tres)-min(tres))
   if abs(tres[1] - mean) > 0.6*mdiff :continue
   rkeep.append(r)
 return rkeep

# Plot 1 - P-values plot 
def pvalPlot(allVals):
  
  canv.Clear()

  if options.verbose: print 'Plotting pvalue...'
  canv.SetLogy(True)
  mg = r.TMultiGraph()
  if not options.legend: leg = r.TLegend(0.14,0.65,0.4,0.8)
  #if not options.legend: leg = r.TLegend(0.6,0.35,0.89,0.45)
  else:
    options.legend[-1]=options.legend[-1].replace("\n","")
    leg = r.TLegend(float(options.legend[0]),float(options.legend[1]),float(options.legend[2]),float(options.legend[3]))
  #leg.SetFillColor(0)
  leg.SetBorderSize(0)
  # make graphs from values
  for k, values in enumerate(allVals):
    minpvalue=99999.
    minpvalueX=99999.
    pvalat125=999999.
    graph = r.TGraph()
    for j in range(len(values)):
      graph.SetPoint(j,values[j][0],values[j][1])
      if (minpvalue > values[j][1]): 
        minpvalue = values[j][1]
        minpvalueX =values[j][0]
      if options.verbose or abs(values[j][0]-125.09)<0.1 or  values[j][0]==125.0 : 
        print options.names[k] ,' at ', values[j][0], " signif ",  r.RooStats.PValueToSignificance(values[j][1])
        pvalat125=values[j][1]
      #print "debug minpval  for ",options.names[k], " at ", values[j][0], " ", minpvalue, "   " , r.RooStats.PValueToSignificance(minpvalue), "values[j][1] " , values[j][1], " ", r.RooStats.PValueToSignificance(values[j][1])
    
  #  with open(options.itLedger, "a") as myfile:
  #      myfile.write("%s %f %f\n" % ( (options.names[k].replace(" ","_"))+" "+options.it, minpvalue,minpvalueX ))
  #      if ("Obs" in options.names[k] ) :
  #        myfile.write("%s %f %f\n" % ( (options.names[k].replace(" ","_"))+"_at125"+" "+options.it, pvalat125,125. ))

    graph.SetLineColor(int(options.colors[k]))
    graph.SetLineStyle(int(options.styles[k]))
    graph.SetLineWidth(int(options.widths[k]))
    if options.names[k]!="-1": leg.AddEntry(graph,options.names[k],'L')
    mg.Add(graph)
 
  # draw dummy hist and multigraph
  dummyHist.GetYaxis().SetTitle('Local p-value')
  dummyHist.GetYaxis().SetTitleSize(0.05)
  mg.Draw("A")
  if (options.xaxis) :
      print mg.GetXaxis()
      #mg.GetXaxis().SetLimits(float(options.xaxis[0]),float(options.xaxis[1]))
      dummyHist.GetXaxis().SetRangeUser(float(options.xaxis[0]),float(options.xaxis[1]))
      #canv.Modified()
      print mg.GetXaxis().GetXmin() 
  if not options.yaxis:
    dummyHist.SetMinimum(mg.GetYaxis().GetXmin())
    dummyHist.SetMaximum(mg.GetYaxis().GetXmax())
  else:
    print "---->",options.yaxis.split('-')[0]
    dummyHist.SetMinimum(float(options.yaxis.split('-')[0]))
    dummyHist.SetMaximum(float(options.yaxis.split('-')[1]))
    #print "y1,y2", options.yaxis.split(',')[0], " , ", options.yaxis.split(',')[1]
    
  dummyHist.SetLineColor(0)
  dummyHist.SetStats(0)
  dummyHist.Draw("AXIS")
  mg.Draw("L")
  dummyHist.Draw("AXIGSAME")

  # draw sigma lines
  sigmas=[1,2,3,4,5,6]
  lines=[]
  labels=[]
  for i,sig in enumerate(sigmas):
    y = r.RooStats.SignificanceToPValue(sig)
    if options.verbose: print sig, y
    if not options.xaxis:  lines.append(r.TLine(105,y,145,y))
    else : 
        axmin = float(options.xaxis[0])
        axmax = float(options.xaxis[1])
        print "set line at  " ,axmin, " " , axmax
        lines.append(r.TLine(axmin,y,axmax,y))

    lines[i].SetLineWidth(2)
    lines[i].SetLineStyle(2)
    lines[i].SetLineColor(13) # greay Lines 
    labels.append(r.TLatex(140, y * 1.1, "%d #sigma" % (i+1)))
    labels[i].SetTextColor(13)
    labels[i].SetTextAlign(11);
    if not options.yaxis:
      if y<=mg.GetYaxis().GetXmax() and y>=mg.GetYaxis().GetXmin():
        lines[i].Draw('SAME')
        labels[i].Draw('SAME')
    else:
      if y<=float(options.yaxis.split('-')[1]) and y>=float(options.yaxis.split('-')[0]):
        lines[i].Draw('SAME')
        labels[i].Draw('SAME')
  # draw legend
  leg.Draw()
  #canv.RedrawAxis()
  drawGlobals(canv)
  # print canvas
  canv.Update()
  if not options.batch: raw_input("Looks ok?")
  canv.Print('%s.pdf'%options.outname)
  canv.Print('%s.root'%options.outname)
  canv.Print('%s.png'%options.outname)
  canv.Print('%s.C'%options.outname)
  canv.SetName(options.outname)
  outf.cd()
  canv.Write()


def runStandard():
  config = []
  for k, f in enumerate(options.files):
    tf = r.TFile(f)
    print f
    tree = tf.Get('limit')
    values=[]
    for i in range(tree.GetEntries()):
      tree.GetEntry(i)
      skippoint = False
      for mhb in options.blacklistMH:
    	if abs(mhb-tree.mh)<0.01 : 
		skippoint = True
		break
      if skippoint: continue
      values.append([tree.mh, tree.limit])
    values.sort(key=lambda x: x[0])
    config.append(values)

  if options.method=='pval': pvalPlot(config)
  elif options.method=='limit': limitPlot(config)
  elif options.method=='maxlh': maxlhPlot(config)

def read1D(file,x,i,xtitle):
  tree = file.Get('limit')
  tree.Draw('2*deltaNLL:%s'%x,'','')
  gr = r.gROOT.FindObject('Graph').Clone('gr_%s_%d'%(x,i))
  gr.SetTitle("")
  gr.GetXaxis().SetTitle(xtitle)
  gr.GetYaxis().SetTitle("-2 #Delta LL")

  gr.Sort()
  last = None
  for i in range(gr.GetN(),0,-1):
    if gr.GetX()[i-1] == last:
      gr.RemovePoint(i-1)
    last = gr.GetX()[i-1]
  return gr










def run():
  if options.verbose:
    print options.method
    print options.files
    print options.colors
    print options.styles
    print options.widths
    print options.names
    print options.xaxis
    print options.yaxis

  if options.method=='pval' or options.method=='limit' or options.method=='maxlh':
    runStandard()
  elif options.method=='mh' or options.method=='mu' or options.method=='rv' or options.method=='rf' or options.method=='mpdfchcomp'  or options.method=='perprocchcomp' or options.method=='mpdfmaxlh':
    path = os.path.expandvars('$CMSSW_BASE/src/flashggFinalFit/Plots/FinalResults/rootPalette.C')
    if not os.path.exists(path):
      sys.exit('ERROR - Can\'t find path: '+path) 
    r.gROOT.ProcessLine(".x "+path)
    path = os.path.expandvars('$CMSSW_BASE/src/flashggFinalFit/Plots/FinalResults/ResultScripts/GraphToTF1.C')
    if not os.path.exists(path):
      sys.exit('ERROR - Can\'t find path: '+path) 
    r.gROOT.LoadMacro(path)
    if options.method=='mpdfchcomp':
      plotMPdfChComp("perTag")
    if options.method=='perprocchcomp':
      plotMPdfChComp("perProc")
    elif options.method=='mpdfmaxlh':
      plotMPdfMaxLH()
    else:
      if len(options.xvar)>0:
        plot1DNLL(False,options.xvar[0])
      else:
        plot1DNLL(False)
  elif options.method=='mumh':
    #plot2DNLL("MH","r","m_{H} (GeV)","#sigma/#sigma_{SM}")
    plot2DNLL("MH","r","m_{H} (GeV)","#mu")
  elif options.method=='rvrf':
    plot2DNLL("RF","RV","#mu_{ggH,ttH}","#mu_{VBF,VH}")
  elif options.method=='cvcf':
    plot2DNLL("CV","CF","#kappa_{V}","#kappa_{f}")
  elif options.method=='xdm':
    plot2DNLL("x","deltaM","x","#Delta m (GeV)")
  elif options.method=='kglukgam':
    plot2DNLL("kgamma","kgluon","#kappa_{#gamma}","#kappa_{g}")

# __MAIN__

if options.datfile:
  d = open(options.datfile)
  for line in d.readlines():
    if line.startswith('#'): continue
    if line=='\n': continue
    config={}
    line = line.replace('\=','EQUALS')
    for opt in line.split(':'):
      #print opt.split('=')[0]
      config[opt.split('=')[0]] = opt.split('=')[1].replace('EQUALS','=').strip('\n').split(',')
      #print line 
      #print opt.split('=')[0], " " , opt.split('=')[1].replace('EQUALS','=').strip('\n').split(',')  
    for opt in ['colors','styles','widths']:
      if opt in config.keys():
        config[opt] = [int(x) for x in config[opt]]
    
    for key, item in config.items():
      if len(item)==1 and key in ['method','text','outname','legend','yaxis','xaxis']:
        item=item[0].strip('\n')
      setattr(options,key,item)

    if options.verbose: print options
    run()


else:
  run()

print 'All canvases written to:', outf.GetName()
outf.Close()
