mass=(120 125 130)
for ((M=120; M <= 130 ; M += 5)); do
  echo "Starting from mass = " $M
  combine -M ProfileLikelihood --significance --pvalue cmb/$M/workspace.root -t -1 --expectSignal=1 -m $M 
done
hadd -f Tot_pvalue.root higgsCombineTest.ProfileLikelihood.mH*.root
python $PWD/../../../scripts/makeSignificancePlots.py -d $PWD/../../../scripts/Significance.dat


