
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

Build the workspace using SM template only in the 0-jet and boosted categories:

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/test/cmb/* -o ws.root --parallel 8 --PO sm_fix`

# Run maximum liklihood scan

Worspaces are created with 4 free parameters kappag, kappaW, kappaZ, mutautau and alpha. The first 4 parameters are used to float the ggH, VBF and VH rates.
By using the option --freezeNuisances these parameters can be prevented from floating in the fit this can be used to change how the VBF/VH background is treated in the fit e.g. VBF cross-section taken as SM or not.
To take VBF/VH cross-section as SM in both rate and shape use:
    `--freezeNuisances kappaW,kappaZ`
To take the H->tautau BR as SM use:
    `--freezeNuisances mutautau`

To scan alpha:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-90,90  --redefineSignalPOIs alpha  -d output/cp130219/cmb/125/ws.root --algo grid  --there -n .alpha --floatOtherPOIs 1 --points=37 --alignEdges 1 -t -1`

To scan mu:
We need to freeze tautau BR to 1 as the fit has no sensitivity to muggH it only has sensitivity to muggH*mutautau so by setting mutautau to 1 we effecitivly just get one rate parameter that scales the XS*BR
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muggH=1 --setPhysicsModelParameterRanges muggH=-0.1,3 --points 20 --redefineSignalPOIs muggH --freezeNuisances mutautau -d ws.root --algo grid -t -1 --there -n .mu --floatOtherPOIs 1`

To run on IC batch use (1 point per job):
 `--job-mode 'SGE' --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --split-points 1`
To run on lx batch use:
  `--job-mode lxbatch --sub-opts '-q 1nh --split-points 1'

Run 2D liklihood scan of mu vs alpha using:
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muggH=1,alpha=0 --freezeNuisances mutautau --setPhysicsModelParameterRanges alpha=-90,90:muggH=0,2.5 --redefineSignalPOIs alpha,muggH -d output/cp261118_nobbb/cmb/125/ws.root --there -n ".2DScan" --points 2000 --algo grid -t -1 --parallel=8 --alignEdges`

# Plot scan

1D scans can be plotted using scripts/plot1DScan.py script.
To plot alpha:
    `python scripts/plot1DScan.py --main=output/test/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root --POI=alpha --output=alpha --no-numbers --no-box --x_title="#alpha_{hgg} (#circ)" --y-max=2.5`

Plot 1D scan of mu:

  python scripts/plot1DScan.py --main=output/test/cmb/125/higgsCombine.mu.MultiDimFit.mH125.root --POI=muggH --output=muggH --no-numbers --no-box --x_title="#mu_{ggH}^{#tau#tau}" --y-max=12

2D scans can be plotted using scripts/plotMultiDimFit.py script:

    `python scripts/plotMultiDimFit.py --title-right="77.8 fb^{-1} (13 TeV)" --cms-sub="" --mass 125 -o mu_vs_alpha output/cp281118_nobbb/cmb/125/higgsCombine.2DScan.MultiDimFit.mH125.root --x-min=-90 --x-max=90`


## Impacts

cd into output directory:
  `cd output/jes_study_dphi_split_jes`

First do initial fit:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --doInitialFit --robustFit 1 -t -1 --parallel 8 --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-90,90 --freezeNuisances mutautau --floatOtherPOIs 1`

Run the fits for all nuisance parameters:

  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 --robustFit 1 -t -1 --minimizerAlgoForMinos Minuit2,Migrad --doFits --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP  --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-90,90 --freezeNuisances mutautau`

Run on lx batch system using `--job-mode lxbatch --sub-opts '-q 1nh' --merge 2`
Run on ic batch using `--job-mode 'SGE'  --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --merge=2`

Collect results:
  
  `combineTool.py -M Impacts -d cmb/125/ws.root -m 125 -o impacts.json`

Make impact plot:

  `plotImpacts.py -i impacts.json -o impacts`


## Make post-fit plots

Run fit:
   combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs muggH  -d output/cp110219/htt_01jet/125/ws.root --algo none --there -n .muggH.plots --floatOtherPOIs 1  --saveFitResult

Run postfitshapes:
   PostFitShapesFromWorkspace -m 125 -d output/cp110219/htt_01jet/125/combined.txt.cmb -w output/cp110219/htt_01jet/125/ws.root -o shapes_unblinding_01jets.root --print --sampling --postfit -f output/cp110219/htt_01jet/125/multidimfit.muggH.plots.freeze.root:fit_mdf

Run with (some) systematics frozen
Do fit and store workspace
  'combineTool.py -m 125 -M MultiDimFit  --redefineSignalPOIs alpha -d output/cp260219/cmb/125/ws.root --algo none  --there -n .saveWS  --saveWorkspace'

Now run scans freezing all systematics with "--freezeNuisances all" - can also freeze individual systematics or groups
  'combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-90,90  --redefineSignalPOIs alpha  -d output/cp260219/cmb/125/higgsCombine.saveWS.MultiDimFit.mH125.root --algo grid --there -n .alpha.nosyst2 --floatOtherPOIs 1 --points=37 --alignEdges 1 --freezeNuisances all --snapshot MultiDimFit'

can also do the following to freeze theory uncertanties only:

combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters alpha=0 --setPhysicsModelParameterRanges alpha=-90,90  --redefineSignalPOIs alpha  -d output/cp260219/cmb/125/higgsCombine.saveWS.MultiDimFit.mH125.root --algo grid --there -n .alpha.notheory --floatOtherPOIs 1 --points=37 --alignEdges 1  --snapshot MultiDimFit --freezeNuisances CMS_scale_gg_13TeV,CMS_FiniteQuarkMass_13TeV,CMS_PS_ggH_13TeV,CMS_UE_ggH_13TeV,BR_htt_THU,BR_htt_PU_mq,BR_htt_PU_alphas,QCDScale_ggH,QCDScale_qqH,QCDScale_WH,QCDScale_ZH,pdf_Higgs_WH,pdf_Higgs_ZH,pdf_Higgs_gg,pdf_Higgs_qq,CMS_ggH_mig01,CMS_ggH_mig12 --job-mode 'SGE' --prefix-file ic --sub-opts "-q hep.q -l h_rt=0:180:0" --split-points 1 --task-name alpha.notheory
