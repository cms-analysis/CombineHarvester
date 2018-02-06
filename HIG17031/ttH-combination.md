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

`for M in A1; do combineTool.py -M T2W -i comb_2017_mu_ttH_ttHComb.txt -o comb_ttH_${M}.root  -m 125 -P HiggsAnalysis.CombinedLimit.LHCHCGModels:${M} --PO dohmm=1 --for-fits --job-mode interactive; done`

## Adding the attributes

`for M in A1; do python addAttributes.py -i comb_ttH_${M}.root --json attributes.json -o comb_ttH_${M}_attr.root | tee attr_ttH_${M}.log; done`

## Saving best-fit snapshots for data, prefit asimov and post asimov

The A1_ttH model has a single POI, `mu_XS_ttH`. All other signal processes, including tHq and tHW, are fixed to 1. The A1_ttH_5D model has five POIs: `mu_XS_ttH_BR_WW`, `mu_XS_ttH_BR_ZZ`, `mu_XS_ttH_BR_bb`, `mu_XS_ttH_BR_gamgam`, `mu_XS_ttH_BR_tautau`. All other signal production processes, as well as other ttH decay modes, are fixed to 1.

`for M in A1_ttH A1_ttH_5D; do combineTool.py -M MultiDimFit -m 125.09 -d comb_ttH_$(./getPOIs.py ${M} -m)_attr.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --generate "t;n;toysFrequentist;;,observed,;-1,prefit_asimov,;-1,postfit_asimov, " --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${M} --job-mode lxbatch --sub-opts='-q 1nd -R "rusage[mem=4000]"' --task-name ${M}.snapshots --dry-run; done`

## Rename
`for M in A1_ttH A1_ttH_5D; do for TYPE in observed prefit_asimov postfit_asimov; do mv higgsCombine.${M}.${TYPE}.MultiDimFit.mH125.09*.root comb_${M}_${TYPE}.root; done; done`

## Scans

The `--generate` command causes the combine command to be repeated with different sets of options. Multiple arguments can be specified, and all possible combinations will be generated. In this case the argument lets us loop through different input workspaces, the second through freezing different nuisance groups, and the third through the different model POIs. The syntax of these arguments is:

    arg1;arg2;...;argN;;val1_1,val2_1,...,valN_1;...;val1_M,val2_M,...,valN_M

The argX statements should be combine options given without the leading `-` or `--`. This generates a loop where the arguments will be set like:

    combine --arg1=val1_1 --arg2=val2_1 ... --argN=valN_1
    combine --arg1=val1_2 --arg2=val2_2 ... --argN=valN_2
    ...
    combine --arg1=val1_M --arg2=val2_M ... --argN=valN_M

The `name` or `n` option is treated specially: the given values will be appended to the existing name instead of replacing it altogether, therefore it can appear in multiple arguments. Note that `:` can also be used instead of `;` as the separator, and `,,` can be used instead of `,` to separate the valX_Y if these themselves need to contain a comma. If a valX_Y is an empty string then no corresponding option or argument will be inserted for that particular combine call.

`for M in A1_ttH A1_ttH_5D; do MOD=$(./getPOIs.py ${M} -m); combineTool.py -M MultiDimFit -m 125.09 --generate "d;D;n;;comb_${M}_observed.root,data_obs,observed;comb_${M}_prefit_asimov.root,toys/toy_asimov,prefit_asimov;comb_${M}_postfit_asimov.root,toys/toy_asimov,postfit_asimov" "freezeNuisanceGroups;n;;,nominal;sigTheory,fr.sigTheory;all,fr.all" $(./getPOIs.py ${M} -g) --redefineSignalPOIs $(./getPOIs.py ${M} -p) --floatOtherPOIs 1 --useAttributes 1 --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${M}  --snapshotName "MultiDimFit" --skipInitialFit --algo grid --points 39 --split-points 5 --job-mode condor --sub-opts='+JobFlavour = "longlunch"' --task-name ${M}_scans --dry-run; done`


## hadd
`START=${PWD}; for M in A1_ttH A1_ttH_5D; do for W in observed prefit_asimov postfit_asimov; do for T in nominal fr.all fr.sigTheory; do for P in $(./getPOIs.py ${M} -P); do hadd -k -f scan.${M}.${W}.${T}.${P}.root higgsCombine.${M}.${W}.${T}.${P}.POINTS.*.root; done; done; done; done`

## plotting

Copy hadd'ed output from above to CombineHarvester/HIG17031. From that directory, run:

