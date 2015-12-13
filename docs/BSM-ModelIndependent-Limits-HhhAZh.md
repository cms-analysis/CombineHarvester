BSM Model independent Limits using MorphingHhh or MorphingAZh {#ModelIndepHhhAZh}
=================================================================

The model independent limits for the H->hh and A->Zh analyses (HIG-14-034) are slightly simpler than for the MSSM H->tautau analysis, since only one signal process is considered and hence no profiling is required. This removes the need for any kind of physics model at the text2workspace step.

Creating datacards {#Hhh-Azh-p1}
========================

The first step is to create the datacards, which will be used to produce the limit later on. To do this, go into the Folder CombineHarvester/Run1BSMComb/ and then execute MorphingHhh or MorphingAZh. All of the programs in the following steps also need to be executed from this folder. Also make sure that all the files have been compiled beforehand:

    cd CombineHarvester/Run1BSMComb/
    MorphingAZh
    MorphingHhh

MorphingHhh.cpp and MorphingAZh.cpp are setup similarly to Example2 and MorphingMSSMUpdate as documented previously. No additional option -m MH is needed as in the case of the MSSMUpdate cards because there is only one Higgs boson considered anyway for these analyses. 


Creating the workspace {#Hhh-Azh-p2}
=======================================

Now that the datacards have been created, we can create a workspace as follows:

text2workspace.py -b output/AZh_cards_nomodel/htt_cmb_AZh.txt -o output/AZh_cards_nomodel/htt_cmb_AZh.root --default-morphing shape2
text2workspace.py -b output/hhh_cards_nomodel/htt_cmb_Hhh.txt -o output/hhh_cards_nomodel/htt_cmb_Hhh.root --default-morphing shape2

This creates a workspace based on the combined datacard.


Calculating values {#Hhh-Azh-p3}
========================

Now that we have created the workspace, we can now run combineTool.py to run the limit for a given masspoint:

python ../CombineTools/scripts/combineTool.py -m 260 -M Asymptotic output/hhh_cards_nomodel/htt_cmb_Hhh.root --freezeNuisances mH --setPhysicsModelParameters mH=260
python ../CombineTools/scripts/combineTool.py -m 220 -M Asymptotic output/AZh_cards_nomodel/htt_cmb_AZh.root --freezeNuisances mA --setPhysicsModelParameters mA=220

This will run the asymptotic limit calculation for mH=260 for the H->hh cards and mA=220 for the A->Zh cards. Note that it is necessary to use the combine options to set the masspoint and to freeze the parameter controlling it so that it is not floated in the fit. 
