# MSSM protocol

This file collects up to date instructions for running the 2016 13 TeV MSSM statistical results. For more detailed information on Combine Harvester please see the documentation at

http://cms-analysis.github.io/CombineHarvester/

## Setting up datacards

The default options to `MorphingMSSMFull2016` have been set to those used to produce the final unblinded results. The following additional options may be of interest:

 - `--bbH_nlo=false`: Revert to the old LO pythia samples for bbH
 - `--ggHatNLO=false`: Revert to the unweighted LO pythia for ggHatNLO
 - `--auto_rebin=true`: enable the auto-rebinning of the templates
 - `--real_data=false`: replace the real data with a background-only asimov
 - `--jetfakes=false`: Use the classic W and QCD background methods
 - `--control_region=1`: Add the W and QCD control regions

### Model independent limits

`MorphingMSSMFull2016 --output_folder="mssm_201017" -m MH --manual_rebin=true`

*FOR SYNC COMPARISONS ONLY*: to make sync comparisons we need to also check the relative differences between observed limits and so --real_data should be set to true in this case. Be very careful and under absolutely no circumstances use directories set up this way for anything other than sync comparisons.

#### Gluon fusion NLO treatment

**SM fractions**

By default the t-only, b-only and interference components of the ggH process are summed in the mass-dependent SM ratio (i.e. assuming Yt=Yb=1). It is possible to select the boson for which these ratios are taken with the `--mod_indep_h [h/H/A]` option. The default is `h`. The ratios for `h` and `H` are identical, whereas there is a small difference for `A` due to the CP-odd nature of the interaction.

**Custom fractions**

However it is also possible to control the fractions directly by setting the option `-- mod_indep_use_sm 0`. In this case two free parameters are introduced: `ggHt_frac` and `ggHb_frac`. These are the fractions of the t-only and b-only contributions respectively. The interference contribution is defined automatically as `1 - ggHt_frac - ggHb_frac`.  The values should be set explicitly when running combine, e.g.: `--setPhysicsModelParameters ggHt_frac=X,ggHb_frac=Y`.


### Model dependent limits (asymptotic)

**MSSMvsBkg**

`MorphingMSSMFull2016 --output_folder="mssm_201017_MSSMvsBkg_mhmodp" --manual_rebin=true`

If not using the argument `-m MH`, the code will create datacards for all three Higgs bosons as required for model dependent limits.

**MSSMvsSM**

`MorphingMSSMFull2016 --output_folder="mssm_201017_MSSMvsSM_mhmodp" --manual_rebin=true -h "signal_SM125"`
`
### Model independent limits with SM H as background

**DO NOT do this until binning for manual_rebin is set to something sensible.**

`MorphingMSSMFull2016 --output_folder="mssm_201017_SMHbkg" -m MH --manual_rebin=true -h "bkg_SM125"`

## Setting up workspaces

### Model independent limits (and 2D ggH-bbH limits)

`combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH.?$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017/*`

This will apply the text2workspace step recursively, setting up for every subdirectory and hence every channel-cat scenario. There are many different options to combineTool, but this particular set will create a "combined card" named combined.txt.cmb in each subdir, and a workspace named ws.root. The option `--parallel X` can be added to run `X` tasks simultaneously.

### Model dependent limits (MSSMvsSM or MSSMvsBkg)

`combineTool.py -M T2W -o "mhmodp.root" -P CombineHarvester.CombinePdfs.MSSM:MSSM --PO filePrefix=$PWD/shapes/Models/ --PO modelFiles=13TeV,mhmodp_mu200_13TeV.root,1 --PO MSSM-NLO-Workspace=$PWD/shapes/Models/higgs_pt_v3_mssm_mode.root [--PO debugOutput="mhmodp_mu200_13TeV_debug.root" --PO makePlots ] -i output/mssm_201017_mhmodp/*`

This will perform the same recursive application of text2workspace, this time applying the mhmodp physics model.

## Running the limits

### Model independent limits (also with SM Higgs as BG)

This can be done directly with combine, but again combineTool makes life a lot easier for us by allowing successive calls (with different choices of job submission, and parallelisation of calculations):

***ggPhi limits***

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json  --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_ggH -d output/mssm_201017/*/ws.root --there -n ".ggH"`

For the ggH limits we also add two additional lines for t-only and b-only coupling, using the datacards where the `-- mod_indep_use_sm 0` option was used as described above:

`combineTool.py -m "90,100,110,120,130" -M Asymptotic --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,ggHt_frac=1,ggHb_frac=0 --redefineSignalPOIs r_ggH -d output/mssm_201017_custom/cmb/ws.root --there -n ".ggH.tonly"`

`combineTool.py -m "90,100,110,120,130" -M Asymptotic --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,ggHt_frac=0,ggHb_frac=1 --redefineSignalPOIs r_ggH -d output/mssm_201017_custom/cmb/ws.root --there -n ".ggH.bonly"`

***bbPhi limits***

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json  --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_bbH -d output/mssm_201017/*/ws.root --there -n ".bbH"`

