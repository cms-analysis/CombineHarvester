#!/usr/bin/env python

import ROOT
import json

import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.opts import OPTS

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase


class PrintSingles(CombineToolBase):
    description = 'Print the output of MultimDitFit --algo singles'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('input', help='The input file')
        group.add_argument(
            '-P', '--POIs', help='The params that were scanned (in scan order)')

    def run_method(self):
        POIs = args.POIs.split(',')
        res = get_singles_results(args.input, POIs, POIs)
        for p in POIs:
            val = res[p][p]
            print '%s = %.3f -%.3f/+%.3f' % (p, val[1], val[1] - val[0], val[2] - val[1])


class CollectLimits(CombineToolBase):
    description = 'Aggregate limit output from combine'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument(
            '-i', '--input', nargs='+', default=[], help='The input files')
        group.add_argument(
            '-o', '--output', help='The name of the output json file')

    def run_method(self):
        js_out = {}
        for filename in self.args.input:
            file = ROOT.TFile(filename)
            if file.IsZombie():
                continue
            tree = file.Get('limit')
            for evt in tree:
                mh = str(evt.mh)
                if mh not in js_out:
                    js_out[mh] = {}
                if evt.quantileExpected == -1:
                    js_out[mh]['observed'] = evt.limit
                elif abs(evt.quantileExpected - 0.5) < 1E-4:
                    js_out[mh]["expected"] = evt.limit
                elif abs(evt.quantileExpected - 0.025) < 1E-4:
                    js_out[mh]["-2"] = evt.limit
                elif abs(evt.quantileExpected - 0.160) < 1E-4:
                    js_out[mh]["-1"] = evt.limit
                elif abs(evt.quantileExpected - 0.840) < 1E-4:
                    js_out[mh]["+1"] = evt.limit
                elif abs(evt.quantileExpected - 0.975) < 1E-4:
                    js_out[mh]["+2"] = evt.limit
        # print js_out
        jsondata = json.dumps(
            js_out, sort_keys=True, indent=2, separators=(',', ': '))
        print jsondata
        if self.args.output is not None:
            with open(self.args.output, 'w') as out_file:
                out_file.write(jsondata)
