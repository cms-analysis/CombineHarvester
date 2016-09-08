#!/usr/bin/env python
import argparse
import CombineHarvester.CombineTools.ch as ch


parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='Input root file')
parser.add_argument('--dir', '-d', help='directory name, excluding _pass and _fail')
parser.add_argument('--output', '-o', default='.', help='Directory where the output cards should be written')
args = parser.parse_args()

cb = ch.CombineHarvester()

procs = {
  'sig': ['ZTT'],
  'bkg': ['ZL', 'ZJ', 'W', 'QCD', 'TT', 'VV']
}

cats = [(0, '%s_fail' % args.dir), (1, '%s_pass' % args.dir)]

cb.AddObservations(['*'], ['tauTP'], ["13TeV"], ['mt'], cats)
cb.AddProcesses(['*'], ['tauTP'], ["13TeV"], ['mt'], procs['bkg'], cats, False)
cb.AddProcesses(['*'], ['tauTP'], ["13TeV"], ['mt'], procs['sig'], cats, True)

print '>> Adding systematic uncertainties...'
# cb.SetFlag('filters-use-regex', True)
cb.cp().AddSyst(
    cb, 'CMS_scale_t_$PROCESS_$BINID', 'shape', ch.SystMap()(1.00))
cb.syst_name(['blah'])

cb.cp().backgrounds().AddSyst(
    cb, 'norm_$PROCESS_$BINID', 'lnN', ch.SystMap()(1.10))

cb.cp().process(['ZTT']).AddSyst(
    cb, 'norm_$PROCESS', 'lnN', ch.SystMap()(1.05))

cb.cp().AddSyst(
    cb, 'CMS_scale_t', 'shape', ch.SystMap()(1.00))

print '>> Extracting histograms from input root files...'
cb.cp().ExtractShapes(
    args.input, 'analysis/$BIN/$PROCESS', 'analysis/$BIN/$PROCESS_$SYSTEMATIC')

cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(lambda s: s.set_name('CMS_scale_t_%s_%i' % (s.process(), s.bin_id())))

# Now we'll do a trick and scale the ZTT to the pass+fail rate in both categories
yield_fail = cb.cp().bin_id([0]).process(['ZTT']).GetRate()
yield_pass = cb.cp().bin_id([1]).process(['ZTT']).GetRate()

yield_W = cb.cp().bin_id([1]).process(['W']).GetRate()
yield_QCD = cb.cp().bin_id([1]).process(['QCD']).GetRate()

eff_initial = yield_pass / (yield_pass + yield_fail)

cb.cp().process(['ZTT']).ForEachProc(lambda p: p.set_rate(yield_pass + yield_fail))

print 'ZTT: %g %g %g' % (yield_pass, yield_fail, eff_initial)
print 'W/ZTT: %g %g' % (yield_W, (yield_W/yield_pass))
print 'QCD/ZTT: %g %g' % (yield_QCD, (yield_QCD/yield_pass))

cb.cp().process(['ZTT']).bin_id([1]).AddSyst(
    cb, 'effsf', 'rateParam', ch.SystMap()(eff_initial))

cb.GetParameter('effsf').set_val(1.0)
cb.GetParameter('effsf').set_range(0.5, 1.5)

cb.cp().process(['ZTT']).bin_id([1]).AddSyst(
    cb, 'pass', 'rateParam', ch.SystMap()(('(%g)' % eff_initial, 'effsf')))

cb.cp().process(['ZTT']).bin_id([0]).AddSyst(
    cb, 'fail', 'rateParam', ch.SystMap()(('(1-@0*%g)' % eff_initial, 'effsf')))


print '>> Generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.0)
bbb.SetMergeThreshold(0.2)
bbb.SetFixNorm(False)
bbb.MergeAndAdd(cb, cb)


# print '>> Setting standardised bin names...'
# ch.SetStandardBinNames(cb)
# cb.PrintAll()

writer = ch.CardWriter('$TAG/$ANALYSIS_%s.txt' % args.dir,
                       '$TAG/$ANALYSIS_%s.input.root' % args.dir)
writer.SetWildcardMasses([])
writer.SetVerbosity(1)
writer.WriteCards(args.output, cb)

print '>> Done!'