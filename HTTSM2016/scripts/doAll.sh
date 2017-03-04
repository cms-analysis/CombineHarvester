combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 8

combineTool.py -M Asymptotic -t -1 -d */*/workspace.root --there -n .limit --parallel 8

combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json

combine -M MaxLikelihoodFit cmb/125/workspace.root -t -1  --robustFit=1 --minimizerAlgoForMinos=Minuit2,Migrad  --rMin 0.5 --rMax 1.5 --expectSignal=1

python ../../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py  mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt

combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --parallel 8

combineTool.py -M Impacts -d cmb/125/workspace.root -m 125 --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --doFits -t -1 --rMin 0.5 --rMax 1.5 --expectSignal=1 --job-mode lxbatch --task-name lxbatch-test --sub-opts='-q 8nh' --merge 5


combine -M ProfileLikelihood --significance cmb/125/workspace.root -t -1 --expectSignal=1

cp ../../../scripts/runPvalue.sh .
sh  runPvalue.sh .


cp ../../../scripts/runSBWeighted.sh .
sh runSBWeighted.sh


