#!/usr/bin/env python

import ROOT
import json
import os
import pprint
import numpy as np
from collections import defaultdict

import CombineHarvester.CombineTools.combine.utils as utils
import CombineHarvester.CombineTools.plotting as plot
# from CombineHarvester.CombineTools.combine.opts import OPTS

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class PrintFit(CombineToolBase):
    description = 'Print the output of MultimDitFit'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('input', help='The input file')
        group.add_argument(
            '--algo', help='The algo used in MultiDimFit', default='none')
        group.add_argument(
            '-P', '--POIs', help='The params that were scanned (in scan order)')
        group.add_argument(
            '--json', help='Write json output (format file.json:key1:key2..')

    def run_method(self):
        if self.args.json is not None:
            json_structure = self.args.json.split(':')
            assert(len(json_structure) >= 1)
            if os.path.isfile(json_structure[0]):
                with open(json_structure[0]) as jsonfile: js = json.load(jsonfile)
            else:
                js = {}
            js_target = js
            if (len(json_structure) >= 2):
                for key in json_structure[1:]:
                    js_target[key] = {}
                    js_target = js_target[key]
        POIs = self.args.POIs.split(',')
        if self.args.algo == 'none':
            res = utils.get_none_results(self.args.input, POIs)
            if self.args.json is not None:
              for key,val in res.iteritems():
                js_target[key] = { 'Val' : val }
            with open(json_structure[0], 'w') as outfile:
              json.dump(js, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        elif self.args.algo == 'singles':
            res = utils.get_singles_results(self.args.input, POIs, POIs)
            for p in POIs:
                val = res[p][p]
                print '%s = %.3f -%.3f/+%.3f' % (p, val[1], val[1] - val[0], val[2] - val[1])


class CollectLimits(CombineToolBase):
    description = 'Aggregate limit output from combine'
    requires_root = True
    default_name='limits.json'

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument(
            'input', nargs='+', default=[], help='The input files')
        group.add_argument(
            '-o', '--output', nargs='?', const='limits.json',
            default='limits.json', help="""The name of the output json file.
            When the --use-dirs option is set the enclosing directory name
            will be appended to the filename given here.""")
        group.add_argument(
            '--use-dirs', action='store_true',
            help="""Use the directory structure to create multiple limit
                 outputs and to set the output file names""")

    def run_method(self):
        limit_sets = defaultdict(list)
        for filename in self.args.input:
            if not plot.TFileIsGood(filename):
                print '>> File %s is corrupt or incomplete, skipping' % filename
            if self.args.use_dirs is False:
                limit_sets['default'].append(filename)
            else:
                label = 'default'
                dirs = filename.split('/')
                # The last dir could be the mass, if so we ignore it and check the next
                if len(dirs) > 1:
                    if not isfloat(dirs[-2]):
                        label = dirs[-2]
                    elif len(dirs) > 2:
                        label = dirs[-3]
                limit_sets[label].append(filename)
        # print limit_sets

        for label, filenames in limit_sets.iteritems():
            js_out = {}
            for filename in filenames:
                file = ROOT.TFile(filename)
                tree = file.Get('limit')
                for evt in tree:
                    mh = str(evt.mh)
                    if mh not in js_out:
                        js_out[mh] = {}
                    if evt.quantileExpected == -1:
                        js_out[mh]['obs'] = evt.limit
                    elif abs(evt.quantileExpected - 0.5) < 1E-4:
                        js_out[mh]["exp0"] = evt.limit
                    elif abs(evt.quantileExpected - 0.025) < 1E-4:
                        js_out[mh]["exp-2"] = evt.limit
                    elif abs(evt.quantileExpected - 0.160) < 1E-4:
                        js_out[mh]["exp-1"] = evt.limit
                    elif abs(evt.quantileExpected - 0.840) < 1E-4:
                        js_out[mh]["exp+1"] = evt.limit
                    elif abs(evt.quantileExpected - 0.975) < 1E-4:
                        js_out[mh]["exp+2"] = evt.limit
            # print js_out
            jsondata = json.dumps(
                js_out, sort_keys=True, indent=2, separators=(',', ': '))
            # print jsondata
            if self.args.output is not None:
                outname = self.args.output.replace('.json', '_%s.json' % label) if self.args.use_dirs else self.args.output
                with open(outname, 'w') as out_file:
                    print '>> Writing output %s from files:' % outname
                    pprint.pprint(filenames, indent=2)
                    out_file.write(jsondata)

class CollectGoodnessOfFit(CombineToolBase):
    description = 'Aggregate Goodness of Fit output from fit and toys'
    requires_root = True
    default_name = 'gof.json'

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('--input', nargs='+', default=[], help='The input files')
        group.add_argument('--input-toys', nargs='+', default=[], help='The toy input files')
        group.add_argument(
            '-o', '--output', nargs='?', const='gof.json',
            default='gof.json', help="""The name of the output json file.
            When the --use-dirs option is set the enclosing directory name
            will be appended to the filename given here.""")
        group.add_argument(
            '--use-dirs', action='store_true',
            help="""Use the directory structure to create multiple limit
                 outputs and to set the output file names""")

    def run_method(self):
        limit_sets = defaultdict(list)
        for filename in self.args.input:
            if not plot.TFileIsGood(filename):
                print '>> File %s is corrupt or incomplete, skipping' % filename
            if not self.args.use_dirs:
                if 'default' not in limit_sets:
                    limit_sets['default'] = ([],[])
                limit_sets['default'][0].append(filename)
            else:
                label = 'default'
                dirs = filename.split('/')
                # The last dir could be the mass, if so we ignore it and check the next
                if len(dirs) > 1:
                    if not isfloat(dirs[-2]):
                        label = dirs[-2]
                    elif len(dirs) > 2:
                        label = dirs[-3]
                if label not in limit_sets:
                    limit_sets[label] = ([],[])
                limit_sets[label][0].append(filename)
        for filename in self.args.input_toys:
            if not plot.TFileIsGood(filename):
                print '>> File %s is corrupt or incomplete, skipping' % filename
            if not self.args.use_dirs:
                limit_sets['default'][1].append(filename)
            else:
                label = 'default'
                dirs = filename.split('/')
                # The last dir could be the mass, if so we ignore it and check the next
                if len(dirs) > 1:
                    if not isfloat(dirs[-2]):
                        label = dirs[-2]
                    elif len(dirs) > 2:
                        label = dirs[-3]
                limit_sets[label][1].append(filename)
        # print limit_sets

        for label, (filenames, toyfiles) in limit_sets.iteritems():
            js_out = {}
            for filename in filenames:
                file = ROOT.TFile(filename)
                tree = file.Get('limit')
                for evt in tree:
                    branches = []
                    for branch in list(tree.GetListOfBranches()):
                        if all([sub in branch.GetName() for sub in ["htt","13TeV"]]) and any([sub in branch.GetName() for sub in ["et","mt","tt","em"]]):
                            branches.append(branch.GetName())
                    mh = str(evt.mh)
                    if mh not in js_out:
                        js_out[mh] = {}
                    if evt.quantileExpected == -1:
                        if branches:
                            for branch in branches:
                                if branch not in js_out[mh]:
                                    js_out[mh][branch] = {}
                                js_out[mh][branch]['obs'] = [getattr(evt,branch)]
                        else:
                            js_out[mh]['obs'] = [evt.limit]
            for filename in toyfiles:
                file = ROOT.TFile(filename)
                tree = file.Get('limit')
                for evt in tree:
                    branches = []
                    for branch in list(tree.GetListOfBranches()):
                        if all([sub in branch.GetName() for sub in ["htt","13TeV"]]) and any([sub in branch.GetName() for sub in ["et","mt","tt","em"]]):
                            branches.append(branch.GetName())
                    mh = str(evt.mh)
                    if mh not in js_out:
                        js_out[mh] = {}
                    if evt.quantileExpected == -1:
                        if branches:
                            for branch in branches:
                                if branch not in js_out[mh]:
                                    js_out[mh][branch] = {}
                                if 'toy' not in js_out[mh][branch]:
                                    js_out[mh][branch]['toy'] = []
                                js_out[mh][branch]['toy'].append(getattr(evt,branch))
                        else:
                            if 'toy' not in js_out[mh]:
                                js_out[mh]['toy'] = []
                            js_out[mh]['toy'].append(evt.limit)
            for mh in js_out:
                if all([entry in js_out[mh] for entry in ['toy','obs']]):
                    js_out[mh]["p"] = float(len([toy for toy in js_out[mh]['toy'] if toy >= js_out[mh]['obs'][0]]))/len(js_out[mh]['toy'])
                else:
                    for branch in js_out[mh]:
                        js_out[mh][branch]["p"] = float(len([toy for toy in js_out[mh][branch]['toy'] if toy >= js_out[mh][branch]['obs'][0]]))/len(js_out[mh][branch]['toy'])

            # print js_out
            jsondata = json.dumps(
                js_out, sort_keys=True, indent=2, separators=(',', ': '))
            # print jsondata
            if self.args.output is not None:
                outname = self.args.output.replace('.json', '_%s.json' % label) if self.args.use_dirs else self.args.output
                with open(outname, 'w') as out_file:
                    print '>> Writing output %s from files:' % outname
                    pprint.pprint(filenames, indent=2)
                    out_file.write(jsondata)

class CollectToyLimits(CombineToolBase):
    description = 'Aggregate limit output from combine output for toys'
    requires_root = True
    default_name='limits.json'

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument(
            'input', nargs='+', default=[], help='The input files')
        group.add_argument(
            '--obs-input', nargs='+', default=[], help='The input files for the observation')
        group.add_argument(
            '-o', '--output', nargs='?', const='limits.json',
            default='limits.json', help="""The name of the output json file.
            When the --use-dirs option is set the enclosing directory name
            will be appended to the filename given here.""")
        group.add_argument(
            '--use-dirs', action='store_true',
            help="""Use the directory structure to create multiple limit
                 outputs and to set the output file names""")

    def run_method(self):
        limit_sets = defaultdict(list)
        obs_limit_sets = defaultdict(list)
        for filename in self.args.input:
            if not plot.TFileIsGood(filename):
                print '>> File %s is corrupt or incomplete, skipping' % filename
                continue
            if self.args.use_dirs is False:
                limit_sets['default'].append(filename)
            else:
                label = 'default'
                dirs = filename.split('/')
                # The last dir could be the mass, if so we ignore it and check the next
                if len(dirs) > 1:
                    if not isfloat(dirs[-2]):
                        label = dirs[-2]
                    elif len(dirs) > 2:
                        label = dirs[-3]
                limit_sets[label].append(filename)
        for filename in self.args.obs_input:
            if not plot.TFileIsGood(filename):
                print '>> File %s is corrupt or incomplete, skipping' % filename
                continue
            if self.args.use_dirs is False:
                obs_limit_sets['default'].append(filename)
            else:
                label = 'default'
                dirs = filename.split('/')
                # The last dir could be the mass, if so we ignore it and check the next
                if len(dirs) > 1:
                    if not isfloat(dirs[-2]):
                        label = dirs[-2]
                    elif len(dirs) > 2:
                        label = dirs[-3]
                obs_limit_sets[label].append(filename)

        for label, filenames in limit_sets.iteritems():
            js_toys = {}
            js_out = {}
            # first take case of the observed limit
            for filename in obs_limit_sets[label]:
                file = ROOT.TFile(filename)
                tree = file.Get('limit')
                for evt in tree:
                    mh = str(evt.mh)
                    if mh not in js_out:
                        js_out[mh] = {}
                    if evt.quantileExpected == -1:
                        js_out[mh]['obs'] = evt.limit
            # no go thorugh the files with the toys for the expected limits and save the results as lists
            for filename in filenames:
                file = ROOT.TFile(filename)
                tree = file.Get('limit')
                for evt in tree:
                    mh = str(evt.mh)
                    if mh not in js_toys:
                        js_toys[mh] = []
                    if evt.quantileExpected == -1:
                        js_toys[mh].append(evt.limit)
            # in the final step go thorugh the generated toys and extract the mean,+-1 and +-2 sigma values
            for mh in js_toys:
                if mh not in js_out:
                    js_out[mh] = {}
                js_out[mh]["exp0"] = np.percentile(np.array(js_toys[mh]),50)
                js_out[mh]["exp-2"] = np.percentile(np.array(js_toys[mh]),2.5)
                js_out[mh]["exp-1"] = np.percentile(np.array(js_toys[mh]),16)
                js_out[mh]["exp+1"] = np.percentile(np.array(js_toys[mh]),84)
                js_out[mh]["exp+2"] = np.percentile(np.array(js_toys[mh]),97.5)
            jsondata = json.dumps(
                js_out, sort_keys=True, indent=2, separators=(',', ': '))
            # print jsondata
            if self.args.output is not None:
                outname = self.args.output.replace('.json', '_%s.json' % label) if self.args.use_dirs else self.args.output
                with open(outname, 'w') as out_file:
                    print '>> Writing output %s from files:' % outname
                    pprint.pprint(filenames, indent=2)
                    out_file.write(jsondata)
