# VHbb instructions

This file collects instructions for producing the statistical results for the VHbb analysis. More detailed information on CombineHarvester can be found in the documentation at

http://cms-analysis.github.io/CombineHarvester/

## Important points to remember
**PLEASE ALWAYS** check that the covariance matrix is positive definite before using a fitDiagnostics result for plotting or to extract parameter uncertainties. If the covariance matrix is not positive definite the uncertainties that you get out are **nonsense**.
[15/06/18]
Analysis is still blind, please use the CR-only-postfit versions of the commands below.
In the previous version of 2016 cards some of the uncertainties had to be excluded for some of the regions because there were problems with the shapes. Once this is fixed please enable the uncertainties again (in python/systematics.py). It concerns the JER, and a few of the LHE_scale_weight uncertainties.
In the previous version of the 2017 cards no factorised JECs were present. Please enable them again, along with the JER, and disable the inclusive JEC.
MET unclustered energy needs to be added when it is in the input histograms, both for 2016 and 2017 (only affects 1-lep and 0-lep).
Split b-tagging uncertainties also need to be included when in the inputs.
Some instructions for adding/disabling systematics, renaming them if needed for the combination, and more can be found at the bottom of this page.


## Setting up the area

    export SCRAM_ARCH=slc6_amd64_gcc530
    scram project CMSSW CMSSW_8_1_0
    cd CMSSW_8_1_0/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
    git checkout v7.0.8
    cd ../..
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    cd CombineHarvester
    git checkout -b HIG16044-dev origin/HIG16044-dev
    cd ..
    scram b

## Getting the input root files

Before checking out the shape files, move to the relevant subdirectory:

`cd CombineHarvester/VH2017`

The input shape files are stored in an external repository. On a machine with a kerberos token for CERN access (e.g. lxplus) the repository can be checked out as:

`git clone https://:@gitlab.cern.ch:8443/cms-vhbb/VH2017.git shapes`

A password is not needed for this. Otherwise with normal https access (which does require a username and password) the repository can be checked out as:

`git clone https://gitlab.cern.ch/cms-vhbb/VH2017.git shapes`

Access to this repository is linked to the higgs-vlephbb e-group. 

## Setting up datacards

python scripts/VHbb2017.py [options]

This creates .txt datacards in the 'output' directory, both combined and per channel (Zee,Zmm,Wen,Wmn,Znn,Wln,Zll), all in separate subdirectories.
At the moment the options are
- `--channel`: set to 'all' by default, can specify individual channels to run here (e.g. `--channel=Zee,Zmm`)
- `--output_folder`: subdirectory of 'output' where the cards are written. Set to 'vhbb2017' by default.
- `--bbb_mode`: toggle to set the bin-by-bin inclusion options. mode 0: do not add bin-by-bins, 1 (default):use autoMCStat mode 
- `--auto_rebin`: switches on automated rebinning of the input histograms. Off by default.
- `--zero_out_low`: sets the bin contents in some of the SR bins to 0 (for the purpose of making yield tables). Off by default.
- `--year`: set to '2017' by default. This governs which filenames to read out of (with -2017 or -2016 postfix!) and appends the year label to the output folder

## Setting up workspaces
**Note: from this point on make sure to have called `ulimit -s unlimited` in your shell since logging in. Otherwise any of these manipulations might lead to a seg fault**

