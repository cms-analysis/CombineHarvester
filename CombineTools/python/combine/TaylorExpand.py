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
    """Calculate the number of unique permutations of a set of indicies

    Args:
        indicies (list): A list of integer indicies, e.g [0, 1, 2, 3]

    Returns:
        int: number of unique permutations
    """
    uniques = sorted(set(indicies))
    freqs = [indicies.count(x) for x in uniques]
    n_perms = math.factorial(len(indicies))
    for freq in freqs:
        n_perms = n_perms / math.factorial(freq)
    return n_perms


def GenerateStencils(d, h, s):
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

# Calculate partial derivatives using finite differences
class ExpansionTerm:
    def __init__(self, parameter_values, derivatives, stencils):
        self.fnval = 0.
        self.parameter_values = np.array(parameter_values, dtype=np.float32)
        self.derivatives = np.array(derivatives, dtype=np.uint8)
        unique_derivatives = np.array(sorted(set(derivatives)), dtype=np.uint8)
        derivative_frequency = np.zeros(len(unique_derivatives), dtype=np.uint8)
        for idx, i in enumerate(unique_derivatives):
            derivative_frequency[idx] = np.count_nonzero(self.derivatives == i)
        terms = list()
        # self.terms = list()
        if len(derivative_frequency):
            parameter = unique_derivatives[0]
            order = derivative_frequency[0]
            self.fundamental = False
            stencil = stencils[parameter][order]
            self.coeffs = np.zeros(len(stencil), dtype=np.float64)
            for i in xrange(len(stencil)):
                remaining_derivatives = np.array(list(
                    filter(lambda a: a != parameter, self.derivatives)), dtype=np.uint8)
                # Make a copy of the current parameters and adjust the
                # value for the current stencil point
                new_parameter_values = np.array(self.parameter_values, dtype=np.float32)
                new_parameter_values[parameter] += stencil[i][0]
                # Add this to the list of terms
                self.coeffs[i] = stencil[i][1]
                terms.append(ExpansionTerm(
                    new_parameter_values, remaining_derivatives, stencils))
            self.terms = np.array(terms)
        else:
            self.fundamental = True

    def FormattedPars(self):
        return [float('%f' % p) for p in self.parameter_values]

    def Eval(self, with_permutations=False, with_factorial=False):
        if self.fundamental:
            return self.fnval
        else:
            summed = 0.
            for i in xrange(len(self.terms)):
                summed += self.coeffs[i] * self.terms[i].Eval()
            if with_permutations:
                n_perms = Permutations(list(self.derivatives))
                summed *= float(n_perms)
            if with_factorial:
                summed *= 1. / float(math.factorial(len(self.derivatives)))
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
        for i in xrange(len(self.terms)):
            self.terms[i].Print(indent + 2, self.coeffs[i])

    def GatherTerms(self, termlist):
        if self.fundamental:
            termlist.append(self)
        else:
            for t in self.terms:
                t.GatherTerms(termlist)

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
        group.add_argument('--config',
                           help=('json configuration file'))
        group.add_argument('--order', type=int, default=2,
                           help=('Taylor expand up to and including this order'))
        group.add_argument('--cross-order', type=int, default=2,
                           help=('Taylor expand up to and including this order for the cross-order terms'))
        group.add_argument('--choose-POIs', default=None,
                           help=('Explict list POIs to expand in'))
        group.add_argument('--do-fits', action='store_true',
                           help=('Actually do the fits'))
        group.add_argument('--test-mode', type=int, default=0,
                           help=('Test on the workspace'))
        group.add_argument('--save', default=None,
                           help=('Save results to a json file'))
        group.add_argument('--load', default=None,
                           help=('Load results from a json file'))
        group.add_argument('--stencil-add', type=int, default=0,
                           help=('Add additional points to each stencil'))
        group.add_argument('--stencil-min', type=int, default=3,
                           help=('Minimum number of points in stencil'))
    def run_method(self):
        mass = self.args.mass
        dc = self.args.datacard
        self.put_back_arg('mass', '-m')
        self.put_back_arg('datacard', '-d')

        ######################################################################
        # Step 1 - establish parameter ranges
        ######################################################################
        with open(self.args.config) as jsonfile:
            cfg = json.load(jsonfile)
        if self.args.choose_POIs is None:
            POIs = sorted([str(x) for x in cfg.keys()])
        else:
            POIs = self.args.choosePOIs.split(',')

        Nx = len(POIs)
        print '>> Taylor expansion in %i variables up to order %i:' % (Nx, self.args.order)
        pprint(cfg)

        x = np.zeros(Nx, dtype=np.float32)
        # hvec = []
        valvec = []
        for i, P in enumerate(POIs):
            valvec.append(cfg[P]["BestFit"])
            x[i] = cfg[P]["BestFit"]

        ######################################################################
        # Step 2 - generate stencils
        ######################################################################
        stencils = {}

        validity = []

        for i, P in enumerate(POIs):
            stencils[i] = {}
            if 'StencilRange' in cfg[P]:
                s_min = cfg[P]['StencilRange'][0] - valvec[i]
                s_max = cfg[P]['StencilRange'][1] - valvec[i]
            elif 'StencilSize' in cfg[P]:
                s_min = -cfg[P]['StencilSize']
                s_max = +cfg[P]['StencilSize']
            validity.append(cfg[P]['Validity'])
            for n in xrange(self.args.order + 1):
                if n == 0:
                    continue
                stencil_size = max(self.args.stencil_min, 1 + (((n + 1) / 2) * 2) + self.args.stencil_add)
                stencil = list()
                stencil_spacing = (s_max - s_min) / (stencil_size - 1)
                for s in range(stencil_size):
                    stencil.append(s_min + float(s) * stencil_spacing)
                coefficients = GenerateStencils(n, 1, stencil)
                stencils[i][n] = zip(stencil, coefficients)

        pprint(stencils)

        evallist = []
        termlist = {}

        diffres = {}
        can_skip = []

        drop_thresh = 0.

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
            for item in itertools.combinations_with_replacement(range(Nx), i):
                if len(set(item)) != 1 and i > self.args.cross_order:
                    continue

                if item in diffres:
                    # print 'Skipping already loaded: %s = %f' % (str(item), diffres[item])
                    # estimate max contribution
                    estimate = diffres[item]
                    for index in item:
                        estimate *= validity[index]
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
                        fact_ratio = float(math.factorial(len(skip_item[0]))) / float(math.factorial(len(item)))
                        expected = diffres[skip_item[0]] * perm_ratio * fact_ratio
                        for index in item:
                            expected *= validity[index]
                        print 'Original = %g, permutations ratio = %g, factorial ratio = %g, final = %g' % (
                            skip_item[2],
                            perm_ratio,
                            fact_ratio,
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

                termlist[item] = ExpansionTerm(
                    x, item, stencils)
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
                    print 'Done %i NLL evaluations...' % i
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
            diffres[key] = val.Eval(with_permutations=True, with_factorial=True)
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
            xvars.append(ROOT.RooRealVar(POI, '', cfg[POI]["BestFit"], cfg[POI]['OutputRange'][0], cfg[POI]['OutputRange'][1]))
            x0vars.append(ROOT.RooRealVar(
                POI + '_In', '', cfg[POI]["BestFit"], -100, 100))
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
        # xvec.Print('v')
        # x0vec.Print('v')
        wsp = ROOT.RooWorkspace('w', '')
        getattr(wsp, 'import')(nllfn, ROOT.RooCmdArg())
        wsp.Write()
        fout.Close()

        print 'Raw number of evaluations: %i' % len(evallist)
        print 'Actual number of evaluations: %i' % len(unique_evallist)
        print 'Actual number of evaluations to do: %i' % n_todo
