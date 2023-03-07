#!/usr/bin/env python

from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch
cb = ch.CombineHarvester()
cb.SetFlag('check-negative-bins-on-import', 0)
cb.ParseDatacard("data/tutorials/htt/125/htt_tt.txt", mass="125")
# cb.cp().bin(['htt_tt_1_8TeV']).SetAutoMCStats(cb, -1.)
cb.WriteDatacard("test.txt", 'test.root')

# cb.FilterProcs(lambda x : x.process() in ['ggH', 'qqH'])
# cb.FilterAll(lambda y : y.mass() == '110')

# def SwitchToSignal(p):
#   if p.process() == 'ggH_hww125':
#     p.set_process('ggH_hww')
#     p.set_mass('125')
#     p.set_signal(True)

# cb.ForEachProc(SwitchToSignal)
# cb.VariableRebin([0., 50., 100., 150., 200., 250., 300.])


# The following is an example of duplicating existing objects and modifying
# them in the process. Here we clone all mH=125 signals, adding "_SM125" to
# the process name, switching it to background and giving it the generic mass
# label. This would let us create a datacard for doing a second Higgs search

# def Signal2Background(obj):
#   obj.set_process(obj.process() + "_SM125")
#   obj.set_signal(False)
#   obj.set_mass("*")

# ch.CloneProcs(cb.cp().signals().mass(['125']), cb, Signal2Background)

# cb.PrintAll()



# for b,e,p in Generate(cb, bin, era, process)

# meta = {
#   'analysis' : ['htt'],
#   'era'      : ['7TeV', '8TeV'],
#   'channel'  : ['et', 'mt'],
#   'bin'      : [
#     (0, 'category0'),
#     (1, 'category1')
#     ]
# }

# obs = {
#   'mass': ['*'],
# }

# bkg_procs = {
#   'mass'   : ['*'],
#   'procs'  : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ'],
#   'signal' : False
# }

# sig_procs = {
#   'mass'   : ['110', '115', '120', '125', '130', '135', '140', '145'],
#   'procs'  : ['ggH', 'qqH'],
#   'signal' : True
# }

# obs.update(meta)
# bkg_procs.update(meta)
# sig_procs.update(meta)


# cmb.AddObservations(**obs)
# cmb.AddProcesses(**bkg_procs)
# cmb.AddProcesses(**sig_procs)


# def Tester(obs):
#   printlist = [ch.Observation.bin_id, ch.Observation.mass]
#   for x in printlist:
#     print str(x(obs))

# cmb.ForEachObs(Tester)



# for card in glob.glob('htt_lhchcg/125/htt*.txt'):
#   print card
#   cmb.ParseDatacard(card, "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

# for card in glob.glob('htt_lhchcg/125/vhtt*.txt'):
#   print card
#   cmb.ParseDatacard(card, "$MASS/$ANALYSIS_$BINID_$ERA.txt")

# cmb.PrintAll()



# cmb.ParseDatacard("output/sm_cards/htt_mt_125.txt", mass="125")
# cmb.cp().backgrounds().AddBinByBin(0.1, True, cmb)
# cmb.WriteDatacard("output/sm_cards/htt_mt_125_bbb.txt", "output/sm_cards/htt_mt_125_bbb.root")





# cmb.Parse("output/sm_cards/htt_mt_125.txt", mass="125")
# cmb.PrintAll()

# cmb.SetVerbosity(1)
# cmb.ParseDatacard("output/sm_cards/htt_mt_125.txt", "htt", "8TeV", "mt", 0, "125")
# cmb.cp()

# # print cmb.cp().bin(['htt_mt_4_8TeV']).process(['ZTT']).GetRate()

# for i,b in enumerate(cmb.bin_set()):
#   print str(i)+":"+b

# mlfit = R.TFile("output/sm_cards/mlfit.root")
# fit = mlfit.Get("fit_s")
# fit.Print()
# mlfit.Close()

# cmb.UpdateParameters(fit)

# hist = cmb.cp().bin(["htt_mt_1_8TeV"]).GetShape()
# hist.Print("range")
# # hist.SetDirectory(0)

# cmb.PrintAll()

# outfile = R.TFile("output_htt_mt_125.root", "RECREATE")

# for bin in cmb.bin_set():
#   dir = R.gDirectory.mkdir(bin)
#   for proc in cmb.cp().bin([bin]).process_set():
#     dir.WriteObject(cmb.cp().bin([bin]).process([proc]).GetShape(), proc)

# outfile.Close()


# cmb.WriteDatacard("test.txt", file)

# cmb.PrintAll()
# cmb.SetVerbosity(3)

# for b in cmb.bin_set():
#   print b
#   print cmb.cp().bin([b]).GetObservedRate()
#   print cmb.cp().bin([b]).GetRate()



