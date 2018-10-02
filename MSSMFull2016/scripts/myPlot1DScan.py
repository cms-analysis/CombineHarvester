#!/usr/bin/env python
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

plot.ModTDRStyle(width=700, l = 0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)

NAMECOUNTER = 0

def read(scan, param, files, chop, remove_near_min, rezero, remove_delta = None, improve = False):
    # print files
    goodfiles = [f for f in files if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    # require quantileExpected > -0.5 to avoid the final point which is always committed twice
    # (even if the fit fails)
    graph = plot.TGraphFromTree(limit, param, '2*deltaNLL', 'quantileExpected > -1.5')
    graph.SetName(scan)
    graph.Sort()
    plot.RemoveGraphXDuplicates(graph)
    if remove_delta is not None: plot.RemoveSmallDelta(graph, remove_delta)
    plot.RemoveGraphYAbove(graph, chop)
    plot.ReZeroTGraph(graph, rezero)
    if remove_near_min is not None: plot.RemoveNearMin(graph, remove_near_min)
    if improve:
        global NAMECOUNTER
        spline = ROOT.TSpline3("spline3", graph)
        func = ROOT.TF1('splinefn'+str(NAMECOUNTER), partial(Eval, spline), graph.GetX()[0], graph.GetX()[graph.GetN() - 1], 1)
        NAMECOUNTER += 1
        plot.ImproveMinimum(graph, func, True)
    # graph.Print()
    return graph

def Eval(obj, x, params):
    return obj.Eval(x[0])


def ProcessEnvelope(main, others, relax_safety = 0):
    '[ProcessEnvelope] Will create envelope from %i other scans' % len(others)
    vals = {}
    for oth in others:
        gr = oth['graph']
        for i in xrange(gr.GetN()):
            x = gr.GetX()[i]
            y = gr.GetY()[i]
            if x not in vals: vals[x] = []
            vals[x].append(y)
    lengths = []
    for key in sorted(vals):
        # print '%f %i' % (key,len(vals[key]))
        lengths.append(len(vals[key]))
    mode = max(set(lengths), key=lengths.count)
    to_del = []
    for key in sorted(vals):
        if len(vals[key]) < (mode - relax_safety): to_del.append(key)
    for x in to_del: del vals[x]

    gr = ROOT.TGraph()
    gr.Set(len(vals)) # will not contain the best fit
    for i, key in enumerate(sorted(vals)):
        gr.SetPoint(i, key, min(vals[key]))

    spline = ROOT.TSpline3("spline3", gr)
    global NAMECOUNTER
    func = ROOT.TF1('splinefn'+str(NAMECOUNTER), partial(Eval, spline), gr.GetX()[0], gr.GetX()[gr.GetN() - 1], 1)
    min_x, min_y = plot.ImproveMinimum(gr, func)
    gr.Set(len(vals)+1)
    gr.SetPoint(len(vals), min_x, min_y)
    gr.Sort()

    for i in xrange(gr.GetN()):
        gr.GetY()[i] -= min_y
    for oth in others:
        for i in xrange(oth['graph'].GetN()):
            oth['graph'].GetY()[i] -= min_y

    plot.RemoveGraphXDuplicates(gr)
    gr.Print()
    return gr



def BuildScan(scan, param, files, color, yvals, chop, remove_near_min = None, rezero = False, envelope = False, pregraph = None, remove_delta = None, improve = False):
    if pregraph is None:
        graph = read(scan, param, files, chop, remove_near_min, rezero, remove_delta, improve)
    else:
        graph = pregraph
    bestfit = None
    for i in xrange(graph.GetN()):
        print graph.GetY()[i]
        if graph.GetY()[i] == 0.:
            bestfit = graph.GetX()[i]
    if envelope: plot.RemoveGraphYAll(graph, 0.)
    graph.SetMarkerColor(color)
    spline = ROOT.TSpline3("spline3", graph)
    global NAMECOUNTER
    func = ROOT.TF1('splinefn'+str(NAMECOUNTER), partial(Eval, spline), graph.GetX()[0], graph.GetX()[graph.GetN() - 1], 1)
    NAMECOUNTER += 1
    func.SetLineColor(color)
    func.SetLineWidth(3)
    assert(bestfit is not None)
    if not envelope: plot.ImproveMinimum(graph, func)
    crossings = {}
    cross_1sig = None
    cross_2sig = None
    other_1sig = []
    other_2sig = []
    val = None
    val_2sig = None
    for yval in yvals:
        crossings[yval] = plot.FindCrossingsWithSpline(graph, func, yval)
        for cr in crossings[yval]:
            cr["contains_bf"] = cr["lo"] <= bestfit and cr["hi"] >= bestfit
    for cr in crossings[yvals[0]]:
        if cr['contains_bf']:
            val = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
            cross_1sig = cr
        else:
            other_1sig.append(cr)
    if len(yvals) > 1:
        for cr in crossings[yvals[1]]:
            if cr['contains_bf']:
                val_2sig = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
                cross_2sig = cr
            else:
                other_2sig.append(cr)
    else:
        val_2sig = (0., 0., 0.)
        cross_2sig = cross_1sig
    return {
        "graph"     : graph,
        "spline"    : spline,
        "func"      : func,
        "crossings" : crossings,
        "val"       : val,
        "val_2sig": val_2sig,
        "cross_1sig" : cross_1sig,
        "cross_2sig" : cross_2sig,
        "other_1sig" : other_1sig,
        "other_2sig" : other_2sig
    }

parser = argparse.ArgumentParser(
    prog='plot1DScan.py',
    )

parser.add_argument('--no-input-label', action='store_true', help='do not draw the input label')
parser.add_argument('--no-numbers', action='store_true', help='do not draw the input label')
parser.add_argument('--improve', action='store_true', help='use spline interp to correct to a better minimum')
parser.add_argument('--remove-delta', type=float, help='remove best fit and close-by points')
parser.add_argument('--no-box', action='store_true', help='do not draw the input label')
parser.add_argument('--pub', action='store_true', help='do not draw the input label')
parser.add_argument('--signif', action='store_true', help='do significance plot')
parser.add_argument('--envelope', action='store_true', help='do envelope plot')
parser.add_argument('--upper-cl', type=float, help='quote upper limit instead')
parser.add_argument('--chop', type=float, default=7., help='remove vals above')
parser.add_argument('--y-max', type=float, default=8., help='max y to draw')
parser.add_argument('--remove-near-min', type=float, help='remove points with this fraction of the average x-spacing to the best-fit point')
parser.add_argument('--rezero', action='store_true', help='correct y-values if a point with a lower minimum than zero is found')
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--main', '-m', help='Main input file for the scan')
parser.add_argument('--json', help='update this json file')
parser.add_argument('--model', help='use this model identifier')
parser.add_argument('--POI', help='use this parameter of interest')
parser.add_argument('--translate', default=None, help='json file with POI name translation')
parser.add_argument('--main-label', default='Observed', type=str, help='legend label for the main scan')
parser.add_argument('--main-color', default=1, type=int, help='line and marker color for main scan')
parser.add_argument('--relax-safety', default=0, type=int, help='line and marker color for main scan')
parser.add_argument('--others', nargs='*', help='add secondary scans processed as main: FILE:LABEL:COLOR')
parser.add_argument('--breakdown', help='do quadratic error subtraction using --others')
parser.add_argument('--meta', default='', help='Other metadata to save in format KEY:VAL,KEY:VAL')
parser.add_argument('--logo', default='CMS')
parser.add_argument('--logo-sub', default='Internal')
args = parser.parse_args()
if args.pub: args.no_input_label = True


print '--------------------------------------'
print  args.output
print '--------------------------------------'

fixed_name = args.POI
if args.translate is not None:
    with open(args.translate) as jsonfile:    
        name_translate = json.load(jsonfile)
    if args.POI in name_translate:
        fixed_name = name_translate[args.POI]

yvals = [1., 4.]
if args.upper_cl is not None:
    yvals = [ROOT.Math.chisquared_quantile(args.upper_cl, 1)]

main_scan = BuildScan(args.output, args.POI, [args.main], args.main_color, yvals, args.chop, args.remove_near_min, args.rezero, remove_delta = args.remove_delta, improve = args.improve)

other_scans = [ ]
other_scans_opts = [ ]
if args.others is not None:
    for oargs in args.others:
        splitargs = oargs.split(':')
        other_scans_opts.append(splitargs)
        other_scans.append(BuildScan(args.output, args.POI, [splitargs[0]], int(splitargs[2]), yvals, args.chop, args.remove_near_min if args.envelope is False else None, args.rezero, args.envelope,  remove_delta = args.remove_delta, improve = args.improve))

if args.envelope:
    new_gr = ProcessEnvelope(main_scan, other_scans, args.relax_safety)
    main_scan = BuildScan(args.output, args.POI, [args.main], args.main_color, yvals, args.chop, args.remove_near_min, args.rezero, pregraph = new_gr)
    for other in other_scans:
        color = other['func'].GetLineColor()
        other['spline'] = ROOT.TSpline3("spline3", other['graph'])
        other['func'] = ROOT.TF1('splinefn'+str(NAMECOUNTER), partial(Eval, other['spline']), other['graph'].GetX()[0], other['graph'].GetX()[other['graph'].GetN() - 1], 1)
        NAMECOUNTER += 1
        other['func'].SetLineColor(color)
        other['func'].SetLineWidth(2)
        # other['func'].SetLineStyle(2)
        other['graph'].SetMarkerSize(0.4)

canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
if args.pub: main_scan['graph'].SetMarkerSize(0)
main_scan['graph'].SetMarkerColor(1)
main_scan['graph'].SetLineColor(ROOT.kBlue)
main_scan['graph'].SetLineStyle(2)
main_scan['graph'].SetLineWidth(3)
main_scan['graph'].Draw('APL')
# main_scan['graph'].Fit('pol4')
# polfunc = main_scan['graph'].GetFunction('pol4')
# print 'Function min at %f' % polfunc.GetMinimumX(0.05, 0.25)


axishist = plot.GetAxisHist(pads[0])
# axishist.SetMinimum(1E-5)
# pads[0].SetLogy(True)
axishist.SetMaximum(args.y_max)
axishist.GetYaxis().SetTitle("- 2 #Delta ln L")
axishist.GetXaxis().SetTitle("%s" % fixed_name)

# main_scan['graph'].Draw('PSAME')


new_min = axishist.GetXaxis().GetXmin()
new_max = axishist.GetXaxis().GetXmax()
mins = []
maxs = []
for other in other_scans:
    mins.append(other['graph'].GetX()[0])
    maxs.append(other['graph'].GetX()[other['graph'].GetN()-1])

if len(other_scans) > 0:
    if min(mins) < main_scan['graph'].GetX()[0]:
        new_min = min(mins) - (main_scan['graph'].GetX()[0] - new_min)
    if max(maxs) > main_scan['graph'].GetX()[main_scan['graph'].GetN()-1]:
        new_max = max(maxs) + (new_max - main_scan['graph'].GetX()[main_scan['graph'].GetN()-1])
    axishist.GetXaxis().SetLimits(new_min, new_max)

for other in other_scans:
    if args.breakdown is not None:
        other['graph'].SetMarkerSize(0.4)
    if args.pub: other['graph'].SetMarkerSize(0.0)
    other['graph'].Draw('PSAME')

line = ROOT.TLine()
line.SetLineColor(16)
# line.SetLineStyle(7)
for yval in yvals:
    plot.DrawHorizontalLine(pads[0], line, yval)
    if (len(other_scans) == 0 or args.upper_cl is not None) and args.pub is False:
        for cr in main_scan['crossings'][yval]:
            if cr['valid_lo']: line.DrawLine(cr['lo'], 0, cr['lo'], yval)
            if cr['valid_hi']: line.DrawLine(cr['hi'], 0, cr['hi'], yval)

main_scan['func'].Draw('same')
main_scan['graph'].Draw('PLSAME')
for other in other_scans:
    if args.breakdown is not None:
        other['func'].SetLineStyle(2)
        other['func'].SetLineWidth(2)
    if args.pub:
        other['func'].SetLineStyle(2)
    other['func'].Draw('SAME')


if args.envelope:
    main_scan['graph'].Draw('PSAME')

# if len(args) >= 4:
#     syst_scan = BuildScan(args.output, args.POI, [args[3]], ROOT.kBlue, yvals)
#     syst_scan['graph'].Draw('sameP')
#     syst_scan['func'].Draw('same')


box = ROOT.TBox(axishist.GetXaxis().GetXmin(), 0.625*args.y_max, axishist.GetXaxis().GetXmax(), args.y_max)
# box = ROOT.TBox(axishist.GetXaxis().GetXmin(), 4.5, axishist.GetXaxis().GetXmax(), 7)
if not args.no_box: box.Draw()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

crossings = main_scan['crossings']
val_nom = main_scan['val']
val_2sig = main_scan['val_2sig']

textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f}' % (fixed_name, val_nom[0], val_nom[1], abs(val_nom[2]))
if args.upper_cl:
    textfit = '%s < %.3f (%i%% CL)' % (fixed_name, val_nom[0]+val_nom[1], int(args.upper_cl * 100))

