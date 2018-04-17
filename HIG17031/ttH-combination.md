# ttH combination

## Set up the repositories

```
# In CMSSW_8_1_0/src:

git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit; git checkout -b comb2017 origin/comb2017; cd ../../
git clone git@github.com:cms-analysis/CombineHarvester.git
cd CombineHarvester; git checkout -b comb2017 origin/comb2017; cd ../
scram b -j8
svn co -N svn+ssh://svn.cern.ch/reps/cmshcg/trunk/summer2017
cd summer2017/couplings
```

## Make the combined card

`python prepareComb.py --stats-mode 2 --postfix _ttHComb --ttH`

## text2workspace

`for CARD in ttH ttH_plus_run1 tth_run1; do for M in A1; do combineTool.py -M T2W -i comb_2017_mu_${CARD}_ttHComb.txt -o comb_${CARD}_${M}.root  -m 125 -P HiggsAnalysis.CombinedLimit.LHCHCGModels:${M} --PO dohmm=1 --for-fits --job-mode interactive; done; done`

For ttH_hbb studies:
`for CARD in tth_hbb tth_hbb_leptonic tth_hbb_hadronic; do combineTool.py -M T2W -i comb_2017_mu_${CARD}_ttHComb.txt -o comb_${CARD}.root  -m 125 --for-fits --job-mode interactive; done`


## Adding the attributes

`for CARD in ttH ttH_plus_run1 tth_run1; do for M in A1; do python addAttributes.py -i comb_${CARD}_${M}.root --json attributes.json -o comb_${CARD}_${M}_attr.root | tee attr_${CARD}_${M}.log; done; done`

## Saving best-fit snapshots for data, prefit asimov and post asimov

The A1_ttH model has a single POI, `mu_XS_ttH`. All other signal processes, including tHq and tHW, are fixed to 1. The A1_ttH_5D model has five POIs: `mu_XS_ttH_BR_WW`, `mu_XS_ttH_BR_ZZ`, `mu_XS_ttH_BR_bb`, `mu_XS_ttH_BR_gamgam`, `mu_XS_ttH_BR_tautau`. All other signal production processes, as well as other ttH decay modes, are fixed to 1.

`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do echo ${CARD} ${M}; done; done`

`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M MultiDimFit -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m)_attr.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --generate 't;n;toysFrequentist;;!,observed,!;-1,prefit_asimov,!;-1,postfit_asimov, ' --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M} --job-mode lxbatch --sub-opts='-q 1nd -R "rusage[mem=4000]"' --task-name ${CARD}.${M}.snapshots --dry-run; done; done`

`for TYPE in observed prefit_asimov postfit_asimov; do for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do echo -e "${CARD} - ${M}\n==========" | tee -a ${TYPE}_${CARD}_fit_results.txt; combineTool.py -M PrintFit --algo none -P $(./getPOIs.py ${M} -p) higgsCombine.${CARD}.${M}.${TYPE}.MultiDimFit.mH125.09.123456.root | tee -a ${TYPE}_${CARD}_fit_results.txt; echo -e "\n" | tee -a ${TYPE}_${CARD}_fit_results.txt; done; done; done`

## Rename
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in A1_ttH A1_ttH_5D A1_ttH_E; do for TYPE in observed prefit_asimov postfit_asimov; do mv higgsCombine.${CARD}.${M}.${TYPE}.MultiDimFit.mH125.09*.root comb_${CARD}_${M}_${TYPE}.root; done; done; done`


## SM point
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do MOD=${M}; combineTool.py -M MultiDimFit -m 125.09 --generate "d;D;n;;comb_${CARD}_${MOD}_observed.root,data_obs,observed" --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) $(./getPOIs.py ${M} -O) -n .smpoint.${CARD}.${M} --snapshotName "MultiDimFit" --skipInitialFit --algo fixed --fixedPointPOIs $(./getPOIs.py ${M} -s)  --pre-cmd "LD_PRELOAD=./libMinuit2.so " --job-mode lxbatch --sub-opts='-q 8nh -R "rusage[mem=4000]"' --task-name ${CARD}.${M}.smpoint --dry-run; done; done`

