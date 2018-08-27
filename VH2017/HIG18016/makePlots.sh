#python ../scripts/makePostFitPlotsCR2017_sup.py AnalysisOutputs/vhbb2017_shapes.root
#python ../scripts/makePostFitPlots2017.py       AnalysisOutputs/vhbb2017_shapes.root
#
##***S/B ordered plot:***
python ../scripts/plotSoverBordered.py -f AnalysisOutputs/sb_weighted_post_assignment_vzbb_2017.root        --log_y --ratio --custom_y_range --outname sbordered_vzbb2017_Supplementary      --lumi "41.3 fb^{-1} (13 TeV)"                                              --extralabel 'Supplementary'  --VH_label_ypos 1.3e5 
#
#python ../scripts/plotSoverBorderedFromcpp.py -f AnalysisOutputs/sb_weighted_post_assignment_vhbb_2017.root        --log_y --ratio --custom_y_range --outname sbordered_vhbb2017_Supplementary      --lumi "41.3 fb^{-1} (13 TeV)"                                              --extralabel 'Supplementary'
#
#python ../scripts/plotSoverBorderedFromcpp.py -f AnalysisOutputs/sb_weighted_post_assignment_vhonly.root           --log_y --ratio --custom_y_range --outname sbordered_vhonly_Supplementary        --lumi "77.2 fb^{-1} (13 TeV)"                                              --extralabel 'Supplementary'
#
#python ../scripts/plotSoverBorderedFromcpp.py -f AnalysisOutputs/sb_weighted_post_assignment_vhonly_plus_run1.root --log_y --ratio --custom_y_range --outname sbordered_vhonly_plus_run1            --lumi "5.1 fb^{-1} (7 TeV) + 18.9 fb^{-1} (8 TeV) + 77.2 fb^{-1} (13 TeV)"
#
#
#***Additional material cc plot:***
#python ../scripts/plotCCC.py -i MultiDimFit_ccc_additionalmaterial.json -o ccPlotAdditionalMaterial_Supplementary --extralabel 'Supplementary'
#python ../scripts/plotCCC.py -i MultiDimFit_ccc_additionalmaterial.json -o ccPlotAdditionalMaterial_Preliminary --extralabel 'Preliminary'
#
#***Mu summary, full Hbb combination:***
#python ../scripts/summaryPlot.py -i 'AnalysisOutputs/stat_syst_observed_FullHbbComb.json:A1_hbb/*' 'AnalysisOutputs/stat_syst_observed_FullHbbComb.json:A1_hbb_5P/mu_XS_ZH_BR_bb,mu_XS_WH_BR_bb,mu_XS_ttHtH_BR_bb,mu_XS_VBF_BR_bb,mu_XS_ggFbbH_BR_bb' -o mu_summary_obs_run1plusrun2 --translate pois.json --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1' --height 600 --labels 0="Combined" --x-title "Best fit #mu" --subline '5.1 fb^{-1} (7 TeV) + 18.9 fb^{-1} (8 TeV) + 77.2 fb^{-1} (13 TeV)' --x-range='0,10' --width 750
#
#***Mu summary, VH-only combination:***
#python ../scripts/summaryPlotVH.py -i 'AnalysisOutputs/stat_syst_observed_VHOnlyPlot.json:VHRun1Run2/*' 'AnalysisOutputs/stat_syst_observed_VHOnlyPlot.json:VH_run1/*' 'AnalysisOutputs/stat_syst_observed_VHOnlyPlot.json:VH_2017/*' 'AnalysisOutputs/stat_syst_observed_VHOnlyPlot.json:VH_2016/*' 'AnalysisOutputs/stat_syst_observed_VHOnlyPlot.json:VHrun2/*' -o mu_summary_obs_VHonly --vlines '1.0:LineStyle=2' --hlines '1.0:LineStyle=1' '2.0:LineStyle=1' --height 600 --labels 0="Combined",1="Run 1",2="2017",3="2016",4="Run 2" --x-title "Best fit #mu" --subline '5.1 fb^{-1} (7 TeV) + 18.9 fb^{-1} (8 TeV) + 77.2 fb^{-1} (13 TeV)' --x-range='0,3.5' --width 675




