make -j4
./bin/ParametricMSSM
text2workspace.py -b htt_mssm_hm.txt  -o htt_mssm_hm.root --default-morphing shape2 -m 900
combine -M MaxLikelihoodFit --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1  --rMin -5 --rMax 5  --out=out htt_mssm_hm.root
