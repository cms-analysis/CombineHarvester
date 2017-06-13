# Kappa-F Work Flow
# This is heavily based off othe the Dec 2016 HiggsAnalysis Combine presentation, modified for SM-HTT analysis.
# it is likely that people will need to adjust the values of CV and CF which are used below for better
# contours in the future.  Default is set for 0 - 5.
# The final command needs to be run once the root session has begun
# We can work on aesthetics of this output plot in the future.


# Note that the version of this plot in the pass includes HWW as a signal higgs with
# a coupling that is profiled here as well.
# use scripts/renameHists.py to rename all HWW_qq125 --> qqH_hww125
# and edit below to change name appropriately
# - bin/MorphingSM2016.cpp
# --- remove HWW_qq125 from bkg_procs["em"]
# --- define new sig_procs: vector<string> sig_procs_em = {"ggH","qqH","WH","ZH","qqH_hww"};
# --- only use 125 GeV signal masses
# --- when doing AddProcesses, add sig_procs_em when chan == "em"
# --- same for writting DCs using ExtractShapes
# - src/HttSystematics_SMRun2.cc
# --- add "qqH_hww" to sig_procs
# --- then find and replace HWW_qq125 --> qqH_hww125


# Before you run this the first time copy the below file and re 'scram b'
# cp python/HiggsCouplings.py ../../HiggsAnalysis/CombinedLimit/python/HiggsCouplings.py



# creating datacards
newFolder=Blinded20170607_cv2cf2_v1
MorphingSM2016 --output_folder=${newFolder} --postfix="-2D" --control_region=1 --manual_rebin=false --real_data=true --mm_fit=false --ttbar_fit=true


# Building the workspaces:
cd output/${newFolder}
cd cmb/125

## Create workspace for hgg using cVcF Physics Model (Does't work in SWAN, but this is how to do it):
##combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF -i {cmb,em,et,mt,tt}/* -o kappaWorkspace.root --parallel 8 # From Combine Tutorial

combineCards.py htt_*_*_13TeV.txt > htt_cmsCards_13TeV.txt
combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcFHiggs -i htt_cmsCards_13TeV.txt -o kappaWorkspace.root

# Run 1D fits for CV and CF using Hgg
###combine -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,5.0:CF=0.0,5.0 kappaWorkspace.root --algo=singles --robustFit=1 -t -1 # From Combine Tutorial

# For better fit convergence
combine -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,2.0:CF=0.0,2.0 kappaWorkspace.root --algo=singles --robustFit=1 --minimizerAlgoForMinos=Minuit2,Migrad --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\"

# Perform 2D scan in CV vs. CF
# Uncomment the following line to run this scan on 1 core.
# This can be sped up by running multicored, see
# scripts/kappaF_kappaV_Multithreading.py
#
#combineTool.py -n CvCf -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,2.0:CF=0.0,2.0 kappaWorkspace.root --algo=grid --points=200 -t -1 --expectSignal=1 --minimizerAlgoForMinos=Minuit2,Migrad
#
echo "python ../../../../scripts/kappaF_kappaV_Multithreading.py"
#XXX python ../../../../scripts/kappaF_kappaV_Multithreading.py
# Run this on the output root file
#root -l higgsCombineCvCf.MultiDimFit.mH125.root ../../../../scripts/contours2D.cxx
#contour2D("CV",3,0.0,3.5,"CF",3,0.0,2.0,1.,1.)


