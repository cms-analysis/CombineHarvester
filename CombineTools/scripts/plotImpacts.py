#!/usr/bin/env python
from __future__ import print_function
from builtins import range
# import enum
import ROOT
import math
import json
import argparse
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding
import HiggsAnalysis.CombinedLimit.calculate_pulls as CP

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

def Translate(name, ndict):
    return ndict[name] if name in ndict else name


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

def IsConstrained(param_info):
    return param_info["type"] != 'Unconstrained'

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input json file')
parser.add_argument('--output', '-o', help='name of the output file to create')
parser.add_argument('--translate', '-t', help='JSON file for remapping of parameter names')
parser.add_argument('--units', default=None, help='Add units to the best-fit parameter value')
parser.add_argument('--per-page', type=int, default=30, help='Number of parameters to show per page')
parser.add_argument('--max-pages', type=int, default=None, help='Maximum number of pages to write')
parser.add_argument('--height', type=int, default=600, help='Canvas height, in pixels')
parser.add_argument('--left-margin', type=float, default=0.4, help='Left margin, expressed as a fraction')
parser.add_argument('--label-size', type=float, default=0.021, help='Parameter name label size')
parser.add_argument('--cms-label', default='Internal', help='Label next to the CMS logo')
parser.add_argument('--transparent', action='store_true', help='Draw areas as hatched lines instead of solid')
parser.add_argument('--checkboxes', action='store_true', help='Draw an extra panel with filled checkboxes')
parser.add_argument('--blind', action='store_true', help='Do not print best fit signal strength')
parser.add_argument('--color-groups', default=None, help='Comma separated list of GROUP=COLOR')
parser.add_argument("--pullDef",  default=None, help="Choose the definition of the pull, see HiggsAnalysis/CombinedLimit/python/calculate_pulls.py for options")
parser.add_argument('--POI', default=None, help='Specify a POI to draw')
parser.add_argument("--sort", "-s", choices=["impact", "constraint", "pull"], default="impact", help="The metric to sort the list of parameters")
args = parser.parse_args()

if args.transparent:
    print('plotImpacts.py: --transparent is now always enabled, the option will be removed in a future update')

externalPullDef = (args.pullDef is not None)

# Dictionary to translate parameter names
translate = {}
if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)

# Load the json output of combineTool.py -M Impacts
data = {}
with open(args.input) as jsonfile:
    data = json.load(jsonfile)

# Set the global plotting style
plot.ModTDRStyle(l=args.left_margin, b=0.10, width=(900 if args.checkboxes else 700), height=args.height)

# We will assume the first POI is the one to plot
POIs = [ele['name'] for ele in data['POIs']]
POI = POIs[0]
if args.POI:
    POI = args.POI

for ele in data['POIs']:
    if ele['name'] == POI:
        POI_info = ele
        break

POI_fit = POI_info['fit']

# Add the actual pull to each entry
params = data['params']
for ele in params:
    if IsConstrained(ele):
        pre = ele['prefit']
        fit = ele['fit']
        pre_err_hi = (pre[2] - pre[1])
        pre_err_lo = (pre[1] - pre[0])
        fit_err_hi = (fit[2] - fit[1])
        fit_err_lo = (fit[1] - fit[0])
        pull = CP.diffPullAsym(fit[1], pre[1], fit_err_hi,pre_err_hi,fit_err_lo,pre_err_lo)
        ele['pull'] = pull[0]
        # Under some conditions (very small constraint) the calculated pull is not reliable.
        # In this case, pull[1] will have a non-zero value.
        ele['pull_ok'] = (pull[1] == 0)
        ele['constraint'] = (fit[2] - fit[0]) / (pre[2] - pre[0])

        if externalPullDef:
            sc_fit, sc_fit_hi, sc_fit_lo = CP.returnPullAsym(args.pullDef, fit[1], pre[1], fit_err_hi, pre_err_hi, fit_err_lo, pre_err_lo)
        else:
            sc_fit = fit[1] - pre[1]
            sc_fit = (sc_fit / pre_err_hi) if sc_fit >= 0 else (sc_fit / pre_err_lo)
            sc_fit_hi = fit[2] - pre[1]
            sc_fit_hi = (sc_fit_hi / pre_err_hi) if sc_fit_hi >= 0 else (sc_fit_hi / pre_err_lo)
            sc_fit_hi = sc_fit_hi - sc_fit
            sc_fit_lo = fit[0] - pre[1]
            sc_fit_lo = (sc_fit_lo / pre_err_hi) if sc_fit_lo >= 0 else (sc_fit_lo / pre_err_lo)
            sc_fit_lo =  sc_fit - sc_fit_lo
        ele["sc_fit"] = sc_fit
        ele["sc_fit_hi"] = sc_fit_hi
        ele["sc_fit_lo"] = sc_fit_lo
    else:
        # For unconstrained parameters there is no pull to define. For sorting purposes we
        # still need to set a value, so will put it to zero
        ele['pull'] = 0
        ele['pull_ok'] = False
        ele['constraint'] = 9999.


