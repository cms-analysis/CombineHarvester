# Links
[CombineHarvester twiki](http://cms-analysis.github.io/CombineHarvester/index.html)
[Combine gitbook](https://cms-hcomb.gitbooks.io/combine/content/)

# Compiling the correct CMSSW version

```bash
export SCRAM_ARCH=slc6_amd64_gcc530
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

scram project CMSSW CMSSW_8_1_0
cd CMSSW_8_1_0/src

# Clone combine
git clone ssh://git@github.com/cms-analysis/HiggsAnalysis-CombinedLimit HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.12
cd ../..

# Clone CombineHarvester
git clone ssh://git@github.com/cms-analysis/CombineHarvester CombineHarvester -b SMHTT2017-dev
mkdir -p CombineHarvester/HTTSM2017/shapes

# Build
scram b -j 24
scram b python
```

# Creating datacards

## Create datacards without bin-by-bin uncertainties

```bash
$CMSSW_BASE/bin/slc6_amd64_gcc530/MorphingSM2017 \
    --base_path=$BASE_PATH \        # Base path for finding ROOT files with shapes
    --input_folder_mt="/mt/" \      # Path relative to base_path containing the
                                    # mt shapes
    --input_folder_et="/et/" \      # Path relative to base_path containing the
                                    # et shapes
    --input_folder_tt="/tt/" \      # Path relative to base_path containing the
                                    # tt shapes
    --input_folder_em="/em/" \      # Path relative to base_path containing the
                                    # em shapes
    --real_data=false \             # Fit with real data or Asimov data
    --jetfakes=$JETFAKES \          # Toggle usage of fake-factor method
    --embedding=$EMBEDDING \        # Toggle usage of embedded samples
    --classic_bbb=false \           # Toggle usage of classic bin-by-bin uncertainties
    --postfix="-ML" \               # Expected postfix for the input ROOT files
                                    # with the shapes
    --channel="${CHANNELS}" \       # Analysis channels: Any combination of "em",
                                    # "et", "mt" and "tt" as single string
    --auto_rebin=true \             # Enable automatic rebinning, which merges bins
                                    # without background contribution
    --stxs_signals=$STXS_SIGNALS \  # Signal templates: "stxs_stage0" for ggH and qqH
                                    # or "stxs_stag1" for the stage 1 splitting
    --categories=$CATEGORIES \      # Categorization optimized for STXS stages:
                                    # "stxs_stage0" or "stxs_stage1"
    --era=$ERA \                    # Data-taking era: 2016 or 2017
    --output="${ERA}_smhtt"         # name of subdirectory in output directory
```

## Add autoMCStats bin-by-bin uncertainties

```bash
cd output/${ERA}_smhtt/cmb/125/
for FILE in *.txt
do
    sed -i '$s/$/\n * autoMCStats 0.0/' $FILE
done
```

# Building the workspaces

## Inclusive signal

```bash
ERA=2016
DATACARD_PATH=output/${ERA}_smhtt/cmb/125
NUM_THREADS=12
combineTool.py -M T2W -o ${ERA}_workspace.root -i ${DATACARD_PATH} --parallel $NUM_THREADS
```

## STXS stage 0 signals

```bash
ERA=2016
DATACARD_PATH=output/${ERA}_smhtt/cmb/125
NUM_THREADS=12
combineTool.py -M T2W -o ${ERA}_workspace.root -i ${DATACARD_PATH} --parallel $NUM_THREADS \
    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    --PO '"map=^.*/ggH.?$:r_ggH[1,-5,5]"' \
    --PO '"map=^.*/qqH.?$:r_qqH[1,-5,5]"'
```

## STXS stage 1 signals

```bash
ERA=2016
DATACARD_PATH=output/${ERA}_smhtt/cmb/125
NUM_THREADS=12
combineTool.py -M T2W -o ${ERA}_workspace.root -i ${DATACARD_PATH} --parallel $NUM_THREADS \
    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    --PO '"map=^.*/ggH_0J.?$:r_ggH_0J[1,-30,30]"' \
    --PO '"map=^.*/ggH_1J_PTH_0_60.?$:r_ggH_1J_PTH_0_60[1,-30,30]"' \
    --PO '"map=^.*/ggH_1J_PTH_60_120.?$:r_ggH_1J_PTH_60_120[1,-30,30]"' \
    --PO '"map=^.*/ggH_1J_PTH_120_200.?$:r_ggH_1J_PTH_120_200[1,-30,30]"' \
    --PO '"map=^.*/ggH_1J_PTH_GT200.?$:r_ggH_1J_PTH_GT200[1,-30,30]"' \
    --PO '"map=^.*/ggH_GE2J_PTH_0_60.?$:r_ggH_GE2J_PTH_0_60[1,-30,30]"' \
    --PO '"map=^.*/ggH_GE2J_PTH_60_120.?$:r_ggH_GE2J_PTH_60_120[1,-30,30]"' \
    --PO '"map=^.*/ggH_GE2J_PTH_120_200.?$:r_ggH_GE2J_PTH_120_200[1,-30,30]"' \
    --PO '"map=^.*/ggH_GE2J_PTH_GT200.?$:r_ggH_GE2J_PTH_GT200[1,-30,30]"' \
    --PO '"map=^.*/ggH_VBFTOPO_JET3.?$:r_ggH_VBFTOPO_JET3[1,-30,30]"' \
    --PO '"map=^.*/ggH_VBFTOPO_JET3VETO.?$:r_ggH_VBFTOPO_JET3VETO[1,-30,30]"' \
    --PO '"map=^.*/qqH_VBFTOPO_JET3VETO.?$:r_qqH_VBFTOPO_JET3VETO[1,-30,30]"' \
    --PO '"map=^.*/qqH_VBFTOPO_JET3.?$:r_qqH_VBFTOPO_JET3[1,-30,30]"' \
    --PO '"map=^.*/qqH_REST.?$:r_qqH_REST[1,-30,30]"' \
    --PO '"map=^.*/qqH_VH2JET.?$:r_qqH_VH2JET[1,-100,100]"' \
    --PO '"map=^.*/qqH_PTJET1_GT200.?$:r_qqH_PTJET1_GT200[1,-30,30]"'
```

# Calculating signal strength constraints

## Inclusive signal

```bash
ERA=2016
combine -M MaxLikelihoodFit -m 125 ${ERA}_workspace.root \
    --robustFit 1 -n $ERA \
    --minimizerAlgoForMinos=Minuit2,Migrad
```

## STXS stage 0 and stage 1 signals

```bash
ERA=2016
combineTool.py -M MultiDimFit -m 125 -d ${ERA}_workspace.root \
    --algo singles -t -1 --expectSignal 1 \
    --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP \
    --robustFit 1 -n $ERA \
    --minimizerAlgoForMinos=Minuit2,Migrad
```

# Pulls and nuisance impacts

## Pulls

```bash
ERA=2016
# This puts the pulls in an HTML page. The option -f text puts the results in a text file.
# The file mlfit${ERA}.root is the result of the MaxLikelihoodFit above.
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a \
    -f html mlfit${ERA}.root > ${ERA}_diff_nuisances.html
```

## Nuisance impacts

```bash
ERA=2016
combineTool.py -M Impacts -m 125 -d ${ERA}_workspace.root --doInitialFit \
    --robustFit 1 -t -1 --expectSignal=1 --parallel 20 --minimizerAlgoForMinos=Minuit2,Migrad
combineTool.py -M Impacts -m 125 -d ${ERA}_workspace.root --doFits \
    --parallel 20 --robustFit 1 -t -1 --expectSignal=1 --minimizerAlgoForMinos=Minuit2,Migrad
combineTool.py -M Impacts -m 125 -d ${ERA}_workspace.root --output ${ERA}_impacts.json
plotImpacts.py -i ${ERA}_impacts.json -o ${ERA}_impacts
```

# Prefit and postfit shapes for plotting

```bash
# Prefit shapes
# The text datacard is referenced only to add the original binning of the shapes
# to the output histograms of the command. Otherwise, the bins are numbered with
# integers.
PostFitShapesFromWorkspace -m 125 -w ${ERA}_workspace.root \
    -d output/${ERA}_smhtt/cmb/125/combined.txt.cmb -o ${ERA}_datacard_shapes_prefit.root

# Postfit shapes
# The file mlfit${ERA}.root is the result of the MaxLikelihoodFit above
PostFitShapesFromWorkspace -m 125 -w ${ERA}_workspace.root \
    -d output/${ERA}_smhtt/cmb/125/combined.txt.cmb -o ${ERA}_datacard_shapes_postfit_sb.root \
    -f mlfit${ERA}.root:fit_s --postfit
```
