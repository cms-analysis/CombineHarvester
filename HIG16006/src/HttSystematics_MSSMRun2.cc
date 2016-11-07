#include "CombineHarvester/HIG16006/interface/HttSystematics_MSSMRun2.h"
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

void AddMSSMRun2Systematics(CombineHarvester & cb, int control_region = 0) {
  // Create a CombineHarvester clone that only contains the signal
  // categories
  CombineHarvester cb_sig = cb.cp();

  std::vector<std::string> ggH = {"ggH", "ggH_Htautau", "ggA_Atautau", "ggh_htautau"};
  std::vector<std::string> bbH = {"bbH", "bbH_Htautau", "bbA_Atautau", "bbh_htautau"};

  if (control_region == 1){
    // we only want to cosider systematic uncertainties in the signal region.
    // limit to only the btag and nobtag categories
    cb_sig.bin_id({8,9});
  }

  std::vector<std::string> SM_procs = {"ggH_SM125", "qqH_SM125", "ZH_SM125", "WminusH_SM125","WplusH_SM125"};

  auto signal = Set2Vec(cb.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  signal = JoinStr({signal,SM_procs});

  //SM theory uncertainties
  cb.cp().process({"ggH_SM125"}).AddSyst(cb, "QCDscale_ggH", "lnN",
    SystMapAsymm<>::init(1.076,0.919));

  cb.cp().process({"qqH_SM125"}).AddSyst(cb, "QCDscale_qqH", "lnN",
    SystMapAsymm<>::init(1.004,0.997));


  cb.cp().process({"ZH_SM125","WplusH_SM125","WminusH_SM125"}).AddSyst(cb, "QCDscale_VH", "lnN",
    SystMapAsymm<process>::init
     ({"ZH_SM125"}, 1.038, 0.969)
     ({"WplusH_SM125","WminusH_SM125"},1.005,0.993));

/*  cb.cp().process({"TTH_SM125"}).AddSyst(cb,"QCDscale_ttH","lnN", 
    SystMapAsymm<>::init(1.058,0.908));*/

  cb.cp().process({"ggH_SM125"}).AddSyst(cb, "pdf_Higgs_gg","lnN",
    SystMap<>::init(1.031));

/*  cb.cp().process({"TTH_SM125"}).AddSyst(cb, "pdf_Higgs_ttH","lnN",
    SystMap<>::init(1.036));*/

  cb.cp().process({"ZH_SM125","WplusH_SM125","WminusH_SM125","qqH_SM125"}).AddSyst(cb, "pdf_Higgs_qqbar","lnN",
    SystMap<process>::init
      ({"ZH_SM125"},1.016)
      ({"WplusH_SM125","WminusH_SM125"},1.019)
      ({"qqH_SM125"},1.021)); 
    

  // Electron and muon efficiencies
  // ------------------------------
  cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
    ({"mt"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZL", "ZJ"}}),  1.02)
    ({"em"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZLL"}}),       1.02));
  
  cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
    ({"et"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZL", "ZJ"}}),  1.02)
    ({"em"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZLL"}}),       1.02));

  /*src.cp().process(ch::JoinStr({signal, {"TT","VV","ZL","ZJ","ZTT","W"}}))
      .AddSyst(cb, "CMS_scale_j_13TeV", "shape", SystMap<>::init(1.00));*/

  // Jet energy scale
  // ----------------
  cb.cp().AddSyst(cb,
    "CMS_scale_j_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    ({"mt"}, {8}, {"TT"},   1.014,  0.986)
    ({"mt"}, {8}, {bbH},  1.01 ,  0.990)
    ({"mt"}, {9}, {"ZL"},   0.97 ,  0.91)
    ({"mt"}, {9}, {"ZJ"},   0.968,  0.960)
    ({"mt"}, {9}, {"ZTT"},  0.969,  1.026)
    ({"mt"}, {9}, {"TT"},   1.092,  0.917)
    ({"mt"}, {9}, {"VV"},   1.0415, 0.979)
    ({"mt"}, {9}, {ggH},  1,      0.94)
    ({"mt"}, {9}, {bbH},  1.02,   0.98)
    ({"et"}, {8}, {"TT"},   1.013,  0.987)
    ({"et"}, {8}, {bbH},  1.01,   0.99)
    ({"et"}, {9}, {"ZL"},   0.983,  1.028)
    ({"et"}, {9}, {"ZJ"},   1.001,  1.112)
    ({"et"}, {9}, {"ZTT"},  0.989,  1.015)
    ({"et"}, {9}, {"VV"},   1.037,  0.955)
    ({"et"}, {9}, {"TT"},   1.0978, 0.9112)
    ({"et"}, {9}, {ggH},  1.06,   0.96)
    ({"et"}, {9}, {ggH},  0.98,   1)
    ({"em"}, {8}, {"TT"},   1.015,  0.986)
    ({"em"}, {8}, {bbH},  1.01,   0.99)
    ({"em"}, {8}, {ggH},  1,      1)
    ({"em"}, {9}, {"W"},    0.879,  0.965)
    ({"em"}, {9}, {"QCD"},  0.979,  0.984)
    ({"em"}, {9}, {"ZLL"},  1.2811, 1.018)
    ({"em"}, {9}, {"ZTT"},  0.9965, 1.0292)
    ({"em"}, {9}, {"VV"},   1.0359, 0.9618)
    ({"em"}, {9}, {"TT"},   1.0808, 0.9202)
    ({"em"}, {9}, {ggH},  1.01,   0.99)
    ({"em"}, {9}, {bbH},  0.98,   1.02)
    ({"tt"}, {8}, {"W"},    1,      0.969)
    ({"tt"}, {8}, {"ZL"},   1.01,   0.99)
    ({"tt"}, {8}, {"ZJ"},   1.01,   0.99)
    ({"tt"}, {8}, {"ZTT"},  1.01,   0.99)
    ({"tt"}, {8}, {"VV"},   1.01,   0.97)
    ({"tt"}, {8}, {"TT"},   1.04,   0.96)
    ({"tt"}, {8}, {ggH},  1.01,   0.99)
    ({"tt"}, {8}, {bbH},  1.02,   0.98)
    ({"tt"}, {9}, {"W"},    1.06,   1.23)
    ({"tt"}, {9}, {"QCD"},  1.004,  1.009)
    ({"tt"}, {9}, {"ZL"},   0.91,   1.12)
    ({"tt"}, {9}, {"ZJ"},   1.16,   1.11)
    ({"tt"}, {9}, {"ZTT"},  0.96,   1.04)
    ({"tt"}, {9}, {"VV"},   1.05,   1.08)
    ({"tt"}, {9}, {"TT"},   1.08,   0.92)
    ({"tt"}, {9}, {bbH},  0.98,   1.04)
    ({"tt"}, {9}, {ggH},  0.98,   1.02));

  // b-tagging efficiency and fake rate
  // ----------------------------------
  cb.cp().AddSyst(cb,
    "CMS_eff_b_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    // ({"mt"},{8}, {"W"}, 0.99,1.01)
    ({"mt"}, {8}, {"VV"},   1.01,   0.99)
    ({"mt"}, {8}, {"TT"},   1.06,   0.95)
    ({"mt"}, {8}, {bbH},  1.01,   0.99)
    // ({"mt"},{9}, {"W"}, 1.41,0.62)
    // ({"mt"},{9}, {"QCD"}, 0.99,1.01)
    ({"mt"}, {9}, {"ZL"},   0.98,   1.02)
    ({"mt"}, {9}, {"ZJ"},   0.97,   1.01)
    ({"mt"}, {9}, {"ZTT"},  0.97,   1.03)
    ({"mt"}, {9}, {"VV"},   0.98,   1.03)
    ({"mt"}, {9}, {"TT"},   0.98,   1.02)
    ({"mt"}, {9}, {ggH},  0.98,   1)
    ({"mt"}, {9}, {bbH},  0.97,   1.04)
    // ({"et"},{8}, {"W"}, 0.99,1.01)
    ({"et"}, {8}, {"VV"},   1.01,   0.99)
    ({"et"}, {8}, {"TT"},   1.05,   0.95)
    ({"et"}, {8}, {bbH},  1.01,   0.99)
    // ({"et"},{9}, {"W"}, 1.19,0.91)
    // ({"et"},{9}, {"QCD"}, 0.99,1)
    ({"et"}, {9}, {"ZL"},   0.99,   1.03)
    ({"et"}, {9}, {"ZJ"},   0.96,   1.3)
    ({"et"}, {9}, {"ZTT"},  0.96,   1.03)
    ({"et"}, {9}, {"VV"},   0.97,   1.03)
    ({"et"}, {9}, {"TT"},   0.98,   1.02)
    ({"et"}, {9}, {ggH},  0.96,   1.03)
    ({"et"}, {9}, {bbH},  0.98,   1.03)
    ({"em"}, {8}, {"VV"},   1.01,   0.99)
    ({"em"}, {8}, {"TT"},   1.06,   0.95)
    ({"em"}, {8}, {"bbH"},  1.01,   0.99)
    ({"em"}, {9}, {"QCD"},  1.06,   0.99)
    ({"em"}, {9}, {"ZLL"},  0.98,   1)
    ({"em"}, {9}, {"ZTT"},  0.97,   1.03)
    ({"em"}, {9}, {"VV"},   0.98,   1.02)
    ({"em"}, {9}, {"TT"},   0.98,   1.02)
    ({"em"}, {9}, {ggH},  0.97,   1.03)
    ({"em"}, {9}, {bbH},  0.97,   1.03)
    ({"tt"}, {8}, {"W"},    1,      0.99)
    ({"tt"}, {8}, {"ZL"},   1.01,   0.99)
    ({"tt"}, {8}, {"TT"},   1.03,   0.92)
    ({"tt"}, {8}, {bbH},  1.01,   0.99)
    ({"tt"}, {9}, {"W"},    1,      1.1)
    ({"tt"}, {9}, {"ZL"},   0.93,   1.03)
    ({"tt"}, {9}, {"ZTT"},  0.99,   1.01)
    ({"tt"}, {9}, {"TT"},   0.99,   1.01)
    ({"tt"}, {9}, {bbH},  0.98,   1.02));


  cb.cp().AddSyst(cb,
    "CMS_fake_b_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    ({"mt"}, {9}, {"W"},    1.01,   1.00)
    ({"mt"}, {9}, {"ZL"},   0.995,  1.03)
    ({"mt"}, {9}, {"ZJ"},   0.96,   1.02)
    ({"mt"}, {9}, {"ZTT"},  0.99,   1.01)
    ({"mt"}, {9}, {ggH},  0.97,   1.03)
    ({"et"}, {9}, {"ZL"},   0.99,   1)
    ({"et"}, {9}, {"ZL"},   0.95,   1.02)
    ({"et"}, {9}, {"ZTT"},  0.99,   1.01)
    ({"em"}, {9}, {"ZTT"},  0.99,   1.01)
    ({"em"}, {9}, {ggH},  0.97,   1.04)
    ({"tt"}, {8}, {"TT"},   1.01,   0.998)
    ({"tt"}, {8}, {ggH},  1.01,   0.99)
    ({"tt"}, {9}, {"ZL"},   0.96,   1.03)
    ({"tt"}, {9}, {"ZTT"},  0.98,   1.03)
    ({"tt"}, {9}, {"VV"},   1.01,   1.03)
    ({"tt"}, {9}, {ggH},  0.97,   1.03));

  // Tau-related systematics
  // -----------------------
  cb.cp().process(JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_$ERA", "lnN", SystMap<channel>::init
    ({"et", "mt"}, 1.05)
    ({"tt"},       1.10));

  cb.cp().process(JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<channel>::init
    ({"et", "mt"}, 1.03)
    ({"tt"},       1.092));

  cb.cp().process(JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_mssmHigh_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp().process(JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp().process(JoinStr({{"ZTT"}})).channel({"et","mt","tt", "em"}).AddSyst(cb,
    "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));

  // Electron energy scale
  // ---------------------
  cb.cp().process(JoinStr({signal, {"ZTT"}})).channel({"em"}).AddSyst(cb,
    "CMS_scale_e_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

  // Recoil corrections
  // ------------------
  // These should not be applied to the W in all control regions becasuse we should
  // treat it as an uncertainty on the low/high mT factor.
  // For now we also avoid applying this to any of the high-mT control regions
  // as the exact (anti-)correlation with low mT needs to be established
  cb.cp().AddSyst(cb,
    "CMS_htt_boson_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, JoinStr({signal, {"ZTT", "W"}}), 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_boson_reso_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, JoinStr({signal, {"ZTT", "W"}}), 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_ewkTop_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, {"TT", "VV"}, 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_ewkTop_reso_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, {"TT", "VV"}, 1.02));

  // top-quark pT reweighting
  // ------------------------
  cb.cp().process({"TT"}).AddSyst(cb,
    "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));

  // Cross-sections and lumi
  // -----------------------
  cb.cp().process(JoinStr({signal, {"TT", "VV", "ZL", "ZJ", "ZTT", "ZLL"}})).AddSyst(cb,
    "lumi_13TeV", "lnN", SystMap<>::init(1.027));

  cb.cp().process({"ZTT", "ZL", "ZJ", "ZLL"}).AddSyst(cb,
    "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));

  // Diboson and ttbar Normalisation - fully correlated
  cb.cp().process({"VV"}).AddSyst(cb,
    "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"TT"}).AddSyst(cb,
    "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));
  
  // W norm, just for em and tt where MC norm is from MC
  cb.cp().process({"W"}).channel({"tt","em"}).AddSyst(cb,
    "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));

  // Category-acceptance
  // -------------------
  // For ZTT use 5% run 1 value for now, should be replaced based
  // on Z->mumu calibration. Also only apply this to signal-region
  // categories for now, using cb_sig instead of cb
  cb_sig.cp().process({"ZTT"}).AddSyst(cb,
    "CMS_htt_zttAccept_$BIN_13TeV", "lnN", SystMap<bin_id>::init
    ({8}, 1.03)
    ({9}, 1.05));
  // Should also add something for ttbar

  // Fake-rates
  // ----------
  cb.cp().process({"ZL"}).channel({"et"}).AddSyst(cb,
    "CMS_htt_eFakeTau_tight_13TeV", "lnN", SystMap<>::init(1.30));

  cb.cp().process({"ZL"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_eFakeTau_loose_13TeV", "lnN", SystMap<>::init(1.10));

  cb.cp().channel({"et", "mt", "tt"}).AddSyst(cb,
    "CMS_htt_jetFakeTau_$CHANNEL_13TeV", "lnN", SystMap<bin_id,process>::init
    ({8,9,10,11,12,13,14,15}, {"ZJ"},1.20)
    ({8,10,11,12},            {"TT"},1.08)
    ({9,13,14,15},            {"TT"},1.04));
  
  cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_jetFakeTau_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));

  cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
    "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(2.00));

  // QCD extrap.
  // -----------
  cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
    "CMS_htt_QCD_OS_SS_syst_$BIN", "lnN", SystMap<bin_id>::init
    ({8}, 1.16)
    ({9}, 1.40));

  cb.cp().process({"QCD"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_QCD_norm_syst_$BIN", "lnN", SystMap<bin_id>::init
    ({8}, 1.06)
    ({9}, 1.21));

  if (control_region == 0) {
    // the uncertainty model in the signal region is the classical one

    // Add back the JES and b-tag uncertainties directly to the W and QCD
    // yields in the signal regions (driven by the effect on other backgrounds
    // in the control regions)
    cb.cp().AddSyst(cb,
      "CMS_scale_j_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
      ({"mt"}, {9}, {"W"},    0.1,    2.08) // changed the lower one from 0.0 to 0.1
      ({"mt"}, {9}, {"QCD"},  1.027,  0.975)
      ({"et"}, {9}, {"W"},    0.687,  1.298)
      ({"et"}, {9}, {"QCD"},  1.013,  0.986));

    cb.cp().AddSyst(cb,
      "CMS_eff_b_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
      ({"mt"}, {8}, {"W"},    0.99, 1.01)
      ({"mt"}, {9}, {"W"},    1.41, 0.62)
      ({"mt"}, {9}, {"QCD"},  0.99, 1.01)
      ({"et"}, {8}, {"W"},    0.99, 1.01)
      ({"et"}, {9}, {"W"},    1.19, 0.91)
      ({"et"}, {9}, {"QCD"},  0.99, 1));

    // Next we add the effect of uncertainties on the W and QCD ratios

    // OS/SS W factor stat. uncertainty
    // Take same numbers as below, but this is probably conservative
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_OS_SS_stat_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.015)
      ({"mt"}, {9}, 1.100)
      ({"et"}, {8}, 1.015)
      ({"et"}, {9}, 1.110));

    // OS/SS W factor syst. uncertainty
    // Based of data/MC for OS/SS ratio in anti-tau iso high mT region
    // Decorrelate between categories for now - but this should be studied
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_OS_SS_syst_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.060)
      ({"mt"}, {9}, 1.110)
      ({"et"}, {8}, 1.100)
      ({"et"}, {9}, 1.140));

    // low/high mT W factor stat. uncertainty
    // Should affect signal region and SS low mT
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_mT_stat_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.020)
      ({"mt"}, {9}, 1.130)
      ({"et"}, {8}, 1.020)
      ({"et"}, {9}, 1.150));

    // low/high mT W factor syst. uncertainty
    // Currently to be determined, could be motivated by low vs high mT jet->tau FR,
    // where we see a 10-15% variation from low to high mT. Go with 20% for now which
    // is comparable to what was used in Run 1 0-jet (20%) and the MSSM update (30%)
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_mT_syst_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.20)
      ({"mt"}, {9}, 1.20)
      ({"et"}, {8}, 1.20)
      ({"et"}, {9}, 1.20));

    // OS/SS QCD factor syst. uncertainty
    // Based on variation in fitted factor from different anti-iso sidebands
    cb.cp().process({"QCD"}).AddSyst(cb,
      "CMS_htt_QCD_OS_SS_syst_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.100)
      ({"mt"}, {9}, 1.400)
      ({"et"}, {8}, 1.100)
      ({"et"}, {9}, 1.400));
    }
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
      for (auto bin : cb_sig.cp().channel({"et", "mt"}).bin_set()) {
        // Regex that matches, e.g. mt_nobtag or mt_nobtag_X
        cb.cp().bin({bin+"(|_.*)$"}).process({"W"}).AddSyst(cb,
          "rate_W_"+bin, "rateParam", SystMap<>::init(1.0));

        // Regex that matches, e.g. mt_nobtag or mt_nobtag_qcd_cr
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"QCD"}).AddSyst(cb,
          "rate_QCD_lowmT_"+bin, "rateParam", SystMap<>::init(1.0));

        // Regex that matches, e.g. mt_nobtag_wjets_cr or mt_nobtag_wjets_ss_cr
        cb.cp().bin({bin+"_wjets(|_ss)_cr$"}).process({"QCD"}).AddSyst(cb,
          "rate_QCD_highmT_"+bin, "rateParam", SystMap<>::init(1.0));

        /////////////////
        // Systematics //
        /////////////////

        // OS/SS W factor stat. uncertainty
        // Should affect signal region and OS high mT
        cb.cp().bin({bin+"(|_wjets_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_OS_SS_stat_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 10}, 1.015)
          ({"mt"}, {9, 13}, 1.100)
          ({"et"}, {8, 10}, 1.015)
          ({"et"}, {9, 13}, 1.110));

        // OS/SS W factor syst. uncertainty
        // Based of data/MC for OS/SS ratio in anti-tau iso high mT region
        // Decorrelate between categories for now - but this should be studied
        cb.cp().bin({bin+"(|_wjets_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_OS_SS_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 10}, 1.060)
          ({"mt"}, {9, 13}, 1.110)
          ({"et"}, {8, 10}, 1.100)
          ({"et"}, {9, 13}, 1.140));

        // low/high mT W factor stat. uncertainty
        // Should affect signal region and SS low mT
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_mT_stat_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 11}, 1.020)
          ({"mt"}, {9, 14}, 1.130)
          ({"et"}, {8, 11}, 1.020)
          ({"et"}, {9, 14}, 1.150));

        // low/high mT W factor syst. uncertainty
        // Currently to be determined, could be motivated by low vs high mT jet->tau FR
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_mT_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 11}, 1.20)
          ({"mt"}, {9, 14}, 1.20)
          ({"et"}, {8, 11}, 1.20)
          ({"et"}, {9, 14}, 1.20));

        // OS/SS QCD factor syst. uncertainty
        // Based on variation in fitted factor from different anti-iso sidebands
        cb.cp().bin({bin+"(|_wjets_cr)$"}).process({"QCD"}).AddSyst(cb,
          "CMS_htt_QCD_OS_SS_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 10}, 1.100)
          ({"mt"}, {9, 13}, 1.400)
          ({"et"}, {8, 10}, 1.100)
          ({"et"}, {9, 13}, 1.400));

        cb.cp().AddSyst(cb,
          "CMS_scale_j_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"mt"},  {10}, {"TT"}, 1.017, 0.986)
          ({"mt"},  {11}, {"TT"}, 1.009, 0.992)
          ({"mt"},  {12}, {"TT"}, 1.011, 0.989)
          ({"mt"},  {13}, {"TT"}, 1.076, 0.924)
          ({"mt"},  {13}, {"VV"}, 1.014, 0.978)
          ({"mt"},  {14}, {"ZJ"}, 0.971, 1.021)
          ({"mt"},  {14}, {"TT"}, 1.132, 0.879)
          ({"mt"},  {15}, {"TT"}, 1.089, 0.918)
          ({"et"},  {10}, {"TT"}, 1.017, 0.985)
          ({"et"},  {11}, {"TT"}, 1.014, 0.988)
          ({"et"},  {12}, {"TT"}, 1.011, 0.988)
          ({"et"},  {13}, {"TT"}, 1.073, 0.927)
          ({"et"},  {13}, {"VV"}, 1.032, 0.972)
          ({"et"},  {14}, {"TT"}, 1.099, 0.896)
          ({"et"},  {15}, {"TT"}, 1.086, 0.924));

        cb.cp().AddSyst(cb,
          "CMS_eff_b_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"mt"},  {10}, {"TT"}, 1.054, 0.951)
          ({"mt"},  {11}, {"TT"}, 1.035, 0.966)
          ({"mt"},  {12}, {"TT"}, 1.036, 0.963)
          ({"mt"},  {13}, {"TT"}, 0.978, 1.020)
          ({"mt"},  {13}, {"VV"}, 0.972, 1.029)
          ({"mt"},  {14}, {"TT"}, 0.975, 1.026)
          ({"mt"},  {15}, {"TT"}, 0.972, 1.022)
          ({"mt"},  {15}, {"VV"}, 0.949, 1.036)
          ({"et"},  {10}, {"TT"}, 1.054, 0.949)
          ({"et"},  {11}, {"TT"}, 1.043, 0.961)
          ({"et"},  {12}, {"TT"}, 1.039, 0.964)
          ({"et"},  {13}, {"TT"}, 0.978, 1.022)
          ({"et"},  {14}, {"TT"}, 0.957, 1.022)
          ({"et"},  {15}, {"TT"}, 0.974, 1.023));
      }
      // Should set a sensible range for our rateParams
      for (auto sys : cb.cp().syst_type({"rateParam"}).syst_name_set()) {
        cb.GetParameter(sys)->set_range(0.0, 5.0);
      }
      cb.SetFlag("filters-use-regex", false);
    }
  }
}