# Now compute each parameters ranking according to: largest pull, strongest constraint, and largest impact
ranking_pull = sorted([(i, abs(v['pull'])) for i, v in enumerate(params)], reverse=True, key=lambda X: X[1])
ranking_constraint = sorted([(i, abs(v['constraint'])) for i, v in enumerate(params)], reverse=False, key=lambda X: X[1])
ranking_impact = sorted([(i, abs(v['impact_{}'.format(POI)])) for i, v in enumerate(params)], reverse=True, key=lambda X: X[1])
for i in range(len(params)):
    params[ranking_pull[i][0]]['rank_pull'] = i + 1
    params[ranking_impact[i][0]]['rank_impact'] = i + 1
    params[ranking_constraint[i][0]]['rank_constraint'] = i + 1

if args.sort == 'pull':
    data['params'].sort(key=lambda x: abs(x['pull']), reverse=True)
elif args.sort == "impact":
    data['params'].sort(key=lambda x: abs(x['impact_%s' % POI]), reverse=True)
elif args.sort == "constraint":
    data['params'].sort(key=lambda x: abs(x['constraint']), reverse=False)
else:
    raise RuntimeError("This error should not have happened!")

if args.checkboxes:
    cboxes = data['checkboxes']

# Set the number of parameters per page (show) and the number of pages (n)
show = args.per_page
n = int(math.ceil(float(len(data['params'])) / float(show)))
if args.max_pages is not None and args.max_pages > 0:
    n = args.max_pages

colors = {
    'Gaussian': 1,
    'Poisson': 8,
    'AsymmetricGaussian': 9,
    'Unconstrained': 39,
    'Unrecognised': 2
}
color_hists = {}
color_group_hists = {}

if args.color_groups is not None:
    color_groups = {
        x.split('=')[0]: int(x.split('=')[1]) for x in args.color_groups.split(',')
    }

seen_types = set()

for name, col in colors.items():
    color_hists[name] = ROOT.TH1F()
    plot.Set(color_hists[name], FillColor=col, Title=name)

if args.color_groups is not None:
    for name, col in color_groups.items():
        color_group_hists[name] = ROOT.TH1F()
        plot.Set(color_group_hists[name], FillColor=col, Title=name)

