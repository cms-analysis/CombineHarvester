FOLDER="output/sm_cards"
CHANNELS=(
  'ee'
  'mm'
  'et'
  'mt'
  'em'
  'tt'
  )

cd ${FOLDER}

for i in "${CHANNELS[@]}"
do
    echo "**************** CHANNEL:${i}"
    text2workspace.py -b htt_${i}_125.txt -o htt_${i}_125.root --default-morphing shape2 -m 125;
    combine -M Asymptotic --rMin -5 --rMax 5 --run expected htt_${i}_125.root -m 125 -n Expected${i}
    combine -M Asymptotic --rMin -5 --rMax 5 --run observed htt_${i}_125.root -m 125 -n Observed${i}
done
