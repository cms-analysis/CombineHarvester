#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.ch as ch
import os

ROOT.TH1.AddDirectory(False)

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG16044/HIG16044cards/'
output = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG16044/output/vhbb_stxs/'

cb = ch.CombineHarvester()
cb2 = ch.CombineHarvester()

#cb2.ParseDatacard(output+"combined.txt.cmb","vhbb","13TeV","Wln")
cb.ParseDatacard(shapes+"vhbb_2016_13TeV.txt","vhbb","13TeV","")
#cb.ParseDatacard(shapes+"znn_test/vhbb_znnhbb_2016_13TeV.txt","vhbb","13TeV","Znn")

cb.cp().ForEachObj(lambda x: x.set_process("ZH_lep_hbb") if x.process()=='ZH_hbb' else None)
cb.cp().ForEachObj(lambda x: x.set_process("WH_lep_hbb") if x.process()=='WH_hbb' else None)
cb.cp().ForEachObj(lambda x: x.set_process("ggZH_lep_hbb") if x.process()=='ggZH_hbb' else None)


cb.syst_name(['pdf_HIGGS_qqbar'],False)
cb.syst_name(['QCDscale_VH_ggZHacceptance_highPt'],False)
cb.syst_name(['QCDscale_VH_ggZHacceptance_lowPt'],False)
cb.syst_name(['QCDscale_VH'],False)

cb.cp().signals().RenameSystematic(cb,'pdf_gg','pdf_Higgs_gg')
cb.cp().signals().RenameSystematic(cb,'pdf_qqbar','pdf_Higgs_qqbar')

cb.cp().process(['ggZH_lep_hbb']).syst_name(['pdf_Higgs_gg']).ForEachSyst(lambda x: x.set_value_u(1.024))
cb.cp().process(['ZH_lep_hbb']).syst_name(['pdf_Higgs_qqbar']).ForEachSyst(lambda x: x.set_value_u(1.016))
cb.cp().process(['WH_lep_hbb']).syst_name(['pdf_Higgs_qqbar']).ForEachSyst(lambda x: x.set_value_u(1.019))

cb.cp().process(['ggZH_lep_hbb']).AddSyst(cb,'QCDscale_ggZH', 'lnN', ch.SystMap()((1.251,0.811)))
cb.cp().AddSyst(cb, 'QCDscale_VH','lnN',ch.SystMap('process')
     (['ZH_lep_hbb'],(1.038,0.969))
     (['WH_lep_hbb'],(1.005,0.993)))

cb.cp().syst_name(['QCDscale_VH']).PrintSysts()

writer=ch.CardWriter(output+"vhbb_2016_stxs0.txt",
                      output+ "vhbb_input.root")
writer.SetWildcardMasses([])
writer.SetVerbosity(1);


writer.WriteCards("cmb",cb);







