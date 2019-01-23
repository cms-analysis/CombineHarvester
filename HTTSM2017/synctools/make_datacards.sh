
INPUT=$1
ERA=$2
REAL=$3

eval `scramv1 runtime -sh`
cd ${CMSSW_BASE}/src/CombineHarvester/HTTSM2017


rm -r output/*_smhtt
MorphingSM2017 --input_folder_mt="${INPUT}/"  --input_folder_et="${INPUT}/"  --input_folder_tt="${INPUT}/"  --input_folder_em="KIT/"  --real_data=${REAL}  --embedding=true --classic_bbb=false  --auto_rebin=true   --stxs_signals=stxs_stage0 --categories=stxs_stage1  --era=2017  --output="2017_smhtt"
MorphingSM2017 --input_folder_mt="${INPUT}/"  --input_folder_et="${INPUT}/"  --input_folder_tt="${INPUT}/"  --input_folder_em="KIT/"  --real_data=${REAL}  --embedding=true --classic_bbb=false  --auto_rebin=true   --stxs_signals=stxs_stage0 --categories=stxs_stage1  --era=2016  --output="2016_smhtt"

cd output/2017_smhtt/cmb/125/
for FILE in *.txt
do
    sed -i '$s/$/\n * autoMCStats 0.0/' $FILE
done
cd -
cd output/2016_smhtt/cmb/125/
for FILE in *.txt
do
    sed -i '$s/$/\n * autoMCStats 0.0/' $FILE
done
cd -

mkdir -p output/cmb_smhtt/cmb/125
mkdir -p output/cmb_smhtt/cmb/common

cp -p output/2016_smhtt/cmb/125/*txt  output/cmb_smhtt/cmb/125/
cp -p output/2016_smhtt/cmb/common/*  output/cmb_smhtt/cmb/common/

cp -p output/2017_smhtt/cmb/125/*txt  output/cmb_smhtt/cmb/125/
cp -p output/2017_smhtt/cmb/common/*  output/cmb_smhtt/cmb/common/