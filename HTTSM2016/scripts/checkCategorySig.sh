#XXX 
#XXX N.B. this is not the proper way to do this. See
#XXX scripts/channelCompatibilityCheck.sh
#XXX 
# Script to produce significances for different category and channel
# breakdowns
#
# Run like this:
# MorphingSM2016 --output_folder=${newFolder} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=true
## Building the workspaces:
# cd output/${newFolder}
# cp ../../scripts/checkCategorySig.sh .
# source ./checkCategorySig.sh > results.txt
# grep -e "Sig" -e "Ch" -e "Ca" -e "Comb" results.txt > summary.txt
#
#
# Then check summary.txt or results.txt for additional info

# Make combined workspace
combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace_cmb.root --parallel 8



# Combine to give us category based cards/workspaces
combineCards.py htt_*_1_13TeV/125/htt_*_1_13TeV.txt > zeroJetDC.txt
combineCards.py htt_*_2_13TeV/125/htt_*_2_13TeV.txt htt_ttbar_1_13TeV/125/*.txt > boostedDC.txt
combineCards.py htt_*_3_13TeV/125/htt_*_3_13TeV.txt htt_ttbar_1_13TeV/125/*.txt > vbfDC.txt

combineTool.py -M T2W -m 125 -i zeroJetDC.txt -o workspace_1.root --parallel 8
combineTool.py -M T2W -m 125 -i boostedDC.txt -o workspace_2.root --parallel 8
combineTool.py -M T2W -m 125 -i vbfDC.txt -o workspace_3.root --parallel 8



# Combine to give us channel based cards/workshapces
for CHANNEL in em et mt tt; do
    combineCards.py htt_${CHANNEL}_*_13TeV/125/htt_${CHANNEL}_*_13TeV.txt > ${CHANNEL}.txt
    combineTool.py -M T2W -m 125 -i ${CHANNEL}.txt -o workspace_${CHANNEL}.root  --parallel 8
done



# Combine to give us per channel per category cards/workspaces
for NUM in 1 2 3; do
    for CHANNEL in em et mt tt; do
        combineTool.py -M T2W -m 125 -i htt_${CHANNEL}_${NUM}_13TeV/125/htt_${CHANNEL}_${NUM}_13TeV.txt -o workspace_${CHANNEL}_${NUM}.root  --parallel 8
    done
done

for CHANNEL in em et mt tt; do
    echo ""
    echo ""
    echo "Channel:" ${CHANNEL}
    combine -M ProfileLikelihood --significance workspace_${CHANNEL}.root -t -1 --expectSignal=1
done

for NUM in 1 2 3; do
    for CHANNEL in em et mt tt; do
        echo ""
        echo ""
        echo "Channel && Number:" ${CHANNEL} ${NUM}
        combine -M ProfileLikelihood --significance htt_${CHANNEL}_${NUM}_13TeV/125/workspace_${CHANNEL}_${NUM}.root -t -1 --expectSignal=1
    done
done

for NUM in 1 2 3; do
    echo ""
    echo ""
    echo "Category based Number:" ${NUM}
    combine -M ProfileLikelihood --significance workspace_${NUM}.root -t -1 --expectSignal=1
done

echo ""
echo ""
echo "Combined"
combine -M ProfileLikelihood --significance cmb/125/workspace_cmb.root -t -1 --expectSignal=1



