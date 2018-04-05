
# creating datacards
    
To create datacards using Aachen groups categorisation use:    

    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true`

To create datacards using IC categorisation and unrolled 2D distributions of m_sv vs sjdphi/D0star for the dijet categories use:

    `MorphingSMCP2016 --output_folder="cp310118" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true --dijet_2d=true`    

To not include shape systematics use the option:
    `--no_shape_systs=true`

# Building the workspaces:

Build the workspace using

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp310118/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8`
   
Currently since we use JHU sample the ggH XS does not depend on alpha. In MG5 XS depends on alpha like cos^2(alpha) + (3/2)^2*sin^2(alpha). To scale the ggH XS according to this function create the workspace using:

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp310118/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8 --PO constrain_ggHYield`

To scale the lumi by a factor X use the option:
    `--PO lumiScale=X`
when creating the worspace

# Run maximum liklihood scan

Worspaces are created with 4 free parameters muF, muV, alpha, and f. muF is the rate parameter for ggH, muV is the rate parameter for VBF/VH, alpha defines the CP mixing for ggH (note alpha is in units of pi/2 -> SM:alpha=0, PS:alpha=1), and f defines the CP mixing for VBF (SM:f=0, PS:f=1) 
By using the option --freezeNuisances these parameters can be prevented from floating in the fit this can be used to change how the VBF background is treated in the fit e.g. VBF taken as SM or not.
To take VBF as SM in both rate and shape use:
    `--freezeNuisances f,muV`
To take the VBF shape as SM and float the rate use:
    `--freezeNuisances f`
Not using the --freezeNuisances will float both the VBF rate and shape by default.

To scan alpha:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0,f=0 --freezeNuisances f --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp310118/cmb/125/ws.root --algo grid -t -1 --there -n .alpha`


To scan muF:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0,f=0 --freezeNuisances f --setPhysicsModelParameterRanges muF=0,4 --points 20 --redefineSignalPOIs muF  -d output/cp310818/cmb/125/ws.root --algo grid -t -1 --there -n .muF`

To scan alpha including the constrain on the XS use:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0,f=0 --freezeNuisances f,muF --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp310118/cmb/125/ws.root --algo grid -t -1 --there -n .alpha`

Run 2D liklihood scan of muF vs alpha using:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0,f=0 --freezeNuisances f --setPhysicsModelParameterRanges alpha=0,1 --redefineSignalPOIs alpha,muF -d output/cp310118/cmb/125/ws.root --there -n ".2DScan" --points 500 --algo grid -t -1 --parallel=8`

# Plot scan

1D scans can be plotted using scripts/plot1DScan.py script.
To plot alpha:
    `python scripts/plot1DScan.py --main=higgsCombine.Test.MultiDimFit.mH125.root --POI=alpha --output=alpha --no-numbers --no-box --x_title="#alpha (#frac{#pi}{2})" --y-max=2.2`
To plot muF:
    `python scripts/plot1DScan.py --main=higgsCombine.Test.MultiDimFit.mH125.root --POI=muF --output=muF --no-numbers --no-box --x_title="#mu_{F}"`

2D scans can be plotted using scripts/plotMultiDimFit.py script:

    `python scripts/plotMultiDimFit.py --title-right="35.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --mass 125 -o muF_vs_alpha output/cp310118/cmb/125/higgsCombine.2DScan.MultiDimFit.mH125.root`


## Impacts

cd into output directory:
  `cd output/jes_study_dphi_split_jes`

First do initial fit:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --doInitialFit --robustFit 1 -t -1 --parallel 8 --setPhysicsModelParameters muF=1,muV=1,f=0,alpha=0 --setPhysicsModelParameterRanges muF=0,4:muV=0,2:alpha=-1,1:f=-1,1`

Run the fits for all nuisance parameters:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --robustFit 1 -t -1 --minimizerAlgoForMinos Minuit2,Migrad --doFits --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP  --setPhysicsModelParameters muF=1,muV=1,f=0,alpha=0 --setPhysicsModelParameterRanges muF=0,4:muV=0,2:alpha=-1,1:f=-1,1`

Run on lx batch system using `--job-mode lxbatch --sub-opts '-q 1nh' --merge 2`
Run on ic batch using `--job-mode 'SGE'  --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --merge=2`

Collect results:
  
  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 -o impacts.json`

Make impact plot:

  `plotImpacts.py -i impacts.json -o impacts`
