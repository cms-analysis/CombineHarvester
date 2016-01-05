#!/usr/bin/env python
import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'input', help="""ROOT file containing the output of the
    combineTool.py AsymptoticGrid or HybridNewGrid methods""")
parser.add_argument(
    '--output', '-o', default='limit_grid_output', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--contours', default='exp-2,exp-1,exp0,exp+1,exp+2,obs', help="""List of
    contours to plot. These must correspond to the names of the TGraph2D
    objects in the input file""")
parser.add_argument(
    '--bin-method', default='BinEdgeAligned', help="""One of BinEdgeAligned or
    BinCenterAligned. See plotting.py documentation for details.""")
parser.add_argument(
    '--debug-output', '-d', help="""If specified, write the contour TH2s and
    TGraphs into this output ROOT file""")
parser.add_argument(
    '--CL', default=0.95, help="""Confidence level for contours""")
parser.add_argument(
    '--x-title', default='m_{A} (GeV)', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='tan#beta', help="""Title for the y-axis""")
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--scenario-label', default='', help="""Scenario name to be drawn in top
    left of plot""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--logy', action='store_true', help="""Draw y-axis in log scale""")
parser.add_argument(
    '--logx', action='store_true', help="""Draw x-axis in log scale""")
parser.add_argument(
    '--force-x-width', type=float, default=None, help="""Use this x bin width in
    BinCenterAligned mode""")
parser.add_argument(
    '--force-y-width', type=float, default=None, help="""Use this y bin width in
    BinCenterAligned mode""")
parser.add_argument(
    '--hist', default=None, help="""Draw this TGraph2D as a histogram with
    COLZ""")
parser.add_argument(
    '--z-range', default=None, type=str, help="""z-axis range of the COLZ
    hist""")
parser.add_argument(
    '--z-title', default=None, help="""z-axis title of the COLZ hist""")
args = parser.parse_args()


plot.ModTDRStyle(r=0.06 if args.hist is None else 0.17, l=0.12)
ROOT.gStyle.SetNdivisions(510, 'XYZ')
plot.SetBirdPalette()

file = ROOT.TFile(args.input)
types = args.contours.split(',')
CL = 1 - args.CL

# Object storage
graphs = {c: file.Get(c) for c in types}
hists = {}
contours = {}

h_proto = plot.TH2FromTGraph2D(graphs[types[0]], method=args.bin_method,
                               force_x_width=args.force_x_width,
                               force_y_width=args.force_y_width)
h_axis = h_proto
h_axis = plot.TH2FromTGraph2D(graphs[types[0]])
# Create the debug output file if requested
if args.debug_output is not None:
    debug = ROOT.TFile(args.debug_output, 'RECREATE')
else:
    debug = None

# Fill TH2s by interpolating the TGraph2Ds, then extract contours
for c in types:
    print 'Filling histo for %s' % c
    hists[c] = h_proto.Clone(c)
    plot.fillTH2(hists[c], graphs[c])
    contours[c] = plot.contourFromTH2(hists[c], CL, 5, frameValue=1)
    if debug is not None:
        debug.WriteTObject(hists[c], 'hist_%s' % c)
        for i, cont in enumerate(contours[c]):
            debug.WriteTObject(cont, 'cont_%s_%i' % (c, i))

# Setup the canvas: we'll use a two pad split, with a small top pad to contain
# the CMS logo and the legend
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.TwoPadSplit(0.8, 0, 0)
pads[1].cd()
h_axis.GetXaxis().SetTitle(args.x_title)
h_axis.GetYaxis().SetTitle(args.y_title)
h_axis.Draw()

if args.hist is not None:
    colzhist = h_proto.Clone(c)
    plot.fillTH2(colzhist, file.Get(args.hist))
    colzhist.SetContour(255)
    colzhist.Draw('COLZSAME')
    colzhist.GetZaxis().SetLabelSize(0.03)
    if args.z_range is not None:
        colzhist.SetMinimum(float(args.z_range.split(',')[0]))
        colzhist.SetMaximum(float(args.z_range.split(',')[1]))
    if args.z_title is not None:
        colzhist.GetZaxis().SetTitle(args.z_title)

pads[1].SetLogy(args.logy)
pads[1].SetLogx(args.logx)
pads[1].SetTickx()
pads[1].SetTicky()
# h_proto.GetXaxis().SetRangeUser(130,400)
# h_proto.GetYaxis().SetRangeUser(1,20)

fillstyle = 'FSAME'
if args.hist is not None:
    fillstyle = 'LSAME'

# Now we draw the actual contours
if 'exp-2' in contours and 'exp+2' in contours:
    for i, gr in enumerate(contours['exp-2']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kGray + 0, FillStyle=1001)
        if args.hist is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 0, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp-1' in contours and 'exp+1' in contours:
    for i, gr in enumerate(contours['exp-1']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kGray + 1, FillStyle=1001)
        if args.hist is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 1, LineWidth=2)
        gr.Draw(fillstyle)
    fill_col = ROOT.kGray+0
    # If we're only drawing the 1 sigma contours then we should fill with
    # white here instead
    if 'exp-2' not in contours and 'exp+2' not in contours:
        fill_col = ROOT.kWhite
    for i, gr in enumerate(contours['exp+1']):
        plot.Set(gr, LineColor=0, FillColor=fill_col, FillStyle=1001)
        if args.hist is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 1, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp-2' in contours and 'exp+2' in contours:
    for i, gr in enumerate(contours['exp+2']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kWhite, FillStyle=1001)
        if args.hist is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 0, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp0' in contours:
    for i, gr in enumerate(contours['exp0']):
        if args.hist is not None:
            plot.Set(gr, LineWidth=2)
        if 'obs' in contours:
            plot.Set(gr, LineColor=ROOT.kBlack, LineStyle=2)
            gr.Draw('LSAME')
        else:
            plot.Set(gr, LineStyle=2, FillStyle=1001,
                     FillColor=plot.CreateTransparentColor(
                        ROOT.kSpring + 6, 0.5))
            gr.Draw(fillstyle)
            gr.Draw('LSAME')
