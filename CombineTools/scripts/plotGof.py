#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.plotting as plot
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'input', help="""Input json file""")
parser.add_argument(
    '--output', '-o', default='', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--mass', default='160.0', help="""Higgs Boson mass to be used""")
parser.add_argument(
    '--statistic', default='saturated', help="""Used Test Statistic""")
parser.add_argument(
    '--x-title', default='Goodness of Fit', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='Number of Toys', help="""Title for the y-axis""")
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--pad-style', default=None, help="""Extra style options for the pad, e.g. Grid=(1,1)""")
parser.add_argument(
    '--auto-style', nargs='?', const='', default=None, help="""Take line colors and styles from a pre-defined list""")
parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
args = parser.parse_args()


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
plot.ModTDRStyle()
ROOT.gStyle.SetNdivisions(510, 'XYZ') # probably looks better

canv = ROOT.TCanvas(args.output, args.output)

pads = plot.OnePad()

# Set the style options of the pads
for padx in pads:
    # Use tick marks on oppsite axis edges
    plot.Set(padx, Tickx=1, Ticky=1)
    if args.pad_style is not None:
        settings = {x.split('=')[0]: eval(x.split('=')[1]) for x in args.pad_style.split(',')}
        print 'Applying style options to the TPad(s):'
        print settings
        plot.Set(padx, **settings)

graphs = []
graph_sets = []

legend = plot.PositionedLegend(0.45, 0.10, 3, 0.015)
plot.Set(legend, NColumns=2)

axis = None

defcols = [
    ROOT.kGreen+3, ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kYellow+2,
    ROOT.kOrange+10, ROOT.kCyan+3, ROOT.kMagenta+2, ROOT.kViolet-5, ROOT.kGray
    ]

deflines = [1, 2, 3]

if args.auto_style is not None:
    icol = {x: 0 for x in args.auto_style.split(',')}
    icol['default'] = 0
    iline = {}
    iline['default'] = 1
    for i, x in enumerate(args.auto_style.split(',')):
        iline[x] = i+1

pValue = 0
if args.statistic in ["AD","KS"]:
    titles = {
            "htt_em_8_13TeV" : "e#mu, nobtag",
            "htt_em_9_13TeV" : "e#mu, btag",
            "htt_et_8_13TeV" : "e#tau_{h}, nobtag",
            "htt_et_9_13TeV" : "e#tau_{h}, btag",
            "htt_mt_8_13TeV" : "#mu#tau_{h}, nobtag",
            "htt_mt_9_13TeV" : "#mu#tau_{h}, btag",
            "htt_tt_8_13TeV" : "#tau_{h}#tau_{h}, nobtag",
            "htt_tt_9_13TeV" : "#tau_{h}#tau_{h}, btag"
            }
    with open(args.input) as jsfile:
        js = json.load(jsfile)
    for key  in js[args.mass]: ## these are the channels
        # title = key if key not in titles else titles[key]
        title = titles.get(key, key)
        # if key not in titles:
        #     continue
        toy_graph = plot.ToyTGraphFromJSON(js, [args.mass,key,'toy'])
        toy_hist = plot.makeHist1D("toys", 100, toy_graph, 1.15)
        for i in range(toy_graph.GetN()):
            toy_hist.Fill(toy_graph.GetX()[i])
        pValue = js[args.mass][key]["p"]
        obs = plot.ToyTGraphFromJSON(js, [args.mass,key,'obs'])
        arr = ROOT.TArrow(obs.GetX()[0], 0.001, obs.GetX()[0], toy_hist.GetMaximum()/8, 0.02, "<|");
        arr.SetLineColor(ROOT.kBlue);
        arr.SetFillColor(ROOT.kBlue);
        arr.SetFillStyle(1001);
        arr.SetLineWidth(6);
        arr.SetLineStyle(1);
        arr.SetAngle(60);
        toy_hist.Draw()
        arr.Draw("<|same");
        pads[0].RedrawAxis()
        pads[0].RedrawAxis('g')
        pads[0].GetFrame().Draw()

        # axis[0].GetYaxis().SetTitle(args.y_title)
        # axis[0].GetXaxis().SetTitle(args.x_title)
        # axis[0].GetXaxis().SetLabelOffset(axis[0].GetXaxis().GetLabelOffset()*2)

        y_min, y_max = (plot.GetPadYMin(pads[0]), plot.GetPadYMax(pads[0]))
        plot.FixBothRanges(pads[0], 0, 0, y_max, 0.25)

        ratio_graph_sets = []
        ratio_graphs = []

        pads[0].cd()
        if legend.GetNRows() == 1:
            legend.SetY1(legend.GetY2() - 0.5*(legend.GetY2()-legend.GetY1()))
        legend.Draw()

        box = ROOT.TPave(pads[0].GetLeftMargin(), 0.81, 1-pads[0].GetRightMargin(), 1-pads[0].GetTopMargin(), 1, 'NDC')
        box.Draw()

        legend.Draw()

        plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.035, 1.2, '', 0.8)
        plot.DrawTitle(pads[0], args.title_right, 3)
        plot.DrawTitle(pads[0], title, 1)

        textlabel = ROOT.TPaveText(0.68, 0.88, 0.80, 0.92, "NDC")
        textlabel.SetBorderSize(   0 )
        textlabel.SetFillStyle (   0 )
        textlabel.SetTextAlign (  32 )
        textlabel.SetTextSize  (0.04 )
        textlabel.SetTextColor (   1 )
        textlabel.SetTextFont  (  62 )
        textlabel.AddText(args.statistic+", %s Toys"%(toy_graph.GetN()))
        textlabel.Draw()

        pvalue = ROOT.TPaveText(0.68, 0.83, 0.80, 0.87, "NDC")
        pvalue.SetBorderSize(   0 )
        pvalue.SetFillStyle (   0 )
        pvalue.SetTextAlign (  32 )
        pvalue.SetTextSize  (0.04 )
        pvalue.SetTextColor (   1 )
        pvalue.SetTextFont  (  62 )
        pvalue.AddText("p-value = %0.3f"%pValue)
        pvalue.Draw()

        canv.Print(key+args.output+'.pdf')
        canv.Print(key+args.output+'.png')

        # some cleaning up
        del toy_hist

