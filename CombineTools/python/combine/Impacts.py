#!/usr/bin/env python

import sys
import json
import ROOT
import CombineHarvester.CombineTools.combine.utils as utils

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase


class Impacts(CombineToolBase):
    description = 'Calculate nuisance parameter impacts'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_intercept_args(self, group):
        CombineToolBase.attach_intercept_args(self, group)
        group.add_argument('-m', '--mass', required=True)
        group.add_argument('-d', '--datacard', required=True)
        group.add_argument('--redefineSignalPOIs')
        group.add_argument('--setPhysicsModelParameters')
        group.add_argument('--name', '-n', default='Test')

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('--named', metavar='PARAM1,PARAM2,...', help=""" By
            default the list of nuisance parameters will be loaded from the
            input workspace. Use this option to specify a different list""")
        group.add_argument('--exclude', metavar='PARAM1,PARAM2,...', help=""" Skip
            these nuisances""")
        group.add_argument('--doInitialFit', action='store_true', help="""Find
            the crossings of all the POIs. Must have the output from this
            before running with --doFits""")
        group.add_argument('--splitInitial', action='store_true', help="""In
            the initial fits generate separate jobs for each POI""")
        group.add_argument('--doFits', action='store_true', help="""Actually
            run the fits for the nuisance parameter impacts, otherwise just
            looks for the results""")
        group.add_argument('--allPars', action='store_true', help="""Run the
            impacts for all free parameters of the model, not just those
            listed as nuisance parameters""")
        group.add_argument('--output', '-o', help="""write output json to a
            file""")

    def run_method(self):
        passthru = self.passthru
        mh = self.args.mass
        ws = self.args.datacard
        name = self.args.name if self.args.name is not None else ''
        named = []
        if self.args.named is not None:
            named = self.args.named.split(',')
        # Put intercepted args back
        passthru.extend(['-m', mh])
        passthru.extend(['-d', ws])
        if self.args.setPhysicsModelParameters is not None:
            passthru.extend(['--setPhysicsModelParameters', self.args.setPhysicsModelParameters])
        pass_str = ' '.join(passthru)
        paramList = []
        if self.args.redefineSignalPOIs is not None:
            poiList = self.args.redefineSignalPOIs.split(',')
        else:
            poiList = utils.list_from_workspace(ws, 'w', 'ModelConfig_POI')
        # print 'Have nuisance parameters: ' + str(paramList)
        print 'Have POIs: ' + str(poiList)
        poistr = ','.join(poiList)
        if self.args.doInitialFit:
            if self.args.splitInitial:
                for poi in poiList:
                    self.job_queue.append(
                        'combine -M MultiDimFit -n _initialFit_%(name)s_POI_%(poi)s --algo singles --redefineSignalPOIs %(poistr)s --floatOtherPOIs 1 --saveInactivePOI 1 -P %(poi)s %(pass_str)s' % vars())
            else:
                self.job_queue.append(
                    'combine -M MultiDimFit -n _initialFit_%(name)s --algo singles --redefineSignalPOIs %(poistr)s %(pass_str)s' % vars())
            self.flush_queue()
            sys.exit(0)
        initialRes = utils.get_singles_results(
            'higgsCombine_initialFit_%(name)s.MultiDimFit.mH%(mh)s.root' % vars(), poiList, poiList)
        if len(named) > 0:
            paramList = named
        elif self.args.allPars:
            paramList = self.all_free_parameters(ws, 'w', 'ModelConfig', poiList)
        else:
            paramList = utils.list_from_workspace(
                ws, 'w', 'ModelConfig_NuisParams')
        if self.args.exclude is not None:
            exclude = self.args.exclude.split(',')
            paramList = [x for x in paramList if x not in exclude]

        print 'Have nuisance parameters: ' + str(len(paramList))
        prefit = utils.prefit_from_workspace(ws, 'w', paramList, self.args.setPhysicsModelParameters)
        res = {}
        res["POIs"] = []
        res["params"] = []
        for poi in poiList:
            res["POIs"].append({"name": poi, "fit": initialRes[poi][poi]})

        missing = []
        for param in paramList:
            pres = {'name': param}
            pres.update(prefit[param])
            # print 'Doing param ' + str(counter) + ': ' + param
            if self.args.doFits:
                self.job_queue.append(
                    'combine -M MultiDimFit -n _paramFit_%(name)s_%(param)s --algo impact --redefineSignalPOIs %(poistr)s -P %(param)s --floatOtherPOIs 1 --saveInactivePOI 1 %(pass_str)s' % vars())
            else:
                paramScanRes = utils.get_singles_results(
                    'higgsCombine_paramFit_%(name)s_%(param)s.MultiDimFit.mH%(mh)s.root' % vars(), [param], poiList + [param])
                if paramScanRes is None:
                    missing.append(param)
                    continue
                pres["fit"] = paramScanRes[param][param]
                for p in poiList:
                    pres.update({p: paramScanRes[param][p], 'impact_' + p: max(map(abs, (x - paramScanRes[
                                param][p][1] for x in (paramScanRes[param][p][2], paramScanRes[param][p][0]))))})
            res['params'].append(pres)
        self.flush_queue()
        jsondata = json.dumps(
            res, sort_keys=True, indent=2, separators=(',', ': '))
        # print jsondata
        if self.args.output is not None:
            with open(self.args.output, 'w') as out_file:
                out_file.write(jsondata)
        if len(missing) > 0:
            print 'Missing inputs: ' + ','.join(missing)

    def all_free_parameters(self, file, wsp, mc, pois):
        res = []
        wsFile = ROOT.TFile(file)
        config = wsFile.Get(wsp).genobj(mc)
        pdfvars = config.GetPdf().getParameters(config.GetObservables())
        it = pdfvars.createIterator()
        var = it.Next()
        while var:
            if var.GetName() not in pois and not var.isConstant():
                res.append(var.GetName())
            var = it.Next()
        return res
