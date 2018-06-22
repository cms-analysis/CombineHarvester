# THIS NEEDS FURTHER UPDATES - work-in-progress

# Link to the CombineHarvester twiki:
[CombineHarvester twiki](http://cms-analysis.github.io/CombineHarvester/index.html)


# Creating datacards

    MorphingSM2017 --input_folder_mt=Vienna/ --input_folder_et=Vienna/ --input_folder_tt=Vienna/ --input_folder_em=Vienna/ --input_folder_mm=Vienna/ --input_folder_ttbar=Vienna/  --channel="mt" --jetfakes=false --postfix="-ML" --auto_rebin=true --real_data=false --output_folder test &>log_dc.txt
    MorphingSM2017 --input_folder_mt=Vienna/ --channel="mt" --jetfakes=false --postfix="-ML" --auto_rebin=true --real_data=false --output_folder test &>log_dc.txt   #same for just one channel
    MorphingSM2017 --input_folder_mt=Vienna/ --input_folder_et=Vienna/ --channel="mt,et" --jetfakes=false --postfix="-ML" --auto_rebin=true --real_data=false --output_folder test &>log_dc.txt   #same for a few channels


# Building the workspaces:

    cd output/test
    combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 8 &>log_ws.txt   #remove directories within curly brackets as desired


# Calculating limits and significances:
    combineTool.py -M Asymptotic -d */*/workspace.root --there -n .limit -t -1 --parallel 8
    combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --expectSignal=1   #a-priori Asimov
    combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --toysFrequentist --expectSignal 1 #a-posteriori Asimov


# run MaxLikelihoodFit

    combine -M MaxLikelihoodFit cmb/125/workspace.root --robustFit=1 -m 125 --minimizerAlgoForMinos=Minuit2,Migrad  --rMin 0.3 --rMax 2.0 --name ".res"
    

# making the pulls

    python ../../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py  mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt


# postfit plots

    PostFitShapes -o postfit_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print -d cmb/125/combined.txt.cmb
    

# Computing the Impact (blinded)

    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8
    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --doFits -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP
    combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 -o impacts.json
    plotImpacts.py -i impacts.json -o impacts