`INPUT=./; for M in A1_ttH A1_ttH_5D; do for W in observed prefit_asimov postfit_asimov; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_full_split_${W}_${M}_${P} --POI ${P} --model ${M} --others \"${INPUT}/scan.${M}.${W}.fr.sigTheory.${P}.root:Freeze Sig. Th.:2\" \"${INPUT}/scan.${M}.${W}.fr.all.${P}.root:Freeze Exp.+Bkg.Th.+Sig.Th.:8\" --breakdown "SigTh,Exp,Stat" --json ${W}.json --translate pois.json --meta "Types:${W},Scans:full_split,POIs:${P}" -m ${INPUT}/scan.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --no-input-label; done; done; done`

`INPUT=./; for M in A1_ttH A1_ttH_5D; do for W in observed prefit_asimov postfit_asimov; do case ${W} in prefit_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_signif_${W}_${M}_${P} --POI ${P} --model ${M} --json ${W}.json --translate pois.json --meta "Types:${W},Scans:significance,POIs:${P}" -m ${INPUT}/scan.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 30 --chop 30 ${EXTRA} --no-input-label --signif; done; done; done`


## impacts

# Per-channel workspaces
`for M in A1; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do combineTool.py -M T2W -i comb_2017_mu_${CARD}_ttHComb.txt -o comb_${CARD}_${M}.root  -m 125 -P HiggsAnalysis.CombinedLimit.LHCHCGModels:${M} --PO dohmm=1 --for-fits --job-mode interactive; done; done`

`for M in A1_ttH; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do combineTool.py -M MultiDimFit -m 125.09 -d comb_${CARD}_$(./getPOIs.py ${M} -m).root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --generate "t;n;toysFrequentist;;,observed,;-1,prefit_asimov," --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${CARD}.${M} --job-mode interactive --dry-run; done; done`

`for M in A1_ttH; do for CARD in hgg hzz4l tth_hbb_hadronic tth_hbb_leptonic tth_htt tth_multilepton; do for TYPE in observed prefit_asimov; do mv higgsCombine.${CARD}.${M}.${TYPE}.MultiDimFit.mH125.09*.root comb_${CARD}_${M}_${TYPE}.root; done; done; done`

## Run the impacts for the prefit_asimov
`for M in A1_ttH A1_ttH_5D; do combineTool.py -M Impacts -m 125.09 --allPars --doFits --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${M}_prefit_asimov.root -D toys/toy_asimov --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV$(./getPOIs.py ${M} -F) --job-mode condor --sub-opts='+JobFlavour = "workday"' --task-name comb_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --merge 4; done`

## And for the data
`for M in A1_ttH A1_ttH_5D; do combineTool.py -M Impacts -m 125.09 --allPars --doFits --splitInitial --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameterRanges $(./getPOIs.py ${M} -r):CMS_hww_DYttnorm0j=0,2:CMS_hww_DYttnorm1j=0,2:CMS_hww_DYttnormvbf=0,2:CMS_hww_DYttnormvh2j=0,2:CMS_hww_Topnorm0j=0,2:CMS_hww_Topnorm0jsf=0,2:CMS_hww_Topnorm1jsf=0,2:CMS_hww_Topnormvbf=0,2:CMS_hww_Topnormvh2j=0,2:CMS_hww_WWnorm1jsf=0,3:CMS_hww_WWnormvbf=0,3:CMS_hww_WWnormvh2j=0,3:CMS_hww_WZ3lnorm=0,2:CMS_hww_ZZ4lnorm=0,2:CMS_hww_Zg3lnorm=0,3:SF_TT_Wln=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Wj0b_Wln=0.5,1.5:SF_Wj2b_Wln=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_norm_high_Zll=0.0,2.0:SF_Zj1b_norm_low_Zll=0.0,2.0:SF_Zj2b_norm_high_Zll=0.0,2.0:SF_Zj2b_norm_low_Zll=0.0,2.0:bgnorm_ddQCD_fh_j7_t3=0.5,1.5:bgnorm_ddQCD_fh_j7_t4=0.5,1.5:bgnorm_ddQCD_fh_j8_t4=0.5,1.5:bgnorm_ddQCD_fh_j9_t4=0.5,1.5 -d comb_${M}_observed.root -D data_obs --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --snapshotName MultiDimFit --robustFit 1 -n comb_observed_${M} --freezeParameters MH,pdfindex_TTHHadronicTag_13TeV,pdfindex_TTHLeptonicTag_13TeV$(./getPOIs.py ${M} -F) --job-mode condor --sub-opts='+JobFlavour = "workday"' --task-name comb_observed_${M}_impacts --X-rtd FITTER_DYN_STEP --setCrossingTolerance 0.001 --merge 4; done`

`for M in A1_ttH A1_ttH_5D; do for P in $(../getPOIs.py ${M} -P); do python ../../CombineTools/scripts/plotImpacts.py -i impacts_comb_observed_${M}_extra.json -o impacts_comb_observed_${M}_${P} --transparent --per-page 25 --translate ../summer2017/couplings/pois.json --POI ${P} --checkboxes; done; done`