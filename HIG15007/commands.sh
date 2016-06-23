# Z->tautau cross section

### Run all commands from inside the HIG15007 directory:
###         cd $CMSSW_BASE/src/CombineHarvester/HIG15007
### Make sure the `shapes` repository is present and up-to-date:
###         git clone https://:@gitlab.cern.ch:8443/cms-htt/HIG-15-007.git shapes
###         cd shapes
###         git pull --rebase
###         cd ..

### Make datacards and workspaces
# Run the datacard creation script. The cards will be arranged in subdirectories
# of output/LIMITS. One combined directory for all channels (`cmb`) and one directory
# per channel.

rm -r ztt_plots
mkdir ztt_plots
for VAR in mvis svfit; do
    python scripts/setupDatacards.py --variable ${VAR} -o output/LIMITS-${VAR}
    ### Also create constrained versions:
    python scripts/setupDatacards.py --variable ${VAR} -o output/CONSTRAINED-${VAR} --constrain-tau-eff --constrain-tau-scale
done

for DIR in output/{LIMITS,CONSTRAINED}-{mvis,svfit}; do
### Create the workspace for the combination:
combineTool.py -M T2W -o wsp.root -i ${DIR}/*/datacard.txt
### Create a second workspace in which there is one POI for each channel:
combineTool.py -M T2W -o wsp_per_chn.root -i ${DIR}/cmb/datacard.txt \
    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    --PO map='mt_.*/ZTT:r_mt[1,-1,3]' \
    --PO map='et_.*/ZTT:r_et[1,-1,3]' \
    --PO map='em_.*/ZTT:r_em[1,-1,3]' \
    --PO map='tt_.*/ZTT:r_tt[1,-1,3]' \
    --PO map='mm_.*/ZTT:r_mm[1,-1,3]' \
    --PO verbose
done


### Max-lilelihood fit and pre-/post-fit plots
## Do the ML fit on the combined:
for DIR in CONSTRAINED; do
for VAR in mvis svfit; do
    combineTool.py -M MaxLikelihoodFit -m 90 --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad -d output/${DIR}-${VAR}/cmb/wsp.root --skipBOnlyFit --setPhysicsModelParameterRanges r=0.5,1.5 --there
    #### Create the pre- and post-fit output:
    PostFitShapesFromWorkspace -w output/${DIR}-${VAR}/cmb/wsp.root -d output/${DIR}-${VAR}/cmb/datacard.txt -o ztt_shapes_${VAR}.root -f output/${DIR}-${VAR}/cmb/mlfit.Test.root:fit_s -m 90 --postfit --sampling --print
    ### Make the plots, using log scale for mm:
    declare -A XVAR
    XVAR=( [mvis]="m_{ll}" [svfit]='m_{#tau#tau}' )
    for CHN in mt et tt em; do
        for TYPE in prefit postfit; do python scripts/postFitPlot.py \
        -i ztt_shapes_${VAR}.root:${CHN}_inclusive_${TYPE} \
        -o ${VAR}_${CHN}_inclusive_${TYPE} -c ${CHN} --x-title ${XVAR[${VAR}]}; done;
    done
    for CHN in mm; do
        for TYPE in prefit postfit; do python scripts/postFitPlot.py \
        -i ztt_shapes_${VAR}.root:${CHN}_inclusive_${TYPE} \
        -o ${VAR}_${CHN}_inclusive_${TYPE} -c ${CHN} --x-title ${XVAR[${VAR}]} --logy --y-min 50; done;
    done
    mkdir -p ztt_plots/postfit
    mv *fit.p* ztt_plots/postfit/
done
done

### Yield tables (all options currently hard-coded in the script)
# Currently produces both pre-fit and post-fit tables directly to the screen
python scripts/yieldTable.py

### Nuisance parameter impacts
for VAR in mvis svfit; do
mkdir -p output/LIMITS-${VAR}/cmb/impacts
pushd output/LIMITS-${VAR}/cmb/impacts
combineTool.py -M Impacts -d ../wsp.root -m 90 -n impacts --setPhysicsModelParameterRanges r=0.5,1.5 --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doInitialFit --allPars
combineTool.py -M Impacts -d ../wsp.root -m 90 -n impacts --setPhysicsModelParameterRanges r=0.5,1.5 --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doFits --parallel 4 --allPars
combineTool.py -M Impacts -d ../wsp.root -m 90 -n impacts --setPhysicsModelParameterRanges r=0.5,1.5 --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --output impacts.json --parallel 4 --allPars
popd
plotImpacts.py -i output/LIMITS-${VAR}/cmb/impacts/impacts.json -o impacts_${VAR}
mv impacts_${VAR}.pdf ztt_plots/
done

### Uncertainty Breakdown
### Unconditional fit saving the snapshot:

for VAR in mvis svfit; do
DIR=output/LIMITS-${VAR}/cmb
combineTool.py --there -M MultiDimFit -d ${DIR}/wsp.root -m 90 --algo none --setPhysicsModelParameterRanges r=0.5,1.5 --saveWorkspace -n .prefit
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r_${CHN}=0.5,1.5 --points 60 --minimizerStrategy 0 -n .nominal
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r_${CHN}=0.5,1.5 --points 60 --minimizerStrategy 0 -n .freeze.lumi --freezeNuisanceGroups lumi
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r_${CHN}=0.5,1.5 --points 60 --minimizerStrategy 0 -n .freeze.lumi.allsyst --freezeNuisanceGroups lumi,allsyst
python scripts/plot1DScan.py -m ${DIR}/higgsCombine.nominal.MultiDimFit.mH90.root \
    --POI r -o nominal_${VAR}.r --no-input-label --translate scripts/translate.json \
    --logo 'CMS' --logo-sub 'Internal' --others \
    "${DIR}/higgsCombine.freeze.lumi.MultiDimFit.mH90.root:Freeze Lumi:2" \
    "${DIR}/higgsCombine.freeze.lumi.allsyst.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" \
    --breakdown "Lumi,Syst,Stat" --chop 20
mkdir -p ztt_plots/scans-1d-cmb-unconst
mv nominal_${VAR}.r.* ztt_plots/scans-1d-cmb-unconst/

DIR=output/CONSTRAINED-${VAR}/cmb
combineTool.py --there -M MultiDimFit -d ${DIR}/wsp.root -m 90 --algo none --setPhysicsModelParameterRanges r=0.5,1.5 --saveWorkspace -n .prefit
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.5,1.5 --points 60 --minimizerStrategy 0 -n .nominal
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.5,1.5 --points 60 --minimizerStrategy 0 -n .freeze.lumi --freezeNuisanceGroups lumi
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.5,1.5 --points 60 --minimizerStrategy 0 -n .freeze.lumi.allsyst --freezeNuisanceGroups lumi,allsyst
python scripts/plot1DScan.py -m ${DIR}/higgsCombine.nominal.MultiDimFit.mH90.root \
    --POI r -o nominal_${VAR}.r --no-input-label --translate scripts/translate.json \
    --logo 'CMS' --logo-sub 'Internal' --others \
    "${DIR}/higgsCombine.freeze.lumi.MultiDimFit.mH90.root:Freeze Lumi:2" \
    "${DIR}/higgsCombine.freeze.lumi.allsyst.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" \
    --breakdown "Lumi,Syst,Stat" --chop 20

python scripts/plot1DScan.py -m ${DIR}/higgsCombine.nominal.MultiDimFit.mH90.root \
    --POI 'r*2.0084' -o nominal_${VAR}.rscaled --no-input-label --translate scripts/translate.json \
    --logo 'CMS' --logo-sub 'Internal' --others \
    "${DIR}/higgsCombine.freeze.lumi.MultiDimFit.mH90.root:Freeze Lumi:2" \
    "${DIR}/higgsCombine.freeze.lumi.allsyst.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" \
    --breakdown "Lumi,Syst,Stat" --chop 20 --model ztt_xsec --json xsec_res_${VAR}.json --json-POI r
mkdir -p ztt_plots/scans-1d-cmb-const
mv nominal_${VAR}.r*.* ztt_plots/scans-1d-cmb-const/
#### or for the per-channel:
DIR=output/CONSTRAINED-${VAR}/cmb
combineTool.py --there -M MultiDimFit -d ${DIR}/wsp_per_chn.root -m 90 --algo none --saveWorkspace -n .chn.prefit
for CHN in et mt em tt mm; do combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.chn.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --redefineSignalPOIs r_${CHN} --setPhysicsModelParameterRanges r_${CHN}=0.6,1.4 --points 60 --minimizerStrategy 0 -n .chn.nominal.r_${CHN}; done
for CHN in et mt em tt mm; do combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.chn.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --redefineSignalPOIs r_${CHN} --setPhysicsModelParameterRanges r_${CHN}=0.6,1.4 --points 60 --minimizerStrategy 0 -n .chn.freeze.lumi.r_${CHN} --freezeNuisanceGroups lumi; done
for CHN in et mt em tt mm; do combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.chn.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --redefineSignalPOIs r_${CHN} --setPhysicsModelParameterRanges r_${CHN}=0.6,1.4 --points 60 --minimizerStrategy 0 -n .chn.freeze.lumi.allsyst.r_${CHN} --freezeNuisanceGroups lumi,allsyst; done
for CHN in et mt em tt mm; do
    python scripts/plot1DScan.py -m ${DIR}/higgsCombine.chn.nominal.r_${CHN}.MultiDimFit.mH90.root \
    --POI r_${CHN} -o chn_${VAR}.nominal.r_${CHN} --no-input-label --translate scripts/translate.json \
    --logo 'CMS' --logo-sub 'Internal' --others \
    "${DIR}/higgsCombine.chn.freeze.lumi.r_${CHN}.MultiDimFit.mH90.root:Freeze Lumi:2" \
    "${DIR}/higgsCombine.chn.freeze.lumi.allsyst.r_${CHN}.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" \
    --breakdown "Lumi,Syst,Stat" --chop 20;
    python scripts/plot1DScan.py -m ${DIR}/higgsCombine.chn.nominal.r_${CHN}.MultiDimFit.mH90.root \
    --POI 'r_'${CHN}'*2.0084' -o chn_${VAR}.nominal.rscaled_${CHN} --no-input-label --translate scripts/translate.json \
    --logo 'CMS' --logo-sub 'Internal' --others \
    "${DIR}/higgsCombine.chn.freeze.lumi.r_${CHN}.MultiDimFit.mH90.root:Freeze Lumi:2" \
    "${DIR}/higgsCombine.chn.freeze.lumi.allsyst.r_${CHN}.MultiDimFit.mH90.root:Freeze Lumi+Syst:4" \
    --breakdown "Lumi,Syst,Stat" --chop 20 --model ztt_xsec --json xsec_res_${VAR}.json --json-POI r_${CHN};
