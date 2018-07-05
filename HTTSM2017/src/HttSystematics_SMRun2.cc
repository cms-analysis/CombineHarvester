#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2.h"
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
      std::vector<std::string> sig_procs = {"ggH","qqH","WH_htt","ZH_htt"};
        // N.B. when adding this list of backgrounds to a nuisance, only
        // the backgrounds that are included in the background process
        // defined in MorphingSM2017.cpp are included in the actual DCs
        // This is a list of all MC based backgrounds
        // QCD is explicitly excluded

        std::vector<std::string> all_mc_bkgs = {
            "ZL","ZJ","ZTT","TTJ","TTT","TT",
            "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
            "ggH_hww125","qqH_hww125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_truetau = {
            "ZTT","TTT","TT","VV","VVT",
            "ggH_hww125","qqH_hww125","EWKZ"};
        std::vector<std::string> all_mc_bkgs_no_W = {
            "ZL","ZJ","ZTT","TTJ","TTT","TT",
            "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
            "ggH_hww125","qqH_hww125","EWKZ"};

        //##############################################################################
        //  lumi # FIXME: Lumi is not applied to all backgrounds?
        //##############################################################################

        cb.cp().process(JoinStr({sig_procs, {"VV","VVT","VVJ","ggH_hww125","qqH_hww125"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
        cb.cp().process({"W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"}).channel({"tt"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.025));

        //Add luminosity uncertainty for W in em, tt, ttbar and the mm region as norm is from MC // FIXME: This does not make sense anymore.
        cb.cp().process({"W"}).channel({"tt","em","mm","ttbar"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));

        cb.cp().process({"TTT","TTJ"}).AddSyst(cb,"lumi_13TeV", "lnN", SystMap<>::init(1.025));

        //##############################################################################
        //  trigger   ##FIXME   the values have been chosen rather arbitrarily # FIXME: What does this mean?
        //##############################################################################

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"mt"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_W})).channel({"et"}).AddSyst(cb,
                                             "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em","ttbar"}).AddSyst(cb,
                                             "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));

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
        // FIXME: Do we need these?
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
        // Decay Mode based TES Settings
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_truetau})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_truetau})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_truetau})).channel({"et","mt","tt"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        //  jet and met energy Scale
        //##############################################################################

        // MET Systematic shapes
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt","em"}).bin_id({1,2,3}).AddSyst(cb,
                                                  "CMS_scale_met_clustered_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt","em"}).bin_id({1,2,3}).AddSyst(cb,
                                                  "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));


        // Standard JES
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,
						           "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));

        // JES factorization in 27 shapes
        /*
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

        for (string uncert:uncertNames){
         cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt","mt", "et"}).AddSyst(cb,
         "CMS_scale_j_"+uncert+"_$ERA", "shape", SystMap<>::init(1.00));
         }
         */

        //##############################################################################
        //  Background normalization uncertainties
        //##############################################################################

        //   Diboson  Normalisation - fully correlated
        cb.cp().process({"VV","VVT","VVJ","VVJ_rest"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
        //   ttbar Normalisation - fully correlated
	    cb.cp().process({"TT","TTT","TTJ","TTJ_rest"}).AddSyst(cb,
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));

        // W norm, just for em, tt and the mm region where MC norm is from MC // FIXME: This needs to be done everywhere.
        cb.cp().process({"W"}).channel({"em"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeLep_13TeV", "lnN", SystMap<>::init(1.20));

        cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));


        // QCD norm, just for em  decorrelating QCD BG for differenet categories

        // QCD norm, just for tt // FIXME: Does not fit for our analysis.
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"QCD"}).channel({"em"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));


        // QCD norm, just for tt // FIXME: Does not fit for our analysis.
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({1}).AddSyst(cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.027));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({2}).AddSyst(cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.027));
        cb.cp().process({"QCD"}).channel({"tt"}).bin_id({3}).AddSyst(cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.15));


        // Iso to antiiso extrapolation
        cb.cp().process({"QCD"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.20));
        cb.cp().process({"QCD"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.20));


        //This should affect only shape (normalized to nominal values)
	/* MISSING SO FAR # FIXME: What does this mean?
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_0jet_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_boosted_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process({"QCD"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "WSFUncert_$CHANNEL_vbf_$ERA", "shape", SystMap<>::init(1.00));
	*/


        // based on the Ersatz study in Run1 // FIXME: This is still correct?
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,
                                             "WHighMTtoLowMT_0jet_$ERA", "lnN", SystMap<>::init(1.10));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,
                                             "WHighMTtoLowMT_boosted_$ERA", "lnN", SystMap<>::init(1.05));
        cb.cp().process({"W"}).channel({"et","mt"}).bin_id({3}).AddSyst(cb,
                                             "WHighMTtoLowMT_vbf_$ERA", "lnN", SystMap<>::init(1.10));

        //##############################################################################
        //  DY LO->NLO reweighting, Between no and twice the correction.
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
        // ZL shape  and electron/muon  to tau fake only in  mt and et channels
        //##############################################################################

        cb.cp().process( {"ZL"}).channel({"mt","et"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"mt","et"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));


        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_mFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"mt"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_mFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_eFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process( {"ZL"}).channel({"et"}).bin_id({1,2,3}).AddSyst(cb,
                                                                     "CMS_eFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // jet  to tau fake only in tt, mt and et channels
        //##############################################################################

        cb.cp().process( {"TTJ","ZJ","VVJ","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"}).channel({"tt","mt","et"}).AddSyst(cb,
                                                                            "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));

        // FIXME: This does not make sense anymore?
        cb.cp().process( {"W"}).channel({"tt","mt","et"}).bin_id({1,2,3,13,14,15}).AddSyst(cb,
                                                                "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // Theoretical Uncertainties on signal
        //##############################################################################

        //scale_gg on signal // FIXME: We don't have this. Should we use the log-normal uncertainties below?
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


        /* // FIXME: What is that?
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
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_THU", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_PU_mq", "lnN", SystMap<>::init(1.0099));
        cb.cp().process({"ggH_hww125","qqH_hww125"}).AddSyst(cb,"BR_hww_PU_alphas", "lnN", SystMap<>::init(1.0066));


        cb.cp().process({"ggH","ggH_hww125"}).AddSyst(cb,"QCDScale_ggH", "lnN", SystMap<>::init(1.039));
        cb.cp().process({"qqH","qqH_hww125"}).AddSyst(cb,"QCDScale_qqH", "lnN", SystMap<>::init(1.004));
        cb.cp().process({"WH_htt"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.007));
        cb.cp().process({"ZH_htt"}).AddSyst(cb,"QCDScale_VH", "lnN", SystMap<>::init(1.038));

        cb.cp().process({"ggH","ggH_hww125"}).AddSyst(cb,"pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
        cb.cp().process({"qqH","qqH_hww125"}).AddSyst(cb,"pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
        cb.cp().process({"WH_htt"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.019));
        cb.cp().process({"ZH_htt"}).AddSyst(cb,"pdf_Higgs_VH", "lnN", SystMap<>::init(1.016));

        //   Additonal uncertainties applied to the paper i.e. top mass // FIXME: What is this doing?
        cb.cp().process( {"ggH"}).channel({"et","mt","em","tt"}).AddSyst(cb,
                                                                         "TopMassTreatment_$ERA", "shape", SystMap<>::init(1.00));

        // FIXME: What does the *_STXSmig* uncertainties do?
        cb.cp().AddSyst(cb, "CMS_ggH_STXSmig01", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 0.959)
                        ({"et"},{1},{"ggH"}, 0.959)
                        ({"mt"},{1},{"ggH"}, 0.959)
                        ({"tt"},{1},{"ggH"}, 0.959)

                        ({"em"},{2},{"ggH"}, 1.079)
                        ({"et"},{2},{"ggH"}, 1.079)
                        ({"mt"},{2},{"ggH"}, 1.079)
                        ({"tt"},{2},{"ggH"}, 1.079)

                        ({"em"},{3},{"ggH"}, 1.039)
                        ({"et"},{3},{"ggH"}, 1.039)
                        ({"mt"},{3},{"ggH"}, 1.039)
                        ({"tt"},{3},{"ggH"}, 1.039)
                        );

        cb.cp().AddSyst(cb, "CMS_ggH_STXSmig12", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 1.000)
                        ({"et"},{1},{"ggH"}, 1.000)
                        ({"mt"},{1},{"ggH"}, 1.000)
                        ({"tt"},{1},{"ggH"}, 1.000)

                        ({"em"},{2},{"ggH"}, 0.932)
                        ({"et"},{2},{"ggH"}, 0.932)
                        ({"mt"},{2},{"ggH"}, 0.932)
                        ({"tt"},{2},{"ggH"}, 0.932)

                        ({"em"},{3},{"ggH"}, 1.161)
                        ({"et"},{3},{"ggH"}, 1.161)
                        ({"mt"},{3},{"ggH"}, 1.161)
                        ({"tt"},{3},{"ggH"}, 1.161)
                        );

        cb.cp().AddSyst(cb, "CMS_ggH_STXSVBF2j", "lnN", SystMap<channel, bin_id, process>::init
                        ({"em"},{1},{"ggH"}, 1.000)
                        ({"et"},{1},{"ggH"}, 1.000)
                        ({"mt"},{1},{"ggH"}, 1.000)
                        ({"tt"},{1},{"ggH"}, 1.000)

                        ({"em"},{2},{"ggH"}, 1.000)
                        ({"et"},{2},{"ggH"}, 1.000)
                        ({"mt"},{2},{"ggH"}, 1.000)
                        ({"tt"},{2},{"ggH"}, 1.000)

                        ({"em"},{3},{"ggH"}, 1.200)
                        ({"et"},{3},{"ggH"}, 1.200)
                        ({"mt"},{3},{"ggH"}, 1.200)
                        ({"tt"},{3},{"ggH"}, 1.200)
                        );

        //  // Recoil corrections // FIXME: Why this is not used?
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

            // Z->mumu CR normalization propagation // FIXME: This does not make sense anymore
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

//            // FIXME should have EWKZ in all // FIXME: This is important for us?
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
} // namespace ch
