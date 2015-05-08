#!/usr/bin/env python

import combineharvester as ch
import ROOT as R
import glob

cb = ch.CombineHarvester()

chns = ['et', 'mt', 'em', 'ee', 'mm', 'tt']

input_folders = {
  'et' : 'Imperial',
  'mt' : 'Imperial',
  'em' : 'MIT',
  'ee' : 'DESY-KIT',
  'mm' : 'DESY-KIT',
  'tt' : 'CERN'
}

bkg_procs = {
  'et' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'mt' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV'],
  'em' : ['Ztt', 'EWK', 'Fakes', 'ttbar', 'ggH_hww125', 'qqH_hww125'],
  'ee' : ['ZTT', 'WJets', 'QCD', 'ZEE', 'TTJ', 'Dibosons', 'ggH_hww125', 'qqH_hww125'],
  'mm' : ['ZTT', 'WJets', 'QCD', 'ZMM', 'TTJ', 'Dibosons', 'ggH_hww125', 'qqH_hww125'],
  'tt' : ['ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TT', 'VV']
}

sig_procs = ['ggH', 'qqH', 'WH', 'ZH']

cats = {
  'et_7TeV' : [
    (1, 'eleTau_0jet_medium'), (2, 'eleTau_0jet_high'),
    (3, 'eleTau_1jet_medium'), (5, 'eleTau_1jet_high_mediumhiggs'),
    (6, 'eleTau_vbf')
  ],
  'et_8TeV' : [
    (1, 'eleTau_0jet_medium'), (2, 'eleTau_0jet_high'),
    (3, 'eleTau_1jet_medium'), (5, 'eleTau_1jet_high_mediumhiggs'),
    (6, 'eleTau_vbf_loose'), (7, 'eleTau_vbf_tight')
  ],
  'mt_7TeV' : [
    (1, 'muTau_0jet_medium'), (2, 'muTau_0jet_high'),
    (3, 'muTau_1jet_medium'), (4, 'muTau_1jet_high_lowhiggs'), (5, 'muTau_1jet_high_mediumhiggs'),
    (6, 'muTau_vbf')
  ],
  'mt_8TeV' : [
    (1, 'muTau_0jet_medium'), (2, 'muTau_0jet_high'),
    (3, 'muTau_1jet_medium'), (4, 'muTau_1jet_high_lowhiggs'), (5, 'muTau_1jet_high_mediumhiggs'),
    (6, 'muTau_vbf_loose'), (7, 'muTau_vbf_tight')
  ],
  'em_7TeV' : [
    (0, 'emu_0jet_low'), (1, 'emu_0jet_high'),
    (2, 'emu_1jet_low'), (3, 'emu_1jet_high'),
    (4, 'emu_vbf_loose')
  ],
  'em_8TeV' : [
    (0, 'emu_0jet_low'), (1, 'emu_0jet_high'),
    (2, 'emu_1jet_low'), (3, 'emu_1jet_high'),
    (4, 'emu_vbf_loose'), (5, 'emu_vbf_tight')
  ],
  'ee_7TeV' : [
    (0, 'ee_0jet_low'), (1, 'ee_0jet_high'),
    (2, 'ee_1jet_low'), (3, 'ee_1jet_high'),
    (4, 'ee_vbf')
  ],
  'mm_7TeV' : [
    (0, 'mumu_0jet_low'), (1, 'mumu_0jet_high'),
    (2, 'mumu_1jet_low'), (3, 'mumu_1jet_high'),
    (4, 'mumu_vbf')
  ],
  'tt_7TeV' : [],
  'tt_8TeV' : [
    (0, 'tauTau_1jet_high_mediumhiggs'), (1, 'tauTau_1jet_high_highhiggs'),
    (2, 'tauTau_vbf')
  ]
}
cats['ee_8TeV'] = cats['ee_7TeV']
cats['mm_8TeV'] = cats['mm_7TeV']

masses = ['110', '115', '120', '125', '130', '135', '140', '145']

print ">> Creating processes and observations..."

for era in ['7TeV', '8TeV']:
  for chn in chns:
    cb.AddObservations(['*'], ['htt'], [era], [chn], cats[chn+"_"+era])
    cb.AddProcesses(['*'],  ['htt'], [era], [chn], bkg_procs[chn], cats[chn+"_"+era], False)
    cb.AddProcesses(masses, ['htt'], [era], [chn], sig_procs,      cats[chn+"_"+era], True)

cb.channel(['mt']).bin_id([1, 2])

cb.SetVerbosity(2)
cb.AddSyst(cb, "test_$BIN", "lnN", ch.SystMap('process', 'bin_id')
    (['ZTT', 'W', 'QCD'],   [1, 2], 1.08)
    (['VV', 'TT', 'blah'],  [1, 2], 1.05)
  )

cb.cp().process(['ZTT']).AddSyst(cb, "test_ZTT", "lnN", ch.SystMap()(1.10))

cb.cp().process(['WH', 'ZH']).AddSyst(
  cb, 'QCDscale_VH', 'lnN', ch.SystMap('channel', 'era', 'bin_id')
    (['mt'], ['7TeV', '8TeV'],  [1, 2],               1.010)
    (['mt'], ['7TeV', '8TeV'],  [3, 4, 5, 6, 7],      1.040)
    (['et'], ['7TeV'],          [1, 2, 3, 5, 6, 7],   1.040)
    (['et'], ['8TeV'],          [1, 2],               1.010)
    (['et'], ['8TeV'],          [3, 5, 6, 7],         1.040))

# cb.PrintSysts()





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



