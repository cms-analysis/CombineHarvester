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
    '--bin-method', default='BinEdgeAligned', help="""One of BinEdgeAligned or
    BinCenterAligned. See plotting.py documentation for details.""")
parser.add_argument(
    '--best-fit', default=[], nargs="+", help="""Input files for the best fit""")
parser.add_argument(
    '--x-title', default='#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} (pb)', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='#sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} (pb)', help="""Title for the x-axis""")
parser.add_argument(
    '--x-range', default=None, type=str, help="""x-axis range""")
parser.add_argument(
    '--y-range', default=None, type=str, help="""y-axis range""")
parser.add_argument(
    '--mass', default='', help="""Mass label on the plot""")
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
args = parser.parse_args()


plot.ModTDRStyle(r=0.06 , l=0.12)
ROOT.gStyle.SetNdivisions(510, 'XYZ')
plot.SetBirdPalette()

file = ROOT.TFile(args.input)
types = ['obs']
cl68 =  0.68
cl95 =  0.95

# Object storage
graphs = {c: file.Get(c) for c in types}
hists = {}
contours68 = {}
contours95 = {}

h_proto = plot.TH2FromTGraph2D(graphs[types[0]], method=args.bin_method,
                               force_x_width=args.force_x_width,
                               force_y_width=args.force_y_width)
h_axis = h_proto
h_axis = plot.TH2FromTGraph2D(graphs[types[0]])



# Fill TH2s by interpolating the TGraph2Ds, then extract contours
for c in types:
    print 'Filling histo for %s' % c
    hists[c] = h_proto.Clone(c)
    plot.fillInvertedTH2(hists[c], graphs[c])
    contours68[c] = plot.contourFromTH2(hists[c], cl68, 5, frameValue=1)
    contours95[c] = plot.contourFromTH2(hists[c], cl95, 5, frameValue=1)


# Setup the canvas: we'll use a two pad split, with a small top pad to contain
# the CMS logo and the legend
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].cd()
h_axis.GetXaxis().SetTitle(args.x_title)
h_axis.GetYaxis().SetTitle(args.y_title)
h_axis.GetXaxis().SetLabelSize(0.025)
h_axis.GetYaxis().SetLabelSize(0.025)
if args.x_range is not None:
    h_axis.GetXaxis().SetRangeUser(float(args.x_range.split(',')[0]),float(args.x_range.split(',')[1]))
if args.y_range is not None:
    h_axis.GetYaxis().SetRangeUser(float(args.y_range.split(',')[0]),float(args.y_range.split(',')[1]))
h_axis.Draw()


pads[0].SetLogy(args.logy)
pads[0].SetLogx(args.logx)
pads[0].SetTickx()
pads[0].SetTicky()
# h_proto.GetXaxis().SetRangeUser(130,400)
# h_proto.GetYaxis().SetRangeUser(1,20)

fillstyle = 'FSAME'

# Now we draw the actual contours
for i, gr in enumerate(contours95['obs']):
    plot.Set(gr, FillColor=ROOT.kBlue-10,LineColor=ROOT.kBlack,LineWidth=2,FillStyle=1001)
    gr.Draw(fillstyle)
    gr.Draw("LSAME")
for i, gr in enumerate(contours68['obs']):
    plot.Set(gr, FillColor=ROOT.kBlue-8,LineColor=ROOT.kBlack,LineWidth=2,FillStyle=1001)
    gr.Draw(fillstyle)
    gr.Draw("LSAME")



# We just want the top pad to look like a box, so set all the text and tick
# sizes to zero

# Draw the legend in the top TPad
legend = plot.PositionedLegend(0.3, 0.2, 3, 0.015)
legend.AddEntry(contours68['obs'][0], "68% CL", "F")
legend.AddEntry(contours95['obs'][0], "95% CL", "F")
#Add best fit value (From MultiDimFit)
if args.best_fit:
    limit_best = plot.MakeTChain(args.best_fit, 'limit')
    best = plot.TGraphFromTree(
       limit_best, "r_ggH", "r_bbH", 'deltaNLL == 0')
    best.SetMarkerStyle(34)
    best.SetMarkerSize(3)
    best.Draw("P SAME")
    legend.AddEntry(best, "Best fit", "P")
if args.mass:
    legend.SetHeader("m_{#phi} = "+args.mass+" GeV")
legend.Draw("SAME")

# Draw logos and titles
plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.035, 1.2, '', 1.0)
plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawTitle(pads[0], args.title_left, 1)
plot.FixOverlay()


canv.Print('.pdf')
canv.Print('.png')
canv.Close()