To create workspaces for every combination of regions the cards have been written out for in the previous step:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/*`

Or, for example, to just create a workspace for the Zee channel:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/Zee/`

**NOTE:** only use `*` for subdirectories. If you used e.g. `-i output/<output_folder>/Zee/*`, text2workspace would be called successively on every file in the Zee folder, including the
just-created workspace which leads to problems. 

## Setting up combinations
### Run1 + 2016 + 2017 combination
Make directory output/cmb-run1run2
Copy into this directory:
- The contents of a freshly set up 2017 cmb directory
- The contents of a freshly set up 2016 cmb directory (or if not available, take the inputs in shapes/HIG16044)
- The Run1 inputs from shapes/7and8TeV

Make the workspace:

`combineTool.py -M T2W -o "ws_masked.root" -i output/cmb-run1run2/ --channel-masks`

Generate a toy using the CR-only-postfit values of nuisance parameters:
`combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV=1,mask_vhbb_Zmm_1_13TeV2017=1,mask_vhbb_Zmm_2_13TeV=1,mask_vhbb_Zmm_2_13TeV2017=1,mask_vhbb_Zee_1_13TeV=1,mask_vhbb_Zee_1_13TeV2017=1,mask_vhbb_Zee_2_13TeV=1,mask_vhbb_Zee_2_13TeV2017=1,mask_vhbb_Wen_1_13TeV=1,mask_vhbb_Wen_1_13TeV2017=1,mask_vhbb_Wmn_1_13TeV=1,mask_vhbb_Wmn_1_13TeV2017=1,mask_vhbb_Znn_1_13TeV=1,mask_vhbb_Znn_1_13TeV2017=1,mask_vhbb_7plus8TeV_vhbb_Wln_7TeV_legacy_ch1_Wenu=1,mask_vhbb_7plus8TeV_vhbb_Wln_7TeV_legacy_ch1_Wenu2=1,mask_vhbb_7plus8TeV_vhbb_Wln_7TeV_legacy_ch2_Wmunu=1,mask_vhbb_7plus8TeV_vhbb_Wln_7TeV_legacy_ch2_Wmunu2=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch1_Wenu=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch1_Wenu2=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch1_Wenu3=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch2_Wmunu=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch2_Wmunu2=1,mask_vhbb_7plus8TeV_vhbb_Wln_8TeV_legacy_ch2_Wmunu3=1,mask_vhbb_7plus8TeV_vhbb_Wtn_8TeV_legacy=1,mask_vhbb_7plus8TeV_vhbb_Zll_7TeV_legacy_card1=1,mask_vhbb_7plus8TeV_vhbb_Zll_7TeV_legacy_card2=1,mask_vhbb_7plus8TeV_vhbb_Zll_7TeV_legacy_card3=1,mask_vhbb_7plus8TeV_vhbb_Zll_7TeV_legacy_card4=1,mask_vhbb_7plus8TeV_vhbb_Zll_8TeV_legacy_ch1=1,mask_vhbb_7plus8TeV_vhbb_Zll_8TeV_legacy_ch3=1,mask_vhbb_7plus8TeV_vhbb_Zll_8TeV_legacy_ch4=1,mask_vhbb_7plus8TeV_vhbb_Znn_7TeV_legacy_ch1=1,mask_vhbb_7plus8TeV_vhbb_Znn_7TeV_legacy_ch2=1,mask_vhbb_7plus8TeV_vhbb_Znn_8TeV_legacy_ZnunuHighPt_8TeV=1,mask_vhbb_7plus8TeV_vhbb_Znn_8TeV_legacy_ZnunuLowPt_8TeV=1,mask_vhbb_7plus8TeV_vhbb_Znn_8TeV_legacy_ZnunuMedPt_8TeV=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/cmb-run1run2/ws_masked.root`

Calculate the expected significance:
`combineTool.py -M Significance --significance -d output/cmb-run1run2/ws_masked.root --there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root`


## Fits
### Signal strength (without uncertainty):
Pre-fit:  
`combineTool.py -M MultiDimFit -t -1 -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0 --expectSignal X`
Here X can be 0 or 1 -> result of the fit will be 0 or 1 too.

Post-fit:  
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0`

### Signal strength (with reasonably accurate uncertainty)
Pre-fit expected[*]:  
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --there -t -1 --cminDefaultMinimizerStrategy 0 --algo singles --expectSignal 1 --robustFit 1`

Post-fit expected:  
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --there -t -1 --cminDefaultMinimizerStrategy 0 --algo singles --expectSignal 1 --toysFrequentist --robustFit 1`

Post-fit:  
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0 --algo singles`

[*]CR-only-postfit:

First we need to create a new workspace, set up for channel masking:

`combineTool.py -M T2W -o "ws_masked.root" -i output/<output_folder>/* --channel-masks`

This adds additional parameters to the workspace which we can use to mask certain regions (=remove them from the likelihood).
We will use this to generate a toy in which the nuisance parameters are set to their best-fit values (from effectively a b-only fit to the control regions):

`combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/<output_folder>/cmb/ws_masked.root --cminDefaultMinimizerStrategy 0`

`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_masked.root --there -t -1 --cminDefaultMinimizerStrategy 0 --algo singles --expectSignal 1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --robustFit 1`

### Significance:
Pre-fit expected[*]: `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1 --cminDefaultMinimizerStrategy 0`\
Post-fit expected: `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1 --toysFrequentist --cminDefaultMinimizerStrategy 0`\
Observed : `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0`\

[*] CR-only-postfit:
However, this is the fairer thing to do as the CR fit can have quite a large effect on the background predictions in the SR:

First we need to create a new workspace, set up for channel masking:

`combineTool.py -M T2W -o "ws_masked.root" -i output/<output_folder>/* --channel-masks`

This adds additional parameters to the workspace which we can use to mask certain regions (=remove them from the likelihood).
We will use this to generate a toy in which the nuisance parameters are set to their best-fit values (from effectively a b-only fit to the control regions):

`combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/<output_folder>/cmb/ws_masked.root --cminDefaultMinimizerStrategy 0`

Finally evaluate the cr-only-post-fit expected significance:
`combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws_masked.root --there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --cminDefaultMinimizerStrategy 0`


## Pre- and post-fit plots
### Post-fit plots
First run the maximum likelihood fit:

`combineTool.py -M FitDiagnostics -m 125 -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0`

create the post-fit shapes with uncertainties from the datacard and the MLFit:\
*Important:* before doing this, check that the covariance matrix is positive definite. If not, the plotted uncertainties will be nonsense. This can be done by opening up the fitDiagnostics result and calling fit_s->Print() (or fit_b->Print() if that is the fit result of interest). At the very top of the printout there should be a line that says 'Covariance matrix quality: Full, accurate covariance matrix'. In that case everything is ok. If it says 'Full matrix, but forced positive definite' or 'Not calculated at all' the uncertainties are no good. 

`PostFitShapesFromWorkspace -d output/<output_folder>/cmb/combined.txt.cmb -w output/<output_folder>/cmb/ws.root -o shapes.root --print --postfit --sampling -f output/<output_folder>/cmb/fitDiagnostics.Test.root:fit_s `

*Note*: PostFitShapesFromWorkspace can be sped up by using the option --skip-proc-errs, which does not evaluate the uncertainty for the individual processes, only for the total background/total s+b/total signal. Most of the time this would suffice. In addition, if you are only interested in the post-fit distributions, --skip-prefit will not extract the pre-fit shapes and uncertainties.

To make pre- and post fit plots of the BDT distributions in the SR:\
`python scripts/makePostFitPlots.py`\
*Note* For now these plots are made blinded in the [0,1] BDT discr. range. This range can be controlled using the options --x_blind_min, --x_blind_max (arguments to postFitPlot.py). The plots
can be fully unblinded by removing the `--blind` option passed in scripts/makePostFitPlots.py.

To make pre- and post fit plots of the CMVA distributions in the CR:\
`python scripts/makePostFitPlotsCR.py`

### CR-only post-fit plots:
`combineTool.py -M T2W -o "ws_masked.root" -i output/<output_folder>/cmb --channel-masks`

Run maximum likelihood fit, masking the SR from the likelihood:
`combineTool.py -M FitDiagnostics -m 125 -d output/<output_folder>/cmb/ws_masked.root --there --cminDefaultMinimizerStrategy 0 --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1,r=0 -n .SRMasked --redefineSignalPOIs SF_TT_Wln_2017 --freezeParameters r`

Note we are just promoting SF_TT_Wln_2017 to be the POI so that we can freeze r to 0 in the fit and then later, when running PostFitShapesFromWorkspace, freeze r back to 1. If we do not do this we are forced to use the b-only fit, where r just does not exist.

create the post-fit shapes with uncertainties from the datacard and the MLFit:
*Important:* before doing this, check that the covariance matrix is positive definite. If not, the plotted uncertainties will be nonsense.

`PostFitShapesFromWorkspace -d output/<output_folder>/cmb/combined.txt.cmb -w output/<output_folder>/cmb/ws_masked.root -o shapes.root --print --freeze r=1 --postfit --sampling -f output/<output_folder>/cmb/fitDiagnostics.SRMasked.root:fit_s`

To make pre- and post fit plots of the BDT distributions in the SR:
`python scripts/makePostFitPlots<year>.py`

To make pre- and post fit plots of the CMVA distributions in the CR:
`python scripts/makePostFitPlotsCR<year>.py`

Note: pre-fit in this case will be pre all fits, post-fit will be CR-only post-fit.

### Full pre-fit plots only:
`PostFitShapesFromWorkspace -d output/<output_folder>/cmb/combined.txt.cmb -w output/<output_folder>/cmb/ws.root -o shapes.root --print `

from scripts/makePostFitPlots<year>.py and scripts/makePostFitPlotsCR<year>.py remove 'postfit' from the 'MODE' line and make plots as above. 

## Yield tables
First run the maximum likelihood fit as described above for the post-fit plots.

Set up new cards and workspace for which the discriminator range we want to ignore is zeroed out. The ranges are defined in scripts/VHbb2017.py

`python scripts/VHbb2017.py [options] --zero_out_low`
`combineTool.py -M T2W -o "ws.root" -i output/<output_folder_zeroed_out>/cmb/`

Create the pre- and postfit yield tables (note: by default this is setup for 2017. We can add a 2016 version if needed, or just replace 2017 by 2016 in printYieldTables.py) :
`./scripts/printYieldTables.py --workspace output/<output_folder_zeroed_out>/cmb/ws.root --fit_file output/<output_folder>/cmb/fitDiagnostics.Test.root`

It is *very* important to use fit results for the *full* model, otherwise the uncertainties on the yields will not be correct. <output_folder_zeroed_out> and <output_folder> are therefore explicitly different, unless yield tables are made for the full model too.


## Other plots
### Channel compatibility (post fit)
Make workspace with separate r_ZH/r_WH:

`combineTool.py -M T2W -i output/<output_folder>/cmb/ -o "ws_proc.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/.*ZH_hbb:r_ZH[1,0,5]' --PO 'map=.*/WH_hbb:r_WH[1,0,5]' `

