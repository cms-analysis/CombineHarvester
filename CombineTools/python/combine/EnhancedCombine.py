import itertools
import CombineHarvester.CombineTools.combine.utils as utils
import json
import os
from CombineHarvester.CombineTools.combine.opts import OPTS
from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class EnhancedCombine(CombineToolBase):
    description = 'combine pass-through with special treatment for some options [DEFAULT]'
    requires_root = False

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument(
            '-m', '--mass', help='Supports range strings for multiple masses, e.g. "120:130:5,140 will produce three combine calls with mass values of 120, 125, 130 and 140"')
        group.add_argument(
            '--points', help='For use with "-M MultiDimFit --algo grid" to split scan points into separate jobs')
        group.add_argument(
            '--singlePoint', help='Supports range strings for multiple points to test, uses the same format as the --mass argument')
        group.add_argument(
            '-s', '--seed', help='Supports range strings for multiple RNG seeds, uses the same format as the --mass argument')
        group.add_argument(
            '-d', '--datacard', nargs='*', default=[], help='Operate on multiple datacards')
        group.add_argument(
            '--boundlist', help='Name of json-file which contains the ranges of physical parameters depending on the given mass and given physics model')
        group.add_argument('--name', '-n', default='.Test',
                           help='Name used to label the combine output file, can be modified by other options')

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument(
            '--opts', nargs='+', default=[], help='Add preset combine option groups')
        group.add_argument(
            '--there', action='store_true', help='Run combine in the same directory as the workspace')
        group.add_argument('--split-points', type=int, default=0,
                           help='When used in conjunction with --points will create multiple combine calls that each run at most the number of points specified here.')

    def set_args(self, known, unknown):
        CombineToolBase.set_args(self, known, unknown)
        if hasattr(self.args, 'opts'):
            for opt in self.args.opts:
                self.passthru.append(OPTS[opt])

    def run_method(self):
        # Put the method back in because we always take it out
        self.put_back_arg('method', '-M')

        # cmd_queue = []
        subbed_vars = {}

        # pre_cmd = ''

        if self.args.mass is not None:
            mass_vals = utils.split_vals(self.args.mass)
            subbed_vars[('MASS',)] = [(mval,) for mval in mass_vals]
            self.passthru.extend(['-m', '%(MASS)s'])

        if self.args.singlePoint is not None:
            single_points = utils.split_vals(self.args.singlePoint)
            subbed_vars[('SINGLEPOINT',)] = [(pval,) for pval in single_points]
            self.passthru.extend(['--singlePoint', '%(SINGLEPOINT)s'])
            self.args.name += '.POINT.%(SINGLEPOINT)s'

        if self.args.seed is not None:
            seed_vals = utils.split_vals(self.args.seed)
            subbed_vars[('SEED',)] = [(sval,) for sval in seed_vals]
            self.passthru.extend(['-s', '%(SEED)s'])

        if len(self.args.datacard) >= 1:
            # Two lists of tuples, one which does specify the mass, and one
            # which doesn't
            dc_mass = []
            dc_no_mass = []
            for dc in self.args.datacard:
                # Split workspace into path and filename
                path, file = os.path.split(dc)
                # If the wsp is in the current directory should call it '.'
                if path == '':
                    path = '.'
                # If we're not using the --there option then leave the
                # workspace argument as the full path
                if not self.args.there:
                    file = dc
                # Figure out if the enclosing directory is a mass value
                dirs = path.split('/')
                if self.args.mass is None and len(dirs) >= 1 and isfloat(dirs[-1]):
                    print 'Assuming card %s uses mass value %s' % (dc, dirs[-1])
                    dc_mass.append((path, file, dirs[-1]))
                dc_no_mass.append((path, file))
            # If at least one mass value was inferred assume all of them are like this
            if len(dc_mass) > 0:
                subbed_vars[('DIR', 'DATACARD', 'MASS')] = dc_mass
                self.passthru.extend(['-d', '%(DATACARD)s', '-m', '%(MASS)s'])
            else:
                subbed_vars[('DIR', 'DATACARD',)] = dc_no_mass
                self.passthru.extend(['-d', '%(DATACARD)s'])
        # elif len(self.args.datacard) == 1:
        #     self.passthru.extend(['-d', self.args.datacard[0]])

        if self.args.boundlist is not None:
            with open(self.args.boundlist) as json_file:
                bnd = json.load(json_file)
            # find the subbed_vars entry containing the mass
            # We will extend it to also specify the ranges
            dict_key = None
            mass_idx = None
            for key in subbed_vars.keys():
                if 'MASS' in key:
                    dict_key = key
                    mass_idx = dict_key.index('MASS')
            new_key = dict_key + ('MODELBOUND',)
            new_list = []
            for entry in subbed_vars[dict_key]:
                command = []
                mval = entry[mass_idx]
                for model in bnd:
                    command.append(model+'=0,'+str(bnd[model][mval]))
                new_list.append(entry + (':'.join(command),))
            # now remove the current mass information from subbed_vars
            # and replace it with the updated one
            del subbed_vars[dict_key]
            subbed_vars[new_key] = new_list
            self.passthru.extend(['--setPhysicsModelParameterRanges',  '%(MODELBOUND)s'])

        if self.args.points is not None:
            self.passthru.extend(['--points', self.args.points])
        if (self.args.split_points is not None and
                self.args.split_points > 0 and
                self.args.points is not None):
            points = int(self.args.points)
            points = math.ceil(points**0.5)**2
            split = self.args.split_points
            start = 0
            ranges = []
            while (start + (split - 1)) <= points:
            #    filename = "higgsCombine"+self.args.name+".POINTS."+str(start)+"."+str(start+(split-1))+".MultiDimFit.mH"+str(self.args.mass)+".root"
            #    if (not os.path.isfile(filename)) or (os.path.getsize(filename)<1024):
            #        # Send job, if the file it's supposed to create doesn't exist yet
            #        # or if the file is empty because the previous job didn't finish
                ranges.append((start, start + (split - 1)))
                start += split
            if start < points:
            #    filename = "higgsCombine"+self.args.name+".POINTS."+str(start)+"."+str(points - 1)+".MultiDimFit.mH"+str(self.args.mass)+".root"
            #    if (not os.path.isfile(filename)) or (os.path.getsize(filename)<1024):
                ranges.append((start, points - 1))
            #if (ranges == []):
            #    print "No jobs were created; All files already exist"
            #    exit()
            subbed_vars[('P_START', 'P_END')] = [(r[0], r[1]) for r in ranges]
            self.passthru.extend(
                ['--firstPoint %(P_START)s --lastPoint %(P_END)s'])
            self.args.name += '.POINTS.%(P_START)s.%(P_END)s'

        # can only put the name option back now because we might have modified
        # it from what the user specified
        self.put_back_arg('name', '-n')
        proto = 'combine ' + (' '.join(self.passthru))
        if self.args.there:
            proto = 'pushd %(DIR)s; combine ' + (' '.join(self.passthru))+'; popd'

        for it in itertools.product(*subbed_vars.values()):
            keys = subbed_vars.keys()
            dict = {}
            for i, k in enumerate(keys):
                for tuple_i, tuple_ele in enumerate(k):
                    dict[tuple_ele] = it[i][tuple_i]
            self.job_queue.append(proto % dict)
        self.flush_queue()
