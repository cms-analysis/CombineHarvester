#!/bin/bash
WSP=$1;
POIsF=""
if [[ "$1" == "" ]]; then echo "usage: $0 model"; exit 1; fi;
  BRU="param_alphaS,param_mB,param_mC,param_mt,HiggsDecayWidthTHU_hqq,HiggsDecayWidthTHU_hvv,HiggsDecayWidthTHU_hll,HiggsDecayWidthTHU_hgg,HiggsDecayWidthTHU_hzg,HiggsDecayWidthTHU_hgluglu"
  THEORY="QCDscale_ggH,QCDscale_qqH,QCDscale_VH,QCDscale_ttH,pdf_Higgs_gg,pdf_Higgs_qq,pdf_Higgs_qg,pdf_Higgs_ttH,${BRU}"
  B1WW_POIS="mu_XS_ggF_x_BR_WW mu_XS_VBF_r_XS_ggF mu_XS_ttH_r_XS_ggF mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_tautau_r_BR_WW mu_BR_bb_r_BR_WW mu_BR_gamgam_r_BR_WW mu_BR_ZZ_r_BR_WW"
  B1WW_RANGES="mu_XS_VBF_r_XS_ggF=-2,5:mu_XS_WH_r_XS_ggF=-2,10:mu_XS_ZH_r_XS_ggF=-2,20:mu_XS_ttH_r_XS_ggF=-2,20:mu_BR_ZZ_r_BR_WW=-2,5:mu_BR_bb_r_BR_WW=-2,5:mu_BR_tautau_r_BR_WW=-2,5:mu_BR_gamgam_r_BR_WW=-2,5:mu_XS_ggF_x_BR_WW=-2,5"
  B1ZZ_POIS="mu_XS_ggF_x_BR_ZZ mu_XS_VBF_r_XS_ggF mu_XS_ttH_r_XS_ggF mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_tautau_r_BR_ZZ mu_BR_bb_r_BR_ZZ mu_BR_gamgam_r_BR_ZZ mu_BR_WW_r_BR_ZZ"
  B1ZZ_RANGES="mu_XS_VBF_r_XS_ggF=-2,5:mu_XS_WH_r_XS_ggF=-2,10:mu_XS_ZH_r_XS_ggF=-2,20:mu_XS_ttH_r_XS_ggF=-2,20:mu_BR_WW_r_BR_ZZ=-2,5:mu_BR_bb_r_BR_ZZ=-2,5:mu_BR_tautau_r_BR_ZZ=-2,5:mu_BR_gamgam_r_BR_ZZ=-2,5:mu_XS_ggF_x_BR_ZZ=-2,5"
case $WSP in
A1_mu) POIs="mu" ;
       POIsF=",${BRU}";
       POIsR="mu=0,2" ;;
A1_4P) POIs="mu_XS_ggFbbH mu_XS_VBF mu_XS_VH mu_XS_ttHtH" ;
       POIsF=",${BRU}";
       POIsR="mu_XS_ggFbbH=-2,2:mu_XS_VBF=-5,5:mu_XS_VH=-10,10:mu_XS_ttHtH=-10,10" ;;
A1_5P) POIs="mu_XS_ggFbbH mu_XS_VBF mu_XS_WH mu_XS_ZH mu_XS_ttHtH" ;
       POIsF=",${BRU}";
       POIsR="mu_XS_ggFbbH=-2,2:mu_XS_VBF=-5,5:mu_XS_WH=-10,10:mu_XS_ZH=-10,10:mu_XS_ttHtH=-10,10" ;;
A1_5D) POIs="mu_BR_WW mu_BR_ZZ mu_BR_bb mu_BR_gamgam mu_BR_tautau" ;
       POIsF=",${BRU}";
       POIsR="mu_BR_WW=-5,5:mu_BR_gamgam=-5,5:mu_BR_ZZ=-5,5:mu_BR_tautau=-5,5:mu_BR_bb=-5,5" ;;
A1_6D) POIs="mu_BR_WW mu_BR_ZZ mu_BR_bb mu_BR_gamgam mu_BR_tautau mu_BR_mumu" ;
       POIsF=",${BRU}";
       POIsR="mu_BR_WW=-5,5:mu_BR_gamgam=-5,5:mu_BR_ZZ=-5,5:mu_BR_tautau=-5,5:mu_BR_bb=-5,5:mu_BR_mumu=-10,10" ;;
