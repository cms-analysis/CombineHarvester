#include "CombineHarvester/HTTSM2016/interface/HttSystematics_SMRun2.h"
#include <vector>
#include <string>
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"

namespace ch {
    
    using ch::syst::SystMap;
    using ch::syst::SystMapAsymm;
    using ch::syst::era;
    using ch::syst::channel;
    using ch::syst::bin_id;
    using ch::syst::process;
    using ch::syst::bin;
    using ch::JoinStr;
    
    void AddSMRun2Systematics(CombineHarvester & cb, int control_region, bool mm_fit) {
        // Create a CombineHarvester clone that only contains the signal
        // categories
        CombineHarvester cb_sig = cb.cp();
        
        //  std::vector<std::string> ggH = {"ggH"};
        //  std::vector<std::string> qqH = {"qqH"};
        //    auto signal = Set2Vec(cb.cp().signals().SetFromProcs(
        //                                                         std::mem_fn(&Process::process)));
        //
        //    signal = JoinStr({signal});
        //
        //
        
        
        if (control_region == 1){
            // we only want to cosider systematic uncertainties in the signal region.
            // limit to only the 0jet/1jet and vbf categories
            cb_sig.bin_id({1,2,3,4,5,6});
        }
        
        
        vector<string> sig_procs = {"ggH","qqH","WH","ZH"};
        
        
        
        
        //  lumi
        // -----------------------
        cb.cp().process(JoinStr({signal, {"TT","VV", "ZL", "ZJ", "ZTT", "ZLL"}})).AddSyst(cb,
                                                                                          "lumi_13TeV", "lnN", SystMap<>::init(1.062));
        
        //Add luminosity uncertainty for W in em, tt and the mm region as norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","mm"}).AddSyst(cb,
                                                                 "lumi_13TeV", "lnN", SystMap<>::init(1.062));
        
        
        
