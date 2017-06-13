#include "CombineHarvester/HIG16037/interface/HttSystematics_MSSMRun2.h"
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

void AddMSSMRun2Systematics(CombineHarvester & cb, int control_region, bool zmm_fit) {
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
    SystMap<>::init(1.039));

  cb.cp().process({"qqH_SM125"}).AddSyst(cb, "QCDscale_qqH", "lnN",
    SystMapAsymm<>::init(1.004,0.997));


  cb.cp().process({"ZH_SM125","WplusH_SM125","WminusH_SM125"}).AddSyst(cb, "QCDscale_VH", "lnN",
    SystMapAsymm<process>::init
     ({"ZH_SM125"}, 1.038, 0.969)
     ({"WplusH_SM125","WminusH_SM125"},1.005,0.993));

/*  cb.cp().process({"TTH_SM125"}).AddSyst(cb,"QCDscale_ttH","lnN", 
    SystMapAsymm<>::init(1.058,0.908));*/

  cb.cp().process({"ggH_SM125"}).AddSyst(cb, "pdf_Higgs_gg","lnN",
    SystMap<>::init(1.032));

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
    ({"zmm"}, {"ZTT", "TT", "VV", "ZL"},  1.04)
    ({"zmm"}, {"ZJ"},  1.02)
    ({"mt"}, JoinStr({signal, {"ZTT", "TTT","TTJ", "VVT","VVJ", "ZL", "ZJ"}}),  1.02)
    ({"em"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZLL"}}),       1.02));
  
  cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
    ({"et"}, JoinStr({signal, {"ZTT", "TTT","TTJ", "VVT","VVJ", "ZL", "ZJ"}}),  1.02)
    ({"em"}, JoinStr({signal, {"ZTT", "TT", "VV", "ZLL"}}),       1.02));


/*  cb.cp().process(ch::JoinStr({signal, {"TTT","TTJ","VVT","VVJ","ZL","ZJ","ZTT","W","VV","TT","ZLL","QCD"}}))
      .AddSyst(cb, "CMS_scale_b_13TeV", "shape", SystMap<>::init(1.00));

  cb.cp().process(ch::JoinStr({signal, {"TTT","TTJ","VVT","VVJ","ZL","ZJ","ZTT","W","VV","TT","ZLL","QCD"}}))
      .AddSyst(cb, "CMS_scale_j_13TeV", "shape", SystMap<>::init(1.00));

  cb.cp().process(ch::JoinStr({signal, {"TTT","TTJ","VVT","VVJ","ZL","ZJ","ZTT","W","VV","TT","ZLL","QCD"}}))
      .AddSyst(cb, "CMS_fake_b_13TeV", "shape", SystMap<>::init(1.00));*/


  // Jet energy scale
  // ----------------
  cb.cp().AddSyst(cb,
    "CMS_scale_j_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    ({"mt"}, {8}, {"TTT","TTJ"},   1.01,  0.99)
    ({"mt"}, {8}, {"VVJ"},   1.00,  0.99)
    ({"mt"}, {8}, {bbH},  1.01, 0.99) 
    ({"mt"}, {9}, {"ZL"},   0.97 ,  1.03)
    ({"mt"}, {9}, {"ZJ"},   1.02,  1.03)
    ({"mt"}, {9}, {"ZTT"},  0.98,  1.01)
    ({"mt"}, {9}, {"TTT"},   1.09,  0.90)
    ({"mt"}, {9}, {"TTJ"},   1.12,  0.88)
    ({"mt"}, {9}, {"VVT"},   1.07, 0.96)
    ({"mt"}, {9}, {"VVJ"},   1.06, 0.95)
    ({"mt"}, {9}, {ggH},  1.03, 0.96) 
    ({"mt"}, {9}, {bbH},  0.98,1.02) 
    ({"et"}, {8}, {"TTT","TTJ"},   1.01,  0.99)
    ({"et"}, {8}, {"VVJ"},   1.01,  0.99)
    ({"et"}, {8}, {bbH},  1.01,0.99) 
    ({"et"}, {9}, {"ZL"},   1.01,  1.00)
    ({"et"}, {9}, {"ZJ"},   0.97,  0.96)
    ({"et"}, {9}, {"ZTT"},  0.96,  1.01)
    ({"et"}, {9}, {"VVT"},   1.04,  0.94)
    ({"et"}, {9}, {"VVJ"},   1.11,  0.96)
    ({"et"}, {9}, {"TTT"},   1.10, 0.91)
    ({"et"}, {9}, {"TTJ"},   1.14, 0.87)
    ({"et"}, {9}, {bbH},  0.98,1.01) 
    ({"et"}, {9}, {ggH},  0.98,1.04) 
    ({"zmm"}, {8}, {"TT"},   1.01,  0.99)
    ({"zmm"}, {9}, {"W"},    1.69,  0.93)
    ({"zmm"}, {9}, {"QCD"},  0.96,  1.04)
    ({"zmm"}, {9}, {"ZL"},   1.01,  1.00)
    ({"zmm"}, {9}, {"ZJ"},   0.97,  0.96)
    ({"zmm"}, {9}, {"ZTT"},  0.99, 1.03)
    ({"zmm"}, {9}, {"VV"},   1.05, 0.95)
    ({"zmm"}, {9}, {"TT"},   1.10, 0.90)
    ({"em"}, {8}, {"TT"},   1.01,  0.99) 
    ({"em"}, {8}, {bbH},  0.99,1.01) 
    ({"em"}, {9}, {"W"},    1.69,  0.93) 
    ({"em"}, {9}, {"QCD"},  0.96,  1.04) 
    ({"em"}, {9}, {"ZLL"},  1.08, 1.38) 
    ({"em"}, {9}, {"ZTT"},  0.99, 1.03) 
    ({"em"}, {9}, {"VV"},   1.05, 0.95) 
    ({"em"}, {9}, {"TT"},   1.10, 0.90)
    ({"em"}, {9}, {ggH},  1.03, 0.98) 
    ({"em"}, {9}, {bbH},  1.01, 0.99) 
    ({"tt"}, {8}, {"VVT"},   1.01,   1.00)
    ({"tt"}, {8}, {"VVJ"},   1.00,   0.98)
    ({"tt"}, {8}, {"TTT"},   1.04,   0.98)
    ({"tt"}, {8}, {"TTJ"},   1.02,   0.99)
    ({"tt"}, {8}, {bbH}, 1.01, 0.99) 
    ({"tt"}, {9}, {"W"},    1.05, 0.94  )
    ({"tt"}, {9}, {"QCD"},  1.004,  1.009)//to be done
    ({"tt"}, {9}, {"ZL"},   1.00,   1.04)
    ({"tt"}, {9}, {"ZJ"},   1.00,   0.95)
    ({"tt"}, {9}, {"VVT"},   1.09,   0.90)
    ({"tt"}, {9}, {"VVJ"},   1.05,   1.08)
    ({"tt"}, {9}, {"TTT"},   1.09,   0.91)
    ({"tt"}, {9}, {"TTJ"},   1.07,   0.87)
    ({"tt"}, {9}, {bbH},  0.98, 1.02) 
    ({"tt"}, {9}, {ggH},  1.00, 0.96)); 

  // b-tagging efficiency and fake rate
  // ----------------------------------
  cb.cp().AddSyst(cb,
    "CMS_eff_b_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    ({"mt"}, {8}, {"TTT","TTJ"},   1.03, 0.97)
    ({"mt"}, {8}, {"VVT"},   1.01, 1.00)
    ({"mt"}, {8}, {"VVJ"},   1.01, 0.99)
    ({"mt"}, {8}, {bbH},  1.01, 0.99) 
    ({"mt"}, {9}, {"ZL"},   0.97,   1.03)
    ({"mt"}, {9}, {"ZJ"},   0.98,   1.02)
    ({"mt"}, {9}, {"TTT","TTJ"},   0.99,   1.01)
    ({"mt"}, {9}, {"VVT"},   0.97,   1.01)
    ({"mt"}, {9}, {"VVJ"},   0.99,   1.02)
    ({"mt"}, {9}, {"ZTT"},  0.98,   1.02)
    ({"mt"}, {9}, {ggH},  0.98,1) 
    ({"mt"}, {9}, {bbH},  0.98, 1.02) 
    ({"et"}, {8}, {"VVT","VVJ"},   1.01,   0.99)
    ({"et"}, {8}, {"TTT","TTJ"},   1.03,   0.97)
    ({"et"}, {8}, {bbH},  1.01, 0.99) 
    ({"et"}, {9}, {"ZL"},   0.99,   1.01)
    ({"et"}, {9}, {"ZJ"},   0.98,   1.04)
    ({"et"}, {9}, {"ZTT"},  0.98,   1.02)
    ({"et"}, {9}, {"VVT"},   0.99,   1.01)
    ({"et"}, {9}, {"VVJ"},   1.00,   1.02)
    ({"et"}, {9}, {"TTT"},   0.99,   1.02)
    ({"et"}, {9}, {"TTJ"},   0.99,   1.01)
    ({"et"}, {9}, {ggH},  0.98, 1.02) 
    ({"et"}, {9}, {bbH},  0.98, 1.02) 
    ({"zmm"}, {8}, {"VV"},   1.01,   0.99) 
    ({"zmm"}, {8}, {"TT"},   1.03,   0.97) 
    ({"zmm"}, {9}, {"W"},  0.99, 1.03  ) 
    ({"zmm"}, {9}, {"QCD"},  1.01, 0.88  ) 
    ({"zmm"}, {9}, {"ZTT"},  0.99,   1.02)
    ({"zmm"}, {9}, {"VV"},   0.98,   1.01)
    ({"zmm"}, {9}, {"TT"},   0.99,   1.01)
    ({"zmm"}, {9}, {"ZL"},   0.97,   1.03)
    ({"zmm"}, {9}, {"ZJ"},   0.98,   1.02)
    ({"em"}, {8}, {"VV"},   1.01,   0.99) 
    ({"em"}, {8}, {"TT"},   1.03,   0.97) 
    ({"em"}, {8}, {"bbH"},  1.01,   0.99) 
    ({"em"}, {9}, {"W"},  0.99, 1.03  ) 
    ({"em"}, {9}, {"QCD"},  1.01, 0.88  ) 
    ({"em"}, {9}, {"ZTT"},  0.99,   1.02)
    ({"em"}, {9}, {"VV"},   0.98,   1.01)
    ({"em"}, {9}, {"TT"},   0.99,   1.01)
    ({"em"}, {9}, {ggH}, 0.97, 1.02) 
    ({"em"}, {9}, {bbH}, 0.99,  1.01) 
    ({"tt"}, {8}, {bbH},  1.01,   0.99)
    ({"tt"}, {8}, {"TTT"},    1.02,      0.96)
    ({"tt"}, {8}, {"TTJ"},    1.04,      0.97)
    ({"tt"}, {9}, {"W"},    1.00,      1.11)
    ({"tt"}, {9}, {"ZTT"},  0.99,   1.02)
    ({"tt"}, {9}, {"TTT"},   0.99,   1.03)
    ({"tt"}, {9}, {"TTJ"},   0.98,   1.01)
    ({"tt"}, {9}, {"VVT"},   0.99,   1.05)
    ({"tt"}, {9}, {bbH},  0.98,   1.02)
    ({"tt"}, {9}, {ggH},  0.99,   1.03));


  cb.cp().AddSyst(cb,
    "CMS_fake_b_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
    ({"mt"}, {9}, {"ZL"},   0.99,  1.02)
    ({"mt"}, {9}, {"ZJ"},   0.93,   1.05)
    ({"mt"}, {9}, {"ZTT"},  0.97,   1.02)
    ({"mt"}, {9}, {ggH},  0.96, 1.04)
    ({"et"}, {9}, {"ZL"},   0.99,   1.01)
    ({"et"}, {9}, {"ZJ"},   0.98,   1.00)
    ({"et"}, {9}, {"ZTT"},  0.97,   1.03)
    ({"zmm"}, {9}, {"ZTT"},  0.98,   1.02)
    ({"zmm"}, {9}, {"ZL"},  0.95,   1.02)
    ({"zmm"}, {9}, {"ZJ"},  0.92,   1.04)
    ({"zmm"}, {9}, {"W"},  0.94,   1.04)
    ({"em"}, {9}, {"ZTT"},  0.98,   1.02)
    ({"em"}, {9}, {"ZLL"},  0.90,   1.05)
    ({"em"}, {9}, {"W"},  0.94,   1.04)
    ({"em"}, {9}, {ggH},  0.97, 1.02)
    ({"tt"}, {8}, {ggH},  0.99, 1.01)
    ({"tt"}, {9}, {"ZJ"},   0.88,   1.11)
    ({"tt"}, {9}, {"ZTT"},  0.98,   1.02)
    ({"tt"}, {9}, {"VVT"},   1.00,   1.03)
    ({"tt"}, {9}, {ggH},  0.97,   1.03));

  // Tau-related systematics
  // -----------------------
  cb.cp().process(JoinStr({signal, {"ZTT","VVT","TTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_$ERA", "lnN", SystMap<channel>::init
    ({"et", "mt"}, 1.05)
    ({"tt"},       1.10));

  cb.cp().process(JoinStr({signal, {"ZTT","VVT","TTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<channel>::init
    ({"et", "mt"}, 1.03)
    ({"tt"},       1.092));

  cb.cp().process(JoinStr({signal, {"ZTT","VVT","TTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_eff_t_mssmHigh_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp().process(JoinStr({signal, {"ZTT","VVT","TTT"}})).channel({"et","mt","tt"}).AddSyst(cb,
    "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

  //DY reweighting
  cb.cp().process(JoinStr({{"ZTT"}})).channel({"et","mt","tt", "em"}).AddSyst(cb,
    "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));

  //W jet->tau FR shape
  cb.cp().process(JoinStr({{"W"}})).channel({"et","mt"}).bin_id({8,9}).AddSyst(cb,
    "CMS_htt_wFakeShape_$ERA","shape",SystMap<>::init(1.00));

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
  // CHECK THIS
  cb.cp().AddSyst(cb,
    "CMS_htt_boson_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, JoinStr({signal, {"ZTT", "W"}}), 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_boson_reso_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, JoinStr({signal, {"ZTT", "W"}}), 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_ewkTop_scale_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, {"TTT","TTJ","TT","VV", "VVT","VVJ"}, 1.02));

  cb.cp().AddSyst(cb,
    "CMS_htt_ewkTop_reso_met_$ERA", "lnN", SystMap<channel, bin_id, process>::init
    ({"et", "mt", "em", "tt"}, {8, 9, 11, 14}, {"TTT","TTJ","TT","VV", "VVT","VVJ"}, 1.02));

  // top-quark pT reweighting
  // ------------------------
  cb.cp().channel({"zmm"},false).process({"TTT","TTJ","TT"}).AddSyst(cb,
    "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));

  // Cross-sections and lumi
  // -----------------------
  cb.cp().process(JoinStr({signal, {"TTT","TTJ","TT","VV","VVT","VVJ", "ZL", "ZJ", "ZTT", "ZLL"}})).AddSyst(cb,
    "lumi_13TeV", "lnN", SystMap<>::init(1.062));

  //Add luminosity uncertainty for W in em, tt and the zmm region as norm is from MC
  cb.cp().process({"W"}).channel({"tt","em","zmm"}).AddSyst(cb,
    "lumi_13TeV", "lnN", SystMap<>::init(1.062));

  if(zmm_fit)
  {
    // Add Z crosssection uncertainty on ZL, ZJ and ZLL (not ZTT due to taking into account the zmm control region).
    // Also don't add it for the zmm control region
    cb.SetFlag("filters-use-regex", true);
    cb.cp().channel({"zmm"},false).process({"ZL", "ZJ", "ZLL"}).AddSyst(cb,
        "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
    cb.cp().channel({"zmm"},false).bin({"_cr$"}).process({"ZTT"}).AddSyst(cb,
        "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
    cb.SetFlag("filters-use-regex", false);

    cb.FilterSysts([](ch::Systematic *syst) {
      return syst->name() == "lumi_13TeV" &&
        (
          (syst->channel() == "zmm" && syst->process() == "ZL") ||
          (syst->channel() != "zmm" && syst->process() == "ZTT" &&
            (syst->bin_id() == 8 || syst->bin_id() == 9))
        );
    });
  }
  else
  {
    cb.cp().process({"ZTT", "ZL", "ZJ", "ZLL"}).AddSyst(cb,
        "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
  }

  // Diboson and ttbar Normalisation - fully correlated
  cb.cp().process({"VV","VVT","VVJ"}).AddSyst(cb,
    "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"TT","TTJ","TTT"}).AddSyst(cb,
    "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));
  
  // W norm, just for em, tt and the zmm region where MC norm is from MC
  cb.cp().process({"W"}).channel({"tt","em","zmm"}).AddSyst(cb,
    "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));

  // Category-acceptance
  // -------------------
  // For ZTT use 5% run 1 value for now, should be replaced based
  // on Z->mumu calibration. Also only apply this to signal-region
  // categories for now, using cb_sig instead of cb
  // In case we use the zmm region in the fit this uncertainty is currently a placeholder for the uncertainty on the Z->mumu/Z->tautau uncertainty
  // THIS IS TO BE CHECKED
  cb_sig.cp().channel({"mt","et","em","tt"}).process({"ZTT"}).AddSyst(cb,
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
    ({8,9,10,11,12,13,14,15}, {"TTJ"},1.20));
  
  cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_jetFakeTau_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.20));

  cb.cp().process({"ZL"}).channel({"mt"}).AddSyst(cb,
    "CMS_htt_mFakeTau_tight_13TeV", "lnN", SystMap<>::init(1.30)); //Uncertainty ranges from 7-35% depending on eta bin

  cb.cp().process({"ZL"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_mFakeTau_loose_13TeV", "lnN", SystMap<>::init(1.20)); //Uncertainty ranges from 5-23% depending on eta bin



  // QCD extrap.
  // -----------
  // emu QCD extrapolation 
  cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
    "CMS_htt_QCD_OS_SS_syst_$BIN", "lnN", SystMap<bin_id>::init
    ({8}, 1.23)
    ({9}, 1.34));

 //tt QCD extrapolation: 
 //No b-tag: 2% stat uncertainty + 12% systematic uncertainty (from difference between OS/SS extrapolation factors from tau1 loose-not tight and tau2 medium-not tight
 //into tau1 loose-not tight and tau2 tight)
 //B-tag: 20% stat uncertainty + 14% systematic uncertainty (from difference between OS and SS extrapolation factors from tau1 loose-not tight and tau2 loose-not tight 
 //into tau1 loose-not tight and tau2 tight)
  cb.cp().process({"QCD"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_QCD_norm_stat_$BIN", "lnN", SystMap<bin_id>::init
    ({8}, 1.02)
    ({9}, 1.20));

  cb.cp().process({"QCD"}).channel({"tt"}).AddSyst(cb,
    "CMS_htt_QCD_norm_syst_$BIN", "lnN", SystMap<bin_id>::init
    ({8}, 1.12)
    ({9}, 1.14));


  if (control_region == 0) {
    // the uncertainty model in the signal region is the classical one

    // Add back the JES and b-tag uncertainties directly to the W and QCD
    // yields in the signal regions (driven by the effect on other backgrounds
    // in the control regions)
    cb.cp().AddSyst(cb,
      "CMS_scale_j_$ERA", "lnN", SystMapAsymm<channel,bin_id,process>::init
      ({"mt"}, {9}, {"W"},    1.02,    1.04) 
      ({"mt"}, {9}, {"QCD"},  1.027,  0.975) //To be chacked still!
      ({"et"}, {9}, {"W"},    0.93,  1.03)
      ({"et"}, {9}, {"QCD"},  1.013,  0.986)); //To be checked still!

    //Need to put these back in in case we did want to fit without the control region for some reason
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
      ({"mt"}, {8}, 1.02)
      ({"mt"}, {9}, 1.03)
      ({"et"}, {8}, 1.02)
      ({"et"}, {9}, 1.03));

    // OS/SS W factor syst. uncertainty
    // Based of data/MC for OS/SS ratio in anti-tau iso high mT region
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_OS_SS_syst_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.080)
      ({"mt"}, {9}, 1.100)
      ({"et"}, {8}, 1.080)
      ({"et"}, {9}, 1.100));

    // low/high mT W factor stat. uncertainty
    // Should affect signal region and SS low mT
    cb.cp().process({"W"}).AddSyst(cb,
      "CMS_htt_W_mT_stat_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
      ({"mt"}, {8}, 1.020)
      ({"mt"}, {9}, 1.030)
      ({"et"}, {8}, 1.020)
      ({"et"}, {9}, 1.030));

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
      ({"mt"}, {8}, 1.040)
      ({"mt"}, {9}, 1.600)
      ({"et"}, {8}, 1.120)
      ({"et"}, {9}, 1.600));
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
          ({"mt"}, {8, 10}, 1.02)
          ({"mt"}, {9, 13}, 1.11)
          ({"et"}, {8, 10}, 1.02)
          ({"et"}, {9, 13}, 1.14));

        // OS/SS W factor syst. uncertainty
        // Based of data/MC for OS/SS ratio in anti-tau iso high mT region
        cb.cp().bin({bin+"(|_wjets_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_OS_SS_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 10}, 1.08)
          ({"mt"}, {9, 13}, 1.10)
          ({"et"}, {8, 10}, 1.08)
          ({"et"}, {9, 13}, 1.10));

        // low/high mT W factor stat. uncertainty
        // Should affect signal region and SS low mT
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_mT_stat_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 11}, 1.02)
          ({"mt"}, {9, 14}, 1.14)
          ({"et"}, {8, 11}, 1.02)
          ({"et"}, {9, 14}, 1.17));

        // low/high mT W factor syst. uncertainty
        // Currently to be determined, could be motivated by low vs high mT jet->tau FR
        cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"W"}).AddSyst(cb,
          "CMS_htt_W_mT_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 11}, 1.20)
          ({"mt"}, {9, 14}, 1.20)
          ({"et"}, {8, 11}, 1.20)
          ({"et"}, {9, 14}, 1.20));

        //W b-tag extrapolation factor stat. uncertainty - merged into low mT/high mT and W OS/SS uncertainties
        //which are now calculated for the full b-tag 
        /*cb.cp().bin({bin+"(|_qcd_cr)$",bin+"(|_wjets_cr)$",bin+"(|_wjets_ss_cr)$"}).process({"W"}).AddSyst(cb,
         "CMS_htt_W_extrap_stat_"+bin+"_$ERA","lnN", SystMap<channel, bin_id>::init
         ({"et"},{9},1.11)
         ({"et"},{13},1.14)
         ({"et"},{14},1.21)
         ({"et"},{15},1.16)
         ({"mt"},{9},1.12)
         ({"mt"},{13},1.08)
         ({"mt"},{14},1.22)
         ({"mt"},{15},1.14));*/
    
        //W b-tag extrapolation factor syst uncertainty
        //1) b-tag efficiency uncertainty
        cb.cp().process({"W"}).AddSyst(cb,
         "CMS_eff_b_13TeV","lnN", SystMapAsymm<channel, bin_id>::init
         ({"mt"},{9},0.96,1.01)
         ({"mt"},{13},0.98,1.04)
         ({"mt"},{14},1.0,1.06)
         ({"mt"},{15},0.96,1.01)
         ({"et"},{9},0.95,1.02)
         ({"et"},{13},0.99,1.02)
         ({"et"},{14},0.90,1.00)
         ({"et"},{15},0.97,1.00));
 
        //W b-tag extrapolation factor syst uncertainty
        //Only needed if fitting 1-jet selection at high mT which we're not doing now
        //2) From difference between MC and data-bkg 'W+'tau'+jet -> W+'tau'+b
        //extrapolation factor in a high mT tau anti-iso region. Uses 
        //number for mt for et too as there is a lot more QCD in this
        //region for et than for mt
        /*cb.cp().bin({bin+"(|_qcd_cr)$"}).process({"W"}).AddSyst(cb,
         "CMS_htt_W_extrap_syst_"+bin+"_$ERA","lnN", SystMap<channel, bin_id>::init
         ({"et"},{9,14},1.10)
         ({"mt"},{9,14},1.10));*/
    


        // OS/SS QCD factor syst. uncertainty
        // Based on variation in fitted factor from different anti-iso sidebands
        cb.cp().bin({bin+"(|_wjets_cr)$"}).process({"QCD"}).AddSyst(cb,
          "CMS_htt_QCD_OS_SS_syst_"+bin+"_$ERA", "lnN", SystMap<channel, bin_id>::init
          ({"mt"}, {8, 10}, 1.040)
          ({"mt"}, {9, 13}, 1.600)
          ({"et"}, {8, 10}, 1.120)
          ({"et"}, {9, 13}, 1.600));

        cb.cp().AddSyst(cb,
          "CMS_scale_j_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"mt"},  {10}, {"TTT"}, 1.015, 0.986)
          ({"mt"},  {10}, {"TTJ"}, 1.013, 0.99)
          ({"mt"},  {11}, {"TTT"}, 1.01, 0.99)
          ({"mt"},  {11}, {"TTJ"}, 1.01, 0.99)
          ({"mt"},  {11}, {"VVJ"}, 1.01, 1.00)
          ({"mt"},  {12}, {"TTJ"}, 1.01, 0.99)
          ({"mt"},  {13}, {"TTT"}, 1.10, 0.91)
          ({"mt"},  {13}, {"TTJ"}, 1.11, 0.89)
          ({"mt"},  {13}, {"VVT"}, 1.04, 0.97)
          ({"mt"},  {13}, {"VVJ"}, 1.04, 0.96)
          ({"mt"},  {13}, {"ZTT"}, 1.06, 0.87)
          ({"mt"},  {13}, {"ZL"}, 0.97, 0.99)
          ({"mt"},  {13}, {"ZJ"}, 0.95, 0.96)
          ({"mt"},  {14}, {"ZJ"}, 0.97, 1.34)
          ({"mt"},  {14}, {"TTT"}, 1.15, 0.92)
          ({"mt"},  {14}, {"TTJ"}, 1.11, 0.87)
          ({"mt"},  {14}, {"VVT"}, 0.96, 0.94)
          ({"mt"},  {14}, {"VVJ"}, 1.02, 0.90)
          ({"mt"},  {15}, {"TTT"}, 1.14, 0.90)
          ({"mt"},  {15}, {"TTJ"}, 1.12, 0.89)
          ({"mt"},  {15}, {"ZJ"}, 0.93, 1.04)
          ({"mt"},  {15}, {"VVT"}, 0.96, 1.01)
          ({"mt"},  {15}, {"VVJ"}, 1.07, 0.93)
          ({"et"},  {10}, {"TTT","TTJ"}, 1.01, 0.99)
          ({"et"},  {11}, {"TTT"}, 1.02, 1.00)
          ({"et"},  {11}, {"TTJ"}, 1.01, 0.99)
          ({"et"},  {12}, {"TTT","TTJ"}, 1.01, 0.99)
          ({"et"},  {13}, {"TTT"}, 1.09, 0.91)
          ({"et"},  {13}, {"TTJ"}, 1.12, 0.90)
          ({"et"},  {13}, {"VVT"}, 1.04, 0.96)
          ({"et"},  {13}, {"VVJ"}, 1.06, 0.96)
					({"et"},  {14}, {"TTJ"}, 1.15, 0.88)
          ({"et"},  {14}, {"VVJ"}, 1.08, 0.94)
          ({"et"},  {15}, {"VVJ"}, 1.07, 0.94)
          ({"et"},  {15}, {"TTJ"}, 1.15, 0.91));

        //If fitting 1-jet selection instead of b-tag in high mT control regions, categories 15 and 13
        //are no longer affected by b-tag efficiency uncertainty
        //Currently using full b-tag definition in this control region
        //so they are back in
        cb.cp().AddSyst(cb,
          "CMS_eff_b_13TeV", "lnN", SystMapAsymm<channel,bin_id,process>::init
          ({"mt"},  {10}, {"TTT"}, 1.03, 0.97)
          ({"mt"},  {10}, {"TTJ"}, 1.02, 0.97)
          ({"mt"},  {10}, {"VVT","VVJ"}, 1.01, 0.99)
          ({"mt"},  {11}, {"TTT"}, 1.03, 0.98)
          ({"mt"},  {11}, {"TTJ"}, 1.02, 0.98)
          ({"mt"},  {12}, {"TTT","TTJ"}, 1.02, 0.97)
          ({"mt"},  {12}, {"VVJ"}, 1.01, 0.99)
          ({"mt"},  {13}, {"TTT","TTJ"}, 0.99, 1.02)
          ({"mt"},  {13}, {"VVT","VVJ"}, 0.99, 1.03)
          ({"mt"},  {14}, {"TTT","TTJ"}, 0.98, 1.03)
          ({"mt"},  {14}, {"VVT"}, 1.01, 1.00)
          ({"mt"},  {15}, {"TTT"}, 0.99, 1.01)
          ({"mt"},  {15}, {"TTJ"}, 0.98, 1.02)
          ({"mt"},  {15}, {"VVT"}, 1.03, 1.00)
          ({"mt"},  {15}, {"VVJ"}, 0.98, 1.02) 
          ({"et"},  {10}, {"TTT"}, 1.03, 0.97)
          ({"et"},  {10}, {"TTJ"}, 1.02, 0.97)
          ({"et"},  {10}, {"VVT"}, 1.01, 0.99)
          ({"et"},  {10}, {"VVJ"}, 1.01, 1.00)
          ({"et"},  {11}, {"TTT"}, 1.03, 0.96)
          ({"et"},  {11}, {"TTJ"}, 1.02, 0.98)
          ({"et"},  {11}, {"VVJ"}, 1.01, 0.99)
          ({"et"},  {12}, {"TTT"}, 1.04, 0.97)
          ({"et"},  {12}, {"TTJ"}, 1.02, 0.98)
          ({"et"},  {12}, {"VVJ"}, 1.01, 0.998)
          ({"et"},  {13}, {"TTT","TTJ"}, 0.99, 1.02)
          ({"et"},  {13}, {"VVT","VVJ"}, 0.99, 1.02)
          ({"et"},  {14}, {"TTJ"}, 0.99, 1.022)
          ({"et"},  {15}, {"TTJ"}, 0.98, 1.02)
          ({"et"},  {15}, {"VVJ"}, 0.96, 1.01));
      }
      // Should set a sensible range for our rateParams
      for (auto sys : cb.cp().syst_type({"rateParam"}).syst_name_set()) {
        cb.GetParameter(sys)->set_range(0.0, 5.0);
      }
      cb.SetFlag("filters-use-regex", false);
    }
    if (zmm_fit) {
        cb.SetFlag("filters-use-regex", true);
        cb.cp().bin({"mt_nobtag","et_nobtag","em_nobtag","tt_nobtag"}).process({"ZTT"}).AddSyst(cb, "rate_ZMM_ZTT_nobtag", "rateParam", SystMap<>::init(1.0));
        cb.cp().bin({"zmm_nobtag"}).process({"ZL"}).AddSyst(cb, "rate_ZMM_ZTT_nobtag", "rateParam", SystMap<>::init(1.0));
        cb.cp().bin({"mt_btag","et_btag","em_btag","tt_btag"}).process({"ZTT"}).AddSyst(cb, "rate_ZMM_ZTT_btag", "rateParam", SystMap<>::init(1.0));
        cb.cp().bin({"zmm_btag"}).process({"ZL"}).AddSyst(cb, "rate_ZMM_ZTT_btag", "rateParam", SystMap<>::init(1.0));
        cb.GetParameter("rate_ZMM_ZTT_btag")->set_range(0.8, 1.2);
        cb.GetParameter("rate_ZMM_ZTT_nobtag")->set_range(0.95, 1.05);
        cb.SetFlag("filters-use-regex", false);
    }
  }
}
