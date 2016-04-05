#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
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
using ch::JoinStr;


void AddMSSMRun2Systematics(CombineHarvester & cb, int control_region = 0) {
  CombineHarvester src = cb.cp();

  if (control_region == 1){
    // we only want to cosider systematic uncertainties in the signal region.
    // limit to only the btag and nobtag categories
    src.bin_id({8,9});
  }

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().process(ch::JoinStr({signal, {"ZTT", "TT","VV","W"}})).channel({"em","mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  src.cp().process(ch::JoinStr({signal, {"ZLL"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  src.cp().process(ch::JoinStr({signal, {"ZL","ZJ"}})).channel({"mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));


  src.cp().process(ch::JoinStr({signal, {"TT","VV","ZLL","ZTT","W"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  src.cp().process(ch::JoinStr({signal, {"TT","VV","ZL","ZJ","ZTT","W"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  /*src.cp().process(ch::JoinStr({signal, {"TT","VV","ZL","ZJ","ZTT","W"}}))
      .AddSyst(cb, "CMS_scale_j_13TeV", "shape", SystMap<>::init(1.00));*/

  src.cp()
    .AddSyst(cb,
      "CMS_scale_j_13TeV","lnN",SystMapAsymm<channel,bin_id,process>::init
       ({"mt"},{8}, {"TT"}, 1.014,0.986)
       ({"mt"},{8}, {"bbH"}, 1.01,0.99)
       ({"mt"},{9}, {"W"}, 0.1,2.08) // changed the lower one from 0.0 to 0.1
       ({"mt"},{9}, {"QCD"}, 1.027,0.975)
       ({"mt"},{9}, {"ZL"}, 0.97,0.91)
       ({"mt"},{9}, {"ZJ"}, 0.968,0.960)
       ({"mt"},{9}, {"ZTT"}, 0.969,1.026)
       ({"mt"},{9}, {"TT"}, 1.092,0.917)
       ({"mt"},{9}, {"VV"}, 1.0415,0.979)
       ({"mt"},{9}, {"ggH"}, 1,0.94)
       ({"mt"},{9}, {"bbH"}, 1.02,0.98)
       ({"et"},{8}, {"TT"}, 1.013,0.987)
       ({"et"},{8}, {"bbH"}, 1.01,0.99)
       ({"et"},{9}, {"W"}, 0.687,1.298)
       ({"et"},{9}, {"QCD"}, 1.013,0.986)
       ({"et"},{9}, {"ZL"}, 0.983,1.028)
       ({"et"},{9}, {"ZJ"}, 1.001,1.112)
       ({"et"},{9}, {"ZTT"}, 0.989,1.015)
       ({"et"},{9}, {"VV"}, 1.037,0.955)
       ({"et"},{9}, {"TT"}, 1.0978,0.9112)
       ({"et"},{9}, {"ggH"}, 1.06,0.96)
       ({"et"},{9}, {"ggH"}, 0.98,1)
       ({"em"},{8}, {"TT"}, 1.015,0.986)
       ({"em"},{8}, {"bbH"}, 1.01,0.99)
       ({"em"},{8}, {"ggH"}, 1,1)
       ({"em"},{9}, {"W"}, 0.879,0.965)
       ({"em"},{9}, {"QCD"}, 0.979,0.984)
       ({"em"},{9}, {"ZLL"}, 1.2811,1.018)
       ({"em"},{9}, {"ZTT"}, 0.9965,1.0292)
       ({"em"},{9}, {"VV"}, 1.0359,0.9618)
       ({"em"},{9}, {"TT"}, 1.0808,0.9202)
       ({"em"},{9}, {"ggH"}, 1.01,0.99)
       ({"em"},{9}, {"bbH"}, 0.98,1.02)
       ({"tt"},{8}, {"W"}, 1,0.969)
       ({"tt"},{8}, {"ZL"}, 1.01,0.99)
       ({"tt"},{8}, {"ZJ"}, 1.01,0.99)
       ({"tt"},{8}, {"ZTT"}, 1.01,0.99)
       ({"tt"},{8}, {"VV"}, 1.01,0.97)
       ({"tt"},{8}, {"TT"}, 1.04,0.96)
       ({"tt"},{8}, {"ggH"}, 1.01,0.99)
       ({"tt"},{8}, {"bbH"}, 1.02,0.98)
       ({"tt"},{9}, {"W"}, 1.06,1.23)
       ({"tt"},{9}, {"QCD"}, 1.004,1.009)
       ({"tt"},{9}, {"ZL"}, 0.91,1.12)
       ({"tt"},{9}, {"ZJ"}, 1.16,1.11)
       ({"tt"},{9}, {"ZTT"}, 0.96,1.04)
       ({"tt"},{9}, {"VV"}, 1.05,1.08)
       ({"tt"},{9}, {"TT"}, 1.08,0.92)
       ({"tt"},{9}, {"bbH"}, 0.98,1.04)
       ({"tt"},{9}, {"ggH"}, 0.98,1.02));

  src.cp()
    .AddSyst(cb,
      "CMS_eff_b_13TeV","lnN",SystMapAsymm<channel,bin_id,process>::init
       ({"mt"},{8}, {"W"}, 0.99,1.01)
       ({"mt"},{8}, {"VV"}, 1.01,0.99)
       ({"mt"},{8}, {"TT"}, 1.06,0.95)
       ({"mt"},{8}, {"bbH"}, 1.01,0.99)
       ({"mt"},{9}, {"W"}, 1.41,0.62)
       ({"mt"},{9}, {"QCD"}, 0.99,1.01)
       ({"mt"},{9}, {"ZL"}, 0.98,1.02)
       ({"mt"},{9}, {"ZJ"}, 0.97,1.01)
       ({"mt"},{9}, {"ZTT"}, 0.97,1.03)
       ({"mt"},{9}, {"VV"}, 0.98,1.03)
       ({"mt"},{9}, {"TT"}, 0.98,1.02)
       ({"mt"},{9}, {"ggH"}, 0.98,1)
       ({"mt"},{9}, {"bbH"}, 0.97,1.04)
       ({"et"},{8}, {"W"}, 0.99,1.01)
       ({"et"},{8}, {"VV"}, 1.01,0.99)
       ({"et"},{8}, {"TT"}, 1.05,0.95)
       ({"et"},{8}, {"bbH"}, 1.01,0.99)
       ({"et"},{9}, {"W"}, 1.19,0.91)
       ({"et"},{9}, {"QCD"}, 0.99,1)
       ({"et"},{9}, {"ZL"}, 0.99,1.03)
       ({"et"},{9}, {"ZJ"}, 0.96,1.3)
       ({"et"},{9}, {"ZTT"}, 0.96,1.03)
       ({"et"},{9}, {"VV"}, 0.97,1.03)
       ({"et"},{9}, {"TT"}, 0.98,1.02)
       ({"et"},{9}, {"ggH"}, 0.96,1.03)
       ({"et"},{9}, {"bbH"}, 0.98,1.03)
       ({"em"},{8}, {"VV"}, 1.01,0.99)
       ({"em"},{8}, {"TT"}, 1.06,0.95)
       ({"em"},{8}, {"bbH"}, 1.01,0.99)
       ({"em"},{9}, {"QCD"}, 1.06,0.99)
       ({"em"},{9}, {"ZLL"}, 0.98,1)
       ({"em"},{9}, {"ZTT"}, 0.97,1.03)
       ({"em"},{9}, {"VV"}, 0.98,1.02)
       ({"em"},{9}, {"TT"}, 0.98,1.02)
       ({"em"},{9}, {"ggH"}, 0.97,1.03)
       ({"em"},{9}, {"bbH"}, 0.97,1.03)
       ({"tt"},{8}, {"W"}, 1,0.99)
       ({"tt"},{8}, {"ZL"}, 1.01,0.99)
       ({"tt"},{8}, {"TT"}, 1.03,0.92)
       ({"tt"},{8}, {"bbH"}, 1.01,0.99)
       ({"tt"},{9}, {"W"}, 1,1.1)
       ({"tt"},{9}, {"ZL"}, 0.93,1.03)
       ({"tt"},{9}, {"ZTT"}, 0.99,1.01)
       ({"tt"},{9}, {"TT"}, 0.99,1.01)
       ({"tt"},{9}, {"bbH"}, 0.98,1.02));


  src.cp()
    .AddSyst(cb,
      "CMS_fake_b_13TeV","lnN",SystMapAsymm<channel,bin_id,process>::init
       ({"mt"},{9}, {"W"}, 1.01,1.00)
       ({"mt"},{9}, {"ZL"}, 0.995,1.03)
       ({"mt"},{9}, {"ZJ"}, 0.96,1.02)
       ({"mt"},{9}, {"ZTT"}, 0.99,1.01)
       ({"mt"},{9}, {"ggH"}, 0.97,1.03)
       ({"et"},{9}, {"ZL"}, 0.99,1)
       ({"et"},{9}, {"ZL"}, 0.95,1.02)
       ({"et"},{9}, {"ZTT"}, 0.99,1.01)
       ({"em"},{9}, {"ZTT"}, 0.99,1.01)
       ({"em"},{9}, {"ggH"}, 0.97,1.04)
       ({"tt"},{8}, {"TT"}, 1.01,0.998)
       ({"tt"},{8}, {"ggH"}, 1.01,0.99)
       ({"tt"},{9}, {"ZL"}, 0.96,1.03)
       ({"tt"},{9}, {"ZTT"}, 0.98,1.03)
       ({"tt"},{9}, {"VV"}, 1.01,1.03)
       ({"tt"},{9}, {"ggH"}, 0.97,1.03));
/*  src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"em"})
      .AddSyst(cb, "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));*/

 src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"})
      .AddSyst(cb, "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

 src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"em"})
      .AddSyst(cb, "CMS_scale_e_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

 src.cp().process({"TT","VV","ZL","W","ZJ","ZTT","ZLL"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.027));

 src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

 src.cp().process(signal).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.027));

 src.cp().channel({"em"}).process({"ZLL"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

 src.cp().channel({"et","tt","mt"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));


 // Diboson and ttbar Normalisation - fully correlated
 src.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.15));

 src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_13TeV", "lnN", SystMap<era>::init
        ({"13TeV"}, 1.10));


  if (control_region == 0 || control_region == 1) {
    // the uncertainty model in the signal region is the classical one
    // QCD Normalisation - separate nuisance for each channel/category
    // TODO: one function call?
    src.cp().process({"QCD"}).channel({"mt"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_QCDNorm_mt_nobtag_13TeV","lnN",SystMap<>::init(1.1));

    src.cp().process({"QCD"}).channel({"mt"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_QCDNorm_mt_btag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"QCD"}).channel({"et"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_QCDNorm_et_nobtag_13TeV","lnN",SystMap<>::init(1.1));

    src.cp().process({"QCD"}).channel({"et"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_QCDNorm_et_btag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"QCD"}).channel({"tt"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_QCDNorm_tt_nobtag_13TeV","lnN",SystMap<>::init(1.35));

    src.cp().process({"QCD"}).channel({"tt"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_QCDNorm_tt_btag_13TeV","lnN",SystMap<>::init(1.35));

    src.cp().process({"QCD"}).channel({"em"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_QCDNorm_em_nobtag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"QCD"}).channel({"em"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_QCDNorm_em_btag_13TeV","lnN",SystMap<>::init(1.3));
        src.cp().process({"W"}).channel({"mt"}).AddSyst(cb,
            "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.2));

    // W Normalisation - separate nuisance for each channel/category
    // TODO: one function call?
    src.cp().process({"W"}).channel({"mt"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_WNorm_mt_nobtag_13TeV","lnN",SystMap<>::init(1.1));

    src.cp().process({"W"}).channel({"mt"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_WNorm_mt_btag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"W"}).channel({"et"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_WNorm_et_nobtag_13TeV","lnN",SystMap<>::init(1.1));

    src.cp().process({"W"}).channel({"et"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_WNorm_et_btag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"W"}).channel({"tt"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_WNorm_tt_nobtag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"W"}).channel({"tt"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_WNorm_tt_btag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"W"}).channel({"em"}).bin_id({8}).AddSyst(cb,
        "CMS_htt_WNorm_em_nobtag_13TeV","lnN",SystMap<>::init(1.3));

    src.cp().process({"W"}).channel({"em"}).bin_id({9}).AddSyst(cb,
        "CMS_htt_WNorm_em_btag_13TeV","lnN",SystMap<>::init(1.3));
    }
    if (control_region == 1 || control_region == 2) {
      // Create rateParams for control regions:
      //  - [x] 1 rateParam for all W in every region
      //  - [x] 1 rateParam for QCD in low mT
      //  - [x] 1 rateParam for QCD in high mT
      //  - [ ] lnNs for the QCD OS/SS ratio
      //         * should account for stat + syst
      //         * systs should account for: extrap. from anti-iso to iso region,
      //           possible difference between ratio in low mT and high mT (overkill?)
      //  - [ ] lnNs for the W+jets OS/SS ratio
      //         * should account for stat only if not being accounted for with bbb,
      //           i.e. because the OS/SS ratio was measured with a relaxed selection
      //         * systs should account for: changes in low/high mT and OS/SS due to JES
      //           and btag (if relevant); OS/SS being wrong in the MC (from enriched data?);
      //           low/high mT being wrong in the MC (fake rate dependence?)

      // Going to use the regex filtering to select the right subset of
      // categories for each rateParam
      cb.SetFlag("filters-use-regex", true);
      for (auto bin : src.cp().channel({"et", "mt"}).bin_id({8, 9}).bin_set()) {
        // Regex that matches, e.g. mt_nobtag or mt_nobtag_X
        cb.cp().bin({bin+"(|_.*)$"}).process({"W"}).AddSyst(cb,
          "rate_W_"+bin, "rateParam", SystMap<>::init(1.0));

        // Regex that matches, e.g. mt_nobtag or mt_nobtag_qcd_cr
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"QCD"}).AddSyst(cb,
          "rate_QCD_lowmT_"+bin, "rateParam", SystMap<>::init(1.0));

        // Regex that matches, e.g. mt_nobtag_wjets_cr or mt_nobtag_wjets_ss_cr
        cb.cp().bin({bin+"_wjets(|_ss)_cr$"}).process({"QCD"}).AddSyst(cb,
          "rate_QCD_highmT_"+bin, "rateParam", SystMap<>::init(1.0));
      }
      // Should set a sensible range for our rateParams
      for (auto sys : cb.cp().syst_type({"rateParam"}).syst_name_set()) {
        cb.GetParameter(sys)->set_range(0.0, 2.0);
      }
      cb.SetFlag("filters-use-regex", false);
    }
    if (control_region == 2) {
      // add the systematic on W+Jets and QCD in the signal region to account for scale factor uncertainties
      src.cp().process({"QCD"}).channel({"et","em","tt","mt"}).bin_id({8,9}).AddSyst(cb,
          "CMS_htt_QCD_13TeV","lnN",SystMap<>::init(1.2));
      src.cp().process({"W"}).channel({"mt"}).bin_id({8,9}).AddSyst(cb,
          "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.1));
    }
  }
}
