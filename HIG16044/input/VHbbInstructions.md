# VHbb instructions

This file collects instructions for producing the statistical results for the VHbb analysis. More detailed information on CombineHarvester can be found in the documentation at

http://cms-analysis.github.io/CombineHarvester/

## Setting up the area

    export SCRAM_ARCH=slc6_amd64_gcc530
    scram project CMSSW CMSSW_8_1_0
    cd CMSSW_8_1_0
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git checkout v7.0.4
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    git checkout -b HIG16044-dev-fast-postfitshapes origin/HIG16044-dev-fast-postfitshapes
    scram b

## Getting the input root files

The input shape files are stored in an external repository. On a machine with a kerberos token for CERN access (e.g. lxplus) the repository can be checked out as:

`git clone https://:@gitlab.cern.ch:8443/cms-vhbb/HIG16044.git shapes`

A password is not needed for this. Otherwise with normal https access (which does require a username and password) the repository can be checked out as:

`git clone https://gitlab.cern.ch/cms-vhbb/HIG16044.git shapes`

Access to this repository is linked to the higgs-vlephbb e-group. 

## Setting up datacards

python ./scripts/VHbb2016.py [options]

This creates .txt datacards in the 'output' directory, both combined and per channel (Zee,Zmm,Wen,Wmn,Znn,Wln,Zll), all in separate subdirectories.
At the moment the options are
- `--channel`: set to 'all' by default, can specify individual channels to run here (e.g. `--channel=Zee,Zmm`)
- `--output_folder`: subdirectory of 'output' where the cards are written. Set to 'vhbb2016' by default.
- `--bbb_mode`: toggle to set the bin-by-bin inclusion options. mode 0: do not add bin-by-bins, 1 (default): add bin-by-bins as in official 2016 cards, 2: add bin-by-bins for all backgrounds in SR and CRs, merging some of the uncertainties to keep the number of nuisance parameters manageable, 3: same as 2, but using the new CMSHistFunc classes, 4: using the autoMCStat mode of combine.
- `--auto_rebin`: switches on automated rebinning of the input histograms. Off by default.

## Setting up workspaces

To create workspaces for every combination of regions the cards have been written out for in the previous step:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/*`

Or, for example, to just create a workspace for the Zee channel:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/Zee/`

## Fits
###Signal strength (without accurate uncertainty):
`combineTool.py -M MultiDimFit -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0`

###Significance:
Pre-fit expected: `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1`
Post-fit expected: `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1 --toysFrequentist`
Observed : `combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there`


## Pre- and post-fit plots
First run the maximum likelihood fit:

`combineTool.py -M FitDiagnostics -m 125 -d output/<output_folder>/cmb/ws.root --there --cminDefaultMinimizerStrategy 0`

create the post-fit shapes with uncertainties from the datacard and the MLFit:
*Important:* before doing this, check that the covariance matrix is positive definite. If not, the plotted uncertainties will be nonsense.

`PostFitShapesFromWorkspace -d output/<output_folder>/cmb/combined.txt.cmb -w output/<output_folder>/cmb/ws.root -o shapes.root --print --postfit --sampling -f output/<output_folder>/cmb/fitDiagnostics.Test.root:fit_s`

To make pre- and post fit plots of the BDT distributions in the SR:
`python scripts/makePostFitPlots.py`

The underlying plotting scripts is scripts/postFitPlot.py. Some small adaptations still need to be made to be able to plot post-fit plots of the CRs (in addition to cosmetic changes).


## Other plots
To be updated

## Diagnostic tools
To be updated

