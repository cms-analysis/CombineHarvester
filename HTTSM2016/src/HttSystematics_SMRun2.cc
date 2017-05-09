#include "CombineHarvester/HTTSM2016/interface/HttSystematics_SMRun2.h"
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
    
    void AddSMRun2Systematics(CombineHarvester & cb, int control_region, bool mm_fit, bool ttbar_fit) {
        // Create a CombineHarvester clone that only contains the signal
        // categories
        //
        // cb_sig is unused at the moment, (was it ever used in this analysis?) delete?
        //CombineHarvester cb_sig = cb.cp();
        //
        //
        //if (control_region == 1){
        //    // we only want to cosider systematic uncertainties in the signal region.
        //    // limit to only the 0jet/1jet and vbf categories
        //    cb_sig.bin_id({1,2,3});
        //}
        
        
        std::vector<std::string> sig_procs = {"ggH","qqH","WH","ZH"};
        
        // N.B. when adding this list of backgrounds to a nuisance, only
        // the backgrounds that are included in the background process
        // defined in MorphingSM2016.cpp are included in the actual DCs
        // This is a list of all MC based backgrounds
        // QCD is explicitly excluded
        std::vector<std::string> all_mc_bkgs = {
            "ZL","ZJ","ZTT","TTJ","TTT","TT",
            "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
            "HWW_gg125","HWW_qq125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_no_W = {
            "ZL","ZJ","ZTT","TTJ","TTT","TT",
            "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
            "HWW_gg125","HWW_qq125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_no_TTJ = {
            "ZL","ZJ","ZTT","TTT","TT",
            "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
            "HWW_gg125","HWW_qq125","EWKZ"};

        //##############################################################################
        //  lumi
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, {"VV","VVT","VVJ","HWW_gg125","HWW_qq125"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
        cb.cp().process({"W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"}).channel({"tt"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.025));
        
        //Add luminosity uncertainty for W in em, tt, ttbar and the mm region as norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","mm","ttbar"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));

	if (!ttbar_fit){
          cb.cp().process({"TTT","TTJ"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.025));
	}
        
        //##############################################################################
        //  trigger   ##FIXME   the values have been chosen rather arbitrarily
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"mt"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"et"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em","ttbar"}).AddSyst(cb,
                                             // hard coding channel here keeps "em" and "ttbar" correlated
                                             "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));

        // New
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).AddSyst(cb,
                                            "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.10));


        
        
        //##############################################################################
        //  Electron, muon and tau Id  efficiencies
        //##############################################################################
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mm"}, {"ZTT", "TT", "VV", "ZL", "ZJ"},  1.02)
                        ({"mt"}, JoinStr({sig_procs, all_mc_bkgs_no_W}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, all_mc_bkgs}),  1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({sig_procs, all_mc_bkgs_no_W}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, all_mc_bkgs}),       1.02));
        

        // Tau Efficiency applied to all MC
        // in tautau channel the applied value depends on the number of taus which is determined by
        // gen match. WJets for example is assumed to have 1 real tau and 1 fake as is TTJ
        // compared to ZTT which has 2 real taus.
        // We also have channel specific components and fully correlated components
        //
        // ETau & MuTau
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.045));
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

        // TauTau - 2 real taus
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VV","VVT","TTT","EWKZ"}})).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.09));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VV","VVT","TTT","EWKZ"}})).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));

        // TauTau - 1+ jet to tau fakes
        cb.cp().process({"TTJ","ZJ","VVJ","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.06));
        
        cb.cp().process({"TTJ","ZJ","VVJ","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        
        
        
        //######################## Tau Id shape uncertainty (added March 08)
        
        cb.cp().process({"ZTT"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                                            "CMS_tauDMReco_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                                                          "CMS_tauDMReco_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                                                          "CMS_tauDMReco_3prong_$ERA", "shape", SystMap<>::init(1.00));
        
        
        
        //##############################################################################
        //  b tag and mistag rate  efficiencies
        //##############################################################################
        
        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"}, {1}, {"TTJ","TTT","TT"}, 1.035));
        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"}, {2,3}, {"TTJ","TTT","TT"}, 1.05));

        cb.cp().AddSyst(cb, "CMS_htt_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"}, {2, 3}, {"VV","VVT","VVJ"}, 1.015)); // Mainly SingleTop
        
        
        //##############################################################################
        //  Electron and tau energy Scale
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"em"}).AddSyst(cb,
                                             "CMS_scale_e_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        
        // Use only one of the TES options below per channel
        // these both need to be included while we work on getting all channels
        // having DM based TES, then we will switch permanently
        //
        // Standard TES
        // FIXME
        // This CR segment is temporary, just to check that the CRs work (needed to use old DCS
        // without scale_t on all shapes)
        // FIXME
//        if (control_region == 1) {
//            cb.cp().process(JoinStr({sig_procs, {"ZTT","TTT","VV","VVT","EWKZ"}})).channel({"et","mt","tt"}).AddSyst(cb,
//                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
//        }
//        else {
//            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
//                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
//        }


        // Decay Mode based TES Settings
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        

        //##############################################################################
        //  jet and met energy Scale
        //##############################################################################
 
        // MET Systematic shapes
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt","em"}).bin_id({1,2,3}).AddSyst(cb,
                                                  "CMS_scale_met_clustered_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt","em"}).bin_id({1,2,3}).AddSyst(cb,
                                                  "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));
        
        
        // Standard JES, factorized 27 JES implementation below
        // only use 1 at a time.
        // full 27 JES...
//        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).bin_id({1,2,3}).AddSyst(cb,
 //                                            "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
 //           cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).bin_id({1,2,3}).channel({"em"}).AddSyst(cb,
 //                                          "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
        
//        cb.cp().process(JoinStr({sig_procs, {"ZTT","TT","W","VV", "ZL", "QCD"}})).channel({"ttbar"}).AddSyst(cb,
//                                             "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));

        // JES factorization test tautau        
        std::vector< std::string > uncertNames = {
            "AbsoluteFlavMap",
            "AbsoluteMPFBias",
            "AbsoluteScale",
            "AbsoluteStat",
            //"CorrelationGroupFlavor",
            //"CorrelationGroupIntercalibration",
            //"CorrelationGroupMPFInSitu",
            //"CorrelationGroupUncorrelated",
            //"CorrelationGroupbJES",
            //"FlavorPhotonJet",
            //"FlavorPureBottom",
            //"FlavorPureCharm",
            //"FlavorPureGluon",
            //"FlavorPureQuark",
            "FlavorQCD",
            //"FlavorZJet",
            "Fragmentation",
            "PileUpDataMC",
            //"PileUpEnvelope",
            //"PileUpMuZero",
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
            //"SubTotalAbsolute",
            //"SubTotalMC",
            //"SubTotalPileUp",
            //"SubTotalPt",
            //"SubTotalRelative",
            //"SubTotalScale",
            "TimePtEta",
            //"TimeRunBCD",
            //"TimeRunE",
            //"TimeRunF",
            //"TimeRunGH",
            //"TotalNoFlavorNoTime",
            //"TotalNoFlavor",
            //"TotalNoTime",
            //"Total", // Total JES value, don't include
            //"Closure", // Closure Measure, don't include
        }; // end uncertNames
        // Uncomment below for 27 JES
        //
        
        /*for (string uncert:uncertNames){
         cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","mt"}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"em"}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         
         //Note:  TTJ is excluded from bin 13 of et channel as it was empty and causing error
         cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).bin_id({1,2,3,10,11,12,14,15}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_TTJ})).channel({"et"}).bin_id({13}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         
         cb.cp().process({"ZTT","TT","W","VV", "ZL", "QCD"}).channel({"ttbar"}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         
         
         }*/
        for (string uncert:uncertNames){
            
            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).bin_id({10,11,14}).AddSyst(cb,
                                                                                                "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));

            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_TTJ})).channel({"et"}).bin_id({13}).AddSyst(cb,
                                                                                                "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
            
            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).bin_id({10,11,13,14}).AddSyst(cb,
                                                                                                "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
            
            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).bin_id({10,11,12}).AddSyst(cb,
                                                                                                 "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        }
        
        
        
        
        
        //JES for tt
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01244515401));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.0065364049));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00532999771));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.984040861582));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeJERHF_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.0065364049));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01175413407));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01148273772));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.994091250891));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.994091250891));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00590874911));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00911644818));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.983412519208));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00923747942));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01961480886));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01299795333));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00665434016));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00490130831));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00546859182));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.968785018213));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.995177865431));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00901271758));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01778152211));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00507694785));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.995758100964));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01324266977));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.01324266977));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01324266977));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.01324266977));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01145848957));
        cb.cp().process({"TTJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01601456021));
        cb.cp().process({"TTJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.01601456021));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.978152281977));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00304039446));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01605523932));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00733361765));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.984061069106));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.957481826367));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01563010796));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.01563010796));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01304150742));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00550070401));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00258860054));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0054169136));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.970464556154));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.0127700062));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.04978898077));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.04978898077));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.992464965254));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.994977368991));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.994977368991));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.962168177775));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.992464965254));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.987865315808));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.994899039926));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.990543662409));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.994604257128));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.997498197377));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.992464965254));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00612831424));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00477238867));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.990543662409));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.994604257128));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.993143284071));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(0.997411443663));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00753503475));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00753503475));
        cb.cp().process({"WH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00502263101));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.995163050671));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.995163050671));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.995163050671));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.973000067032));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.995163050671));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.992768216286));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.995704576397));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.995235563563));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.992945187505));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.993631939099));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.993595340174));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.991284030971));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.995229348543));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00483694933));
        cb.cp().process({"ZH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00483694933));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.988201361617));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.994177883119));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00735936163));
        cb.cp().process({"ZTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.930682290098));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.03206293817));
        cb.cp().process({"TTT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.976739002514));
        cb.cp().process({"TTJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.936103550246));
        cb.cp().process({"TTJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.985502638586));
        cb.cp().process({"TTJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.95060091166));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.996671566248));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.985040891467));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.985040891467));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.944578399679));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.961525208044));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.989842753761));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.984098986063));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.974130055161));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.06359277713));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01536930075));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.992276075207));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.98671063641));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.955642098242));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.994523711198));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(0.987193209781));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.974321168649));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.0083002728));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.994819855338));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.996180645626));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01616751148));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.0039404164));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.995378323073));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.989040290257));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.992278591597));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.992278591597));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.946981211794));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.989040290257));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.979131977658));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.989040290257));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.986311663591));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.993830318856));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.9929092503));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.983314350593));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.994823102767));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01386808651));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.989040290257));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.989457029298));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.993830318856));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.990146913854));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.989457029298));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01095970974));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.01095970974));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.976012239375));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.994121241522));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.993655662105));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.997357749372));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00986566507));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.993542068993));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.993850958212));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.994955378963));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.0083821342));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.979467710722));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.994592433175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.990371297744));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.992371091175));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.99642896464));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00506440968));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.992357346592));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.990779855344));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.992799503635));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00762890882));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00762890882));
        cb.cp().process({"ggH125"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00824765659));
        cb.cp().process({"qqH125"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.0091440601));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00338910703));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00306955129));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00306955129));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01827664079));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00338910703));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01347068811));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00595749357));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.01008158108));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.0043090623));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.960178177268));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.989598863185));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00595749357));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01219939448));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.00306955129));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.995690937703));
        cb.cp().process({"W"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.996610892972));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0098131016));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00411059982));
        cb.cp().process({"VVJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.996583522013));
        cb.cp().process({"VVT"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00460742089));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00545399358));
        cb.cp().process({"ZL"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.990937653045));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01781285153));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(1.00258242243));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00969599723));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00481928938));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00073305545));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.997417577572));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.0076960679));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00928458423));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00725082062));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.995180710617));
        cb.cp().process({"ZJ"}).channel({"tt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.995180710617));
        
        //JES for mt
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00875543073));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00340771995));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00308758623));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.989422208727));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00718285709));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00358859032));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00380986955));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00285619361));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01039940134));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00643274475));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.971191744164));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01347393224));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.993477456034));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.992465895443));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00462587782));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00462587782));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01713360958));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00462587782));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00956754445));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.01085128552));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00374610181));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00462587782));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.964501009216));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.996328419623));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01202647073));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01636407755));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00355001893));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.995374122183));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.995374122183));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.991159078245));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.992094457121));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00706895106));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.966078565099));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.0089091179));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00633449848));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00336332746));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.976932854818));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00837233812));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.02023064736));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.02023064736));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00728993949));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.02023064736));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.02023064736));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.947513030852));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.979769352641));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01591552631));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.03289938497));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.02023064736));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01402620293));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01402620293));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.01402620293));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.914534696061));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01402620293));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01470862451));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.01402620293));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.985973797065));
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00503474319));
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01313336657));
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.996268355665));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.996282570126));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00197412817));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.992506735988));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.989714782855));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.988307272894));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.988307272894));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.988307272894));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.964614284114));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.988307272894));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.981478076583));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.994304039596));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.990468343263));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.993872374901));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.987356118648));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00397854329));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01279043944));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.99169145042));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.99441368147));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.989296408995));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.995018708204));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01169272711));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.01169272711));
        cb.cp().process({"ZH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00469058116));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.98787604858));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.990650198813));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.990650198813));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.94087610903));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.98787604858));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.981473254224));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.990344999985));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.985944474503));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.996446760541));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.996024125391));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.985591342828));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01007824107));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.989669941739));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.993945761219));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.981654272163));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.99640916107));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01324583894));
        cb.cp().process({"TTT"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.01212395142));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.980537482999));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.98536457347));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.98536457347));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.906233289684));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.980537482999));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.975552383438));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.980537482999));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.960243395266));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.989150278466));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.995014897673));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.975552383438));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.993853989944));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00412138335));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(1.00054769527));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.971884129202));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.989150278466));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.990079187599));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.995014897673));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.019462517));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.019462517));
        cb.cp().process({"TTJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.999294292877));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.959325155195));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.982955869862));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.989919238234));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.990114049845));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.988405176493));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.0112458796));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.993459244292));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.984935765881));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.963556592018));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.986675216542));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00715428284));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0052653548));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.995356068001));
        cb.cp().process({"W"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00614735607));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00650567923));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00536793128));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00725584143));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00533131585));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00533302987));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.990814615807));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00411142219));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"mt"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));



        
        //JES for et
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0048383722));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.0048383722));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.0037164185));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.0048383722));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.978975501165));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00381338592));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00659462719));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.0037164185));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.0025944648));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01378219704));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00355649047));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00472408872));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00550161786));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00355649047));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.974333798522));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.990941891677));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00472408872));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00550161786));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00817876323));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01606132087));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00837305724));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00447312882));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00524154876));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.972907339731));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00569765039));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01336685248));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.992531187318));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00584256819));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00584256819));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.971413924559));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.99415743181));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00499381715));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01654735523));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00570655773));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00458372602));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.02742016102));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00462055321));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01523211383));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00999380281));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.01315940828));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.93919891208));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.03770578358));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00493370182));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.01530808176));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.995614418117));
        cb.cp().process({"W"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.995420947555));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01062418327));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.977113288947));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01451084244));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.02826481265));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.02099955212));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00761191381));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00726526053));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.01338763831));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.01305080511));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.946369075612));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.986612361691));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00761191381));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01738687126));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.0304988994));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.0054388913));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.986949194891));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.994561108704));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.03461762363));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.0159274809));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.01063778335));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00703035708));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00889712383));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00703035708));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.961972008201));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.992969642923));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.01063778335));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01397819542));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.02361397854));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.00703035708));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01939374359));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.995326027535));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.995326027535));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.995326027535));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.970950114276));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.995326027535));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.986493689147));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.99404195075));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.995714381214));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.996712173785));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.994067134148));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00524283655));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00461994668));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.994066090936));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.992456002277));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.993956942201));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.995458567259));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(0.996459650631));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00467397247));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00467397247));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00354034937));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.993921815117));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.974831683349));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.993921815117));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.987988394229));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.99401551005));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.993620645077));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.996805830392));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.99072764551));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00705979501));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00258348828));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.997416511724));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.996505303393));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.996588442131));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.9798539615));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.993198773461));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00607818488));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00607818488));
        cb.cp().process({"ZH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.996805830392));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.992063843377));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.99746758781));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.99746758781));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.933106229849));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.992063843377));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.983712850775));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.991688714458));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.974301291569));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.987436650734));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.99746758781));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.978022065076));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.97561036182));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.0134151712));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.997190335232));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.981408189167));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.987457038471));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.996857189566));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.989037606731));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(0.99746758781));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.99746758781));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01052180789));
        cb.cp().process({"TTT"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00793615662));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.921806365519));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.98364887871));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.971343272596));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00209081445));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.987390543632));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.98398199789));
        cb.cp().process({"TTJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.984728871667));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.988671490294));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.99315031858));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.99315031858));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.957524674036));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.98611095831));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.979801605076));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.990820978756));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.986920578426));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.989861490503));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.984633964176));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.05738740556));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01163349148));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.992458999711));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.985570123101));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.96457223392));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.991320450885));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.987892911267));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01536603582));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.01132850971));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00887925576));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.986938042279));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.995102468135));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00283340853));
        cb.cp().process({"VV"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.995337502828));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.985760796865));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.99520708884));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01307998958));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.0037271877));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.992292034078));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.991263304811));
        cb.cp().process({"WH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00412806839));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01823106077));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00764294811));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00543505218));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00509582235));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.985490821089));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00757426854));
        cb.cp().process({"ZTT"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.00938849466));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01537987215));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00562906787));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.98994534881));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.0057061085));
        cb.cp().process({"ggH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01312477458));
        cb.cp().process({"qqH125"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.993394483237));
        cb.cp().process({"W"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00297021796));
        cb.cp().process({"W"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00278747264));
        cb.cp().process({"W"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01549307286));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.0053791628));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.992430104093));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00737925287));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.02362595031));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.00507169961));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00577867172));
        cb.cp().process({"ZL"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01355018283));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00436417685));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.987891184451));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.996372218572));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZJ"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.0081910023));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.995302730771));


        //JES for em
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00676941355));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0014575809));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.99518590626));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.993847147922));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.02328861079));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.991796579248));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.996240670101));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.969793313569));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.0096011381));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.993847147922));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01580583282));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.995370373676));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.00954217909));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00676941355));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.995772592208));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.0037593299));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.99760647782));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.00960045445));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.991432204849));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.991432204849));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00848545696));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.0181682496));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.991432204849));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.0192949246));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01658363571));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.01178102352));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.009558801));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.909240354708));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.995941356151));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01471908584));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.04070986812));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00925393377));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.993680409313));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.979004019653));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.993689739712));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.994453995785));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.99061611512));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.981443072596));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.0077865187));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00710524872));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00631959069));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.996031438653));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00659071898));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.999652357008));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.00117876903));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.01447828114));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00729545302));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.0030760427));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.923273562341));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00824745578));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtBB_$ERA", "lnN", SystMap<>::init(0.996031438653));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00269302791));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.0213666739));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.02302756582));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00782400766));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00051694943));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00508816404));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.00508816404));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.00508816404));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.03310161245));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00508816404));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.0328056197));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.02919732423));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00411471437));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.0328056197));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.914088576968));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.03081343036));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeJERHF_$ERA", "lnN", SystMap<>::init(1.00311861971));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.02919732423));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.968099041941));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.02869090533));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00411471437));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00411471437));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.994911835964));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.994911835964));
        cb.cp().process({"W"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.973431619713));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01102597069));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00933936271));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00414979416));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.00634593132));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.00612778437));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.961878881892));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00419541212));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.02205871779));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00482506075));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.0062174462));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.1250269225));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.06465927863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.06465927863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.934567185869));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.06465927863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.06465927863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.935340721368));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.993199236324));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.99442533425));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.995146433938));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.972916821539));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.993199236324));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.992627453416));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.99572172102));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.991925157068));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.991188145687));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01022207847));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00744844542));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.985924340725));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.993962608285));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00680076368));
        cb.cp().process({"WH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00680076368));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.978813815429));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.992199028857));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.995246821578));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.0094640226));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00297194844));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.997028051555));
        cb.cp().process({"ZH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.992816817419));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.990897338536));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.951479862871));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.990542494245));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.982150387093));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.994743596109));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.989048005531));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.98745112454));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.985385273714));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01480105025));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00838722459));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.991542083557));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.983605806418));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.985906704643));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.992058457586));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01062163914));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00910266146));
        cb.cp().process({"TT"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00618592869));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.986302579197));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.993504667879));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.01414090413));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.991044357922));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.990911852449));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(0.99249137129));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(0.993427168572));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.989008590585));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(0.978937278544));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtBB_$ERA", "lnN", SystMap<>::init(0.996240713961));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(0.99119964913));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(0.982384195265));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(0.992529011228));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.985309837601));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.00648336786));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(0.996333693539));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.979518107556));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.992969216819));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(0.995342843105));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(0.9908952621));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.01175209754));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00908814755));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00507924044));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.984617787229));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.0090927899));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(0.988424945947));
        cb.cp().process({"W"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.991563567743));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.979864770635));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.02017063214));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.984008465348));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.990276705399));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZTT"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.01902591435));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.00839006826));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00472025522));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.984893367818));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.00636095136));
        cb.cp().process({"ggH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.00362663521));
        cb.cp().process({"qqH125"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.997768819194));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.02113808791));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.0038120458));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.987226178017));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.993095444628));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.016727463));
        cb.cp().process({"W"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.01369354434));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"VV"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(1.00793952863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteScale_$ERA", "lnN", SystMap<>::init(1.006534453));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteStat_$ERA", "lnN", SystMap<>::init(1.006534453));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(1.05068930688));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(1.00793952863));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "lnN", SystMap<>::init(1.01704551229));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC1_$ERA", "lnN", SystMap<>::init(1.0065709944));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "lnN", SystMap<>::init(1.00901489605));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtHF_$ERA", "lnN", SystMap<>::init(1.01043737862));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(1.01076014652));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(0.945504599973));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(0.984964296975));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC1_$ERA", "lnN", SystMap<>::init(1.00516190506));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "lnN", SystMap<>::init(1.01336870411));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(1.04386625676));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(1.00676088281));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatFSR_$ERA", "lnN", SystMap<>::init(1.00576890734));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatHF_$ERA", "lnN", SystMap<>::init(1.00634484896));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(0.991322942217));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(0.99206047137));
        cb.cp().process({"ZL"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(0.994069598803));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_AbsoluteMPFBias_$ERA", "lnN", SystMap<>::init(0.990785577842));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_FlavorQCD_$ERA", "lnN", SystMap<>::init(0.97850514428));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_Fragmentation_$ERA", "lnN", SystMap<>::init(0.990144491785));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpDataMC_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_PileUpPtRef_$ERA", "lnN", SystMap<>::init(0.989192044919));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "lnN", SystMap<>::init(1.02316158807));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeFSR_$ERA", "lnN", SystMap<>::init(1.01024839233));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtEC2_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativePtHF_$ERA", "lnN", SystMap<>::init(0.989055395336));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_RelativeStatEC_$ERA", "lnN", SystMap<>::init(0.989895270923));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionECAL_$ERA", "lnN", SystMap<>::init(1.00988206177));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_SinglePionHCAL_$ERA", "lnN", SystMap<>::init(1.00921442216));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,"CMS_scale_j_TimePtEta_$ERA", "lnN", SystMap<>::init(1.00904793135));



