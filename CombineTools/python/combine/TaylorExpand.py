#!/usr/bin/env python

import os
import cPickle as pickle
import math
import json
import itertools
import hashlib
import ROOT
from array import array
import numpy as np
from pprint import pprint
from CombineHarvester.CombineTools.combine.opts import OPTS
from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase


def Permutations(indicies):
    indicies = list(indicies)
    uniques = sorted(set(indicies))
    freqs = [indicies.count(x) for x in uniques]
    n_perms = math.factorial(len(indicies))
    for freq in freqs:
        n_perms = n_perms / math.factorial(freq)
    return n_perms

# parameter_values = [x1, x2, ..., xn]
# derivatives = [0,1,1]
# stencils = {
#     1: {  <-- parameter 1
#         2: [(dx1, c1), (dx2, c2), ...], <-- order 2
#
#     }
# }
# Calculate partial derivatives using finite differences
class PartialDerivative:
    def __init__(self, parameter_values, derivatives, stencils):
        self.fnval = 0.
        self.parameter_values = list(parameter_values)
        self.derivatives = list(derivatives)
        self.unique_derivatives = sorted(set(derivatives))
        self.derivative_frequency = []
        for i in self.unique_derivatives:
            self.derivative_frequency.append(self.derivatives.count(i))
        self.terms = list()
        if len(self.derivative_frequency):
            parameter = self.unique_derivatives[0]
            order = self.derivative_frequency[0]
            self.fundamental = False
            stencil = stencils[parameter][order]
            for i in range(len(stencil)):
                remaining_derivatives = list(
                    filter(lambda a: a != parameter, self.derivatives))
                # Make a copy of the current parameters and adjust the
                # value for the current stencil point
                new_parameter_values = list(self.parameter_values)
                new_parameter_values[parameter] += stencil[i][0]
                # Add this to the list of terms
                self.terms.append((stencil[i][1], PartialDerivative(
                    new_parameter_values, remaining_derivatives, stencils)))
        else:
            self.fundamental = True

    def FormattedPars(self):
        return [float('%f' % p) for p in self.parameter_values]

    def Eval(self, with_permutations=False):
        if self.fundamental:
            return self.fnval
        else:
            summed = 0
            for t in self.terms:
                summed += t[0] * t[1].Eval()
            if with_permutations:
                n_perms = math.factorial(len(self.derivatives))
                for freq in self.derivative_frequency:
                    n_perms = n_perms / math.factorial(freq)
                return summed * float(n_perms)
            else:
                return summed

    def Print(self, indent=0, coeff=None):
        sp = ' ' * indent
        extra = ''
        if self.fundamental:
            extra = ' %s' % self.FormattedPars()
        if coeff is None:
            print '%s%s%s' % (sp, self.derivatives, extra)
        else:
            print '%s%+.1f*%s%s' % (sp, coeff, self.derivatives, extra)
        for t in self.terms:
            t[1].Print(indent + 2, t[0])

    def GatherTerms(self, termlist):
        if self.fundamental:
            termlist.append(self)
        else:
            for t in self.terms:
                t[1].GatherTerms(termlist)

# Should report:
#
#  Order  nTerms nEvals nNewEvals  nFoundNegTerms  nExpNegTerms  nActualEvals nNewActualEvals
#    2       X       Y         Z                         T
#


