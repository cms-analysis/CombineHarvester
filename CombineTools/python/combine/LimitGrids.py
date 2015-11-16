import ROOT
import json
import itertools
import glob
import sys
import re
from math import floor
from array import array

import CombineHarvester.CombineTools.combine.utils as utils
from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
from CombineHarvester.CombineTools.mssm_multidim_fit_boundaries import mssm_multidim_fit_boundaries as bounds
import Tools.Plotting.plotting as plot

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

class HybridNewGrid(CombineToolBase):
  description = 'Calculate toy-based limits on parameter grids' 
  requires_root = True

  def __init__(self):
    CombineToolBase.__init__(self)

  def attach_intercept_args(self, group):
    CombineToolBase.attach_intercept_args(self, group)

  def attach_args(self, group):
    CombineToolBase.attach_args(self, group)
    group.add_argument('config', help='json config file')
    group.add_argument('--cycles', default=0, type=int, help='Number of job cycles to create per point')

  def GetCombinedHypoTest(self, files):
    if len(files) == 0: return None
    results = []
    for file in files:
      f = ROOT.TFile(file)
      ROOT.gDirectory.cd('toys')
      for key in ROOT.gDirectory.GetListOfKeys():
        if ROOT.gROOT.GetClass(key.GetClassName()).InheritsFrom(ROOT.RooStats.HypoTestResult.Class()):
          results.append(ROOT.gDirectory.Get(key.GetName()))
      f.Close()
    if (len(results)) > 1:
      for r in results[1:]:
        results[0].Append(r)
    return results[0]

  def ValidateHypoTest(self, result, min_toys=500, max_toys=5000, contours=['obs', 'exp0', 'exp+1', 'exp-1', 'exp+2', 'exp-2'], signif=5.0, cl=0.95):
    # 1st test - do we have any HypoTestResult at all?
    if result is None:
      print '>> No toys completed!'
      return False
    # 2nd test - have we thrown the minimum number of toys?
    ntoys = min(result.GetNullDistribution().GetSize(), result.GetAltDistribution().GetSize())
    if ntoys < min_toys:
      print '>> Only %i/%i toys completed!' % (ntoys, min_toys)
      return False
    # 3rd test - have we thrown the maximum (or more) toys?
    if ntoys >= max_toys:
      print '>> More than max toys %i/%i toys completed!' % (ntoys, min_toys)
      return True
    # 3rd test - are we  > X sigma away from the exclusion CLs? This must be true for all the
    # contours we're interested in
    btoys = [x for x in result.GetNullDistribution().GetSamplingDistribution()]
    btoys.sort()
    crossing = 1 - cl
    signif_results = {}
    # save the real observed test stat, we'll change it in this
    # loop to get the expected but we'll want to restore it at the end
    testStatObs = result.GetTestStatisticData()
    allGood = True
    for contour in contours:
      signif_results[contour] = True
      if 'exp' in contour:
        quantile = ROOT.Math.normal_cdf(float(contour.replace('exp', '')))
        print '>> Checking the %s contour at quantile=%f' % (contour, quantile)
        testStat = btoys[int(min(floor(quantile * len(btoys) +0.5), len(btoys)))]
        print '>> Test statistic for %f quantile: %f' % (quantile, testStat)
        result.SetTestStatisticData(testStat)
      result.Print("v")
      CLs = result.CLs()
      CLsErr = result.CLsError()
      if CLsErr == 0.:
        print '>> CLsErr is zero'
      else:
        dist = abs(CLs - crossing) / CLsErr
        if dist < signif:
          print '>> [%s] Only reached %.1f sigma signifance from chosen CL (target %.1f)' % (contour, dist, signif)
          signif_results[contour] = False
      result.SetTestStatisticData(testStatObs)
    print signif_results
    for (key, val) in signif_results.iteritems():
      if val == False: return False
    print 'POINT IS OK AFTER %i TOYS' % ntoys
    return True

  def PlotTest(self, result, name, one_sided=False, model_desc=''):
    plot.ModTDRStyle()
    canv = ROOT.TCanvas(name, name)
    pad = ROOT.TPad('pad', 'pad', 0., 0., 1., 1.)
    pad.Draw()
    pad.cd()
    null_vals = [x * 2. for x in result.GetNullDistribution().GetSamplingDistribution()]
    alt_vals = [x * 2. for x in result.GetAltDistribution().GetSamplingDistribution()]
    min_val = min(min(alt_vals), min(null_vals))
    max_val = max(max(alt_vals), max(null_vals))
    min_plot_range = min_val - 0.05 * (max_val - min_val)
    if one_sided:
      min_plot_range = 0.
      pad.SetLogy(True)
    max_plot_range = max_val + 0.05 * (max_val - min_val)
    hist_null = ROOT.TH1F('null', 'null', 40, min_plot_range, max_plot_range)
    hist_alt = ROOT.TH1F('alt', 'alt', 40, min_plot_range, max_plot_range)
    for val in null_vals: hist_null.Fill(val)
    for val in alt_vals: hist_alt.Fill(val)
    hist_alt.SetLineColor(ROOT.TColor.GetColor(4, 4, 255))
    hist_alt.SetFillColorAlpha(ROOT.TColor.GetColor(4, 4, 255), 0.4)
    hist_alt.GetXaxis().SetTitle('-2 #times ln(Q_{TEV})')
    hist_alt.GetYaxis().SetTitle('Pseudo-experiments')
    hist_alt.Draw()
    hist_alt.SetMaximum(hist_alt.GetMaximum() * 1.5)
    hist_null.SetLineColor(ROOT.TColor.GetColor(252, 86, 11))
    hist_null.SetFillColorAlpha(ROOT.TColor.GetColor(254, 195, 40), 0.4)
    hist_null.Draw('SAME')
    val_obs = result.GetTestStatisticData() * 2.
    obs = ROOT.TArrow(val_obs, 0, val_obs, hist_alt.GetMaximum() * 0.3, 0.05 , '<-|')
    obs.SetLineColor(ROOT.kRed)
    obs.SetLineWidth(3)
    obs.Draw()
    leg = plot.PositionedLegend(0.22, 0.2, 3, 0.02)
    leg.AddEntry(hist_null, "B", "F")
    leg.AddEntry(hist_alt, "S+B", "F")
    leg.AddEntry(obs, "Observed", "L")
    leg.Draw()
    plot.DrawCMSLogo(pad, "CMS", "Internal", 0, 0.15, 0.035, 1.2)
    pt_l = ROOT.TPaveText(0.23, 0.75, 0.33, 0.9, 'NDCNB')
    if model_desc: pt_l.AddText('Model:')
    pt_l.AddText('Toys:')
    pt_l.AddText('CLs+b:')
    pt_l.AddText('CLb:')
    pt_l.AddText('CLs:')
    pt_l.SetTextAlign(11)
    pt_l.SetTextFont(62)
    pt_l.Draw()
    pt_r = ROOT.TPaveText(0.33, 0.75, 0.63, 0.9, 'NDCNB')
    if model_desc: pt_r.AddText(model_desc)
    pt_r.AddText('%i (B) + %i (S+B)' % (result.GetNullDistribution().GetSize(), result.GetAltDistribution().GetSize()))
    pt_r.AddText('%.3f #pm %.3f' % (result.CLsplusb(), result.CLsplusbError()))
    pt_r.AddText('%.3f #pm %.3f' % (result.CLb(), result.CLbError()))
    pt_r.AddText('%.3f #pm %.3f' % (result.CLs(), result.CLsError()))
    pt_r.SetTextAlign(11)
    pt_r.SetTextFont(42)
    pt_r.Draw()
    canv.SaveAs('.pdf')

  def run_method(self):
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

    for f in glob.glob('higgsCombine.%s.*.%s.*.HybridNew.mH*.root' % (POIs[0], POIs[1])):
      # print f
      rgx = re.compile('higgsCombine\.%s\.(?P<p1>.*)\.%s\.(?P<p2>.*)\.HybridNew\.mH.*\.(?P<toy>.*)\.root' % (POIs[0], POIs[1]))
      matches = rgx.search(f)
      p = (matches.group('p1'), matches.group('p2'))
      if p in file_dict:
        file_dict[p].append((f, int(matches.group('toy'))))

    for key,val in file_dict.iteritems():
      name = '%s.%s.%s.%s' % (POIs[0], key[0], POIs[1], key[1])
      print '>> Point %s' % name
      res = self.GetCombinedHypoTest([x[0] for x in val])
      ok = self.ValidateHypoTest(res)
      if res is not None and True: self.PlotTest(res, 'plot_'+name, False, 'm_{H}^{mod+} [m_{A} = %.1f, tan#beta = %.1f]' % (float(key[0]), float(key[1])))

      if not ok:
        print 'Going to generate %i job(s) for point %s' % (self.args.cycles, key)
        done_cycles = [x[1] for x in val]
        print 'Done cycles: ' + ','.join(str(x) for x in done_cycles)
        new_idx = max(done_cycles)+1 if len(done_cycles) > 0 else 1
        new_cycles = range(new_idx, new_idx+self.args.cycles)
        print 'New cycles: ' + ','.join(str(x) for x in new_cycles)
        point_args = '-n .%s --setPhysicsModelParameters %s=%s,%s=%s --freezeNuisances %s,%s' % (name, POIs[0], key[0], POIs[1], key[1], POIs[0], POIs[1])
        for idx in new_cycles:
          cmd = ' '.join(['combine -M HybridNew', cfg['opts'], point_args, '-T %i' % cfg['toys_per_cycle'], '-s %i' % idx])
          self.job_queue.append(cmd)

    # bail_out = len(self.job_queue) > 0
    self.flush_queue()

    # if bail_out: 
    #     print ">> New jobs were created / run in this cycle, run the script again to collect the output"
    #     sys.exit(0)

    # xvals = []
    # yvals = []
    # zvals_m2s = []; zvals_m1s = []; zvals_exp = []; zvals_p1s = []; zvals_p2s = []; zvals_obs = []
    # for key,val in file_dict.iteritems():
    #   for filename in val:
    #     fin = ROOT.TFile(filename)
    #     if fin.IsZombie(): continue
    #     tree = fin.Get('limit')
    #     for evt in tree:
    #       if abs(evt.quantileExpected+1)<0.01:
    #         xvals.append(float(key[0]))
    #         yvals.append(float(key[1]))
    #         #print 'At point %s have observed CLs = %f' % (key, evt.limit)
    #         zvals_obs.append(float(evt.limit))
    #       if abs(evt.quantileExpected-0.025)<0.01:
    #         #print 'At point %s have -2sigma CLs = %f' % (key, evt.limit)
    #         zvals_m2s.append(float(evt.limit))
    #       if abs(evt.quantileExpected-0.16)<0.01:
    #         #print 'At point %s have -1sigma CLs = %f' % (key, evt.limit)
    #         zvals_m1s.append(float(evt.limit))
    #       if abs(evt.quantileExpected-0.5)<0.01:
    #         #print 'At point %s have expected CLs = %f' % (key, evt.limit)
    #         zvals_exp.append(float(evt.limit))
    #       if abs(evt.quantileExpected-0.84)<0.01:
    #         #print 'At point %s have +1sigma CLs = %f' % (key, evt.limit)
    #         zvals_p1s.append(float(evt.limit))
    #       if abs(evt.quantileExpected-0.975)<0.01:
    #         #print 'At point %s have +2sigma CLs = %f' % (key, evt.limit)
    #         zvals_p2s.append(float(evt.limit))
    # for POI1, POI2, CLs in blacklisted_points:
    #   xvals.append(float(POI1))
    #   yvals.append(float(POI2))
    #   zvals_m2s.append(float(CLs))
    #   zvals_m1s.append(float(CLs))
    #   zvals_exp.append(float(CLs))
    #   zvals_p1s.append(float(CLs))
    #   zvals_p2s.append(float(CLs))
    #   zvals_obs.append(float(CLs))
    # graph_m2s = ROOT.TGraph2D(len(zvals_m2s), array('d', xvals), array('d', yvals), array('d', zvals_m2s))
    # graph_m1s = ROOT.TGraph2D(len(zvals_m1s), array('d', xvals), array('d', yvals), array('d', zvals_m1s))
    # graph_exp = ROOT.TGraph2D(len(zvals_exp), array('d', xvals), array('d', yvals), array('d', zvals_exp))
    # graph_p1s = ROOT.TGraph2D(len(zvals_p1s), array('d', xvals), array('d', yvals), array('d', zvals_p1s))
    # graph_p2s = ROOT.TGraph2D(len(zvals_p2s), array('d', xvals), array('d', yvals), array('d', zvals_p2s))
    # graph_obs = ROOT.TGraph2D(len(zvals_obs), array('d', xvals), array('d', yvals), array('d', zvals_obs))
    # #h_bins = cfg['hist_binning']
    # #hist = ROOT.TH2F('h_observed', '', h_bins[0], h_bins[1], h_bins[2], h_bins[3], h_bins[4], h_bins[5])
    # #for i in xrange(1, hist.GetNbinsX()+1):
    # #  for j in xrange(1, hist.GetNbinsY()+1):
    # #    hist.SetBinContent(i, j, graph.Interpolate(hist.GetXaxis().GetBinCenter(i), hist.GetYaxis().GetBinCenter(j)))
    # fout = ROOT.TFile('asymptotic_grid.root', 'RECREATE')
    # fout.WriteTObject(graph_m2s, 'minus2sigma')
    # fout.WriteTObject(graph_m1s, 'minus1sigma')
    # fout.WriteTObject(graph_exp, 'expected')
    # fout.WriteTObject(graph_p1s, 'plus1sigma')
    # fout.WriteTObject(graph_p2s, 'plus2sigma')
    # fout.WriteTObject(graph_obs, 'observed')
    # #fout.WriteTObject(hist)
    # fout.Close()
    # # Next step: open output files
    # # Fill TGraph2D with CLs, CLs+b


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