export DIRS=vhbb_Wen_1_13TeV2016,vhbb_Wen_2_13TeV2016,vhbb_Wen_3_13TeV2016,vhbb_Wen_4_13TeV2016,vhbb_Wmn_1_13TeV2016,vhbb_Wmn_2_13TeV2016,vhbb_Wmn_3_13TeV2016,vhbb_Wmn_4_13TeV2016,vhbb_Zee_1_13TeV2016,vhbb_Zee_2_13TeV2016,vhbb_Zee_3_13TeV2016,vhbb_Zee_4_13TeV2016,vhbb_Zee_5_13TeV2016,vhbb_Zee_6_13TeV2016,vhbb_Zee_7_13TeV2016,vhbb_Zee_8_13TeV2016,vhbb_Zmm_1_13TeV2016,vhbb_Zmm_2_13TeV2016,vhbb_Zmm_3_13TeV2016,vhbb_Zmm_4_13TeV2016,vhbb_Zmm_5_13TeV2016,vhbb_Zmm_6_13TeV2016,vhbb_Zmm_7_13TeV2016,vhbb_Zmm_8_13TeV2016,vhbb_Znn_1_13TeV2016,vhbb_Znn_2_13TeV2016,vhbb_Znn_3_13TeV2016,vhbb_Znn_4_13TeV2016,vhbb_Wen_1_13TeV2017,vhbb_Wen_2_13TeV2017,vhbb_Wen_3_13TeV2017,vhbb_Wen_4_13TeV2017,vhbb_Wmn_1_13TeV2017,vhbb_Wmn_2_13TeV2017,vhbb_Wmn_3_13TeV2017,vhbb_Wmn_4_13TeV2017,vhbb_Zee_1_13TeV2017,vhbb_Zee_2_13TeV2017,vhbb_Zee_3_13TeV2017,vhbb_Zee_4_13TeV2017,vhbb_Zee_5_13TeV2017,vhbb_Zee_6_13TeV2017,vhbb_Zee_7_13TeV2017,vhbb_Zee_8_13TeV2017,vhbb_Zmm_1_13TeV2017,vhbb_Zmm_2_13TeV2017,vhbb_Zmm_3_13TeV2017,vhbb_Zmm_4_13TeV2017,vhbb_Zmm_5_13TeV2017,vhbb_Zmm_6_13TeV2017,vhbb_Zmm_7_13TeV2017,vhbb_Zmm_8_13TeV2017,vhbb_Znn_1_13TeV2017,vhbb_Znn_2_13TeV2017,vhbb_Znn_3_13TeV2017,vhbb_Znn_4_13TeV2017
export WEIGHTS=2.18251776695,1.20454995334,0.563389338553,0.119766108692,2.27008919418,0.898437984288,0.383157942444,0.115042841062,6.48667296767,2.96908780187,3.30715821683,1.0908950381,1.5469660908,0.371646625921,0.322309277952,0.071404336486,6.09692686796,2.53801263124,3.00464068353,0.953174807131,1.3696834594,0.327793927863,0.290382675827,0.0635606837459,2.11065731943,1.2496779561,0.715630084276,0.307100284845,1.48150682449,0.804383218288,0.351386845112,0.109551861882,1.97497589886,1.14692237973,0.459985695779,0.100629679859,4.11311735213,2.15742979199,2.22783026099,1.01754971221,1.04506763071,0.380578959361,0.183018391952,0.0584016591311,3.92503848672,2.01142670214,2.0984633863,1.00007971749,0.97894039005,0.36052381061,0.172459747642,0.0527528487146,2.85589504242,1.80272145569,1.01317084581,0.390911564231

