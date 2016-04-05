import CombineHarvester.CombineTools.ch as ch
import sys

args = sys.argv[1:]

cmb = ch.CombineHarvester()
cmb.ParseDatacard(args[0], mass=args[1])
#cmb.FilterSysts(lambda x : RemoveBinByBin(x))
cmb.PrintAll()

for p in cmb.process_set():
  cmb.cp().process([p]).PrintSysts()


#bbb = ch.BinByBinFactory()
#bbb.SetAddThreshold(0.05).SetFixNorm(False)
#bbb.AddBinByBin(cmb.cp().backgrounds(), cmb)

#cmb.syst_name(['CMS___b2lss_ee_0tau_pos__WZ_bin_6', 'CMS___b2lss_ee_0tau_pos__WWss_bin_3', 'CMS___b2lss_mm_0tau_bl_neg__WWss_bin_6'], False)

#cmb.WriteDatacard('test.txt','input.root')
#cmb.cp().syst_type(['shape']).PrintSysts()