class TaylorExpand(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument('--name', '-n', default='Test')
        group.add_argument('-m', '--mass', required=True)
        group.add_argument('-d', '--datacard', required=True)

    def get_results(self, file):
        f = ROOT.TFile(file)
        if f is None or f.IsZombie():
            return None
        t = f.Get("limit")
        for i, evt in enumerate(t):
            if i != 1:
                continue
            res = getattr(evt, 'deltaNLL')
        return res

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('--input-json',
                           help=('json file and dictionary containing the fit values, of form file:key1:key2..'))
        group.add_argument('--order', type=int, default=2,
                           help=('Taylor expand up to and including this order'))
        group.add_argument('--cross-order', type=int, default=2,
                           help=('Taylor expand up to and including this order for the cross-order terms'))
        group.add_argument('--choosePOIs', default=None,
                           help=('Explict list POIs to expand in'))
        group.add_argument('--do-fits', action='store_true',
                           help=('Actually do the fits'))
        group.add_argument('--step-size', choices=['1sigma', '2sigma'], default='1sigma',
                           help=('Take the one or two sigma interval as step size for calculation derivatives'))
        group.add_argument('--override-ranges', default=None,
                           help=('Explict list POIs to expand in'))
        group.add_argument('--override-sigmas', default=None,
                           help=('Explict list POIs to expand in'))
        group.add_argument('--test-mode', type=int, default=0,
                           help=('Test on the workspace'))
        group.add_argument('--save', default=None,
                           help=('Save results to a json file'))
        group.add_argument('--load', default=None,
                           help=('Load results from a json file'))
        group.add_argument('--validity', default=None,
                           help=('Set the validity ranges'))
    def run_method(self):
        mass = self.args.mass
        dc = self.args.datacard
        self.put_back_arg('mass', '-m')
        self.put_back_arg('datacard', '-d')

        ######################################################################
        # Step 1 - establish parameter ranges
        ######################################################################
        in_json = self.args.input_json.split(':')
        with open(in_json[0]) as jsonfile:
            js = json.load(jsonfile)
        for key in in_json[1:]:
            js = js[key]
        if self.args.choosePOIs is None:
            POIs = sorted([str(x) for x in js.keys()])
        else:
            POIs = self.args.choosePOIs.split(',')
        print POIs
        N = len(POIs)

        print 'Taylor expand with N = %i up to order %i' % (N, self.args.order)

        hvec_overrides = {}
        if self.args.override_sigmas is not None:
            new_ranges = [x.split("=")
                          for x in self.args.override_sigmas.split(',')]
            for new_range in new_ranges:
                hvec_overrides[new_range[0]] = float(new_range[1])

        xvec = np.zeros((N))
        hvec = []
        valvec = []
        for i, P in enumerate(POIs):
            valvec.append(js[P]["Val"])
            xvec[i] = js[P]["Val"]
            if P in hvec_overrides:
                hvec.append(hvec_overrides[P])
            elif self.args.step_size == '2sigma' and js[P]["2sig_ValidErrorHi"] and js[P]["2sig_ValidErrorLo"]:
                hvec.append(
                    min((js[P]["2sig_ErrorHi"] - js[P]["2sig_ErrorLo"]), js[P]['Val'] * 0.95))
            else:
                hvec.append((js[P]["ErrorHi"] - js[P]["ErrorLo"]) / 2.)

        stencil_ranges = {}
        if self.args.override_ranges is not None:
            new_ranges = [x.split("=")
                          for x in self.args.override_ranges.split(':')]
            for new_range in new_ranges:
                stencil_ranges[new_range[0]] = [
                    float(x) for x in new_range[1].split(',')]

        ######################################################################
        # Step 2 - generate stencils
        ######################################################################
        stencils = {}

        validity = []

        for i, P in enumerate(POIs):
            stencils[i] = {}
            if P in stencil_ranges:
                s_min = stencil_ranges[P][0] - valvec[i]
                s_max = stencil_ranges[P][1] - valvec[i]
            else:
                s_min = -hvec[i]
                s_max = +hvec[i]
            validity.append(max(abs(s_min), abs(s_max)))
            for n in xrange(self.args.order + 1):
                if n == 0:
                    continue
                stencil_size = max(7, 3 + ((n + 1) / 2) * 2)
                # N  add1   add3    add5     add3min7   add5min7
                # 2     3      5       7            7          7
                # 3     5      7       9            7          9
                # 4     5      7       9            7          9
                # 5     7      9       11           9         11
                # 6     7      9       11           9         11
                # 7     9      11      13          11         13
                # 8     9      11      13          11         13
                # 9     11     13      15          13         11
                # stencil_size = 5 + ((i + 1) / 2) * 2
                stencil = list()
                stencil_spacing = (s_max - s_min) / (stencil_size - 1)
                for s in range(stencil_size):
                    stencil.append(s_min + float(s) * stencil_spacing)
                coefficients = self.generate_fd(n, 1, stencil)
                stencils[i][n] = zip(stencil, coefficients)

        if self.args.validity is not None:
            validity_dict = {x.split('=')[0]: float(x.split('=')[1]) for x in self.args.validity.split(',')}
            for i, P in enumerate(POIs):
                if P in validity_dict:
                    print 'Updating valididty range of %s to %f' % (P, validity_dict[P])
                    validity[i] = validity_dict[P]


        pprint(stencils)

        evallist = []
        termlist = {}

        diffres = {}
        can_skip = []

        drop_thresh = 1E-1

        ######################################################################
        # Step 3 - load pre-existing terms
        ######################################################################
        if self.args.load is not None and os.path.isfile(self.args.load):
            with open(self.args.load) as jsonfile:
                diffres = pickle.load(jsonfile)

        for i in xrange(self.args.order + 1):
            print '>> Order %i' % i
            if i == 0 or i == 1:
                continue
            for item in itertools.combinations_with_replacement(range(N), i):
                if len(set(item)) != 1 and i > self.args.cross_order:
                    continue
                # if i == 3 and len(set(item)) == 2:
                #     continue
                # print item
                if item in diffres:
                    # print 'Skipping already loaded: %s = %f' % (str(item), diffres[item])
                    # estimate max contribution
                    estimate = diffres[item]
                    for index in item:
                        estimate *= validity[index]
                    estimate /= float(math.factorial(len(item)))
                    # if abs(diffres[item]) < drop_thresh:
                    if abs(estimate) < drop_thresh:
                        can_skip.append((item, {x: item.count(x) for x in set(item)}, estimate))
                        # can_skip.add(item)
                    continue
                skip_me = False
                # Be careful: [0, 0, 1] is not a subset of [0, 1, 2, 3]
                for skip_item in can_skip:
                    has_all_terms = True
                    for x, freq in skip_item[1].iteritems():
                        if item.count(x) < freq:
                            has_all_terms = False
                            break
                    if has_all_terms:
                        print 'Skipping %s containing %s' % (str(item), str(skip_item))
                        perm_ratio = float(Permutations(item)) / float(Permutations(skip_item[0]))
                        expected = diffres[skip_item[0]] * perm_ratio * (1. / math.factorial(len(item)))
                        for index in item:
                            expected *= validity[index]
                        print 'Original = %g, permutations ratio: %g/%g = %g, factorial term = %g, final = %g' % (
                            skip_item[2],
                            Permutations(item),
                            Permutations(skip_item[0]),
                            perm_ratio,
                            (1. / math.factorial(len(item))),
                            expected)
                        # print 'Original estimate was %g, scaling with missing %s = %g' % (skip_item[2], str(remainder_terms), expected)
                        if abs(expected) < drop_thresh:
                            skip_me = True
                            break
                        else:
                            print 'Expectation too large...'
                if skip_me:
                    # print 'Skipping negligible: %s' % str(item)
                    continue

                termlist[item] = PartialDerivative(
                    xvec, item, stencils)
                # termlist[item].Print()
                termlist[item].GatherTerms(evallist)
            # print len(termlist)

        unique_evallist = [list(x) for x in set(
            tuple(x.FormattedPars()) for x in evallist)]

        print 'Raw number of evaluations: %i' % len(evallist)
        print 'Actual number of evaluations: %i' % len(unique_evallist)
        filelist = []

        wsp_vars = {}
        if self.args.test_mode > 0 and len(unique_evallist) > 0:
            print 'Loading NLL...'
            infile = ROOT.TFile(dc)
            wsp = infile.Get('w')
            mc = wsp.genobj('ModelConfig')
            pdf = mc.GetPdf()
            data = wsp.data('data_obs')
            ll = ROOT.RooLinkedList()
            nll = pdf.createNLL(data, ll)
            wsp.loadSnapshot('MultiDimFit')
            print '...NLL loaded'
            nll.Print()
            nll0 = nll.getVal()

            for POI in POIs:
                wsp_vars[POI] = wsp.var(POI)

        vallist = []
        for i, vals in enumerate(unique_evallist):
            set_vals = []
            for POI, val, shift in zip(POIs, valvec, vals):
                set_vals.append('%s=%f' % (POI, shift))
                if self.args.test_mode > 0:
                    wsp_vars[POI].setVal(shift)
            set_vals_str = ','.join(set_vals)
            hash_id = hashlib.sha1(set_vals_str).hexdigest()
            filename = 'higgsCombine.TaylorExpand.%s.MultiDimFit.mH%s.root' % (
                hash_id, mass)
            filelist.append(filename)
            arg_str = '-M MultiDimFit -n .TaylorExpand.%s --algo fixed --redefineSignalPOIs %s --fixedPointPOIs ' % (
                hash_id, ','.join(POIs))
            arg_str += set_vals_str
            if self.args.do_fits and not os.path.isfile(filename) and not self.args.test_mode > 0:
                self.job_queue.append('combine %s %s' %
                                      (arg_str, ' '.join(self.passthru)))
            if self.args.test_mode > 0:
                if i % 10000 == 0:
                    print 'Done %i evaluations...' % i
                vallist.append(nll.getVal() - nll0)
        n_todo = len(self.job_queue)
        self.flush_queue()

        print 'Raw number of evaluations: %i' % len(evallist)
        print 'Actual number of evaluations: %i' % len(unique_evallist)
        if self.args.do_fits:
            return

        fnresults = {}
        for i, vals in enumerate(unique_evallist):
            if self.args.test_mode > 0:
                fnresults[tuple(vals)] = vallist[i]
            else:
                fnresults[tuple(vals)] = self.get_results(filelist[i])
            # print ('%s %s %f' % (vals, filelist[i], fnresults[tuple(vals)]))
            # if fnresults[tuple(vals)] < 0. or fnresults[tuple(vals)] > 100:
            #     print 'ODD VALUE'
        # print fnresults

        for x in evallist:
            x.fnval = fnresults[tuple(x.FormattedPars())]

        for key, val in termlist.items():
            diffres[key] = val.Eval(with_permutations=True)
            # print key, val.Eval()

        if self.args.save is not None:
            jsondata = pickle.dumps(
                diffres)
            with open(self.args.save, 'w') as out_file:
                out_file.write(jsondata)

        # Build the taylor expansion object
        xvars = []
        x0vars = []
        xvec = ROOT.RooArgList()
        x0vec = ROOT.RooArgList()
        for i, POI in enumerate(POIs):
            xvars.append(ROOT.RooRealVar(POI, '', js[POI]["Val"], js[POI]["Val"] + 4 *
                                         js[POI]["2sig_ErrorLo"], js[POI]["Val"] + 4 * js[POI]["2sig_ErrorHi"]))
            x0vars.append(ROOT.RooRealVar(
                POI + '_In', '', js[POI]["Val"], -100, 100))
            x0vars[-1].setConstant(True)
            xvec.add(xvars[-1])
            x0vec.add(x0vars[-1])

        te_terms = ROOT.vector('double')()
        pos = 0
        te_tracker = ROOT.vector('std::vector<int>')()

        n_terms = 0
        n_below = 0
        for tracker, val in diffres.iteritems():
            # Check if this is a really big value
            # if abs(val) > 1E9:
            #     print '%i -- %s --> %s: %f <ERROR LARGE VALUE>' % (pos, tracker, tracker, val)
            #     val = 0.

            # Push back the terms
            te_terms.push_back(val)
            i_tracker = ROOT.vector('int')(len(tracker))
            for idx, tr in enumerate(tracker):
                i_tracker[idx] = tr
            te_tracker.push_back(i_tracker)

            # Keep track of the number of terms of order n
            n_terms += 1
            if abs(val) < drop_thresh:
                n_below += 1

            # Print it
            if n <= 3:
                print '%i -- %s --> %s: %f' % (pos, tracker, tracker, val)

        # print 'NEGLIGIBLE TERMS AT ORDER %i: %i/%i' % (n, n_below, n_terms)

        nllfn = ROOT.RooTaylorExpansion(
            'nll', '', xvec, x0vec, te_tracker, te_terms)

        fout = ROOT.TFile('taylor_expansion.root', 'RECREATE')
        xvec.Print('v')
        x0vec.Print('v')
        wsp = ROOT.RooWorkspace('w', '')
        getattr(wsp, 'import')(nllfn, ROOT.RooCmdArg())
        wsp.Write()
        fout.Close()

        print 'Raw number of evaluations: %i' % len(evallist)
        print 'Actual number of evaluations: %i' % len(unique_evallist)
        print 'Actual number of evaluations to do: %i' % n_todo

    def generate_fd(self, d, h, s):
        N = len(s)
        smatrix = np.zeros((N, N))
        dvec = np.zeros((N))
        for i in range(N):
            for j in range(N):
                smatrix[i, j] = pow(s[j], i)
            dvec[i] = math.factorial(d) if i == d else 0.
        # print smatrix
        # print dvec
        res = (1. / pow(h, d)) * np.dot(np.linalg.inv(smatrix), dvec)
        return res

    def TaylorExpand1D(self, devs, x0, x):
        res = 0.
        for i in xrange(self.args.order + 1):
            if i == 1:
                continue
            term = pow(x - x0, i) / math.factorial(i)
            if tuple([0] * i) in devs:
                term *= devs[tuple([0] * i)]
            else:
                term *= 0.
            res += term
        return res

    def QuickTestOneVar(self, POI, x0, r_min, r_max, points, devs):
        fout = ROOT.TFile('scan_covariance_%s.root' %
                          (POI), 'RECREATE')
        tout = ROOT.TTree('limit', 'limit')
        a_r = array('f', [x0])
        a_deltaNLL = array('f', [0])
        a_quantileExpected = array('f', [1])

        tout.Branch(POI, a_r, '%s/f' % POI)
        tout.Branch('deltaNLL', a_deltaNLL, 'deltaNLL/f')
        tout.Branch('quantileExpected', a_quantileExpected,
                    'quantileExpected/f')
        tout.Fill()

        width = (r_max - r_min) / points
        r = r_min + 0.5 * width
        for p in xrange(points):
            a_r[0] = r
            nllf = self.TaylorExpand1D(devs, x0, r)
            a_deltaNLL[0] = nllf
            print '%s = %f: %f' % (POI, r, nllf)
            if a_deltaNLL[0] > 0.:
                tout.Fill()
            r += width

        tout.Write()
        fout.Close()