        // Electron and muon efficiencies
        // ------------------------------
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mm"}, {"ZTT", "TT", "VV", "ZLL", "ZJ"},  1.02)
                        ({"mt"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ"}}),  1.02)
                        ({"tt"}, JoinStr({sig_procs, {"W"}}),  1.02)
                        ({"em"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ", "W"}}),       1.02));
        
        cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ"}}),  1.02)
                        ({"tt"}, JoinStr({sig_procs, {"W"}}),  1.02)
                        ({"em"}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ", "W"}}),       1.02));
        
        
        
        
        // Tau-related systematics
        // -----------------------
        cb.cp().process(JoinStr({sig_procs, {"ZTT,TTT,VV"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                                                                                "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<channel>::init
                                                                                                ({"et", "mt"}, 1.10)
                                                                                                ({"tt"},       1.20));
        
        // Tau Trigger ???????????????
        
        
        
        
        // Tau energy scale
        // ---------------------
        cb.cp().process(JoinStr({sig_procs, {"ZTT,TTJ"}})).channel({"et","mt","tt"}).AddSyst(cb,
                                                                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        
        // Electron energy scale
        // ---------------------
        cb.cp().process(JoinStr({sig_procs, {"ZTT"}})).channel({"em"}).AddSyst(cb,
                                                                               "CMS_scale_e_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));
        
        
        // jet energy scale
        // ---------------------
        cb.cp().process(JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ"}})).AddSyst(cb,
                                                                                        "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
        
        
        // met energy scale
        // ---------------------
        cb.cp().AddSyst(cb,
                        "CMS_htt_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
                        ({"et", "mt", "em", "tt"}, {1, 2, 3}, JoinStr({sig_procs, {"ZTT", "TT", "VV", "ZLL", "ZJ"}}), 1.01)); // FIXME  This needs to get updated
        
        
        
        
        //   Diboson  Normalisation - fully correlated
        cb.cp().process({"VV"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
        //   ttbar Normalisation - fully correlated
        cb.cp().process({"TT"}).AddSyst(cb,
                                        "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));
        
        // W norm, just for em, tt and the mm region where MC norm is from MC
        cb.cp().process({"W"}).channel({"tt","em","mm"}).AddSyst(cb,
                                                                 "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.05));
        
        // QCD norm, just for em
        cb.cp().process({"qcd"}).channel({"em"}).AddSyst(cb,
                                                                 "CMS_htt_QCD_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.30));
        
        
        // Fake-rates
        // ----------
        cb.cp().process({"ZL"}).channel({"et"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.20)); //Uncertainty ranges from 7-35% depending on eta bin
        cb.cp().process({"TTJ","ZJ"}).channel({"tt","mt","et"}).AddSyst(cb,
                                                       "CMS_htt_jetFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        
        
        
        
        
        
        
        // DY LO->NLO reweighting, Between no and twice the correc(on.
        // ---------------------
        cb.cp().process( {"ZTT","ZJ","ZLL"}).AddSyst(cb,
                                                            "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
        
        // Ttbar shape reweighting, Between no and twice the correc(on.
        // ---------------------
        cb.cp().process( {"TT","TTJ","TTT"}).AddSyst(cb,
                                                     "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
        
        // Scale uncertainty on signal Applies to ggH in boosted and VBF. Event-by-event weight applied as a func(on of pth or mjj. Fully correlated between categories and final states.
        // ---------------------
        cb.cp().process( {"ggH"}).{2, 3},AddSyst(cb,
                                                     "CMS_htt_XXXXXX_$ERA", "shape", SystMap<>::init(1.00));
        
        
        // Signal Theory uncertainty  currently just call it pdf
        cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"em"},process( {"ggH"}),{1}, 1.10)
                        ({"et"},process( {"ggH"}),{1}, 1.10)
                        ({"mt"},process( {"ggH"}),{1}, 1.10)
                        ({"tt"},process( {"ggH"}),{1}, 1.10)
                        
                        ({"em"},process( {"ggH"}),{2}, 1.20)
                        ({"et"},process( {"ggH"}),{2}, 1.20)
                        ({"mt"},process( {"ggH"}),{2}, 1.20)
                        ({"tt"},process( {"ggH"}),{2}, 1.20)
                        
                        
                        ({"em"},process( {"ggH"}),{3}, 1.50)
                        ({"et"},process( {"ggH"}),{3}, 1.40)
                        ({"mt"},process( {"ggH"}),{3}, 1.30)
                        ({"tt"},process( {"ggH"}),{3}, 1.40)
                        
                        
                        ({"em"},process( {"qqh"}),{1}, 1.10)
                        ({"et"},process( {"qqh"}),{1}, 1.10)
                        ({"mt"},process( {"qqh"}),{1}, 1.10)
                        ({"tt"},process( {"qqh"}),{1}, 1.08)
                        
                        ({"em"},process( {"qqh"}),{2}, 1.07)
                        ({"et"},process( {"qqh"}),{2}, 1.07)
                        ({"mt"},process( {"qqh"}),{2}, 1.07)
                        ({"tt"},process( {"qqh"}),{2}, 1.07)
                        
                        
                        ({"em"},process( {"qqh"}),{3}, 1.05)
                        ({"et"},process( {"qqh"}),{3}, 1.05)
                        ({"mt"},process( {"qqh"}),{3}, 1.05)
                        ({"tt"},process( {"qqh"}),{3}, 1.05)
                        
                        
                        
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
            // Add Z crosssection uncertainty on ZL, ZJ and ZLL (not ZTT due to taking into account the mm control region).
            // Also don't add it for the mm control region
            cb.SetFlag("filters-use-regex", true);
            cb.cp().channel({"mm"},false).process({"ZL", "ZJ", "ZLL"}).AddSyst(cb,
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
            cb.cp().process({"ZTT", "ZL", "ZJ", "ZLL"}).AddSyst(cb,
                                                                "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
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
            
            
            
            cb.cp().bin({"mt_0jet_low","mt_0jet_high","mt_wjets_0jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_0jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_1jet_low","mt_1jet_high","mt_wjets_1jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_1jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_vbf_low","mt_vbf_high","mt_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet_low","et_0jet_high","et_wjets_0jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_1jet_low","et_1jet_high","et_wjets_1jet_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_1jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf_low","et_vbf_high","et_wjets_vbf_cr"}).process({"W"}).AddSyst(cb, "rate_W_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            cb.cp().bin({"mt_0jet_low","mt_0jet_high","mt_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_1jet_low","mt_1jet_high","mt_antiiso_1jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_1jet_mt", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mt_vbf_low","mt_vbf_high","mt_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_mt", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"et_0jet_low","et_0jet_high","et_antiiso_0jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_0jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_1jet_low","et_1jet_high","et_antiiso_1jet_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_1jet_et", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf_low","et_vbf_high","et_antiiso_vbf_cr"}).process({"QCD"}).AddSyst(cb, "rate_QCD_cr_vbf_et", "rateParam", SystMap<>::init(1.0));
            
            
            
            //          cb.cp().bin({bin+"(|_0jet)$"}).process({"W"}).AddSyst(cb, "rate_QCD_cr_0jet_"+bin, "rateParam", SystMap<>::init(1.0));
            //          cb.cp().bin({bin+"(|_1jet)$"}).process({"W"}).AddSyst(cb, "rate_W_cr_1jet_"+bin, "rateParam", SystMap<>::init(1.0));
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
            
            cb.cp().bin({"mt_0jet_low","mt_0jet_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_0jet_low","et_0jet_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_0jet"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_0jet", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_1jet_low","mt_1jet_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_1jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_1jet_low","et_1jet_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_1jet", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_1jet"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_1jet", "rateParam", SystMap<>::init(1.0));
            
            cb.cp().bin({"mt_vbf_low","mt_vbf_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"et_vbf_low","et_vbf_high"}).process({"ZTT"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            cb.cp().bin({"mm_vbf"}).process({"ZL"}).AddSyst(cb, "rate_mm_ZTT_vbf", "rateParam", SystMap<>::init(1.0));
            
            cb.GetParameter("rate_mm_ZTT_0jet")->set_range(0.8, 1.2);
            cb.GetParameter("rate_mm_ZTT_1jet")->set_range(0.95, 1.05);
            cb.GetParameter("rate_mm_ZTT_vbf")->set_range(0.95, 1.05);
            
            cb.SetFlag("filters-use-regex", false);
        }
    }
}
