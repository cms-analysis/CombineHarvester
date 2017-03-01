#! /bin/csh -f

WriteDatacards_2lss_1tau -i datacard_MEM_nomiss.root -o ttH_2lss_1tau_2016_MEM_nomiss.root

WriteDatacards_2lss_1tau -i datacard_MEM_missing.root -o ttH_2lss_1tau_2016_MEM_missing.root

combineCards.py ttH_2lss_1tau_2016_MEM_nomiss.txt ttH_2lss_1tau_2016_MEM_missing.txt > ttH_2lss_1tau_2016_MEM_2cat.txt

combine -M MaxLikelihoodFit -m 125 ttH_2lss_1tau_2016_MEM_2cat.txt

combine -M Asymptotic -m 125 ttH_2lss_1tau_2016_MEM_2cat.txt

PostFitShapes -d ttH_2lss_1tau_2016_MEM_2cat.txt -o ttH_2lss_1tau_2016_MEM_2cat_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print

cd macros
root -b -n -q -l makePostFitPlots_2lss_1tau.C++
cd -
