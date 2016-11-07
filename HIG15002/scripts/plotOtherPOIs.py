#!/usr/bin/env python
# import sys
import ROOT
# import math
# from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
# import os.path

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(width=700, l=0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)

NAMECOUNTER = 0


def read(scan, param, other_param, files, remove_dups=True):
    # print files
    goodfiles = [f for f in files if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    graph = plot.TGraphFromTree(
        limit, param, other_param, 'quantileExpected > -0.5')
    # print 'INPUT'
    # graph.Print()
    graph.SetName(scan)
    graph.Sort()
    if remove_dups:
        plot.RemoveGraphXDuplicates(graph)
    # graph.Print()
    return graph


def Eval(obj, x, params):
    return obj.Eval(x[0])


parser = argparse.ArgumentParser()

# parser.add_argument(
#     '--no-input-label', action='store_true', help='do not draw the input label')
# parser.add_argument(
#     '--no-numbers', action='store_true', help='do not draw the input label')
# parser.add_argument('--improve', action='store_true',
#                     help='use spline interp to correct to a better minimum')
# parser.add_argument(
#     '--remove-delta', type=float, help='remove best fit and close-by points')
# parser.add_argument(
#     '--remin-main', action='store_true', help='remove the deltaNLL=0 point in the main scan and run improve')
# parser.add_argument(
#     '--no-box', action='store_true', help='do not draw the input label')
# parser.add_argument(
#     '--pub', action='store_true', help='do not draw the input label')
# parser.add_argument('--signif', action='store_true', help='do significance plot')
# parser.add_argument('--envelope', action='store_true', help='do envelope plot')
# parser.add_argument('--old-envelope', action='store_true', help='do envelope plot (old method)')
# parser.add_argument('--hide-envelope', action='store_true', help='do not show envelope markers')
# parser.add_argument('--upper-cl', type=float, help='quote upper limit instead')
# parser.add_argument('--chop', type=float, default=7., help='remove vals above')
parser.add_argument('--y-max', type=float, default=5., help='max y to draw')
parser.add_argument('--y-min', type=float, default=-5., help='min y to draw')
# parser.add_argument('--remove-near-min', type=float,
#                     help='remove points with this fraction of the average x-spacing to the best-fit point')
# parser.add_argument('--rezero', action='store_true',
#                     help='correct y-values if a point with a lower minimum than zero is found')
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--main', '-m', help='Main input file for the scan')
# parser.add_argument('--json', help='update this json file')
# parser.add_argument('--model', help='use this model identifier')
parser.add_argument('--POI', help='use this parameter of interest')
parser.add_argument('--other-POIs', help='list of other POIs')
# parser.add_argument('--POI-line', default=None)
parser.add_argument('--translate', default='texName.json',
                    help='json file with POI name translation')
# parser.add_argument('--main-label', default='Observed',
#                     type=str, help='legend label for the main scan')
# parser.add_argument(
#     '--main-color', default=1, type=int, help='line and marker color for main scan')
# parser.add_argument('--relax-safety', default=0, type=int,
#                     help='line and marker color for main scan')
# parser.add_argument('--others', nargs='*',
#                     help='add secondary scans processed as main: FILE:LABEL:COLOR')
# parser.add_argument(
#     '--breakdown', help='do quadratic error subtraction using --others')
# parser.add_argument(
#     '--meta', default='', help='Other metadata to save in format KEY:VAL,KEY:VAL')
# parser.add_argument('--legend-pos', default=1, type=int, help='Predefined legend area')
# parser.add_argument('--box-frac', default=0.625, type=float, help='fraction of the pad occupied by box')
# parser.add_argument('--x-title', default=None)
# parser.add_argument('--x-range', default=None)
# parser.add_argument('--premade', action='store_true')
# parser.add_argument('--vertical-line', type=float, default=None)

args = parser.parse_args()
# if args.pub:
#     args.no_input_label = True


print '--------------------------------------'
print args.output
print '--------------------------------------'

fixed_name = args.POI
if args.translate is not None:
    with open(args.translate) as jsonfile:
        name_translate = json.load(jsonfile)
    if args.POI in name_translate:
        fixed_name = name_translate[args.POI]

graphs = []

POIs = args.other_POIs.split(',')

print POIs

for poi in POIs:
    if poi == args.POI: continue
    graphs.append(read(poi, args.POI, poi, [args.main]))


canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()

colors = [1, 2, 4, 6, 8, 45, 28, 38]


axishist = plot.CreateAxisHist(graphs[0], True)
axishist.SetMinimum(args.y_min)
axishist.SetMaximum(args.y_max)
pads[0].cd()
axishist.Draw()

legend = ROOT.TLegend(0.15, 0.6, 0.5, 0.9, '', 'NBNDC')

for gr in graphs:
    gr.SetLineColor(colors.pop())
    gr.SetLineWidth(2)
    legend.AddEntry(gr, name_translate[gr.GetName()], 'L')
    gr.Draw('CSAME')

legend.Draw()
# # axishist.GetYaxis().SetTitle("- 2 #Delta ln #Lambda(%s)" % fixed_name)
axishist.GetYaxis().SetTitle("Parameter value")
axishist.GetXaxis().SetTitle("%s" % fixed_name)
# if args.x_title is not None:
#     axishist.GetXaxis().SetTitle(args.x_title)

# # main_scan['graph'].Draw('PSAME')


# new_min = axishist.GetXaxis().GetXmin()
# new_max = axishist.GetXaxis().GetXmax()
# mins = []
# maxs = []
# for other in other_scans:
#     mins.append(other['graph'].GetX()[0])
#     maxs.append(other['graph'].GetX()[other['graph'].GetN() - 1])

# if len(other_scans) > 0:
#     if min(mins) < main_scan['graph'].GetX()[0]:
#         new_min = min(mins) - (main_scan['graph'].GetX()[0] - new_min)
#     if max(maxs) > main_scan['graph'].GetX()[main_scan['graph'].GetN() - 1]:
#         new_max = max(maxs) + (new_max - main_scan['graph'].GetX()[main_scan['graph'].GetN() - 1])
#     axishist.GetXaxis().SetLimits(new_min, new_max)

# if args.x_range is not None:
#     axishist.GetXaxis().SetLimits(float(args.x_range.split(',')[0]), float(args.x_range.split(',')[1]))

# if args.vertical_line is not None:
#     vline = ROOT.TLine()
#     plot.Set(vline, LineColor=16, LineWidth=1, LineStyle=7)
#     plot.DrawVerticalLine(pads[0], vline, args.vertical_line)

# if args.breakdown and args.envelope:
#     for other in new_others:
#         other['graph'].Draw('PSAME')

# for other in other_scans:
#     if args.breakdown is not None:
#         other['graph'].SetMarkerSize(0.4)
#     if args.pub:
#         other['graph'].SetMarkerSize(0.0)
#     other['graph'].Draw('PSAME')

# line = ROOT.TLine()
# for i, yval in enumerate(yvals):
#     line.SetLineColor(ROOT.kRed)
#     if args.pub and i > 0:
#         line.SetLineColor(ROOT.kGreen+2)
#     plot.DrawHorizontalLine(pads[0], line, yval)
#     if (len(other_scans) == 0 or args.upper_cl is not None) and args.pub is False:
#         for cr in main_scan['crossings'][yval]:
#             if cr['valid_lo']:
#                 line.DrawLine(cr['lo'], 0, cr['lo'], yval)
#             if cr['valid_hi']:
#                 line.DrawLine(cr['hi'], 0, cr['hi'], yval)


# main_scan['func'].Draw('same')
# for other in other_scans:
#     if args.breakdown is not None:
#         other['func'].SetLineStyle(2)
#         other['func'].SetLineWidth(2)
#     if args.pub:
#         other['func'].SetLineStyle(2)
#     if args.hide_envelope:
#         other['func'].SetLineWidth(1)
#         other['graph'].Draw('PSAME') # redraw this
#         # other['func'].SetLineWidth(3)
#     other['func'].Draw('SAME')

# if args.breakdown and args.envelope:
#     for other in new_others:
#         # other['func'].SetLineStyle(2)
#         other['func'].SetLineWidth(1)
#         other['func'].Draw('SAME')

# if args.envelope:
#     main_scan['graph'].Draw('PSAME')

# # if len(args) >= 4:
# #     syst_scan = BuildScan(args.output, args.POI, [args[3]], ROOT.kBlue, yvals)
# #     syst_scan['graph'].Draw('sameP')
# #     syst_scan['func'].Draw('same')


# box = ROOT.TBox(axishist.GetXaxis().GetXmin(), args.box_frac *
#                 args.y_max, axishist.GetXaxis().GetXmax(), args.y_max)
# # box = ROOT.TBox(axishist.GetXaxis().GetXmin(), 4.5, axishist.GetXaxis().GetXmax(), 7)
# if not args.no_box:
#     box.Draw()
#     if args.vertical_line is not None:
#         vline.DrawLine(args.vertical_line, args.box_frac *
#                 args.y_max, args.vertical_line, args.y_max)
# pads[0].GetFrame().Draw()
# pads[0].RedrawAxis()

# crossings = main_scan['crossings']
# val_nom = main_scan['val']
# val_2sig = main_scan['val_2sig']

# textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f}' % (
#     fixed_name, val_nom[0], val_nom[1], abs(val_nom[2]))
# if args.upper_cl:
#     textfit = '%s < %.2f (%i%% CL)' % (
#         fixed_name, val_nom[0] + val_nom[1], int(args.upper_cl * 100))

# pt = ROOT.TPaveText(0.59, 0.82 - len(other_scans) * 0.08, 0.95, 0.91, 'NDCNB')
# if args.envelope:
#     pt.SetY2(0.78)
# if args.envelope:
#     pt.SetY1(0.66)
# pt.AddText(textfit)

# if args.breakdown is None and args.envelope is False:
#     for i, other in enumerate(other_scans):
#         textfit = '#color[%s]{%s = %.3f{}^{#plus %.3f}_{#minus %.3f}}' % (
#             other_scans_opts[i][2], fixed_name, other['val'][0], other['val'][1], abs(other['val'][2]))
#         if args.upper_cl:
#             print 'here'
#             textfit = '#color[%s]{%s < %.2f (%i%% CL)}' % (
#                 other_scans_opts[i][2], fixed_name, other['val'][1], int(args.upper_cl * 100))
#         pt.AddText(textfit)

# breakdown_json = {}
# if args.breakdown is not None:
#     pt.SetX1(0.50)
#     if len(other_scans) >= 3:
#         pt.SetX1(0.19)
#         pt.SetX2(0.88)
#         pt.SetY1(0.66)
#         pt.SetY2(0.82)
#     breakdown = args.breakdown.split(',')
#     v_hi = [val_nom[1]]
#     v_lo = [val_nom[2]]
#     for other in other_scans:
#         v_hi.append(other['val'][1])
#         v_lo.append(other['val'][2])
#     assert(len(v_hi) == len(breakdown))
#     textfit = '%s = %.3f' % (fixed_name, val_nom[0])
#     for i, br in enumerate(breakdown):
#         if i < (len(breakdown) - 1):
#             if (abs(v_hi[i + 1]) > abs(v_hi[i])):
#                 print 'ERROR SUBTRACTION IS NEGATIVE FOR %s HI' % br
#                 hi = 0.
#             else:
#                 hi = math.sqrt(v_hi[i] * v_hi[i] - v_hi[i + 1] * v_hi[i + 1])
#             if (abs(v_lo[i + 1]) > abs(v_lo[i])):
#                 print 'ERROR SUBTRACTION IS NEGATIVE FOR %s LO' % br
#                 lo = 0.
#             else:
#                 lo = math.sqrt(v_lo[i] * v_lo[i] - v_lo[i + 1] * v_lo[i + 1])
#         else:
#             hi = v_hi[i]
#             lo = v_lo[i]
#         breakdown_json[br + "Hi"] = hi
#         breakdown_json[br + "Lo"] = abs(lo) * -1.
#         textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi, abs(lo), br)
#     pt.AddText(textfit)
#     # hi_1 = math.sqrt(val_nom[1]*val_nom[1] - other_scans[0]['val'][1]*other_scans[0]['val'][1])
#     # lo_1 = math.sqrt(val_nom[2]*val_nom[2] - other_scans[0]['val'][2]*other_scans[0]['val'][2])
#     # textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f}(%s)' % (fixed_name, val_nom[0], hi_1, lo_1, breakdown[0])
#     # hi_2 = math.sqrt(other_scans[0]['val'][1]*other_scans[0]['val'][1] - other_scans[1]['val'][1]*other_scans[1]['val'][1])
#     # lo_2 = math.sqrt(other_scans[0]['val'][2]*other_scans[0]['val'][2] - other_scans[1]['val'][2]*other_scans[1]['val'][2])
#     # hi_3 = math.sqrt(other_scans[1]['val'][1]*other_scans[1]['val'][1] - other_scans[2]['val'][1]*other_scans[2]['val'][1])
#     # lo_3 = math.sqrt(other_scans[1]['val'][2]*other_scans[1]['val'][2] - other_scans[2]['val'][2]*other_scans[2]['val'][2])
#     # textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi_3, lo_3, breakdown[2])
#     # hi_4 = math.sqrt(other_scans[2]['val'][1]*other_scans[2]['val'][1])
#     # lo_4 = math.sqrt(other_scans[2]['val'][2]*other_scans[2]['val'][2])
#     # textfit += '{}^{#plus %.3f}_{#minus %.3f}(%s)' % (hi_4, lo_4, breakdown[3])


# # print textfit
# # textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f} (stat.)' %
# # (fixed_name, syst_scan['val'][0], abs(syst_scan['val'][1]),
# # abs(syst_scan['val'][2]))

# signif = None
# signif_x = None
# signif_y = None
# if args.signif:
#     gr = main_scan['graph']
#     for i in xrange(gr.GetN()):
#         if abs(gr.GetX()[i] - 0.) < 1E-4:
#             print 'Found scan point at %s = %.6f' % (args.POI, gr.GetX()[i])
#             pt.SetY1(pt.GetY1() - 0.1)
#             pt.SetX1(0.52)
#             signif = ROOT.Math.normal_quantile_c(
#                 ROOT.Math.chisquared_cdf_c(gr.GetY()[i], 1) / 2., 1)
#             signif_x = gr.GetX()[i]
#             signif_y = gr.GetY()[i]
#             txt_cross = '[-2#DeltalnL @ %s = %.1f is %.3f]' % (
#                 fixed_name, gr.GetX()[i], gr.GetY()[i])
#             txt_signif = '[Significance = %.2f#sigma]' % (signif)
#             pt.AddText(txt_cross)
#             pt.AddText(txt_signif)
#             print '-2#DeltalnL @ %s = %.1f is %.3f]' % (fixed_name, 1., main_scan['func'].Eval(1.0))


# # pt.AddText(textfit)
# # if len(args) >= 4:
# #     syst_hi = math.sqrt(val_nom[1]*val_nom[1] - syst_scan['val'][1] * syst_scan['val'][1])
# #     syst_lo = math.sqrt(val_nom[2]*val_nom[2] - syst_scan['val'][2] * syst_scan['val'][2])
# # textfit = '%s = %.3f{}^{#plus %.3f}_{#minus %.3f} (stat.){}^{#plus %.3f}_{#minus %.3f} (syst.)' % (fixed_name, syst_scan['val'][0], abs(syst_scan['val'][1]), abs(syst_scan['val'][2]), syst_hi, syst_lo)
# #     pt.AddText(textfit)
# pt.SetTextAlign(11)
# pt.SetTextFont(42)
# if not args.no_numbers:
#     pt.Draw()


# if args.json is not None:
#     if os.path.isfile(args.json):
#         with open(args.json) as jsonfile:
#             js = json.load(jsonfile)
#     else:
#         js = {}
#     if not args.model in js:
#         js[args.model] = {}
#     js[args.model][args.POI] = {
#         'Val': val_nom[0],
#         'ErrorHi': val_nom[1],
#         'ErrorLo': val_nom[2],
#         'ValidErrorHi': main_scan['cross_1sig']['valid_hi'],
#         'ValidErrorLo': main_scan['cross_1sig']['valid_lo'],
#         '2sig_ErrorHi': val_2sig[1],
#         '2sig_ErrorLo': val_2sig[2],
#         '2sig_ValidErrorHi': main_scan['cross_2sig']['valid_hi'],
#         '2sig_ValidErrorLo': main_scan['cross_2sig']['valid_lo']
#     }
#     if signif is not None:
#         js[args.model][args.POI].update({
#             'Signif': signif,
#             'Signif_x': signif_x,
#             'Signif_y': signif_y
#         })
#     if args.breakdown is not None:
#         js[args.model][args.POI].update(breakdown_json)
#     if args.envelope is not None:
#         print main_scan['other_1sig']
#         print main_scan['other_2sig']
#         js_extra = {
#             'OtherLimitLo': 0.,
#             'OtherLimitHi': 0.,
#             '2sig_OtherLimitLo': 0.,
#             '2sig_OtherLimitHi': 0.,
#             'ValidOtherLimitLo': False,
#             'ValidOtherLimitHi': False,
#             '2sig_ValidOtherLimitLo': False,
#             '2sig_ValidOtherLimitHi': False
#         }
#         if len(main_scan['other_1sig']) >= 1:
#             other = main_scan['other_1sig'][0]
#             js_extra['OtherLimitLo'] = other['lo']
#             js_extra['OtherLimitHi'] = other['hi']
#             js_extra['ValidOtherLimitLo'] = other['valid_lo']
#             js_extra['ValidOtherLimitHi'] = other['valid_hi']
#         if len(main_scan['other_2sig']) >= 1:
#             other = main_scan['other_2sig'][0]
#             js_extra['2sig_OtherLimitLo'] = other['lo']
#             js_extra['2sig_OtherLimitHi'] = other['hi']
#             js_extra['2sig_ValidOtherLimitLo'] = other['valid_lo']
#             js_extra['2sig_ValidOtherLimitHi'] = other['valid_hi']
#         js[args.model][args.POI].update(js_extra)

#     with open(args.json, 'w') as outfile:
#         json.dump(js, outfile, sort_keys=True, indent=4, separators=(',', ': '))

# collab = 'Combined'
# if 'cms_' in args.output:
#     collab = 'CMS'
# if 'atlas_' in args.output:
#     collab = 'ATLAS'

# subtext = '{#it{LHC} #bf{Run 1 Internal}}'
# if args.pub:
#     subtext = '{#it{LHC} #bf{Run 1}}'
#     # subtext = '#it{#splitline{LHC Run 1}{Internal}}'
# plot.DrawCMSLogo(pads[0], '#splitline{#it{ATLAS}#bf{ and }#it{CMS}}'+subtext,
#                  '', 11, 0.045, 0.035, 1.2, '', 0.9 if args.pub else 0.8)
# # plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS',
# #                  '#it{LHC Run 1 Internal}', 11, 0.045, 0.035, 1.2)
# # plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1
# # Preliminary}', 11, 0.025, 0.035, 1.1, cmsTextSize = 1.)

# if args.POI_line is not None:
#     POIs = sorted(args.POI_line.split())
#     for i,P in enumerate(POIs):
#         if P in name_translate:
#             POIs[i] = name_translate[P]
#     POI_line = '['+ ','.join(POIs) + ']'

# if not args.no_input_label:
#     plot.DrawTitle(pads[0], '#bf{Input:} %s' % collab, 3)
# # legend_l = 0.70 if len(args) >= 4 else 0.73


# latex = ROOT.TLatex()
# latex.SetNDC()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)

# legend_l = 0.73
# if len(other_scans) > 0:
#     legend_l = legend_l - len(other_scans) * 0.04
# if args.legend_pos == 1:
#     legend = ROOT.TLegend(0.15, legend_l, 0.45, 0.78, '', 'NBNDC')
# elif args.legend_pos == 2:
#     legend = ROOT.TLegend(0.55, legend_l+0.075, 0.85, 0.78+0.075, '', 'NBNDC')
#     if args.POI_line is not None:
#         latex.DrawLatex(0.55, 0.875, POI_line)
# elif args.legend_pos == 3:
#     legend = ROOT.TLegend(0.15, legend_l-0.04, 0.45, 0.78-0.04, '', 'NBNDC')
# elif args.legend_pos == 4:
#     legend = ROOT.TLegend(0.50, legend_l+0.075, 0.80, 0.78+0.075, '', 'NBNDC')
#     if args.POI_line is not None:
#         latex.SetTextSize(0.035)
#         latex.DrawLatex(0.50, 0.875, POI_line)
# if len(other_scans) >= 3:
#     y_sub = 0. if args.POI_line is None else 0.07
#     if args.envelope:
#         legend = ROOT.TLegend(0.58, 0.79 - y_sub, 0.95, 0.93 - y_sub, '', 'NBNDC')
#         legend.SetNColumns(2)
#         if args.POI_line is not None:
#             latex.DrawLatex(0.58, 0.875, POI_line)
#     else:
#         legend = ROOT.TLegend(0.46, 0.83 - y_sub, 0.95, 0.93 - y_sub, '', 'NBNDC')
#         legend.SetNColumns(2)

# legend.AddEntry(main_scan['func'], args.main_label, 'L')
# if args.breakdown and args.envelope:
#     for i in xrange(n_env):
#         legend.AddEntry(new_others[i]['func'], other_scans_opts[i][1], 'L')
# else:
#     for i, other in enumerate(other_scans):
#         legend.AddEntry(other['func'], other_scans_opts[i][1], 'L')
# # if len(args) >= 4: legend.AddEntry(syst_scan['func'], 'Stat. Only', 'L')
# legend.Draw()

# save_graph = main_scan['graph'].Clone()
# save_graph.GetXaxis().SetTitle('%s = %.3f %+.3f/%+.3f' %
#                                (fixed_name, val_nom[0], val_nom[2], val_nom[1]))
# outfile = ROOT.TFile(args.output + '.root', 'RECREATE')
# outfile.WriteTObject(save_graph, 'main')
# for i, other in enumerate(other_scans):
#     save_graph = other['graph'].Clone()
#     if args.envelope:
#         min_val = plot.ImproveMinimum(save_graph, other['func'])
#         save_graph.Set(save_graph.GetN() + 1)
#         save_graph.SetPoint(save_graph.GetN() - 1, min_val[0], min_val[1])
#         save_graph.Sort()
#     save_graph.SetTitle(other_scans_opts[i][1])
#     outfile.WriteTObject(save_graph, other_scans_opts[i][0].replace('.root','').split('/')[-1])

# outfile.Close()
canv.Print('.pdf')
canv.Print('.png')

# meta = {}

# if args.meta != '':
#     meta_list = args.meta.split(',')
#     for m in meta_list:
#         meta_pair = m.split(':')
#         meta[meta_pair[0]] = meta_pair[1]
#     with open(args.output + '.json', 'w') as outmeta:
#         json.dump(
#             meta, outmeta, sort_keys=True, indent=4, separators=(',', ': '))

# canv.Print('.C')