`for CARD in ttH ttH_plus_run1 tth_run1; do for TYPE in observed; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do echo -e "${M}\n==========" >> ${CARD}_${TYPE}_smpoint_results.txt; combineTool.py -M PrintFit --algo fixed -P $(./getPOIs.py ${M} -p) higgsCombine.smpoint.${CARD}.${M}.${TYPE}.MultiDimFit.mH125.09.root >> ${CARD}_${TYPE}_smpoint_results.txt; echo -e "\n" >> ${CARD}_${TYPE}_smpoint_results.txt; done; done; done`

## Scans

The `--generate` command causes the combine command to be repeated with different sets of options. Multiple arguments can be specified, and all possible combinations will be generated. In this case the argument lets us loop through different input workspaces, the second through freezing different nuisance groups, and the third through the different model POIs. The syntax of these arguments is:

    arg1;arg2;...;argN;;val1_1,val2_1,...,valN_1;...;val1_M,val2_M,...,valN_M

The argX statements should be combine options given without the leading `-` or `--`. This generates a loop where the arguments will be set like:

    combine --arg1=val1_1 --arg2=val2_1 ... --argN=valN_1
    combine --arg1=val1_2 --arg2=val2_2 ... --argN=valN_2
    ...
    combine --arg1=val1_M --arg2=val2_M ... --argN=valN_M

The `name` or `n` option is treated specially: the given values will be appended to the existing name instead of replacing it altogether, therefore it can appear in multiple arguments. Note that `:` can also be used instead of `;` as the separator, and `,,` can be used instead of `,` to separate the valX_Y if these themselves need to contain a comma. If a valX_Y is an empty string then no corresponding option or argument will be inserted for that particular combine call.

`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do MOD=$(./getPOIs.py ${M} -m); combineTool.py -M MultiDimFit -m 125.09 --generate "d;D;n;;comb_${CARD}_${M}_observed.root,data_obs,observed;comb_${CARD}_${M}_prefit_asimov.root,toys/toy_asimov,prefit_asimov;comb_${CARD}_${M}_postfit_asimov.root,toys/toy_asimov,postfit_asimov" 'freezeNuisanceGroups;n;;!,nominal;sigTheory,fr.sigTheory;sigTheory,bkgTheory,,fr.allTheory;all,fr.all' $(./getPOIs.py ${M} -g) --redefineSignalPOIs $(./getPOIs.py ${M} -p) --floatOtherPOIs 1 --useAttributes 1 --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M}  --snapshotName "MultiDimFit" --skipInitialFit --algo grid --points 40 --split-points 6 --job-mode condor --sub-opts='+JobFlavour = "workday"' --task-name ${CARD}_${M}_scans --pre-cmd "LD_PRELOAD=./libMinuit2.so " --dry-run; done; done`


## hadd
`START=${PWD}; for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do for W in observed prefit_asimov postfit_asimov; do for T in nominal fr.all fr.sigTheory fr.allTheory; do for P in $(./getPOIs.py ${M} -P); do hadd -k -f scan.${CARD}.${M}.${W}.${T}.${P}.root higgsCombine.${CARD}.${M}.${W}.${T}.${P}.POINTS.*.root; done; done; done; done; done`

## plotting

Copy hadd'ed output from above to CombineHarvester/HIG17031. From that directory, run:

`INPUT="ttHComb_Mar20/results"; OUTPUT="ttHComb_Mar20/plots"; for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do mkdir -p ${OUTPUT}/${CARD}/${M}; for W in observed prefit_asimov postfit_asimov; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_full_split_${W}_${M}_${P} --POI ${P} --model ${M} --others \"${INPUT}/scan.${CARD}.${M}.${W}.fr.sigTheory.${P}.root:Freeze Sig. Th.:2\" \"${INPUT}/scan.${CARD}.${M}.${W}.fr.allTheory.${P}.root:Freeze Bkg.Th.+Sig.Th:38\" \"${INPUT}/scan.${CARD}.${M}.${W}.fr.all.${P}.root:Freeze Exp.+Bkg.Th.+Sig.Th.:8\" --breakdown "SigTh,BkgTh,Exp,Stat" --json ${OUTPUT}/${CARD}/${W}.json --translate pois.json --meta "Types:${W},Scans:full_split,POIs:${P}" -m ${INPUT}/scan.${CARD}.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --no-input-label --outdir ${OUTPUT}/${CARD}/${M}; done; done; done; done`