for page in range(n):
    canv = ROOT.TCanvas(args.output, args.output)
    n_params = len(data['params'][show * page:show * (page + 1)])
    pdata = data['params'][show * page:show * (page + 1)]
    print(">> Doing page %i, have %i parameters" % (page, n_params))

    boxes = []
    for i in range(n_params):
        y1 = ROOT.gStyle.GetPadBottomMargin()
        y2 = 1. - ROOT.gStyle.GetPadTopMargin()
        h = (y2 - y1) / float(n_params)
        y1 = y1 + float(i) * h
        y2 = y1 + h
        box = ROOT.TPaveText(0, y1, 1, y2, 'NDC')
        plot.Set(box, TextSize=0.02, BorderSize=0, FillColor=0, TextAlign=12, Margin=0.005)
        if i % 2 == 0:
            box.SetFillColor(18)
        box.AddText('%i' % (n_params - i + page * show))
        box.Draw()
        boxes.append(box)

    # Crate and style the pads
    if args.checkboxes:
        pads = plot.MultiRatioSplitColumns([0.54, 0.24], [0., 0.], [0., 0.])
        pads[2].SetGrid(1, 0)
    else:
        pads = plot.MultiRatioSplitColumns([0.7], [0.], [0.])
    pads[0].SetGrid(1, 0)
    pads[0].SetTickx(1)
    pads[1].SetGrid(1, 0)
    pads[1].SetTickx(1)

    min_pull = -0.9
    max_pull = +0.9

    g_fit = ROOT.TGraphAsymmErrors(n_params)
    g_pull = ROOT.TGraph(n_params)
    g_impacts_hi = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_lo = ROOT.TGraphAsymmErrors(n_params)
    g_check = ROOT.TGraphAsymmErrors()
    g_check_i = 0

    max_impact = 0.

    text_entries = []
    redo_boxes = []
    y_bin_labels = []
    for p in range(n_params):
        par = pdata[p]
        i = n_params - (p + 1)
        pre = par['prefit']
        fit = par['fit']
        tp = par['type']
        seen_types.add(tp)
        if IsConstrained(par):
            if par['pull'] < min_pull:
                min_pull = float(int(par['pull']) - 1)
            if par['pull'] > max_pull:
                max_pull = float(int(par['pull']) + 1)
            if (par["sc_fit"] - par["sc_fit_lo"]) < min_pull:
                min_pull = float(int(par["sc_fit"] - par["sc_fit_lo"]) - 1)
            if (par["sc_fit"] + par["sc_fit_hi"]) > max_pull:
                max_pull = float(int(par["sc_fit"] + par["sc_fit_hi"]) + 1)

            g_fit.SetPoint(i, par["sc_fit"], float(i) + 0.7)
            g_fit.SetPointError(i, par["sc_fit_lo"], par["sc_fit_hi"], 0., 0.)
            if par['pull_ok']:
                g_pull.SetPoint(i, par['pull'], float(i) + 0.3)
            else:
                # If pull not valid, hide it
                g_pull.SetPoint(i, 0., 9999.)

            # y1 = ROOT.gStyle.GetPadBottomMargin()
            # y2 = 1. - ROOT.gStyle.GetPadTopMargin()
            # x1 = ROOT.gStyle.GetPadLeftMargin()
            # h = (y2 - y1) / float(n_params)
            # y1 = y1 + ((float(i)+0.5) * h)
            # pleft = (1. - pads[0].GetRightMargin())
            # pright = pads[1].GetLeftMargin()
            # x1 = (1. - pads[0].GetRightMargin()) * 0.33 + pads[1].GetLeftMargin() * 0.67
            # print(x1)
            # if pdata[p]['pull_ok']:
            #     text_entries.append((0.65, y1, '{:.1f}^{{{:.1f}}}_{{{:.1f}}} ({})  {:.1f} ({})'.format(par["sc_fit"], -1. * par["sc_fit_lo"], par["sc_fit_hi"], par['rank_constraint'], par['pull'], par['rank_pull'])))
            #     # text_entries.append((0.65, y1, '{}'.format(pdata[p]['rank_pull'])))
            # else:
            #     text_entries.append((x1, y1, '--'))
        else:
            # Hide this point
            g_fit.SetPoint(i, 0., 9999.)
            g_pull.SetPoint(i, 0., 9999.)
            y1 = ROOT.gStyle.GetPadBottomMargin()
            y2 = 1. - ROOT.gStyle.GetPadTopMargin()
            x1 = ROOT.gStyle.GetPadLeftMargin()
            h = (y2 - y1) / float(n_params)
            y1 = y1 + ((float(i)+0.5) * h)
            x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
            s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
            text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom, s_hi, s_lo)))
            redo_boxes.append(i)
        g_impacts_hi.SetPoint(i, 0, float(i) + 0.5)
        g_impacts_lo.SetPoint(i, 0, float(i) + 0.5)
        if args.checkboxes:
            pboxes = pdata[p]['checkboxes']
            for pbox in pboxes:
                cboxes.index(pbox)
                g_check.SetPoint(g_check_i, cboxes.index(pbox) + 0.5, float(i) + 0.5)
                g_check_i += 1
        imp = pdata[p][POI]
        g_impacts_hi.SetPointError(i, 0, imp[2] - imp[1], 0.5, 0.5)
        g_impacts_lo.SetPointError(i, imp[1] - imp[0], 0, 0.5, 0.5)
        max_impact = max(
            max_impact, abs(imp[1] - imp[0]), abs(imp[2] - imp[1]))
        col = colors.get(tp, 2)
        if args.color_groups is not None and len(pdata[p]['groups']) >= 1:
            for p_grp in pdata[p]['groups']:
                if p_grp in color_groups:
                    col = color_groups[p_grp]
                    break
        y_bin_labels.append((i, col, pdata[p]['name']))

    h_pulls = ROOT.TH2F("pulls", "pulls", 6, -2.9, +2.9, n_params, 0, n_params)
    for i, col, name in y_bin_labels:
        h_pulls.GetYaxis().SetBinLabel(
            i + 1, ('#color[%i]{%s}'% (col, Translate(name, translate))))

    # Style and draw the pulls histo
    if externalPullDef:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title=CP.returnTitle(args.pullDef))
    else:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title='#scale[0.7]{(#hat{#theta}-#theta_{I})/#sigma_{I} #color[4]{(#hat{#theta}-#theta_{I})/#sqrt{#sigma_{I}^{2} - #sigma^{2}}}}')

    plot.Set(h_pulls.GetYaxis(), LabelSize=args.label_size, TickLength=0.0)
    h_pulls.GetYaxis().LabelsOption('v')
    h_pulls.Draw()

    for i in redo_boxes:
        newbox = boxes[i].Clone()
        newbox.Clear()
        newbox.SetY1(newbox.GetY1()+0.005)
        newbox.SetY2(newbox.GetY2()-0.005)
        newbox.SetX1(ROOT.gStyle.GetPadLeftMargin()+0.001)
        newbox.SetX2(0.7-0.001)
        newbox.Draw()
        boxes.append(newbox)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.02)
    latex.SetTextAlign(22)
    for entry in text_entries:
        latex.DrawLatex(*entry)

    # Go to the other pad and draw the impacts histo
    pads[1].cd()
    if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
    h_impacts = ROOT.TH2F(
        "impacts", "impacts", 6, -max_impact * 1.1, max_impact * 1.1, n_params, 0, n_params)
    plot.Set(h_impacts.GetXaxis(), LabelSize=0.03, TitleSize=0.04, Ndivisions=505, Title=
        '#Delta#hat{%s}' % (Translate(POI, translate)))
    plot.Set(h_impacts.GetYaxis(), LabelSize=0, TickLength=0.0)
    h_impacts.Draw()

    if args.checkboxes:
        pads[2].cd()
        h_checkboxes = ROOT.TH2F(
            "checkboxes", "checkboxes", len(cboxes), 0, len(cboxes), n_params, 0, n_params)
        for i, cbox in enumerate(cboxes):
            h_checkboxes.GetXaxis().SetBinLabel(i+1, Translate(cbox, translate))
        plot.Set(h_checkboxes.GetXaxis(), LabelSize=0.03, LabelOffset=0.002)
        h_checkboxes.GetXaxis().LabelsOption('v')
        plot.Set(h_checkboxes.GetYaxis(), LabelSize=0, TickLength=0.0)
        h_checkboxes.Draw()
        # g_check.SetFillColor(ROOT.kGreen)
        g_check.Draw('PSAME')

    # Back to the first pad to draw the pulls graph
    pads[0].cd()
    plot.Set(g_fit, MarkerSize=0.7, LineWidth=2)
    g_fit.Draw('PSAME')
    plot.Set(g_pull, MarkerSize=0.5, LineWidth=2, MarkerStyle=5, MarkerColor=4)
    g_pull.Draw('PSAME')
    # And back to the second pad to draw the impacts graphs
    pads[1].cd()
    alpha = 0.7

    lo_color = {
        'default': 38,
        'hesse': ROOT.kOrange - 3,
        'robust': ROOT.kGreen + 1
    }
    hi_color = {
        'default': 46,
        'hesse': ROOT.kBlue,
        'robust': ROOT.kAzure - 5
    }
    method = 'default'
    if 'method' in data and data['method'] in lo_color:
        method = data['method']
    g_impacts_hi.SetFillColor(plot.CreateTransparentColor(hi_color[method], alpha))
    g_impacts_hi.Draw('2SAME')
    g_impacts_lo.SetFillColor(plot.CreateTransparentColor(lo_color[method], alpha))
    g_impacts_lo.Draw('2SAME')
    pads[1].RedrawAxis()

    legend = ROOT.TLegend(0.02, 0.02, 0.35, 0.09, '', 'NBNDC')
    legend.SetNColumns(2)
    legend.AddEntry(g_fit, 'Fit', 'LP')
    legend.AddEntry(g_impacts_hi, '+1#sigma Impact', 'F')
    legend.AddEntry(g_pull, 'Pull', 'P')
    legend.AddEntry(g_impacts_lo, '-1#sigma Impact', 'F')
    legend.Draw()

    leg_width = pads[0].GetLeftMargin() - 0.01
    if args.color_groups is not None:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_group_hists.items():
            legend2.AddEntry(h, Translate(name, translate), 'F')
        legend2.Draw()
    elif len(seen_types) > 1:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_hists.items():
            if name == 'Unrecognised': continue
            legend2.AddEntry(h, name, 'F')
        legend2.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.cms_label, 0, 0.25, 0.00, 0.00)
    s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
    if not args.blind:
        plot.DrawTitle(pads[1], '#hat{%s} = %s^{#plus%s}_{#minus%s}%s' % (
            Translate(POI, translate), s_nom, s_hi, s_lo,
            '' if args.units is None else ' '+args.units), 3, 0.27)
    extra = ''
    if page == 0:
        extra = '('
    if page == n - 1:
        extra = ')'
    canv.Print('.pdf%s' % extra)
