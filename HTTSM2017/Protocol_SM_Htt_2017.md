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

# Build
scram b -j 24
scram b python

# Get shapes
cd CombineHarvester/HTTSM2017
git clone https://:@gitlab.cern.ch:8443/cms-htt/SM-ML-2017.git shapes
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

# Fit signal strength and compute Hesse matrix

## Fit signal strength modifier for inclusive, STXS stage 0 and STXS stage 1

```bash
ERA=2016
combineTool.py -M MultiDimFit -m 125 -d ${ERA}_workspace.root \
    --algo singles -t -1 --expectSignal 1 \
    --robustFit 1 -n $ERA \
    --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0
```

## Calculate Hesse matrix

```bash
# The workspace is built using the inclusive signal definition.
# The fit result is used for pulls and prefit/postfit shapes.
ERA=2016
combine -M FitDiagnostics -m 125 -d ${ERA}_workspace.root \
        --robustFit 1 -n $ERA -v1 \
        --robustHesse 1 \
        --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0
```

# Pulls and nuisance impacts

## Pulls

```bash
ERA=2016
# This puts the pulls in an HTML page. The option -f text puts the results in a text file.
# The file fitDiagnostics${ERA}.root is the result of the FitDiagnostics above.
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a \
    -f html fitDiagnostics${ERA}.root > ${ERA}_diff_nuisances.html
```

## Nuisance impacts

```bash
ERA=2016
combineTool.py -M Impacts -m 125 -d ${ERA}_workspace.root \
    --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
    --doInitialFit --robustFit 1 \
    -t -1 --expectSignal=1 \
    --parallel 32
combineTool.py -M Impacts -m 125 -d ${ERA}_workspace.root \
    --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
    --doFits --parallel 20 --robustFit 1 \
    -t -1 --expectSignal=1 \
    --parallel 32
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
# The file fitDiagnostics${ERA}.root is the result of the FitDiagnostics shown
PostFitShapesFromWorkspace -m 125 -w ${ERA}_workspace.root \
    -d output/${ERA}_smhtt/cmb/125/combined.txt.cmb -o ${ERA}_datacard_shapes_postfit_sb.root \
    -f fitDiagnostics${ERA}.root:fit_s --postfit
```

# Extract POI correlation from the `RooFitResult`

```python
import ROOT
f = ROOT.TFile(filename)
result = f.Get("fit_s")
params = result.floatParsInit()
correlation = result.correlation(
                params.find(name_poi_1),
                params.find(name_poi_2))
```

# Perform goodness of fit test

```bash
ERA=$1
MASS=125
TOYS=30
NUM_THREADS=20

STATISTIC=saturated # or KS or AD

# Get test statistic value
# NOTE: --plots makes for KS and AD plots showing the bins with most tension.
# These plots can be found in the higgsCombine${NAME}.GoodnessOfFit.mH125.root
# file in the folder GoodnessOfFit.
combineTool.py -M GoodnessOfFit --algo=${STATISTIC} -m $MASS -d ${ERA}_workspace.root \
        -n ${ERA} \
        --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
        --plots

# Throw toys
combineTool.py -M GoodnessOfFit --algo=${STATISTIC} -m $MASS -d ${ERA}_workspace.root \
        -n ${ERA} \
        -s 1230:1249:1 -t $TOYS \
        --parallel $NUM_THREADS \
        --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0

# Collect results
combineTool.py -M CollectGoodnessOfFit \
    --input higgsCombine${ERA}.GoodnessOfFit.mH$MASS.root \
        higgsCombine${ERA}.GoodnessOfFit.mH$MASS.*.root \
    --output gof.json

# Plot
plotGof.py --statistic ${STATISTIC} --mass $MASS.0 --output gof gof.json
```

# Perform NLL scan and plot

```bash
ERA=2016
POI=r
NUM=20
MIN=0
MAX=2

# Perform scan
combineTool.py -M MultiDimFit -d ${ERA}_workspace.root -m 125 \
    --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
    --algo grid \
    -P ${POI} \
    --floatOtherPOIs 1 \
    --points $NUM \
    --rMin $MIN --rMax $MAX \
    -n ${ERA}_${POI}

# Create dummy translate.json file needed for plotting
echo "{}" > translate.json

# Plot 2*deltaNLL vs POI
python ${CMSSW_BASE}/bin/slc6_amd64_gcc530/plot1DScan.py \
    --main higgsCombine${ERA}_${POI}.MultiDimFit.mH125.root \
    --POI $POI \
    --output ${ERA}_${POI}_plot_nll \
    --translate translate.json
```
# Perform expected/observed synchronization

Needed scripts can be found under `$CMSSW_BASE/src/CombineHarvester/HTTSM2017/synctools`. The shape files to be compared have to be in the folder `$CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes`.
The synchronization can be performed on the signal strength using `show_sync_signalstrength.py` or on the significance using `show_sync_significance.py`. The output is a `json` file containing the sync result and a visualization in form of a `png` file.

How to run:
```
python show_sync_signalstrength.py shape1 shape2 real_data era
python show_sync_significance.py shape1 shape2 real_data era

shape1,shape2       input folder from $CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes (e.g Vienna KIT)
real_data           true or false
era                 2016 or 2017
```
