
# See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#MultiSignalModel_ready_made_mode

# It is helpful to break down the significance by
# channel and category. When doing this, we want to
# maintain the benefits of any nuisance parameter constraints
# received from other categories/channels. Therefore
# we define multiple physics models with the 
# POIs broken down into different groups so we
# can find the significance of a single POI at a time
# but maintain the benefit of the whole analysis
# being constrained.
#
# 1) All combine for reference
# 2) By channel: et, mt, em, tt
# 3) By category: 0jet, boosted, vbf
# 4) By channel by category

#newFolder=Blinded20170228_v3
#FIXME set --control_region=1 when ready
#MorphingSM2016 --output_folder=${newFolder} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=true
#cd output/${newFolder}

# All combined for reference
#combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 8

# Per channel specific workspace
text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
    --PO 'map=htt_em_.*_13TeV/.*H:r_em[1,0,5]' \
    --PO 'map=htt_et_.*_13TeV/.*H:r_et[1,0,5]' \
    --PO 'map=htt_mt_.*_13TeV/.*H:r_mt[1,0,5]' \
    --PO 'map=htt_tt_.*_13TeV/.*H:r_tt[1,0,5]' \
    cmb/125/combined.txt.cmb -o workspace_channel_breakdown.root -m 125

# Per category specific workspace
text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
    --PO 'map=htt_.*_1_13TeV/.*H:r_0jet[1,0,5]' \
    --PO 'map=htt_.*_2_13TeV/.*H:r_boosted[1,0,5]' \
    --PO 'map=htt_.*_3_13TeV/.*H:r_vbf[1,0,5]' \
    cmb/125/combined.txt.cmb -o workspace_category_breakdown.root -m 125

# Per channel per category specific workspace
text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
    --PO 'map=htt_em_1_13TeV/.*H:r_em_1[1,0,5]' \
    --PO 'map=htt_em_2_13TeV/.*H:r_em_2[1,0,5]' \
    --PO 'map=htt_em_3_13TeV/.*H:r_em_3[1,0,5]' \
    --PO 'map=htt_et_1_13TeV/.*H:r_et_1[1,0,5]' \
    --PO 'map=htt_et_2_13TeV/.*H:r_et_2[1,0,5]' \
    --PO 'map=htt_et_3_13TeV/.*H:r_et_3[1,0,5]' \
    --PO 'map=htt_mt_1_13TeV/.*H:r_mt_1[1,0,5]' \
    --PO 'map=htt_mt_2_13TeV/.*H:r_mt_2[1,0,5]' \
    --PO 'map=htt_mt_3_13TeV/.*H:r_mt_3[1,0,5]' \
    --PO 'map=htt_tt_1_13TeV/.*H:r_tt_1[1,0,5]' \
    --PO 'map=htt_tt_2_13TeV/.*H:r_tt_2[1,0,5]' \
    --PO 'map=htt_tt_3_13TeV/.*H:r_tt_3[1,0,5]' \
    cmb/125/combined.txt.cmb -o workspace_channel_and_category_breakdown.root -m 125

# Run for each channel
for SIGNAL in r_em r_et r_mt r_tt; do
    echo ""
    echo "group: Channel " ${SIGNAL}
    combine -M ProfileLikelihood --significance workspace_channel_breakdown.root --setPhysicsModelParameters r_em=1,r_et=1,r_mt=1,r_tt=1 --redefineSignalPOIs ${SIGNAL} -n _Sig${SIGNAL}
done

# Run for each category
for SIGNAL in r_0jet r_boosted r_vbf; do
    echo ""
    echo "group: Category " ${SIGNAL}
    combine -M ProfileLikelihood --significance workspace_category_breakdown.root  --setPhysicsModelParameters r_0jet=1,r_boosted=1,r_vbf=1 --redefineSignalPOIs ${SIGNAL} -n _Sig${SIGNAL}
done

# Run for each category
for SIGNAL in r_em_1 r_em_2 r_em_3 r_et_1 r_et_2 r_et_3 r_mt_1 r_mt_2 r_mt_3 r_tt_1 r_tt_2 r_tt_3; do
    echo ""
    echo "group: Category " ${SIGNAL}
    combine -M ProfileLikelihood --significance workspace_channel_and_category_breakdown.root  --setPhysicsModelParameters r_em_1=1,r_em_2=1,r_em_3=1,r_et_1=1,r_et_2=1,r_et_3=1,r_mt_1=1,r_mt_2=1,r_mt_3=1,r_tt_1=1,r_tt_2=1,r_tt_3=1, --redefineSignalPOIs ${SIGNAL} -n _Sig${SIGNAL}
done

echo ""
echo "group: Combined"
combine -M ProfileLikelihood --significance cmb/125/workspace.root  -n _SigCombined