A1_5PD) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_VBF_BR_ZZ mu_XS_WH_BR_ZZ mu_XS_ZH_BR_ZZ mu_XS_ttHtH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau" ;
       POIsF=",${THEORY}";
       #POIsR="mu_XS_ggFbbH_BR_WW=-10,10:mu_XS_VBF_BR_WW=-10,10:mu_XS_WH_BR_WW=-30,30:mu_XS_ZH_BR_WW=-30,30:mu_XS_ttHtH_BR_WW=-20,20:mu_XS_ggFbbH_BR_ZZ=-10,10:mu_XS_VBF_BR_ZZ=-100,100:mu_XS_WH_BR_ZZ=0,300:mu_XS_ZH_BR_ZZ=-300,300:mu_XS_ttHtH_BR_ZZ=-100,100:mu_XS_WH_BR_bb=-30,30:mu_XS_ZH_BR_bb=-30,30:mu_XS_ttHtH_BR_bb=-20,20:mu_XS_ggFbbH_BR_gamgam=-10,10:mu_XS_VBF_BR_gamgam=-10,10:mu_XS_WH_BR_gamgam=-30,30:mu_XS_ZH_BR_gamgam=-30,30:mu_XS_ttHtH_BR_gamgam=-20,20:mu_XS_ggFbbH_BR_tautau=-10,10:mu_XS_VBF_BR_tautau=-10,10:mu_XS_WH_BR_tautau=-30,30:mu_XS_ZH_BR_tautau=-30,30:mu_XS_ttHtH_BR_tautau=-20,20" ;;
       POIsR="mu_XS_ggFbbH_BR_WW=0,10:mu_XS_VBF_BR_WW=0,10:mu_XS_WH_BR_WW=0,30:mu_XS_ZH_BR_WW=0,30:mu_XS_ttHtH_BR_WW=0,20:mu_XS_ggFbbH_BR_ZZ=0,10:mu_XS_VBF_BR_ZZ=0,100:mu_XS_WH_BR_ZZ=0,300:mu_XS_ZH_BR_ZZ=0,300:mu_XS_ttHtH_BR_ZZ=0,100:mu_XS_WH_BR_bb=0,30:mu_XS_ZH_BR_bb=0,30:mu_XS_ttHtH_BR_bb=0,20:mu_XS_ggFbbH_BR_gamgam=0,10:mu_XS_VBF_BR_gamgam=0,10:mu_XS_WH_BR_gamgam=0,30:mu_XS_ZH_BR_gamgam=0,30:mu_XS_ttHtH_BR_gamgam=0,20:mu_XS_ggFbbH_BR_tautau=0,10:mu_XS_VBF_BR_tautau=0,10:mu_XS_WH_BR_tautau=0,30:mu_XS_ZH_BR_tautau=0,30:mu_XS_ttHtH_BR_tautau=0,20" ;;
