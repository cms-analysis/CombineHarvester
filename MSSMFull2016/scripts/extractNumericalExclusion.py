#!/usr/bin/env python

#This takes the debug output from plotLimitGrid.py as input file. It removes the boundaries at
#low mA and high tanb from the TGraph contours stored in those files, and writes these
#new, slimmed contours (which represent just the exclusion power of the analysis and not the 
#boundaries of the input model) to a new file. These contours can then be used with TGraph::Eval
#to find tanb for a given mA. In case multiple regions are excluded multiple contours (_0,_1,etc)
#will exist and the bounds of each region can be found individually.
#FIXME: at the moment this script will not work in cases where at a point mA the exclusion runs up to
#a value tanb1 and from a value tanb2 up to 60, if the upper and lower contour are joined up
#elsewhere
import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
from array import array
import copy

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',help='Input file with contour graphs and histograms')
parser.add_argument('--outname', help='Output file name')
args = parser.parse_args()

infile = ROOT.TFile(args.file)
outfile = ROOT.TFile(args.outname,'RECREATE')
contours = {"cont_exp-2","cont_exp-1","cont_exp+1","cont_exp+2","cont_exp0","cont_obs"}
exp0_histo = infile.Get("hist_exp0")
mA_min = exp0_histo.GetXaxis().GetBinLowEdge(0)
tanb_max = exp0_histo.GetYaxis().GetBinUpEdge(exp0_histo.GetNbinsY())

for cont in contours:
  for key in infile.GetListOfKeys():
    if cont in key.GetName() : 
      xbins = []
      ybins = []
      xval = ROOT.Double(0)
      yval = ROOT.Double(0) 
      graph = infile.Get(key.GetName()) 
      for i in range(0,graph.GetN()):
        graph.GetPoint(i,xval,yval)
        if not (xval < mA_min) and not (yval > tanb_max): 
          xbins.append(copy.copy(xval))
          ybins.append(copy.copy(yval))
      slimgraph = ROOT.TGraph(len(xbins),array('d',xbins),array('d',ybins)) 
      outname = key.GetName()
      outname=outname.replace("+","p")
      outname=outname.replace("-","m")
      outfile.WriteTObject(slimgraph,outname)
      

outfile.Close()

