# Z->tautau cross section

Run all commands from inside the HIG15007 directory:

        cd $CMSSW_BASE/src/CombineHarvester/HIG15007

Make sure the `shapes` repository is present and up-to-date:

        git clone https://:@gitlab.cern.ch:8443/cms-htt/HIG-15-007.git shapes
        cd shapes
        git pull --rebase
        cd ..

Run the datacard creation script:

        python scripts/setupDatacards.py

The cards will be arranged in subdirectories of `output/LIMITS/` - one combined directory for all channels (`cmb`) and one directory per channel.

Create the workspaces:

    combineTool.py -M T2W -i output/LIMITS/*/datacard.txt -o workspace.root

Now we can do some fits, e.g. in the cmb directory:

    cd output/LIMITS/cmb/

Do a quick scan of the NLL in r to get an idea of the uncertainty:

    combine -M MultiDimFit workspace.root --algo singles --setPhysicsModelParameterRanges r=0.5,1.5 --minimizerAlgoForMinos Minuit2,Migrad --robustFit 1 --minimizerStrategy 0

Add `-t -1 --expectSignal 1` to scan a pre-fit asimov dataset.

## Uncertainty Breakdown

### On real data

Unconditional fit saving the snapshot:

        combine -M MultiDimFit workspace.root -m 90 --algo none --setPhysicsModelParameterRanges r=0.5,1.5 --saveWorkspace -n .prefit
        mv higgsCombine.prefit.MultiDimFit.mH90.root workspace.prefit.root

Run the scans, nominal first:

        combine -M MultiDimFit workspace.prefit.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.85,1.15 --points 50 --minimizerStrategy 0  -n .nominal

Then freezing successive groups of nuisance parameters:

        combine -M MultiDimFit workspace.prefit.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.85,1.15 --points 50 --minimizerStrategy 0 --freezeNuisanceGroups lumi -n .freeze.lumi
        combine -M MultiDimFit workspace.prefit.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.85,1.15 --points 50 --minimizerStrategy 0 --freezeNuisanceGroups lumi,syst -n .freeze.lumi.syst

Copy the results up to the top level:
        
        cp higgsCombine.* ../../../; cd ../../../

Plot the scan:

        python scripts/plot1DScan.py -m higgsCombine.nominal.MultiDimFit.mH90.root --POI r -o nominal --no-input-label --translate scripts/translate.json --logo 'CMS' --logo-sub 'Internal' --others "higgsCombine.freeze.lumi.MultiDimFit.mH90.root:Freeze Lumi:2" "higgsCombine.freeze.lumi.syst.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" --breakdown "Lumi,Syst,Stat"

### On an asimov dataset

Unconditional fit saving the snapshot and toy:

        combine -M MultiDimFit workspace.root -m 90 -t -1 --expectSignal 1 --algo none --setPhysicsModelParameterRanges r=0.5,1.5 --saveWorkspace --saveToys -n .asimov.prefit

Copy the output file adding the asimov dataset into the workspace in the process:

        combineTool.py -M ModifyDataSet higgsCombine.asimov.prefit.MultiDimFit.mH90.123456.root:w workspace.asimov.prefit.root:w:data_asimov -d higgsCombine.asimov.prefit.MultiDimFit.mH90.123456.root:/toys/toy_asimov

Then run the scans exactly as above but on `workspace.asimov.prefit.root` with the option `-D data_asimov` added to every combine command.

# Other things... work in progress

## MDF
        combine -M MaxLikelihoodFit --skipBOnlyFit prefit_asimov_ztt_13TeV.root -v 3 --setPhysicsModelParameterRanges r=0.8,1.2 -m 90 -D data_asimov --snapshotName MultiDimFit

## 1D Scans
        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.8,1.2 --points 50 --minimizerStrategy 0 -n .nominal.r
        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --redefineSignalPOIs eff_t --setPhysicsModelParameterRanges eff_t=0.8,1.2:r=0.5,1.5 --points 50 --minimizerStrategy 0 -n .nominal.eff
        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --redefineSignalPOIs CMS_scale_t --setPhysicsModelParameterRanges CMS_scale_t=-0.7,0.7:eff_t=0.8,1.2:r=0.5,1.5 --points 50 --minimizerStrategy 0 -n .nominal.scale

        ../../../../HIG15002/scripts/plot1DScan.py -m higgsCombine.nominal.r.MultiDimFit.mH90.root --POI r -o scan_r --no-input-label --translate ../translate.json --logo 'CMS' --logo-sub 'Internal'
        ../../../../HIG15002/scripts/plot1DScan.py -m higgsCombine.nominal.eff.MultiDimFit.mH90.root --POI eff_t -o scan_eff --no-input-label --translate ../translate.json --logo 'CMS' --logo-sub 'Internal'
        ../../../../HIG15002/scripts/plot1DScan.py -m higgsCombine.nominal.scale.MultiDimFit.mH90.root --POI "1+CMS_scale_t*0.03" -o scan_scale --no-input-label --translate ../translate.json --logo 'CMS' --logo-sub 'Internal'

## 2D r,eff

        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.8,1.2:eff_t=0.8,1.2 --points 3600 --minimizerStrategy 0 -n .2d.r.eff --redefineSignalPOIs r,eff_t

        ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.r.eff.MultiDimFit.mH90.root -o 2d_r_eff --x-axis r --y-axis eff_t --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"

## 2D r,ES

        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.6,1.4:CMS_scale_t=-0.7,0.7 --points 3600 --minimizerStrategy 0 -n .2d.r.scale --redefineSignalPOIs r,CMS_scale_t

        ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.r.scale.MultiDimFit.mH90.root -o 2d_r_scale --x-axis r --y-axis "1+CMS_scale_t*0.03" --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"

##  2D eff,ES

        combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.5,1.5:CMS_scale_t=-0.7,0.7:eff_t=0.8,1.2 --points 3600 --minimizerStrategy 0 -n .2d.eff.scale --redefineSignalPOIs eff_t,CMS_scale_t

        ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.eff.scale.MultiDimFit.mH90.root -o 2d_eff_scale --x-axis eff_t --y-axis "1+CMS_scale_t*0.03" --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"