#A1_5PD_cms) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam" ; # for cov-matrix
A1_5PD_cms) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_VBF_BR_ZZ mu_XS_ZH_BR_ZZ mu_XS_WH_BR_ZZ mu_XS_ttHtH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam" ;
            POIsF=",${THEORY}";
            #POIsF=",${BRU},mu_XS_VBF_BR_ZZ,mu_XS_ZH_BR_ZZ,mu_XS_WH_BR_ZZ,mu_XS_ttHtH_BR_ZZ";  # for cov-matrix
            POIsR="mu_XS_ggFbbH_BR_WW=-10,10:mu_XS_VBF_BR_WW=-10,10:mu_XS_WH_BR_WW=-30,30:mu_XS_ZH_BR_WW=-30,30:mu_XS_ttHtH_BR_WW=-20,20:mu_XS_ggFbbH_BR_ZZ=-10,10:mu_XS_VBF_BR_ZZ=0,100:mu_XS_WH_BR_ZZ=-300,300:mu_XS_ZH_BR_ZZ=-300,300:mu_XS_ttHtH_BR_ZZ=-100,100:mu_XS_WH_BR_bb=-30,30:mu_XS_ZH_BR_bb=-30,30:mu_XS_ttHtH_BR_bb=-20,20:mu_XS_ggFbbH_BR_gamgam=-10,10:mu_XS_VBF_BR_gamgam=-10,10:mu_XS_WH_BR_gamgam=-30,30:mu_XS_ZH_BR_gamgam=-30,30:mu_XS_ttHtH_BR_gamgam=-20,20:mu_XS_ggFbbH_BR_tautau=-10,10:mu_XS_VBF_BR_tautau=-10,10:mu_XS_WH_BR_tautau=-30,30:mu_XS_ZH_BR_tautau=-30,30:mu_XS_ttHtH_BR_tautau=-20,20" ;;
            #POIsR="mu_XS_ggFbbH_BR_WW=0,10:mu_XS_VBF_BR_WW=0,10:mu_XS_WH_BR_WW=0,30:mu_XS_ZH_BR_WW=0,30:mu_XS_ttHtH_BR_WW=0,20:mu_XS_ggFbbH_BR_ZZ=0,10:mu_XS_VBF_BR_ZZ=0,100:mu_XS_WH_BR_ZZ=0,300:mu_XS_ZH_BR_ZZ=0,300:mu_XS_ttHtH_BR_ZZ=0,100:mu_XS_WH_BR_bb=0,30:mu_XS_ZH_BR_bb=0,30:mu_XS_ttHtH_BR_bb=0,20:mu_XS_ggFbbH_BR_gamgam=0,10:mu_XS_VBF_BR_gamgam=0,10:mu_XS_WH_BR_gamgam=0,30:mu_XS_ZH_BR_gamgam=0,30:mu_XS_ttHtH_BR_gamgam=0,20:mu_XS_ggFbbH_BR_tautau=0,10:mu_XS_VBF_BR_tautau=0,10:mu_XS_WH_BR_tautau=0,30:mu_XS_ZH_BR_tautau=0,30:mu_XS_ttHtH_BR_tautau=0,20" ;;
A1_5PD_atlas) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_VBF_BR_ZZ mu_XS_WH_BR_ZZ mu_XS_ZH_BR_ZZ mu_XS_ttHtH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau" ;
             POIsF=",${THEORY}";
             POIsR="mu_XS_ggFbbH_BR_WW=-10,10:mu_XS_VBF_BR_WW=-10,10:mu_XS_WH_BR_WW=-30,30:mu_XS_ZH_BR_WW=-30,30:mu_XS_ttHtH_BR_WW=-20,20:mu_XS_ggFbbH_BR_ZZ=-10,10:mu_XS_VBF_BR_ZZ=-100,100:mu_XS_WH_BR_ZZ=0,30:mu_XS_ZH_BR_ZZ=0,30:mu_XS_ttHtH_BR_ZZ=-100,100:mu_XS_WH_BR_bb=-30,30:mu_XS_ZH_BR_bb=-30,30:mu_XS_ttHtH_BR_bb=-20,20:mu_XS_ggFbbH_BR_gamgam=-10,10:mu_XS_VBF_BR_gamgam=-10,10:mu_XS_WH_BR_gamgam=-30,30:mu_XS_ZH_BR_gamgam=0,30:mu_XS_ttHtH_BR_gamgam=-20,20:mu_XS_ggFbbH_BR_tautau=-10,10:mu_XS_VBF_BR_tautau=-10,10:mu_XS_WH_BR_tautau=-30,30:mu_XS_ZH_BR_tautau=-60,60:mu_XS_ttHtH_BR_tautau=-20,20" ;;
             #POIsR="mu_XS_ggFbbH_BR_WW=0,10:mu_XS_VBF_BR_WW=0,10:mu_XS_WH_BR_WW=0,30:mu_XS_ZH_BR_WW=0,30:mu_XS_ttHtH_BR_WW=0,20:mu_XS_ggFbbH_BR_ZZ=0,10:mu_XS_VBF_BR_ZZ=0,100:mu_XS_WH_BR_ZZ=0,300:mu_XS_ZH_BR_ZZ=0,300:mu_XS_ttHtH_BR_ZZ=0,100:mu_XS_WH_BR_bb=0,30:mu_XS_ZH_BR_bb=0,30:mu_XS_ttHtH_BR_bb=0,20:mu_XS_ggFbbH_BR_gamgam=0,10:mu_XS_VBF_BR_gamgam=0,10:mu_XS_WH_BR_gamgam=0,30:mu_XS_ZH_BR_gamgam=0,30:mu_XS_ttHtH_BR_gamgam=0,20:mu_XS_ggFbbH_BR_tautau=0,10:mu_XS_VBF_BR_tautau=0,10:mu_XS_WH_BR_tautau=0,30:mu_XS_ZH_BR_tautau=0,30:mu_XS_ttHtH_BR_tautau=0,20" ;;