pt = ROOT.TPaveText(0.59, 0.82 - len(other_scans)*0.08, 0.95, 0.91, 'NDCNB')
if args.envelope: pt.SetY2(0.78)
if args.envelope: pt.SetY1(0.66)
pt.AddText(textfit)

if args.breakdown is None and args.envelope is False:
    for i, other in enumerate(other_scans):
        textfit = '#color[%s]{%s = %.3f{}^{#plus %.3f}_{#minus %.3f}}' % (other_scans_opts[i][2], fixed_name, other['val'][0], other['val'][1], abs(other['val'][2]))
        if args.upper_cl:
            print 'here'
            textfit = '#color[%s]{%s < %.3f (%i%% CL)}' % (other_scans_opts[i][2], fixed_name, other['val'][1], int(args.upper_cl * 100))
        pt.AddText(textfit)
    
breakdown_json = {}
if args.breakdown is not None:
    pt.SetX1(0.50)
    if len(other_scans) >= 3:
        pt.SetX1(0.19)
        pt.SetX2(0.88)
        pt.SetY1(0.66)
        pt.SetY2(0.82)
    breakdown = args.breakdown.split(',')
    v_hi = [val_nom[1]]
    v_lo = [val_nom[2]]
    for other in other_scans:
        v_hi.append(other['val'][1])
        v_lo.append(other['val'][2])
    assert(len(v_hi) == len(breakdown))
    textfit = '%s = %.3f' % (fixed_name, val_nom[0])
    for i, br in enumerate(breakdown):
        if i < (len(breakdown) - 1):
            if (abs(v_hi[i+1]) > abs(v_hi[i])):
                print 'ERROR SUBTRACTION IS NEGATIVE FOR %s HI' % br
                hi = 0.
            else:
                hi = math.sqrt(v_hi[i]*v_hi[i] - v_hi[i+1]*v_hi[i+1])
            if (abs(v_lo[i+1]) > abs(v_lo[i])):
                print 'ERROR SUBTRACTION IS NEGATIVE FOR %s LO' % br
                lo = 0.
            else:
                lo = math.sqrt(v_lo[i]*v_lo[i] - v_lo[i+1]*v_lo[i+1])
        else:
            hi = v_hi[i]
            lo = v_lo[i]
        breakdown_json[br+"Hi"] = hi
        breakdown_json[br+"Lo"] = abs(lo) * -1.
        textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi, abs(lo), br)
    pt.AddText(textfit)
    # hi_1 = math.sqrt(val_nom[1]*val_nom[1] - other_scans[0]['val'][1]*other_scans[0]['val'][1])
    # lo_1 = math.sqrt(val_nom[2]*val_nom[2] - other_scans[0]['val'][2]*other_scans[0]['val'][2])
    # textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f}(%s)' % (fixed_name, val_nom[0], hi_1, lo_1, breakdown[0])
    # hi_2 = math.sqrt(other_scans[0]['val'][1]*other_scans[0]['val'][1] - other_scans[1]['val'][1]*other_scans[1]['val'][1])
    # lo_2 = math.sqrt(other_scans[0]['val'][2]*other_scans[0]['val'][2] - other_scans[1]['val'][2]*other_scans[1]['val'][2])
    # hi_3 = math.sqrt(other_scans[1]['val'][1]*other_scans[1]['val'][1] - other_scans[2]['val'][1]*other_scans[2]['val'][1])
    # lo_3 = math.sqrt(other_scans[1]['val'][2]*other_scans[1]['val'][2] - other_scans[2]['val'][2]*other_scans[2]['val'][2])
    # textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi_3, lo_3, breakdown[2])
    # hi_4 = math.sqrt(other_scans[2]['val'][1]*other_scans[2]['val'][1])
    # lo_4 = math.sqrt(other_scans[2]['val'][2]*other_scans[2]['val'][2])
    # textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi_4, lo_4, breakdown[3])


