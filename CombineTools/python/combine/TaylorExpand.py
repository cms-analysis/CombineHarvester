#!/usr/bin/env python

# import argparse
import os
# import re
# import sys
import json
import math
import itertools
import hashlib
# import stat
# import glob
import ROOT
from array import array
from multiprocessing import Pool
import numpy as np
from numpy.linalg import solve
# import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.opts import OPTS

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase


class PartialFD:
    def __init__(self, pars, d, stencils, coeffs, hvec):
        self.pars = list(pars)
        #self.pars = [float('%f' % p) for p in pars]
        self.d = list(d)
        uniques = sorted(set(d))
        freq = []
        for i in uniques:
            freq.append(self.d.count(i))
        # print '(%s) %s: %s -> %s' % (self.pars, d, uniques, freq)
        self.terms = list()
        if len(freq):
            self.fundamental = False
            stencil = stencils[uniques[0]][freq[0]]
            coeff = coeffs[uniques[0]][freq[0]]
            scale_coeff = 1. / pow(hvec[uniques[0]], freq[0])
            for i in range(len(stencil)):
                remainder = list(filter(lambda a: a != uniques[0], self.d))
                newpars = list(self.pars)
                newpars[uniques[0]] += (stencil[i] * hvec[uniques[0]])
                # print (stencil[i], coeff[i], remainder)
                self.terms.append((stencil[i], coeff[i] * scale_coeff, remainder, PartialFD(newpars, remainder, stencils, coeffs, hvec)))
        else:
            self.fundamental = True
    
    def FormattedPars(self):
        return [float('%f' % p) for p in self.pars]

    def Eval(self):
        if self.fundamental:
            return self.fnval
        else:
            summed = 0
            for t in self.terms:
                summed += t[1] * t[3].Eval()
            return summed

    def Print(self, indent=0, coeff=None):
        sp = ' ' * indent
        extra = ''
        if self.fundamental:
            extra = ' %s' % self.FormattedPars()
        if coeff is None:
            print '%s%s%s' % (sp, self.d, extra)
        else:
            print '%s%+.1f*%s%s' % (sp, coeff, self.d, extra)
        for t in self.terms:
            t[3].Print(indent + 2, t[1])

    def GatherTerms(self, termlist):
        if self.fundamental:
            termlist.append(self)
        else:
            for t in self.terms:
                t[3].GatherTerms(termlist)


