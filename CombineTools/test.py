import libCHCombineTools as ch
import itertools
import ROOT as R

cmb = ch.CombineHarvester()
# cmb.ParseDatacard("output/sm_cards/htt_mt_125.txt", "$ANALYSIS_$CHANNEL_$MASS.txt")

cmb.ParseDatacard("output/sm_cards/htt_mt_125.txt", "htt", "8TeV", "mt", 0, "125")

# print cmb.cp().bin(['htt_mt_4_8TeV']).process(['ZTT']).GetRate()

# for i,b in enumerate(cmb.bin_set()):
#   print str(i)+":"+b

mlfit = R.TFile("output/sm_cards/mlfit.root")
fit = mlfit.Get("fit_s")
mlfit.Close()

cmb.UpdateParameters(fit)

hist = cmb.cp().bin(["htt_mt_1_8TeV"]).GetShapeWithUncertainty(fit, 500)
# hist.SetDirectory(0)
hist.Print("range")

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
#   print cmb.cp().bin([b], True).GetObservedRate()
#   print cmb.cp().bin([b], True).GetRate()



