combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 18

combineTool.py -M Asymptotic  -d */*/workspace.root --there -n .limit --parallel 18

combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json

combine -M MaxLikelihoodFit cmb/125/workspace.root  --robustFit=1 --minimizerAlgoForMinos=Minuit2,Migrad  --rMin 0.5 --rMax 1.5

python ../../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py  mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt



cp ../../../scripts/runPvalue.sh .
sh  runPvalue.sh .




cp ../../../scripts/runSBWeighted.sh .
sh runSBWeighted.sh


