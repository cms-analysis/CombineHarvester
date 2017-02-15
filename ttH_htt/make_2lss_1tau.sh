#! /bin/csh -f

WriteDatacards_2lss_1tau_FRjt_syst

combine -M MaxLikelihoodFit -m 125 ttH_2lss_1tau.txt

combine -M Asymptotic -m 125 ttH_2lss_1tau.txt

PostFitShapes -d ttH_2lss_1tau.txt -o ttH_2lss_1tau_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print

cd macros
root -b -n -q -l makePostFitPlots_2lss_1tau.C++
cd -
