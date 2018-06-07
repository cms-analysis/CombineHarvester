#!/usr/bin/env python
# import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plotting
import json
import argparse
import os.path
import pprint

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)


# TODO: make the pad settings into options
plotting.ModTDRStyle(width=700, l=0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)

NAMECOUNTER = 0
NPX = 200


def Eval(obj, x, params):
    return obj.Eval(x[0])


def ParseDictArgs(str):
    return {x.split('=')[0]: eval(x.split('=')[1]) for x in str.split(',')}


class Scan:
    def __init__(self, graph, label=None, graph_settings=None, func_settings=None):
        # start by assuming the label is the name of the graph...
        self.label = graph.GetName()
        # unless the user overrides it.
        if label is not None:
            self.label = label
        self.gr = graph
        self.fn = None
        self.draw_graph = True
        self.draw_func = True
        self.graph_settings = {
            'MarkerSize': 0.7,
            'MarkerColor': 1,
            'Name': self.label  # set name to the current label value
        }
        self.func_settings = {
            'LineWidth': 2,
            'LineColor': 1
        }
        if graph_settings is not None:
            # 'Name' might get updated here
            self.graph_settings.update(graph_settings)
        if func_settings is not None:
            self.func_settings.update(func_settings)
        # # in case 'Name' changed, keep the label in sync
        # self.label =self.graph_settings['Name']

    def BuildSpline(self):
        global NAMECOUNTER
        spline = ROOT.TSpline3("spline3", self.gr)
        self.fn = ROOT.TF1('splinefn' + str(NAMECOUNTER),
                        partial(Eval, spline),
                        self.gr.GetX()[0],
                        self.gr.GetX()[self.gr.GetN() - 1], 1)
        self.fn.SetNpx(NPX)
        NAMECOUNTER += 1


