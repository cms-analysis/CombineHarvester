#! /bin/csh -f

WriteDatacards_1l_2tau_FRjt_syst

combine -M MaxLikelihoodFit -m 125 ttH_1l_2tau.txt

combine -M Asymptotic -m 125 ttH_1l_2tau.txt

PostFitShapes -d ttH_1l_2tau.txt -o ttH_1l_2tau_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print

cd macros
root -b -n -q -l makePostFitPlots_1l_2tau.C++
cd -
