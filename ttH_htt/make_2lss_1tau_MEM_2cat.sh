#! /bin/csh -f

WriteDatacards_2lss_1tau_FRjt_syst -i /data_CMS/cms/strebler/ttH_prod_80X_01_2017/datacards/datacard_MEM_ttH_vs_full_bkg_2lSS_nomiss_nofaketau_35.9fb_012017.root -o ttH_2lss_1tau_MEM_nomiss.root -b ttH_2lss_1tau_nomiss

WriteDatacards_2lss_1tau_FRjt_syst -i /data_CMS/cms/strebler/ttH_prod_80X_01_2017/datacards/datacard_MEM_ttH_vs_full_bkg_2lSS_missing_nofaketau_35.9fb_012017.root -o ttH_2lss_1tau_MEM_missing.root -b ttH_2lss_1tau_missing

combineCards.py ttH_2lss_1tau_MEM_nomiss.txt ttH_2lss_1tau_MEM_missing.txt > ttH_2lss_1tau_MEM_2cat.txt

combine -M MaxLikelihoodFit -m 125 ttH_2lss_1tau_MEM_2cat.txt

combine -M Asymptotic -m 125 ttH_2lss_1tau_MEM_2cat.txt

PostFitShapes -d ttH_2lss_1tau_MEM_2cat.txt -o ttH_2lss_1tau_MEM_2cat_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print

cd macros
root -b -n -q -l makePostFitPlots_2lss_1tau.C++
cd -