# print textfit
# textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f} (stat.)' % (fixed_name, syst_scan['val'][0], abs(syst_scan['val'][1]), abs(syst_scan['val'][2]))

signif = None
signif_x = None
signif_y = None
if args.signif:
    gr = main_scan['graph']
    for i in xrange(gr.GetN()):
        if abs(gr.GetX()[i] - 0.) < 1E-4:
            print 'Found scan point at %s = %.6f' % (args.POI, gr.GetX()[i])
            pt.SetY1(pt.GetY1() - 0.1)
            pt.SetX1(0.52)
            signif = ROOT.Math.normal_quantile_c(ROOT.Math.chisquared_cdf_c(gr.GetY()[i], 1)/2., 1)
            signif_x = gr.GetX()[i]
            signif_y = gr.GetY()[i]
            txt_cross  = '[-2#DeltalnL @ %s = %.1f is %.3f]' % (fixed_name, gr.GetX()[i], gr.GetY()[i])
            txt_signif = '[Significance = %.2f#sigma]' % (signif)
            pt.AddText(txt_cross)
            pt.AddText(txt_signif)
            print '-2#DeltalnL @ %s = %.1f is %.3f]' % (fixed_name, 1., main_scan['func'].Eval(1.0))


# pt.AddText(textfit)
# if len(args) >= 4:
#     syst_hi = math.sqrt(val_nom[1]*val_nom[1] - syst_scan['val'][1] * syst_scan['val'][1])
#     syst_lo = math.sqrt(val_nom[2]*val_nom[2] - syst_scan['val'][2] * syst_scan['val'][2])
#     textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f} (stat.){}^{#plus %.3f}_{#minus %.3f} (syst.)' % (fixed_name, syst_scan['val'][0], abs(syst_scan['val'][1]), abs(syst_scan['val'][2]), syst_hi, syst_lo)
#     pt.AddText(textfit)
pt.SetTextAlign(11)
pt.SetTextFont(42)
if not args.no_numbers: pt.Draw()