This goes to each subdirectory of output/mssm_120717/ (--there) and performs the combine calculation for the masses listed on the workspace. The combine output files are stored in the directories alongside the datacards. Note the option `--parallel X` allows you to run the calculations interactively with `X` in parallel, and e.g. `--job-mode 'lxbatch' --task-name 'mssm_ggH' --sub-opts '-q 1nh' --merge=4` could be used to instead run on  lxbatch, merging 4 masspoints into 1 job and submitting to the 1 hour queue.

**Collecting the output**

Once all calculations are complete, the results are collected into json files using:

`combineTool.py -M CollectLimits output/mssm_201017/*/higgsCombine.ggH*.root --use-dirs -o "mssm_201017_ggH.json"`

`combineTool.py -M CollectLimits output/mssm_201017/*/higgsCombine.bbH*.root --use-dirs -o "mssm_201017_bbH.json"`

This will place a json in the current directory, and append the string "mssm_201017_ggH" or "mssm_201017_ggH" to them. One will be placed for every subdir, so every channel-cat, combination requested will be available then for plotting.

When producing the limit with the SM Higgs as BG simply change the datacards/directories to run for accordingly.

*FOR SYNC COMPARISONS ONLY*: Run the limit calculation without the -t -1 option.

### Model dependent limits (asymptotic)

To run limits in MSSMvsBkg mode run the following command:

`combineTool.py -M AsymptoticGrid ./scripts/mssm_asymptotic_grid_mhmodp.json -d output/mssm_201017_mhmodp/cmb/mhmodp.root  --job-mode 'interactive' --task-name 'mssm_mhmodp'`

To run limits in MSSMvsSig mode run the additional options `--redefineSignalPOI x --setPhysicsModelParameters r=1 --freezeNuisances r` are required:

`combineTool.py -M AsymptoticGrid ./scripts/mssm_asymptotic_grid_mhmodp.json -d output/mssm_201017_mhmodp/cmb/mhmodp.root  --job-mode 'interactive' --task-name 'mssm_mhmodp' --redefineSignalPOI x --setPhysicsModelParameters r=1 --freezeNuisances r'`

(To run hMSSM scenario instead of mhmodp use mssm_asymptotic_grid_hMSSM.json)

The asymptotic grid mode reads in an input json to define a set of mA-tanb points to scan and perform the limit calculation for. This time the calculation is done once per workspace, since the script has a nice feature which is that if you call it multiple times with the same workspace and asymptotic grid it will check which points have already completed successfully and only run those remaining. This makes it really easy to top up the grid for a finer scan for example. Once all points are complete, on the final call the script will create asymptotic_grid.root file containing the results.

### Model dependent limits (MSSMvsSM hypothesis test)

**UPDATE ME**

`combineTool.py -M HybridNewGrid ./scripts/mssm_hybrid_grid_mhmodp.json --cycles 2 -d output/mssm_201017_mhmodp/cmb/mhmodp.root  --job-mode 'crab3' --task-name 'mssm_mhmodp_hybridgrid' --crab-area 'Jun7_Combine'`

The mssm_hybrid_grid.json file specifies ao the mA-tanb points to scan, for more info see CombineHarvester/docs/HybridNewGrid.md

Like in AsymptoticGrid mode, points can be added or more toys can be generated for points which haven't met the significance/number of toy requirements specified in mssm_hybrid_grid_mhmodp.json. To check the progress of points, copy the output files back over from dcache and run with --cycles 0, the output graphs can be added by adding the --output option. This will write out a file HybridNewGridMSSM.root

