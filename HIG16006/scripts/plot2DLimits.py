import ROOT
import math
import sys
import os
import numpy as np
import fnmatch
import json 
ROOT.gROOT.SetBatch(ROOT.kTRUE)


def getLimitValue(channel,workingpoint,mtcut,masspoint,process,plot_error=False):
  data = {}
  filename = "mssm_optimisation_round2_%(process)s_%(workingpoint)s%(mtcut)s_%(channel)s.json"%vars()
  with open(filename) as jsonfile:
    data = json.load(jsonfile)
    if not plot_error:
      xval = data[masspoint]["exp0"]
    else:
      xval = (data[masspoint]["exp+1"]-data[masspoint]["exp-1"])
  return xval

def set_plot_style():
  NRGBs = 5;
  NCont = 255;
  stops = {0.00,0.34,0.61,0.84,1.00}
  red = {0.00,0.00,0.87,1.00,0.51}
  green = {0.00,0.81,1.00,0.20,0.00} 
  blue = {0.51,1.00,0.12,0.00,0.00}
  ROOT.TColor.CreateGradientColorTable(NRGBs,np.array(stops),np.array(red),np.array(green),np.array(blue),NCont)
  ROOT.gStyle.SetNumberContours(NCont)

set_plot_style()
#ROOT.TColor.SetPalette(51,0)

workingpoints={"vloose":1,"loose":2,"medium":3,"tight":4,"vtight":5}
mtcut={"mt30":1,"mt40":2,"mt50":3,"mt60":4,"mt70":5}
masspoints = {"90.0","100.0","110.0","120.0","130.0","140.0","160.0","180.0","200.0","250.0","350.0","400.0","450.0","500.0","600.0","700.0","800.0","900.0","1000.0","1200.0","1400.0","1600.0","1800.0","2000.0", "2300.0","2600.0","2900.0","3200.0"}
processes = {"bbH","ggH"}
channels = {"et","mt"}

for process in processes:
  for ch in channels:
    for massp in masspoints:
      limit_histo = ROOT.TH2D("%(process)s_%(ch)s_%(massp)s"%vars(),";iso WP;m_{T} cut",5,0.5,5.5,5,0.5,5.5)
      limit_width_histo = ROOT.TH2D("width_%(process)s_%(ch)s_%(massp)s"%vars(),";iso WP;m_{T} cut",5,0.5,5.5,5,0.5,5.5)
      limit_histo_diffaswidthfrac = ROOT.TH2D("widthfrac_%(process)s_%(ch)s_%(massp)s"%vars(),";iso WP;m_{T} cut",5,0.5,5.5,5,0.5,5.5)

      for wp_key in workingpoints:
        limit_histo.GetXaxis().SetBinLabel(workingpoints[wp_key],wp_key)
        limit_width_histo.GetXaxis().SetBinLabel(workingpoints[wp_key],wp_key)
        limit_histo_diffaswidthfrac.GetXaxis().SetBinLabel(workingpoints[wp_key],wp_key)

      for mt_key in mtcut:
        limit_histo.GetYaxis().SetBinLabel(mtcut[mt_key],mt_key)
        limit_histo_diffaswidthfrac.GetYaxis().SetBinLabel(mtcut[mt_key],mt_key)
        limit_width_histo.GetYaxis().SetBinLabel(mtcut[mt_key],mt_key)


      for wp_key in workingpoints:
        for mt_key in mtcut:
          limit_histo.Fill(workingpoints[wp_key],mtcut[mt_key],getLimitValue(ch,wp_key,mt_key,massp,process,False))
          limit_histo_diffaswidthfrac.Fill(workingpoints[wp_key],mtcut[mt_key],getLimitValue(ch,wp_key,mt_key,massp,process,False))
          limit_width_histo.Fill(workingpoints[wp_key],mtcut[mt_key],getLimitValue(ch,wp_key,mt_key,massp,process,True))


      minx = ROOT.Long(0)
      miny = ROOT.Long(0)
      minz = ROOT.Long(0)

      limit_histo.GetMinimumBin(minx,miny,minz)
      minimumbin = limit_histo.GetBinContent(minx,miny)
      minimumwidth = limit_width_histo.GetBinContent(minx,miny)
      for ilim in range(1,limit_histo.GetNbinsX()+1):
        for jlim in range(1,limit_histo.GetNbinsY()+1):
          limit_histo_diffaswidthfrac.SetBinContent(ilim,jlim,float((limit_histo_diffaswidthfrac.GetBinContent(ilim,jlim)-minimumbin)/minimumwidth))
      print limit_histo.GetBinContent(minx,miny)
      print limit_histo_diffaswidthfrac.GetBinContent(minx,miny)
      limit_histo.Scale(1./(limit_histo.GetBinContent(minx,miny)))
      print limit_histo.GetBinContent(minx,miny)
      limit_histo_minpoint = ROOT.TGraph(1)
      limit_histo_minpoint.SetPoint(0,limit_histo.GetXaxis().GetBinCenter(minx),limit_histo.GetYaxis().GetBinCenter(miny))
      


      c1 = ROOT.TCanvas()
      limit_histo.SetStats(0)
      limit_histo.Draw("COLZ")
      limit_histo_minpoint.Draw("*SAME")
      c1.SaveAs("optimisation_mttot_EXP_%(process)s_%(ch)s_%(massp)s.pdf"%vars())
      limit_histo.GetZaxis().SetRangeUser(0.99,2)
      limit_histo.Draw("COLZ")
      limit_histo_minpoint.Draw("*SAME")
      c1.SaveAs("optimisation_mttot_EXP_%(process)s_%(ch)s_%(massp)s_range12.pdf"%vars())
      limit_histo_diffaswidthfrac.SetStats(0)
      limit_histo_diffaswidthfrac.Draw("COLZ")
      limit_histo_minpoint.Draw("*SAME")
      c1.SaveAs("optimisation_mttot_EXPDiffAsWidthFrac_%(process)s_%(ch)s_%(massp)s.pdf"%vars())
