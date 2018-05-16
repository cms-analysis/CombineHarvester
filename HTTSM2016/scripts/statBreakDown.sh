# Based on Combine Tutorial "Uncertainty breakdown and nuisance parameter groups"

# This needs to have:
#    texName.json 
#    plot1DScan.py
#    in the same directory


echo "THIS CREATES UNBLINDED RESULTS!"
echo "add -t -1 --expectSignal to combine -M MultiDimFit lines"
echo "TO UNDO THIS"


# N.B.: --rMin, --rMax, --points are defined so that a point will land directly on the best fit values of 1.057
#       This ensures we do not produce plots with altered 'best-fits' values
#       --- lastly, the plot1Scan.py will need to be adjusted depending on the 
#           number of nuisances included to maintain smooth color coordination
#           search for colorMap to adjust if needed.



# From Combine Tutorial
# First perform the fit and save a copy of the workspace in the output file with a "snapshot" of the best- fit model parameters included
combine -M MultiDimFit -m 125 --algo grid --points 101 --rMin 0.057 --rMax 2.057 cmb/125/workspace.root -n nominal  --minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP
combine -M MultiDimFit --algo none --rMin 0.057 --rMax 2.057 cmb/125/workspace.root -m 125 -n bestfit --saveWorkspace  --minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP

# Can then repeat the scan by first loading this snapshot, then freezing all the nuisance parameters. The uncertainty from this scan gives us the statistical component of the uncertainty. By defining: sigma_total^2 = sigma_stat^2 + sigma_syst^2 we can infer the systematic component.
combine -M MultiDimFit --algo grid --points 101 --rMin 0.057 --rMax 2.057 -m 125 -n stat \
higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisances all \
--minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP

python ./plot1DScan.py --main higgsCombinenominal.MultiDimFit.mH125.root \
--POI r -o cms_output_freeze_All \
--others 'higgsCombinestat.MultiDimFit.mH125.root:Freeze all:2' \
--breakdown syst,stat



# Repeat again singling out Theory Uncertainties
combine -M MultiDimFit --algo grid --points 101 --rMin 0.057 --rMax 2.057 -m 125 -n Theory \
higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Theory \
--minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP


python ./plot1DScan.py --main higgsCombinenominal.MultiDimFit.mH125.root \
--POI r -o cms_output_freeze_All_Theory \
--others \
    'higgsCombineTheory.MultiDimFit.mH125.root:Freeze Theory:2' \
    'higgsCombinestat.MultiDimFit.mH125.root:Freeze All:3' \
--breakdown theory,syst,stat


# Repeat again singling out Bin-by-Bin uncertainties
combine -M MultiDimFit --algo grid --points 101 --rMin 0.057 --rMax 2.057 -m 125 -n BinByBin \
higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups BinByBin \
--minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP

combine -M MultiDimFit --algo grid --points 101 --rMin 0.057 --rMax 2.057 -m 125 -n TheoryAndBBB \
higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups TheoryAndBBB \
--minimizerAlgoForMinos Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP


python ./plot1DScan.py --main higgsCombinenominal.MultiDimFit.mH125.root \
--POI r -o cms_output_freeze_All_Theory_bbb \
--others \
    'higgsCombineTheory.MultiDimFit.mH125.root:Freeze Theory:2' \
    'higgsCombineTheoryAndBBB.MultiDimFit.mH125.root:Freeze TheoryAndBBB:2' \
    'higgsCombinestat.MultiDimFit.mH125.root:Freeze All:3' \
--breakdown theory,bbb,syst,stat




#N.B. breakdown works by taking the "observed" uncertainty and subtracting the first listed uncertainty fit, then the second ... to leave you with a final estimate of the statistical uncertainty