`INPUT="ttHComb_Mar20/results"; OUTPUT="ttHComb_Mar20/plots"; for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do mkdir -p ${OUTPUT}/${CARD}/${M}; for W in observed prefit_asimov postfit_asimov; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_split_${W}_${M}_${P} --POI ${P} --model ${M} --others \"${INPUT}/scan.${CARD}.${M}.${W}.fr.all.${P}.root:Freeze all:8\" --breakdown "Syst,Stat" --json ${OUTPUT}/${CARD}/stat_syst_${W}.json --translate pois.json --meta "Types:${W},Scans:split,POIs:${P}" -m ${INPUT}/scan.${CARD}.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --no-input-label --outdir ${OUTPUT}/${CARD}/${M}; done; done; done; done`

`INPUT="ttHComb_Mar20/results"; OUTPUT="ttHComb_Mar20/plots"; for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do mkdir -p ${OUTPUT}/${CARD}/${M}; for W in observed prefit_asimov postfit_asimov; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_signif_${W}_${M}_${P} --POI ${P} --model ${M} --json ${OUTPUT}/${CARD}/signif_${W}.json --translate pois.json --meta "Types:${W},Scans:significance,POIs:${P}" -m ${INPUT}/scan.${CARD}.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 30 --chop 30 ${EXTRA} --no-input-label --signif --outdir ${OUTPUT}/${CARD}/${M}; done; done; done; done`

## impacts

# Per-channel workspaces
`for M in A1; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do combineTool.py -M T2W -i comb_2017_mu_${CARD}_ttHComb.txt -o comb_${CARD}_${M}.root  -m 125 -P HiggsAnalysis.CombinedLimit.LHCHCGModels:${M} --PO dohmm=1 --for-fits --job-mode interactive; done; done`

`for M in A1_ttH; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do combineTool.py -M MultiDimFit -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m).root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --generate "t;n;toysFrequentist;;,observed,;-1,prefit_asimov," --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M} --job-mode interactive --dry-run; done; done`

`for M in A1_ttH; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do for TYPE in observed prefit_asimov; do mv higgsCombine.${CARD}.${M}.${TYPE}.MultiDimFit.mH125.09*.root comb_${CARD}_${M}_${TYPE}.root; done; done; done`

## Run the impacts for the prefit_asimov
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M Impacts -m 125.09 --allPars --doInitialFit --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${CARD}_${M}_prefit_asimov.root -D toys/toy_asimov --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_prefit_asimov_${CARD}_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_9_7TeV,pdfindex_11_8TeV,pdfindex_12_8TeV$(./getPOIs.py ${M} -F) --job-mode condor --sub-opts='+JobFlavour = "workday"' --task-name comb_prefit_asimov_${CARD}_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --pre-cmd "LD_PRELOAD=./libMinuit2.so " --merge 4 --dry-run; done; done`
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M Impacts -m 125.09 --allPars --doFits --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${CARD}_${M}_prefit_asimov.root -D toys/toy_asimov --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_prefit_asimov_${CARD}_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_9_7TeV,pdfindex_11_8TeV,pdfindex_12_8TeV$(./getPOIs.py ${M} -F) --job-mode crab3 --custom-crab custom_crab_andrew.py --crab-extra-files "libMinuit2.so" --task-name comb_prefit_asimov_${CARD}_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --pre-cmd "LD_PRELOAD=./libMinuit2.so " --merge 4 --dry-run; done; done`

