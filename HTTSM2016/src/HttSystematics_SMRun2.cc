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
        CombineHarvester cb_sig = cb.cp();
        
        
        if (control_region == 1){
            // we only want to cosider systematic uncertainties in the signal region.
            // limit to only the 0jet/1jet and vbf categories
            cb_sig.bin_id({1,2,3});
        }
        
        
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

        //##############################################################################
        //  lumi
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, {"VV","VVT","HWW_gg125","HWW_qq125","EWKZ"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.026));
        cb.cp().process({"W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"}).channel({"tt"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.026));
        
        //Add luminosity uncertainty for W in em, tt, ttbar and the mm region as norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","mm","ttbar"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.062));

	if (!ttbar_fit){
          cb.cp().process({"TTT","TTJ"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.062));
	}
        
        //##############################################################################
        //  trigger   ##FIXME   the values have been chosen rather arbitrarily
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, {"TTJ","TTT","VV","VVT", "ZL", "ZJ", "ZTT", "EWKZ"}})).channel({"mt"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, {"TTJ","TTT","VV","VVT", "ZL", "ZJ", "ZTT", "EWKZ"}})).channel({"et"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
        
        cb.cp().process(JoinStr({sig_procs, {"TT","VV", "ZL", "ZJ", "ZTT","EWKZ","W", "HWW_gg125","HWW_qq125"}})).channel({"em","ttbar"}).AddSyst(cb,
                                             // hard coding channel here keeps "em" and "ttbar" correlated
                                             "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));

        // "CMS_eff_trigger_tt_$ERA" is covered by tau ID

        
        
        //##############################################################################
        //  Electron, muon and tau Id  efficiencies
        //##############################################################################
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mm"}, {"ZTT", "TT", "VV", "ZL", "ZJ"},  1.02)
                        ({"mt"}, JoinStr({sig_procs, {"ZTT", "VV","VVT", "ZL", "ZJ","TTT", "TTJ", "EWKZ"}}),  1.02)
//                        ({"tt"}, JoinStr({sig_procs, {"W"}}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZL", "ZJ", "W", "HWW_gg125","HWW_qq125","EWKZ"}}),       1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({sig_procs, {"ZTT", "VV","VVT", "ZL", "ZJ","TTT", "TTJ", "EWKZ"}}),  1.02)
//                        ({"tt"}, JoinStr({sig_procs, {"W"}}),  1.02)
                        ({"em","ttbar"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZL", "ZJ", "W", "HWW_gg125","HWW_qq125"}}),       1.02));
        

        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VV","VVT","TTT","EWKZ"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<channel>::init
                                             ({"et", "mt"}, 1.08)
                                             ({"tt"},       1.16));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","VV","VVT","TTT","EWKZ"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<channel>::init
                                             ({"et", "mt"}, 1.04)
                                             ({"tt"}, 1.10));
        cb.cp().process(JoinStr({sig_procs, {"TTJ","ZJ"}})).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<channel>::init
                                             ({"tt"}, 1.05));
        
        //##############################################################################
        //  Electron, tau, jet and met energy Scale
        //##############################################################################
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT", "W", "ZL", "TT", "VV", "EWKZ", "HWW_gg125", "HWW_qq125","QCD"}})).channel({"em"}).AddSyst(cb,
                                             "CMS_scale_e_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        
        // Use only one of the TES options below per channel
        // these both need to be included while we work on getting all channels
        // having DM based TES, then we will switch permanently
        //
        // Standard TES
        cb.cp().process(JoinStr({sig_procs, {"ZTT","TTT","VV","VVT","EWKZ"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

        // Decay Mode based TES Settings
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).AddSyst(cb,
        //                                          "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","tt"}).AddSyst(cb,
        //                                          "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","tt"}).AddSyst(cb,
        //                                          "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        //cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","tt"}).AddSyst(cb,
        //                                          "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","TTJ","TTT","W","VVT","VV", "ZL", "ZJ","EWKZ"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
        
        cb.cp().process(JoinStr({sig_procs, {"ZTT","TT","W","VV", "ZL", "QCD"}})).channel({"ttbar"}).AddSyst(cb,
                                             //"CMS_scale_j_$BIN_$ERA", "shape", SystMap<>::init(1.00));
                                             "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, {"ZTT","TT","W","VV", "ZL", "QCD", "HWW_gg125","HWW_qq125"}})).channel({"em"}).AddSyst(cb,
                                             //"CMS_scale_j_$BIN_$ERA", "shape", SystMap<>::init(1.00));
                                             "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));

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
        //for (string uncert:uncertNames){
        //    //cb.cp().process(JoinStr({sig_procs, {"ZTT","TTJ","TTT","W","VV", "ZL", "ZJ","EWKZ"}})).channel({"et"}).AddSyst(cb,
        //    //                             "CMS_Jet"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    //cb.cp().process(JoinStr({sig_procs, {"ZTT","TTJ","TTT","W","VV", "ZL", "ZJ","EWKZ"}})).channel({"mt"}).AddSyst(cb,
        //    //                             "CMS_scale_j_Jet"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    cb.cp().process(JoinStr({sig_procs, {"ZTT","TTJ","TTT","W","VV", "ZL", "ZJ","EWKZ"}})).channel({"tt","et","mt"}).AddSyst(cb,
        //                                   "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //    //cb.cp().process(JoinStr({sig_procs, {"ZTT","TT","W","VV", "ZL", "QCD", "HWW_gg125","HWW_qq125"}})).channel({"em"}).AddSyst(cb,
        //    //                             "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
        //}


        cb.cp().AddSyst(cb,
                        "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"et", "mt", "em", "tt","ttbar"}, {1, 2, 3}, JoinStr({sig_procs, {"ZTT", "TT", "VV","VVT", "ZL", "ZJ","TTJ","TTT","EWKZ"}}), 1.01));
        cb.cp().AddSyst(cb,
                        "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em","tt"}, {1, 2, 3}, JoinStr({sig_procs, {"W"}}), 1.01));
        
        
        
        
        
        //##############################################################################
        //  Background normalization uncertainties
        //##############################################################################
        
        //   Diboson  Normalisation - fully correlated
        cb.cp().process({"VV","VVT"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
        if (! ttbar_fit){
        //   ttbar Normalisation - fully correlated
	  cb.cp().process({"TT"}).AddSyst(cb, //mf: TTJ, TTT missing?
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));}

        // W norm, just for em, tt and the mm region where MC norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","mm"}).AddSyst(cb,
                                             "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.20));
        
        // QCD norm, just for em  decorrelating QCD BG for differenet categories
//        cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
//        
//                                           "CMS_htt_QCD_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));

        // QCD norm, just for tt
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.15));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.15));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.30));
        
        
        // QCD norm, just for tt
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.05));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.05));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.43));
        
        
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
                                             "WHighMTtoLowMT_$CHANNEL_0jet_$ERA", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,
                                             "WHighMTtoLowMT_$CHANNEL_boosted_$ERA", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "WHighMTtoLowMT_$CHANNEL_vbf_$ERA", "lnN", SystMap<>::init(1.20));
        
        

        
        //##############################################################################
        //  DY LO->NLO reweighting, Between no and twice the correc(on.
        //##############################################################################
        
        cb.cp().process( {"ZTT","ZJ","ZL"}).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZTT","ZL"}).channel({"em"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        
        
        //##############################################################################
        // Ttbar shape reweighting, Between no and twice the correction
        //##############################################################################
        