#A1_5PD_lhc) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_VBF_BR_ZZ mu_XS_ttHtH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau mu_XS_ZH_BR_ZZ" ; # for cov-matrix
A1_5PD_lhc) POIs="mu_XS_ggFbbH_BR_WW mu_XS_VBF_BR_WW mu_XS_WH_BR_WW mu_XS_ZH_BR_WW mu_XS_ttHtH_BR_WW mu_XS_ggFbbH_BR_ZZ mu_XS_VBF_BR_ZZ mu_XS_WH_BR_ZZ mu_XS_ZH_BR_ZZ mu_XS_ttHtH_BR_ZZ mu_XS_WH_BR_bb mu_XS_ZH_BR_bb mu_XS_ttHtH_BR_bb mu_XS_ggFbbH_BR_gamgam mu_XS_VBF_BR_gamgam mu_XS_WH_BR_gamgam mu_XS_ZH_BR_gamgam mu_XS_ttHtH_BR_gamgam mu_XS_ggFbbH_BR_tautau mu_XS_VBF_BR_tautau mu_XS_WH_BR_tautau mu_XS_ZH_BR_tautau mu_XS_ttHtH_BR_tautau" ;
            #POIsF=",${BRU},mu_XS_WH_BR_ZZ"; # for cov-matrix
            POIsF=",${THEORY}";
            POIsR="mu_XS_ggFbbH_BR_WW=-10,10:mu_XS_VBF_BR_WW=-10,10:mu_XS_WH_BR_WW=-30,30:mu_XS_ZH_BR_WW=-30,30:mu_XS_ttHtH_BR_WW=-20,20:mu_XS_ggFbbH_BR_ZZ=-10,10:mu_XS_VBF_BR_ZZ=-100,100:mu_XS_WH_BR_ZZ=0,100:mu_XS_ZH_BR_ZZ=-100,100:mu_XS_ttHtH_BR_ZZ=-100,100:mu_XS_WH_BR_bb=-30,30:mu_XS_ZH_BR_bb=-30,30:mu_XS_ttHtH_BR_bb=-20,20:mu_XS_ggFbbH_BR_gamgam=-10,10:mu_XS_VBF_BR_gamgam=-10,10:mu_XS_WH_BR_gamgam=-30,30:mu_XS_ZH_BR_gamgam=-30,30:mu_XS_ttHtH_BR_gamgam=-20,20:mu_XS_ggFbbH_BR_tautau=-10,10:mu_XS_VBF_BR_tautau=-10,10:mu_XS_WH_BR_tautau=-30,30:mu_XS_ZH_BR_tautau=-30,30:mu_XS_ttHtH_BR_tautau=-20,20" ;;
            #POIsR="mu_XS_ggFbbH_BR_WW=0,10:mu_XS_VBF_BR_WW=0,10:mu_XS_WH_BR_WW=0,30:mu_XS_ZH_BR_WW=0,30:mu_XS_ttHtH_BR_WW=0,20:mu_XS_ggFbbH_BR_ZZ=0,10:mu_XS_VBF_BR_ZZ=0,100:mu_XS_WH_BR_ZZ=0,300:mu_XS_ZH_BR_ZZ=0,300:mu_XS_ttHtH_BR_ZZ=0,100:mu_XS_WH_BR_bb=0,30:mu_XS_ZH_BR_bb=0,30:mu_XS_ttHtH_BR_bb=0,20:mu_XS_ggFbbH_BR_gamgam=0,10:mu_XS_VBF_BR_gamgam=0,10:mu_XS_WH_BR_gamgam=0,30:mu_XS_ZH_BR_gamgam=0,30:mu_XS_ttHtH_BR_gamgam=0,20:mu_XS_ggFbbH_BR_tautau=0,10:mu_XS_VBF_BR_tautau=0,10:mu_XS_WH_BR_tautau=0,30:mu_XS_ZH_BR_tautau=0,30:mu_XS_ttHtH_BR_tautau=0,20" ;;