## And for the data
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M Impacts -m 125.09 --allPars --doInitialFit --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${CARD}_${M}_observed.root -D data_obs --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_observed_${CARD}_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_9_7TeV,pdfindex_11_8TeV,pdfindex_12_8TeV$(./getPOIs.py ${M} -F) --job-mode lxbatch --sub-opts='-q 1nd -R "rusage[mem=4000]"' --task-name comb_observed_${CARD}_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --pre-cmd "LD_PRELOAD=./libMinuit2.so " --dry-run; done; done`
`for CARD in ttH ttH_plus_run1 tth_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH A1_ttH_5D A1_ttH_E";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M Impacts -m 125.09 --allPars --doFits --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${CARD}_${M}_observed.root -D data_obs --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_observed_${CARD}_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV,pdfindex_9_7TeV,pdfindex_11_8TeV,pdfindex_12_8TeV$(./getPOIs.py ${M} -F) --job-mode crab3 --custom-crab custom_crab_andrew.py --crab-extra-files "libMinuit2.so" --task-name comb_observed_${CARD}_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --pre-cmd "LD_PRELOAD=./libMinuit2.so " --merge 4 --dry-run; done; done`



`for M in A1_ttH A1_ttH_5D; do for P in $(../getPOIs.py ${M} -P); do python ../../CombineTools/scripts/plotImpacts.py -i impacts_comb_observed_${M}_extra.json -o impacts_comb_observed_${M}_${P} --transparent --per-page 25 --translate ../summer2017/couplings/pois.json --POI ${P} --checkboxes; done; done`

## GoF tests

`for TYPE in tth_hbb tth_hbb_leptonic tth_hbb_hadronic; do combineTool.py -M GoodnessOfFit --algorithm KS --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -m 125.09 comb_${TYPE}.root -n .${TYPE} --parallel 4; done`

`for TYPE in tth_hbb tth_hbb_leptonic tth_hbb_hadronic; do combineTool.py -M GoodnessOfFit --algorithm KS --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -m 125.09 -d comb_${TYPE}.root -n .toys.${TYPE} -t 20 --expectSignal 1 --toysFrequentist -s 1:50:1 --job-mode lxbatch --sub-opts='-q 8nh' --task-name ${TYPE}.gof; done`

`for M in tth_hbb{,_leptonic,_hadronic}; do combineTool.py -M CollectGoodnessOfFit --input higgsCombine.sat*${M}.* --output ${M}_sat_gof.json; done`

`for M in tth_hbb{,_leptonic,_hadronic}; plotGof.py ${M}_sat_gof.json -o ${M}_sat_gof --statistic saturated --mass "125.089996338"`

## Correlation bias tests

`for X in def altB altD; do for CARD in ttH_plus_run1; do for M in A1_ttH; do combineTool.py -M GenerateOnly -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m)_${X}.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) -t 2 -s 1:100:1 --job-mode lxbatch --sub-opts='-q 1nd' --task-name bias_toygen_${CARD}_${M}_${X} --saveToys --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M}.${X}; done; done; done`

`for X in def; do for Y in def altB altD; do for CARD in ttH_plus_run1; do for M in A1_ttH; do combineTool.py -M FitDiagnostics --skipBOnlyFit --robustFit 1 --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m)_${X}.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) -t 2 -s 1:100:1 --job-mode lxbatch --sub-opts='-q 1nd' --task-name bias_fit_${CARD}_${M}_${X}_${Y} --toysFile higgsCombine.${CARD}.${M}.${Y}.GenerateOnly.mH125.09.'%(SEED)s'.root --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --pre-cmd "LD_PRELOAD=./libMinuit2.so " -n .${CARD}.${M}.mod.${X}.toy.${Y}.'%(SEED)s'; done; done; done; done`


## Extra plots

`python scripts/summaryPlot.py -i 'ttHComb_Mar12/Mar12/ttH/stat_syst_observed.json:A1_ttH/*' 'ttHComb_Mar12/Mar12/ttH/stat_syst_observed.json:A1_ttH_5D/mu_XS_ttH_BR_bb,mu_XS_ttH_BR_tautau,mu_XS_ttH_BR_gamgam,mu_XS_ttH_BR_WW,mu_XS_ttH_BR_ZZ' -o test --translate pois.json --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1'`