else:
    with open(args.input) as jsfile:
        js = json.load(jsfile)
    # graph_sets.append(plot.StandardLimitsFromJSONFile(file, args.show.split(',')))
    toy_graph = plot.ToyTGraphFromJSON(js, [args.mass, "toy"])
    toy_hist = plot.makeHist1D("toys", 100, toy_graph)
    for i in range(toy_graph.GetN()):
        toy_hist.Fill(toy_graph.GetX()[i])
    pValue = js[args.mass]["p"]
    obs = plot.ToyTGraphFromJSON(js, [args.mass,"obs"])
    arr = ROOT.TArrow(obs.GetX()[0], 0.001, obs.GetX()[0], toy_hist.GetMaximum()/8, 0.02, "<|");
    # if axis is None:
        # axis = plot.CreateAxisHists(1, graph_sets[-1].values()[0], True)
        # DrawAxisHists(pads, axis, pads[0])
    arr.SetLineColor(ROOT.kBlue);
    arr.SetFillColor(ROOT.kBlue);
    arr.SetFillStyle(1001);
    arr.SetLineWidth(6);
    arr.SetLineStyle(1);
    arr.SetAngle(60);
    toy_hist.Draw()
    arr.Draw("<|same");
    pads[0].RedrawAxis()
    pads[0].RedrawAxis('g')
    pads[0].GetFrame().Draw()
    # axis[0].GetYaxis().SetTitle(args.y_title)
    # axis[0].GetXaxis().SetTitle(args.x_title)
    # axis[0].GetXaxis().SetLabelOffset(axis[0].GetXaxis().GetLabelOffset()*2)

    y_min, y_max = (plot.GetPadYMin(pads[0]), plot.GetPadYMax(pads[0]))
    plot.FixBothRanges(pads[0], 0, 0, y_max, 0.25)

    ratio_graph_sets = []
    ratio_graphs = []

    pads[0].cd()
    if legend.GetNRows() == 1:
        legend.SetY1(legend.GetY2() - 0.5*(legend.GetY2()-legend.GetY1()))
    legend.Draw()

    box = ROOT.TPave(pads[0].GetLeftMargin(), 0.81, 1-pads[0].GetRightMargin(), 1-pads[0].GetTopMargin(), 1, 'NDC')
    box.Draw()

    legend.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.035, 1.2, '', 0.8)
    plot.DrawTitle(pads[0], args.title_right, 3)
    plot.DrawTitle(pads[0], args.title_left, 1)


    textlabel = ROOT.TPaveText(0.68, 0.88, 0.80, 0.92, "NDC")
    textlabel.SetBorderSize(   0 )
    textlabel.SetFillStyle (   0 )
    textlabel.SetTextAlign (  32 )
    textlabel.SetTextSize  (0.04 )
    textlabel.SetTextColor (   1 )
    textlabel.SetTextFont  (  62 )
    textlabel.AddText(args.statistic+", %s Toys"%(toy_graph.GetN()))
    textlabel.Draw()

    pvalue = ROOT.TPaveText(0.68, 0.83, 0.80, 0.87, "NDC")
    pvalue.SetBorderSize(   0 )
    pvalue.SetFillStyle (   0 )
    pvalue.SetTextAlign (  32 )
    pvalue.SetTextSize  (0.04 )
    pvalue.SetTextColor (   1 )
    pvalue.SetTextFont  (  62 )
    pvalue.AddText("p-value = %0.3f"%pValue)
    pvalue.Draw()

    canv.Print('.pdf')
    canv.Print('.png')
