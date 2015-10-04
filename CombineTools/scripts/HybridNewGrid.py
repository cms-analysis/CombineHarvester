#!/usr/bin/env python

import argparse
import os
import re
import sys
import json
import math
import itertools
import stat
import ROOT
import glob
import plotting

DRY_RUN = False

def split_vals(vals):
  res = set()
  first = vals.split(',')
  for f in first:
    second = re.split('[:|]', f)
    print second
    if len(second) == 1: res.add(second[0])
    if len(second) == 3:
      x1 = float(second[0])
      ndigs = '0'
      split_step = second[2].split('.')
      if len(split_step) == 2:
        ndigs = len(split_step[1])
      fmt = '%.'+str(ndigs)+'f'
      while x1 < float(second[1]) + 0.001:
        res.add(fmt % x1)
        x1 += float(second[2])
  return sorted([x for x in res], key = lambda x : float(x))

def run(command):
  print command
  if not DRY_RUN: return os.system(command)

def GetCombinedHypoTest(files):
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


def ValidateHypoTest(result, min_toys, contours, contour_min_signif, conf_level):
  # 1st test - do we have any HypoTestResult at all?
  if result is None:
    print 'No toys completed!'
    return False
  # 2nd test - have we thrown the minimum number of toys?
  ntoys = min(result.GetNullDistribution().GetSize(), result.GetAltDistribution().GetSize())
  if ntoys < min_toys:
    print 'Only %i/%i toys completed!'
    return False
  # 3rd test - are we  > X sigma away from the exclusion CLs? This must be true for all the
  # contours we're interested in
  # But first, if the CLs error is zero:
  # result.Print("v")
  CLs = result.CLs()
  CLsErr = result.CLsError()
  if CLsErr == 0.:
    print 'CLsErr is zero, no further toys required'
    return True
  crossing = 1 - conf_level
  dist = abs(CLs - crossing) / CLsErr
  if dist < contour_min_signif:
    print 'Only reached %.1f sigma signifance from chosen CL (target %.1f)' % (dist, contour_min_signif)
    result.Print("v")
    return False
  print 'POINT IS OK AFTER %i TOYS' % ntoys
  return True


def PlotTest(result, name, one_sided=False, model_desc=''):
  plotting.ModTDRStyle()
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
  hist_alt.GetXaxis().SetTitle('-2 #times ln(Q_{LHC})')
  hist_alt.GetYaxis().SetTitle('Pseudo-experiments')
  hist_alt.Draw()
  hist_null.SetLineColor(ROOT.TColor.GetColor(252, 86, 11))
  hist_null.SetFillColorAlpha(ROOT.TColor.GetColor(254, 195, 40), 0.4)
  hist_null.Draw('SAME')
  val_obs = result.GetTestStatisticData() * 2.
  obs = ROOT.TArrow(val_obs, 0, val_obs, hist_alt.GetMaximum() / 50., 0.05 , '<-|')
  obs.SetLineColor(ROOT.kRed)
  obs.SetLineWidth(3)
  obs.Draw()
  leg = plotting.PositionedLegend(0.22, 0.2, 3, 0.02)
  leg.AddEntry(hist_null, "B", "F")
  leg.AddEntry(hist_alt, "S+B", "F")
  leg.AddEntry(obs, "Observed", "L")
  leg.Draw()
  plotting.DrawCMSLogo(pad, "CMS", "Internal", 0, 0.045, 0.035, 1.2)
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


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

parser = argparse.ArgumentParser(prog='HybridNewGrid.py')
parser.add_argument('config', help="configuration json file")
parser.add_argument('--dry-run', action='store_true', help='Commands are echoed to the screen but not run')
parser.add_argument('--plots', action='store_true', help='Create plots of test statistic distributions')
parser.add_argument('--cycles', default=0, type=int, help='Number of job cycles to create per point')
(args, unknown) = parser.parse_known_args()

DRY_RUN = args.dry_run

with open(args.config) as json_file:    
    cfg = json.load(json_file)

points = []

for igrid in cfg['grids']:
  assert(len(igrid) == 2)
  points.extend(itertools.product(split_vals(igrid[0]), split_vals(igrid[1])))

POIs = cfg['POIs']

file_dict = { }

for p in points:
  file_dict[p] = []

for f in glob.glob('higgsCombine.%s.*.%s.*.HybridNew.mH*.*.root' % (POIs[0], POIs[1])):
  print f
  rgx = re.compile('higgsCombine\.%s\.(?P<p1>.*)\.%s\.(?P<p2>.*)\.HybridNew\.mH.*\.(?P<toy>.*)\.root' % (POIs[0], POIs[1]))
  matches = rgx.search(f)
  p = (matches.group('p1'), matches.group('p2'))
  if p in file_dict:
    file_dict[p].append((f, int(matches.group('toy'))))

for key,val in file_dict.iteritems():
  name = '%s.%s.%s.%s' % (POIs[0], key[0], POIs[1], key[1])
  print '>> Point %s' % name
  res = GetCombinedHypoTest([x[0] for x in val])
  ok = ValidateHypoTest(res, 500, ['obs'], 5, 0.95)
  if res is not None and args.plots: PlotTest(res, 'plot_'+name, True, 'm_{H}^{max} [m_{A} = %.1f, tan#beta = %.1f]' % (float(key[0]), float(key[1])))
  if not ok:
    print 'Going to generate %i jobs for point %s' % (args.cycles, key)
    done_cycles = [x[1] for x in val]
    print 'Done cycles: ' + ','.join(str(x) for x in done_cycles)
    new_idx = max(done_cycles)+1 if len(done_cycles) > 0 else 1
    new_cycles = range(new_idx, new_idx+args.cycles)
    print 'New cycles: ' + ','.join(str(x) for x in new_cycles)
    point_args = '-n .%s --setPhysicsModelParameters %s=%s,%s=%s --freezeNuisances %s,%s' % (name, POIs[0], key[0], POIs[1], key[1], POIs[0], POIs[1])
    for idx in new_cycles:
      cmd = ' '.join(['combine -M HybridNew', cfg['opts'], point_args, '-T %i' % cfg['toys_per_cycle'], '-s %i' % idx])
      run(cmd)