class ScanTool:

    def __init__(self):
        self.verbosity = 0
        self.fn_points = 200

    def attach_job_args(self, group):
        parser.add_argument('--fn-points', default=self.fn_points, type=int,
                            help='Number of points to use in function objects')

    def ReadScanFromTFiles(self, filenames, param_name, tree_selection='quantileExpected > -1.5'):
        # TODO: should report bad files here
        goodfiles = [f for f in filenames if plotting.TFileIsGood(f)]
        if len(goodfiles) == 0:
            raise RuntimeError('[ReadScanFromTFiles] no valid TFiles')
        limit = plotting.MakeTChain(goodfiles, 'limit')
        graph = plotting.TGraphFromTree(
            limit, param_name, '2*deltaNLL', tree_selection)
        # graph.SetName(label)
        graph.Sort()
        if self.verbosity >= 2:
            print '[ReadScanFromTFiles] Produced TGraph:'
            graph.Print()
        return graph

    def FilterDuplicates(self, graph, unique_x=True):
        frequencies = {}
        to_delete = []
        for i in xrange(graph.GetN() - 1):
            x = graph.GetX()[i]
            y = graph.GetY()[i]
            if x not in frequencies:
                frequencies[x] = {}
            if y not in frequencies[x]:
                frequencies[x][y] = 0
            frequencies[x][y] += 1
            if frequencies[x][y] >= 2:
                to_delete.append(i)
        for i in sorted(to_delete, reverse=True):
            graph.RemovePoint(i)
        return

    def RemoveNearMin(self, graph, val, spacing=None):
        # assume graph is sorted:
        n = graph.GetN()
        if n < 5:
            return
        if spacing is None:
            spacing = (graph.GetX()[n - 1] - graph.GetX()[0]) / float(n - 2)
            # print '[RemoveNearMin] Graph has spacing of %.3f' % spacing
        bf_i = None
        for i in xrange(graph.GetN()):
            if graph.GetY()[i] == 0.:
                bf = graph.GetX()[i]
                bf_i = i
                # print '[RemoveNearMin] Found best-fit at %.3f' % bf
                break
        if bf_i is None:
            print '[RemoveNearMin] No minimum found!'
            return
        for i in xrange(graph.GetN()):
            if i == bf_i:
                continue
            if abs(graph.GetX()[i] - bf) < (val * spacing):
                print '[RemoveNearMin] Removing point (%f, %f) close to minimum at %f' % (graph.GetX()[i], graph.GetY()[i], bf)
                graph.RemovePoint(i)
                self.RemoveNearMin(graph, val, spacing)
                break

    def FindGlobalBestFit(self, graph):
        for i in xrange(graph.GetN()):
            if graph.GetY()[i] == 0.:
                return (i, graph.GetX()[i], graph.GetY()[i])
        return (-1, 0., 0.)

    def ImproveMinimum(self, graph, func, doIt=False, adjustY=False, xMin=None, xMax=None):
        fit_x = 0.
        fit_y = 99999.
        fit_i = -1
        for i in xrange(graph.GetN()):
            if xMin is not None and graph.GetX()[i] < xMin:
                continue
            if xMax is not None and graph.GetX()[i] > xMax:
                continue
            if graph.GetY()[i] < fit_y:
                fit_i = i
                fit_x = graph.GetX()[i]
                fit_y = graph.GetY()[i]
        if fit_i == 0 or fit_i == (graph.GetN() - 1):
            if doIt:
                min_x = graph.GetX()[fit_i]
                min_y = graph.GetY()[fit_i]
                if adjustY:
                    for i in xrange(graph.GetN()):
                        before = graph.GetY()[i]
                        graph.GetY()[i] -= min_y
                        after = graph.GetY()[i]
                        print 'Point %i, before=%f, after=%f' % (i, before, after)
            return (fit_x, fit_y)
        # Decide the region to search in
        # If fit_i is still -1, then we didn't find a single point in the [xMin, xMax] range
        if fit_i == -1 and xMin is not None and xMax is not None:
            search_min = xMin
            search_max = xMax
        elif fit_i >= 0:
            iMin = fit_i - 2 if fit_i >= 2 else fit_i - 1
            iMax = fit_i + 2 if fit_i + 2 < graph.GetN() else fit_i + 1
            search_min = graph.GetX()[iMin]
            search_max = graph.GetX()[iMax]
        min_x = func.GetMinimumX(search_min, search_max)
        min_y = func.Eval(min_x)
        print '[ImproveMinimum] Fit minimum was (%f, %f)' % (fit_x, fit_y)
        print '[ImproveMinimum] Better minimum was (%f, %f)' % (min_x, min_y)
        if doIt:
            if adjustY:
                for i in xrange(graph.GetN()):
                    before = graph.GetY()[i]
                    graph.GetY()[i] -= min_y
                    after = graph.GetY()[i]
                    print 'Point %i, before=%f, after=%f' % (i, before, after)
            graph.Set(graph.GetN() + 1)
            graph.SetPoint(graph.GetN() - 1, min_x, 0 if adjustY else min_y)
            graph.Sort()
        return (min_x, min_y)


    def AddMinima(self, scan_info, scan, use_interval="1sig"):
        intervals = scan_info["Intervals"][use_interval]
        global_fit = self.FindGlobalBestFit(scan.gr)
        for interval in intervals:
            interval['IsGlobalMin'] = False
            if global_fit[0] >= 0 and global_fit[1] >= interval['Lo'] and global_fit[1] <= interval['Hi']:
                # This interval contains the global best-fit
                interval['Min'] = global_fit[1]
                interval['IsGlobalMin'] = True
            else:
                min_point = self.ImproveMinimum(scan.gr, scan.fn, xMin=interval['Lo'], xMax=interval['Hi'])
                interval['Min'] = min_point[0]


    def FindIntervalContainingBF(self, interval_list, best_fit_val):
        for interval in interval_list:
            if interval["Lo"] <= best_fit_val and interval["Hi"] >= best_fit_val:
                return interval
        return None


    def AddUnc(self, scan_dict, use_interval="1sig", label="Unc"):
        scan_dict[label] = {}
        intervals = scan_dict["Intervals"][use_interval]
        bf_interval = self.FindIntervalContainingBF(intervals, scan_dict["Val"])
        if use_interval not in scan_dict[label]:
            scan_dict[label][use_interval] = {}
        scan_dict[label][use_interval]["ErrorHi"] = bf_interval["Hi"] - scan_dict["Val"]
        scan_dict[label][use_interval]["ErrorLo"] = bf_interval["Lo"] - scan_dict["Val"]

    # ['Nominal', 'FR.sigTheory' 'FR.all']   ['SigTh', 'Expt.', 'Stat.']
    #                                           nom^2 - fr.sig^2, fr.sig^2 - fr.all^2   fr.all^2
    # Requries this scan has "Val" present

    # Basic logic:
    # scan_labels[0] - this is the total scan, and therefore special.
    # I will loop through each interval in this scan:
    #    I will find


    def AddUncs(self, info, scan_labels, brk_labels, use_interval="1sig", label="Unc"):
        intervals = info[scan_labels[0]]['Intervals'][use_interval]
        print '>> [AddUncs] Found %i interval(s) at level "%s" in scan "%s"' % (len(intervals), use_interval, scan_labels[0])
        for interval in intervals:
            breakdown_intervals = [interval]
            min_x = interval['Min']
            lo = interval['Lo']
            hi = interval['Hi']
            print '>> [AddUncs] -- interval [%f, %f] with minimum = %f' % (lo, hi, min_x)
            for scan_label in scan_labels[1:]:
                for oth_interval in info[scan_label]['Intervals'][use_interval]:
                    if min_x >= oth_interval['Lo'] and min_x <= oth_interval['Hi']:
                        breakdown_intervals.append(oth_interval)
            print '>> [AddUncs] -- found %i/%i intervals for the breakdown' % (len(breakdown_intervals), len(scan_labels))

        # for e in ['Hi', 'Lo']:
        #     tot = scan_dict[label][use_interval]['Error%s' % e]
        #     tot2 = tot * tot
        #     for i, scan_label, breakdown_label in enumerate(zip(scan_labels, brk_labels)):
        #         bf_interval = self.FindIntervalContainingBF(scan_dict[scan_label]["Intervals"][use_interval], scan_dict["Val"])
        #         brk = bf_interval[e] - scan_dict["Val"]
        #         brk2 = brk * brk
        #         if tot2 >= brk2:
        #             unc = math.sqrt(tot2 - brk2)
        #         else:
        #             unc = 0.0
        #         scan_dict['Unc'][use_interval]['%s%s' % (breakdown_label, e)]

    def BuildValuesBox(self, box, scans, info, use_crossing='1sig'):
        for scan in scans:
            label = scan.label
            box.AddText('#color[%s]{%s = %.3f{}^{#plus %.3f}_{#minus %.3f}}' % (
                scan.func_settings['LineColor'], 'r',
                info[label]['Val'],
                abs(info[label]['Unc'][use_crossing]['ErrorHi']),
                abs(info[label]['Unc'][use_crossing]['ErrorLo'])))

    def RemoveGraphYAll(self, graph, val):
        for i in xrange(graph.GetN()):
            if graph.GetY()[i] == val:
                print '[RemoveGraphYAll] Removing point (%f, %f)' % (graph.GetX()[i], graph.GetY()[i])
                graph.RemovePoint(i)
                self.RemoveGraphYAll(graph, val)
                break

    def BuildEnvelope(self, scans):
        print '[ProcessEnvelope] Will create envelope from %i scans' % len(scans)
        min_x = min([sc.gr.GetX()[0] for sc in scans])
        max_x = max([sc.gr.GetX()[sc.gr.GetN() - 1] for sc in scans])
        print '(min_x,max_x) = (%f, %f)' % (min_x, max_x)
        npoints = 200
        step = (max_x - min_x) / float(npoints - 1)
        x = min_x
        xvals = []
        yvals = []
        # for oth in others:
        #     oth['graph'].Print()
        for i in xrange(npoints):
            yset = []
            for sc in scans:
                gr = sc.gr
                if x >= gr.GetX()[0] and x <= (gr.GetX()[gr.GetN() - 1] + 1E-6):
                    yset.append(sc.fn.Eval(x))
            # print 'At x=%f, possible y vals are %s' % (x, yset)
            if len(yset) > 0:
                xvals.append(x)
                yvals.append(min(yset))
            x = x + step

        gr = ROOT.TGraph()
        gr.Set(len(xvals))  # will not contain the best fit
        for i in xrange(gr.GetN()):
            gr.SetPoint(i, xvals[i], yvals[i])

        # print 'Envelope'
        gr.Print()

        # spline = ROOT.TSpline3("spline3", gr)
        # global NAMECOUNTER
        # func = ROOT.TF1('splinefn' + str(NAMECOUNTER), partial(Eval, spline),
        #                 gr.GetX()[0], gr.GetX()[gr.GetN() - 1], 1)
        # func.SetNpx(NPX)
        # min_x, min_y = plot.ImproveMinimum(gr, func)
        # gr.Set(len(xvals) + 1)
        # gr.SetPoint(len(xvals), min_x, min_y)
        # gr.Sort()

        # for i in xrange(gr.GetN()):
        #     gr.GetY()[i] -= min_y
        # for oth in others:
        #     for i in xrange(oth['graph'].GetN()):
        #         oth['graph'].GetY()[i] -= min_y
        #     # print 'OTHER'
        #     # oth['graph'].Print()

        # plot.RemoveGraphXDuplicates(gr)
        return gr




parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', nargs='*',
                    help='Add scans FILE:LABEL:COLOR')
parser.add_argument('--var', default='r',
                    help='Variable name')
parser.add_argument('--output', default='test',
                    help='Variable name')
parser.add_argument('--values-box', default='0.59,0.82,0.95,0.91',
                    help='Position and size of the box containing best-fit values')
parser.add_argument('--crossings', default='1sig=1.0,2sig=4.0',
                    help='Labels and values for the 2deltaNLL crossings of interest')
# parser.add_argument('--type', default='default', choices=['default', 'breakdown', 'envelope', 'breakdown+envelope'],
#                     help='Type of scan plot to make')
parser.add_argument('--envelope', nargs='*', default=None,
                    help='Define envelope scans E1:N1,N2:SETTINGS')
parser.add_argument('--breakdown', nargs='*', default=None,
                    help='Define breakdown calculations via quadratic subraction: NOMINAL,FR_TH,FR_ALL:"Sig Th","Exp.","Stat."')
parser.add_argument('--fn-points', default=200, type=int,
                    help='Number of points to use in function objects')
parser.add_argument('--y-max', type=float, default=8., help='max y to draw')
parser.add_argument('--box-frac', default=0.625, type=float, help='fraction of the pad occupied by box')
parser.add_argument('--chop', type=float, default=7., help='remove vals above')


