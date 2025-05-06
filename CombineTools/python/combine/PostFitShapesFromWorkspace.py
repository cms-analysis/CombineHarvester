#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import sys
import re
import json
import ROOT
import CombineHarvester.CombineTools.combine.utils as utils

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
from six.moves import map


class PostFitShapesFromWorkspace(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument('-w', '--workspace', required=True)
        group.add_argument('-f', '--fitresult', required=True)
        group.add_argument('-d','--datacard', default="")
        group.add_argument('--freeze', default="")
        group.add_argument('-m', '--mass')
        group.add_argument('--samples', default="")
        group.add_argument('--covariance', action='store_true')
        group.add_argument('--skip-proc-errs', action='store_true')
        group.add_argument('--total-shapes', action='store_true')
        group.add_argument('--postfit', action='store_true')
        
    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('--outdir', '-o', help="""output directory for root files""")

    def run_method(self):
        wsFile = ROOT.TFile(self.args.workspace)
        w = wsFile.Get('w')
        pass_str = ' '.join(self.passthru)
        bins = [ nameIdx.first for nameIdx in w.allCats()["CMS_channel"] ]
        print("bins",bins)

        extra_args_str = " --workspace %s --fitresult %s "%(self.args.workspace,self.args.fitresult)
        if self.args.skip_proc_errs:
            extra_args_str += " --skip-proc-errs "
        if self.args.total_shapes:
            extra_args_str += " --total-shapes "
        if self.args.postfit:
            extra_args_str += " --postfit "
        if self.args.covariance:
            extra_args_str += " --covariance "
        if self.args.freeze!="":
            extra_args_str += " --freeze %s "%(self.args.freeze)
        if self.args.datacard!="":
            extra_args_str += " --datacard %s "%(self.args.datacard)
        if self.args.samples!="":
            extra_args_str += " --samples %s "%(self.args.samples)
            
        for b in bins:
            outfile="%s/shapes_%s.root"%(self.args.outdir, b)
            self.job_queue.append(
                'PostFitShapesFromWorkspace %s --selected-bins %s --output %s'%(extra_args_str,b,outfile))
        self.flush_queue()
        sys.exit(0)

