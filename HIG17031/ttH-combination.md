# ttH combination

## Make the combined card

`python prepareComb.py --ttH`

## text2workspace

`for M in A1; do combineTool.py -M T2W -i comb_2017_mu_ttH.txt -o comb_ttH_${M}.root  -m 125 -P HiggsAnalysis.CombinedLimit.LHCHCGModels:${M} --PO dohmm=1 --for-fits --job-mode interactive; done`

## Adding the attributes

`for M in A1; do python addAttributes.py -i comb_ttH_${M}.root --json attributes.json -o comb_ttH_${M}_attr.root | tee attr_ttH_${M}.log; done`

## Making the prefit asimov

The A1_ttH model has a single POI, `mu_XS_ttH`. All other signal processes, including tHq and tHW, are fixed to 1.

`for M in A1_ttH; do combineTool.py -M MultiDimFit -m 125 -d comb_ttH_$(./getPOIs.py ${M} -m)_attr.root --redefineSignalPOIs $(./getPOIs.py ${M} -p) --setParameters $(./getPOIs.py ${M} -s) --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) -t -1 --saveToys --saveWorkspace --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${M}.prefit_asimov --job-mode lxbatch --sub-opts='-q 1nd -R "rusage[mem=4000]"' --task-name ${M}.prefit_asimov --dry-run; done`

## Rename
`for M in A1_ttH; do for TYPE in prefit_asimov; do mv higgsCombine.${M}.${TYPE}.MultiDimFit.mH125.123456.root comb_${M}_${TYPE}.root; done; done`

## Scans

The `--generate` command causes the combine command to be repeated with different sets of options. Multiple arguments can be specified, and all possible combinations will be generated. In this case the argument lets us loop through different input workspaces, the second through freezing different nuisance groups, and the third through the different model POIs. The syntax of these arguments is:

    arg1;arg2;...;argN;;val1_1,val2_1,...,valN_1;...;val1_M,val2_M,...,valN_M

The argX statements should be combine options given without the leading `-` or `--`. This generates a loop where the arguments will be set like:

    combine --arg1=val1_1 --arg2=val2_1 ... --argN=valN_1
    combine --arg1=val1_2 --arg2=val2_2 ... --argN=valN_2
    ...
    combine --arg1=val1_M --arg2=val2_M ... --argN=valN_M

The `name` or `n` option is treated specially: the given values will be appended to the existing name instead of replacing it altogether, therefore it can appear in multiple arguments. Note that `:` can also be used instead of `;` as the separator, and `,,` can be used instead of `,` to separate the valX_Y if these themselves need to contain a comma. If a valX_Y is an empty string then no corresponding option or argument will be inserted for that particular combine call.

`for M in A1_ttH; do MOD=$(./getPOIs.py ${M} -m); combineTool.py -M MultiDimFit -m 125 --generate "d;D;n;;comb_${M}_prefit_asimov.root,toys/toy_asimov,prefit_asimov" "freezeNuisanceGroups;n;;,nominal;sigTheory,fr.sigTheory;all,fr.all" $(./getPOIs.py ${M} -g) --redefineSignalPOIs $(./getPOIs.py ${M} -p) --useAttributes 1 --setParameterRanges $(./getPOIs.py ${M} -r) --freezeParameters MH$(./getPOIs.py ${M} -F) --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH -n .${M}  --snapshotName "MultiDimFit" --skipInitialFit --algo grid --points 20 --split-points 1 --job-mode lxbatch --sub-opts='-q 1nd' --task-name ${M}_scans --dry-run; done`

## hadd
`START=${PWD}; for M in A1_ttH; do for W in prefit_asimov; do for T in nominal fr.all fr.sigTheory; do for P in $(./getPOIs.py ${M} -p); do hadd -k -f scan.${M}.${W}.${T}.${P}.root higgsCombine.${M}.${W}.${T}.${P}.POINTS.*.root; done; done; done; done`

## plotting
`INPUT=./; for M in A1_ttH; do for W in prefit_asimov; do case ${W} in *_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -p); do eval python scripts/plot1DScan.py -o scan_full_split_${W}_${M}_${P} --POI ${P} --model ${M} --others \"${INPUT}/scan.${M}.${W}.fr.sigTheory.${P}.root:Freeze Sig. Th.:2\" \"${INPUT}/scan.${M}.${W}.fr.all.${P}.root:Freeze Exp.+Bkg.Th.+Sig.Th.:8\" --breakdown "SigTh,Exp,Stat" --json ${W}.json --translate pois.json --meta "Types:${W},Scans:full_split,POIs:${P}" -m ${INPUT}/scan.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 10 ${EXTRA} --no-input-label; done; done; done`

`INPUT=./; for M in A1_ttH; do for W in prefit_asimov; do case ${W} in *_asimov) EXTRA='--main-label "SM Expected" --main-color 4';; *) EXTRA="";; esac; for P in $(./getPOIs.py ${M} -p); do eval python scripts/plot1DScan.py -o scan_signif_${W}_${M}_${P} --POI ${P} --model ${M} --json ${W}.json --translate pois.json --meta "Types:${W},Scans:full_split,POIs:${P}" -m ${INPUT}/scan.${M}.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 30 --chop 30 ${EXTRA} --no-input-label --signif; done; done; done`