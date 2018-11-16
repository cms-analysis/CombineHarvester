#include "CombineHarvester/HTTSMCP2016/interface/HttSystematics_SMRun2.h"
#include <vector>
#include <string>
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"

using namespace std;

namespace ch {
    
    using ch::syst::SystMap;
    using ch::syst::SystMapAsymm;
    using ch::syst::era;
    using ch::syst::channel;
    using ch::syst::bin_id;
    using ch::syst::process;
    using ch::syst::bin;
    using ch::JoinStr;
    
    void __attribute__((optimize("O0"))) AddSMRun2Systematics(CombineHarvester & cb, int control_region, bool ttbar_fit, bool no_jec_split) {
        // Create a CombineHarvester clone that only contains the signal
        // categories
        //
        // cb_sig is unused at the moment, (was it ever used in this analysis?) delete?
        //CombineHarvester cb_sig = cb.cp();
        //
        //
        
        
        std::vector<std::string> sig_procs = {"ggH_htt","qqH_htt","WH_htt","ZH_htt","ggHsm_htt", "ggHps_htt", "ggHmm_htt","qqHsm_htt", "qqHps_htt", "qqHmm_htt","qqH_htt125","qqHsm_htt125", "qqHps_htt125", "qqHmm_htt125","WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125", "WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt", "ggHsm_jhu_htt","ggHps_jhu_htt","ggHmm_jhu_htt"};
        std::vector<std::string> ggH_sig_procs = {"ggH_htt","ggHsm_htt", "ggHps_htt", "ggHmm_htt","ggHsm_jhu_htt","ggHps_jhu_htt","ggHmm_jhu_htt"};
        std::vector<std::string> qqH_sig_procs = {"qqH_htt","qqHsm_htt", "qqHps_htt", "qqHmm_htt", "qqH_htt125","qqHsm_htt125", "qqHps_htt125", "qqHmm_htt125"};
        
        // N.B. when adding this list of backgrounds to a nuisance, only
        // the backgrounds that are included in the background process
        // defined in MorphingSM2016.cpp are included in the actual DCs
        // This is a list of all MC based backgrounds
        // QCD is explicitly excluded
        std::vector<std::string> all_mc_bkgs = {
            "ZL","ZLL","ZJ","ZTT","TTJ","TTT","TT",
            "W","VV","VVT","VVJ",
            "ggH_hww125","qqH_hww125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_no_W = {
            "ZL","ZLL","ZJ","ZTT","TTJ","TTT","TT",
            "VV","VVT","VVJ",
            "ggH_hww125","qqH_hww125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_no_TTJ = {
            "ZL","ZLL","ZJ","ZTT","TTT","TT",
            "VV","VVT","VVJ",
            "ggH_hww125","qqH_hww125","EWKZ"};
        std::vector<std::string> embed = {"EmbedZTT"};
        std::vector<std::string> real_tau_mc_bkgs = {"ZTT","TTT","TT","VV","VVT","EWKZ"};
            
        //##############################################################################
        //  lumi
        //##############################################################################
        
        // lumi uncertainty is 2.5% for 2016 and 2.3% for 2017 - uncorrelated accross years

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","tt_2016","et","et_2016","mt","mt_2016","em","em_2016","ttbar","ttbar_2016"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt_2017","mt_2017","et_2017","em_2017","ttbar_2017"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.023));

        //##############################################################################
        //  trigger   
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_trigger_mt_13TeV", "lnN", SystMap<>::init(1.02));
        cb.cp().process(embed).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_mt_13TeV", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","et_2016","et_2017"}).AddSyst(cb,
                                             "CMS_eff_trigger_et_13TeV", "lnN", SystMap<>::init(1.02)); 
        cb.cp().process(embed).channel({"et","et_2016","et_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_et_13TeV", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}).AddSyst(cb,
                                             "CMS_eff_trigger_em_13TeV", "lnN", SystMap<>::init(1.02)); 
        cb.cp().process(embed).channel({"em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_em_13TeV", "lnN", SystMap<>::init(1.04)); // increasing to 4% to cover larger data/embedded differences in this channel which are likly due to the trigger modelling

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb,
                                            "CMS_eff_trigger_tt_13TeV", "lnN", SystMap<>::init(1.10)); 
        cb.cp().process(embed).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb,
                                            "CMS_eff_embedded_trigger_tt_13TeV", "lnN", SystMap<>::init(1.10));
        
        //##############################################################################
        //  Electron, muon and tau Id  efficiencies
        //##############################################################################
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mt","mt_2016","mt_2017","em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}, JoinStr({sig_procs, all_mc_bkgs}),  1.02));
        cb.cp().AddSyst(cb, "CMS_eff_embedded_m", "lnN", SystMap<channel, process>::init
                        ({"mt","mt_2016","mt_2017""em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}, embed,  1.02));
        
        // embedded selection efficiency
        cb.cp().AddSyst(cb, "CMS_eff_m_embedsel", "lnN", SystMap<channel, process>::init
                        ({"em","em_2016","em_2017","et","et_2016","et_2017","tt","tt_2016","tt_2017","mt","mt_2016","mt_2017","ttbar","ttbar_2016","ttbar_2017"}, embed,  1.04)); 
        
        cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et","et_2016","et_2017","em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}, JoinStr({sig_procs, all_mc_bkgs}),       1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_embedded_e", "lnN", SystMap<channel, process>::init
                        ({"et","et_2016","et_2017","em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}, embed,       1.02));
        

        // Tau Efficiency applied to all MC
        // in tautau channel the applied value depends on the number of taus which is determined by
        // gen match. WJets for example is assumed to have 1 real tau and 1 fake as is TTJ
        // compared to ZTT which has 2 real taus.
        // We also have channel specific components and fully correlated components
        //
        // for embedding there is a 2% uncertainty due to tracking that should be correlated between 2016/2017 and all channels and a 3% uncertainty for the tau ID which is split into a part correlated and a part uncorrelated accross channels
        // The tracking uncertainty is increased from 2% to 4% as it is derived from MC so does not sover the uncertainty on the data/MC tracking differences
        // ETau & MuTau
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","et_2016","mt","mt_2016"}).AddSyst(cb,
                                             "CMS_eff_t_13TeV", "lnN", SystMap<>::init(1.045));
        cb.cp().process(embed).channel({"et","et_2016","mt","mt_2016"}).AddSyst(cb,
                                             "CMS_track_eff_embedded_t_13TeV", "lnN", SystMap<>::init(1.04)); 
        cb.cp().process(embed).channel({"et","et_2016","mt","mt_2016"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_13TeV", "lnN", SystMap<>::init(1.027));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","mt_2016"}).AddSyst(cb,
                                             "CMS_eff_t_mt_13TeV", "lnN", SystMap<>::init(1.02));
        cb.cp().process(embed).channel({"mt","mt_2016"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_mt_13TeV", "lnN", SystMap<>::init(1.012));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","et_2016"}).AddSyst(cb,
                                             "CMS_eff_t_et_13TeV", "lnN", SystMap<>::init(1.02));
        cb.cp().process(embed).channel({"et","et_2016"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_et_13TeV", "lnN", SystMap<>::init(1.012));

        // TauTau - 2 real taus
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_eff_t_13TeV", "lnN", SystMap<>::init(1.09));
        cb.cp().process(embed).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_track_eff_embedded_t_13TeV", "lnN", SystMap<>::init(1.08));
        cb.cp().process(embed).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_13TeV", "lnN", SystMap<>::init(1.055));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt","tt_2016"}).AddSyst(cb,
                                            "CMS_eff_t_tt_13TeV", "lnN", SystMap<>::init(1.04));
        cb.cp().process(embed).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_tt_13TeV", "lnN", SystMap<>::init(1.024));

        // TauTau - 1+ jet to tau fakes
        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_eff_t_13TeV", "lnN", SystMap<>::init(1.06));
        
        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt","tt_2016"}).AddSyst(cb,
                                             "CMS_eff_t_tt_13TeV", "lnN", SystMap<>::init(1.02));

        
        // 2017 tau efficiency uncertainties

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et_2017","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.027));

        cb.cp().process(embed).channel({"et_2017","mt_2017"}).AddSyst(cb,
                                             "CMS_track_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.04));
        cb.cp().process(embed).channel({"et_2017","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.018));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et_2017","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.012));
        cb.cp().process(embed).channel({"et_2017","mt_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.01));

        // TauTau - 2 real taus
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.055));
        cb.cp().process(embed).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_track_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.08));
        cb.cp().process(embed).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.036));

        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt_2017"}).AddSyst(cb,
                                            "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.024));
        cb.cp().process(embed).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

        // TauTau - 1+ jet to tau fakes
        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.018));

        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt_2017"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.012));

        
        //##############################################################################
        //  b tag and mistag rate  efficiencies 
        //##############################################################################
 
        // update number for 2017 
        // real uncerts for TT and VV only (others are small) 
        cb.cp().AddSyst(cb,
          "CMS_eff_b_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"et","et_2016","et_2017"}, {1}, {"TTT"}, 1.020,0.969)
          ({"et","et_2016","et_2017"}, {2}, {"TTT"}, 1.034,0.968)
          ({"et","et_2016","et_2017"}, {3}, {"TTT"}, 1.025,0.932)
          ({"et","et_2016","et_2017"}, {4}, {"TTT"}, 1.008,0.969)
          ({"et","et_2016","et_2017"}, {5}, {"TTT"}, 1.032,0.963)
          ({"et","et_2016","et_2017"}, {6}, {"TTT"}, 1.015,0.942)
          ({"et","et_2016","et_2017"}, {2}, {"VVT"}, 1.010,0.989)
          ({"et","et_2016","et_2017"}, {3}, {"VVT"}, 1.024,0.987)
          ({"et","et_2016","et_2017"}, {4}, {"VVT"}, 1.000,0.983)
          ({"mt","mt_2016","mt_2017"}, {1}, {"TTT"}, 1.024,0.975)
          ({"mt","mt_2016","mt_2017"}, {2}, {"TTT"}, 1.030,0.967)
          ({"mt","mt_2016","mt_2017"}, {3}, {"TTT"}, 1.069,0.967)
          ({"mt","mt_2016","mt_2017"}, {4}, {"TTT"}, 1.040,0.964)
          ({"mt","mt_2016","mt_2017"}, {5}, {"TTT"}, 1.028,0.968)
          ({"mt","mt_2016","mt_2017"}, {6}, {"TTT"}, 1.060,0.952)
          ({"mt","mt_2016","mt_2017"}, {2}, {"VVT"}, 1.010,0.994)
          ({"mt","mt_2016","mt_2017"}, {3}, {"VVT"}, 1.015,1.000)
          ({"mt","mt_2016","mt_2017"}, {4}, {"VVT"}, 1.014,0.987)
          ({"mt","mt_2016","mt_2017"}, {5}, {"VVT"}, 1.005,1.000)
          ({"mt","mt_2016","mt_2017"}, {6}, {"VVT"}, 1.024,0.986)
          ({"em","em_2016","em_2017"}, {1}, {"TT"}, 1.016,0.982)
          ({"em","em_2016","em_2017"}, {2}, {"TT"}, 1.030,0.968)
          ({"em","em_2016","em_2017"}, {3}, {"TT"}, 1.033,0.968)
          ({"em","em_2016","em_2017"}, {4}, {"TT"}, 1.032,0.957)
          ({"em","em_2016","em_2017"}, {5}, {"TT"}, 1.032,0.975)
          ({"em","em_2016","em_2017"}, {6}, {"TT"}, 1.032,0.969)
          ({"em","em_2016","em_2017"}, {2}, {"VV"}, 1.008,0.992)
          ({"em","em_2016","em_2017"}, {3}, {"VV"}, 1.013,0.986)
          ({"em","em_2016","em_2017"}, {4}, {"VV"}, 1.008,0.988)
          ({"em","em_2016","em_2017"}, {5}, {"VV"}, 1.010,0.992)
          ({"em","em_2016","em_2017"}, {6}, {"VV"}, 1.011,0.988)
        );

        cb.cp().process({"TTT","TT","VVT","VV"}).bin_id({31,32,33,34,35,36,37,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "CMS_eff_b_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process({"TTT","TT","VVT","VV"}).channel({"em","em_2016","em_2017","mt","mt_2016","mt_2017","et","et_2016","et_2017"}).bin_id({100,101,102,103,104,105,106,107,108}).AddSyst(cb,
        //                                     "CMS_eff_b_13TeV", "shape", SystMap<>::init(1.00));
 
        //##############################################################################
        //  Electron, muon and tau energy Scale
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, embed})).channel({"et","et_2016","et_2017","em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}).AddSyst(cb,
                                             "CMS_scale_e_13TeV", "shape", SystMap<>::init(1.00));
        
        // Decay Mode based TES Settings
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs, embed})).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017"}).AddSyst(cb,
                                                "CMS_scale_t_1prong_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs, embed})).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017"}).AddSyst(cb,
                                                "CMS_scale_t_1prong1pizero_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs, embed})).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017"}).AddSyst(cb,
                                                "CMS_scale_t_3prong_13TeV", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        //  Embedded uncertainty on ttbar contamination (and VV contamination)
        //##############################################################################        
        cb.cp().process(embed).AddSyst(cb,"CMS_ttbar_embeded_13TeV", "shape", SystMap<>::init(1.00));
 
        //##############################################################################
        //  jet and met energy Scale
        //##############################################################################
 
        // MET Systematic shapes - recoil uncertainties for recoil corrected met, unclustered energy uncertainty for samples with no recoil correction, jes uncertainties propogated to met for samples with no recoil correction
        cb.cp().process({"TT","TTJ","TTT","VV","VVJ","VVT"}).AddSyst(cb,
                                                  "CMS_scale_met_unclustered_13TeV", "shape", SystMap<>::init(1.00));


       // recoil uncertainties only for 2016 so far, add these back for 2017 when they are available - ask DESY about correlations
       // cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ","W"}})).AddSyst(cb,
       //                                           "CMS_htt_boson_reso_met_13TeV", "shape", SystMap<>::init(1.00)); 
       // cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ","W"}})).AddSyst(cb,
       //                                           "CMS_htt_boson_scale_met_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ","W"}})).channel({"tt","tt_2016","et","et_2016","mt","mt_2016","em","em_2016","ttbar","ttbar_2016"}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_13TeV", "shape", SystMap<>::init(1.00)); 
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ","W"}})).channel({"tt","tt_2016","et","et_2016","mt","mt_2016","em","em_2016","ttbar","ttbar_2016"}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_13TeV", "shape", SystMap<>::init(1.00));      
 

      

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_corr_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_uncorr_13TeV", "shape", SystMap<>::init(1.00));
 
        // uncomment for regional JES uncertainties
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to5_corr_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to3_corr_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta3to5_corr_13TeV", "shape", SystMap<>::init(1.00)); 
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to5_uncorr_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to3_uncorr_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta3to5_uncorr_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_RelativeBal_13TeV", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em_2017","et_2017","mt_2017","tt_2017","ttbar_2017"}).AddSyst(cb,"CMS_scale_j_RelativeSample_$ERA", "shape", SystMap<>::init(1.00));

        
        //##############################################################################
        //  Background normalization uncertainties
        //##############################################################################
        
        //   Diboson  Normalisation - fully correlated
        cb.cp().process({"VV","VVT","VVJ"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));

        cb.cp().process({"ZTT","ZJ","ZL","ZLL"}).AddSyst(cb,
                                        "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));        
 
        cb.cp().process({"EWKZ"}).AddSyst(cb,
                                        "CMS_htt_ewkzXsec_13TeV", "lnN", SystMap<>::init(1.04));

        if (! ttbar_fit){
        //   ttbar Normalisation - fully correlated
	    cb.cp().process({"TT","TTT","TTJ"}).AddSyst(cb,
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));
        }

        // W norm, just for em, tt and the mm region where MC norm is from MC
        
        cb.cp().process({"W"}).channel({"em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeLep_13TeV", "lnN", SystMap<>::init(1.20));
        
        cb.cp().process({"W"}).channel({"tt","tt_2016","tt_2017","em","em_2016","em_2017","ttbar","ttbar_2016","ttbar_2017"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));
        
        if(control_region==0){
          cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));    
        }
        
        // QCD uncerts for em
        
        cb.cp().AddSyst(cb,
                  "CMS_em_QCD_0JetRate_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"em","em_2016","em_2017"}, {1}, {"QCD"}, 0.904, 1.096)
        ); 
        cb.cp().process({"QCD"}).channel({"em","em_2016","em_2017"}).bin_id({31,32,33,34,35,36,37,100,101,102,103,104,105,106,107,108}).AddSyst(cb,
                                             "CMS_em_QCD_0JetRate_13TeV", "shape", SystMap<>::init(1.00));
    
        // neglect these as they are small 
        //cb.cp().AddSyst(cb,
        //  "CMS_em_QCD_1JetRate_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
        //  ({"em","em_2016","em_2017"}, {4}, {"QCD"}, 0.995, 1.005)
        //  ({"em","em_2016","em_2017"}, {3}, {"QCD"}, 0.995, 1.005)
        //  ({"em","em_2016","em_2017"}, {6}, {"QCD"}, 0.993, 1.007)
        //  ({"em","em_2016","em_2017"}, {5}, {"QCD"}, 0.995, 1.005)
        //  ({"em","em_2016","em_2017"}, {2}, {"QCD"}, 0.995, 1.005)
        //  ({"ttbar","ttbar_2016","ttbar_2017"}, {1}, {"QCD"}, 0.997, 1.003)

        //); // neglect small uncertainties

        cb.cp().process({"QCD"}).channel({"em","em_2016","em_2017"}).bin_id({31,32,33,34,35,36,37,41,42,43,44,45,46,47,48,49,100,101,102,103,104,105,106,107,108}).AddSyst(cb,
                                             "CMS_em_QCD_1JetRate_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em","em_2016","em_2017"}).bin_id({1,31,32,33,34,35,36,37,100,101,102,103,104,105,106,107,108}).AddSyst(cb,
                                             "CMS_em_QCD_0JetShape_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb,
          "CMS_em_QCD_1JetShape_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"ttbar","ttbar_2016","ttbar_2017"}, {1}, {"QCD"}, 0.955, 1.045)
          ({"em","em_2016","em_2017"}, {4}, {"QCD"}, 0.966, 1.034)
          ({"em","em_2016","em_2017"}, {3}, {"QCD"}, 0.955, 1.045)
          ({"em","em_2016","em_2017"}, {6}, {"QCD"}, 0.874, 1.121)
          ({"em","em_2016","em_2017"}, {5}, {"QCD"}, 0.940, 1.060)
        );

        cb.cp().process({"QCD"}).channel({"em","em_2016","em_2017"}).bin_id({2,31,32,33,34,35,36,37,41,42,43,44,45,47,48,49,100,101,102,103,104,105,106,107,108}).AddSyst(cb,
                                             "CMS_em_QCD_1JetShape_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb,
          "CMS_em_QCD_IsoExtrap_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"ttbar","ttbar_2016","ttbar_2017"}, {1}, {"QCD"}, 0.967, 1.039)
          ({"em","em_2016","em_2017"}, {1}, {"QCD"}, 1.050, 0.956)
          ({"em","em_2016","em_2017"}, {4}, {"QCD"}, 1.034, 0.965)
          ({"em","em_2016","em_2017"}, {3}, {"QCD"}, 1.042, 0.962)
          ({"em","em_2016","em_2017"}, {6}, {"QCD"}, 0.703, 1.260)
          ({"em","em_2016","em_2017"}, {5}, {"QCD"}, 1.040, 0.965)
          ({"em","em_2016","em_2017"}, {2}, {"QCD"}, 1.047, 0.960)

        );

        cb.cp().process({"QCD"}).channel({"em","em_2016","em_2017"}).bin_id({31,32,33,34,35,36,37,41,42,43,44,45,47,48,49,100,101,102,103,104,105,106,107,108}).AddSyst(cb,
                                             "CMS_em_QCD_IsoExtrap_13TeV", "shape", SystMap<>::init(1.00));

        
        // QCD norm, just for tt 
        cb.cp().process({"QCD"}).channel({"tt","tt_2016","tt_2017"}).bin_id({1,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.02));
        cb.cp().process({"QCD"}).channel({"tt","tt_2016","tt_2017"}).bin_id({2,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.04));
        cb.cp().process({"QCD"}).channel({"tt","tt_2016","tt_2017"}).bin_id({3,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "CMS_htt_QCD_dijet_lowboost_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.08));
        cb.cp().process({"QCD"}).channel({"tt","tt_2016","tt_2017"}).bin_id({4,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "CMS_htt_QCD_dijet_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.48));
        
        
        // QCD OS/SS uncertainty should include also extrapolation from non-iso -> iso (update me)
        cb.cp().process({"QCD"}).channel({"et","et_2016","et_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "QCD_OSSS_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.21));											 
        cb.cp().process({"QCD"}).channel({"et","et_2016","et_2017"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "QCD_OSSS_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.33));										 
        cb.cp().process({"QCD"}).channel({"et","et_2016","et_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "QCD_OSSS_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.48));

	cb.cp().process({"QCD"}).channel({"mt","mt_2016","mt_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
	                                     "QCD_OSSS_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.09));											 
        cb.cp().process({"QCD"}).channel({"mt","mt_2016","mt_2017"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
	                                     "QCD_OSSS_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.07));										 
        cb.cp().process({"QCD"}).channel({"mt","mt_2016","mt_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
	                                     "QCD_OSSS_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.08));       
        
        // based on the Ersatz study
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).bin_id({1,11,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WHighMTtoLowMT_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.033));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).bin_id({2,14,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WHighMTtoLowMT_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.067));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).bin_id({3,4,17,20,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WHighMTtoLowMT_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.182));
        
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).bin_id({4,20,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WlowPTtoHighPT_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.279));
        
        // W OS/SS systematic uncertainties 
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.002));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.029));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WOSSS_syst_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.131));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.012));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({2,13,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WOSSS_syst_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.049));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WOSSS_syst_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.086));
        
        // W OS/SS statistical uncertainties
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.035));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.026));
        cb.cp().process({"W"}).channel({"et","et_2016","et_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WOSSS_stat_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.082));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.026));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.020));
        cb.cp().process({"W"}).channel({"mt","mt_2016","mt_2017"}).bin_id({3,4,16,41,42,43,44,45,46,47,48,49}).AddSyst(cb,
                                             "WOSSS_stat_dijet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.066));

        //##############################################################################
        //  Fake-Factor Method Uncertainties
        //##############################################################################

        // FF ststistical uncertainties are uncorrelated between 2016 and 2017

        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_qcd_dm0_njet0_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_qcd_dm0_njet1_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_qcd_dm1_njet0_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_qcd_dm1_njet1_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_w_dm0_njet0_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_w_dm0_njet1_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_w_dm1_njet0_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_w_dm1_njet1_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_tt_dm0_njet0_et_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_tt_dm1_njet0_et_stat", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_qcd_dm0_njet0_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_qcd_dm0_njet1_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_qcd_dm1_njet0_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_qcd_dm1_njet1_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_w_dm0_njet0_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_w_dm0_njet1_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_w_dm1_njet0_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_w_dm1_njet1_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_tt_dm0_njet0_mt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_tt_dm1_njet0_mt_stat", "shape", SystMap<>::init(1.00));

        // tt statistical uncertainties

        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_qcd_dm0_njet0_tt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_qcd_dm0_njet1_tt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_qcd_dm1_njet0_tt_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_qcd_dm1_njet1_tt_stat", "shape", SystMap<>::init(1.00));

        // FF systematic uncertainties 

        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017","et","et_2016","et_2017"}).AddSyst(cb, "ff_w_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017","et","et_2016","et_2017"}).AddSyst(cb, "ff_tt_syst", "shape", SystMap<>::init(1.00));
        //cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017","et","et_2016"}).AddSyst(cb, "ff_tt_syst", "shape", SystMap<>::init(1.00)); // add back for et 2017

        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_w_tt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_tt_tt_syst", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_qcd_et_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_qcd_mt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_qcd_tt_syst", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016"}).AddSyst(cb,"ff_dy_frac_tt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb,"ff_w_frac_tt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb,"ff_tt_frac_tt_syst", "shape", SystMap<>::init(1.00));

        // et subtraction uncertainties

        cb.cp().process({"jetFakes"}).channel({"et","et_2016","et_2017"}).AddSyst(cb, "ff_sub_syst_et", "shape", SystMap<>::init(1.00));

        // mt subtraction uncertainties

        cb.cp().process({"jetFakes"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb, "ff_sub_syst_mt", "shape", SystMap<>::init(1.00));

        // tt subtraction uncertainties

        cb.cp().process({"jetFakes"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb, "ff_sub_syst_tt", "shape", SystMap<>::init(1.00));

        //##############################################################################
        //  DY LO->NLO reweighting, Between no and twice the correction.
        //##############################################################################
        
        cb.cp().process( {"ZTT","ZJ","ZL","ZLL"}).AddSyst(cb,
                                             "CMS_htt_dyShape_13TeV", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Ttbar shape reweighting, Between no and twice the correction
        //##############################################################################
        
        cb.cp().process( {"TTJ","TTT","TT"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_13TeV", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        // ZL shape  and electron/muon  to tau fake only in  mt and et channels (updated March 22)
        //##############################################################################

        
        cb.cp().process( {"ZL"}).channel({"et","et_2016","et_2017"}).AddSyst(cb,
                                                         "CMS_ZLShape_et_1prong_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"et","et_2016","et_2017"}).AddSyst(cb,
                                                         "CMS_ZLShape_et_1prong1pizero_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().process( {"ZL"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb,
                                                         "CMS_ZLShape_mt_1prong_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"mt","mt_2016","mt_2017"}).AddSyst(cb,
                                                         "CMS_ZLShape_mt_1prong1pizero_13TeV", "shape", SystMap<>::init(1.00));
       
        // weighted avarages of recommended tau POG uncertainties provided in bins of eta
        cb.cp().process({"ZL","EWKZ"}).channel({"mt","mt_2016"}).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.07));
        cb.cp().process({"ZL","EWKZ"}).channel({"mt_2017"}).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.12));
        cb.cp().process({"ZL","EWKZ"}).channel({"et","et_2016"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"ZL","EWKZ"}).channel({"tt","tt_2016"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.21));
        cb.cp().process({"ZL","EWKZ"}).channel({"et_2017"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.16));
        cb.cp().process({"ZL","EWKZ"}).channel({"tt_2017"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.35));
        
        //##############################################################################
        // jet  to tau fake only in tt, mt and et channels
        //##############################################################################
        
        
        cb.cp().process({"W"}).channel({"tt","tt_2016","tt_2017"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20)); 
        cb.cp().process({"VVJ","TTJ","ZJ"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        if(control_region==0){
          cb.cp().process({"W"}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20));    
        }
        
        cb.cp().process( {"W"}).channel({"tt","tt_2016","tt_2017","mt","mt_2016","mt_2017","et","et_2016","et_2017"}).AddSyst(cb,
                                                                "CMS_htt_jetToTauFake_13TeV", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Theoretical Uncertainties on signal (update me)
        //##############################################################################
        // don't use acceptance uncertainties on VBF as there isn't an easy way to get these for the JHU samples (and they are expected to be small for this process)
        // Removed PDF acceptance uncertainties for ggH as these are verysmall compared to PDF uncertainty on XS and scale uncertainty on acceptance/shape
        
        //scale_gg on signal
        cb.cp().process(ggH_sig_procs).bin_id({2,3,4,5,6,31,32,33,34,35,36,37,41,42,43,44,45,46,47,48,49}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017","em","em_2016","em_2017"}).AddSyst(cb,
                                             "CMS_scale_gg_13TeV", "shape", SystMap<>::init(1.00));
       
        cb.cp().AddSyst(cb,
          "CMS_scale_gg_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHps_htt125"}, 0.937, 1.063)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHsm_htt125"}, 0.928, 1.069)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHmm_htt125"}, 0.942, 1.059)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHps_htt125"}, 0.948, 1.054)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHsm_htt125"}, 0.939, 1.061)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHmm_htt125"}, 0.946, 1.056)
          ({"et","et_2016","et_2017"}, {1}, {"ggHps_htt125"}, 0.946, 1.056)
          ({"et","et_2016","et_2017"}, {1}, {"ggHsm_htt125"}, 0.966, 1.042)
          ({"et","et_2016","et_2017"}, {1}, {"ggHmm_htt125"}, 0.929, 1.069)
          ({"em","em_2016","em_2017"}, {1}, {"ggHps_htt125"}, 0.947, 1.056)
          ({"em","em_2016","em_2017"}, {1}, {"ggHsm_htt125"}, 0.942, 1.058)
          ({"em","em_2016","em_2017"}, {1}, {"ggHmm_htt125"}, 0.950, 1.053)
        ); 
       
        cb.cp().process(ggH_sig_procs).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017","em","em_2016","em_2017"}).AddSyst(cb,
                                             "CMS_FiniteQuarkMass_13TeV", "shape", SystMap<>::init(1.00)); // this uncertainty takes the difference between the finite top-mass dependence and the EFT

        // PS uncertainty affects njets and pT distribution so is included as a shape uncertainty for the boosted category where pT is fitted
        cb.cp().process(ggH_sig_procs).bin_id({2,31,32,33,34,35,36,37,41,42,43,44,45,46,47,48,49}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017","em","em_2016","em_2017"}).AddSyst(cb,
                                             "CMS_PS_ggH_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb,
          "CMS_PS_ggH_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHps_htt125"}, 0.981, 1.016)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHsm_htt125"}, 0.984, 1.012)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHmm_htt125"}, 0.977, 1.019)
          //({"tt","tt_2016","tt_2017"}, {2}, {"ggHps_htt125"}, 0.984, 1.016)
          //({"tt","tt_2016","tt_2017"}, {2}, {"ggHsm_htt125"}, 0.982, 1.016)
          //({"tt","tt_2016","tt_2017"}, {2}, {"ggHmm_htt125"}, 0.983, 1.016)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHps_htt125"}, 1.002, 1.003)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHsm_htt125"}, 0.993, 1.010)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHmm_htt125"}, 0.997, 1.007)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHps_htt125"}, 1.018, 0.991)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHsm_htt125"}, 1.016, 0.992)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHmm_htt125"}, 1.017, 0.992)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHps_htt125"}, 0.993, 1.010)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHsm_htt125"}, 0.999, 1.004)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHmm_htt125"}, 0.997, 1.006)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHps_htt125"}, 1.018, 0.991)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHsm_htt125"}, 1.020, 0.990)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHmm_htt125"}, 1.019, 0.991)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHps_htt125"}, 0.990, 1.007)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHsm_htt125"}, 0.993, 1.005)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHmm_htt125"}, 0.989, 1.008)
          //({"mt","mt_2016","mt_2017"}, {2}, {"ggHps_htt125"}, 0.986, 1.014)
          //({"mt","mt_2016","mt_2017"}, {2}, {"ggHsm_htt125"}, 0.988, 1.012)
          //({"mt","mt_2016","mt_2017"}, {2}, {"ggHmm_htt125"}, 0.987, 1.013)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHps_htt125"}, 0.986, 1.014)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHsm_htt125"}, 0.983, 1.017)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHmm_htt125"}, 0.983, 1.017)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHps_htt125"}, 1.011, 0.996)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHsm_htt125"}, 1.012, 0.995)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHmm_htt125"}, 1.012, 0.995)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHps_htt125"}, 0.984, 1.017)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHsm_htt125"}, 0.988, 1.012)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHmm_htt125"}, 0.980, 1.020)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHps_htt125"}, 1.013, 0.994)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHsm_htt125"}, 1.011, 0.996)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHmm_htt125"}, 1.011, 0.996)
          ({"et","et_2016","et_2017"}, {1}, {"ggHps_htt125"}, 0.985, 1.012)
          ({"et","et_2016","et_2017"}, {1}, {"ggHsm_htt125"}, 0.985, 1.012)
          ({"et","et_2016","et_2017"}, {1}, {"ggHmm_htt125"}, 0.984, 1.013)
          //({"et","et_2016","et_2017"}, {2}, {"ggHps_htt125"}, 0.983, 1.016)
          //({"et","et_2016","et_2017"}, {2}, {"ggHsm_htt125"}, 0.982, 1.017)
          //({"et","et_2016","et_2017"}, {2}, {"ggHmm_htt125"}, 0.980, 1.018)
          ({"et","et_2016","et_2017"}, {3}, {"ggHps_htt125"}, 0.989, 1.011)
          ({"et","et_2016","et_2017"}, {3}, {"ggHsm_htt125"}, 0.993, 1.009)
          ({"et","et_2016","et_2017"}, {3}, {"ggHmm_htt125"}, 0.990, 1.011)
          ({"et","et_2016","et_2017"}, {4}, {"ggHps_htt125"}, 1.016, 0.993)
          ({"et","et_2016","et_2017"}, {4}, {"ggHsm_htt125"}, 1.015, 0.993)
          ({"et","et_2016","et_2017"}, {4}, {"ggHmm_htt125"}, 1.010, 0.996)
          ({"et","et_2016","et_2017"}, {5}, {"ggHps_htt125"}, 0.986, 1.014)
          ({"et","et_2016","et_2017"}, {5}, {"ggHsm_htt125"}, 0.984, 1.015)
          ({"et","et_2016","et_2017"}, {5}, {"ggHmm_htt125"}, 0.984, 1.018)
          ({"et","et_2016","et_2017"}, {6}, {"ggHps_htt125"}, 1.016, 0.993)
          ({"et","et_2016","et_2017"}, {6}, {"ggHsm_htt125"}, 1.012, 0.995)
          ({"et","et_2016","et_2017"}, {6}, {"ggHmm_htt125"}, 1.015, 0.993)
          ({"em","em_2016","em_2017"}, {1}, {"ggHps_htt125"}, 1.006, 0.993)
          ({"em","em_2016","em_2017"}, {1}, {"ggHsm_htt125"}, 1.005, 0.993)
          ({"em","em_2016","em_2017"}, {1}, {"ggHmm_htt125"}, 1.003, 0.996)
          //({"em","em_2016","em_2017"}, {2}, {"ggHps_htt125"}, 0.995, 1.007)
          //({"em","em_2016","em_2017"}, {2}, {"ggHsm_htt125"}, 1.000, 1.003)
          //({"em","em_2016","em_2017"}, {2}, {"ggHmm_htt125"}, 0.996, 1.006)
          ({"em","em_2016","em_2017"}, {3}, {"ggHps_htt125"}, 0.984, 1.015)
          ({"em","em_2016","em_2017"}, {3}, {"ggHsm_htt125"}, 0.982, 1.017)
          ({"em","em_2016","em_2017"}, {3}, {"ggHmm_htt125"}, 0.984, 1.015)
          ({"em","em_2016","em_2017"}, {4}, {"ggHps_htt125"}, 1.004, 1.001)
          ({"em","em_2016","em_2017"}, {4}, {"ggHsm_htt125"}, 1.008, 0.999)
          ({"em","em_2016","em_2017"}, {4}, {"ggHmm_htt125"}, 1.006, 1.000)
          ({"em","em_2016","em_2017"}, {5}, {"ggHps_htt125"}, 0.992, 1.009)
          ({"em","em_2016","em_2017"}, {5}, {"ggHsm_htt125"}, 0.995, 1.012)
          ({"em","em_2016","em_2017"}, {5}, {"ggHmm_htt125"}, 0.985, 1.015)
          ({"em","em_2016","em_2017"}, {6}, {"ggHps_htt125"}, 1.008, 0.998)
          ({"em","em_2016","em_2017"}, {6}, {"ggHsm_htt125"}, 1.008, 0.998)
          ({"em","em_2016","em_2017"}, {6}, {"ggHmm_htt125"}, 1.007, 0.999)
        );

        cb.cp().process(ggH_sig_procs).bin_id({31,32,33,34,35,36,37,41,42,43,44,45,46,47,48,49}).channel({"et","et_2016","et_2017","mt","mt_2016","mt_2017","tt","tt_2016","tt_2017","em","em_2016","em_2017"}).AddSyst(cb,
                                             "CMS_UE_ggH_13TeV", "shape", SystMap<>::init(1.00));

        // UE uncertainty affects njets distributions so included as lnN for cut based approach.
        cb.cp().AddSyst(cb,
          "CMS_UE_ggH_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHps_htt125"}, 0.997, 1.009)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHsm_htt125"}, 0.997, 1.010)
          ({"tt","tt_2016","tt_2017"}, {1}, {"ggHmm_htt125"}, 0.997, 1.010)
          ({"tt","tt_2016","tt_2017"}, {2}, {"ggHps_htt125"}, 0.993, 1.026)
          ({"tt","tt_2016","tt_2017"}, {2}, {"ggHsm_htt125"}, 0.993, 1.025)
          ({"tt","tt_2016","tt_2017"}, {2}, {"ggHmm_htt125"}, 0.993, 1.025)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHps_htt125"}, 0.992, 1.036)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHsm_htt125"}, 0.992, 1.033)
          ({"tt","tt_2016","tt_2017"}, {3}, {"ggHmm_htt125"}, 0.992, 1.034)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHps_htt125"}, 0.990, 1.037)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHsm_htt125"}, 0.990, 1.037)
          ({"tt","tt_2016","tt_2017"}, {4}, {"ggHmm_htt125"}, 0.990, 1.037)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHps_htt125"}, 0.992, 1.034)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHsm_htt125"}, 0.992, 1.032)
          ({"tt","tt_2016","tt_2017"}, {5}, {"ggHmm_htt125"}, 0.991, 1.034)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHps_htt125"}, 0.989, 1.037)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHsm_htt125"}, 0.989, 1.038)
          ({"tt","tt_2016","tt_2017"}, {6}, {"ggHmm_htt125"}, 0.989, 1.037)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHps_htt125"}, 1.000, 0.999)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHsm_htt125"}, 1.000, 0.998)
          ({"mt","mt_2016","mt_2017"}, {1}, {"ggHmm_htt125"}, 1.000, 0.998)
          ({"mt","mt_2016","mt_2017"}, {2}, {"ggHps_htt125"}, 0.995, 1.017)
          ({"mt","mt_2016","mt_2017"}, {2}, {"ggHsm_htt125"}, 0.995, 1.017)
          ({"mt","mt_2016","mt_2017"}, {2}, {"ggHmm_htt125"}, 0.995, 1.017)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHps_htt125"}, 0.993, 1.028)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHsm_htt125"}, 0.993, 1.027)
          ({"mt","mt_2016","mt_2017"}, {3}, {"ggHmm_htt125"}, 0.993, 1.028)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHps_htt125"}, 0.990, 1.035)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHsm_htt125"}, 0.990, 1.036)
          ({"mt","mt_2016","mt_2017"}, {4}, {"ggHmm_htt125"}, 0.991, 1.036)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHps_htt125"}, 0.994, 1.026)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHsm_htt125"}, 0.993, 1.024)
          ({"mt","mt_2016","mt_2017"}, {5}, {"ggHmm_htt125"}, 0.993, 1.026)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHps_htt125"}, 0.990, 1.036)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHsm_htt125"}, 0.990, 1.035)
          ({"mt","mt_2016","mt_2017"}, {6}, {"ggHmm_htt125"}, 0.990, 1.035)
          ({"et","et_2016","et_2017"}, {1}, {"ggHps_htt125"}, 0.998, 1.005)
          ({"et","et_2016","et_2017"}, {1}, {"ggHsm_htt125"}, 0.998, 1.006)
          ({"et","et_2016","et_2017"}, {1}, {"ggHmm_htt125"}, 0.998, 1.005)
          ({"et","et_2016","et_2017"}, {2}, {"ggHps_htt125"}, 0.994, 1.020)
          ({"et","et_2016","et_2017"}, {2}, {"ggHsm_htt125"}, 0.994, 1.020)
          ({"et","et_2016","et_2017"}, {2}, {"ggHmm_htt125"}, 0.994, 1.021)
          ({"et","et_2016","et_2017"}, {3}, {"ggHps_htt125"}, 0.993, 1.030)
          ({"et","et_2016","et_2017"}, {3}, {"ggHsm_htt125"}, 0.992, 1.032)
          ({"et","et_2016","et_2017"}, {3}, {"ggHmm_htt125"}, 0.993, 1.030)
          ({"et","et_2016","et_2017"}, {4}, {"ggHps_htt125"}, 0.990, 1.037)
          ({"et","et_2016","et_2017"}, {4}, {"ggHsm_htt125"}, 0.990, 1.036)
          ({"et","et_2016","et_2017"}, {4}, {"ggHmm_htt125"}, 0.990, 1.035)
          ({"et","et_2016","et_2017"}, {5}, {"ggHps_htt125"}, 0.993, 1.029)
          ({"et","et_2016","et_2017"}, {5}, {"ggHsm_htt125"}, 0.992, 1.032)
          ({"et","et_2016","et_2017"}, {5}, {"ggHmm_htt125"}, 0.992, 1.029)
          ({"et","et_2016","et_2017"}, {6}, {"ggHps_htt125"}, 0.990, 1.036)
          ({"et","et_2016","et_2017"}, {6}, {"ggHsm_htt125"}, 0.990, 1.036)
          ({"et","et_2016","et_2017"}, {6}, {"ggHmm_htt125"}, 0.990, 1.036)
          ({"em","em_2016","em_2017"}, {1}, {"ggHps_htt125"}, 1.003, 0.989)
          ({"em","em_2016","em_2017"}, {1}, {"ggHsm_htt125"}, 1.003, 0.989)
          ({"em","em_2016","em_2017"}, {1}, {"ggHmm_htt125"}, 1.003, 0.989)
          ({"em","em_2016","em_2017"}, {2}, {"ggHps_htt125"}, 0.996, 1.013)
          ({"em","em_2016","em_2017"}, {2}, {"ggHsm_htt125"}, 0.996, 1.012)
          ({"em","em_2016","em_2017"}, {2}, {"ggHmm_htt125"}, 0.996, 1.013)
          ({"em","em_2016","em_2017"}, {3}, {"ggHps_htt125"}, 0.994, 1.025)
          ({"em","em_2016","em_2017"}, {3}, {"ggHsm_htt125"}, 0.994, 1.024)
          ({"em","em_2016","em_2017"}, {3}, {"ggHmm_htt125"}, 0.993, 1.024)
          ({"em","em_2016","em_2017"}, {4}, {"ggHps_htt125"}, 0.991, 1.032)
          ({"em","em_2016","em_2017"}, {4}, {"ggHsm_htt125"}, 0.991, 1.033)
          ({"em","em_2016","em_2017"}, {4}, {"ggHmm_htt125"}, 0.991, 1.033)
          ({"em","em_2016","em_2017"}, {5}, {"ggHps_htt125"}, 0.993, 1.025)
          ({"em","em_2016","em_2017"}, {5}, {"ggHsm_htt125"}, 0.993, 1.025)
          ({"em","em_2016","em_2017"}, {5}, {"ggHmm_htt125"}, 0.994, 1.022)
          ({"em","em_2016","em_2017"}, {6}, {"ggHps_htt125"}, 0.991, 1.033)
          ({"em","em_2016","em_2017"}, {6}, {"ggHsm_htt125"}, 0.991, 1.034)
          ({"em","em_2016","em_2017"}, {6}, {"ggHmm_htt125"}, 0.991, 1.033)
        );
        
        //    Uncertainty on BR for HTT @ 125 GeV
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_THU", "lnN", SystMap<>::init(1.017));
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
        
        //    Uncertainty on BR of HWW @ 125 GeV
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_THU", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_PU_mq", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_PU_alphas", "lnN", SystMap<>::init(1.0066));
        
        
        cb.cp().process(JoinStr({ggH_sig_procs, {"ggH_hww125"}})).AddSyst(cb,"QCDScale_ggH", "lnN", SystMap<>::init(1.039));
        cb.cp().process(JoinStr({qqH_sig_procs, {"qqH_hww125"}})).AddSyst(cb,"QCDScale_qqH", "lnN", SystMap<>::init(1.004));
        cb.cp().process({"WH_htt","WHsm_htt125","WHps_htt125","WHmm_htt125","WHsm_htt","WHps_htt","WHmm_htt"}).AddSyst(cb,"QCDScale_WH", "lnN", SystMap<>::init(1.007));
        cb.cp().process({"ZH_htt","ZHsm_htt125","ZHps_htt125","ZHmm_htt125","ZHsm_htt","ZHps_htt","ZHmm_htt"}).AddSyst(cb,"QCDScale_ZH", "lnN", SystMap<>::init(1.038));
        
        cb.cp().process(JoinStr({ggH_sig_procs, {"ggH_hww125"}})).AddSyst(cb,"pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
        cb.cp().process(JoinStr({qqH_sig_procs, {"qqH_hww125"}})).AddSyst(cb,"pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
        cb.cp().process({"WH_htt","WHsm_htt125","WHps_htt125","WHmm_htt125","WHsm_htt","WHps_htt","WHmm_htt"}).AddSyst(cb,"pdf_Higgs_WH", "lnN", SystMap<>::init(1.019));
        cb.cp().process({"ZH_htt""ZHsm_htt125","ZHps_htt125","ZHmm_htt125","ZHsm_htt","ZHps_htt","ZHmm_htt"}).AddSyst(cb,"pdf_Higgs_ZH", "lnN", SystMap<>::init(1.016));
        
        // jet bin migration uncertainties from: https://arxiv.org/pdf/1610.07922.pdf#subsection.1.4.2.5 (Table 20)
        // For boosted category this is not exclusivly 1 jet events since events with > 1 jets and mjj<300 enter also. So take weighted average of Njets=1 and Njets>=1 uncertainties i.e sigma(boosted) = sigma(njets=1)*(# Njets=1 && boosted)/(# boosted) + sigma(njets>=1)*(#Njets>1 && boosted)/(# boosted)
        // These need to be set properly for MVA approach (placeholders for now)
        
        cb.cp().AddSyst(cb, "CMS_ggH_mig01", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em","em_2016","em_2017"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"et","et_2016","et_2017"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"mt","mt_2016","mt_2017"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"tt","tt_2016","tt_2017"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        
                        ({"em","em_2016","em_2017"},{2},ggH_sig_procs, 1.071)
                        ({"et","et_2016","et_2017"},{2},ggH_sig_procs, 1.071)
                        ({"mt","mt_2016","mt_2017"},{2},ggH_sig_procs, 1.071)
                        ({"tt","tt_2016","tt_2017"},{2},ggH_sig_procs, 1.071)
                        
                        ({"em","em_2016","em_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.036)
                        ({"et","et_2016","et_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.036)
                        ({"mt","mt_2016","mt_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.036)
                        ({"tt","tt_2016","tt_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.036)
                        );
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_mig12", "lnN", SystMap<channel, bin_id, process>::init 
                        ({"em","em_2016","em_2017"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.986)
                        ({"et","et_2016","et_2017"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.986)
                        ({"mt","mt_2016","mt_2017"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.986)
                        ({"tt","tt_2016","tt_2017"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.986)
                        
                        ({"em","em_2016","em_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.145)
                        ({"et","et_2016","et_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.145)
                        ({"mt","mt_2016","mt_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.145)
                        ({"tt","tt_2016","tt_2017"},{3,4,5,6,41,42,43,44,45,46,47,48,49},ggH_sig_procs, 1.145)
                        );
        

        if (control_region > 0) {
            // Create rateParams for control regions:
            //  - [x] 1 rateParam for all W in every region
            //  - [x] 1 rateParam for QCD in low mT
            //  - [x] 1 rateParam for QCD in high mT
            //  - [x] lnNs for the QCD OS/SS ratio
            //         * should account for stat + syst
            //         * systs should account for: extrap. from anti-iso to iso region,
            //  - [x] lnNs for the W+jets OS/SS ratio
            //         * should account for stat only if not being accounted for with bbb,
            //           i.e. because the OS/SS ratio was measured with a relaxed selection
            //         * systs should account for: changes in low/high mT and OS/SS due to experimental effects e.g JES,
            //           OS/SS being wrong in the MC 
            //           low/high mT being wrong in the MC 
            
            // W rate params added for all et/mt signal-regions/control-regions. The same W rate param is used for dijet_lowboost and dijet_boosted since the W for the dijet_boosted category is estimated using dijet_lowboost control-region and extraplated to dijet_boosted using MC
            cb.cp().bin({"mt_0jet","mt_0jet_wjets_cr","mt_0jet_qcd_cr","mt_0jet_wjets_ss_cr"}).process({"W"}).AddSyst(cb, "rate_W_mt_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"mt_boosted","mt_boosted_wjets_cr","mt_boosted_qcd_cr","mt_boosted_wjets_ss_cr"}).process({"W"}).AddSyst(cb, "rate_W_mt_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_dijet_lowboost","mt_dijet_lowboost_wjets_cr","mt_dijet_lowboost_qcd_cr","mt_dijet_lowboost_wjets_ss_cr","mt_dijet_boosted","mt_dijet_boosted_qcd_cr"}).process({"W"}).AddSyst(cb, "rate_W_mt_dijet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet","et_0jet_wjets_cr","et_0jet_qcd_cr","et_0jet_wjets_ss_cr"}).process({"W"}).AddSyst(cb, "rate_W_et_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"et_boosted","et_boosted_wjets_cr","et_boosted_qcd_cr","et_boosted_wjets_ss_cr"}).process({"W"}).AddSyst(cb, "rate_W_et_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_lowboost","et_dijet_lowboost_wjets_cr","et_dijet_lowboost_qcd_cr","et_dijet_lowboost_wjets_ss_cr","et_dijet_boosted","et_dijet_boosted_qcd_cr"}).process({"W"}).AddSyst(cb, "rate_W_et_dijet", "rateParam", SystMap<>::init(1.0));
            
            // QCD rate params added for low-mT region   
            cb.cp().bin({"mt_0jet","mt_0jet_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_mt_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"mt_boosted","mt_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_mt_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_dijet_lowboost","mt_dijet_lowboost_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_mt_dijet_lowboost", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_dijet_boosted","mt_dijet_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_mt_dijet_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet","et_0jet_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_et_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"et_boosted","et_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_et_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_lowboost","et_dijet_lowboost_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_et_dijet_lowboost", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_boosted","et_dijet_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_lowmT_et_dijet_boosted", "rateParam", SystMap<>::init(1.0));
            
            // QCD rate params added for high-mT regions    
            cb.cp().bin({"mt_0jet_wjets_cr","mt_0jet_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_mt_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"mt_boosted_wjets_cr","mt_boosted_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_mt_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_dijet_lowboost_wjets_cr","mt_dijet_lowboost_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_mt_dijet_lowboost", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet_wjets_cr","et_0jet_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_et_0jet", "rateParam", SystMap<>::init(1.0)); 
            cb.cp().bin({"et_boosted_wjets_cr","et_boosted_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_et_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_lowboost_wjets_cr","et_dijet_lowboost_wjets_ss_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_highmT_et_dijet_lowboost", "rateParam", SystMap<>::init(1.0));

            // tt QCD rate params
            cb.cp().bin({"tt_0jet","tt_0jet_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_tt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_boosted","tt_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_tt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_dijet_lowboost","tt_dijet_lowboost_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_dijet_lowboost_tt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_dijet_boosted","tt_dijet_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_dijet_boosted_tt", "rateParam", SystMap<>::init(1.0));  

            // Should set a sensible range for our rateParams
            for (auto sys : cb.cp().syst_type({"rateParam"}).syst_name_set()) {
                cb.GetParameter(sys)->set_range(0.0, 5.0);
            }
        }

        
        if (ttbar_fit) {
            //cb.cp().channel({"ttbar","em","et","mt","tt","ttbar_2016","em_2016","et_2016","mt_2016","tt_2016"}).process({"TT","TTT","TTJ"}).AddSyst(cb, "rate_ttbar_2016", "rateParam", SystMap<>::init(1.0));
            //cb.cp().channel({"ttbar_2017","em_2017","et_2017","mt_2017","tt_2017"}).process({"TT","TTT","TTJ"}).AddSyst(cb, "rate_ttbar_2017", "rateParam", SystMap<>::init(1.0));
            
            //cb.GetParameter("rate_ttbar_2016")->set_range(0.80, 1.20);
            //cb.GetParameter("rate_ttbar_2017")->set_range(0.80, 1.20);
        }
        
    }
}
