WORKAREA="output/roundtrip"
DEF_MLFIT="--rMin=-5 --rMax=5 --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=1.0 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --robustFit=1 --setPhysicsModelParameters MH=125 --freezeNuisances MH"
mkdir -p ${WORKAREA}

MODEL="-P HiggsAnalysis.CombinedLimit.TwoHiggsModels:justOneHiggs --PO verbose"

# SOURCE_vhbb="output/cmshcg/summer2013/searches/vhbb/125"

# cd ${SOURCE_vhbb}
# combineCards.py \
#   vhbb_Wln_7TeV=vhbb_Wln_7TeV.txt \
#   vhbb_Wln_8TeV=vhbb_Wln_8TeV.txt \
#   vhbb_Wtn_8TeV=vhbb_Wtn_8TeV.txt \
#   vhbb_Zll_7TeV=vhbb_Zll_7TeV.txt \
#   vhbb_Zll_8TeV=vhbb_Zll_8TeV.txt \
#   vhbb_Znn_7TeV=vhbb_Znn_7TeV.txt \
#   vhbb_Znn_8TeV=vhbb_Znn_8TeV.txt &> vhbb_in.txt
# cd -

# ./bin/RoundTrip -i ${SOURCE_vhbb}/vhbb_in.txt -o ${WORKAREA}/vhbb_out.txt -r ${WORKAREA}/vhbb_out.root -m 125 --print &> ${WORKAREA}/vhbb.log

# text2workspace.py -b ${SOURCE_vhbb}/vhbb_in.txt -o ${WORKAREA}/ws_vhbb_in.root  --default-morphing shape2 -m 125 ${MODEL}
# text2workspace.py -b ${WORKAREA}/vhbb_out.txt   -o ${WORKAREA}/ws_vhbb_out.root --default-morphing shape2 -m 125 ${MODEL}


# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_vhbb_in.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_vhbb_in.root
# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_vhbb_out.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_vhbb_out.root

# ./bin/PostFitShapes -d ${WORKAREA}/vhbb_out.txt -o ${WORKAREA}/shapes_vhbb_out.root -m 125 -f ${WORKAREA}/mlfit_vhbb_out.root:fit_s --postfit --sampling --print


# SOURCE_hww2l2v="output/cmshcg/summer2013/searches/hww2l2v/125"

# cd ${SOURCE_hww2l2v}
# combineCards.py \
#   hwwof_0j_shape_7TeV=hwwof_0j_shape_7TeV.txt \
#   hwwof_1j_shape_7TeV=hwwof_1j_shape_7TeV.txt \
#   hwwof_2j_shape_7TeV=hwwof_2j_shape_7TeV.txt \
#   hwwof_0j_shape_8TeV=hwwof_0j_shape_8TeV.txt \
#   hwwof_1j_shape_8TeV=hwwof_1j_shape_8TeV.txt \
#   hwwof_2j_shape_8TeV=hwwof_2j_shape_8TeV.txt &> hww2l2v_in.txt
# cd -

# ./bin/RoundTrip -i ${SOURCE_hww2l2v}/hww2l2v_in.txt -o ${WORKAREA}/hww2l2v_out.txt -r ${WORKAREA}/hww2l2v_out.root -m 125 --print &> ${WORKAREA}/hww2l2v.log

# text2workspace.py -b ${SOURCE_hww2l2v}/hww2l2v_in.txt -o ${WORKAREA}/ws_hww2l2v_in.root  --default-morphing shape2 -m 125 ${MODEL}
# text2workspace.py -b ${WORKAREA}/hww2l2v_out.txt -o ${WORKAREA}/ws_hww2l2v_out.root --default-morphing shape2 -m 125 ${MODEL}

# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hww2l2v_in.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hww2l2v_in.root
# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hww2l2v_out.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hww2l2v_out.root

# ./bin/PostFitShapes -d ${WORKAREA}/hww2l2v_out.txt -o ${WORKAREA}/shapes_hww2l2v_out.root -m 125 -f ${WORKAREA}/mlfit_hww2l2v_out.root:fit_s --postfit --sampling --print


# SOURCE_hzz4l="output/cmshcg/summer2013/searches/hzz4l/125"
# cd ${SOURCE_hzz4l}
# combineCards.py \
#   hzz4l_2e2muS_7TeV_0=hzz4l_2e2muS_7TeV_0.txt \
#   hzz4l_2e2muS_7TeV_1=hzz4l_2e2muS_7TeV_1.txt \
#   hzz4l_2e2muS_8TeV_0=hzz4l_2e2muS_8TeV_0.txt \
#   hzz4l_2e2muS_8TeV_1=hzz4l_2e2muS_8TeV_1.txt \
#   hzz4l_4eS_7TeV_0=hzz4l_4eS_7TeV_0.txt \
#   hzz4l_4eS_7TeV_1=hzz4l_4eS_7TeV_1.txt \
#   hzz4l_4eS_8TeV_0=hzz4l_4eS_8TeV_0.txt \
#   hzz4l_4eS_8TeV_1=hzz4l_4eS_8TeV_1.txt \
#   hzz4l_4muS_7TeV_0=hzz4l_4muS_7TeV_0.txt \
#   hzz4l_4muS_7TeV_1=hzz4l_4muS_7TeV_1.txt \
#   hzz4l_4muS_8TeV_0=hzz4l_4muS_8TeV_0.txt \
#   hzz4l_4muS_8TeV_1=hzz4l_4muS_8TeV_1.txt &> hzz4l_in.txt
# cd -