args = parser.parse_args()

scanner = ScanTool()
scanner.verbosity = 2


info = {}

"""
INPUT="Comb_Jan31"; M=K2Inv; for W in prefit_asimov; do case ${W} in *_asimov) EXTRA='--main-label "SM Expected" \
--main-color 4';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); \
 do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} \
 --others \
 \"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\"  \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0:40\"  \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --envelope \
--chop 15 --translate pois.json --json neg_${W}.json  --hide-envelope --meta "Types:${W},POIs:${P}"; done; done


E1:N1,N4

--pre-process N1fr,N1frS:ShiftMinTo:N1


"""

# Types:
    # Default
    # Breakdown
    # Envelope
    # Breakdown+Envelope

# Do all the stuff that doesn't depend on which plot type we're making

canv = ROOT.TCanvas(args.output, args.output)
pads = plotting.OnePad()

scans = []

# Define the NLL crossings of interest
crossing_labels = [x.split('=')[0] for x in args.crossings.split(',')]
crossings_vals = [float(x.split('=')[1]) for x in args.crossings.split(',')]

for i, iargs in enumerate(args.input):
    splitargs = iargs.split(':')

    scans.append(Scan(
        scanner.ReadScanFromTFiles([splitargs[1]], args.var),
        label=splitargs[0]
        ))
    scan = scans[-1]

    if len(splitargs) > 2:
        scan.graph_settings.update(ParseDictArgs(splitargs[2]))
    if len(splitargs) > 3:
        scan.func_settings.update(ParseDictArgs(splitargs[3]))
    label = scan.label
    info[label] = {}
    scan_info = info[label]


    # THEN DO SOME PROCESSING OF THE GRAPH

    # STANDARD PROCESSING
    #   1. Remove (x, y) duplicates
    scanner.FilterDuplicates(scan.gr)
    #   2. Remove near the minimum (0.8)
    scanner.RemoveNearMin(scan.gr, 0.8)
    #   3. Remove y points above some cutoff (mostly cosmetic - should come later because envelope processing will change things)
    plotting.RemoveGraphYAbove(scan.gr, args.chop)
    # TOOD: what if there is a scan point with deltaNLL < 0.0

    scan.gr.Print()

    bestfit = scanner.FindGlobalBestFit(scan.gr)
    scan_info['Val'] = bestfit[1]
    scan.BuildSpline()
    # scanner.ImproveMinimum(scan.gr, scan.fn)




# PROCESS ENVELOPE
#   1. Remove (x, y) duplicates (previously didn't remove duplicates,
#      but was only checking x duplicates before). Guess was worried about
#      removing a legit point with deltaNLL > 0 at the same x as the minimum
#   2. Remove the minimum
#   3. Run the enveloping procedure
#   4. Run ImproveMinimum -> then add the extra point it produces
#   5. Remove X duplicates, because conceivably Improve will find the same
#      point as one that's already there.
if args.envelope is not None:
    for i, iargs in enumerate(args.envelope):
        splitargs = iargs.split(':')
        envelope_label = splitargs[0]
        input_scan_labels = splitargs[1].split(',')
        envelope_scans = []
        for lab in input_scan_labels:
            for sc in scans:
                if sc.label == lab:
                    envelope_scans.append(sc)
        for sc in envelope_scans:
            scanner.RemoveGraphYAll(sc.gr, 0.0)
            sc.BuildSpline()
            scanner.ImproveMinimum(sc.gr, sc.fn, doIt=True)
            sc.BuildSpline()
            # Now need to rebuild the spline
        scans.append(Scan(
            scanner.BuildEnvelope(envelope_scans),
            label=splitargs[0]
            ))
        scan = scans[-1]
        scan.BuildSpline()
        if len(splitargs) > 2:
            scan.graph_settings.update(ParseDictArgs(splitargs[2]))
        if len(splitargs) > 3:
            scan.func_settings.update(ParseDictArgs(splitargs[3]))



