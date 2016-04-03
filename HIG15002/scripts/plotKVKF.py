#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.plotting as plot
import argparse


def read(scan, param_x, param_y, file):
    # print files
    goodfiles = [f for f in [file] if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    graph = plot.TGraph2DFromTree(
        limit, param_x, param_y, '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0 && deltaNLL < 100')
    best = plot.TGraphFromTree(
        limit, param_x, param_y, 'quantileExpected > -0.5 && deltaNLL == 0')
    plot.RemoveGraphXDuplicates(best)
    assert(best.GetN() == 1)
    graph.SetName(scan)
    best.SetName(scan + '_best')
    # graph.Print()
    return (graph, best)


def fillTH2(hist2d, graph):
    for x in xrange(1, hist2d.GetNbinsX() + 1):
        for y in xrange(1, hist2d.GetNbinsY() + 1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            val = graph.Interpolate(xc, yc)
            hist2d.SetBinContent(x, y, val)


def fixZeros(hist2d):
    for x in xrange(1, hist2d.GetNbinsX() + 1):
        for y in xrange(1, hist2d.GetNbinsY() + 1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            if hist2d.GetBinContent(x, y) == 0:
                # print 'Bin at (%f,%f) is zero!' % (xc, yc)
                hist2d.SetBinContent(x, y, 1000)


def makeHist(name, bins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(bins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(bins) - 1.)) - 1E-5
    hist = ROOT.TH2F(name, '', bins, graph2d.GetXmin() - binw_x, graph2d.GetXmax() +
                     binw_x, bins, graph2d.GetYmin() - binw_y, graph2d.GetYmax() + binw_y)
    return hist

SETTINGSC = {
    'tau': {
        'xvar': 'kappa_V_tautau',
        'yvar': 'kappa_F_tautau',
        'fill_color': ROOT.TColor.GetColor(204, 204, 102),
        'line_color': ROOT.TColor.GetColor(51, 51, 0),
        'legend': 'H#rightarrow#tau#tau',
        'multi': 2
    },
    'b': {
        'xvar': 'kappa_V_bb',
        'yvar': 'kappa_F_bb',
        'fill_color': ROOT.TColor.GetColor(255, 252, 102),
        'line_color': ROOT.TColor.GetColor(102, 102, 0),
        'legend': 'H#rightarrowbb',
        'multi': 4
    },
    'Z': {
        'xvar': 'kappa_V_ZZ',
        'yvar': 'kappa_F_ZZ',
        'fill_color': ROOT.TColor.GetColor(102, 102, 255),
        'line_color': ROOT.TColor.GetColor(21, 21, 183),
        'legend': 'H#rightarrowZZ',
        'multi': 2
    },
    'gam': {
        'xvar': 'kappa_V_gamgam',
        'yvar': 'kappa_F_gamgam',
        'fill_color': ROOT.TColor.GetColor(102, 204, 103),
        'line_color': ROOT.TColor.GetColor(23, 102, 0),
        'legend': 'H#rightarrow#gamma#gamma',
        'multi': 2
    },
    'W': {
        'xvar': 'kappa_V_WW',
        'yvar': 'kappa_F_WW',
        'fill_color': ROOT.TColor.GetColor(153, 153, 255),
        'line_color': ROOT.TColor.GetColor(90, 85, 216),
        'legend': 'H#rightarrowWW',
        'multi': 2
    },
    'comb': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        'fill_color': ROOT.TColor.GetColor(153, 153, 153),
        'line_color': ROOT.TColor.GetColor(0, 0, 0),
        'legend': 'ATLAS+CMS',
        'multi': 2
    },
    'cms': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        'fill_color': ROOT.TColor.GetColor(250, 226, 235),
        'line_color': ROOT.kRed,
        'legend': 'CMS',
        'multi': 2
    },
    'atlas': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        'fill_color': ROOT.TColor.GetColor(234, 239, 255),
        'line_color': ROOT.kBlue,
        'legend': 'ATLAS',
        'multi': 2
    }
}

