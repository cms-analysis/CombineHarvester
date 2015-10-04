import ROOT
import json
import itertools
import glob
import sys
import re
from array import array

import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase

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
    points = []
    for igrid in cfg['grids']:
      assert(len(igrid) == 2)
      points.extend(itertools.product(utils.split_vals(igrid[0]), utils.split_vals(igrid[1])))

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
    zvals = []
    for key,val in file_dict.iteritems():
      for filename in val:
        fin = ROOT.TFile(filename)
        if fin.IsZombie(): continue
        tree = fin.Get('limit')
        for evt in tree:
          if evt.quantileExpected == -1:
            print 'At point %s have observed CLs = %f' % (key, evt.limit)
            xvals.append(float(key[0]))
            yvals.append(float(key[1]))
            zvals.append(float(evt.limit))
    graph = ROOT.TGraph2D(len(zvals), array('d', xvals), array('d', yvals), array('d', zvals))
    h_bins = cfg['hist_binning']
    hist = ROOT.TH2F('h_observed', '', h_bins[0], h_bins[1], h_bins[2], h_bins[3], h_bins[4], h_bins[5])
    for i in xrange(1, hist.GetNbinsX()+1):
      for j in xrange(1, hist.GetNbinsY()+1):
        hist.SetBinContent(i, j, graph.Interpolate(hist.GetXaxis().GetBinCenter(i), hist.GetYaxis().GetBinCenter(j)))
    fout = ROOT.TFile('asymptotic_grid.root', 'RECREATE')
    fout.WriteTObject(graph, 'observed')
    fout.WriteTObject(hist)
    fout.Close()
    # Next step: open output files
    # Fill TGraph2D with CLs, CLs+b
