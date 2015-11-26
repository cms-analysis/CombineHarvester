#!/usr/bin/env python

import argparse
import os
import re
import sys
import json
import math
import itertools
import stat
import glob
import ROOT
from array import array
from multiprocessing import Pool
import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.opts import OPTS

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase

class ImpactsFromScans(CombineToolBase):
  description = 'Calculate nuisance parameter impacts' 
  requires_root = True

  def __init__(self):
    CombineToolBase.__init__(self)

  def attach_intercept_args(self, group):
    CombineToolBase.attach_intercept_args(self, group)
    group.add_argument('--name', '-n', default='Test')
    group.add_argument('-m', '--mass', required=True)

  def get_fixed_results(self, file, POIs):
    """Extracts the output from the MultiDimFit singles mode
    Note: relies on the list of parameters that were run (scanned) being correct"""
    res = {}
    f = ROOT.TFile(file)
    if f is None or f.IsZombie():
        return None
    t = f.Get("limit")
    for i, evt in enumerate(t):
        if i != 1: continue
        for POI in POIs:
            res[POI] = getattr(evt, POI)
    return res


  def attach_args(self, group):
    CombineToolBase.attach_args(self, group)
    # group.add_argument('--offset', default=0, type=int,
    #     help='Start the loop over parameters with this offset (default: %(default)s)')
    # group.add_argument('--advance', default=1, type=int,
    #     help='Advance this many parameters each step in the loop (default: %(default)s')
    group.add_argument('--input-json',
        help=('json file and dictionary containing the fit values, of form file:key1:key2..'))
    group.add_argument('--do-fits', action='store_true',
        help=('Actually do the fits'))
  def run_method(self):
    mass = self.args.mass
    self.put_back_arg('mass', '-m')
    in_json = self.args.input_json.split(':')
    with open(in_json[0]) as jsonfile:
      js = json.load(jsonfile)
    for key in in_json[1:]:
      js = js[key]
    POIs = [str(x) for x in js.keys()]
    print POIs
    for POI in POIs:
      if not self.args.do_fits: break
      arg_str = '-M MultiDimFit --algo fixed --saveInactivePOI 1 --floatOtherPOIs 1 -P %s' % POI
      cmd_hi = arg_str + ' -n %s --fixedPointPOIs %s=%f' % (self.args.name+'.%s.Hi'%POI, POI, js[POI]["Val"] + js[POI]["ErrorHi"])
      cmd_lo = arg_str + ' -n %s --fixedPointPOIs %s=%f' % (self.args.name+'.%s.Lo'%POI, POI, js[POI]["Val"] + js[POI]["ErrorLo"])
      self.job_queue.append('combine %s %s' % (cmd_hi, ' '.join(self.passthru)))  
      self.job_queue.append('combine %s %s' % (cmd_lo, ' '.join(self.passthru)))
    self.flush_queue()
    if self.args.do_fits:
      print '>> Re-run without --do-fits to harvest the results'
      return
    res = {}
    for POI in POIs:
      res[POI] = {}
      name_hi = 'higgsCombine%s.%s.Hi.MultiDimFit.mH%s.root' % (self.args.name, POI, mass)
      name_lo = 'higgsCombine%s.%s.Lo.MultiDimFit.mH%s.root' % (self.args.name, POI, mass)
      res_hi = self.get_fixed_results(name_hi, POIs)
      res_lo = self.get_fixed_results(name_lo, POIs)
      for fPOI in POIs:
        res[POI][fPOI] = [res_lo[fPOI], js[fPOI]["Val"], res_hi[fPOI]]
    print res
    cor = ROOT.TMatrixDSym(len(POIs))
    cov = ROOT.TMatrixDSym(len(POIs))
    for i,p in enumerate(POIs):
      cor[i][i] = ROOT.Double(1.) # diagonal correlation is 1
      cov[i][i] = ROOT.Double(pow((res[p][p][2] - res[p][p][0])/2.,2.)) # symmetrized error
    for i,ip in enumerate(POIs):
      for j,jp in enumerate(POIs):
        if i == j: continue
        val_i = ((res[ip][jp][2] - res[ip][jp][0])/2.)/math.sqrt(cov[j][j])
        val_j = ((res[jp][ip][2] - res[jp][ip][0])/2.)/math.sqrt(cov[i][i])
        correlation = (val_i+val_j)/2. # take average correlation?
        #correlation = min(val_i,val_j, key=abs) # take the max?
        cor[i][j] = correlation
        cor[j][i] = correlation
        covariance = correlation * math.sqrt(cov[i][i]) * math.sqrt(cov[j][j])
        cov[i][j] = covariance
        cov[j][i] = covariance
    cor.Print()
    fout = ROOT.TFile('covariance_%s.root' % self.args.name, 'RECREATE')
    fout.WriteTObject(cor, 'cor')
    h_cor = self.fix_TH2(ROOT.TH2D(cor), POIs)
    fout.WriteTObject(h_cor, 'h_cor')
    fout.WriteTObject(cov, 'cov')
    h_cov = self.fix_TH2(ROOT.TH2D(cov), POIs)
    fout.WriteTObject(h_cov, 'h_cov')
    xvars = []
    muvars = []
    xvec = ROOT.RooArgList()
    mu = ROOT.RooArgList()
    for POI in POIs:
      xvars.append(ROOT.RooRealVar(POI, '', js[POI]["Val"], -10, 10))
      muvars.append(ROOT.RooRealVar(POI+'_In', '', js[POI]["Val"], -10, 10))
      muvars[-1].setConstant(True)
      xvec.add(xvars[-1])
      mu.add(muvars[-1])
    xvec.Print('v')
    mu.Print('v')
    pdf = ROOT.RooMultiVarGaussian('pdf', '', xvec, mu, cov)
    dat = ROOT.RooDataSet('global_obs', '', ROOT.RooArgSet(mu))
    dat.add(ROOT.RooArgSet(mu))
    pdf.Print()
    dat.Print()
    #fitRes = pdf.fitTo(dat, ROOT.RooFit.Minimizer('Minuit2', 'Migrad'), ROOT.RooFit.Hesse(True), ROOT.RooFit.Save(True))
    #fitRes.Print('v')
    wsp = ROOT.RooWorkspace('w', '')
    getattr(wsp, 'import')(pdf)
    getattr(wsp, 'import')(dat)
    wsp.Write()
    fout.Close()


  def fix_TH2(self, h, labels):
      h_fix = h.Clone()
      for y in range(1, h.GetNbinsY() + 1):
          for x in range(1, h.GetNbinsX() + 1):
              h_fix.SetBinContent(
                  x, y, h.GetBinContent(x, h.GetNbinsY() + 1 - y))
      for x in range(1, h_fix.GetNbinsX() + 1):
          h_fix.GetXaxis().SetBinLabel(x, labels[x - 1])
      for y in range(1, h_fix.GetNbinsY() + 1):
          h_fix.GetYaxis().SetBinLabel(y, labels[-y])
      return h_fix


      

