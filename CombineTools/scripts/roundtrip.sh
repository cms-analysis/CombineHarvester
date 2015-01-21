WORKAREA="output/roundtrip"
DEF_MLFIT="--rMin=-5 --rMax=5 --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --robustFit=1 --setPhysicsModelParameters MH=125 --freezeNuisances MH"
mkdir -p ${WORKAREA}


SOURCE_vhbb="output/cmshcg/summer2013/searches/vhbb/125"

cd ${SOURCE_vhbb}
combineCards.py \
  vhbb_Wln_7TeV=vhbb_Wln_7TeV.txt \
  vhbb_Wln_8TeV=vhbb_Wln_8TeV.txt \
  vhbb_Wtn_8TeV=vhbb_Wtn_8TeV.txt \
  vhbb_Zll_7TeV=vhbb_Zll_7TeV.txt \
  vhbb_Zll_8TeV=vhbb_Zll_8TeV.txt \
  vhbb_Znn_7TeV=vhbb_Znn_7TeV.txt \
  vhbb_Znn_8TeV=vhbb_Znn_8TeV.txt &> vhbb_in.txt
cd -

./bin/RoundTrip -i ${SOURCE_vhbb}/vhbb_in.txt -o ${WORKAREA}/vhbb_out.txt -r ${WORKAREA}/vhbb_out.root -m 125 --print &> ${WORKAREA}/vhbb.log

text2workspace.py -b ${SOURCE_vhbb}/vhbb_in.txt -o ${WORKAREA}/ws_vhbb_in.root  --default-morphing shape2 -m 125
text2workspace.py -b ${WORKAREA}/vhbb_out.txt   -o ${WORKAREA}/ws_vhbb_out.root --default-morphing shape2 -m 125


combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_vhbb_in.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_vhbb_in.root
combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_vhbb_out.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_vhbb_out.root

./bin/PostFitShapes -d ${WORKAREA}/vhbb_out.txt -o ${WORKAREA}/shapes_vhbb_out.root -m 125 -f ${WORKAREA}/mlfit_vhbb_out.root:fit_s --postfit --sampling --print


SOURCE_hww2l2v="output/cmshcg/summer2013/searches/hww2l2v/125"

cd ${SOURCE_hww2l2v}
combineCards.py \
  hwwof_0j_shape_7TeV=hwwof_0j_shape_7TeV.txt \
  hwwof_1j_shape_7TeV=hwwof_1j_shape_7TeV.txt \
  hwwof_2j_shape_7TeV=hwwof_2j_shape_7TeV.txt \
  hwwof_0j_shape_8TeV=hwwof_0j_shape_8TeV.txt \
  hwwof_1j_shape_8TeV=hwwof_1j_shape_8TeV.txt \
  hwwof_2j_shape_8TeV=hwwof_2j_shape_8TeV.txt &> hww2l2v_in.txt
cd -

./bin/RoundTrip -i ${SOURCE_hww2l2v}/hww2l2v_in.txt -o ${WORKAREA}/hww2l2v_out.txt -r ${WORKAREA}/hww2l2v_out.root -m 125 --print &> ${WORKAREA}/hww2l2v.log

text2workspace.py -b ${SOURCE_hww2l2v}/hww2l2v_in.txt -o ${WORKAREA}/ws_hww2l2v_in.root  --default-morphing shape2 -m 125
text2workspace.py -b ${WORKAREA}/hww2l2v_out.txt -o ${WORKAREA}/ws_hww2l2v_out.root --default-morphing shape2 -m 125

combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hww2l2v_in.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hww2l2v_in.root
combine -M MaxLikelihoodFit ${DEF_MLFIT} --out=${WORKAREA} -m 125 ${WORKAREA}/ws_hww2l2v_out.root
mv ${WORKAREA}/mlfit.root ${WORKAREA}/mlfit_hww2l2v_out.root

./bin/PostFitShapes -d ${WORKAREA}/hww2l2v_out.txt -o ${WORKAREA}/shapes_hww2l2v_out.root -m 125 -f ${WORKAREA}/mlfit_hww2l2v_out.root:fit_s --postfit --sampling --print