import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def m6bandFromVEps(h2, best, xmin, xmax, points, toys):
    c68 = ROOT.TGraphAsymmErrors()
    c95 = ROOT.TGraphAsymmErrors()
    sm = ROOT.TGraph()
    h2 = h2.Clone(h2.GetName()+'_th2_prob')
    for ix in xrange(1, h2.GetNbinsX()+1):
        for iy in xrange(1, h2.GetNbinsY()+1):
            hx = h2.GetXaxis().GetBinCenter(ix)
            hy = h2.GetYaxis().GetBinCenter(iy)
            h2.SetBinContent(ix, iy, ROOT.TMath.Prob(h2.GetBinContent(ix,iy),2))
 
    # h2->Draw("COLZ"); c1->Print("~/public_html/drop/plot.png"); 
    # make histogram of log of relative shift wrt SM
    v0 = 246.22
    # TH1D *histos[99]; double x[99];
    # if (points > 98) points = 98;

    histos = []
    x = [0.] * points
    for p in xrange(points):
        x[p] = xmin * math.exp(p*math.log(xmax/xmin)/(points-1))
        print 'x[%i] = %f' % (p, x[p])
        histos.append(ROOT.TH1D('h%d' % p,'', 10000, -5., 5.))
        
    for t in xrange(toys):
        v = ROOT.Double()
        eps = ROOT.Double()
        h2.GetRandom2(v,eps)
        for p in xrange(points):
            histos[p].Fill((1+eps)*math.log(x[p]/v) - math.log(x[p]/v0))
    # get 68% and 95% bands
    c68.Set(points)
    c95.Set(points)
    sm.Set(points)
    vbest = best.GetX()[0]
    epsbest = best.GetY()[0]
    for p in xrange(points):
        ybest = math.exp((1+epsbest)*math.log(x[p]/vbest))
        ysm = math.exp(math.log(x[p]/v0))
        c68.SetPoint(p, x[p], ybest)
        c95.SetPoint(p, x[p], ybest)
        sm.SetPoint(p, x[p], ysm)
        c68.SetPointError(p, 0.,0.,  0.,0.)
        c95.SetPointError(p, 0.,0.,  0.,0.)
        histos[p].Scale(1.0/histos[p].Integral(0,histos[p].GetNbinsX()+1))
        prob0 = histos[p].GetBinContent(0)
        for ix in xrange(1, histos[p].GetNbinsX() + 1):
            prob  = prob0 + histos[p].GetBinContent(ix)
            if prob >= 0.025 and prob0 < 0.025:
                c95.GetEYlow()[p] = ybest - (x[p]/v0)*math.exp(histos[p].GetBinLowEdge(ix))
            elif prob >= 0.16 and prob0 < 0.16:
                c68.GetEYlow()[p] = ybest - (x[p]/v0)*math.exp(histos[p].GetBinLowEdge(ix))
            elif prob > 0.84 and prob0 <= 0.84:
                c68.GetEYhigh()[p] = (x[p]/v0)*math.exp(histos[p].GetBinLowEdge(ix)) - ybest
            elif prob > 0.975 and prob0 <= 0.975:
                c95.GetEYhigh()[p] = (x[p]/v0)*math.exp(histos[p].GetBinLowEdge(ix)) - ybest
            prob0 = prob
    
        #printf("at x[%d] = %.0f GeV, c = %.5f -%.5f/+%.5f\n", p, x[p], ybest, c68->GetEYlow()[p],  c68->GetEYhigh()[p]);
    c68.SetFillColor(ROOT.kGreen)
    c95.SetFillColor(ROOT.kYellow)
    return (c68, c95, sm)

def GetFromTFile(filename, object):
    fin = ROOT.TFile(filename)
    obj = ROOT.gDirectory.Get(object).Clone()
    fin.Close()
    return obj

ROOT.TH1.AddDirectory(False)

parser = argparse.ArgumentParser()
parser.add_argument('--th2-input', help='input file containing the 2D NLL scan in the format FILE.root:NAME')
parser.add_argument('--best-fit-input', help='input file containing the best fit TGraph in the format FILE.root:NAME')
parser.add_argument('--kappa-results', help='json file containing kappa-model fit results')
parser.add_argument('--title-right', default='', help='title text')
parser.add_argument('--output', default='Meps', help='output filename')
parser.add_argument('--masses', help='particle masses')
args = parser.parse_args()

SM_VEV = 246.22


plot.ModTDRStyle(l=0.18)

# Get the TH2 input
hist_nll = GetFromTFile(*args.th2_input.split(':'))
best_fit = GetFromTFile(*args.best_fit_input.split(':'))

