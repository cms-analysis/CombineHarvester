#!/usr/bin/env python

import ROOT
import argparse
import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input mlfit file')
parser.add_argument('-p', '--parameters', help='parameters for listing correlations')
parser.add_argument('-o', '--outname', default='correlationMatrix', help='output name')

args = parser.parse_args()

fin = ROOT.TFile(args.input.split(':')[0])
rfr = fin.Get(args.input.split(':')[1])
parameters = args.parameters.split(",")
outname=args.outname

plot.SetCorrMatrixPalette()
correlation_matrix = ROOT.TH2F("correlation_matrix","",len(parameters),0,len(parameters),len(parameters),0,len(parameters))
for i in range(0,len(parameters)):
    correlation_matrix.GetXaxis().SetBinLabel(i+1,parameters[i])
    correlation_matrix.GetYaxis().SetBinLabel(i+1,parameters[i])


all_pars = rfr.floatParsFinal()
correlations = []
for p1 in range(0,len(parameters)):
    for p2 in range(0,len(parameters)):
            param1=parameters[p1]
            param2=parameters[p2]
            correlation_matrix.SetBinContent(p1+1,p2+1,rfr.correlation(param1,param2))
            correlations.append((param1, param2,
                rfr.correlation(param1, param2)))

correlation_matrix.SetStats(0)
correlation_matrix.GetZaxis().SetRangeUser(-1,1)
correlation_matrix.GetYaxis().SetLabelSize(0.02)
correlation_matrix.GetXaxis().SetLabelSize(0.02)
correlation_matrix.GetZaxis().SetLabelSize(0.02)


outfile = ROOT.TFile("%(outname)s.root"%vars(),"RECREATE")
correlation_matrix.Write()
outfile.Close()

c2 = ROOT.TCanvas()
c2.SetCanvasSize(800,700)
c2.cd()
pads=plot.OnePad()
pads[0].SetLeftMargin(0.25)
pads[0].SetBottomMargin(0.25)
#pads[0].SetRightMargin(0.15)
c2.SetFixedAspectRatio()
pads[0].cd()
correlation_matrix.Draw("COLZTEXT")
c2.SaveAs("%(outname)s.pdf"%vars())
c2.SaveAs("%(outname)s.png"%vars())