Make workspace with separate r for 0,1 and 2 lepton channels:
`combineTool.py -M T2W -i output/<output_folder>/cmb/ -o "ws_channel.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=vhbb_Zee_.*/.*H_hbb:r_twolep[1,0,5]' --PO 'map=vhbb_Zmm_.*/.*H_hbb:r_twolep[1,0,5]' --PO 'map=vhbb_Znn_.*/.*H_hbb:r_zerolep[1,-2,5]' --PO 'map=vhbb_Wen_.*/.*H_hbb:r_onelep[1,0,5]' --PO 'map=vhbb_Wmn_.*/.*H_hbb:r_onelep[1,0,5]' `

Now we need to run MultiDimFit to get the best-fit value and uncertainty for each separate signal strength, as well as the combined signal strength:

```
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --cminDefaultMinimizerStrategy 0 --algo singles -n .cmb

combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_ZH=1,r_WH=1 --redefineSignalPOIs r_ZH -n .ZH --algo singles --cminDefaultMinimizerStrategy 0
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_ZH=1,r_WH=1 --redefineSignalPOIs r_WH -n .WH --algo singles --cminDefaultMinimizerStrategy 0

combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_channel.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_zerolep -n .zerolep --algo singles --cminDefaultMinimizerStrategy 0
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_channel.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_onelep -n .onelep --algo singles --cminDefaultMinimizerStrategy 0
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_channel.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_twolep -n .twolep --algo singles --cminDefaultMinimizerStrategy 0
```

