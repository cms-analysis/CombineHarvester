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
        
        
        std::vector<std::string> sig_procs = {"ggH_htt","qqH_htt","WH_htt","ZH_htt","ggHsm_htt", "ggHps_htt", "ggHmm_htt","qqHsm_htt", "qqHps_htt", "qqHmm_htt","qqH_htt125","qqHsm_htt125", "qqHps_htt125", "qqHmm_htt125","WH_htt125","ZH_htt125"};
        std::vector<std::string> ggH_sig_procs = {"ggH_htt","ggHsm_htt", "ggHps_htt", "ggHmm_htt"};
        std::vector<std::string> qqH_sig_procs = {"qqH_htt""qqHsm_htt", "qqHps_htt", "qqHmm_htt", "qqH_htt125""qqHsm_htt125", "qqHps_htt125", "qqHmm_htt125","WH_htt125","ZH_htt125"};
        
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
        

        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZJ","ZL","ZLL","EWKZ","VV","VVT","VVJ","ggH_hww125","qqH_hww125"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
        
        //Add luminosity uncertainty for W in em, tt, ttbar and the mm region as norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","ttbar"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));

	if (!ttbar_fit){
          cb.cp().process({"TT","TTT","TTJ"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.025));
	}
	if(control_region==0){
          cb.cp().process({"W"}).channel({"et","mt"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));    
        }
        
        //##############################################################################
        //  trigger   
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"mt"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        cb.cp().process(embed).channel({"mt"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"et"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(embed).channel({"et"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em","ttbar"}).AddSyst(cb,
                                             "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(embed).channel({"em","ttbar"}).AddSyst(cb,
                                             "CMS_eff_embedded_trigger_em_$ERA", "lnN", SystMap<>::init(1.05)); // increasing to 5% to cover larger data/embedded difference

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).AddSyst(cb,
                                            "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.10));
        
        cb.cp().process(embed).channel({"tt"}).AddSyst(cb,
                                            "CMS_eff_embedded_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.10));


        
        
        //##############################################################################
        //  Electron, muon and tau Id  efficiencies
        //##############################################################################
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mt"}, JoinStr({sig_procs, all_mc_bkgs_no_W}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, all_mc_bkgs}),  1.02));
        cb.cp().AddSyst(cb, "CMS_eff_embedded_m", "lnN", SystMap<channel, process>::init
                        ({"mt"}, embed,  1.02)
                        ({"em","ttbar"}, embed,  1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_m_embedsel", "lnN", SystMap<channel, process>::init
                        ({"et","tt","em","mt"}, embed,  1.04)); 
        
        cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({sig_procs, all_mc_bkgs_no_W}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, all_mc_bkgs}),       1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_embedded_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, embed,  1.02)
                        ({"em","ttbar"}, embed,       1.02));
        

        // Tau Efficiency applied to all MC
        // in tautau channel the applied value depends on the number of taus which is determined by
        // gen match. WJets for example is assumed to have 1 real tau and 1 fake as is TTJ
        // compared to ZTT which has 2 real taus.
        // We also have channel specific components and fully correlated components
        //
        // ETau & MuTau
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.045));
        cb.cp().process(embed).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.045));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        cb.cp().process(embed).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

        // TauTau - 2 real taus
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.09));
        cb.cp().process(embed).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$ERA", "lnN", SystMap<>::init(1.09));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VVT","TTT","EWKZ"}})).channel({"tt"}).AddSyst(cb,
                                            "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));
        cb.cp().process(embed).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_embedded_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));

        // TauTau - 1+ jet to tau fakes
        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.06));
        
        cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        
        //##############################################################################
        //  b tag and mistag rate  efficiencies (update me)
        //##############################################################################
        
        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em","et","mt"}, {1,31,32,33,34,35,36,37}, {"TTJ","TTT","TT"}, 1.035));
        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em","et","mt"}, {2,3,4,41,42,43,44,45,46,47}, {"TTJ","TTT","TT"}, 1.05));

        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em","et","mt"}, {2,3,4,41,42,43,44,45,46,47}, {"VV","VVT","VVJ"}, 1.015)); // Mainly SingleTop
        // need to update numbers for mt and et channles just set these the same as em channel for nowt
        
        //##############################################################################
        //  Electron, muon and tau energy Scale
        //##############################################################################
        
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"em"}).AddSyst(cb,
        //                                     "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(embed).channel({"em","et"}).AddSyst(cb,
                                             "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(embed).channel({"em","mt"}).AddSyst(cb,
                                             "CMS_scale_m_$ERA", "shape", SystMap<>::init(1.00));
        
        // Decay Mode based TES Settings
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, real_tau_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(embed).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(embed).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(embed).channel({"et","mt","tt"}).AddSyst(cb,
                                                "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        //  Embedded uncertainty on ttbar contamination
        //##############################################################################        
        cb.cp().process({"EmbedZTT"}).AddSyst(cb,"CMS_ttbar_embeded_$ERA", "shape", SystMap<>::init(1.00));
 

        //##############################################################################
        //  jet and met energy Scale
        //##############################################################################
 
        // MET Systematic shapes - recoil uncertainties for recoil corrected met, unclustered energy uncertainty for samples with no recoil correction, jes uncertainties propogated to met for samples with no recoil correction
        cb.cp().process({"TT","TTJ","TTT","VV","VVJ","VVT"}).AddSyst(cb,
                                                  "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));
        
        // recoil uncertainties need to be split by njets. W effectivly has njets+1 (due to tau/electron from fake jet)
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({1,10,11,12,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_0Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_0Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({1,10,11,12,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_0Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_0Jet_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({2,13,14,15,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et","mt","em"}).bin_id({1,10,11,12,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({2,11,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({2,13,14,15,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et","mt","em"}).bin_id({1,10,11,12,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({2,11,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({2,13,14,15,3,4,16,17,18,20,41,42,43,44,45,46,47}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({2,11,3,4,12,13,41,42,43,44,45,46,47}).AddSyst(cb,
                                                  "CMS_htt_boson_reso_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"et","mt","em"}).bin_id({2,13,14,15,3,4,16,17,18,20,41,42,43,44,45,46,47}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"tt"}).bin_id({2,11,3,4,12,13,41,42,43,44,45,46,47}).AddSyst(cb,
                                                  "CMS_htt_boson_scale_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));


        if(ttbar_fit){        
          cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"ttbar"}).AddSyst(cb,
                                                    "CMS_htt_boson_reso_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
          cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"ttbar"}).AddSyst(cb,
                                                    "CMS_htt_boson_scale_met_1Jet_$ERA", "shape", SystMap<>::init(1.00));
          cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"ttbar"}).AddSyst(cb,
                                                    "CMS_htt_boson_reso_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));
          cb.cp().process(JoinStr({sig_procs, {"W","ZTT","ZLL","ZL","ZJ","EWKZ"}})).channel({"ttbar"}).AddSyst(cb,
                                                    "CMS_htt_boson_scale_met_2Jet_$ERA", "shape", SystMap<>::init(1.00));
        }
 

        // JES factorization test tautau  
        std::vector< std::string > uncertNames;
        if (!no_jec_split) {      
            uncertNames = {
              "AbsoluteFlavMap",
              "AbsoluteMPFBias",
              "AbsoluteScale",
              "AbsoluteStat",
              "FlavorQCD",
              "Fragmentation",
              "PileUpDataMC",
              "PileUpPtBB",
              "PileUpPtEC1",
              "PileUpPtEC2",
              "PileUpPtHF",
              "PileUpPtRef",
              "RelativeBal",
              "RelativeFSR",
              "RelativeJEREC1",
              "RelativeJEREC2",
              "RelativeJERHF",
              "RelativePtBB",
              "RelativePtEC1",
              "RelativePtEC2",
              "RelativePtHF",
              "RelativeStatEC",
              "RelativeStatFSR",
              "RelativeStatHF",
              "SinglePionECAL",
              "SinglePionHCAL",
              "TimePtEta"
            }; // end uncertNames
        } else { uncertNames = { "Total" }; }
        
        //for (string uncert:uncertNames){
        //    
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).bin_id({10,11,14}).AddSyst(cb,
        //                                                                                        "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_TTJ})).channel({"et"}).bin_id({13}).AddSyst(cb,
        //                                                                                        "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).bin_id({10,11,13,14}).AddSyst(cb,
        //                                                                                        "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).bin_id({10,11,12}).AddSyst(cb,
        //                                                                                         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","mt","et"}).bin_id({1,2,3,4,5,6}).AddSyst(cb,
        //                                   "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).bin_id({1,2,3,4,5,6}).channel({"em"}).AddSyst(cb,
        //                                   "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //}
        
        
        // uncomment for regional JES uncertainties
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to5_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta0to3_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_eta3to5_$ERA", "shape", SystMap<>::init(1.00)); 
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));

        
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
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));}

        // W norm, just for em, tt and the mm region where MC norm is from MC
        
        cb.cp().process({"W"}).channel({"em"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeLep_13TeV", "lnN", SystMap<>::init(1.20));
        
        cb.cp().process({"W"}).channel({"tt","em"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));
        
        if(control_region==0){
          cb.cp().process({"W"}).channel({"et","mt"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));    
        }
        
        // QCD uncerts for em 

        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_em_QCD_0JetRate_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2,3,4,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "CMS_em_QCD_1JetRate_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_em_QCD_0JetShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2,3,4,41,42,43,44,45,47}).AddSyst(cb,
                                             "CMS_em_QCD_1JetShape_$ERA", "shape", SystMap<>::init(1.00));
        //cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
        //                                     "CMS_em_QCD_IsoExtrap_$ERA", "shape", SystMap<>::init(1.00));
        if(ttbar_fit) {
          cb.cp().process({"QCD"}).channel({"ttbar"}).bin_id({2,3,4}).AddSyst(cb,
                                               "CMS_em_QCD_1JetRate_$ERA", "shape", SystMap<>::init(1.00));
          cb.cp().process({"QCD"}).channel({"ttbar"}).bin_id({2,3,4}).AddSyst(cb,
                                               "CMS_em_QCD_1JetShape_$ERA", "shape", SystMap<>::init(1.00));
          cb.cp().process({"QCD"}).channel({"ttbar"}).AddSyst(cb,
                                               "CMS_em_QCD_IsoExtrap_$ERA", "shape", SystMap<>::init(1.00));
        }
        
        // QCD norm, just for tt 
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({1,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({2,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({3,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "CMS_htt_QCD_dijet_lowboost_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.08));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({4,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "CMS_htt_QCD_dijet_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.48));
        
        
        // QCD OS/SS uncertainty should include also extrapolation from non-iso -> iso (update me)
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "QCD_OSSS_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.21));											 
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "QCD_OSSS_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.33));										 
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "QCD_OSSS_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.48));

	cb.cp().process({"QCD"}).channel({"mt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
	                                     "QCD_OSSS_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.09));											 
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
	                                     "QCD_OSSS_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.07));										 
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
	                                     "QCD_OSSS_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.08));       
        
        // based on the Ersatz study
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({1,11,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WHighMTtoLowMT_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.033));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({2,14,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WHighMTtoLowMT_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.067));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({3,4,17,20,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WHighMTtoLowMT_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.182));
        
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({4,20,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WlowPTtoHighPT_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.279));
        
        // W OS/SS systematic uncertainties 
        cb.cp().process({"W"}).channel({"et"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.002));
        cb.cp().process({"W"}).channel({"et"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.029));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WOSSS_syst_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.131));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_syst_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.012));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({2,13,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WOSSS_syst_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.049));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WOSSS_syst_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.086));
        
        // W OS/SS statistical uncertainties
        cb.cp().process({"W"}).channel({"et"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.035));
        cb.cp().process({"W"}).channel({"et"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.026));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WOSSS_stat_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.082));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({1,10,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.026));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({2,13,31,32,33,34,35,36,37}).AddSyst(cb,
                                             "WOSSS_stat_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.020));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3,4,16,41,42,43,44,45,46,47}).AddSyst(cb,
                                             "WOSSS_stat_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.066));

        //##############################################################################
        //  Fake-Factor Method Uncertainties
        //##############################################################################

        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_qcd_dm0_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_qcd_dm0_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_qcd_dm1_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_qcd_dm1_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_w_dm0_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_w_dm0_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_w_dm1_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_w_dm1_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_tt_dm0_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_tt_dm1_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_qcd_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_w_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "ff_tt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "ff_w_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "ff_tt_$CHANNEL_syst", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb,"ff_dy_frac_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb,"ff_w_frac_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb,"ff_tt_frac_$CHANNEL_syst", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).bin_id({1}).AddSyst(cb, "ff_sub_syst_$CHANNEL_0jet", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).bin_id({2}).AddSyst(cb, "ff_sub_syst_$CHANNEL_boosted", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).bin_id({3}).AddSyst(cb, "ff_sub_syst_$CHANNEL_dijet_lowboost", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).bin_id({4}).AddSyst(cb, "ff_sub_syst_$CHANNEL_dijet_boosted", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        //  DY LO->NLO reweighting, Between no and twice the correction.
        //##############################################################################
        
        cb.cp().process( {"ZTT","ZJ","ZL","ZLL"}).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZTT","ZL","ZLL"}).channel({"em"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Ttbar shape reweighting, Between no and twice the correction
        //##############################################################################
        
        cb.cp().process( {"TTJ","TTT"}).channel({"tt"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"TTJ","TTT"}).channel({"et","mt"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"TT"}).channel({"em"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        // ZL shape  and electron/muon  to tau fake only in  mt and et channels (updated March 22)
        //##############################################################################

        
        cb.cp().process( {"ZL"}).channel({"mt","et"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"mt","et"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
       
        // weighted avarages of recommended tau POG uncertainties provided in bins of eta
        cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.07));
        cb.cp().process({"ZL"}).channel({"et"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.10));

        
        //##############################################################################
        // jet  to tau fake only in tt, mt and et channels
        //##############################################################################
        
        
        cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20)); 
        cb.cp().process({"VVJ","TTJ","ZJ"}).channel({"et","mt","tt"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        if(control_region==0){
          cb.cp().process({"W"}).channel({"et","mt"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20));    
        }
        
        cb.cp().process( {"W"}).channel({"tt","mt","et"}).AddSyst(cb,
                                                                "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Theoretical Uncertainties on signal (update me)
        //##############################################################################
        // don't use acceptance uncertainties on VBF as there isn't an easy way to get these for the JHU samples (and they are expected to be small for this process)
        // For now just use the ggH uncertainties computed for the POWHEG samples - update this for MG5
        // Removed PDF acceptance uncertainties for ggH as these are verysmall compared to PDF uncertainty on XS and scale uncertainty on acceptance/shape
        // Check ST uncertainties for ggH
        // Update parton-shower (PS) uncertainty for MG5 ggH
        
        //scale_gg on signal
        cb.cp().process(ggH_sig_procs).channel({"et","mt","tt","em"}).AddSyst(cb,
                                             "CMS_scale_gg_$ERA", "shape", SystMap<>::init(1.00));
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_UEPS", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.015)
                        ({"et"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.015)
                        ({"mt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.015)
                        ({"tt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.015)
                        
                        ({"em"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.945)
                        ({"et"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.945)
                        ({"mt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.945)
                        ({"tt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.945)
                        
                        ({"em"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.03)
                        ({"et"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.03)
                        ({"mt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.03)
                        ({"tt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.03)
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
        cb.cp().process({"WH_htt"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.007));
        cb.cp().process({"ZH_htt"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.038));
        
        cb.cp().process(JoinStr({ggH_sig_procs, {"ggH_hww125"}})).AddSyst(cb,"pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
        cb.cp().process(JoinStr({qqH_sig_procs, {"qqH_hww125"}})).AddSyst(cb,"pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
        cb.cp().process({"WH_htt"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.019));
        cb.cp().process({"ZH_htt"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.016));
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_STXSmig01", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"et"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"mt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        ({"tt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 0.959)
                        
                        ({"em"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.079)
                        ({"et"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.079)
                        ({"mt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.079)
                        ({"tt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.079)
                        
                        ({"em"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.039)
                        ({"et"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.039)
                        ({"mt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.039)
                        ({"tt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.039)
                        );
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_STXSmig12", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"et"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"mt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"tt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        
                        ({"em"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.932)
                        ({"et"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.932)
                        ({"mt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.932)
                        ({"tt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 0.932)
                        
                        ({"em"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.161)
                        ({"et"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.161)
                        ({"mt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.161)
                        ({"tt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.161)
                        );
        
        cb.cp().AddSyst(cb, "CMS_ggH_STXSVBF2j", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"et"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"mt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"tt"},{1,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        
                        ({"em"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"et"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"mt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        ({"tt"},{2,31,32,33,34,35,36,37},ggH_sig_procs, 1.000)
                        
                        ({"em"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.200)
                        ({"et"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.200)
                        ({"mt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.200)
                        ({"tt"},{3,4,41,42,43,44,45,46,47},ggH_sig_procs, 1.200)
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
            cb.SetFlag("filters-use-regex", true);
            
            cb.cp().bin({"mt_0jet"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_0jet"}).process({"TTJ","TTT","TTJ_rest"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_0jet"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0)); 
            
            cb.cp().bin({"mt_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_boosted"}).process({"TTJ","TTT","TTJ_rest"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_boosted"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_dijet_lowboost"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_lowboost"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_dijet_lowboost"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_dijet_lowboost"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_dijet_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_dijet_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_dijet_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_dijet_boosted"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"em_ttbar"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.GetParameter("rate_ttbar")->set_range(0.80, 1.20);
            
            cb.SetFlag("filters-use-regex", false);
        }
        
    }
}
