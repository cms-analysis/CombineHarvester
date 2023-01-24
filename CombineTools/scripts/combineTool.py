#!/usr/bin/env python3
from __future__ import absolute_import
import argparse
import ROOT

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
from CombineHarvester.CombineTools.combine.EnhancedCombine import EnhancedCombine
from CombineHarvester.CombineTools.combine.Impacts import Impacts
from CombineHarvester.CombineTools.combine.ImpactsFromScans import ImpactsFromScans
from CombineHarvester.CombineTools.combine.Workspace import PrintWorkspace, ModifyDataSet
from CombineHarvester.CombineTools.combine.CovMatrix import CovMatrix
from CombineHarvester.CombineTools.combine.LimitGrids import AsymptoticGrid, HybridNewGrid
from CombineHarvester.CombineTools.combine.Output import PrintFit, CollectLimits, CollectGoodnessOfFit
from CombineHarvester.CombineTools.combine.T2W import T2W
from CombineHarvester.CombineTools.combine.FastScan import FastScan
from CombineHarvester.CombineTools.combine.TaylorExpand import TaylorExpand

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)


def register_method(parser, method_dict, method_class):
    class_name = method_class.__name__
    parser.description += '  %-20s : %s\n' % (
        class_name, method_class.description)
    method_dict[class_name] = method_class

parser = argparse.ArgumentParser(
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.description = 'Available methods:\n\n'
methods = {}
register_method(parser, methods, EnhancedCombine)
register_method(parser, methods, T2W)
register_method(parser, methods, PrintWorkspace)
register_method(parser, methods, ModifyDataSet)
register_method(parser, methods, Impacts)
register_method(parser, methods, ImpactsFromScans)
register_method(parser, methods, CollectLimits)
register_method(parser, methods, CollectGoodnessOfFit)
register_method(parser, methods, CovMatrix)
register_method(parser, methods, PrintFit)
register_method(parser, methods, AsymptoticGrid)
register_method(parser, methods, HybridNewGrid)
register_method(parser, methods, FastScan)
register_method(parser, methods, TaylorExpand)

parser.add_argument('-M', '--method')

(args, unknown) = parser.parse_known_args()

# DRY_RUN = args.dry_run

method = methods[
    args.method]() if args.method in methods else EnhancedCombine()

# Loading libs is slow: only do it if the method has requested it
if method.__class__.requires_root:
    ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

job_group = parser.add_argument_group(
    'job options', 'options for creating, running and submitting jobs')

# One group of options that are specific to the chosen method
tool_group = parser.add_argument_group(
    '%s options' % method.__class__.__name__, 'options specific to this method')
# And another group for combine options that will be intercepted
intercept_group = parser.add_argument_group(
    'combine options', 'standard combine options that will be re-interpreted')

# Let the chosen method create the arguments in both groups
method.attach_job_args(job_group)
method.attach_intercept_args(intercept_group)
method.attach_args(tool_group)

# Now we can add the normal help option
parser.add_argument('-h', '--help', action='help')

(args, unknown) = parser.parse_known_args()

method.set_args(args, unknown)
method.run_method()