export WEIGHTS2016=2.18251776695,1.20454995334,0.563389338553,0.119766108692,2.27008919418,0.898437984288,0.383157942444,0.115042841062,6.48667296767,2.96908780187,3.30715821683,1.0908950381,1.5469660908,0.371646625921,0.322309277952,0.071404336486,6.09692686796,2.53801263124,3.00464068353,0.953174807131,1.3696834594,0.327793927863,0.290382675827,0.0635606837459,2.110657,1.2496779561,0.715630084276,0.307100284845
export DIRS2016=vhbb_Wen_1_13TeV2016,vhbb_Wen_2_13TeV2016,vhbb_Wen_3_13TeV2016,vhbb_Wen_4_13TeV2016,vhbb_Wmn_1_13TeV2016,vhbb_Wmn_2_13TeV2016,vhbb_Wmn_3_13TeV2016,vhbb_Wmn_4_13TeV2016,vhbb_Zee_1_13TeV2016,vhbb_Zee_2_13TeV2016,vhbb_Zee_3_13TeV2016,vhbb_Zee_4_13TeV2016,vhbb_Zee_5_13TeV2016,vhbb_Zee_6_13TeV2016,vhbb_Zee_7_13TeV2016,vhbb_Zee_8_13TeV2016,vhbb_Zmm_1_13TeV2016,vhbb_Zmm_2_13TeV2016,vhbb_Zmm_3_13TeV2016,vhbb_Zmm_4_13TeV2016,vhbb_Zmm_5_13TeV2016,vhbb_Zmm_6_13TeV2016,vhbb_Zmm_7_13TeV2016,vhbb_Zmm_8_13TeV2016,vhbb_Znn_1_13TeV2016,vhbb_Znn_2_13TeV2016,vhbb_Znn_3_13TeV2016,vhbb_Znn_4_13TeV2016

export WEIGHTS2017=1.48150682449,0.804383218288,0.351386845112,0.109551861882,1.97497589886,1.14692237973,0.459985695779,0.100629679859,4.11311735213,2.15742979199,2.22783026099,1.01754971221,1.04506763071,0.380578959361,0.183018391952,0.0584016591311,3.92503848672,2.01142670214,2.0984633863,1.00007971749,0.97894039005,0.36052381061,0.172459747642,0.0527528487146,2.85589504242,1.80272145569,1.01317084581,0.390911564231
export DIRS2017=vhbb_Wen_1_13TeV2017,vhbb_Wen_2_13TeV2017,vhbb_Wen_3_13TeV2017,vhbb_Wen_4_13TeV2017,vhbb_Wmn_1_13TeV2017,vhbb_Wmn_2_13TeV2017,vhbb_Wmn_3_13TeV2017,vhbb_Wmn_4_13TeV2017,vhbb_Zee_1_13TeV2017,vhbb_Zee_2_13TeV2017,vhbb_Zee_3_13TeV2017,vhbb_Zee_4_13TeV2017,vhbb_Zee_5_13TeV2017,vhbb_Zee_6_13TeV2017,vhbb_Zee_7_13TeV2017,vhbb_Zee_8_13TeV2017,vhbb_Zmm_1_13TeV2017,vhbb_Zmm_2_13TeV2017,vhbb_Zmm_3_13TeV2017,vhbb_Zmm_4_13TeV2017,vhbb_Zmm_5_13TeV2017,vhbb_Zmm_6_13TeV2017,vhbb_Zmm_7_13TeV2017,vhbb_Zmm_8_13TeV2017,vhbb_Znn_1_13TeV2017,vhbb_Znn_2_13TeV2017,vhbb_Znn_3_13TeV2017,vhbb_Znn_4_13TeV2017





#python ../scripts/postFitPlot.py --file AnalysisOutputs/qshapes4cats5.root  --mode postfit --file_dir $DIRS     --channel Znn --weights $WEIGHTS                                                  --ratio --ratio_range 0.95,1.05  --extralabel "Supplementary" --custom_y_range --y_axis_min 0.001 --y_axis_max 20000 
#python ../scripts/postFitPlot.py --file AnalysisOutputs/qshapes4cats5.root  --mode postfit --file_dir $DIRS     --channel Znn --weights $WEIGHTS      --subbkg 1  --custom_y_range --y_axis_min=-200. --outname 2016and2017 --lumi '77.2 fb^{-1} (13 TeV)'                --extralabel "Supplementary" 
#python ../scripts/postFitPlot.py --file AnalysisOutputs/qshapes4cats5.root  --mode postfit --file_dir $DIRS2017 --channel Znn --weights $WEIGHTS2017  --subbkg 1  --custom_y_range --y_axis_min=-200. --outname only2017    --lumi '41.3 fb^{-1} (13 TeV)' --extralabel "Supplementary" --channel_label "2017"
#python ../scripts/postFitPlot.py --file AnalysisOutputs/qshapes4cats5.root  --mode postfit --file_dir $DIRS2016 --channel Znn --weights $WEIGHTS2016  --subbkg 1  --custom_y_range --y_axis_min=-200. --outname only2016    --lumi '35.9 fb^{-1} (13 TeV)' --extralabel "Supplementary" --channel_label "2016"