~~~
python scripts/summaryPlot.py -i \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH/*' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS13_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS8_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_5D/mu_XS_ttH_BR_bb,mu_XS_ttH_BR_tautau,mu_XS_ttH_BR_gamgam,mu_XS_ttH_BR_WW,mu_XS_ttH_BR_ZZ' \
-o mu_summary_obs --translate pois.json --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1' '3.0:LineStyle=1' --height 600 --labels 0="Combined",1="13 TeV",2="7+8 TeV",3="H#rightarrowbb",4="H#rightarrow#tau#tau",5="H#rightarrow#gamma#gamma,6="H#rightarrowWW"",7="H#rightarrowZZ" --x-title "#mu_{ttH}" --subline '4.9 fb^{-1} (7 TeV) + 19.8 fb^{-1} (8 TeV) + 35.9 fb^{-1} (13 TeV)' --x-range='-1,7'

python scripts/summaryPlot.py -i \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH/*' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS13_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS8_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_5D/mu_XS_ttH_BR_bb,mu_XS_ttH_BR_tautau,mu_XS_ttH_BR_gamgam,mu_XS_ttH_BR_WW,mu_XS_ttH_BR_ZZ' \
-o mu_summary_obs --translate pois.json --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1' '3.0:LineStyle=1' --height 600 --labels 0="Combined",1="13 TeV",2="7+8 TeV",3='t#bar{t}H(b#bar{b})',4="t#bar{t}H(#tau^{+}#tau^{-})",5="t#bar{t}H(#gamma#gamma)",6='t#bar{t}H(WW*)',7='t#bar{t}H(ZZ*)' --x-title "#mu_{t#bar{t}H}" --subline '5.1 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 35.9 fb^{-1} (13 TeV)' --x-range='-1,7'

python scripts/summaryPlot.py -i \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH/*' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS13_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_E/mu_XS8_ttH' \
'ttHComb_Mar20/Mar20/ttH_plus_run1/stat_syst_observed.json:A1_ttH_5D/mu_XS_ttH_BR_bb,mu_XS_ttH_BR_tautau,mu_XS_ttH_BR_gamgam,mu_XS_ttH_BR_ZZ,mu_XS_ttH_BR_WW' \
-o mu_summary_obs --translate pois.json --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1' '3.0:LineStyle=1' --height 600 --labels 0="Combined",1="13 TeV",2="7+8 TeV",3='t#bar{t}H(b#bar{b})',4="t#bar{t}H(#tau^{+}#tau^{-})",5="t#bar{t}H(#gamma#gamma)",6='t#bar{t}H(ZZ*)',7='t#bar{t}H(WW*)' --x-title "#mu_{t#bar{t}H}" --subline '5.1 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 35.9 fb^{-1} (13 TeV)' --x-range='-1,7'



M=A1_ttH; P=mu_XS_ttH; INPUT="ttHComb_Mar20/results"; OUTPUT="ttHComb_Mar20/plots/pub"; mkdir -p ${OUTPUT}; for W in observed; do eval python scripts/plot1DScan.py -o scan_pub_signif_w_exp_${W} --POI ${P} --model ${M} --others \
 \"${INPUT}/scan.ttH_plus_run1.A1_ttH.postfit_asimov.nominal.mu_XS_ttH.root:SM expected:418:mu_XS_ttH:2\" \
\"${INPUT}/scan.ttH_plus_run1.A1_ttH_E.${W}.nominal.mu_XS13_ttH.root:13 TeV:4:mu_XS13_ttH\" \
\"${INPUT}/scan.ttH_plus_run1.A1_ttH_E.${W}.nominal.mu_XS8_ttH.root:7+8 TeV:2:mu_XS8_ttH\" \
 --translate pois.json  -m ${INPUT}/scan.ttH_plus_run1.A1_ttH.${W}.nominal.mu_XS_ttH.root --remove-near-min 0.8 --y-max 35 --chop 40 --pub --no-numbers --no-input-label --outdir ${OUTPUT} --legend-pos 9 --no-box --x-range "0,3.7" --signif --decorate-signif "1,2,3,4,5" --title-right \"5.1 fb^{-1} \(7 TeV\) + 19.7 fb^{-1} \(8 TeV\) + 35.9 fb^{-1} \(13 TeV\)\" --main-label "Combined"; done

~~~


# Uncertainty breakdown

`for CARD in ttH_plus_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH";; ttH) echo "A1_ttH";; tth_run1) echo "A1_ttH";; esac); do MOD=$(./getPOIs.py ${M} -m); combineTool.py -M MultiDimFit -m 125.09 --generate "d;D;n;;comb_${CARD}_${M}_observed.root,data_obs,observed" 'freezeNuisanceGroups;n;;!,fr.nominal;ttHMCStat,fr.ttHMCStat;ttHBkg,fr.ttHBkg;ttHttHF,fr.ttHttHF;ttHSigAcc,fr.ttHSigAcc;ttHLum,fr.ttHLum;ttHttV,fr.ttHttV;ttHBtag,fr.ttHBtag;ttHPho,fr.ttHPho;ttHlEff,fr.ttHlEff;ttHlFR,fr.ttHlFR;ttHJES,fr.ttHJES;ttHIncXS,fr.ttHIncXS;ttHOthHiggs,fr.ttHOthHiggs' $(./getPOIs.py ${M} -g) --redefineSignalPOIs $(./getPOIs.py ${M} -p) --floatOtherPOIs 1 --useAttributes 1 --setParameterRanges mu_XS_ttH=0.6,2.2 --freezeParameters MH$(./getPOIs.py ${M} -F) --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M}  --snapshotName "MultiDimFit" --skipInitialFit --algo grid --points 20 --split-points 7 --job-mode condor --sub-opts='+JobFlavour = "workday"' --task-name ${CARD}_${M}_bigscans --pre-cmd "LD_PRELOAD=./libMinuit2.so " --dry-run; done; done`

`START=${PWD}; for CARD in ttH_plus_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do for W in observed; do for T in fr.nominal fr.ttHMCStat fr.ttHBkg fr.ttHttHF fr.ttHSigAcc fr.ttHLum fr.ttHttV fr.ttHBtag fr.ttHPho fr.ttHlEff fr.ttHlFR fr.ttHJES fr.ttHIncXS fr.ttHOthHiggs; do for P in $(./getPOIs.py ${M} -P); do hadd -k -f breakdown.${CARD}.${M}.${W}.${T}.${P}.root higgsCombine.${CARD}.${M}.${W}.${T}.${P}.POINTS.*.root; done; done; done; done; done`

`INPUT="ttHComb_Mar20/results"; OUTPUT="ttHComb_Mar20/plots"; for CARD in ttH_plus_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do mkdir -p ${OUTPUT}/${CARD}/breakdown; for W in observed; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do for FR in ttHMCStat ttHBkg ttHttHF ttHSigAcc ttHLum ttHttV ttHBtag ttHPho ttHlEff ttHlFR ttHJES ttHIncXS ttHOthHiggs; do eval python scripts/plot1DScan.py -o scan_fr_${FR}_${W}_${M}_${P} --POI ${P} --model ${M}_${FR} --others \"${INPUT}/breakdown.${CARD}.${M}.${W}.fr.${FR}.${P}.root:Freeze ${FR}:8\" --breakdown "${FR},Rest" --json ${OUTPUT}/${CARD}/breakdown_${W}.json --translate pois.json --meta "Types:${W},Scans:breakdown,POIs:${P}" -m ${INPUT}/breakdown.${CARD}.${M}.${W}.fr.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --no-input-label --outdir ${OUTPUT}/${CARD}/breakdown; done; done; done; done; done`


# S/B weighted

`for CARD in ttH_plus_run1; do for M in $(case ${CARD} in ttH_plus_run1) echo "A1_ttH";; ttH) echo "A1_ttH A1_ttH_5D";; tth_run1) echo "A1_ttH";; esac); do combineTool.py -M MultiDimFit -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m)_fullmod.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --generate 't;n;toysFrequentist;;!,observed,!' --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M}.fullmod --saveFitResult --job-mode interactive --dry-run; done; done`