done
mkdir -p ztt_plots/scans-1d-cmb-const
mv chn_${VAR}.* ztt_plots/scans-1d-cmb-const/
done

### Scans for other POIs
for VAR in mvis svfit; do
DIR=output/LIMITS-${VAR}/cmb
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --points 50 --minimizerStrategy 0 -n .nominal.id --redefineSignalPOIs CMS_eff_t --setPhysicsModelParameterRanges CMS_eff_t=0.8,1.2:r=0.5,1.5
combineTool.py --there -M MultiDimFit -d ${DIR}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --points 50 --minimizerStrategy 0 -n .nominal.es --redefineSignalPOIs CMS_scale_t --setPhysicsModelParameterRanges CMS_scale_t=-1,1:r=0.5,1.5
python scripts/plot1DScan.py -m ${DIR}/higgsCombine.nominal.id.MultiDimFit.mH90.root --POI CMS_eff_t -o nominal_${VAR}.id --no-input-label --translate scripts/translate.json --logo 'CMS' --logo-sub 'Internal'
python scripts/plot1DScan.py -m ${DIR}/higgsCombine.nominal.es.MultiDimFit.mH90.root --POI "1+CMS_scale_t*0.03" -o nominal_${VAR}.es --no-input-label --translate scripts/translate.json --logo 'CMS' --logo-sub 'Internal'
mkdir -p ztt_plots/scans-1d-cmb-unconst
mv nominal_${VAR}.* ztt_plots/scans-1d-cmb-unconst/
done

# ### Scans on separate channel constrained cards:
# for CHN in et mt em tt mm; do combineTool.py --there -M MultiDimFit -d output/CONSTRAINED/${CHN}/wsp.root -m 90 --algo none --setPhysicsModelParameterRanges r=0.5,1.5 --saveWorkspace -n .prefit; done
# for CHN in et mt em tt mm; do combineTool.py --there -M MultiDimFit -d output/CONSTRAINED/${CHN}/higgsCombine.prefit.MultiDimFit.mH90.root -m 90 --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.4,1.6 --points 50 --minimizerStrategy 0 -n .nominal.r; done
# for CHN in et mt em tt mm; do python scripts/plot1DScan.py -m output/CONSTRAINED/${CHN}/higgsCombine.nominal.r.MultiDimFit.mH90.root --POI r -o chn_sep.${CHN}.nominal.r --no-input-label --translate scripts/translate.json --logo 'CMS' --logo-sub 'Internal'; done

######## OLD ############################################
# ## 2D r,eff

#         combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.8,1.2:eff_t=0.8,1.2 --points 3600 --minimizerStrategy 0 -n .2d.r.eff --redefineSignalPOIs r,eff_t

#         ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.r.eff.MultiDimFit.mH90.root -o 2d_r_eff --x-axis r --y-axis eff_t --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"

# ## 2D r,ES

#         combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.6,1.4:CMS_scale_t=-0.7,0.7 --points 3600 --minimizerStrategy 0 -n .2d.r.scale --redefineSignalPOIs r,CMS_scale_t

#         ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.r.scale.MultiDimFit.mH90.root -o 2d_r_scale --x-axis r --y-axis "1+CMS_scale_t*0.03" --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"

# ##  2D eff,ES

#         combine -M MultiDimFit prefit_asimov_ztt_13TeV.root -m 90 -D data_asimov --snapshotName MultiDimFit --algo grid --setPhysicsModelParameterRanges r=0.5,1.5:CMS_scale_t=-0.7,0.7:eff_t=0.8,1.2 --points 3600 --minimizerStrategy 0 -n .2d.eff.scale --redefineSignalPOIs eff_t,CMS_scale_t

#         ../../../../HIG15002/scripts/generic2D.py -f higgsCombine.2d.eff.scale.MultiDimFit.mH90.root -o 2d_eff_scale --x-axis eff_t --y-axis "1+CMS_scale_t*0.03" --translate ../translate.json --logo CMS --logo-sub Internal --title-right "Z#rightarrow#tau#tau"