Note that mssm_hybrid_grid_mhmodp.json and mssm_hybrid_grid_hmssm.json are copied from the ICHEP analysis and the number of toys per cycle will probably have to be adjusted down as the fit is now more complex (lots of extra categories). Some points along the 2sigma contour will need 60 000 - 100 000 toys, so best to increase the number of cycles per submission as the number of points still to be scanned becomes smaller.

### ggH-bbH 2D limits (Asymptotic)

**UPDATE ME**

The 2D limits are run using combineTool to take advantage of the possibilty to run for multiple masses and submission.

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_ggH,r_bbH -d output/mssm_201017/cmb/ws.root --there -n ".ggH-bbH" --points 500 --algo grid`

This will create one job per mass point with 500 each. For batch-submission one can also specify the option "--split-points N" where N will be the maximum number of points per sub-job.

This workflow has also been tested on the grid (normal crab submission options). The run time for number of submitted points is still to be benchmarked. Note that the scannable boundaries in input/mssm_ggH_bbH_2D_boundaries.json are extremely wide, and still need to be adjusted

To get the point for the SM expectation one first needs to create a corresponding asimov dataset. This is done using combine and the setPhysicsModelParameters and saveToys options.

`combineTool.py -m "125" -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOI r_ggH,r_bbH -t -1 -d output/mssm_201017_SMHbkg/cmb/ws.root --there -n ".2D.ToyDataset.SM1" --algo none --saveToys`

The resulting asimov dataset can then be loaded in a second step and fitted using the POIs `r_ggH` and `r_bbH`. For this copy the toy file into the corresponding folder and run combine loading the toy from this file.

`cp output/mssm_070617_SMHbkg/cmb/higgsCombine.2D.ToyDataset.SM1.MultiDimFit.mH125.123456.root output/mssm_201017/cmb/higgsCombine.2D.ToyDataset.SM1.MultiDimFit.mH125.123456.root`

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOI r_ggH,r_bbH -t -1 -d output/mssm_201017/cmb/ws.root --there -n ".2D.SM1.bestfit" --algo none --toysFile higgsCombine.2D.ToyDataset.SM1.MultiDimFit.mH125.123456.root`

### ggH-bbH 2D limits (Feldman-Cousins)

Feldman Cousins regions are produced using combineTool's HybridNewGrid. You'll need one config file per mass point, for example at mH=700 GeV:

`combineTool.py -M HybridNewGrid ./scripts/mssm_hybrid_grid_FCInterval.json --cycles 2 -d output/mssm_201017/cmb/ws.root  --job-mode 'crab3' --task-name 'mssm_FCIntervals700' --crab-area 'Jul27_Combine'`

This will submit 2*700 toys for each point

After this is finished and you've retrieved and untarred all the output files, run, in the directory where you have all the output files:

`combineTool.py -M HybridNewGrid /FULL/PATH/TO/CH/AREA/scripts/mssm_hybrid_grid_FCInterval.json --cycles 0 -d /FULL/PATH/TO/CH/AREA/output/mssm_201017/cmb/ws.root  --output`

**Notes:**

 - Make sure the crab storage site is set correctly. This can be done e.g by creating a python file like CombineTools/scripts/custom_crab.py and adding, to the combineTool.py call above, --custom-crab ../CombineTools/scripts/custom_crab.py
 - The grids to be scanned for each mass point still need to be determined. Easiest is probably to run Asymptotic version first to determine reasonable bounds
 - Make sure you do not try to submit more than 10000 jobs in one crab task - if you end up creating a grid with more than 5000 points, cannot submit two cycles in one go - in that case should submit in multiple stages; perhaps by splitting the grid into smaller, disjoint grids and launch them in separate crab tasks, or by waiting for the first task to complete and then submit a second cycle. Do not simply run the above command twice with a different task name, as you will just generate the exact same set of toys twice.

Easiest way to get the best-fit value:

`combineTool.py -m "700" -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_ggH,r_bbH -d output/mssm_201017/cmb/ws.root --there -n ".ggH-bbH-bestfit"`

### Running model independent limits with signal injected

**Not been used for a long time, seek advice before trying this**

For generating the toys first of all a snapshot with the bestfit values for the BG+SM higgs hypothesis needs to be generated:

`combineTool.py -m 160 -M GenerateOnly --setPhysicsModelParameters r_ggH=0,r_bbH=0,r_SM=1 --freezeNuisances r_SM --redefineSignalPOI r_ggH,r_bbH -t -1 --toysFrequentist -d output/mssm_201017_withSM/cmb/ws_SM_and_MSSM.root --there -n ".InitalFit" --saveWorkspace`

Based on this snapshot (it is called clean) the toys can then be generated.

`combineTool.py -m "160"  -M GenerateOnly --setPhysicsModelParameters r_ggH=0,r_bbH=0 --snapshot clean --freezeNuisances r_SM --rerefineSignalPOI r_ggH,r_bbH -t 50 -d output/mssm_201017_withSM/cmb/higgsCombine.InitalFit.GenerateOnly.mH160.root --there -n ".Toys" -s 0 --saveToys`

As these toys are later on fitted in one job each, it is recommended to generate multiple of these smaller toy files (as usual the option -s can be modified to generate multiple files based on different seeds in one go)

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic --boundlist input/mssm_boundaries.json --freezeNuisances r_SM --redefineSignalPOI r_ggH -t 50 -d output/mssm_201017_withSM/cmb/ws_SM_and_MSSM.root --there -n ".ggH.0" --task-name "ggH.0" --toysFile higgsCombine.Toys.GenerateOnly.mH160.0.root --run observed`

`combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic --boundlist input/mssm_boundaries.json --freezeNuisances r_SM --redefineSignalPOI r_bbH -t 50 -d output/mssm_201017_withSM/cmb/ws_SM_and_MSSM.root --there -n ".bbH.0" --task-name "bbH.0" --toysFile higgsCombine.Toys.GenerateOnly.mH160.0.root --run observed`

Once all jobs are done the results can be collected into a single json file. For this the corresponding quantiles of the distribution of toys is evaluated.

`combineTool.py -M CollectLimits output/mssm_201017_withSM/cmb/higgsCombine.ggH.*.root --use-dirs -o "mssm_201017_BlueBand_ggH.json"`

`combineTool.py -M CollectLimits output/mssm_201017_withSM/cmb/higgsCombine.bbH.*.root --use-dirs -o "mssm_201017_BlueBand_bbH.json"`

## Plotting

### Model independent limits

The usual Brazil band plots can be made using this script, for e.g. the mutau channel:

`python scripts/plotMSSMLimits.py --logy --logx mssm_201017_ggH_mt.json --cms-sub="Preliminary" -o mssm_201017_mt --process 'gg#phi' --title-right="35.9 fb^{-1}" --title-left="#mu#tau_{h}" --show 'exp' --plot-exp-points`

Or comparison plots can be made using the following script:

`python scripts/MSSMlimitCompare.py --file=mssm_201017_ggH_mt.json,mssm_201017_ggH_et.json --labels="mutau,etau" --expected_only --outname="mssm_201017_freezing_mt_vs_et_ggH" --process="gg#phi"`

The options --absolute and --relative can be used to make ratio plots as well. Note that it is also possible to apply parton luminosity scale factors to any of the limits.

To get the color scheme for the treatment of the SM higgs as BG the option --higgs-bg is implemented

`python scripts/plotMSSMLimits.py --logy --logx mssm_201017_withSMBG_ggH_mt.json --cms-sub="Preliminary" -o mssm_201017_SMHbg_mt --higgs-bg`

**Final plots for the paper**

ggH limits with lines added for t-only and b-only:
`python scripts/plotMSSMLimits.py --logy --logx mssm_201017_ggH_smfracs_cmb.json 'mssm_201017_ggH_bonly_cmb.json:exp0:MarkerSize=0,LineStyle=1,LineWidth=2,LineColor=4,Title="Expected b-only"' 'mssm_201017_ggH_tonly_cmb.json:exp0:MarkerSize=0,LineStyle=1,LineWidth=2,LineColor=2,Title="Expected t-only"' --cms-sub="Preliminary" -o mssm_201017_ggH_cmb --process 'gg#phi' --title-right="35.9 fb^{-1} (13 TeV)" --use-hig-17-020-style --do-new-ggH`

bbH limits:
`python scripts/plotMSSMLimits.py --logy --logx mssm_201017_bbH_smfracs_cmb.json --cms-sub="Preliminary" -o mssm_201017_bbH_cmb --process 'bb#phi' --title-right="35.9 fb^{-1} (13 TeV) --use-hig-17-020-style"`

### Limit comparisons for sync purposes

Plotting the relative difference in observed and expected limits: *DO NOT RUN WITHOUT THE --relative OPTION*

`python scripts/MSSMlimitCompare.py --file=mssm_ggH_mt_group1.json,mssm_ggH_mt_group2.json --labels="group1,group2" --relative --outname="mssm_ggH_mt_group1vsgroup2" --process="gg#phi"`

### Model dependent limits

`python ../CombineTools/scripts/plotLimitGrid.py HybridNewGridMSSM.root --scenario-label="m_{h}^{mod+} scenario"  --output="mssm_201017_unblinding_mhmodp_cmb" --title-right="12.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --contours="exp-2,exp-1,exp0,exp+1,exp+2,obs" --model_file=$PWD/shapes/Models/mhmodp_mu200_13TeV.root`

