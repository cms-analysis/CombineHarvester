for M in 110 120 125 130 140; do
  echo "Starting from mass = " $M
  combine -M ProfileLikelihood --significance --pvalue cmb/$M/workspace.root -t -1 --toysFrequentist --expectSignal=1 -m $M -n _Exp
  combine -M ProfileLikelihood --significance --pvalue cmb/$M/workspace.root -m $M -n _Obs
done
hadd -f Tot_pvalue_Exp.root higgsCombine_Exp.ProfileLikelihood.mH*.root
hadd -f Tot_pvalue_Obs.root higgsCombine_Obs.ProfileLikelihood.mH*.root
python $PWD/../../../scripts/makeSignificancePlots.py -d $PWD/../../../scripts/Significance.dat