# ./bin/RoundTrip -i ${SOURCE_hzz4l}/hzz4l_in.txt -o ${WORKAREA}/hzz4l_out.txt -r ${WORKAREA}/hzz4l_out.root -m 125 --print &> ${WORKAREA}/hzz4l.log

# text2workspace.py -b ${SOURCE_hzz4l}/hzz4l_in.txt -o ${WORKAREA}/ws_hzz4l_in.root  --default-morphing shape2 -m 125 ${MODEL}
# text2workspace.py -b ${WORKAREA}/hzz4l_out.txt -o ${WORKAREA}/ws_hzz4l_out.root --default-morphing shape2 -m 125 ${MODEL}

# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hzz4l_in.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hzz4l_in.root
# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hzz4l_out.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hzz4l_out.root

# ./bin/PostFitShapes -d ${WORKAREA}/hzz4l_out.txt -o ${WORKAREA}/shapes_hzz4l_out.root -m 125 -f ${WORKAREA}/mlfit_hzz4l_out.root:fit_s --postfit --sampling --print



SOURCE_hgg="output/cmshcg/summer2013/searches/hgg"
cd ${SOURCE_hgg}
combineCards.py \
  hsm_all_mvab_8=hsm_all_mvab_8.txt &> hgg_in.txt
  # hsm_all_mvab_7=hsm_all_mvab_7.txt \
cd -

./bin/RoundTrip -i ${SOURCE_hgg}/hgg_in.txt -o ${WORKAREA}/hgg_out.txt -r ${WORKAREA}/hgg_out.root -m 125 --print &> ${WORKAREA}/hgg.log

text2workspace.py -b ${SOURCE_hgg}/hgg_in.txt -o ${WORKAREA}/ws_hgg_in.root  --default-morphing shape2 -m 125 ${MODEL}
text2workspace.py -b ${WORKAREA}/hgg_out.txt -o ${WORKAREA}/ws_hgg_out.root --default-morphing shape2 -m 125 ${MODEL}

combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hgg_in.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hgg_in.root
combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hgg_out.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hgg_out.root




SOURCE_htt="output/cmshcg/summer2013/searches/htt_HwwAsBg/125"

cd ${SOURCE_htt}
# combineCards.py \
# htt_ee_0_7TeV=htt_ee_0_7TeV.txt \
# htt_ee_0_8TeV=htt_ee_0_8TeV.txt \
# htt_ee_1_7TeV=htt_ee_1_7TeV.txt \
# htt_ee_1_8TeV=htt_ee_1_8TeV.txt \
# htt_ee_2_7TeV=htt_ee_2_7TeV.txt \
# htt_ee_2_8TeV=htt_ee_2_8TeV.txt \
# htt_ee_3_7TeV=htt_ee_3_7TeV.txt \
# htt_ee_3_8TeV=htt_ee_3_8TeV.txt \
# htt_ee_4_7TeV=htt_ee_4_7TeV.txt \
# htt_ee_4_8TeV=htt_ee_4_8TeV.txt &> htt_in.txt

# combineCards.py \
# htt_em_0_7TeV=htt_em_0_7TeV.txt \
# htt_em_0_8TeV=htt_em_0_8TeV.txt \
# htt_em_1_7TeV=htt_em_1_7TeV.txt \
# htt_em_1_8TeV=htt_em_1_8TeV.txt \
# htt_em_2_7TeV=htt_em_2_7TeV.txt \
# htt_em_2_8TeV=htt_em_2_8TeV.txt \
# htt_em_3_7TeV=htt_em_3_7TeV.txt \
# htt_em_3_8TeV=htt_em_3_8TeV.txt \
# htt_em_4_7TeV=htt_em_4_7TeV.txt \
# htt_em_4_8TeV=htt_em_4_8TeV.txt \
# htt_em_5_8TeV=htt_em_5_8TeV.txt &> htt_in.txt

