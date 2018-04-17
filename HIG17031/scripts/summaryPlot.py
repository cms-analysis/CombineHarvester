#!/usr/bin/env python
import ROOT
import math
import json
import argparse
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding
import fnmatch

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', nargs='*', help='input json file')
parser.add_argument('--template', default='default', help='input json file')
parser.add_argument('--output', '-o', help='name of the output file to create')
parser.add_argument('--translate', '-t', help='JSON file for remapping of parameter names')
parser.add_argument('--show-bars', default='2sig_Error,Error,Syst', help='JSON file for remapping of parameter names')
parser.add_argument('--legend', default='Error,Syst,2sig_Error', help='JSON file for remapping of parameter names')
parser.add_argument('--vlines', nargs='*', help='JSON file for remapping of parameter names')
parser.add_argument('--hlines', nargs='*', help='JSON file for remapping of parameter names')
parser.add_argument('--require-valid', default='2sig_ValidError,ValidError', help='JSON file for remapping of parameter names')
parser.add_argument('--cms-label', default='Internal', help='Label next to the CMS logo')
parser.add_argument('--height', type=int, default=700, help='Label next to the CMS logo')
parser.add_argument('--labels', default=None, help='Label next to the CMS logo')
parser.add_argument('--x-title', default='Parameter value', help='Label next to the CMS logo')
parser.add_argument('--x-range', default='0,10', help='Label next to the CMS logo')
parser.add_argument('--subline', default='35.9 fb^{-1} (13 TeV)', help='Label next to the CMS logo')
args = parser.parse_args()


default_bar_styles = {
    '2sig_Error': {
        'LineWidth': 2,
        'LineColor': ROOT.kBlue,
        'MarkerSize': 0
    },
    'Error': {
        'LineWidth': 4,
        'LineColor': ROOT.kBlue,
        'MarkerSize': 0
    },
    'Stat': {
        'LineWidth': 6,
        'LineColor': ROOT.kRed,
        'MarkerSize': 0
    },
    'Syst': {
        'LineWidth': 6,
        'LineColor': ROOT.kRed,
        'MarkerSize': 0
    },
    'BestFit': {
        'MarkerSize': 1.1
    }
}

default_bar_labels = {
    '2sig_Error': '#pm2#sigma (stat #oplus syst)',
    'Error': '#pm1#sigma (stat #oplus syst)',
    'Stat': '#pm1#sigma (stat)',
    'Syst': '#pm1#sigma (syst)'
}




def Translate(name, ndict):
    return ndict[name] if name in ndict else name

def ParseDictArgs(str):
    return {x.split('=')[0]: eval(x.split('=')[1]) for x in str.split(',')}

def GetRounded(nom, e_hi, e_lo):
    if e_hi < 0.0:
        e_hi = 0.0
    if e_lo < 0.0:
        e_lo = 0.0
    rounded = rounding.PDGRoundAsym(nom, e_hi if e_hi != 0.0 else 1.0, e_lo if e_lo != 0.0 else 1.0)
    s_nom = rounding.downgradePrec(rounded[0],rounded[2])
    s_hi = rounding.downgradePrec(rounded[1][0][0],rounded[2]) if e_hi != 0.0 else '0'
    s_lo = rounding.downgradePrec(rounded[1][0][1],rounded[2]) if e_lo != 0.0 else '0'
    return (s_nom, s_hi, s_lo)

# Dictionary to translate parameter names
translate = {}
if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)


# blah.json:modelA/*


# Set the global plotting style
plot.ModTDRStyle(l=0.20, b=0.10, height=args.height, t=0.05)
ROOT.gStyle.SetNdivisions(510, 'XYZ')

canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
# pads[0].SetGrid(1, 0)
# pads[0].SetTickx(1)

drawlist = []


for i, iargs in enumerate(args.input):
    split = iargs.split(':')
    jsonfilename = split[0]
    jsonpath = split[1].split('/')
    with open(jsonfilename) as jsonfile:
        full = json.load(jsonfile)
    for p in jsonpath[:-1]:
        full = full[p]

    if '*' in jsonpath[-1]:
        for key in full:
            if (fnmatch.fnmatch(key, jsonpath[-1])):
                drawlist.append(full[key])
                drawlist[-1]['Name'] = key
    elif ',' in jsonpath[-1]:
        for key in jsonpath[-1].split(','):
            drawlist.append(full[key])
            drawlist[-1]['Name'] = key
    else:
        drawlist.append(full[jsonpath[-1]])
        drawlist[-1]['Name'] = jsonpath[-1]

