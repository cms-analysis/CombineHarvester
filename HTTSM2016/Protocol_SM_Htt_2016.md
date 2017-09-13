
# Link to the CombineHarvester twiki:
[CombineHarvester twiki](http://cms-analysis.github.io/CombineHarvester/index.html)


# Checkout the CombineHarvester
    export SCRAM_ARCH=slc6_amd64_gcc481 (bash) or  setnev SCRAM_ARCH slc6_amd64_gcc481 (tcsh)
    scram project CMSSW CMSSW_7_4_7
    cd CMSSW_7_4_7/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    //Check the recommended tag on link above, a tag &gt;= v5.0.2 is sufficient
    cd HiggsAnalysis/CombinedLimit
    git fetch origin
    git checkout v6.3.1
    cd ../..
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    cd CombineHarvester
    git checkout SM2016-dev
    scram b -j 8

    
    
#Get the shape
    cd CombineHarvester/HTTSM2016
    git clone https://:@gitlab.cern.ch:8443/cms-htt/SM-PAS-2016.git shapes  (from lxplus)
    git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes      (from elsewhere)
    git pull --rebase 

# creating datacards
    
    MorphingSM2016 --output_folder="Blinded25112016" --postfix="-2D" --control_region=1 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=true


# Building the workspaces:

    cd output/Blinded25112016
    combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 18


# Calculating limits:
    combineTool.py -M Asymptotic -d */*/workspace.root --there -n .limit --parallel 18


# Collect the output:
    combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json


# Plotting the limit:

        
    python ../../../plotLimits_SM2.py limits_{cmb,em,et,mt,tt}.json:exp0 --auto-style --cms-sub Preliminary  -o lim_compare
    python ../../../plotLimits_SM2.py limits_cmb.json  --auto-style --cms-sub Preliminary     -o lim_expected_cmb
    python ../../../plotLimits_SM2.py limits_tt.json  --auto-style --cms-sub Preliminary     -o lim_expected_tt
    python ../../../plotLimits_SM2.py limits_mt.json  --auto-style --cms-sub Preliminary     -o lim_expected_mt
    python ../../../plotLimits_SM2.py limits_et.json  --auto-style --cms-sub Preliminary     -o lim_expected_et
    python ../../../plotLimits_SM2.py limits_em.json  --auto-style --cms-sub Preliminary     -o lim_expected_em


# run MaxLikelihoodFit

    combine -M MaxLikelihoodFit cmb/125/workspace.root --robustFit=1 --minimizerAlgoForMinos=Minuit2,Migrad  --rMin 0.5 --rMax 1.5 
    


# making the pulls

    python ../../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py  mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt


# postfit plots

    PostFitShapes -o postfit_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print -d cmb/125/combined.txt.cmb
    

# Computing the Impact

    [Blinded]combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8
    [UnBlinded]combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --doInitialFit --robustFit 1 --rMin 0.5 --rMax 1.5  --parallel 8
    ---------------------------
    [Blinded]combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --doFits -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP
    [UnBlinded]combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --doFits -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP

    *Note*: Instead of the above line one can run the jobs via lxbatch:
    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --doFits -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --job-mode lxbatch --task-name lxbatch-test --sub-opts='-q 8nh' --merge 10 --dry-run   (--dry-run option let you check how the jobs will look like before submiting to lxbatch)  
    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --doFits --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --rMin 0.5 --rMax 1.5  --job-mode lxbatch --task-name lxbatch-test --sub-opts='-q 8nh' --merge 5 
    ---------------------------
    # Impact for limited number of nuisance parameters 

   combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --doFits  --minimizerAlgoForMinos Minuit2,Migrad --rMin 0.5 --rMax 1.5  --parallel 18 --named CMS_scale_t_et_13TeV,CMS_scale_t_mt_13TeV --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP

    ---------------------------

    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 -o impacts.json
    plotImpacts.py -i impacts.json -o impacts


# Computing the expected significance:

    [PreFit Asimov]combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --expectSignal=1
    [PostFit Asimov]combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --toysFrequentist --expectSignal 1
    [PostFit]combine -M ProfileLikelihood --significance cmb/125/workspace.root 

# Computing the expected significance per channel per category (including constraints from all channels)

    cd scripts
    sh channelCompatibilityCheck.sh


# Making the pvalue plot:

    cp ../../../scripts/runPvalue.sh .
    sh  runPvalue.sh .

# Making the S/S+B weighted plot

    cp ../../../scripts/runSBWeighted.sh .
    sh runSBWeighted.sh