Next we want to collect all of the fit results in a single json file:

```
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r -i higgsCombine.cmb.MultiDimFit.mH120.root --algo singles

combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_ZH -i higgsCombine.ZH.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_WH -i higgsCombine.WH.MultiDimFit.mH120.root --algo singles

combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_zerolep -i higgsCombine.zerolep.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_onelep -i higgsCombine.onelep.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_twolep -i higgsCombine.twolep.MultiDimFit.mH120.root --algo singles
```

Now make the plot:

`./scripts/plotCCC.py -i MultiDimFit_cc.json -o cccPlot`

### Channel compatibility (pre fit with CRs unblind)
Make a regular workspace with channel masks if it does not already exist:

`combineTool.py -M T2W -o "ws_masked.root" -i output/<output_folder>/* --channel-masks`

Make workspace with separate r_ZH/r_WH:

`combineTool.py -M T2W -i output/<output_folder>/cmb/ -o "ws_proc.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/.*ZH_hbb:r_ZH[1,0,5]' --PO 'map=.*/WH_hbb:r_WH[1,0,5]' --channel-masks `

Make workspace with separate r for 0,1 and 2 lepton channels:
`combineTool.py -M T2W -i output/<output_folder>/cmb/ -o "ws_channel.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=vhbb_Zee_.*/.*H_hbb:r_twolep[1,0,5]' --PO 'map = vhbb_Zmm_.*/.*H_hbb:r_twolep[1,0,5]' --PO 'map=vhbb_Znn_.*/.*H_hbb:r_zerolep[1,-2,5]' --PO 'map=vhbb_Wen_.*/.*H_hbb:r_onelep[1,0,5]' --PO 'map=vhbb_Wmn_.*/.*H_hbb:r_onelep[1,0,5]' --channel-masks `



Now generate toys for each workspace:
```
combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/<output_folder>/cmb/ws_masked.root --cminDefaultMinimizerStrategy 0

combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1,r_ZH=1,r_WH=1 -t -1 --toysFrequentist  --saveToys --there -d output/<output_folder>/cmb/ws_proc.root -n .ToyPerProc --cminDefaultMinimizerStrategy 0

combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1,r_zerolep=1,r_onelep=1,r_twolep=1 -t -1 --toysFrequentist  --saveToys --there -d output/<output_folder>/cmb/ws_channel.root -n .ToyPerChn --cminDefaultMinimizerStrategy 0

```

Now we need to run MultiDimFit to get the best-fit value and uncertainty for each separate signal strength, as well as the combined signal strength:
```
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --cminDefaultMinimizerStrategy 0 --algo singles -n .cmb -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --there
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_ZH=1,r_WH=1 --redefineSignalPOIs r_ZH -n .ZH --algo singles --cminDefaultMinimizerStrategy 0 -t -1 --toysFrequentist --toysFile higgsCombine.ToyPerProc.GenerateOnly.mH120.123456.root --there
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_ZH=1,r_WH=1 --redefineSignalPOIs r_WH -n .WH --algo singles --cminDefaultMinimizerStrategy 0 -t -1 --toysFrequentist --toysFile higgsCombine.ToyPerProc.GenerateOnly.mH120.123456.root --there


combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_zerolep -n .zerolep --algo singles --cminDefaultMinimizerStrategy 0 -t -1 --toysFrequentist --toysFile higgsCombine.ToyPerChn.GenerateOnly.mH120.123456.root --there
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_onelep -n .onelep --algo singles --cminDefaultMinimizerStrategy 0 -t -1 --toysFrequentist --toysFile higgsCombine.ToyPerChn.GenerateOnly.mH120.123456.root --there
combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_proc.root --setParameters r_zerolep=1,r_onelep=1,r_twolep=1 --redefineSignalPOIs r_twolep -n .twolep --algo singles --cminDefaultMinimizerStrategy 0 -t -1 --toysFrequentist --toysFile higgsCombine.ToyPerChn.GenerateOnly.mH120.123456.root --there
```

Next we want to collect all of the fit results in a single json file:

```
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r -i output/<output_folder>/cmb/higgsCombine.cmb.MultiDimFit.mH120.root --algo singles

combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_ZH -i output/<output_folder>/cmb/higgsCombine.ZH.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_WH -i output/<output_folder>/cmb/higgsCombine.WH.MultiDimFit.mH120.root --algo singles

combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_zerolep -i output/<output_folder>/cmb/higgsCombine.zerolep.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_onelep -i output/<output_folder>/cmb/higgsCombine.onelep.MultiDimFit.mH120.root --algo singles
combineTool.py -M PrintFit --json MultiDimFit_ccc.json -P r_twolep -i output/<output_folder>/cmb/higgsCombine.twolep.MultiDimFit.mH120.root --algo singles
```

Now make the plot:

`python scripts/plotCCC.py -i MultiDimFit_ccc.json -o cccPlot`


### S-over-B ordered plot
**Note: at the moment this is set up for HIG-16-044 and 2017 only. Can adapt as needed - to run with re-loaded 2016 the category names in prepareSoverBordered will need to be adapted**

As inputs we will need the orignal combined datacard, the original combined workspace and the RooFit result obtained when running FitDiagnostics.  
For 2016+2017 for now we use the contents of a fresh 2017 cmb directory + HIG16044 (from the shapes directory). Put the results in a combined directory output/cmb-sbordered/

First make the workspace

`combineTool.py -M T2W -o "ws_masked.root" -i output/cmb-sbordered/ --channel-masks`

And run FitDiagnostics (note: have to check that the covariance matrix is accurate):

`combineTool.py -M FitDiagnostics -m 125 -d output/cmb-for-sbordered/ws_masked.root --there --cminDefaultMinimizerStrategy 0 --setParameters mask_vhbb_Zmm_1_13TeV=1,mask_vhbb_Zmm_1_13TeV2017=1,mask_vhbb_Zmm_2_13TeV=1,mask_vhbb_Zmm_2_13TeV2017=1,mask_vhbb_Zee_1_13TeV=1,mask_vhbb_Zee_1_13TeV2017=1,mask_vhbb_Zee_2_13TeV=1,mask_vhbb_Zee_2_13TeV2017=1,mask_vhbb_Wen_1_13TeV=1,mask_vhbb_Wen_1_13TeV2017=1,mask_vhbb_Wmn_1_13TeV=1,mask_vhbb_Wmn_1_13TeV2017=1,mask_vhbb_Znn_1_13TeV=1,mask_vhbb_Znn_1_13TeV2017=1,r=0 -n .SRMasked --redefineSignalPOIs SF_TT_Wln_2017 --freezeParameters r`

Now we need to set up some datacards with the bins re-ordered according to (pre-fit S)/(post-fit B) 

`python ./scripts/prepareSoverBordered.py -w output/cmb-for-sbordered/ws_masked.root -f output/cmb-for-sbordered/fitDiagnostics.SRMasked.root -d output/cmb-for-sbordered/combined.txt.cmb`

This writes out S/B ordered datacards for the SR categories only to output/vhbb_sbordered_12jun/vhbb_20162017.txt

Make the workspace for these cards:
`combineTool.py -M T2W -o "ws.root" -i output/vhbb_sbordered_12jun/ `

Now we need to run PostFitShapesFromWorkspace on the new S/B ordered workspace we have just made, using the RooFit result we have been using all along:

`PostFitShapesFromWorkspace -d output/vhbb_sbordered_12jun/vhbb_20162017.txt -w output/vhbb_sbordered_12jun/ws.root -o shapes_sbordered.root --postfit --sampling -f output/cmb-for-sbordered/cmb/fitDiagnostics.Test.root:fit_s --total-shapes`

To make the plot:
`python ./scripts/plotSoverBordered.py -f shapes_sbordered.root --log_y --custom_y_range --ratio`

Note: for now this will NOT plot the data, it is commented in the plotting script.

### S/(S+B) weighted plot
a-la-HIG-16-044 we would need multiple steps. First we have to extract S/(S+B) weights from the existing model:

`./scripts/extractSoverSplusBweights.py -w output/<original_output_folder>/cmb/ws.root -f output/<original_output_folder>/cmb/fitDiagnostics.Test.root -d output/<original_output_folder>/cmb/combined.txt.cmb`

This writes a file store_ssplusbweights.root which contains histograms with the same BDT binning as used in the analysis, containing the relevant weight for each BDT bin that can then be applied by the analysts. In HIG-16-044 style the analysts then provide m_jj shape inputs with the weights applied, which we will use to make the plot. First set up the datacards for the mjj shapes up as before (currently would need to hack the input root file names into VHbb2017.py but we should add an option to do this instead).

Then make the workspace for these cards:  
`combineTool.py -M T2W -o "ws.root" -i output/mjj_cards/cmb/`  

And as before run PostFitShapesFromWorkspace on this new workspace with the fit result we have been using all along as input:

`PostFitShapesFromWorkspace -d output/mjj_cards/cmb/combined.txt.cmb -w output/mjj_cards/cmb/ws.root -o shapes_mjj.root --postfit --sampling -f output/<original_output_folder>/cmb/fitDiagnostics.Test.root:fit_s --total-shapes`  

Plotting script very similar to ./scripts/plotSoverBordered.py still needed.

## Impacts (post-fit)
First set up the datacards as above and create the workspace.

Run the initial fit:
```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doInitialFit --robustFit 1 --setParameterRanges r=0,3 --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP
```

