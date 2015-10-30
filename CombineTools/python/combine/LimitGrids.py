import ROOT
import json
import itertools
import glob
import sys
import re
from array import array

import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
from CombineHarvester.CombineTools.mssm_multidim_fit_boundaries import mssm_multidim_fit_boundaries as bounds

class AsymptoticGrid(CombineToolBase):
  description = 'Calculate asymptotic limits on parameter grids' 
  requires_root = True

  def __init__(self):
    CombineToolBase.__init__(self)

  def attach_intercept_args(self, group):
    CombineToolBase.attach_intercept_args(self, group)

  def attach_args(self, group):
    CombineToolBase.attach_args(self, group)
    group.add_argument('config', help='json config file')

  def run_method(self):
    # This is what the logic should be:
    #  - get the list of model points
    #  - figure out which files are:
    #    - completely missing
    #    - there but corrupt, missing tree
    #    - ok
    #  - If we have anything in the third category proceed to produce output files
    #  - Anything in the first two gets added to the queue only if --doFits is specified
    #    so that the 


    # Step 1 - open the json config file
    with open(self.args.config) as json_file:    
        cfg = json.load(json_file)
    # to do - have to handle the case where it doesn't exist
    points = []; blacklisted_points = []
    for igrid in cfg['grids']:
      assert(len(igrid) == 3)
      if igrid[2]=='' : points.extend(itertools.product(utils.split_vals(igrid[0]), utils.split_vals(igrid[1])))
      else : blacklisted_points.extend(itertools.product(utils.split_vals(igrid[0]), utils.split_vals(igrid[1]), utils.split_vals(igrid[2])))
    POIs = cfg['POIs']

    file_dict = { }
    for p in points:
      file_dict[p] = []

    for f in glob.glob('higgsCombine.%s.*.%s.*.Asymptotic.mH*.root' % (POIs[0], POIs[1])):
      # print f
      rgx = re.compile('higgsCombine\.%s\.(?P<p1>.*)\.%s\.(?P<p2>.*)\.Asymptotic\.mH.*\.root' % (POIs[0], POIs[1]))
      matches = rgx.search(f)
      p = (matches.group('p1'), matches.group('p2'))
      if p in file_dict:
        file_dict[p].append(f)

    for key,val in file_dict.iteritems():
      name = '%s.%s.%s.%s' % (POIs[0], key[0], POIs[1], key[1])
      print '>> Point %s' % name
      if len(val) == 0:
        print 'Going to run limit for point %s' % (key,)
        point_args = '-n .%s --setPhysicsModelParameters %s=%s,%s=%s --freezeNuisances %s,%s' % (name, POIs[0], key[0], POIs[1], key[1], POIs[0], POIs[1])
        cmd = ' '.join(['combine -M Asymptotic', cfg['opts'], point_args] + self.passthru)
        self.job_queue.append(cmd)

    bail_out = len(self.job_queue) > 0
    self.flush_queue()

    if bail_out: 
        print ">> New jobs were created / run in this cycle, run the script again to collect the output"
        sys.exit(0)

    xvals = []
    yvals = []
    zvals_m2s = []; zvals_m1s = []; zvals_exp = []; zvals_p1s = []; zvals_p2s = []; zvals_obs = []
    for key,val in file_dict.iteritems():
      for filename in val:
        fin = ROOT.TFile(filename)
        if fin.IsZombie(): continue
        tree = fin.Get('limit')
        for evt in tree:
          if abs(evt.quantileExpected+1)<0.01:
            xvals.append(float(key[0]))
            yvals.append(float(key[1]))
            #print 'At point %s have observed CLs = %f' % (key, evt.limit)
            zvals_obs.append(float(evt.limit))
          if abs(evt.quantileExpected-0.025)<0.01:
            #print 'At point %s have -2sigma CLs = %f' % (key, evt.limit)
            zvals_m2s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.16)<0.01:
            #print 'At point %s have -1sigma CLs = %f' % (key, evt.limit)
            zvals_m1s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.5)<0.01:
            #print 'At point %s have expected CLs = %f' % (key, evt.limit)
            zvals_exp.append(float(evt.limit))
          if abs(evt.quantileExpected-0.84)<0.01:
            #print 'At point %s have +1sigma CLs = %f' % (key, evt.limit)
            zvals_p1s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.975)<0.01:
            #print 'At point %s have +2sigma CLs = %f' % (key, evt.limit)
            zvals_p2s.append(float(evt.limit))
    for POI1, POI2, CLs in blacklisted_points:
      xvals.append(float(POI1))
      yvals.append(float(POI2))
      zvals_m2s.append(float(CLs))
      zvals_m1s.append(float(CLs))
      zvals_exp.append(float(CLs))
      zvals_p1s.append(float(CLs))
      zvals_p2s.append(float(CLs))
      zvals_obs.append(float(CLs))
    graph_m2s = ROOT.TGraph2D(len(zvals_m2s), array('d', xvals), array('d', yvals), array('d', zvals_m2s))
    graph_m1s = ROOT.TGraph2D(len(zvals_m1s), array('d', xvals), array('d', yvals), array('d', zvals_m1s))
    graph_exp = ROOT.TGraph2D(len(zvals_exp), array('d', xvals), array('d', yvals), array('d', zvals_exp))
    graph_p1s = ROOT.TGraph2D(len(zvals_p1s), array('d', xvals), array('d', yvals), array('d', zvals_p1s))
    graph_p2s = ROOT.TGraph2D(len(zvals_p2s), array('d', xvals), array('d', yvals), array('d', zvals_p2s))
    graph_obs = ROOT.TGraph2D(len(zvals_obs), array('d', xvals), array('d', yvals), array('d', zvals_obs))
    #h_bins = cfg['hist_binning']
    #hist = ROOT.TH2F('h_observed', '', h_bins[0], h_bins[1], h_bins[2], h_bins[3], h_bins[4], h_bins[5])
    #for i in xrange(1, hist.GetNbinsX()+1):
    #  for j in xrange(1, hist.GetNbinsY()+1):
    #    hist.SetBinContent(i, j, graph.Interpolate(hist.GetXaxis().GetBinCenter(i), hist.GetYaxis().GetBinCenter(j)))
    fout = ROOT.TFile('asymptotic_grid.root', 'RECREATE')
    fout.WriteTObject(graph_m2s, 'minus2sigma')
    fout.WriteTObject(graph_m1s, 'minus1sigma')
    fout.WriteTObject(graph_exp, 'expected')
    fout.WriteTObject(graph_p1s, 'plus1sigma')
    fout.WriteTObject(graph_p2s, 'plus2sigma')
    fout.WriteTObject(graph_obs, 'observed')
    #fout.WriteTObject(hist)
    fout.Close()
    # Next step: open output files
    # Fill TGraph2D with CLs, CLs+b