class TaylorExpand(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument('--name', '-n', default='Test')
        group.add_argument('-m', '--mass', required=True)

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
        # group.add_argument('--offset', default=0, type=int,
        #     help='Start the loop over parameters with this offset (default: %(default)s)')
        # group.add_argument('--advance', default=1, type=int,
        #     help='Advance this many parameters each step in the loop (default: %(default)s')
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

        # group.add_argument('--do-fits', action='store_true',
        #     help=('Actually do the fits'))
        # group.add_argument('--cov-method', choices=['full', 'asymm'], default='full')
        # group.add_argument('--cor-method', choices=['full', 'asymm', 'average'], default='full')
        # group.add_argument('--asymm-vals', default='')
        # group.add_argument('--do-generic', action='store_true')

    def run_method(self):
        mass = self.args.mass
        self.put_back_arg('mass', '-m')
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
            new_ranges = [x.split("=") for x in self.args.override_sigmas.split(',')]
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
                hvec.append((js[P]["2sig_ErrorHi"] - js[P]["2sig_ErrorLo"]) / 2.)
            else: 
                hvec.append((js[P]["ErrorHi"] - js[P]["ErrorLo"]) / 2.)


        stencil_ranges = {}
        if self.args.override_ranges is not None:
            new_ranges = [x.split("=") for x in self.args.override_ranges.split(':')]
            for new_range in new_ranges:
                stencil_ranges[new_range[0]] = [float(x) for x in new_range[1].split(',')]

        stencils = []
        coeffs = []



        for i,P in enumerate(POIs):
            stencil_item = {}
            coeff_item = {}
            if P in stencil_ranges:
                s_min = stencil_ranges[P][0] - valvec[i]
                s_max = stencil_ranges[P][1] - valvec[i]
                hvec[i] = 1.
            else:
                s_min = -hvec[i]
                s_max = +hvec[i]
                hvec[i] = 1.
            for i in xrange(self.args.order + 1):
                print '>> Order %i' % i
                if i == 0:
                    continue
                stencil_size = max(3, 1 + ((i + 1) / 2) * 2)
                stencil = list()
                stencil_spacing = (s_max - s_min) / (stencil_size - 1)
                for s in range(stencil_size):
                    stencil.append(s_min + float(s) * stencil_spacing)
                stencil_item[i] = sorted(stencil)
                coeff_item[i] = self.generate_fd(i, 1, stencil_item[i])
            stencils.append(stencil_item)
            coeffs.append(coeff_item)

        print stencils
        print coeffs
        evallist = []
        termlist = {}
        for i in xrange(self.args.order + 1):
            print '>> Order %i' % i
            if i == 0 or i == 1:
                continue
            for item in itertools.combinations_with_replacement(range(N), i):
                if len(set(item)) != 1 and i > self.args.cross_order:
                    continue
                termlist[item] = PartialFD(xvec, item, stencils, coeffs, hvec)
                termlist[item].Print()
                termlist[item].GatherTerms(evallist)
            print len(termlist)

        unique_evallist = [list(x) for x in set(tuple(x.FormattedPars()) for x in evallist)]

        filelist = []
        for i, vals in enumerate(unique_evallist):
            set_vals = []
            for POI, val, shift in zip(POIs, valvec, vals):
                set_vals.append('%s=%f' % (POI, shift))
            set_vals_str = ','.join(set_vals)
            hash_id = hashlib.sha1(set_vals_str).hexdigest()
            filename = 'higgsCombine.TaylorExpand.%s.MultiDimFit.mH%s.root' % (hash_id, mass)
            filelist.append(filename)
            arg_str = '-M MultiDimFit -n .TaylorExpand.%s --algo fixed --redefineSignalPOIs %s --fixedPointPOIs ' % (hash_id, ','.join(POIs))
            arg_str += set_vals_str
            if self.args.do_fits and not os.path.isfile(filename):
                self.job_queue.append('combine %s %s' % (arg_str, ' '.join(self.passthru)))

        n_todo = len(self.job_queue)
        self.flush_queue()

        print 'Raw number of evaluations: %i' % len(evallist)
        print 'Actual number of evaluations: %i' % len(unique_evallist)
        print 'Actual number of evaluations to do: %i' % n_todo 
        if self.args.do_fits:
            return

        fnresults = {}
        for i, vals in enumerate(unique_evallist):
            fnresults[tuple(vals)] = self.get_results(filelist[i])
            print ('%s %s %f' % (vals, filelist[i], fnresults[tuple(vals)]))
            if fnresults[tuple(vals)] < 0. or fnresults[tuple(vals)] > 100:
                print 'ODD VALUE'
        # print fnresults

        for x in evallist:
            x.fnval = fnresults[tuple(x.FormattedPars())]

        diffres = {}
        for key, val in termlist.items():
            diffres[key] = val.Eval()
            # print key, val.Eval()


        # Build the taylor expansion object
        xvars = []
        x0vars = []
        xvec = ROOT.RooArgList()
        x0vec = ROOT.RooArgList()
        for i, POI in enumerate(POIs):
            xvars.append(ROOT.RooRealVar(POI, '', js[POI]["Val"], max(0.01, js[POI]["Val"] + 1 * js[POI]["ErrorLo"]), js[POI]["Val"] + 1 * js[POI]["ErrorHi"]))
            x0vars.append(ROOT.RooRealVar(POI+'_In', '', js[POI]["Val"], -100, 100))
            x0vars[-1].setConstant(True)
            xvec.add(xvars[-1])
            x0vec.add(x0vars[-1])


        n_te_terms = 0
        for i in xrange(self.args.order + 1):
            n_te_terms += pow(N, i)

        te_terms = ROOT.TVectorD(n_te_terms)
        pos = 0;
        for n in xrange(self.args.order + 1):
            tracker = [0] * n
            for i in xrange(pow(N, n)):
                sorted_tracker = tuple(sorted(tracker))
                if sorted_tracker in diffres:
                    val = ROOT.Double(diffres[sorted_tracker])
                    te_terms[pos] = val
                    print '%i -- %s --> %s: %f' % (pos, tracker, sorted_tracker, te_terms[pos])
                    if abs(val) > 1000:
                        print '%i -- %s --> %s: %f <ERROR LARGE VALUE>' % (pos, tracker, sorted_tracker, te_terms[pos])
                        te_terms[pos] = ROOT.Double(0.)
                else:
                    te_terms[pos] = ROOT.Double(0.)
                    print '%i -- %s --> %s: <not found>' % (pos, tracker, sorted_tracker)
                for t in xrange(n):
                    if tracker[n - 1 - t] == N -1:
                        tracker[n - 1 - t] = 0
                    else:
                        tracker[n - 1 - t] += 1
                        break
                pos += 1

        nllfn = ROOT.RooTaylorExpansion('nll', '', xvec, x0vec, self.args.order, te_terms)


        fout = ROOT.TFile('taylor_expansion.root', 'RECREATE')
        xvec.Print('v')
        x0vec.Print('v')
        wsp = ROOT.RooWorkspace('w', '')
        getattr(wsp, 'import')(nllfn, ROOT.RooCmdArg())
        wsp.Write()
        fout.Close()
        print hvec



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
                          ( POI), 'RECREATE')
        tout = ROOT.TTree('limit', 'limit')
        a_r = array('f', [x0])
        a_deltaNLL = array('f', [0])
        a_quantileExpected = array('f', [1])

        tout.Branch(POI, a_r, '%s/f' % POI)
        tout.Branch('deltaNLL', a_deltaNLL, 'deltaNLL/f')
        tout.Branch('quantileExpected', a_quantileExpected, 'quantileExpected/f')
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