Then run fits for all nuisance parameters:
```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doFits --robustFit 1 --setParameterRanges r=0,3 --allPars --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP [--job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 5]
```

We can submit these fits to a batch system, by adding:  
(lxbatch): `--job-mode lxbatch --sub-opts '-q <queuename>' --merge 10`  
(condor):  `--job-mode condor --sub-opts='+JobFlavour = "workday"' ` 

`--merge N` runs N of the fits in the same job, these fits can take a long time so --merge 5 is probably reasonable. This is given in square brackets as an example above 

Collecting the results in a json file: 
`combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --allPars -o impacts.json`

Plotting:  
`plotImpacts.py -i impacts.json -o impacts_out --transparent`

## Impacts (pre-fit)
First set up the datacards as above and create the workspace.

Run the initial fit:
```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doInitialFit --robustFit 1 --setParameterRanges r=0,3 -t -1 --expectSignal 1 --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP
```

Then run fits for all nuisance parameters (remember to submit them to the batch!):
```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doFits --robustFit 1 --setParameterRanges r=0,3 --allPars -t -1 --expectSignal 1 --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP [--job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 5]
```
Collecting the results in a json file: 
`combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --allPars -o impacts.json`

Plotting:  
`plotImpacts.py -i impacts.json -o impacts_out --transparent`

## Impacts (approximation):
Instructions based on slide 14 here: https://indico.cern.ch/event/718592/contributions/3042780/attachments/1669046/2676739/HFuture-Proj-June.pdf 

To use it, you will have to change both your **combine** branch and you **CombineHarvester** branch:

**To switch combine branch:**
Go to $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit and do:

```
git checkout -b ajgilbert-81x-root606-yr 
git pull https://github.com/ajgilbert/HiggsAnalysis-CombinedLimit.git 81x-root606-yr
```

Then go to $CMSSW_BASE/src/CombineHarvester/ (make sure you have no local changes) and do:

```
git pull origin master
```

(NB if someone pushes these changes to the main HIG16044-dev branch this last step can be skipped)

Finally go back to $CMSSW_BASE/src and re-compile with scram

### Impacts (approximation) post-fit:

```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doFits --robustFit 1 --setParameterRanges r=0,3 --allPars --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP --approx robust
```
NOTE: in this case there is only one fit, therefore no need to submit to the batch

Collecting the results in a json file: 
`combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --allPars --approx robust -o impacts_approx.json`

Plotting:  
`plotImpacts.py -i impacts_approx.json -o impacts_out --transparent`

### Impacts (approximation) pre-fit:

```
combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --doFits --robustFit 1 --setParameterRanges r=0,3 --allPars --cminDefaultMinimizerStrategy 0 --X-rtd FITTER_DYN_STEP --approx robust -t -1 --expectSignal 1
```
NOTE: in this case there is only one fit, therefore no need to submit to the batch

Collecting the results in a json file: 
`combineTool.py -M Impacts -d output/<output_folder>/cmb/ws.root -m 125 --allPars --approx robust -o impacts_approx.json`

Plotting:  
`plotImpacts.py -i impacts_approx.json -o impacts_out --transparent`