A1_muVmuF) POIs="mu_V_gamgam mu_V_ZZ mu_V_WW mu_V_tautau mu_V_bb mu_F_gamgam mu_F_ZZ mu_F_WW mu_F_tautau mu_F_bb" ;
           POIsF=",${BRU}";
           POIsR="mu_V_ZZ=-20,20:mu_V_gamgam=-5,5:mu_V_WW=-5,5:mu_V_tautau=-5,5:mu_V_bb=-5,5:mu_F_gamgam=-5,5:mu_F_ZZ=-5,5:mu_F_WW=-5,5:mu_F_tautau=-5,5:mu_F_bb=-5,5" ;;
A2) POIs="mu_V_r_F mu_F_gamgam mu_F_ZZ mu_F_WW mu_F_tautau mu_F_bb" ;
    POIsF=",mu_V_r_F_WW,mu_V_r_F_ZZ,mu_V_r_F_gamgam,mu_V_r_F_bb,mu_V_r_F_tautau,${BRU}";
    POIsR="mu_V_r_F=-5,5:mu_F_gamgam=-5,5:mu_F_ZZ=-5,5:mu_F_WW=-5,5:mu_F_tautau=-5,5:mu_F_bb=-5,5" ;;
A2_5D) POIs="mu_F_gamgam mu_F_ZZ mu_F_WW mu_F_tautau mu_F_bb mu_V_r_F_WW mu_V_r_F_ZZ mu_V_r_F_gamgam mu_V_r_F_bb mu_V_r_F_tautau" ;
       POIsF=",mu_V_r_F,${BRU}" ;
       POIsR="mu_F_gamgam=-5,5:mu_F_ZZ=-5,5:mu_F_WW=-5,5:mu_F_tautau=-5,5:mu_F_bb=-5,5:mu_V_r_F_ZZ=-20,20" ;;
B1WW)     POIs="${B1WW_POIS}" ;
          POIsD="mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_bb_r_BR_WW" ;
          POIsR="${B1WW_RANGES}" ;
          POIsF=",${THEORY},mu_XS7_r_XS8_VBF,mu_XS7_r_XS8_WH,mu_XS7_r_XS8_ZH,mu_XS7_r_XS8_ggF,mu_XS7_r_XS8_ttH";;
B1ZZ)     POIs="${B1ZZ_POIS}" ;
          POIsD="mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_bb_r_BR_ZZ" ;
          POIsR="${B1ZZ_RANGES}" ;
          POIsF=",${THEORY},mu_XS7_r_XS8_VBF,mu_XS7_r_XS8_WH,mu_XS7_r_XS8_ZH,mu_XS7_r_XS8_ggF,mu_XS7_r_XS8_ttH";;
B1WW_TH)  POIs="${B1WW_POIS}" ;
          POIsD="mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_bb_r_BR_WW" ;
          POIsR="${B1WW_RANGES}" ;
          POIsF=",${BRU},mu_XS7_r_XS8_VBF,mu_XS7_r_XS8_WH,mu_XS7_r_XS8_ZH,mu_XS7_r_XS8_ggF,mu_XS7_r_XS8_ttH";;
B1ZZ_TH)  POIs="${B1ZZ_POIS}" ;
          POIsD="mu_XS_WH_r_XS_ggF mu_XS_ZH_r_XS_ggF mu_BR_bb_r_BR_ZZ" ;
          POIsR="${B1ZZ_RANGES}" ;
          POIsF=",${BRU},mu_XS7_r_XS8_VBF,mu_XS7_r_XS8_WH,mu_XS7_r_XS8_ZH,mu_XS7_r_XS8_ggF,mu_XS7_r_XS8_ttH";;