# Inject info about NLL crossings
for i, scan in enumerate(scans):
    # print 'Found %i envelope scans' % len(envelope_scans)
    ## Info extraction should come later, and be customisable
    scan_info = {}
    scan_info["Intervals"] = {}
    for j, crossing in enumerate(crossings_vals):
        scan_info["Intervals"][crossing_labels[j]] = []
        intervals = plotting.FindCrossingsWithSpline(scan.gr, scan.fn, crossing)
        for interval in intervals:
            sub_info = scan_info["Intervals"][crossing_labels[j]].append({
                "Lo": interval['lo'],
                "Hi": interval['hi'],
                "ValidLo": interval['valid_lo'],
                "ValidHi": interval['valid_hi'],
                })
        info[scan.label].update(scan_info)
    scanner.AddMinima(scan_info=info[scan.label], scan=scan)
    scanner.AddUnc(info[scan.label])

scanner.AddUncs(info, ['nominal'], ['Error'])
scanner.AddUncs(info, ['nominal', 'fr_all'], ['Syst', 'Stat'])
pprint.pprint(info)




for i, scan in enumerate(scans):
    plotting.Set(scan.gr, **scan.graph_settings)
    plotting.Set(scan.fn, **scan.func_settings)
    if i == 0:
        scan.gr.Draw('AP')
        axishist = plotting.GetAxisHist(pads[0])
        axishist.SetMaximum(args.y_max)
        axishist.GetYaxis().SetTitle("#minus2 ln #Lambda")
        axishist.GetXaxis().SetTitle("x")

        for crossing in crossings_vals:
            line = ROOT.TLine()
            line.SetLineColor(ROOT.kRed)
            plotting.DrawHorizontalLine(pads[0], line, crossing)

    scan.gr.Draw('PSAME')
    scan.fn.Draw('SAME')


## Draw a white box in the top of the pad
box = ROOT.TBox(axishist.GetXaxis().GetXmin(), args.box_frac *
                args.y_max, axishist.GetXaxis().GetXmax(), args.y_max)
box.Draw()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()


## Draw the box containing the best fit values
draw_values_box = True
if draw_values_box:
    # box_args = [float(x) for x in args.values_box]
    values_box = ROOT.TPaveText(*([float(x) for x in args.values_box.split(',')]+['NDCNB']))
    scanner.BuildValuesBox(values_box, scans, info)
    values_box.Draw()

pprint.pprint(info)

canv.Print('.pdf')
canv.Print('.png')


    # PROCESS ENVELOPE + BREAKDOWN
    # Current problem is when doing the envelope for the frozen scans:
    #  x[6]=0.95, y[6]=0.237087
    #  x[7]=1, y[7]=-0.000580226
    #  x[8]=1.00005, y[8]=-0.000248406
    #  x[9]=1.05, y[9]=0.21612
    # This screws up the spline interpolation. So why didn't one of these points get cleaned?
    #  - there's no remove near min, as well as no removal of the minimum.
    # How to solve


    # Information extraction
    # - intervals / best-fit given crossings
"""
        "Val": the global best-fit, # where deltaNLL = 0
        "Unc": {
            "ErrorLo": -1,
            "ErrorHi": +1,
            "StatLo": -1,
            "StatHi": +1,
            "ValidErrorHi": true,
            "ValidErrorLo": true
        },
        "Intervals": {
            "DNLL0.5": [
                {
                    "FullLo": -1.5,
                    "FullHi": -0.5,
                    "StatLo": -1.4,
                    "StatHi": -0.4
                },
            ]
        },
        "LocalMinima": [
            -1.0,
            -0.5
        ],


"""
    # - upper limit
    # - significance (wrt what?)
    # - uncertainty breakdown











    # Removing duplicates is usually always done. Exception is if we're processing the envelope