# combineCards.py \
# htt_et_1_7TeV=htt_et_1_7TeV.txt \
# htt_et_1_8TeV=htt_et_1_8TeV.txt \
# htt_et_2_7TeV=htt_et_2_7TeV.txt \
# htt_et_2_8TeV=htt_et_2_8TeV.txt \
# htt_et_3_7TeV=htt_et_3_7TeV.txt \
# htt_et_3_8TeV=htt_et_3_8TeV.txt \
# htt_et_5_7TeV=htt_et_5_7TeV.txt \
# htt_et_5_8TeV=htt_et_5_8TeV.txt \
# htt_et_6_7TeV=htt_et_6_7TeV.txt \
# htt_et_6_8TeV=htt_et_6_8TeV.txt \
# htt_et_7_8TeV=htt_et_7_8TeV.txt &> htt_in.txt

# combineCards.py \
# htt_mm_0_7TeV=htt_mm_0_7TeV.txt \
# htt_mm_0_8TeV=htt_mm_0_8TeV.txt \
# htt_mm_1_7TeV=htt_mm_1_7TeV.txt \
# htt_mm_1_8TeV=htt_mm_1_8TeV.txt \
# htt_mm_2_7TeV=htt_mm_2_7TeV.txt \
# htt_mm_2_8TeV=htt_mm_2_8TeV.txt \
# htt_mm_3_7TeV=htt_mm_3_7TeV.txt \
# htt_mm_3_8TeV=htt_mm_3_8TeV.txt \
# htt_mm_4_7TeV=htt_mm_4_7TeV.txt \
# htt_mm_4_8TeV=htt_mm_4_8TeV.txt &> htt_in.txt

# combineCards.py \
# htt_mt_1_7TeV=htt_mt_1_7TeV.txt \
# htt_mt_1_8TeV=htt_mt_1_8TeV.txt \
# htt_mt_2_7TeV=htt_mt_2_7TeV.txt \
# htt_mt_2_8TeV=htt_mt_2_8TeV.txt \
# htt_mt_3_7TeV=htt_mt_3_7TeV.txt \
# htt_mt_3_8TeV=htt_mt_3_8TeV.txt \
# htt_mt_4_7TeV=htt_mt_4_7TeV.txt \
# htt_mt_4_8TeV=htt_mt_4_8TeV.txt \
# htt_mt_5_7TeV=htt_mt_5_7TeV.txt \
# htt_mt_5_8TeV=htt_mt_5_8TeV.txt \
# htt_mt_6_7TeV=htt_mt_6_7TeV.txt \
# htt_mt_6_8TeV=htt_mt_6_8TeV.txt \
# htt_mt_7_8TeV=htt_mt_7_8TeV.txt &> htt_in.txt

# combineCards.py \
# htt_tt_0_8TeV=htt_tt_0_8TeV.txt \
# htt_tt_1_8TeV=htt_tt_1_8TeV.txt \
# htt_tt_2_8TeV=htt_tt_2_8TeV.txt &> htt_in.txt

# combineCards.py \
# vhtt_0_7TeV=vhtt_0_7TeV.txt \
# vhtt_0_8TeV=vhtt_0_8TeV.txt \
# vhtt_1_7TeV=vhtt_1_7TeV.txt \
# vhtt_1_8TeV=vhtt_1_8TeV.txt \
# vhtt_3_7TeV=vhtt_3_7TeV.txt \
# vhtt_3_8TeV=vhtt_3_8TeV.txt \
# vhtt_4_7TeV=vhtt_4_7TeV.txt \
# vhtt_4_8TeV=vhtt_4_8TeV.txt \
# vhtt_5_7TeV=vhtt_5_7TeV.txt \
# vhtt_5_8TeV=vhtt_5_8TeV.txt \
# vhtt_6_7TeV=vhtt_6_7TeV.txt \
# vhtt_6_8TeV=vhtt_6_8TeV.txt \
# vhtt_7_7TeV=vhtt_7_7TeV.txt \
# vhtt_7_8TeV=vhtt_7_8TeV.txt \
# vhtt_8_7TeV=vhtt_8_7TeV.txt \
# vhtt_8_8TeV=vhtt_8_8TeV.txt &> htt_in.txt
# cd -

# ./bin/RoundTrip -i ${SOURCE_htt}/htt_in.txt -o ${WORKAREA}/htt_out.txt -r ${WORKAREA}/htt_out.root -m 125 --print &> ${WORKAREA}/htt.log

# text2workspace.py -b ${SOURCE_htt}/htt_in.txt -o ${WORKAREA}/ws_htt_in.root  --default-morphing shape2 -m 125 ${MODEL}
# text2workspace.py -b ${WORKAREA}/htt_out.txt -o ${WORKAREA}/ws_htt_out.root --default-morphing shape2 -m 125  ${MODEL}

# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_htt_in.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_htt_in.root
# combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_htt_out.root
# mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_htt_out.root

# ./bin/PostFitShapes -d ${WORKAREA}/htt_out.txt -o ${WORKAREA}/shapes_htt_out.root -m 125 -f ${WORKAREA}/mlfit_htt_out.root:fit_s --postfit --sampling --print


