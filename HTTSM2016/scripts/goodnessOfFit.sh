# Base off ./HIG16006/input/mssm_protocol.txt



# We look at the Goodness of Fit for three different algorithms. 
# The saturated model (saturated), Anderson-Darling (AD) and 
# Kolmogorow-Smirnow (KS). For the AD and KS it is sufficient to 
# run the fits for the combined cards as the test-statitic for 
# the individual channels can be extracted from these results. 
# For the saturated model it is necessary to run them independtly 
# of each other.


###  THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!  ###
echo ""
echo ""
echo "THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!"
echo ""
echo ""

newFolder=Blinded20170305_v1_bbb
MorphingSM2016 --output_folder=${newFolder} --postfix="-2D" --control_region=1 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=true
## Building the workspaces:
cd output/${newFolder}
combineTool.py -M T2W -i {cmb,em,et,mt,tt}/* -o workspace.root --parallel 12





# Do Anderson Darling first
ALGO=AD
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d cmb/125/workspace.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d cmb/125/workspace.root -n ".$ALGO" --fixedSignalStrength=1

combineTool.py -M CollectGoodnessOfFit --input cmb/125/higgsCombine.${ALGO}.GoodnessOfFit.mH125.root cmb/125/higgsCombine.${ALGO}.toys.GoodnessOfFit.mH125.*.root -o collectGoodness_${ALGO}.json

python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-AD'





# Do KS test
ALGO=KS
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d cmb/125/workspace.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d cmb/125/workspace.root -n ".$ALGO" --fixedSignalStrength=1

combineTool.py -M CollectGoodnessOfFit --input cmb/125/higgsCombine.${ALGO}.GoodnessOfFit.mH125.root cmb/125/higgsCombine.${ALGO}.toys.GoodnessOfFit.mH125.*.root -o collectGoodness_${ALGO}.json

python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-KS'





# Do Saturated
# For the saturated model run for each category seperatly
# We need to make indivual workspaces for each channel/bin
ALGO=saturated

for CHANNEL in em et mt tt; do
    for BIN in 1 2 3; do
        echo "Saturated for ${CHANNEL} ${BIN}"
        combineTool.py -M T2W -i htt_${CHANNEL}_${BIN}_13TeV/125/*.txt -o workspace_${CHANNEL}_${BIN}.root --parallel 2
        combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d htt_${CHANNEL}_${BIN}_13TeV/125/workspace_${CHANNEL}_${BIN}.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
        combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d htt_${CHANNEL}_${BIN}_13TeV/125/workspace_${CHANNEL}_${BIN}.root -n ".$ALGO" --fixedSignalStrength=1
        combineTool.py -M CollectGoodnessOfFit --input htt_${CHANNEL}_${BIN}_13TeV/125/higgsCombine.saturated.GoodnessOfFit.mH125.root htt_${CHANNEL}_${BIN}_13TeV/125/higgsCombine.saturated.toys.GoodnessOfFit.mH125.*.root -o htt_${CHANNEL}_${BIN}_saturated.json
    done
done

# Do saturated plotting separately to properly label
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_em_1_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='em_1-Saturated' --title-left="e#mu, 0-jet"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_em_2_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='em_2-Saturated' --title-left="e#mu, Boosted"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_em_3_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='em_3-Saturated' --title-left="e#mu, VBF"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_et_1_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='et_1-Saturated' --title-left="e#tau_{h}, 0-jet"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_et_2_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='et_2-Saturated' --title-left="e#tau_{h}, Boosted"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_et_3_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='et_3-Saturated' --title-left="e#tau_{h}, VBF"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_mt_1_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mt_1-Saturated' --title-left="#mu#tau_{h}, 0-jet"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_mt_2_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mt_2-Saturated' --title-left="#mu#tau_{h}, Boosted"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_mt_3_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mt_3-Saturated' --title-left="#mu#tau_{h}, VBF"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_tt_1_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='tt_1-Saturated' --title-left="#tau_{h}#tau_{h}, 0-jet"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_tt_2_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='tt_2-Saturated' --title-left="#tau_{h}#tau_{h}, Boosted"
python ../../../CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 htt_tt_3_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='tt_3-Saturated' --title-left="#tau_{h}#tau_{h}, VBF"








