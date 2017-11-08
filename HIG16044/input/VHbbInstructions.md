# VHbb instructions

This file collects instructions for producing the statistical results for the VHbb analysis. More detailed information on CombineHarvester can be found in the documentation at

http://cms-analysis.github.io/CombineHarvester/

## Getting the input root files

A repository still needs to be made

## Setting up datacards

python ./scripts/VHbb2016.py [options]

This creates .txt datacards in the 'output' directory, both combined and per channel (Zee,Zmm,Wen,Wmn,Znn - combinations thereof can also be specified in the script).
At the moment the options are
- `--channel`: set to 'all' by default, can specify individual channels to run here (e.g. `--channel=Zee,Zmm`)
- `--auto_rebin`: switches on automated rebinning of the input histograms. Off by default.


## Setting up workspaces

`combineTool.py -M T2W -o "ws.root" -i output/*`

## Fits
To be updated

## Pre- and post-fit plots
To be updated

## Other plots
To be updated

## Diagnostic tools
To be updated