//        for (string uncert:uncertNames){
//            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","mt","et"}).bin_id({1,2,3}).AddSyst(cb,
//                                           "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
//            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).bin_id({1,2,3}).channel({"em"}).AddSyst(cb,
//                                           "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
//        }


//        cb.cp().AddSyst(cb,
//                        "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
//                        ({"et", "mt", "em", "tt","ttbar"}, {1, 2, 3}, JoinStr({sig_procs, all_mc_bkgs_no_W}), 1.01));
        cb.cp().AddSyst(cb,
                        "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"ttbar"}, {1, 2, 3}, {all_mc_bkgs}, 1.01));
        
        if (control_region > 0) {
            // Add to all CRs, don't include QCD or WJets in et/mt which have CRs, or QCD in tt
            
            cb.cp().process(all_mc_bkgs).channel({"et","mt"}).bin_id({10, 11, 12, 13, 14, 15}).AddSyst(cb,
                                                            "CMS_scale_met_clustered_$ERA", "shape", SystMap<>::init(1.00));
            cb.cp().process(all_mc_bkgs).channel({"et","mt"}).bin_id({10, 11, 12, 13, 14, 15}).AddSyst(cb,
                                                            "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));
            
//            cb.cp().AddSyst(cb,
//                            "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
//                            ({"et", "mt"}, {10, 11, 12, 13, 14, 15}, JoinStr({all_mc_bkgs_no_W}), 1.01));
//            cb.cp().AddSyst(cb,
//                            "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
//                            ({"tt"}, {10, 11, 12}, JoinStr({all_mc_bkgs}), 1.01));
        }


        
        
        
        
        //##############################################################################
        //  Background normalization uncertainties
        //##############################################################################
        
        //   Diboson  Normalisation - fully correlated
        cb.cp().process({"VV","VVT","VVJ","VVJ_rest"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
        if (! ttbar_fit){
        //   ttbar Normalisation - fully correlated
	    cb.cp().process({"TT","TTT","TTJ","TTJ_rest"}).AddSyst(cb,
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));}

        // W norm, just for em, tt and the mm region where MC norm is from MC
//        cb.cp().process({"W","W_rest"}).channel({"tt","em","mm"}).AddSyst(cb,
//                                             "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.20)); // splitted to two uncertainties as following
        
        cb.cp().process({"W"}).channel({"em"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeLep_13TeV", "lnN", SystMap<>::init(1.20));
        
        cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));
        
        
        // QCD norm, just for em  decorrelating QCD BG for differenet categories
//        cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
//        
//                                           "CMS_htt_QCD_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));

        // QCD norm, just for tt
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));
        
        
        // QCD norm, just for tt
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.027));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.027));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.15));
        
        
        //Iso to antiiso extrapolation
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.20));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.20));
        
        
        //This should affect only shape (normalized to nominal values)
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_0jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_boosted_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_vbf_$ERA", "shape", SystMap<>::init(1.00));
        
        
        // based on the Ersatz study in Run1
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                             "WHighMTtoLowMT_0jet_$ERA", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,
                                             "WHighMTtoLowMT_boosted_$ERA", "lnN", SystMap<>::init(1.05));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "WHighMTtoLowMT_vbf_$ERA", "lnN", SystMap<>::init(1.10));
        
        

        
        //##############################################################################
        //  DY LO->NLO reweighting, Between no and twice the correc(on.
        //##############################################################################
        
        cb.cp().process( {"ZTT","ZJ","ZL","ZJ_rest"}).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZTT","ZL"}).channel({"em"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Ttbar shape reweighting, Between no and twice the correction
        //##############################################################################
        
        cb.cp().process( {"TTJ","TTT","TTJ_rest"}).channel({"tt"}).AddSyst(cb,
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
        
        
        
        
        

        //Changed March 10
//        cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
//                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.25));
//        cb.cp().process({"ZL"}).channel({"et"}).AddSyst(cb,
//                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.12));
        
        
        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_mFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_mFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_eFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_eFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        
//        
//        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1}).AddSyst(cb,
//                                                                        "CMS_ZLShape_mFakeTau_0jet_1prong_$ERA", "shape", SystMap<>::init(1.00));
//        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1}).AddSyst(cb,
//                                                                        "CMS_ZLShape_mFakeTau_0jet_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
//        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1}).AddSyst(cb,
//                                                                        "CMS_ZLShape_eFakeTau_0jet_1prong_$ERA", "shape", SystMap<>::init(1.00));
//        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1}).AddSyst(cb,
//                                                                        "CMS_ZLShape_eFakeTau_0jet_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
//        
        
        //##############################################################################
        // jet  to tau fake only in tt, mt and et channels
        //##############################################################################
        
        cb.cp().process( {"TTJ","ZJ","VVJ","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"}).channel({"tt","mt","et"}).AddSyst(cb,
                                                                            "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process( {"W"}).channel({"tt","mt","et"}).bin_id({1,2,3,13,14,15}).AddSyst(cb,
                                                                "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));
        

        //##############################################################################
        // Theoretical Uncertainties on signal
        //##############################################################################
        
        //scale_gg on signal
        cb.cp().process( {"ggH"}).channel({"et","mt","tt","em"}).AddSyst(cb,
                                             "CMS_scale_gg_$ERA", "shape", SystMap<>::init(1.00));
        
        // Scale uncertainty on signal Applies to ggH in boosted and VBF. Event-by-event weight applied as a func(on of pth or mjj. Fully correlated between categories and final states.
        
        
        // Covered by CMS_scale_gg above
        //cb.cp().AddSyst(cb, "CMS_ggH_QCDUnc", "lnN", SystMap<channel, bin_id, process>::init
        //                ({"em"},{1},{"ggH"}, 0.93)
        //                ({"et"},{1},{"ggH"}, 0.93)
        //                ({"mt"},{1},{"ggH"}, 0.93)
        //                ({"tt"},{1},{"ggH"}, 0.93)
        //                
        //                ({"em"},{2},{"ggH"}, 1.15)
        //                ({"et"},{2},{"ggH"}, 1.18)
        //                ({"mt"},{2},{"ggH"}, 1.18)
        //                ({"tt"},{2},{"ggH"}, 1.20)
        //                
        //                
        //                ({"em"},{3},{"ggH"}, 1.25)
        //                ({"et"},{3},{"ggH"}, 1.15)
        //                ({"mt"},{3},{"ggH"}, 1.08)
        //                ({"tt"},{3},{"ggH"}, 1.10)
        //                );
                        
                        
                        
            cb.cp().AddSyst(cb, "CMS_qqH_QCDUnc", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 0.997)
                        ({"et"},{1},{"qqH"}, 1.003)
                        ({"mt"},{1},{"qqH"}, 0.998)
                        ({"tt"},{1},{"qqH"}, 0.997)
                        
                        ({"em"},{2},{"qqH"}, 1.004)
                        ({"et"},{2},{"qqH"}, 1.004)
                        ({"mt"},{2},{"qqH"}, 1.002)
                        ({"tt"},{2},{"qqH"}, 1.003)
                        
                        
                        ({"em"},{3},{"qqH"}, 1.005)
                        ({"et"},{3},{"qqH"}, 1.005)
                        ({"mt"},{3},{"qqH"}, 1.002)
                        ({"tt"},{3},{"qqH"}, 1.003)
                        );
       
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_PDF", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 1.007)
                        ({"et"},{1},{"ggH"}, 1.007)
                        ({"mt"},{1},{"ggH"}, 1.007)
                        ({"tt"},{1},{"ggH"}, 1.009)
                        
                        ({"em"},{2},{"ggH"}, 1.007)
                        ({"et"},{2},{"ggH"}, 1.007)
                        ({"mt"},{2},{"ggH"}, 1.007)
                        ({"tt"},{2},{"ggH"}, 1.009)
                        
                        
                        ({"em"},{3},{"ggH"}, 1.007)
                        ({"et"},{3},{"ggH"}, 1.007)
                        ({"mt"},{3},{"ggH"}, 1.007)
                        ({"tt"},{3},{"ggH"}, 1.009)
                        );
        
        
        
        cb.cp().AddSyst(cb, "CMS_qqH_PDF", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 1.011)
                        ({"et"},{1},{"qqH"}, 1.005)
                        ({"mt"},{1},{"qqH"}, 1.005)
                        ({"tt"},{1},{"qqH"}, 1.008)
                        
                        ({"em"},{2},{"qqH"}, 1.005)
                        ({"et"},{2},{"qqH"}, 1.002)
                        ({"mt"},{2},{"qqH"}, 1.002)
                        ({"tt"},{2},{"qqH"}, 1.003)
                        
                        
                        ({"em"},{3},{"qqH"}, 1.005)
                        ({"et"},{3},{"qqH"}, 1.005)
                        ({"mt"},{3},{"qqH"}, 1.005)
                        ({"tt"},{3},{"qqH"}, 1.005)
                        );
        
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_UEPS", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 1.015)
                        ({"et"},{1},{"ggH"}, 1.015)
                        ({"mt"},{1},{"ggH"}, 1.015)
                        ({"tt"},{1},{"ggH"}, 1.015)
                        
                        ({"em"},{2},{"ggH"}, 0.945)
                        ({"et"},{2},{"ggH"}, 0.945)
                        ({"mt"},{2},{"ggH"}, 0.945)
                        ({"tt"},{2},{"ggH"}, 0.945)
                        
                        ({"em"},{3},{"ggH"}, 1.03)
                        ({"et"},{3},{"ggH"}, 1.03)
                        ({"mt"},{3},{"ggH"}, 1.03)
                        ({"tt"},{3},{"ggH"}, 1.03)
                        );
        
        
        
        cb.cp().AddSyst(cb, "CMS_qqH_UEPS", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 1.015)
                        ({"et"},{1},{"qqH"}, 1.015)
                        ({"mt"},{1},{"qqH"}, 1.015)
                        ({"tt"},{1},{"qqH"}, 1.015)
                        
                        ({"em"},{2},{"qqH"}, 0.945)
                        ({"et"},{2},{"qqH"}, 0.945)
                        ({"mt"},{2},{"qqH"}, 0.945)
                        ({"tt"},{2},{"qqH"}, 0.945)
                        
                        ({"em"},{3},{"qqH"}, 1.03)
                        ({"et"},{3},{"qqH"}, 1.03)
                        ({"mt"},{3},{"qqH"}, 1.03)
                        ({"tt"},{3},{"qqH"}, 1.03)
                        );
        
        
        /*
        cb.cp().AddSyst(cb, "CMS_ggH_mcComp", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 0.95)
                        ({"et"},{1},{"ggH"}, 0.95)
                        ({"mt"},{1},{"ggH"}, 0.95)
                        ({"tt"},{1},{"ggH"}, 0.95)
                        
                        ({"em"},{2},{"ggH"}, 1.15)
                        ({"et"},{2},{"ggH"}, 1.15)
                        ({"mt"},{2},{"ggH"}, 1.15)
                        ({"tt"},{2},{"ggH"}, 1.15)
                        
                        ({"em"},{3},{"ggH"}, 1.20)
                        ({"et"},{3},{"ggH"}, 1.10)
                        ({"mt"},{3},{"ggH"}, 1.10)
                        ({"tt"},{3},{"ggH"}, 1.10)
                        );
        
        
        
        cb.cp().AddSyst(cb, "CMS_qqH_mcComp", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 0.95)
                        ({"et"},{1},{"qqH"}, 0.95)
                        ({"mt"},{1},{"qqH"}, 1.05)
                        ({"tt"},{1},{"qqH"}, 1.05)
                        
                        ({"em"},{2},{"qqH"}, 1.10)
                        ({"et"},{2},{"qqH"}, 1.10)
                        ({"mt"},{2},{"qqH"}, 1.10)
                        ({"tt"},{2},{"qqH"}, 1.05)
                        
                        ({"em"},{3},{"qqH"}, 0.90)
                        ({"et"},{3},{"qqH"}, 0.90)
                        ({"mt"},{3},{"qqH"}, 0.90)
                        ({"tt"},{3},{"qqH"}, 0.90)
                        );
        */
        
        //    Uncertainty on BR for HTT @ 125 GeV
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_THU", "lnN", SystMap<>::init(1.017));
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
        cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
        
        //    Uncertainty on BR of HWW @ 125 GeV
        cb.cp().process({"HWW_gg125","HWW_qq125"}).AddSyst(cb,"BR_hww_THU", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"HWW_gg125","HWW_qq125"}).AddSyst(cb,"BR_hww_PU_mq", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"HWW_gg125","HWW_qq125"}).AddSyst(cb,"BR_hww_PU_alphas", "lnN", SystMap<>::init(1.0066));
        
        
        cb.cp().process({"ggH","HWW_gg125"}).AddSyst(cb,"QCDScale_ggH", "lnN", SystMap<>::init(1.039));
        cb.cp().process({"qqH","HWW_qq125"}).AddSyst(cb,"QCDScale_qqH", "lnN", SystMap<>::init(1.004));
        cb.cp().process({"WH"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.007));
        cb.cp().process({"ZH"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.038));
        
        cb.cp().process({"ggH","HWW_gg125"}).AddSyst(cb,"pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
        cb.cp().process({"qqH","HWW_qq125"}).AddSyst(cb,"pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
        cb.cp().process({"WH"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.019));
        cb.cp().process({"ZH"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.016));
        
        
        
        
        
        //  // Recoil corrections
        //  // ------------------
        //  // These should not be applied to the W in all control regions becasuse we should
        //  // treat it as an uncertainty on the low/high mT factor.
        //  // For now we also avoid applying this to any of the high-mT control regions
        //  // as the exact (anti-)correlation with low mT needs to be established
        //  // CHECK THIS
        //  cb.cp().AddSyst(cb,
        //    "CMS_htt_boson_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
        //    ({"et", "mt", "em", "tt"}, {1, 2, 3, 4,5,6}, JoinStr({signal, {"ZTT", "W"}}), 1.02));
        //
        
        
        
        if(mm_fit)
        {
            // Add Z crosssection uncertainty on ZL, ZJ  (not ZTT due to taking into account the mm control region).
            // Also don't add it for the mm control region
            cb.SetFlag("filters-use-regex", true);
            cb.cp().channel({"mm"},false).process({"ZL", "ZJ"}).AddSyst(cb,
                                             "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
            cb.cp().channel({"mm"},false).bin({"_cr$"}).process({"ZTT"}).AddSyst(cb,
                                             "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
            cb.SetFlag("filters-use-regex", false);
            
            cb.FilterSysts([](ch::Systematic *syst) {
                return syst->name() == "lumi_13TeV" &&
                (
                 (syst->channel() == "mm" && syst->process() == "ZL") ||
                 (syst->channel() != "mm" && syst->process() == "ZTT" &&
                  (syst->bin_id() == 1 || syst->bin_id() == 2 || syst->bin_id() == 3 || syst->bin_id() == 4 || syst->bin_id() == 5 || syst->bin_id() == 6 ))
                 );
            });
        }
        else
        {
            // Z->mumu CR normalization propagation
            // 0jet normalization only
            cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_0jet_$CHANNEL_$ERA", "lnN",
                                             SystMap<channel, bin_id>::init({"em","tt"},{1}, 1.07));
            cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_0jet_lt_$ERA", "lnN",
                                             SystMap<channel, bin_id>::init({"et","mt"},{1}, 1.07));
            
            // boosted normalization only
            cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_boosted_$CHANNEL_$ERA", "lnN",
                                             SystMap<channel, bin_id>::init({"em","tt"},{2}, 1.07));
            cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_boosted_lt_$ERA", "lnN",
                                             SystMap<channel, bin_id>::init({"et","mt"},{2}, 1.07));
            
            // VBF norm and shape for et/mt/tt
            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"em"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_VBF_em_$ERA", "lnN", SystMap<>::init(1.15));
            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_VBF_lt_$ERA", "lnN", SystMap<>::init(1.15));
            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_zmm_norm_extrap_VBF_tt_$ERA", "lnN", SystMap<>::init(1.10));

//            // FIXME should have EWKZ in all
//            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"tt"}).bin_id({3}).AddSyst(cb,
//                                             "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));
//            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"mt","et"}).bin_id({3}).AddSyst(cb,
//                                             "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));
//            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest"}).channel({"em"}).bin_id({3}).AddSyst(cb,
//                                            "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));

            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"tt","et","mt"}).bin_id({3}).AddSyst(cb,
                                            "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));
            cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest"}).channel({"em"}).bin_id({3}).AddSyst(cb,
                                            "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));


            // Add the zmumu extrapolation uncertainties to Drell-Yan in CRs
            // if applicable
            if(control_region > 0)
            {
                // Z->mumu CR normalization propagation
                // 0jet normalization only
                cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_0jet_$CHANNEL_$ERA", "lnN",
                                                 SystMap<channel, bin_id>::init({"tt"},{10}, 1.07));
                cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_0jet_lt_$ERA", "lnN",
                                                 SystMap<channel, bin_id>::init({"et","mt"},{10,13}, 1.07));
                
                // boosted normalization only
                cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_boosted_$CHANNEL_$ERA", "lnN",
                                                 SystMap<channel, bin_id>::init({"tt"},{11}, 1.07));
                cb.cp().process({"ZTT", "ZL", "ZJ", "ZJ_rest", "EWKZ"}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_boosted_lt_$ERA", "lnN",
                                                 SystMap<channel, bin_id>::init({"et","mt"},{11,14}, 1.07));
                
                // VBF norm and shape for et/mt/tt
                cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"et","mt"}).bin_id({12,15}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_VBF_lt_$ERA", "lnN", SystMap<>::init(1.15));
                cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"tt"}).bin_id({12}).AddSyst(cb,
                                                 "CMS_htt_zmm_norm_extrap_VBF_tt_$ERA", "lnN", SystMap<>::init(1.10));

                cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest"}).channel({"mt","et"}).bin_id({12,15}).AddSyst(cb,
                                                 "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));
                cb.cp().process( {"ZL","ZTT","ZJ", "ZJ_rest", "EWKZ"}).channel({"tt"}).bin_id({12,15}).AddSyst(cb,
                                                 "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));

            }
            
        } // end not mm_fit
        
        
        
        
        //  if (control_region == 0) {
        //    // the uncertainty model in the signal region is the classical one
        
        //    }
        

        if (control_region == 1) {
            // Create rateParams for control regions:
            //  - [x] 1 rateParam for all W in every region
            //  - [x] 1 rateParam for QCD in low mT
            //  - [x] 1 rateParam for QCD in high mT
            //  - [x] lnNs for the QCD OS/SS ratio
            //         * should account for stat + syst
            //         * systs should account for: extrap. from anti-iso to iso region,
            //           possible difference between ratio in low mT and high mT (overkill?)
            //  - [x] lnNs for the W+jets OS/SS ratio
            //         * should account for stat only if not being accounted for with bbb,
            //           i.e. because the OS/SS ratio was measured with a relaxed selection
            //         * systs should account for: changes in low/high mT and OS/SS due to JES
            //           and btag (if relevant); OS/SS being wrong in the MC (from enriched data?);
            //           low/high mT being wrong in the MC (fake rate dependence?)
            
            // Going to use the regex filtering to select the right subset of
            // categories for each rateParam
            cb.SetFlag("filters-use-regex", true);
            //      for (auto bin : cb_sig.cp().channel({"et", "mt"}).bin_set()) {
            // Regex that matches, e.g. mt_nobtag or mt_nobtag_X
            
            
            
            cb.cp().bin({"mt_0jet","mt_wjets_0jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_0jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_boosted","mt_wjets_boosted_cr","mt_vbf"}).process({"W"}).AddSyst(cb, "rate_W_cr_boosted_mt", "rateParam", SystMap<>::init(1.0));
//            cb.cp().bin({"mt_vbf","mt_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet","et_wjets_0jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted","et_wjets_boosted_cr","et_vbf"}).process({"W"}).AddSyst(cb, "rate_W_cr_boosted_et", "rateParam", SystMap<>::init(1.0));
//            cb.cp().bin({"et_vbf","et_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            cb.cp().bin({"mt_0jet","mt_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_boosted","mt_antiiso_boosted_cr","mt_vbf"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_mt", "rateParam", SystMap<>::init(1.0));
//            cb.cp().bin({"mt_vbf","mt_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet","et_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted","et_antiiso_boosted_cr","et_vbf"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_et", "rateParam", SystMap<>::init(1.0));
//            cb.cp().bin({"et_vbf","et_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            //          cb.cp().bin({bin+"(|_0jet)$"}).process({"W"}).AddSyst(cb, "rate_QCD_cr_0jet_"+bin, "rateParam", SystMap<>::init(1.0));
            //          cb.cp().bin({bin+"(|_boosted)$"}).process({"W"}).AddSyst(cb, "rate_W_cr_1jet_"+bin, "rateParam", SystMap<>::init(1.0));
            //          cb.cp().bin({bin+"(|_vbf)$"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_"+bin, "rateParam", SystMap<>::init(1.0));
 
            cb.cp().bin({"tt_0jet","tt_0jet_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_tt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_boosted","tt_boosted_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_tt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_vbf","tt_vbf_qcd_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_tt", "rateParam", SystMap<>::init(1.0));
            
            
            //        cb.cp().bin({bin+"(|_.*)$"}).process({"W"}).AddSyst(cb,
            //          "rate_W_cr_"+bin, "rateParam", SystMap<>::init(1.0));
            //
            //        // Regex that matches, e.g. mt_nobtag or mt_nobtag_qcd_cr
            //        cb.cp().bin({bin+"(|_antiiso_)$"}).process({"QCD"}).AddSyst(cb,
            //          "rate_QCD_antiiso_"+bin, "rateParam", SystMap<>::init(1.0));
            
            // Regex that matches, e.g. mt_nobtag_wjets_cr or mt_nobtag_wjets_ss_cr
            //        cb.cp().bin({bin+"_wjets_$"}).process({"QCD"}).AddSyst(cb,
            //          "rate_QCD_highmT_"+bin, "rateParam", SystMap<>::init(1.0));
            //      }
            
            /////////////////
            // Systematics //
            /////////////////

            
            // Should set a sensible range for our rateParams
            for (auto sys : cb.cp().syst_type({"rateParam"}).syst_name_set()) {
                cb.GetParameter(sys)->set_range(0.0, 5.0);
            }
            cb.SetFlag("filters-use-regex", false);
        }
            
        
        if (mm_fit) {
            cb.SetFlag("filters-use-regex", true);
            
            cb.cp().bin({"mt_0jet"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_0jet"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_0jet"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_0jet"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_boosted"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_boosted"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_boosted"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_boosted", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_1jet"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_1jet", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_vbf"}).process({"ZTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_vbf"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_vbf"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_vbf"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            
            cb.GetParameter("rate_mm_ZTT_0jet")->set_range(0.9, 1.1);
            cb.GetParameter("rate_mm_ZTT_1jet")->set_range(0.9, 1.1);
            cb.GetParameter("rate_mm_ZTT_vbf")->set_range(0.9, 1.1);
            
            cb.SetFlag("filters-use-regex", false);
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
            
            
            cb.cp().bin({"mt_vbf"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_vbf"}).process({"TTJ","TTT","TTJ_rest"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_vbf"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"ttbar_all"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.GetParameter("rate_ttbar")->set_range(0.80, 1.20);
            
            cb.SetFlag("filters-use-regex", false);
        }

	//jet fakes: shape uncertainties
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_norm_ff_qcd_1prong_njet0_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_norm_ff_qcd_1prong_njet1_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_norm_ff_qcd_3prong_njet0_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_norm_ff_qcd_3prong_njet1_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_w_1prong_njet0_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_w_1prong_njet1_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_w_3prong_njet0_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_w_3prong_njet1_$CHANNEL_stat_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_tt_1prong_njet0_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_tt_1prong_njet1_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_tt_3prong_njet0_stat_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_tt_3prong_njet1_stat_13TeV", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_norm_ff_qcd_$CHANNEL_syst_13TeV", "shape", SystMap<>::init(1.00));
        
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_w_syst_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "CMS_htt_norm_ff_tt_syst_13TeV", "shape", SystMap<>::init(1.00));
        
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "CMS_htt_norm_ff_w_$CHANNEL_syst_13TeV", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "CMS_htt_norm_ff_ttbar_$CHANNEL_syst_13TeV", "shape", SystMap<>::init(1.00));

        //jet fakes: stat norm unc
	cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_ff_norm_stat_$CHANNEL_$BIN_13TeV", "lnN", SystMap<channel, bin_id>::init
                                                                        ({"mt"}, {1}, 1.04)
                                                                        ({"mt"}, {2}, 1.03)
                                                                        ({"mt"}, {3}, 1.045)
                                                                        ({"et"}, {1}, 1.04)
                                                                        ({"et"}, {2}, 1.05)
                                                                        ({"et"}, {3}, 1.065)
                                                                        ({"tt"}, {1}, 1.03)
                                                                        ({"tt"}, {2}, 1.04)
                                                                        ({"tt"}, {3}, 1.05)
                                                                        );
        //jet fakes: syst norm: bin-correlated
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_ff_norm_syst_$CHANNEL_13TeV", "lnN", SystMap<channel, bin_id>::init
                                                                        ({"mt"}, {1}, 1.065)
                                                                        ({"mt"}, {2}, 1.062)
                                                                        ({"mt"}, {3}, 1.078)
                                                                        ({"et"}, {1}, 1.073)
                                                                        ({"et"}, {2}, 1.067)
                                                                        ({"et"}, {3}, 1.083)
                                                                        ({"tt"}, {1}, 1.026)
                                                                        ({"tt"}, {2}, 1.032)
                                                                        ({"tt"}, {3}, 1.040)
                                                                        );
        //jet fakes: syst norm: bin-dependent
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "CMS_htt_ff_sub_syst_$CHANNEL_$BIN_13TeV", "lnN", SystMap<channel, bin_id>::init
                                                                        ({"mt"}, {1}, 1.06)
                                                                        ({"mt"}, {2}, 1.04)
                                                                        ({"mt"}, {3}, 1.04)
                                                                        ({"et"}, {1}, 1.06)
                                                                        ({"et"}, {2}, 1.04)
                                                                        ({"et"}, {3}, 1.04)
                                                                        ({"tt"}, {1}, 1.06)
                                                                        ({"tt"}, {2}, 1.04)
									);

        
    }
}