if args.json is not None:
    if os.path.isfile(args.json):
        with open(args.json) as jsonfile:    
            js = json.load(jsonfile)
    else:
        js = {}
    if not args.model in js: js[args.model] = {}
    js[args.model][args.POI] = {
        'Val' : val_nom[0],
        'ErrorHi' : val_nom[1],
        'ErrorLo' : val_nom[2],
        'ValidErrorHi' : main_scan['cross_1sig']['valid_hi'],
        'ValidErrorLo' : main_scan['cross_1sig']['valid_lo'],
        '2sig_ErrorHi' : val_2sig[1],
        '2sig_ErrorLo' : val_2sig[2],
        '2sig_ValidErrorHi' : main_scan['cross_2sig']['valid_hi'],
        '2sig_ValidErrorLo' : main_scan['cross_2sig']['valid_lo']
    }
    if signif is not None:
      js[args.model][args.POI].update({
          'Signif' : signif,
          'Signif_x' : signif_x,
          'Signif_y' : signif_y
      })
    if args.breakdown is not None:
        js[args.model][args.POI].update(breakdown_json)
    if args.envelope is not None:
        print main_scan['other_1sig']
        print main_scan['other_2sig']
        js_extra = {
            'OtherLimitLo': 0.,
            'OtherLimitHi': 0.,
            '2sig_OtherLimitLo': 0.,
            '2sig_OtherLimitHi': 0.,
            'ValidOtherLimitLo': False,
            'ValidOtherLimitHi': False,
            '2sig_ValidOtherLimitLo': False,
            '2sig_ValidOtherLimitHi': False
        }
        if len(main_scan['other_1sig']) >= 1:
            other = main_scan['other_1sig'][0]
            js_extra['OtherLimitLo'] = other['lo']
            js_extra['OtherLimitHi'] = other['hi']
            js_extra['ValidOtherLimitLo'] = other['valid_lo']
            js_extra['ValidOtherLimitHi'] = other['valid_hi']
        if len(main_scan['other_2sig']) >= 1:
            other = main_scan['other_2sig'][0]
            js_extra['2sig_OtherLimitLo'] = other['lo']
            js_extra['2sig_OtherLimitHi'] = other['hi']
            js_extra['2sig_ValidOtherLimitLo'] = other['valid_lo']
            js_extra['2sig_ValidOtherLimitHi'] = other['valid_hi']
        js[args.model][args.POI].update(js_extra)

    with open(args.json, 'w') as outfile:
        json.dump(js, outfile, sort_keys=True, indent=4, separators=(',', ': '))