print drawlist

N = len(drawlist)

xmin = float(args.x_range.split(',')[0])
xmax = float(args.x_range.split(',')[1])

hframe = ROOT.TH2F("hframe", "hframe", 6, xmin, xmax, N+1, 0, N+1)

relabel = {}
if args.labels is not None:
    labels = args.labels.split(',')
    for l in labels:
        relabel[int(l.split('=')[0])] = l.split('=')[1]

for i, info in enumerate(drawlist):
    hframe.GetYaxis().SetBinLabel(i + 1, Translate(info['Name'], translate))
    if i in relabel:
        hframe.GetYaxis().SetBinLabel(i + 1, relabel[i])


hframe.GetYaxis().LabelsOption('v')
plot.Set(hframe.GetYaxis(), LabelSize=0.05)
plot.Set(hframe.GetXaxis(), Title=args.x_title)

hframe.Draw()


for vline in args.vlines:
    xlines = vline.split(':')[0].split(',')
    linestyle = ParseDictArgs(vline.split(':')[1])
    line = ROOT.TLine()
    plot.Set(line, **linestyle)
    for x in xlines:
        line.DrawLine(float(x), 0., float(x), float(N))


for hline in args.hlines:
    ylines = hline.split(':')[0].split(',')
    linestyle = ParseDictArgs(hline.split(':')[1])
    line = ROOT.TLine()
    plot.Set(line, **linestyle)
    for y in ylines:
        line.DrawLine(xmin, float(y), xmax, float(y))

graphs = []
bars = args.show_bars.split(',')

valid_checks = args.require_valid.split(',')

invalid_regions = []

for bar in bars:
    gr_bar = ROOT.TGraphAsymmErrors(N)
    plot.Set(gr_bar, **default_bar_styles[bar])
    for i, info in enumerate(drawlist):
        gr_bar.SetPoint(i, info["Val"], float(i)+0.5)
        err_lo = -1.0 * info["%sLo" % bar]
        err_hi = info["%sHi" % bar]
        valid_lo = True
        valid_hi = True
        for v in valid_checks:
            if not info["%sLo" % v]:
                valid_lo = False
            if not info["%sHi" % v]:
                valid_hi = False
        if not valid_lo:
            print 'Entry %sLo for %s is not valid and will not be drawn' % (bar, info["Name"])
            err_lo = 0.0
            invalid_regions.append((xmin, info["Val"], i))
        if not valid_hi:
            print 'Entry %sHi for %s is not valid and will not be drawn' % (bar, info["Name"])
            err_hi = 0.0
            invalid_regions.append((info["Val"], xmax, i))
        gr_bar.SetPointError(i, err_lo, err_hi, 0., 0.)
    # gr_bar.Draw('ZPSAME')
    graphs.append(gr_bar)

gr_fit = ROOT.TGraph(N)
plot.Set(gr_fit, **default_bar_styles['BestFit'])
for i, info in enumerate(drawlist):
    gr_fit.SetPoint(i, info["Val"], float(i)+0.5)

ROOT.gStyle.SetHatchesLineWidth(1)
ROOT.gStyle.SetHatchesSpacing(3)

if len(invalid_regions):
    gr_invalid = ROOT.TGraphAsymmErrors(len(invalid_regions))
    for i, inv in enumerate(invalid_regions):
        gr_invalid.SetPoint(i, inv[0], float(inv[2]) + 0.5)
        gr_invalid.SetPointError(i, 0.0, inv[1] - inv[0], 0.5, 0.5)

    gr_invalid.SetFillColor(17)
    gr_invalid.SetFillStyle(3144)
    gr_invalid.Draw('2SAME')


for gr in graphs:
    gr.Draw('ZPSAME')
gr_fit.Draw('PSAME')

pads[0].RedrawAxis()


title_box = ROOT.TPaveText(xmin + (xmax-xmin)*0.01, float(N)+0.3, xmin + (xmax-xmin)*0.65, float(N+1)-0.2, 'NB')
title_box.SetTextFont(42)
title_box.SetTextAlign(12)
title_box.AddText('#scale[1.4]{#bf{CMS}}')
# title_box.AddText('#scale[0.5]{%s}' % '')
plot.DrawTitle(pads[0], args.subline, 3)
title_box.SetMargin(0.0)
title_box.Draw()