SETTINGSA = {
    'tau': {
        'xvar': 'kappa_V_tautau',
        'yvar': 'kappa_F_tautau',
        'fill_color': ROOT.TColor.GetColor(240, 234, 245),
        'line_color': ROOT.TColor.GetColor(102, 51,  153),
        'legend': 'H#rightarrow#tau#tau',
        'multi': 4
    },
    'b': {
        'xvar': 'kappa_V_bb',
        'yvar': 'kappa_F_bb',
        'fill_color': ROOT.TColor.GetColor(230, 249, 249),
        'line_color': ROOT.TColor.GetColor(51, 204, 204),
        'legend': 'H#rightarrowbb',
        'multi': 4
    },
    'Z': {
        'xvar': 'kappa_V_ZZ',
        'yvar': 'kappa_F_ZZ',
        'fill_color': ROOT.TColor.GetColor(230, 249, 236),
        'line_color': ROOT.TColor.GetColor(56,  204, 51),
        'legend': 'H#rightarrowZZ',
        'multi': 2
    },
    'gam': {
        'xvar': 'kappa_V_gamgam',
        'yvar': 'kappa_F_gamgam',
        'fill_color': ROOT.TColor.GetColor(254, 234, 235),
        'line_color': ROOT.TColor.GetColor(249, 51, 51),
        'legend': 'H#rightarrow#gamma#gamma',
        'multi': 2
    },
    'W': {
        'xvar': 'kappa_V_WW',
        'yvar': 'kappa_F_WW',
        'fill_color': ROOT.TColor.GetColor(208, 236, 249),
        'line_color': ROOT.TColor.GetColor(7, 111, 249),
        'legend': 'H#rightarrowWW',
        'multi': 2
    },
    'comb': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        'fill_color': ROOT.TColor.GetColor(200, 200, 200),
        'line_color': ROOT.TColor.GetColor(0, 0, 0),
        'legend': 'Combined',
        'multi': 2
    },
    'cms': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        # 'fill_color': ROOT.TColor.GetColor(250, 226, 235),
        'fill_color': ROOT.TColor.GetColor(255, 249, 255),
        'line_color': ROOT.kRed,
        'legend': 'CMS',
        'multi': 2
    },
    'atlas': {
        'xvar': 'kappa_V',
        'yvar': 'kappa_F',
        'fill_color': ROOT.TColor.GetColor(234, 239, 255),
        'line_color': ROOT.kBlue,
        'legend': 'ATLAS',
        'multi': 2
    }
}

SETTINGS = SETTINGSA


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(l=0.13, b=0.10)
# ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetNdivisions(506, "Y")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--files', '-f', help='named input scans')
parser.add_argument('--multi', type=int, default=1, help='scale number of bins')
parser.add_argument('--thin', type=int, default=1, help='thin graph points')
parser.add_argument('--order', default='b,tau,Z,gam,W,comb')
parser.add_argument('--legend-order', default='b,tau,Z,gam,W,comb')
parser.add_argument('--x-range', default=None)
parser.add_argument('--pub', action='store_true')
parser.add_argument('--x-axis', default='#kappa_{V}')
parser.add_argument('--y-axis', default='#kappa_{F}')
parser.add_argument('--axis-hist', default=None)
parser.add_argument('--layout', type=int, default=1)
args = parser.parse_args()

infiles = {key: value for (
    key, value) in [tuple(x.split('=')) for x in args.files.split(',')]}
print infiles

order = args.order.split(',')
legend_order = args.legend_order.split(',')

graph_test = read('test', SETTINGS[order[0]]['xvar'], SETTINGS[
                  order[0]]['yvar'], infiles[order[0]])[0]


if args.axis_hist is not None:
    hargs = args.axis_hist.split(',')
    axis = ROOT.TH2F('hist2d', '', int(hargs[0]), float(hargs[1]), float(
        hargs[2]), int(hargs[3]), float(hargs[4]), float(hargs[5]))
else:
    axis = makeHist('hist2d', 40 * args.multi, graph_test)

# axis = None
axis.GetXaxis().SetTitle(args.x_axis)
axis.GetYaxis().SetTitle(args.y_axis)

canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].SetGridx(False)
pads[0].SetGridy(False)
pads[0].Draw()
axis.Draw()
if args.x_range is not None:
    xranges = args.x_range.split(',')
    axis.GetXaxis().SetRangeUser(float(xranges[0]), float(xranges[1]))

if args.layout == 1:
    legend = ROOT.TLegend(0.15, 0.53, 0.35, 0.74, '', 'NBNDC')
if args.layout == 2:
    legend = ROOT.TLegend(0.15, 0.11, 0.46, 0.27, '', 'NBNDC')
    legend.SetNColumns(2)


graphs = {}
bestfits = {}
hists = {}
conts68 = {}
conts95 = {}

outfile = ROOT.TFile(args.output + '.root', 'RECREATE')