// FIXME?        cb.cp().process( {"TTJ","TTT"}).channel({"et","mt","tt"}).AddSyst(cb,
// FIXME?                                    "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"TT"}).channel({"em"}).AddSyst(cb,
                                             "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        
        //##############################################################################
        // electron/muon/jet  to tau fake only in tt, mt and et channels ##FIXME  should add mt and et channels
        //##############################################################################
        
        cb.cp().process({"ZL"}).channel({"et"}).AddSyst(cb,
                                             "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.12));
        cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
                                             "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.25));
        //cb.cp().process( {"TTJ","W","ZJ"}).channel({"tt","mt","et"}).AddSyst(cb,
        //                                   "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));
        
 
        // mu to tau FR
        cb.cp().process( {"ZL"}).channel({"mt"}).AddSyst(cb,
                                             "CMS_htt_ZLShape_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        // e to tau FR
        cb.cp().process( {"ZL"}).channel({"et"}).AddSyst(cb,
                                             "CMS_htt_ZLShape_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
 
        

        //##############################################################################
        // Theoretical Uncertainties on signal
        //##############################################################################
        
        //scale_gg on signal
        //cb.cp().process( {"ggH"}).channel({"et","mt","tt","em"}).AddSyst(cb,
        cb.cp().process( {"ggH"}).channel({"et","mt","tt"}).AddSyst(cb,
                                             "CMS_scale_gg_$ERA", "shape", SystMap<>::init(1.00));
        
        // Scale uncertainty on signal Applies to ggH in boosted and VBF. Event-by-event weight applied as a func(on of pth or mjj. Fully correlated between categories and final states.
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_QCDUnc", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 0.93)
                        ({"et"},{1},{"ggH"}, 0.93)
                        ({"mt"},{1},{"ggH"}, 0.93)
                        ({"tt"},{1},{"ggH"}, 0.93)
                        
                        ({"em"},{2},{"ggH"}, 1.15)
                        ({"et"},{2},{"ggH"}, 1.18)
                        ({"mt"},{2},{"ggH"}, 1.18)
                        ({"tt"},{2},{"ggH"}, 1.20)
                        
                        
                        ({"em"},{3},{"ggH"}, 1.25)
                        ({"et"},{3},{"ggH"}, 1.15)
                        ({"mt"},{3},{"ggH"}, 1.08)
                        ({"tt"},{3},{"ggH"}, 1.10)
                        );
                        
                        
                        
            cb.cp().AddSyst(cb, "CMS_qqH_QCDUnc", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 0.97)
                        ({"et"},{1},{"qqH"}, 0.95)
                        ({"mt"},{1},{"qqH"}, 1.07)
                        ({"tt"},{1},{"qqH"}, 1.07)
                        
                        ({"em"},{2},{"qqH"}, 1.04)
                        ({"et"},{2},{"qqH"}, 1.10)
                        ({"mt"},{2},{"qqH"}, 1.10)
                        ({"tt"},{2},{"qqH"}, 1.05)
                        
                        
                        ({"em"},{3},{"qqH"}, 0.84)
                        ({"et"},{3},{"qqH"}, 0.9)
                        ({"mt"},{3},{"qqH"}, 0.9)
                        ({"tt"},{3},{"qqH"}, 0.9)
                        );
       
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_PDF", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 1.007)
                        ({"et"},{1},{"ggH"}, 1.008)
                        ({"mt"},{1},{"ggH"}, 1.007)
                        ({"tt"},{1},{"ggH"}, 1.009)
                        
                        ({"em"},{2},{"ggH"}, 1.005)
                        ({"et"},{2},{"ggH"}, 1.005)
                        ({"mt"},{2},{"ggH"}, 1.005)
                        ({"tt"},{2},{"ggH"}, 1.005)
                        
                        
                        ({"em"},{3},{"ggH"}, 1.01)
                        ({"et"},{3},{"ggH"}, 1.005)
                        ({"mt"},{3},{"ggH"}, 1.005)
                        ({"tt"},{3},{"ggH"}, 1.008)
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
                        
                        
                        ({"em"},{3},{"qqH"}, 1.004)
                        ({"et"},{3},{"qqH"}, 1.005)
                        ({"mt"},{3},{"qqH"}, 1.005)
                        ({"tt"},{3},{"qqH"}, 1.005)
                        );
        
        
        
        
        cb.cp().AddSyst(cb, "CMS_ggH_UEPS", "lnN", SystMap<channel, bin_id, process>::init
        // Run I values were in 2%-10% range, I just took those as estimates for now
                        //({"em"},{1},{"ggH"}, 1.02)
                        //({"et"},{1},{"ggH"}, 1.02)
                        //({"mt"},{1},{"ggH"}, 1.02)
                        //({"tt"},{1},{"ggH"}, 0.98)
                        //
                        //({"em"},{2},{"ggH"}, 0.95)
                        //({"et"},{2},{"ggH"}, 1.05)
                        //({"mt"},{2},{"ggH"}, 0.95)
                        //({"tt"},{2},{"ggH"}, 0.95)
                        //
                        //
                        //({"em"},{3},{"ggH"}, 0.90)
                        //({"et"},{3},{"ggH"}, 0.90)
                        //({"mt"},{3},{"ggH"}, 0.90)
                        //({"tt"},{3},{"ggH"}, 0.90)
                        ({"em"},{1},{"ggH"}, 1.04)
                        ({"et"},{1},{"ggH"}, 1.07)
                        ({"mt"},{1},{"ggH"}, 1.07)
                        ({"tt"},{1},{"ggH"}, 0.93)
                        
                        ({"em"},{2},{"ggH"}, 0.95)
                        ({"et"},{2},{"ggH"}, 1.04)
                        ({"mt"},{2},{"ggH"}, 0.85)
                        ({"tt"},{2},{"ggH"}, 0.82)
                        
                        
                        ({"em"},{3},{"ggH"}, 0.85)
                        ({"et"},{3},{"ggH"}, 0.80)
                        ({"mt"},{3},{"ggH"}, 0.70)
                        ({"tt"},{3},{"ggH"}, 0.60)
                        );
        
        
        
        cb.cp().AddSyst(cb, "CMS_qqH_UEPS", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"qqH"}, 1.10)
                        ({"et"},{1},{"qqH"}, 1.25)
                        ({"mt"},{1},{"qqH"}, 1.12)
                        ({"tt"},{1},{"qqH"}, 1.07)
                        
                        ({"em"},{2},{"qqH"}, 1.02)
                        ({"et"},{2},{"qqH"}, 1.07)
                        ({"mt"},{2},{"qqH"}, 1.06)
                        ({"tt"},{2},{"qqH"}, 1.09)
                        
                        
                        ({"em"},{3},{"qqH"}, 0.94)
                        ({"et"},{3},{"qqH"}, 1.06)
                        ({"mt"},{3},{"qqH"}, 1.08)
                        ({"tt"},{3},{"qqH"}, 1.08)
                        );
        
        
        
        
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
            cb.cp().process({"ZTT", "ZL", "ZJ"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_zmm_extrap_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.06));
            cb.cp().process({"ZTT", "ZL", "ZJ"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_zmm_extrap_0jet_$ERA", "lnN", SystMap<>::init(1.06));
            
            cb.cp().process({"ZTT", "ZL", "ZJ"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_zmm_extrap_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
            cb.cp().process({"ZTT", "ZL", "ZJ"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_zmm_extrap_boosted_$ERA", "lnN", SystMap<>::init(1.02));
            
            
            cb.cp().process( {"ZL","ZTT","ZJ"}).channel({"em","tt","mt","et"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_zmumuShape_VBF_$ERA", "shape", SystMap<>::init(1.00));
            
            
        }
        
        
        
        
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
            cb.cp().bin({"mt_boosted","mt_wjets_boosted_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_boosted_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_vbf","mt_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet","et_wjets_0jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted","et_wjets_boosted_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_boosted_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf","et_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            cb.cp().bin({"mt_0jet","mt_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_boosted","mt_antiiso_boosted_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_vbf","mt_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet","et_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted","et_antiiso_boosted_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_boosted_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf","et_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            
            
            //          cb.cp().bin({bin+"(|_0jet)$"}).process({"W"}).AddSyst(cb, "rate_QCD_cr_0jet_"+bin, "rateParam", SystMap<>::init(1.0));
            //          cb.cp().bin({bin+"(|_boosted)$"}).process({"W"}).AddSyst(cb, "rate_W_cr_1jet_"+bin, "rateParam", SystMap<>::init(1.0));
            //          cb.cp().bin({bin+"(|_vbf)$"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_"+bin, "rateParam", SystMap<>::init(1.0));
            
            
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
            cb.cp().bin({"tt_0jet"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_0jet"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            
            cb.cp().bin({"mt_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_boosted"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_boosted"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            
            cb.cp().bin({"mt_vbf"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"tt_vbf"}).process({"TTJ","TTT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"em_vbf"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"ttbar_all"}).process({"TT"}).AddSyst(cb, "rate_ttbar", "rateParam", SystMap<>::init(1.0));
            
            cb.GetParameter("rate_ttbar")->set_range(0.80, 1.20);
            
            cb.SetFlag("filters-use-regex", false);
        }

	//jet fakes: shape uncertainties
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "norm_ff_qcd_dm0_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "norm_ff_qcd_dm0_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "norm_ff_qcd_dm1_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "norm_ff_qcd_dm1_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_w_dm0_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_w_dm0_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_w_dm1_njet0_$CHANNEL_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_w_dm1_njet1_$CHANNEL_stat", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_tt_dm0_njet0_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_tt_dm0_njet1_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_tt_dm1_njet0_stat", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_tt_dm1_njet1_stat", "shape", SystMap<>::init(1.00));

        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "norm_ff_qcd_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_w_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"mt","et"}).AddSyst(cb, "norm_ff_tt_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "norm_ff_w_$CHANNEL_syst", "shape", SystMap<>::init(1.00));
        cb.cp().process({"jetFakes"}).channel({"tt"}).AddSyst(cb, "norm_ff_tt_$CHANNEL_syst", "shape", SystMap<>::init(1.00));

        //jet fakes: stat norm unc
	cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_norm_stat_$CHANNEL_$BIN", "lnN", SystMap<channel, bin_id>::init
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
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_norm_syst_$CHANNEL", "lnN", SystMap<channel, bin_id>::init
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
        cb.cp().process({"jetFakes"}).channel({"mt","et","tt"}).AddSyst(cb, "ff_sub_syst_$CHANNEL_$BIN", "lnN", SystMap<channel, bin_id>::init
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
