# VHbb instructions

This file collects instructions for producing the statistical results for the VHbb analysis. More detailed information on CombineHarvester can be found in the documentation at

http://cms-analysis.github.io/CombineHarvester/

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
- `--auto_rebin`: switches on automated rebinning of the input histograms. Off by default.

## Setting up workspaces

To create workspaces for every combination of regions the cards have been written out for in the previous step:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/*`

Or, for example, to just create a workspace for the Zee channel:

`combineTool.py -M T2W -o "ws.root" -i output/<output_folder>/Zee/`

## Fits
To be updated

## Pre- and post-fit plots
To be updated

## Other plots
To be updated

## Diagnostic tools
To be updated