frame_h = 1. - pads[0].GetBottomMargin() - pads[0].GetTopMargin()
frame_frac = pads[0].GetBottomMargin() + (frame_h * ((float(N)-0.4)/float(N+1)))
legend = ROOT.TLegend(0.66, frame_frac, 0.95, 0.945, '', 'NBNDC')
legend.AddEntry(gr_fit, 'Observed', 'P')


for bar in args.legend.split(','):
    i = bars.index(bar)
    legend.AddEntry(graphs[i], default_bar_labels[bar], 'L')
legend.Draw()


# plot.DrawCMSLogo(pads[0], 'CMS',
#                  args.cms_label, 11, 0.045, 0.035, 1.2, '', 2.5)

    # g_pulls = ROOT.TGraphAsymmErrors(n_params)
    # g_impacts_hi = ROOT.TGraphAsymmErrors(n_params)
    # g_impacts_lo = ROOT.TGraphAsymmErrors(n_params)
    # g_check = ROOT.TGraphAsymmErrors()
    # g_check_i = 0

    # max_impact = 0.

    # text_entries = []
    # redo_boxes = []
    # for p in xrange(n_params):
    #     i = n_params - (p + 1)
    #     pre = pdata[p]['prefit']
    #     fit = pdata[p]['fit']
    #     tp = pdata[p]['type']
    #     seen_types.add(tp)
    #     if pdata[p]['type'] != 'Unconstrained':
    #         pre_err_hi = (pre[2] - pre[1])
    #         pre_err_lo = (pre[1] - pre[0])
    #         pull = fit[1] - pre[1]
    #         pull = (pull/pre_err_hi) if pull >= 0 else (pull/pre_err_lo)
    #         pull_hi = fit[2] - pre[1]
    #         pull_hi = (pull_hi/pre_err_hi) if pull_hi >= 0 else (pull_hi/pre_err_lo)
    #         pull_hi = pull_hi - pull
    #         pull_lo = fit[0] - pre[1]
    #         pull_lo = (pull_lo/pre_err_hi) if pull_lo >= 0 else (pull_lo/pre_err_lo)
    #         pull_lo =  pull - pull_lo
    #         g_pulls.SetPoint(i, pull, float(i) + 0.5)
    #         g_pulls.SetPointError(
    #             i, pull_lo, pull_hi, 0., 0.)
    #     else:
    #         # Hide this point
    #         g_pulls.SetPoint(i, 0., 9999.)
    #         y1 = ROOT.gStyle.GetPadBottomMargin()
    #         y2 = 1. - ROOT.gStyle.GetPadTopMargin()
    #         x1 = ROOT.gStyle.GetPadLeftMargin()
    #         h = (y2 - y1) / float(n_params)
    #         y1 = y1 + ((float(i)+0.5) * h)
    #         x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
    #         s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
    #         text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom, s_hi, s_lo)))
    #         redo_boxes.append(i)
    #     g_impacts_hi.SetPoint(i, 0, float(i) + 0.5)
    #     g_impacts_lo.SetPoint(i, 0, float(i) + 0.5)
    #     if args.checkboxes:
    #         pboxes = pdata[p]['checkboxes']
    #         for pbox in pboxes:
    #             cboxes.index(pbox)
    #             g_check.SetPoint(g_check_i, cboxes.index(pbox) + 0.5, float(i) + 0.5)
    #             g_check_i += 1
    #     imp = pdata[p][POI]
    #     g_impacts_hi.SetPointError(i, 0, imp[2] - imp[1], 0.5, 0.5)
    #     g_impacts_lo.SetPointError(i, imp[1] - imp[0], 0, 0.5, 0.5)
    #     max_impact = max(
    #         max_impact, abs(imp[1] - imp[0]), abs(imp[2] - imp[1]))
    #     col = colors.get(tp, 2)
    #     if args.color_groups is not None and len(pdata[p]['groups']) == 1:
    #         col = color_groups.get(pdata[p]['groups'][0], 1)
    #     h_pulls.GetYaxis().SetBinLabel(
    #         i + 1, ('#color[%i]{%s}'% (col, Translate(pdata[p]['name'], translate))))

    # # Style and draw the pulls histo
    # plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title='(#hat{#theta}-#theta_{0})/#Delta#theta')
    # plot.Set(h_pulls.GetYaxis(), LabelSize=0.022, TickLength=0.0)
    # h_pulls.GetYaxis().LabelsOption('v')
    # h_pulls.Draw()

    # for i in redo_boxes:
    #     newbox = boxes[i].Clone()
    #     newbox.Clear()
    #     newbox.SetY1(newbox.GetY1()+0.005)
    #     newbox.SetY2(newbox.GetY2()-0.005)
    #     newbox.SetX1(ROOT.gStyle.GetPadLeftMargin()+0.001)
    #     newbox.SetX2(0.7-0.001)
    #     newbox.Draw()
    #     boxes.append(newbox)
    # latex = ROOT.TLatex()
    # latex.SetNDC()
    # latex.SetTextFont(42)
    # latex.SetTextSize(0.02)
    # latex.SetTextAlign(22)
    # for entry in text_entries:
    #     latex.DrawLatex(*entry)

    # # Go to the other pad and draw the impacts histo
    # pads[1].cd()
    # if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
    # h_impacts = ROOT.TH2F(
    #     "impacts", "impacts", 6, -max_impact * 1.1, max_impact * 1.1, n_params, 0, n_params)
    # plot.Set(h_impacts.GetXaxis(), LabelSize=0.03, TitleSize=0.04, Ndivisions=505, Title=
    #     '#Delta#hat{%s}' % (Translate(POI, translate)))
    # plot.Set(h_impacts.GetYaxis(), LabelSize=0, TickLength=0.0)
    # h_impacts.Draw()

    # if args.checkboxes:
    #     pads[2].cd()
    #     h_checkboxes = ROOT.TH2F(
    #         "checkboxes", "checkboxes", len(cboxes), 0, len(cboxes), n_params, 0, n_params)
    #     for i, cbox in enumerate(cboxes):
    #         h_checkboxes.GetXaxis().SetBinLabel(i+1, Translate(cbox, translate))
    #     plot.Set(h_checkboxes.GetXaxis(), LabelSize=0.03, LabelOffset=0.002)
    #     h_checkboxes.GetXaxis().LabelsOption('v')
    #     plot.Set(h_checkboxes.GetYaxis(), LabelSize=0, TickLength=0.0)
    #     h_checkboxes.Draw()
    #     # g_check.SetFillColor(ROOT.kGreen)
    #     g_check.Draw('PSAME')

    # # Back to the first pad to draw the pulls graph
    # pads[0].cd()
    # plot.Set(g_pulls, MarkerSize=0.8, LineWidth=2)
    # g_pulls.Draw('PSAME')

    # # And back to the second pad to draw the impacts graphs
    # pads[1].cd()
    # alpha = 0.7 if args.transparent else 1.0
    # g_impacts_hi.SetFillColor(plot.CreateTransparentColor(46, alpha))
    # g_impacts_hi.Draw('2SAME')
    # g_impacts_lo.SetFillColor(plot.CreateTransparentColor(38, alpha))
    # g_impacts_lo.Draw('2SAME')
    # pads[1].RedrawAxis()

    # legend = ROOT.TLegend(0.02, 0.02, 0.40, 0.06, '', 'NBNDC')
    # legend.SetNColumns(3)
    # legend.AddEntry(g_pulls, 'Pull', 'LP')
    # legend.AddEntry(g_impacts_hi, '+1#sigma Impact', 'F')
    # legend.AddEntry(g_impacts_lo, '-1#sigma Impact', 'F')
    # legend.Draw()

    # leg_width = pads[0].GetLeftMargin() - 0.01
    # if args.color_groups is not None:
    #     legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
    #     legend2.SetNColumns(2)
    #     for name, h in color_group_hists.iteritems():
    #         legend2.AddEntry(h, Translate(name, translate), 'F')
    #     legend2.Draw()
    # elif len(seen_types) > 1:
    #     legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
    #     legend2.SetNColumns(2)
    #     for name, h in color_hists.iteritems():
    #         if name == 'Unrecognised': continue
    #         legend2.AddEntry(h, name, 'F')
    #     legend2.Draw()

    # plot.DrawCMSLogo(pads[0], 'CMS', args.cms_label, 0, 0.25, 0.00, 0.00)
    # s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
    # plot.DrawTitle(pads[1], '#hat{%s} = %s^{#plus%s}_{#minus%s}%s' % (
    #     Translate(POI, translate), s_nom, s_hi, s_lo,
    #     '' if args.units is None else ' '+args.units), 3, 0.27)
    # extra = ''
    # if page == 0:
    #     extra = '('
    # if page == n - 1:
    #     extra = ')'

canv.Print('.pdf')
canv.Print('.png')