B1WW_P78) POIs="${B1WW_POIS} mu_XS7_r_XS8_VBF mu_XS7_r_XS8_ggF mu_XS7_r_XS8_ttH mu_XS7_r_XS8_WH mu_XS7_r_XS8_ZH" ;
          POIsR="${B1WW_RANGES}:mu_XS7_r_XS8_VBF=-5,5:mu_XS7_r_XS8_WH=-10,10:mu_XS7_r_XS8_ZH=-10,10:mu_XS7_r_XS8_ggF=-5,5:mu_XS7_r_XS8_ttH=-30,30" ;
          POIsF=",${THEORY}";;
B1ZZ_P78) POIs="${B1ZZ_POIS} mu_XS7_r_XS8_VBF mu_XS7_r_XS8_ggF mu_XS7_r_XS8_ttH mu_XS7_r_XS8_WH mu_XS7_r_XS8_ZH" ;
          POIsR="${B1ZZ_RANGES}:mu_XS7_r_XS8_VBF=-5,5:mu_XS7_r_XS8_WH=-10,10:mu_XS7_r_XS8_ZH=-10,10:mu_XS7_r_XS8_ggF=-5,5:mu_XS7_r_XS8_ttH=-30,30" ;
          POIsF=",${THEORY}";;
D1_general) POIs="mu_WW mu_ZZ mu_gamgam mu_tautau l_VBF_gamgam l_VBF_WW l_VBF_ZZ l_VBF_tautau l_WH_gamgam l_WH_WW l_WH_ZZ l_WH_tautau l_WH_bb l_ZH_gamgam l_ZH_WW l_ZH_ZZ l_ZH_tautau l_ZH_bb l_ttH_gamgam l_ttH_WW l_ttH_ZZ l_ttH_tautau l_ttH_bb";
            #POIsR="mu_WW=-5,5:mu_ZZ=-5,5:mu_bb=-5,5:mu_gamgam=-5,5:mu_tautau=-5,5,l_VBF_gamgam=-5,5:l_VBF_WW=-5,5:l_VBF_ZZ=-10,10:l_VBF_tautau=-5,5:l_VBF_bb=-20,20:l_WH_gamgam=-30,30:l_WH_WW=-10,10:l_WH_ZZ=-30,30:l_WH_tautau=-10,10:l_WH_bb=-10,10:l_ZH_gamgam=-10,10:l_ZH_WW=-20,20:l_ZH_ZZ=-50,50:l_ZH_tautau=-20,20:l_ZH_bb=-5,5:l_ttH_gamgam=-20,20:l_ttH_WW=-10,10:l_ttH_ZZ=-50,50:l_ttH_tautau=-30,30:l_ttH_bb=-10,10";
            POIsR="mu_WW=0,5:mu_ZZ=0,5:mu_gamgam=0,5:mu_tautau=0,5:l_VBF_gamgam=0,5:l_VBF_WW=0,5:l_VBF_ZZ=0,10:l_VBF_tautau=0,5:l_WH_gamgam=0,30:l_WH_WW=0,10:l_WH_ZZ=0,30:l_WH_tautau=0,10:l_WH_bb=0,10:l_ZH_gamgam=0,10:l_ZH_WW=0,20:l_ZH_ZZ=0,50:l_ZH_tautau=0,100:l_ZH_bb=0,5:l_ttH_gamgam=0,20:l_ttH_WW=0,10:l_ttH_ZZ=0,50:l_ttH_tautau=0,30:l_ttH_bb=0,10";
            POIsF=",l_VBF,l_WH,l_ZH,l_ttH,mu_bb,${BRU}";;
D1_rank1) POIs="mu_WW mu_ZZ mu_gamgam mu_tautau mu_bb l_VBF l_WH l_ZH l_ttH";
          POIsR="mu_WW=0,5:mu_ZZ=0,5:mu_gamgam=0,5:mu_tautau=0,5:mu_bb=0,5:l_VBF=0,5:l_WH=0,10:l_ZH=0,10:l_ttH=0,10";
          POIsF=",l_VBF_gamgam,l_VBF_WW,l_VBF_ZZ,l_VBF_tautau,l_WH_gamgam,l_WH_WW,l_WH_ZZ,l_WH_tautau,l_WH_bb,l_ZH_gamgam,l_ZH_WW,l_ZH_ZZ,l_ZH_tautau,l_ZH_bb,l_ttH_gamgam,l_ttH_WW,l_ttH_ZZ,l_ttH_tautau,l_ttH_bb,${BRU}";;