collab = 'Combined'
if 'cms_' in args.output: collab = 'CMS'
if 'atlas_' in args.output: collab = 'ATLAS'

plot.DrawCMSLogo(pads[0], args.logo, args.logo_sub, 11, 0.045, 0.035, 1.2,  cmsTextSize = 1.)
# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1 Preliminary}', 11, 0.025, 0.035, 1.1, cmsTextSize = 1.)

#if not args.no_input_label: plot.DrawTitle(pads[0], '#bf{Input:} %s' % collab, 3)
plot.DrawTitle(pads[0], '35.9 fb^{-1} (13 TeV)', 3)
#plot.DrawTitle(pads[0], 'm_{H} = 125 GeV', 1)

#info = ROOT.TPaveText(0.59, 0.75, 0.95, 0.91, 'NDCNB')
#info.SetTextFont(42)
#info.SetTextAlign(12)
#info.AddText('#bf{ttH combination}')
#info.AddText('HIG-15-005 H#rightarrow#gamma#gamma')
#info.AddText('HIG-15-008 H#rightarrowleptons')
#info.AddText('HIG-16-004 H#rightarrowbb')
#info.Draw()
# legend_l = 0.70 if len(args) >= 4 else 0.73
legend_l = 0.69
if len(other_scans) > 0:
    legend_l = legend_l - len(other_scans) * 0.04
