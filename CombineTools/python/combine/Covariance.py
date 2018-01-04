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
            self.terms = []
            self.fundamental = True

    def FormattedPars(self):
        return tuple(self.parameter_values)

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
            extra = ' %s = %f' % (list(self.FormattedPars()), self.fnval)
        if coeff is None:
            print '%s%s%s' % (sp, self.derivatives, extra)
        else:
            print '%s%+.1f*%s%s' % (sp, coeff, self.derivatives, extra)
        for i in xrange(len(self.terms)):
            self.terms[i].Print(indent + 2, self.coeffs[i])

    def GatherFundamentalTerms(self, termlist):
        if self.fundamental:
            termlist.append(self)
        else:
            for t in self.terms:
                t.GatherFundamentalTerms(termlist)


class Covariance(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)
        self.nll = None

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument('--name', '-n', default='Test')
        group.add_argument('-d', '--datacard', required=True)


    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('--stencil-add', type=int, default=0,
                           help=('Add additional points to each stencil'))
        group.add_argument('--stencil-min', type=int, default=3,
                           help=('Minimum number of points in stencil'))

    def load_workspace(self, file, POIs, data='data_obs', snapshot='MultiDimFit'):
        if self.nll is not None:
            return
        print 'Loading NLL...'
        self.infile = ROOT.TFile(file)
        self.loaded_wsp = self.infile.Get('w')
        # infile.Close()
        mc = self.loaded_wsp.genobj('ModelConfig')
        pdf = mc.GetPdf()
        data = self.loaded_wsp.data(data)
        ll = ROOT.RooLinkedList()
        self.nll = pdf.createNLL(data, ll)
        self.loaded_wsp.loadSnapshot('MultiDimFit')
        print '...NLL loaded'
        # nll.Print()
        self.nll0 = self.nll.getVal()
        self.wsp_vars = {}
        if POIs is None:
            POIs = []
            allvars = self.nll.getParameters(ROOT.RooArgSet())
            it = allvars.createIterator()
            var = it.Next()
            while var:
                if var.InheritsFrom("RooRealVar") and not var.isConstant():
                    POIs.append(var.GetName())
                var = it.Next()
        for POI in POIs:
            self.wsp_vars[POI] = self.loaded_wsp.var(POI)
        return POIs

    def run_method(self):
        dc = self.args.datacard
        self.put_back_arg('mass', '-m')
        self.put_back_arg('datacard', '-d')

        ######################################################################
        # Step 1 - establish parameter ranges
        ######################################################################

        POIs = self.load_workspace(dc, None)
        cfg = {}
        for P in POIs:
            cfg[P] = {}
            self.wsp_vars[P].Print()
            cfg[P]["BestFit"] = self.wsp_vars[P].getVal()
            cfg[P]["StencilSize"] = self.wsp_vars[P].getError() * 0.1
            cfg[P]["Validity"] = self.wsp_vars[P].getError() * 0.1
        Nx = len(POIs)
        pprint(cfg)

        xvec = np.zeros(Nx, dtype=np.float32)
        # hvec = []
        valvec = []
        for i, P in enumerate(POIs):
            valvec.append(cfg[P]["BestFit"])
            xvec[i] = cfg[P]["BestFit"]

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
            for n in xrange(3):
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

        for i in xrange(3):
            print '>> Order %i' % i
            if i == 0 or i == 1:
                continue

            for item in itertools.combinations_with_replacement(range(Nx), i):
                evallist = []

                term = ExpansionTerm(xvec, item, stencils)
                term.GatherFundamentalTerms(evallist)

                for point in evallist:
                    for POI, val in zip(POIs, point.FormattedPars()):
                            self.wsp_vars[POI].setVal(val)
                    point.fnval = self.nll.getVal() - self.nll0

                val = term.Eval(with_permutations=False, with_factorial=True)
                print '%s = %f' % (str(item), val)



        # # Build the taylor expansion object
        # xvars = []
        # x0vars = []
        # xvec = ROOT.RooArgList()
        # x0vec = ROOT.RooArgList()
        # for i, POI in enumerate(POIs):
        #     xvars.append(ROOT.RooRealVar(POI, '', cfg[POI]["BestFit"], cfg[POI]['OutputRange'][0], cfg[POI]['OutputRange'][1]))
        #     x0vars.append(ROOT.RooRealVar(
        #         POI + '_In', '', cfg[POI]["BestFit"], -100, 100))
        #     x0vars[-1].setConstant(True)
        #     xvec.add(xvars[-1])
        #     x0vec.add(x0vars[-1])

        # te_terms = ROOT.vector('double')()
        # pos = 0
        # te_tracker = ROOT.vector('std::vector<int>')()

        # sorted_terms = []
        # for i in xrange(self.args.order + 1):
        #     sorted_tmp = []
        #     for tracker, val in cached_terms.iteritems():
        #         if len(tracker) == i:
        #             sorted_tmp.append((tracker, val))
        #     sorted_terms.extend(sorted(sorted_tmp, key=lambda x: x[0]))
        # for tracker, val in sorted_terms:
        #     # Check if this is a really big value
        #     # if abs(val) > 1E9:
        #     #     print '%i -- %s --> %s: %f <ERROR LARGE VALUE>' % (pos, tracker, tracker, val)
        #     #     val = 0.

        #     # Push back the terms
        #     te_terms.push_back(val)
        #     i_tracker = ROOT.vector('int')(len(tracker))
        #     for idx, tr in enumerate(tracker):
        #         i_tracker[idx] = tr
        #     te_tracker.push_back(i_tracker)

        #     # Print it
        #     print '%i -- %s --> %s: %f' % (pos, tracker, tracker, val)

        # # print 'NEGLIGIBLE TERMS AT ORDER %i: %i/%i' % (n, n_below, n_terms)

        # nllfn = ROOT.RooTaylorExpansion(
        #     'nll', '', xvec, x0vec, te_tracker, te_terms)

        # fout = ROOT.TFile('taylor_expansion.root', 'RECREATE')
        # # xvec.Print('v')
        # # x0vec.Print('v')
        # wsp = ROOT.RooWorkspace('w', '')
        # getattr(wsp, 'import')(nllfn, ROOT.RooCmdArg())
        # wsp.Write()
        # fout.Close()

        # print '%-10s %-20s %-20s %-20s %-20s %-20s' % ('Order', 'nTerms', 'nCachedTerms', 'nSmallTerms', 'nAllNewTerms', 'nActualNewTerms')
        # print '-' * 94
        # for i in stats:
        #     print '%-10i %-20i %-20i %-20i %-20i %-20i' % (i, stats[i]['nTerms'], stats[i]['nCachedTerms'], stats[i]['nSmallTerms'], stats[i]['nAllNewTerms'], stats[i]['nActualNewTerms'])

        # print '\n%-10s %-20s %-20s %-20s' % ('Order', 'nEvals', 'nUniqueEvals', 'nActualUniqueEvals')
        # print '-' * 74
        # for i in stats:
        #     print '%-10i %-20i %-20i %-20i' % (i, stats[i]['nEvals'], stats[i]['nUniqueEvals'], stats[i]['nActualUniqueEvals'])