c68, c95, sm = m6bandFromVEps(hist_nll, best_fit, 0.07, 300, 40, 20000)

best_line = c68.Clone()


plot.Set(sm, LineColor=ROOT.kRed, LineWidth=3, LineStyle=7)
plot.Set(best_line, LineColor=ROOT.kBlue, LineWidth=3)

with open(args.kappa_results.split(':')[0]) as jsonfile:
    k1_res = json.load(jsonfile)[args.kappa_results.split(':')[1]]

masses = args.masses.split(',')
mass_dict = {}
for m in masses:
    particle = m.split(':')[0]
    mass = float(m.split(':')[1])
    mass_dict[particle] = mass

kappa_graph = ROOT.TGraphAsymmErrors(len(k1_res.keys()))



canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()

haxis = plot.CreateAxisHist(c68, True)
haxis.GetXaxis().SetTitle('Particle mass [GeV]')
haxis.GetYaxis().SetTitle('#kappa_{F}#frac{m_{F}}{v} or #sqrt{#kappa_{V}}#frac{m_{V}}{v}')
haxis.GetYaxis().SetTitleOffset(haxis.GetYaxis().GetTitleOffset()* 0.9)
haxis.SetMinimum(1E-4)
pads[0].SetLogx(True)
pads[0].SetLogy(True)
pads[0].cd()
haxis.Draw()
c95.Draw('SAME3')
c68.Draw('SAME3')
sm.Draw('LSAME')
best_line.Draw('LXSAME')

xmin = haxis.GetXaxis().GetXmin()
xmax = haxis.GetXaxis().GetXmax()
ymin = haxis.GetMinimum()
ymax = haxis.GetMaximum()
print (xmin, xmax, ymin, ymax)

pl = pads[0].GetLeftMargin()
pr = pads[0].GetRightMargin()
pt = pads[0].GetTopMargin()
pb = pads[0].GetBottomMargin()

latex = ROOT.TLatex()
latex.SetNDC()
plot.Set(latex, TextAlign=21, TextSize=0.04)

for i, POI in enumerate(k1_res):
    particle = POI.replace('kappa_','')
    mass = mass_dict[particle]
    kappa = k1_res[POI]['Val']
    if particle in ['W', 'Z']:
        kappa = math.sqrt(kappa)
    reduced = kappa * mass / SM_VEV
    err_hi = (abs(k1_res[POI]['ErrorHi'])) * mass / SM_VEV
    err_lo = (abs(k1_res[POI]['ErrorLo'])) * mass / SM_VEV
    kappa_graph.SetPoint(i, mass, reduced)
    kappa_graph.SetPointError(i, 0, 0, err_lo, err_hi)
    print (particle, reduced, reduced+err_hi)
    pad_x = (math.log(mass) - math.log(xmin))/(math.log(xmax) - math.log(xmin))
    pad_y = (math.log(reduced+err_hi) - math.log(ymin))/(math.log(ymax) - math.log(ymin))
    pad_x = pl + (1-pl-pr) * pad_x
    if particle == 'W': pad_x -= 0.01
    if particle == 'Z': pad_x += 0.01
    pad_y = (pb + (1-pt-pb) * pad_y) + 0.025
    text = particle
    if particle in ['tau', 'mu']:
        text = '#' + text
    latex.DrawLatex(pad_x, pad_y, text)

plot.Set(kappa_graph, LineWidth=3)
kappa_graph.Draw('P0SAME')

legend = ROOT.TLegend(0.20, 0.68, 0.6, 0.78, '', 'NBNDC')
legend.AddEntry(kappa_graph, 'Observed (68% CL)', 'EP')
legend.AddEntry(sm, 'SM Higgs Boson', 'L')
legend.Draw()

legend2 = ROOT.TLegend(0.68, 0.16, 0.93, 0.37, '', 'NBNDC')
legend2.SetHeader('(M, #epsilon) fit')
legend2.AddEntry(best_line, 'Observed', 'L')
legend2.AddEntry(c68, '68% CL', 'F')
legend2.AddEntry(c95, '95% CL', 'F')
legend2.Draw()

plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1 Internal}', 11, 0.045, 0.035, 1.2)

pads[0].RedrawAxis()


canv.Print('.pdf')
canv.Print('.png')

fout = ROOT.TFile('%s.root' % args.output, 'RECREATE')
fout.WriteTObject(c68, 'MepsFit68')
fout.WriteTObject(c95, 'MepsFit95')
fout.WriteTObject(kappa_graph, 'ReducedKappas')
fout.WriteTObject(sm, 'SMExpected')
fout.Close()


