# Kappa-F Work Flow
# This is heavily based off othe the Dec 2016 HiggsAnalysis Combine presentation, modified for SM-HTT analysis.
# it is likely that people will need to adjust the values of CV and CF which are used below for better
# contours in the future.  Default is set for 0 - 5.
# The final command needs to be run once the root session has begun
# We can work on aesthetics of this output plot in the future.

# creating datacards
MorphingSM2016 --output_folder="Blinded25112016_kappa" --postfix="-2D" --control_region=1 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=true


# Building the workspaces:
cd output/Blinded25112016_kappa
# Create workspace for hgg using cVcF Physics Model (Does't work in SWAN, but this is how to do it):
#combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF -i {cmb,em,et,mt,tt}/* -o kappaWorkspace.root --parallel 8 # From Combine Tutorial
combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF -i cmb/125/htt*.txt -o kappaWorkspace.root --parallel 8

# Run 1D fits for CV and CF using Hgg
###combine -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,5.0:CF=0.0,5.0 kappaWorkspace.root --algo=singles --robustFit=1 -t -1 # From Combine Tutorial
combine -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,5.0:CF=0.0,5.0 cmb/125/kappaWorkspace.root --algo=singles --robustFit=1 -t -1 --expectSignal=1

# Perform 2D scan in CV vs. CF
combineTool.py -n CvCf -M MultiDimFit -m 125 --setPhysicsModelParameterRanges CV=0.0,5.0:CF=0.0,5.0 cmb/125/kappaWorkspace.root --algo=grid --points=2000 -t -1 --expectSignal=1

# Run this on the output root file
#root -l higgsCombineCvCf.MultiDimFit.mH125.root ../../scripts/contours2D.cxx
#contour2D("CV",40,0.0,5.0,"CF",40,0.0,5.0,1.,1.)