B2) POIs="mu_XS_ggF_x_BR_WW mu_XS_VBF_x_BR_tautau mu_XS_WH_r_XS_VBF mu_XS_ZH_r_XS_WH mu_XS_ttH_r_XS_ggF mu_BR_ZZ_r_BR_WW mu_BR_gamgam_r_BR_WW mu_BR_tautau_r_BR_WW mu_BR_bb_r_BR_tautau" ;
    POIsR="mu_XS_ggF_x_BR_WW=0,5:mu_XS_VBF_x_BR_tautau=0,5:mu_XS_WH_r_XS_VBF=-10,30:mu_XS_ZH_r_XS_WH=-20,60:mu_XS_ttH_r_XS_ggF=-10,10:mu_BR_ZZ_r_BR_WW=-5,5:mu_BR_gamgam_r_BR_WW=-5,5:mu_BR_tautau_r_BR_WW=-5,5:mu_BR_bb_r_BR_tautau=-5,5" ;
    POIsF=",${THEORY},mu_XS7_r_XS8_VBF,mu_XS7_r_XS8_WH,mu_XS7_r_XS8_ZH,mu_XS7_r_XS8_ggF,mu_XS7_r_XS8_ttH";;
K1) POIs="kappa_W kappa_Z kappa_tau kappa_t kappa_b" ;
    POIsF=",BRinv"
    POIsR="kappa_W=0,2:kappa_Z=0,2:kappa_tau=0,2:kappa_t=0,2:kappa_b=0,2:BRinv=0,0.0000000" ;;
K1_mm) POIs="kappa_W kappa_Z kappa_tau kappa_t kappa_b kappa_mu" ;
    POIsF=",BRinv"
    POIsR="kappa_W=0,2:kappa_Z=0,2:kappa_tau=0,2:kappa_t=0,2:kappa_b=0,2:kappa_mu=0,10:BRinv=0,0.0000000" ;;
# BRinv set to 0.5 in ATLAS workspaces, we have to reset it to 0  
K2) POIs="kappa_W kappa_Z kappa_tau kappa_t kappa_b kappa_g kappa_gam" ;
    POIsF=",BRinv"
    POIsR="kappa_W=0,2:kappa_Z=0,2:kappa_tau=0,2:kappa_t=0,5:kappa_b=0,2:kappa_g=0,2:kappa_gam=0,2:BRinv=0,0.0000000" ;;
K2_BSM) POIs="kappa_W kappa_Z kappa_tau kappa_t kappa_b kappa_g kappa_gam BRinv" ;
        POIsR="kappa_W=0,1:kappa_Z=0,1:kappa_tau=0,2:kappa_t=0,5:kappa_b=0,2:kappa_g=0,2:kappa_gam=0,2:BRinv=0,0.6" ;;
K2_BSM_N) POIs="kappa_W kappa_Z kappa_tau kappa_t kappa_b kappa_g kappa_gam BRinv" ;
        POIsR="kappa_W=0,1:kappa_Z=0,1:kappa_tau=0,2:kappa_t=0,5:kappa_b=0,2:kappa_g=0,2:kappa_gam=0,2:BRinv=-1,0.6" ;;
K2_2D) POIs="kappa_g kappa_gam" ;
    POIsF=",BRinv,kappa_W,kappa_Z,kappa_tau,kappa_t,kappa_b "
    POIsR="kappa_g=0,2:kappa_gam=0,2:BRinv=0,0.0000000" ;;
K3) POIs="kappa_V kappa_F" ;
    POIsR="kappa_V=0,2:kappa_F=0,2" ;;
