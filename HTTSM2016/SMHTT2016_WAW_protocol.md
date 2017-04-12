To perform exclusion limits and signal significance calculations perform following steps:

Get HiggsAnalysis-CombinedLimit and CombineHarvester in a way described in Protocol_SM_Htt_2016.md.
Some minor changes adapting the code to WAW analysis is in apyskir's repo. Get it from:
git clone git@github.com:apyskir/CombineHarvester.git
cd CombineHarvester
git checkout SM2016-dev

You can get files from other groups:
Get the shapes
cd CombineHarvester/HTTSM2016 
git clone https://:@gitlab.cern.ch:8443/cms-htt/SM-PAS-2016.git shapes #(from lxplus) 
git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes #(from elsewhere) git pull --rebase

Run HTTAnalysis

Run script makeShapesUnrolled.py in RootAnalysis/HTTAnalyzer. Inside the script update directories of input files RootAnalysis_AnalysisMuTau.root and RootAnalysis_AnalysisTT.root.
The script produces input files to MorphingSM2016_WAW.

Copy htt_mt.inputs-sm-13TeV-2D.root and htt_tt.inputs-sm-13TeV-2D.root to $CMSSW_BASE/src/CombineHarvester/HTTSM2016/shapes/WAW directory.


Use CombineHarvester:

Create datacards and workspace:
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2016/
MorphingSM2016_WAW --output_folder="YourFavoriteFolderName" --postfix="-2D" --control_region=1 --manual_rebin=false --real_data=true --mm_fit=false --ttbar_fit=false
cd output/YourFavoriteFolderNamebl
combineTool.py -M T2W -i {cmb,mt,tt}/* -o workspace.root --parallel 8

Calculate limits:
combineTool.py -M Asymptotic -d */*/workspace.root --there -n .limit --parallel 8
combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json

plotLimits.py limits_{cmb,mt,tt}.json:exp0 --auto-style -o lim_compare
plotLimits.py limits_cmb.json --auto-style   -o lim_expected_cmb 

python ../../plotLimits_SM2.py limits_{cmb,mt,tt}.json:exp0 --auto-style --cms-sub Preliminary  -o lim_compare
python ../../plotLimits_SM2.py limits_cmb.json  --auto-style --cms-sub Preliminary --show exp    -o lim_expected_cmb
python ../../plotLimits_SM2.py limits_tt.json  --auto-style --cms-sub Preliminary --show exp    -o lim_expected_tt
python ../../plotLimits_SM2.py limits_mt.json  --auto-style --cms-sub Preliminary --show exp    -o lim_expected_mt

Max likelihood fit:
combine -M MaxLikelihoodFit cmb/125/workspace.root --robustFit=1 --minimizerAlgoForMinos=Minuit2,Migrad  --rMin 0.5 --rMax 1.5 --expectSignal=1

Significances:
combine -M ProfileLikelihood --significance cmb/125/workspace.root --expectSignal=1

Pre- and postfit shapes:
PostFitShapes -o postfit_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print -d cmb/125/combined.txt.cmb
root -b plotPostFit.C

Pulls:
python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py  mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt


NOTE: in order to perform fits etc. on Asimov dataset add "-t -1" in the command line
