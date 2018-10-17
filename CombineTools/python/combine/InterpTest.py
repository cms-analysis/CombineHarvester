#!/usr/bin/env python

import sys
import json
import ROOT
import re
import CombineHarvester.CombineTools.combine.utils as utils

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
import CombineHarvester.CombineTools.plotting as plot


class InterpTest(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        # group.add_argument('-w', '--workspace', required=True)
        # group.add_argument('-d', '--data')
        # group.add_argument('-f', '--fitres')
        # group.add_argument('--match')
        # group.add_argument('--no-match')
        group.add_argument('-o', '--output', default='nll')
        group.add_argument('-p', '--points', default=200, type=int)

    def RooColIter(self, coll):
        it = coll.createIterator()
        var = it.Next()
        while var:
            yield var
            var = it.Next()

    def run_method(self):
        ROOT.gROOT.SetBatch(ROOT.kTRUE)
        outfile = ROOT.TFile('%s.root' % self.args.output, 'RECREATE')
        points = self.args.points

        xvar = ROOT.RooRealVar("x", "", 0, -2, 2)
        fn = ROOT.RooCMSInterpVar("func", "", xvar, -0.2, 4, 2, -0.5, -0.4)

        # vlo = ROOT.vector('double')(1)
        # vlo[0] = 9.9
        # vhi = ROOT.vector('double')(1)
        # vhi[0] = 14
        # fn = ROOT.RooStats.HistFactory.FlexibleInterpVar("func", "", ROOT.RooArgList(xvar), 10., vlo, vhi)
        # fn.setInterpCode(xvar, 3)

        # fn = ROOT.RooFormulaVar('fn', '', "0.1*@0 + ((1. + tanh(2*@0)) / 2.) * (4*@0 - 0.1*@0)", ROOT.RooArgList(xvar))
        N = 100
        nllvar = ROOT.RooFormulaVar("nll", "", "-(%s)*log(%s+@0) + (%s+@0)" % (N, N, N), ROOT.RooArgList(fn))
        nll = fn
        page = 0
        doPars = []
        for par in [xvar]:
            if par.isConstant():
                continue
            par.Print()
            if not (par.hasMax() and par.hasMin()):
                print 'Parameter does not have an associated range, skipping'
                continue
            doPars.append(par)
        plot.ModTDRStyle(width=700, height=1000)
        for idx, par in enumerate(doPars):
            print '%s : (%i/%i)' % (par.GetName(), idx+1, len(doPars))
            nlld1 = nll.derivative(par, 1)
            nlld2 = nll.derivative(par, 2)
            xmin = par.getMin()
            xmax = par.getMax()
            gr = ROOT.TGraph(points)
            grd1 = ROOT.TGraph(points)
            grd2 = ROOT.TGraph(points)
            gr.SetName(par.GetName())
            grd1.SetName(par.GetName()+"_d1")
            grd2.SetName(par.GetName()+"_d2")
            w = (xmax - xmin) / float(points)
            for i in xrange(points):
                x = xmin + (float(i) + 0.5) * w
                par.setVal(x)
                gr.SetPoint(i, x, nll.getVal())
                grd1.SetPoint(i, x, nlld1.getVal())
                grd2.SetPoint(i, x, nlld2.getVal())
            # plot.ReZeroTGraph(gr, True)
            # plot.RemoveGraphYAbove(gr, 2.)
            # gr.Print()
            outfile.cd()
            gr.Write()
            gr.Print()
            grd1.Write()
            grd2.Write()
            canv = ROOT.TCanvas(self.args.output, self.args.output)
            pads = plot.MultiRatioSplit([0.25, 0.2], [0.02, 0.02], [0.02, 0.02])
            pads[0].cd()
            pads[0].SetGrid(1, 1)
            plot.Set(gr, MarkerSize=0.5)
            gr.Draw('AL')
            axis1 = plot.GetAxisHist(pads[0])
            axis1.GetYaxis().SetTitle('f(x)')
            pads[1].cd()
            pads[1].SetGrid(1, 1)
            plot.Set(grd1, MarkerSize=0.5)
            grd1.Draw('AL')
            axis2 = plot.GetAxisHist(pads[1])
            axis2.GetYaxis().SetTitle('f\'(x)')
            pads[2].cd()
            pads[2].SetGrid(1, 1)
            plot.Set(grd2, MarkerSize=0.5)
            grd2.Draw('AL')
            axis3 = plot.GetAxisHist(pads[2])
            axis3.GetYaxis().SetTitle('f\'\'(x)')
            plot.Set(axis3.GetXaxis(),Title=par.GetName(),
                TitleSize=axis3.GetXaxis().GetTitleSize()*0.5,
                TitleOffset=axis3.GetXaxis().GetTitleOffset()*2,
                )
            extra = ''
            if page == 0:
                extra = '('
            if page == len(doPars) - 1:
                extra = ')'
            print extra
            canv.Print('.pdf%s' % extra)
            page += 1

        outfile.Write()