The plotting takes the asymptotic_grid or HybridNewGridMSSM file as input, and performs interpolation to produce smooth contours of exclusion for a 2D mA-tanb plot. Note that this script contains many different optional settings for this interpolation.

### ggH-bbH 2D limits

The plotting of the 2D limits takes as input the output from the previous combine calls. For each mass point $MASS you will need to run the following. The script also offers the --debug-output option to allow for saving the inital TGraph2 and contours to a root-file.

`python scripts/plotMultiDimFit.py --title-right="35.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --mass $MASS -o 2D_limit_mH${MASS} output/mssm_201017/cmb/higgsCombine.ggH-bbH.MultiDimFit.mH${MASS}.root`

For also plotting the expectation for the SM Higgs you need to additionally provide the TFile with the points for the SM Higgs (see 3d) with the --sm-exp option.

`python scripts/plotMultiDimFit.py --title-right="35.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --mass $MASS -o 2D_limit_mH${MASS} output/mssm_201017/cmb/higgsCombine.ggH-bbH.MultiDimFit.mH${MASS}.root --sm-exp output/mssm_201017/cmb/higgsCombine.2D.SM1.bestfit.MultiDimFiti.mH${MASS}.root`

### ggH-bbH 2D limits (from HybridNewGrid output)

`python scripts/plotFCIntervals.py HybridNewGridFCInterval.root --output="2D_limit_FC_mH${MASS}" --title-right="35.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --mass 700 --best-fit output/mssm_201017/cmb/higgsCombine.ggH-bbH-bestfit.MultiDimFit.mH700.root`

Addition of the expectation for SM Higgs + bkg not yet implemented, but should be added in a similar fashion to scripts/plotMultiDimFit.py

### Model independent limits with signal injected (blue band)

For plotting the blue band limits the same script as for the Brazil band plots is used

`python scripts/plotMSSMLimits.py --logy --logx mssm_freezing_BlueBand_bbH_cmb.json --process "gg#phi" --title-right="2.3 fb^{-1} (13 TeV)" --cms-sub="Preliminary" -o mssm_201017_BlueBand_bbH_cmb --higgs-injected`

### Prefit plots

Prefit plots can be made and either the model dependent (3 Higgs) or signal resonance signal can be added for a benchmark point. The usage:

`PostFitShapesFromWorkspace -d output/mssm_201017_mhmodp/cmb/combined.txt.cmb -w output/mssm_201017_mhmodp/cmb/mhmodp.root -o shapes_070617.root --print --freeze mA=1000,tanb=50,r=1,x=1`

To make the plots in the docs:

`python scripts/makeMassPlotsPrefit.py`

First is a call to PostFitShapesFromWorkspace, which will generate the signal and background templates for the benchmark point of mA = 1 TeV, tanb=50 in the mhmodp scenario. The postFitPlotJetFakes script, which is called from makeMassPlotsPrefit.py will  make a stacked plot. With the current settings the plots are blind above 100 GeV.

To also create the yield tables, add --make_yield_tables as additional option to the PostFitShapesFromWorkspace call. For the data yield this prints '0' for now.

### Postfit plots
Postfit plots require a sensible choice of fit. You can choose either the model independent or model dependent workspace, and simply need to set the appropriate parameters to something sensible.

The plotting code can then be used in postfit mode and passed the output of the maximum likelihood fit. Some examples are given for the model-dependent and the model-independent case.

