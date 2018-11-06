
# creating datacards
    
To create datacards first run morphing:    

    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D"`

By default this only uses 2016 data at the moment. To run on 2017 data use option --era=2017. To combine 2016 and 2017 use option --era="2016,2017"

To not include shape systematics use the option:
    `--no_shape_systs=true`

# Building the workspaces:

Build the to fit alpha with ggH rate floating workspace using

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/test/cmb/* -o ws.root --parallel 8`

Build the to fit mu vs alpha build workspace using

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/test/cmb/* -o ws.root --parallel 8 --PO fit_2D`

# Run maximum liklihood scan

Worspaces are created with 4 free parameters kappag, kappaW, kappaZ, mutautau and alpha. The first 4 parameters are used to float the ggH, VBF and VH rates.
By using the option --freezeNuisances these parameters can be prevented from floating in the fit this can be used to change how the VBF/VH background is treated in the fit e.g. VBF cross-section taken as SM or not.
To take VBF/VH cross-section as SM in both rate and shape use:
    `--freezeNuisances kappaW,kappaZ`
To take the H->tautau BR as SM use:
    `--freezeNuisances mutautau`

To scan alpha:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-1,1 --points 20 --redefineSignalPOIs alpha  -d output/test/cmb/125/ws.root --algo grid -t -1 --there -n .alpha --floatOtherPOIs 1`

To run on IC batch use (1 point per job):
 `--job-mode 'SGE' --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --split-points 1`
To run on lx batch use:
  `--job-mode lxbatch --sub-opts '-q 1nh --split-points 1'

Run 2D liklihood scan of mu vs alpha using:
  (this needs to be updated)
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0,f=0 --freezeNuisances f --setPhysicsModelParameterRanges alpha=0,1 --redefineSignalPOIs alpha,muF -d output/cp310118/cmb/125/ws.root --there -n ".2DScan" --points 500 --algo grid -t -1 --parallel=8 `

# Plot scan

1D scans can be plotted using scripts/plot1DScan.py script.
To plot alpha:
    `python scripts/plot1DScan.py --main=output/test/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root --POI=alpha --output=alpha --no-numbers --no-box --x_title="#alpha_{hgg} (#circ)" --y-max=2.5`

Plot 1D scan of mu:

  python scripts/plot1DScan.py --main=output/test/cmb/125/higgsCombine.mu.MultiDimFit.mH125.root --POI=muggH --output=muggH --no-numbers --no-box --x_title="#mu_{ggH}^{#tau#tau}" --y-max=6

2D scans can be plotted using scripts/plotMultiDimFit.py script:

    `python scripts/plotMultiDimFit.py --title-right="35.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --mass 125 -o muF_vs_alpha output/cp310118/cmb/125/higgsCombine.2DScan.MultiDimFit.mH125.root`


## Impacts

cd into output directory:
  `cd output/jes_study_dphi_split_jes`

First do initial fit:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --doInitialFit --robustFit 1 -t -1 --parallel 8 --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-1,1`

Run the fits for all nuisance parameters:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --robustFit 1 -t -1 --minimizerAlgoForMinos Minuit2,Migrad --doFits --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP  --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-1,1`

Run on lx batch system using `--job-mode lxbatch --sub-opts '-q 1nh' --merge 2`
Run on ic batch using `--job-mode 'SGE'  --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --merge=2`

Collect results:
  
  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 -o impacts.json`

Make impact plot:

  `plotImpacts.py -i impacts.json -o impacts`