if 'obs' in contours:
    for i, gr in enumerate(contours['obs']):
        plot.Set(gr, FillStyle=1001, FillColor=plot.CreateTransparentColor(
            ROOT.kAzure + 6, 0.5))
        if args.hist is not None:
            plot.Set(gr, LineWidth=2)
        gr.Draw(fillstyle)
        gr.Draw('LSAME')

# We just want the top pad to look like a box, so set all the text and tick
# sizes to zero
pads[0].cd()
h_top = h_axis.Clone()
plot.Set(h_top.GetXaxis(), LabelSize=0, TitleSize=0, TickLength=0)
plot.Set(h_top.GetYaxis(), LabelSize=0, TitleSize=0, TickLength=0)
h_top.Draw()

# Draw the legend in the top TPad
legend = plot.PositionedLegend(0.4, 0.11, 3, 0.015)
plot.Set(legend, NColumns=2, Header='#bf{%.0f%% CL Excluded:}' % (args.CL*100.))
if 'obs' in contours:
    legend.AddEntry(contours['obs'][0], "Observed", "F")
if 'exp-1' in contours and 'exp+1' in contours:
    legend.AddEntry(contours['exp-1'][0], "#pm 1#sigma Expected", "F")
if 'exp0' in contours:
    if 'obs' in contours:
        legend.AddEntry(contours['exp0'][0], "Expected", "L")
    else:
        legend.AddEntry(contours['exp0'][0], "Expected", "F")
if 'exp-2' in contours and 'exp+2' in contours:
    legend.AddEntry(contours['exp-2'][0], "#pm 2#sigma Expected", "F")
legend.Draw()

# Draw logos and titles
plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.15, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawTitle(pads[0], args.title_left, 1)


# Redraw the frame because it usually gets covered by the filled areas
pads[1].cd()
pads[1].GetFrame().Draw()
pads[1].RedrawAxis()

# Draw the scenario label
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.155, 0.75, args.scenario_label)

canv.Print('.pdf')
canv.Print('.png')
canv.Close()

if debug is not None:
    debug.Close()