#### For the plots in the docs:


**Model dependent case: mhmodp model with mu = 200 GeV, m_A = 700 GeV, tanb = 20 at 13 TeV with the fit performed for all categories combined. Parameters for the shapes are taken from the signal plus background (s + b) fit. Signal strengh parameters for the signal yields are taken equal to the model expectation.**

1. Set up workspace:

`MorphingMSSMFull2016 --output_folder="mssm_201017_unblinding_mhmodp" --postfix="-mttot" --manual_rebin=true`

`combineTool.py -M T2W -o "mhmodp.root" -P CombineHarvester.CombinePdfs.MSSM:MSSM --PO filePrefix=$PWD/shapes/Models/ --PO modelFiles=13TeV,mhmodp_mu200_13TeV.root,1 -i output/mssm_201017_unblinding_mhmodp/cmb/ --PO MSSM-NLO-Workspace=$PWD/shapes/Models/higgs_pt_v3_mssm_mode.root`

2. Max likelihood fit:

`combineTool.py -M MaxLikelihoodFit --setPhysicsModelParameters mA=700,tanb=20 -d output/mssm_201017_unblinding_mhmodp/cmb/mhmodp.root --there --minimizerTolerance 0.1 --minimizerStrategy 0 --cminPreScan --robustFit 1`

3. Get the shapes:

`PostFitShapesFromWorkspace -d output/mssm_201017_unblinding_mhmodp/cmb/combined.txt.cmb -w output/mssm_201017_unblinding_mhmodp/cmb/mhmodp.root -o shapes.root --print --freeze mA=700,tanb=20,r=1,x=1 --postfit --sampling -f output/mssm_final_limit_shapes_mhmodp/cmb/mlfit.Test.root:fit_s`

4. Plot the shapes with current style setup:

`python scripts/makeMassPlots_split-y-scale.py`


**Model independent case: general multi signal model for the resonance mass m = 700 GeV with the fit performed for all categories combined. Parameters for the shapes are taken from the background only (b) fit. Therefore, the signal strengh parameters in the s + b fit are restricted to values near 0. For the shapes, the ggH and bbH signals are scaled both to 10 pb.**

1. Set up workspace:

`MorphingMSSMFull2016 --output_folder="mssm_201017_unblinding" -m MH --postfix="-mttot" --manual_rebin=true`

`combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_unblinding/cmb/ `

2. Max likelihood fit:

`combineTool.py -M MaxLikelihoodFit --setPhysicsModelParameters r_ggH=0,r_bbH=0 --freezeNuisances r_bbH --redefineSignalPOIs r_ggH -m 700  --setPhysicsModelParameterRanges r_ggH=-0.000001,0.000001 --minimizerTolerance 0.1 --minimizerStrategy 0 -d output/mssm_201017_unblinding/cmb/ws.root --there`

3. Get the shapes:

`PostFitShapesFromWorkspace -d output/mssm_201017_unblinding_mhmodp/cmb/combined.txt.cmb -w output/mssm_201017_unblinding/cmb/ws.root -o shapes.root --print --freeze r_ggH=10,r_bbH=10 --postfit --sampling -f output/mssm_201017_unblinding/cmb/mlfit.Test.root:fit_b`

4. Plot the shapes with current style setup:

`python scripts/makeMassPlots_model-independent.py`

## Creating datacards for pulls and GOF tests

**ALL GOF instructions to be updated**

The commands below needed to create a workspace are chosen consistently with the first two steps for model-independent limits 1a) and 2a) with the change --real_data=true for the Morphing step.

`MorphingMSSMFull2016 --output_folder="mssm_201017_unblinding" -m MH --postfix="-mttot" --control_region=0 --auto_rebin=true --real_data=true --zmm_fit=true --ttbar_fit=true --jetfakes=true`

For creating the workspace for pulls from the datacards we use the multi-signal model.

`combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_unblinding/*`

For creating the workspace for GoF tests from the datacards it's easier to use a single-signal model, since the GoodnessOfFit
code assumes, that only one parameter of interest exists in order to fix it with '--fixedSignalStrength=0' option in step 8a). Otherwise you'll have to
use additional options in 8a) to demote one of the POI's to a fixed nuisance parameter to achieve a signal-signal model from a multi-signal model.

