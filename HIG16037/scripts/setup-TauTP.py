#!/usr/bin/env python
import argparse
import CombineHarvester.CombineTools.ch as ch


parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='Input root file')
parser.add_argument('--dir', '-d', help='directory name, excluding _pass and _fail')
parser.add_argument('--prefix', '-p', default='', help='prefix to add to the card names')
parser.add_argument('--output', '-o', default='.', help='Directory where the output cards should be written')
args = parser.parse_args()

cb = ch.CombineHarvester()

procs = {
  'sig': ['ZTT'],
  'bkg': ['ZL', 'ZJ', 'W', 'QCD', 'TT', 'VV']
}

cats = [(0, 'fail'), (1, 'pass')]

cb.AddObservations(['*'], ['tauTP'], ["13TeV"], ['mt'], cats)
cb.AddProcesses(['*'], ['tauTP'], ["13TeV"], ['mt'], procs['bkg'], cats, False)
cb.AddProcesses(['*'], ['tauTP'], ["13TeV"], ['mt'], procs['sig'], cats, True)

print '>> Adding systematic uncertainties...'
# cb.SetFlag('filters-use-regex', True)
cb.cp().AddSyst(
    cb, 'CMS_scale_t_$PROCESS_$BIN', 'shape', ch.SystMap()(1.00))
cb.syst_name(['blah'])

cb.cp().process(['QCD', 'TT', 'VV']).AddSyst(
    cb, 'norm_$PROCESS_$BIN', 'lnN', ch.SystMap()(1.10))

cb.cp().process(['ZL', 'ZJ']).AddSyst(
    cb, 'norm_$PROCESS_$BIN', 'lnN', ch.SystMap()(1.20))

cb.cp().process(['ZTT', 'ZL', 'ZJ', 'W', 'TT', 'VV']).AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap()(1.02))

cb.cp().process(['ZTT', 'ZL', 'ZJ', 'W', 'TT', 'VV']).AddSyst(
    cb, 'lumi_13TeV_2016', 'lnN', ch.SystMap()(1.062))

cb.cp().process(['ZTT', 'ZL', 'ZJ']).AddSyst(
    cb, 'CMS_htt_zjXsec_13TeV', 'lnN', ch.SystMap()(1.05))

cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_htt_tjXsec_13TeV', 'lnN', ch.SystMap()(1.06))

cb.cp().process(['W']).AddSyst(
    cb, 'CMS_htt_wjXsec_13TeV', 'lnN', ch.SystMap()(1.10))

cb.cp().AddSyst(
    cb, 'CMS_scale_t', 'shape', ch.SystMap()(1.00))

print '>> Extracting histograms from input root files...'
cb.cp().ExtractShapes(
    args.input, 'analysis/%s_$BIN/$PROCESS' % args.dir, 'analysis/%s_$BIN/$PROCESS_$SYSTEMATIC' % args.dir)

cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(lambda s: s.set_name('CMS_scale_t_%s_%s' % (s.process(), s.bin())))


print '>> Generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.0)
bbb.SetMergeThreshold(0.2)
bbb.SetFixNorm(False)
bbb.MergeAndAdd(cb, cb)


# Now we'll do a trick and scale the ZTT to the pass+fail rate in both categories
yield_fail = cb.cp().bin_id([0]).process(['ZTT']).GetRate()
yield_pass = cb.cp().bin_id([1]).process(['ZTT']).GetRate()

yield_W_fail = cb.cp().bin_id([0]).process(['W']).GetRate()
yield_W_pass = cb.cp().bin_id([1]).process(['W']).GetRate()

yield_QCD = cb.cp().bin_id([1]).process(['QCD']).GetRate()

eff_initial = yield_pass / (yield_pass + yield_fail)
eff_W_initial = yield_W_pass / (yield_W_pass + yield_W_fail)

cb.cp().process(['ZTT']).ForEachProc(lambda p: p.set_rate(yield_pass + yield_fail))
cb.cp().process(['W']).ForEachProc(lambda p: p.set_rate(yield_W_pass + yield_W_fail))

print 'ZTT: %g %g %g' % (yield_pass, yield_fail, eff_initial)
print 'W/ZTT: %g %g' % (yield_W_pass, (yield_W_pass/yield_pass))
print 'QCD/ZTT: %g %g' % (yield_QCD, (yield_QCD/yield_pass))

cb.cp().process(['ZTT']).bin_id([1]).AddSyst(
    cb, 'effsf', 'rateParam', ch.SystMap()(1.0))

cb.cp().process(['W']).bin_id([1]).AddSyst(
    cb, 'fakesf', 'rateParam', ch.SystMap()(1.0))

cb.cp().process(['ZTT', 'ZL', 'ZJ']).AddSyst(
    cb, 'DY_XS', 'rateParam', ch.SystMap()(1.0))

# cb.cp().process(['ZL']).AddSyst(
#     cb, 'muon_fr', 'rateParam', ch.SystMap()(1.0))

cb.GetParameter('effsf').set_val(1.0)
cb.GetParameter('effsf').set_range(0.5, 1.5)

cb.GetParameter('fakesf').set_val(1.0)
cb.GetParameter('fakesf').set_range(0.5, 2.5)

# cb.GetParameter('muon_fr').set_val(1.5)
# cb.GetParameter('muon_fr').set_range(0.5, 2.5)

cb.cp().process(['ZTT']).bin_id([1]).AddSyst(
    cb, 'pass', 'rateParam', ch.SystMap()(('(%g)' % eff_initial, 'effsf')))

cb.cp().process(['ZTT']).bin_id([0]).AddSyst(
    cb, 'fail', 'rateParam', ch.SystMap()(('(1-@0*%g)' % eff_initial, 'effsf')))

cb.cp().process(['W']).bin_id([1]).AddSyst(
    cb, 'passW', 'rateParam', ch.SystMap()(('(%g)' % eff_W_initial, 'fakesf')))

cb.cp().process(['W']).bin_id([0]).AddSyst(
    cb, 'failW', 'rateParam', ch.SystMap()(('(1-@0*%g)' % eff_W_initial, 'fakesf')))


# print '>> Setting standardised bin names...'
# ch.SetStandardBinNames(cb)
# cb.PrintAll()

writer = ch.CardWriter('$TAG/$ANALYSIS_%s.txt' % (args.prefix + args.dir),
                       '$TAG/$ANALYSIS_%s.input.root'  % (args.prefix + args.dir))
writer.SetWildcardMasses([])
writer.SetVerbosity(1)
writer.WriteCards(args.output, cb)

print '>> Done!'