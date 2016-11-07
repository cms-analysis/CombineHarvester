#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.plotting as plot
import argparse
# import CombineHarvester.CombineTools.maketable as maketable

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     'input', nargs='+', help="""Input json files""")
# parser.add_argument(
#     '--output', '-o', default='limit', help="""Name of the output
#     plot without file extension""")
# parser.add_argument(
#     '--show', default='exp,obs')
# # parser.add_argument(
# #     '--debug-output', '-d', help="""If specified, write the
# #     TGraphs into this output ROOT file""")
# parser.add_argument(
#     '--x-title', default='m_{H} (GeV)', help="""Title for the x-axis""")
# parser.add_argument(
#     '--y-title', default=None, help="""Title for the y-axis""")
# parser.add_argument(
#     '--limit-on', default='#sigma/#sigma_{SM}', help="""Shortcut for setting the y-axis label""")
# parser.add_argument(
#     '--cms-sub', default='Internal', help="""Text below the CMS logo""")
# parser.add_argument(
#     '--scenario-label', default='', help="""Scenario name to be drawn in top
#     left of plot""")
# parser.add_argument(
#     '--title-right', default='', help="""Right header text above the frame""")
# parser.add_argument(
#     '--title-left', default='', help="""Left header text above the frame""")
# parser.add_argument(
#     '--logy', action='store_true', help="""Draw y-axis in log scale""")
# parser.add_argument(
#     '--logx', action='store_true', help="""Draw x-axis in log scale""")
# parser.add_argument(
#     '--ratio-to', default=None)
# parser.add_argument(
#     '--pad-style', default=None, help="""Extra style options for the pad, e.g. Grid=(1,1)""")
# parser.add_argument(
#     '--auto-style', nargs='?', const='', default=None, help="""Take line colors and styles from a pre-defined list""")
# parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
# args = parser.parse_args()


def DrawLimitBand(pad, graph_dict, draw=['obs', 'exp0', 'exp1', 'exp2'],
                  legend=None):
    pad.cd()
    do_obs = False
    do_exp0 = False
    do_exp1 = False
    do_exp2 = False
    if 'exp2' in graph_dict and ('exp2' in draw or 'exp' in draw):
        do_exp2 = True
        graph_dict['exp2'].Draw('2SAME')
    if 'exp1' in graph_dict and ('exp1' in draw or 'exp' in draw):
        do_exp1 = True
        graph_dict['exp1'].Draw('2SAME')
    if 'exp0' in graph_dict and ('exp0' in draw or 'exp' in draw):
        do_exp0 = True
        graph_dict['exp0'].SetMarkerSize(0)
        graph_dict['exp0'].Draw('PSAME')
    if 'obs' in graph_dict and 'obs' in draw:
        do_obs = True
        graph_dict['obs'].Draw('PSAME')
    if legend is not None:
        if do_obs:
            legend.AddEntry(graph_dict['obs'], 'Observed', 'LP')
        if do_exp0:
            legend.AddEntry(graph_dict['exp0'], 'Expected', 'L')
        if do_exp1:
            legend.AddEntry(graph_dict['exp1'], '#pm1#sigma Expected', 'F')
        if do_exp2:
            legend.AddEntry(graph_dict['exp2'], '#pm2#sigma Expected', 'F')


def DrawAxisHists(pads, axis_hists, def_pad=None):
    for i, pad in enumerate(pads):
        pad.cd()
        axis_hists[i].Draw('AXIS')
        axis_hists[i].Draw('AXIGSAME')
    if def_pad is not None:
        def_pad.cd()


## Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle(height=500)
ROOT.gStyle.SetNdivisions(510, 'XYZ') # probably looks better

canv = ROOT.TCanvas('ttH_comb_limit', 'ttH_comb_limit')


pads = plot.OnePad()

graphs = plot.StandardLimitsFromJSONFile('merged_limit.json')

legend = ROOT.TLegend(0.17, 0.50, 0.55, 0.75, '', 'NBNDC')

plot.Set(legend, NColumns=1, Header='#bf{ttH production limits}')

for name, gr in graphs.iteritems():
    gr.Print()
    newgr = ROOT.TGraphAsymmErrors(gr.GetN())
    for i in xrange(gr.GetN()):
        if name in ['exp1', 'exp2']:
            newgr.GetEYlow()[i] = gr.GetEYlow()[i]
            newgr.GetEYhigh()[i] = gr.GetEYhigh()[i]
        else:
            newgr.GetEYlow()[i] = 0.
            newgr.GetEYhigh()[i] = 0.
        newgr.GetEXlow()[i] = 0.5
        newgr.GetEXhigh()[i] = 0.5
        newgr.GetX()[i] = gr.GetX()[i]
        newgr.GetY()[i] = gr.GetY()[i]
    graphs[name] = newgr

axis = ROOT.TH1F('axis', '', 4, 0, 4)
pads[0].cd()
axis.Draw('AXIS')

plot.StyleLimitBand(graphs)
DrawLimitBand(pads[0], graphs, legend=legend)
legend.Draw()

y_min, y_max = (plot.GetPadYMin(pads[0]), plot.GetPadYMax(pads[0]))
plot.FixBothRanges(pads[0], 0, 0, y_max, 0.10)






axis.GetYaxis().SetTitle('95%% CL upper limit on %s' % '#mu_{ttH}')

labels = ['Combined', '#splitline{H#rightarrowleptons}{#scale[0.8]{ HIG-15-008}}', '#splitline{   H#rightarrowbb}{#scale[0.8]{ HIG-16-004}}', '#splitline{   H#rightarrow#gamma#gamma}{#scale[0.8]{HIG-15-005}}']
# labels = ['Combined', 'H#rightarrowleptons', 'H#rightarrowbb', 'H#rightarrow#gamma#gamma']
for i in xrange(len(labels)):
    axis.GetXaxis().SetBinLabel(i+1, labels[i])
axis.GetXaxis().SetLabelSize(axis.GetXaxis().GetLabelSize()*1.5)
# axis.GetXaxis().SetNdivisions(4, False)
# axis[0].GetXaxis().SetTitle(args.x_title)
# axis[0].GetXaxis().SetLabelOffset(axis[0].GetXaxis().GetLabelOffset()*2)

pads[0].RedrawAxis()
pads[0].RedrawAxis('g')
pads[0].GetFrame().Draw()

line = ROOT.TLine()
line.SetLineColor(ROOT.kBlue)
line.SetLineWidth(2)
plot.DrawHorizontalLine(pads[0], line, 1)

# info = ROOT.TPaveText(0.47, 0.75, 0.70, 0.91, 'NDCNB')
# info.SetTextFont(42)
# info.SetTextAlign(12)
# info.AddText('#bf{ttH combination}')
# info.AddText('HIG-15-005 H#rightarrow#gamma#gamma')
# info.AddText('HIG-15-008 H#rightarrowleptons')
# info.AddText('HIG-16-004 H#rightarrowbb')
# info.Draw()

# box = ROOT.TPave(pads[0].GetLeftMargin(), 0.81, 1-pads[0].GetRightMargin(), 1-pads[0].GetTopMargin(), 1, 'NDC')
# box.Draw()


plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.035, 1.2, '', 1.1)
plot.DrawTitle(pads[0], '2.3-2.7 fb^{-1} (13 TeV)', 3)
plot.DrawTitle(pads[0], 'm_{H} = 125 GeV', 1)

canv.Print('.pdf')
canv.Print('.png')