#          self.job_queue.append('combine -M MultiDimFit -n _initialFit_%(name)s_POI_%(poi)s --algo singles --redefineSignalPOIs %(poistr)s --floatOtherPOIs 1 --saveInactivePOI 1 -P %(poi)s %(pass_str)s --altCommit' % vars())
#      else:
#        self.job_queue.append('combine -M MultiDimFit -n _initialFit_%(name)s --algo singles --redefineSignalPOIs %(poistr)s %(pass_str)s --altCommit' % vars())
#      self.flush_queue()
#      sys.exit(0)
#    initialRes = utils.get_singles_results('higgsCombine_initialFit_%(name)s.MultiDimFit.mH%(mh)s.root' % vars(), poiList, poiList)
#    if len(named) > 0:
#      paramList = named
#    else:
#      paramList = utils.list_from_workspace(ws, 'w', 'ModelConfig_NuisParams')
#    print 'Have nuisance parameters: ' + str(len(paramList))
#    prefit = utils.prefit_from_workspace(ws, 'w', paramList)
#    res = { }
#    res["POIs"] = []
#    res["params"] = []
#    # for poi in poiList:
#    #   res["POIs"].append({"name" : poi, "fit" : initialRes[poi][poi]})
#
#    missing = [ ]
#    for param in paramList:
#      pres = { }
#      # print 'Doing param ' + str(counter) + ': ' + param
#      if self.args.doFits:
#        self.job_queue.append('combine -M MultiDimFit -n _paramFit_%(name)s_%(param)s --algo singles --redefineSignalPOIs %(param)s,%(poistr)s -P %(param)s --floatOtherPOIs 1 --saveInactivePOI 1 %(pass_str)s --altCommit' % vars())
#      else:
#        paramScanRes = get_singles_results('higgsCombine_paramFit_%(name)s_%(param)s.MultiDimFit.mH%(mh)s.root' % vars(), [param], poiList + [param])
#        if paramScanRes is None:
#          missing.append(param)
#          continue
#        pres.update({"name" : param, "fit" : paramScanRes[param][param], "prefit" : prefit[param]})
#        for p in poiList:
#          pres.update({p : paramScanRes[param][p], 'impact_'+p : (paramScanRes[param][p][2] - paramScanRes[param][p][0])/2.})
#        res['params'].append(pres)
#    self.flush_queue()
#    jsondata = json.dumps(res, sort_keys=True, indent=2, separators=(',', ': '))
#    print jsondata
#    if self.args.output is not None:
#      with open(args.output, 'w') as out_file:
#        out_file.write(jsondata)
#    if len(missing) > 0:
#      print 'Missing inputs: ' + ','.join(missing)

