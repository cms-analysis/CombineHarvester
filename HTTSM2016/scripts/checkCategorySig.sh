
combineCards.py htt_*_1_13TeV/125/htt_*_1_13TeV.txt > zeroJetDC.txt
combineCards.py htt_*_2_13TeV/125/htt_*_2_13TeV.txt htt_ttbar_1_13TeV/125/*.txt > boostedDC.txt
combineCards.py htt_*_3_13TeV/125/htt_*_3_13TeV.txt htt_ttbar_1_13TeV/125/*.txt > vbfDC.txt

combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 8
combineTool.py -M T2W -m 125 -i zeroJetDC.txt -o workspace1.root --parallel 8
combineTool.py -M T2W -m 125 -i boostedDC.txt -o workspace2.root --parallel 8
combineTool.py -M T2W -m 125 -i vbfDC.txt -o workspace3.root --parallel 8


for NUM in 1 2 3; do
    echo "Number:" ${NUM}
    combine -M ProfileLikelihood --significance workspace${NUM}.root -t -1 --expectSignal=1
done

echo "Combined"
combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --expectSignal=1