K3_5D) POIs="kappa_V_gamgam kappa_F_gamgam kappa_V_WW kappa_F_WW kappa_V_ZZ kappa_F_ZZ kappa_V_tautau kappa_F_tautau kappa_V_bb kappa_F_bb" ;
       POIsF=",kappa_V,kappa_F" ;
       POIsR="kappa_V_gamgam=0,5:kappa_F_gamgam=0,5:kappa_V_WW=0,5:kappa_F_WW=0,5:kappa_V_ZZ=0,15:kappa_F_ZZ=0,5:kappa_V_tautau=0,5:kappa_F_tautau=0,5:kappa_V_bb=0,5:kappa_F_bb=0,5" ;;
L1) POIs="lambda_WZ lambda_Zg lambda_bZ lambda_gamZ lambda_tauZ lambda_tg kappa_gZ" ;
    POIsR="lambda_WZ=0,2:lambda_tg=0,5:lambda_bZ=0,4:lambda_tauZ=0,4:lambda_Zg=0,4:lambda_gamZ=0,2:kappa_gZ=0,3" ;;
L2_ldu) POIs="kappa_uu lambda_du lambda_Vu" ;
	      POIsR="lambda_du=0,3:lambda_Vu=0,3:kappa_uu=0,3" ;
        POIsF=",kappa_qq,lambda_lq,lambda_Vq,kappa_VV,lambda_FV" ;;
L2_llq) POIs="kappa_qq lambda_lq lambda_Vq" ;
        POIsR="lambda_lq=0,3:lambda_Vq=0,3:kappa_qq=0,3" ;
        POIsF=",kappa_uu,lambda_du,lambda_Vu,kappa_VV,lambda_FV" ;;
L2_lfv) POIs="kappa_VV lambda_FV" ;
        POIsR="lambda_FV=0,3:kappa_VV=0,3" ;
        POIsF=",kappa_uu,lambda_du,lambda_Vu,kappa_qq,lambda_lq,lambda_Vq" ;;
M1) POIs="M eps";
    POIsR="M=150,350:eps=-1,1";
    POIsF=",BRinv";;
M1_2D) POIs="M,eps";
       POIsR="M=160,340:eps=-0.2,0.2";
       POIsF=",BRinv";;
K3_2D) POIs="kappa_V,kappa_F" ;
       POIsR="kappa_V=0.7,1.4:kappa_F=0.4,1.6" ;;
K3_5D_2D) POIs="kappa_V_gamgam,kappa_F_gamgam kappa_V_WW,kappa_F_WW kappa_V_ZZ,kappa_F_ZZ kappa_V_tautau,kappa_F_tautau kappa_V_bb,kappa_F_bb" ;
    POIsF=",kappa_V,kappa_F" ;
    POIsR="kappa_V_gamgam=0.2,2.0:kappa_F_gamgam=0,3:kappa_V_WW=0.2,2.0:kappa_F_WW=0,3:kappa_V_ZZ=0.2,2.0:kappa_F_ZZ=0,3:kappa_V_tautau=0.2,2.0:kappa_F_tautau=0,3:kappa_V_bb=0.2,2.0:kappa_F_bb=0,3" ;;
K3_5D_2D_N) POIs="kappa_V_gamgam,kappa_F_gamgam kappa_V_WW,kappa_F_WW kappa_V_ZZ,kappa_F_ZZ kappa_V_tautau,kappa_F_tautau kappa_V_bb,kappa_F_bb" ;
    POIsF=",kappa_V,kappa_F" ;
    POIsR="kappa_V_gamgam=0.2,2.0:kappa_F_gamgam=-2.5,0:kappa_V_WW=0.2,2.0:kappa_F_WW=-2.5,0:kappa_V_ZZ=0.2,2.0:kappa_F_ZZ=-2.5,0:kappa_V_tautau=0.2,2.0:kappa_F_tautau=-2.5,0:kappa_V_bb=0.2,2.0:kappa_F_bb=0,2.5" ;;
# ---- FOR L1 ----
esac;
if [[ "$2" == "-r" ]]; then
    echo " --redefineSignalPOIs=${POIs// /,}";
elif [[ "$2" == "-b" ]]; then
    echo " --setPhysicsModelParameterRanges=${POIsR}";
elif [[ "$2" == "-f" ]]; then
    echo "${POIsF}";
elif [[ "$2" == "-d" ]]; then
    echo "${POIsD}";
elif [[ "$2" == "-," ]]; then
    echo "${POIs// /,}";
else
    echo $POIs; 
fi;