class Limit1D(CombineToolBase):
  description = 'Calculate asymptotic limits on parameter grids' 
  requires_root = True

  def __init__(self):
    CombineToolBase.__init__(self)

  def attach_intercept_args(self, group):
    CombineToolBase.attach_intercept_args(self, group)

  def attach_args(self, group):
    CombineToolBase.attach_args(self, group)
    group.add_argument('config', help='json config file')

  def run_method(self):
    # Step 1 - open the json config file
    with open(self.args.config) as json_file:    
        cfg = json.load(json_file)
    # to do - have to handle the case where it doesn't exist
    points = []; blacklisted_points = []
    for igrid in cfg['grids']:
      assert(len(igrid) == 1)
      points.extend(itertools.product(utils.split_vals(igrid[0])))
    POIs = cfg['POIs']

    file_dict = { }
    for p in points:
      file_dict[p] = []

    for f in glob.glob('higgsCombine.%s.*.Asymptotic.mH*.root' % (POIs[0])):
      rgx = re.compile('higgsCombine\.%s\.(?P<p1>.*)\.Asymptotic\.mH.*\.root' % (POIs[0]))
      matches = rgx.search(f)
      p = (matches.group('p1'),)
      if p in file_dict:
        file_dict[p].append(f)

    for key,val in file_dict.iteritems():
      name = '%s.%s' % (POIs[0], key[0])
      print '>> Point %s' % name
      if len(val) == 0:
        print 'Going to run limit for point %s' % (key)
        r_process = cfg['r']
        point_args = ''
        if r_process[0] == "r_ggA" :
          point_args = '-n .%s --setPhysicsModelParameters %s=%s --setPhysicsModelParameterRanges %s=0,%s --freezeNuisances %s' % (name, POIs[0], key[0], r_process[0], str(bounds["ggH-bbH",key[0]][0]), POIs[0])
        elif r_process[0] == "r_bbA" :
          point_args = '-n .%s --setPhysicsModelParameters %s=%s --setPhysicsModelParameterRanges %s=0,%s --freezeNuisances %s' % (name, POIs[0], key[0], r_process[0], str(bounds["ggH-bbH",key[0]][1]), POIs[0])
        cmd = ' '.join(['combine -M Asymptotic', cfg['opts'], point_args] + self.passthru)
        self.job_queue.append(cmd)

    bail_out = len(self.job_queue) > 0
    self.flush_queue()

    if bail_out: 
        print ">> New jobs were created / run in this cycle, run the script again to collect the output"
        sys.exit(0)

    xvals = []
    zvals_m2s = []; zvals_m1s = []; zvals_exp = []; zvals_p1s = []; zvals_p2s = []; zvals_obs = []
    for key,val in file_dict.iteritems():
      for filename in val:
        fin = ROOT.TFile(filename)
        if fin.IsZombie(): continue
        tree = fin.Get('limit')
        for evt in tree:
          if abs(evt.quantileExpected+1)<0.01:
            xvals.append(float(key[0]))
            #print 'At point %s have observed CLs = %f' % (key, evt.limit)
            zvals_obs.append(float(evt.limit))
          if abs(evt.quantileExpected-0.025)<0.01:
            #print 'At point %s have -2sigma CLs = %f' % (key, evt.limit)
            zvals_m2s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.16)<0.01:
            #print 'At point %s have -1sigma CLs = %f' % (key, evt.limit)
            zvals_m1s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.5)<0.01:
            #print 'At point %s have expected CLs = %f' % (key, evt.limit)
            zvals_exp.append(float(evt.limit))
          if abs(evt.quantileExpected-0.84)<0.01:
            #print 'At point %s have +1sigma CLs = %f' % (key, evt.limit)
            zvals_p1s.append(float(evt.limit))
          if abs(evt.quantileExpected-0.975)<0.01:
            #print 'At point %s have +2sigma CLs = %f' % (key, evt.limit)
            zvals_p2s.append(float(evt.limit))
    graph_m2s = ROOT.TGraph(len(zvals_m2s), array('d', xvals), array('d', zvals_m2s))
    graph_m1s = ROOT.TGraph(len(zvals_m1s), array('d', xvals), array('d', zvals_m1s))
    graph_exp = ROOT.TGraph(len(zvals_exp), array('d', xvals), array('d', zvals_exp))
    graph_p1s = ROOT.TGraph(len(zvals_p1s), array('d', xvals), array('d', zvals_p1s))
    graph_p2s = ROOT.TGraph(len(zvals_p2s), array('d', xvals), array('d', zvals_p2s))
    graph_obs = ROOT.TGraph(len(zvals_obs), array('d', xvals), array('d', zvals_obs))
    #h_bins = cfg['hist_binning']
    #hist = ROOT.TH2F('h_observed', '', h_bins[0], h_bins[1], h_bins[2], h_bins[3], h_bins[4], h_bins[5])
    #for i in xrange(1, hist.GetNbinsX()+1):
    #  for j in xrange(1, hist.GetNbinsY()+1):
    #    hist.SetBinContent(i, j, graph.Interpolate(hist.GetXaxis().GetBinCenter(i), hist.GetYaxis().GetBinCenter(j)))
    fout = ROOT.TFile('asymptotic_1Dlimit.root', 'RECREATE')
    fout.WriteTObject(graph_m2s, 'minus2sigma')
    fout.WriteTObject(graph_m1s, 'minus1sigma')
    fout.WriteTObject(graph_exp, 'expected')
    fout.WriteTObject(graph_p1s, 'plus1sigma')
    fout.WriteTObject(graph_p2s, 'plus2sigma')
    fout.WriteTObject(graph_obs, 'observed')
    #fout.WriteTObject(hist)
    fout.Close()
    # Next step: open output files
    # Fill TGraph2D with CLs, CLs+b