`combineTool.py -M T2W -o "ws.root" -i output/mssm_201017_unblinding/*`

You may parallelize the procedure by e.g. adding `--parallel 20` to the commands above

### Running the GoF jobs

We look at the Goodness of Fit for three different algorithms. The saturated model (saturated), Anderson-Darling (AD) and Kolmogorow-Smirnow (KS).
For the AD and KS it is sufficient to run the fits for the combined cards as the test-statitic for the individual channels can be extracted from these results. For the saturated model it is necessary to run them independtly of each other.
The choice of the mass value as 160 is arbitrary and not of any relevance here as we look at background only fits,

ALGO=AD (or ALGO=KS, ALGO=saturated)

`combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 160 --there -d output/mssm_201017_unblinding/cmb/ws.root -n ".$ALGO.toys" --fixedSignalStrength=0 -t 500`

`combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 160 --there -d output/mssm_201017_unblinding/cmb/ws.root -n ".$ALGO" --fixedSignalStrength=0`

ALGO=saturated

`combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 160 --there -d output/mssm_201017_unblinding/*_13TeV/ws.root -n ".$ALGO.toys" --fixedSignalStrength=0 -t 500`

`combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 160 --there -d output/mssm_201017_unblinding/*_13TeV/ws.root -n ".$ALGO" --fixedSignalStrength=0`

The toys can also be split in multiple batches by adding e.g. -s 0:10:1 as option (setting the seed to be 0-10 in 11 jobs)

To speed up the calculation, it's better to use more jobs with small amount of toys for example with the options -t 10 -s 0:99:1 --parallel 20

### Collecting GoF outputs

For the saturated model run for each category seperately

`combineTool.py -M CollectGoodnessOfFit --input output/mssm_201017_unblinding/htt_et_8_13TeV/higgsCombine.saturated.GoodnessOfFit.mH160.root output/mssm_201017_unblinding/htt_et_8_13TeV/higgsCombine.saturated.toys.GoodnessOfFit.mH160.*.root -o htt_et_8_13TeV_saturated.json`

For the AD and KS run

ALGO=AD (or ALGO=KS)

`combineTool.py -M CollectGoodnessOfFit --input output/mssm_201017_unblinding/cmb/higgsCombine.$ALGO.GoodnessOfFit.mH160.root output/mssm_201017_unblinding/cmb/higgsCombine.$ALGO.toys.GoodnessOfFit.mH160.*.root -o cmb_$ALGO.json`

### Plotting the GoF results

For the saturated model you again need to run the plotting once per category like

`python ../CombineTools/scripts/plotGof.py --statistic saturated --mass 160.0 -o htt_et_9_13TeV-saturated htt_et_9_13TeV_saturated.json  --title-right="12.9 fb^{-1} (13 TeV)" --title-left="e#tau_{h}, btag"`

For the AD or KS algorithm the plotting is done for all categories in one go (inclusing labelling of the plots)

ALGO=AD (or ALGO=KS)

`python ../CombineTools/scripts/plotGof.py --statistic $ALGO --mass 160.0 cmb_$ALGO.json --title-right="12.9 fb^{-1} (13 TeV)" --output='-$ALGO'`

8d) Getting the pulls

For determining the pulls in the b-only fit we run

`combineTool.py -M MaxLikelihoodFit output/mssm_201017_unblinding/cmb/ws.root`

Workaround for not unblinding fitted signal strength: can also set signal to only float within a very small range, e.g:

`combine -M MaxLikelihoodFit --setPhysicsModelParameters r_ggH=0,r_bbH=0 --freezeNuisances r_bbH --redefineSignalPOIs r_ggH -m 700  --setPhysicsModelParameterRanges r_ggH=-0.000001,0.000001 --minimizerTolerance 0.1 --minimizerStrategy 0 -d output/mssm_201017_unblinding/cmb/ws.root`

From this point on the pulls can then be extracted using the script diffNuisances.py which is provided together with combine.

`python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f html mlfit.Test.root > mlfit.html`

9) Producing and plotting impacts

First, set up the datacards as above.

Create the workspace:

`combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH$:r_ggH[0,-1,200]"' --PO '"map=^.*/bbH$:r_bbH[0,-1,200]"' -i output/mssm_201017/*`