for scan in order:
    if scan not in infiles:
        continue
    graphs[scan], bestfits[scan] = read(
        scan, SETTINGS[scan]['xvar'], SETTINGS[scan]['yvar'], infiles[scan])
    outfile.WriteTObject(graphs[scan], scan + '_graph')
    outfile.WriteTObject(bestfits[scan])
    # hists[scan] = makeHist(
    #     scan + '_hist', 40 * SETTINGS[scan]['multi'] * args.multi, graph_test)
    hists[scan] = plot.TH2FromTGraph2D(graphs[scan], method='BinCenterAligned')
    plot.fillTH2(hists[scan], graphs[scan])
    # fillTH2(hists[scan], graphs[scan])
    outfile.WriteTObject(hists[scan], hists[scan].GetName() + '_input')
    fixZeros(hists[scan])
    outfile.WriteTObject(hists[scan], hists[scan].GetName() + '_processed')
    conts68[scan] = plot.contourFromTH2(hists[scan], ROOT.Math.chisquared_quantile_c(
        1 - 0.68, 2), frameValue=10)
    if scan in ['cms', 'atlas', 'comb']:
        conts95[scan] = plot.contourFromTH2(
            hists[scan], ROOT.Math.chisquared_quantile_c(1 - 0.95, 2))
    for i, c in enumerate(conts68[scan]):
        c.SetName('graph68_%s_%i' % (scan, i))
        if args.thin > 1:
            newgr = ROOT.TGraph(c.GetN() / args.thin)
            needLast = True
            for a, p in enumerate(range(0, c.GetN(), args.thin)):
                if p == c.GetN() - 1:
                    needLast = False
                newgr.SetPoint(a, c.GetX()[p], c.GetY()[p])
            if needLast:
                newgr.SetPoint(
                    newgr.GetN(), c.GetX()[c.GetN() - 1], c.GetY()[c.GetN() - 1])
            conts68[scan][i] = newgr
            c = conts68[scan][i]
        c.SetFillColor(SETTINGS[scan]['fill_color'])
        c.SetLineColor(SETTINGS[scan]['line_color'])
        c.SetLineWidth(3)
        pads[0].cd()
        c.Draw('F SAME')
        outfile.WriteTObject(c, 'graph68_%s_%i' % (scan, i))
    if scan in conts95:
        c.SetName('graph95_%s_%i' % (scan, i))
        for i, c in enumerate(conts95[scan]):
            c.SetLineColor(SETTINGS[scan]['line_color'])
            c.SetLineWidth(3)
            c.SetLineStyle(3)
            pads[0].cd()
            outfile.WriteTObject(c, 'graph95_%s_%i' % (scan, i))
for scan in legend_order:
    legend.AddEntry(conts68[scan][0], SETTINGS[scan]['legend'], 'F')
for scan in order:
    for i, c in enumerate(conts68[scan]):
        c.Draw('L SAME')
    if scan in conts95:
        for i, c in enumerate(conts95[scan]):
            c.Draw('C SAME')

for scan in order:
    bestfits[scan].SetMarkerColor(SETTINGS[scan]['line_color'])
    bestfits[scan].SetMarkerStyle(34)
    bestfits[scan].SetMarkerSize(1.2)
    if scan == 'comb':
        bestfits[scan].SetMarkerSize(1.5)
    bestfits[scan].Draw('PSAME')

sm_point = ROOT.TGraph()
sm_point.SetPoint(0, 1, 1)
# sm_point.SetMarkerColor(ROOT.TColor.GetColor(249, 71, 1))
sm_point.SetMarkerColor(ROOT.kBlack)
sm_point.SetMarkerStyle(29)
sm_point.SetMarkerSize(2)
sm_point.Draw('PSAME')
# sm_point.SetFillColor(ROOT.TColor.GetColor(248, 255, 1))

legend.Draw()

if args.layout == 1:
    legend2 = ROOT.TLegend(0.15, 0.11, 0.94, 0.15, '', 'NBNDC')
    legend2.SetNColumns(4)
if args.layout == 2:
    legend2 = ROOT.TLegend(0.14, 0.53, 0.38, 0.74, '', 'NBNDC')
    legend2.SetFillStyle(0)
    # legend2.SetNColumns(2)
legend2.AddEntry(conts68['comb'][0], '68% CL', 'L')
legend2.AddEntry(conts95['comb'][0], '95% CL', 'L')
legend2.AddEntry(bestfits['comb'], 'Best fit', 'P')
legend2.AddEntry(sm_point, 'SM expected', 'P')
legend2.SetMargin(0.4)
legend2.Draw()

box = ROOT.TPave(0.15, 0.82, 0.41, 0.92, 0, 'NBNDC')
box.Draw()
if args.pub:
    plot.DrawCMSLogo(pads[0], '#splitline{#it{ATLAS}#bf{ and }#it{CMS}}{#scale[0.9]{#it{LHC} #bf{Run 1 Internal}}}', '',
                     11, 0.025, 0.035, 1.1)
else:
    plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }#it{CMS}', '#it{LHC Run 1}',
                     11, 0.025, 0.035, 1.1, extraText2='#it{Internal}')
# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{+}CMS', '#it{LHC Run 1}', 11, 0.02, 0.035, 1.1, extraText2='#it{Internal}')
pads[0].RedrawAxis()
canv.Print('.pdf')
canv.Print('.png')
canv.Print('.C')
outfile.Close()