legend = ROOT.TLegend(0.15, legend_l, 0.45, 0.78, '', 'NBNDC')
if len(other_scans) >= 3:
    if args.envelope:
        legend = ROOT.TLegend(0.58, 0.79, 0.95, 0.93, '', 'NBNDC')
        legend.SetNColumns(2)
    else:
        legend = ROOT.TLegend(0.46, 0.83, 0.95, 0.93, '', 'NBNDC')
        legend.SetNColumns(2)

legend.AddEntry(main_scan['func'], args.main_label + ': %.2f{}^{#plus %.2f}_{#minus %.2f}' % (val_nom[0], val_nom[1], abs(val_nom[2])), 'L')
for i, other in enumerate(other_scans):
    legend.AddEntry(other['func'], other_scans_opts[i][1] + ': %.2f{}^{#plus %.2f}_{#minus %.2f}' % (other['val'][0], other['val'][1], abs(other['val'][2])), 'L')
# if len(args) >= 4: legend.AddEntry(syst_scan['func'], 'Stat. Only', 'L')
legend.Draw()

save_graph = main_scan['graph'].Clone()
save_graph.GetXaxis().SetTitle('%s = %.3f %+.3f/%+.3f' % (fixed_name, val_nom[0], val_nom[2], val_nom[1]))
outfile = ROOT.TFile(args.output+'.root', 'RECREATE')
outfile.WriteTObject(save_graph)
outfile.Close()
canv.Print('.pdf')
canv.Print('.png')

meta = {}

if args.meta != '':
    meta_list = args.meta.split(',')
    for m in meta_list:
        meta_pair = m.split(':')
        meta[meta_pair[0]] = meta_pair[1]
    with open(args.output+'.json', 'w') as outmeta:
        json.dump(meta, outmeta, sort_keys=True, indent=4, separators=(',', ': '))

# canv.Print('.C')