Note the bbH and ggH range setting: we need to allow r_ggH and r_bbH to go negative if we wish to inject 0 signal. Note that this will only work at low masses, at higher mass points a negative signal strength could make the pdf negative and RooFit won't be happy. We'll set the appropriate r_ggH and r_bbH range that we wish to consider later on.

Run the initial fit, assuming you want to float r_ggH - description of parameters below:

`combineTool.py -t -1 -M Impacts -d output/mssm_201017/cmb/ws.root -m $MASS --doInitialFit --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances r_bbH --setPhysicsModelParameters r_bbH=0,r_ggH=$INJECTED_SIGNAL --setPhysicsModelParameterRanges r_ggH=$RANGE`

$MASS: pick a mass point. The chosen mass point will affect $INJECTED_SIGNAL and $RANGE.
At *low* mass, we can inject 0 signal. If we inject 0 signal, $RANGE should be something like -1,1. In what follows I'll asume we're using a low mass point.
At higher mass, we could run into trouble if we allow the signal strength to go negative - easiest is to inject roughly the expected limit. Then set a reasonable range, for example 0,0.1, depending on what limit you're injecting. When you run the initial fit, pay close attention to the result. Is the uncertainty interval found? If not, try reducing the value of the --stepSize option. Default is 0.1, 0.01 could be needed at very high mass.
If you injected 0 signal, check that negative signal strengths don't cause the pdf to go negative. RooFit will spit out a complaint as it's stepping around if this happens.

-Run the fits for all nuisance parameters:

`combineTool.py -t -1 -M Impacts -d output/mssm_201017/cmb/ws.root -m 200 --doFits --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances r_bbH --setPhysicsModelParameters r_bbH=0,r_ggH=0 --setPhysicsModelParameterRanges r_ggH=-1,1 --allPars`

The --allPars option runs the fits for unconstrained parameters as well, which we need to include if we want to check the rateParam impacts and constraints.
As there are around 700 nuisance parameters it's best to submit the fits to a batch system. If you're submitting to lxbatch, add e.g. following:
--job-mode lxbatch --sub-opts '-q 1nh' --merge 10
If you want to use your local batch system, additional options are needed. First of all create a file that includes the necessary setup for your batch system. The easiest is to place it in
/CombineHarvester/CombineTools/input/job_prefixes/ as job_prefix_<NAME>.txt, but it can be placed elsewhere with a different name if you prefer. To submit:
For an LSF batch system (jobs submitted using bsub):
--job-mode lxbatch --prefix-file <NAME> --sub-opts 'whatever you need to do to specify the queue for your batch system' --merge 10 (or another number if you want fewer or more jobs)
for an SGE batch system (jobs submitted using qsub):
--job-mode SGE --prefix-file <NAME> --sub-opts 'whatever you need to do to specifiy the queue for your batch system' --merge 10 (or another number)
*NOTE*: if you did *NOT* put your job prefix file in /CombineHarvester/CombineTools/input/job_prefixes/job_prefix_<NAME>.txt, you will have to pass the full path to your job prefix file via the --prefix-file option.

-Manual intervention for the ZMM_ZTT no b-tag rate param:

`combineTool.py -t -1 -M Impacts -d output/mssm_201017/cmb/ws.root -m 200 --doFits --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances r_bbH --setPhysicsModelParameters r_bbH=0,r_ggH=0 --setPhysicsModelParameterRanges r_ggH=-1,1:rate_ZMM_ZTT_nobtag=0.999,1.001 --named rate_ZMM_ZTT_nobtag --stepSize 0.01`

This is needed because the constraint on this rateParam is so tight that with the default step size the correct interval cannot be found. The other option would be to submit all of the fits with the --stepSize 0.01 option and setting the rateParam range to the narrow choice used here, but this would slow the fits down.

-Collect the results into a json file:

`combineTool.py -M Impacts -d output/mssm_201017/cmb/ws.root -m 200 --redefineSignalPOIs r_ggH --allPars --exclude r_bbH -o impacts_ggH_200.json`

We're calling --exclude r_bbH as we froze this parameter to 0, so not much point looking at the impact!

-Plot the impacts

`plotImpacts.py -i impacts_ggH_200.json -o impacts_ggH_200 --transparent`

the --transparent option allows us to see the size of the impacts when both +/-1sigma impact go in the same direction.