## Goodness-of-Fit
**NOTE: There is no such thing as a blind goodness-of-fit test, so only run once it is ok to unblind**  
Several GoF tests  are implemented in combine: the saturated model, Kolmogorov-Smirnov and Anderson-Darling tests. More info [here](https://cms-hcomb.gitbooks.io/combine/content/part3/commonstatsmethods.html#goodness-of-fit-tests).\n
Both KS and AD rely on the full model, but compute a GoF measure in each category/region. The saturated model test is defined for individiual categories/regions as well as combinations thereof.\n
Because our background predictions rely heavily on the fitted control regions we need to use post-fit toys to build our test-statistic distribution. The KS and AD tests are then slightly fairer since at least the post-fit toys will be fully post-fit, not just in the category/region we are testing. However, there is nothing technically to stop us from running the saturated model.

### AD/KS
$ALGO = AD,KS:  
```
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d output/<output_folder>/cmb/ws.root -n ".$ALGO.toys" --expectSignal 1 -t 500 --toysFrequentist  
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d output/<output_folder>/cmb/ws.root -n ".$ALGO" 
```

these jobs can be submitted to a batch system/condor as specified above. In that case we probably want to split the N toys into fewer toys per job, for example for 5 toys/job we could replace `-t 500` by `-t 5 -s 0:99:1` (which sets the seed of each job to 0,1...99).
When the jobs finish we collect the output:

`combineTool.py -M CollectGoodnessOfFit --input output/<output_folder>/cmb/higgsCombine.$ALGO.GoodnessOfFit.mH125.root output/<output_folder>/cmb/higgsCombine.$ALGO.toys.GoodnessOfFit.mH125.*.root -o cmb_$ALGO.json`

And to make plots for all regions:

`python ../CombineTools/scripts/plotGof.py --statistic $ALGO --mass 125.0 cmb_$ALGO.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-$ALGO'`

### Saturated model
**Note: we do not currently write datacards for individual regions into separate folders. Workspaces for individual regions can be created like as, e.g. for 1-electron channel SR:  
`text2workspace.py -o output/<output_folder>/Wen/ws_wen1.root output/<output_folder>/Wen/vhbb_Wen_1_13TeV.txt`**

Now run everything separately for each region/combination of regions you want to look at:
```
combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d output/<output_folder>/Zee/ws.root -n ".saturated.toys" --expectSignal 1 -t 500 --toysFrequentist  
combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d output/<output_folder>/Zee/ws.root -n ".saturated" 

combineTool.py -M CollectGoodnessOfFit --input output/<output_folder>/Zee/higgsCombine.saturated.GoodnessOfFit.mH125.root output/<output_folder>/Zee/higgsCombine.saturated.toys.GoodnessOfFit.mH125.*.root -o Zee_saturated.json

python ../CombineTools/scripts/plotGof.py --statistic saturated --mass 125.0 -o Zee_saturated Zee_saturated.json  --title-right="35.9 fb^{-1} (13 TeV)" --title-left="2-electron (SRs+CRs)"

```

## Freezing groups of nuisances
To determine the effect of addition or removal of a group of nuisances on the signal strength. The nuisance groups are defined in VH2017.py, search for `SetGroup`. Note that a group for the bin-by-bin parameters has to be created during the text2workspace step and cannot be defined at the datacard making stage. You will need to merge this PR: https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/pull/478 to be able to do this. The group is called autoMCStats.
With that in hand the groups defined now are: signal_theory, bkg_theory, sim_modelling, jes, jer, btag, mistag, lumi, lep_eff, met, autoMCStats.

### Effect of addition/removal of nuisance parameters (SR blind)

First we need to generate the usual toy:
`combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/<output_folder>/cmb/ws_masked.root`

Now we need to run the nominal fit and save a snapshot with the best-fit values of the parameters:
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws_masked.root --there --cminDefaultMinimizerStrategy 0  -t -1 --expectSignal 1 --toysFrequentist --saveWorkspace -n .snapshot --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root `

#### Removal of a group of nuisances
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/higgsCombine.snapshot.MultiDimFit.mH120.123456.root --cminDefaultMinimizerStrategy 0 --snapshotName MultiDimFit --algo singles -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --freezeNuisanceGroups <groupname> --there -n .freeze<groupname> --robustFit 1 `

This should be compared with the total uncertainty:
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/higgsCombine.snapshot.MultiDimFit.mH120.123456.root --cminDefaultMinimizerStrategy 0 --snapshotName MultiDimFit --algo singles -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --there -n .freeze<groupname> --robustFit 1 ` (note: we do not technically need the snapshot etc. here, but it also does not hurt to do it)

The effect of the removal of this group on the uncertainty is then: sqrt((total uncertainty)^2 - (uncertainty with frozen group)^2)
#### Addition of a group of nuisances
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/higgsCombine.snapshot.MultiDimFit.mH120.123456.root --cminDefaultMinimizerStrategy 0 --snapshotName MultiDimFit --algo singles -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --freezeNuisanceGroups ^<groupname> --there -n .nofreeze<groupname> --robustFit 1 ` NOTE THE '^', this means 'freeze everything apart from this nuisance'.

This should be compared with the uncertainty with all nuisances frozen:
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/higgsCombine.snapshot.MultiDimFit.mH120.123456.root --cminDefaultMinimizerStrategy 0 --snapshotName MultiDimFit --algo singles -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --there --freezeParameters all -n .freezeall --robustFit 1 `

The effect of addition of this group on the uncertainty is sqrt((uncertainty without frozen group)^2-(uncertainty with all params frozen)^2).



A handy thing we can do is to run everything in one go just generating the fits separately and running it in the background, or submitting to the batch/condor once the fit starts taking longer:
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/higgsCombine.snapshot.MultiDimFit.mH120.123456.root --cminDefaultMinimizerStrategy 0 --snapshotName MultiDimFit --algo singles -t -1 --toysFrequentist --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root --there --robustFit 1 --generate 'freezeNuisanceGroups;n;;!,fr.nominal;signal_theory,fr.signaltheory;bkg_theory,fr.bkgtheory;sim_modelling,fr.modelling;jes,fr.jes;jer,fr.jer;btag,fr.btag;mistag,fr.mistag;lumi,fr.lumi;lep_eff,fr.lep_eff;met,fr.met;autoMCStats,fr.autoMCStats;^signal_theory,nofr.signaltheory;^bkg_theory,nofr.bkgtheory;^sim_modelling,nofr.modelling;^jes,nofr.jes;^jer,nofr.jer;^btag,nofr.btag;^mistag,nofr.mistag;^lumi,nofr.lumi;^lep_eff,nofr.lep_eff;^met,nofr.met;^autoMCStats,nofr.autoMCStats'


## Diagnostic tools
### Printing/visualising correlations:
We can use the FitDiagnostics output to print/plot the correlations (from the fit covariance matrix).\
To print the top N correlations:\
`./scripts/printAllCorrelations -i output/<output_folder>/cmb/fitDiagnostics.Test.root:fit_s -m N`\
To print the N largest correlations of other parameters with a given parameter:\
`./scripts/printCorrelations -i output/<output_folder>/cmb/fitDiagnostics.Test.root:fit_s -p PARAMETER_NAME -m N`\
To save and draw the correlation matrix for a given set of parameters:\
`./scripts/plotCorrelations -i output/<output_folder>/cmb/fitDiagnostics.Test.root:fit_s -p PARAM_NAME_1,PARAM_NAME_2,...,PARAM_NAME_3 -o <output_name_string>`\
This plots the correlation matrix as <output_name_string>.pdf/png and saves the TH2 in <output_name_string>.root 

### FastScan 
FastScan can be used to get an idea of what the likelihood looks like as a function of the parameters. This assumes you have a FitDiagnostics result with an inaccurate convariance matrix that you want to inspect. Assume the file is called fitDiagnostics.root
If we want to run this on an asimov dataset, we need to generate a toy first. Assuming we want to generate an asimov dataset with the CRs unblind:
`combineTool.py -M GenerateOnly --setParameters mask_vhbb_Zmm_1_13TeV<year>=1,mask_vhbb_Zmm_2_13TeV<year>=1,mask_vhbb_Zee_1_13TeV<year>=1,mask_vhbb_Zee_2_13TeV<year>=1,mask_vhbb_Wen_1_13TeV<year>=1,mask_vhbb_Wmn_1_13TeV<year>=1,mask_vhbb_Znn_1_13TeV<year>=1 -t -1 --toysFrequentist  --expectSignal 1 --saveToys --there -d output/<output_folder>/cmb/ws_masked.root`

then:
`combineTool.py -M FastScan -w ws_masked.root:w -d higgsCombineTest.GenerateOnly.mH120.123456.root:toys/toy_asimov -f fitDiagnostics.root:fit_b` (or fit_s, depending on which of the two is giving problems)

The output of this is is a plot of the NLL as a function of each parameter, in addition to the first and second derivative of the NLL as a function of each parameter. Kinks in the likelihood will show up as discontinuities in the derivatives of the NLL. If such a feature is present near the minimum of a particular parameter, that indicates this parameter could be causing the problems in the fit.

## General troubleshooting
### Covariance matrix not accurate
After running FitDiagnostics in the steps to make post-fit plots you should always check that the covariance matrix is accurate, as described above. 
If the quality is `covariance matrix quality: Full matrix, but forced positive-definite` or `covariance matrix quality: Not calculated at all` you should not use this fit result to make post-fit plots because the uncertainties will not make sense. 
Things to try to solve this include:
- playing around with the minimizerTolerance (--cminDefaultMinimizerTolerance) and minimizerStrategy (--cminDefaultMinimizerStrategy). The strategy is set to 0 in the instructions at the moment, which is the least likely to give these problems. The minimizerTolerance is 0.1 by default.
- Checking if any parameters are strongly anti-correlated. 
- Are any parameters close to their boundaries?
- Are there discontinuities in the NLL? Try running FastScan to determine this. If this is the case, try freezing the suspicious parameter and see if this solves the problem. Of course one should then check if there are any problems with the input shapes for that parameter for example and try to fix any possible problems.

###To be updated
To be updated

## Quick guide to adding/removing/renaming systematics
The map of which bin_id number corresponds to which region can be found in scripts/VHbb2017.py . The map is called 'cats'.

Some examples:

Here we have *added* a shape systematics CMS_scale_j_13TeV for every channel and every category. We then immediately disable it in the signal regions (bin_id() 1 and 2) for all channels: 
```
  cb.cp().AddSyst(cb,
      'CMS_scale_j_13TeV','shape',ch.SystMap()(1.0))

  cb.FilterSysts(lambda x: (x.bin_id()==2 or x.bin_id()==1) and x.name()=='CMS_scale_j_13TeV')
```

Similar to the above, here we want to drop this uncertainty for the 0-lepton channel only, in all 0-lepton categories:
```
  cb.cp().AddSyst(cb,
      'CMS_vhbb_puWeight_2016','shape',ch.SystMap()(1.0))

  cb.FilterSysts(lambda x: (x.channel()=='Znn') and x.name()=='CMS_vhbb_puWeight_2016')
```

In this example we add an uncertainy only for a particular process in a subset of the channels:

```
cb.cp().channel(['Wmn','Wen','Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
      'CMS_LHE_weights_scale_muR_Zj1b','shape',ch.SystMap()(1.0))
```

If we want to rename an uncertainty, say 'CMS_scale_j_13TeV' to 'CMS_scale_j_13TeV_2017':
```
cb.cp().RenameSystematic(cb,'CMS_scale_j_13TeV','CMS_scale_j_13TeV_2017')
```
This should be done between the call to 'ExtractShapes' and the creation of the CardWriter in scripts/VHbb2017.py.

To rename a process, for example 'WH_hbb' to 'WH_lep':
```
cb.cp().ForEachObj(lambda x: x.set_process("WH_lep") if x.process()=='WH_hbb' else None)
```
This should again be done between the call to 'ExtractShapes' and the creation of the CardWriter in scripts/VHbb2017.py.



