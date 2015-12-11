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

void AddMSSMUpdateSystematics_et_mt(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();
  src.channel({"et", "mt"});

  // This regular expression will match any Higgs signal process.
  // It's useful for catching all these processes when we don't know
  // which of them will be signal or background
  //std::string bb_rgx = "(bb[hHA])*";
  //std::string gg_rgx = "(gg[hHA])*";

  std::vector<std::string> ggH = {"ggH", "ggH_Htautau", "ggA_Atautau", "ggh_htautau"};
  std::vector<std::string> bbH = {"bbH", "bbH_Htautau", "bbA_Atautau", "bbh_htautau"};

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().process(JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
	     //({"7TeV"}, 1.026)
	     ({"8TeV"}, 1.026));
  
  src.cp().process({"ZTT"})
    .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel>::init({"mt"}, 1.010));
  src.cp().process({"ZTT"})
    .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel>::init({"et"}, 1.020));
		   
  src.cp()
    .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({10, 11, 12, 13, 14}, JoinStr({signal,{"ZTT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.08)
	     ({10, 11, 12}, {"TT"}, 1.080));

  src.cp()
    .AddSyst(cb, "CMS_eff_t_mssmHigh_mutau_$ERA", "shape", SystMap<channel, process>::init
	     ({"mt"}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1));

  src.cp()
    .AddSyst(cb, "CMS_eff_t_mssmHigh_etau_$ERA", "shape", SystMap<channel, process>::init
	     ({"et"}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1));
  
//  src.cp().process(JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}))
//    .AddSyst(cb, "CMS_eff_t_mssmHigh_$CHANNEL_$ERA", "shape", SystMap<>::init(1));

  src.cp()
    .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<channel, process>::init
	     ({"mt"}, JoinStr({signal,{"ZTT", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1));
  
  src.cp()
    .AddSyst(cb, "CMS_scale_t_etau_$ERA", "shape", SystMap<channel, process>::init
	     ({"et"}, JoinStr({signal,{"ZTT", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1));

//  src.cp().process(JoinStr({signal,{"ZTT", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
//    .AddSyst(cb, "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<channel>::init(1));
  
  //! [part1]
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
  //! [part1]
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_medium_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_medium_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_muTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_btag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_muTau_btag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_muTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_muTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_btag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_muTau_btag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_muTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_muTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {10}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {10}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_medium_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {11}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_medium_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {11}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {12}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_eleTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_eleTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {12}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_eleTau_btag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {13}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_eleTau_btag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_eleTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_eleTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {13}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_eleTau_btag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {14}, 1.000));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift2_eleTau_btag_high_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {14}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_eleTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {14}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_eleTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<channel, bin_id>::init({"et"}, {14}, 1.000));

  src.cp()
    .AddSyst(cb, "CMS_scale_j_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	     ({"mt", "et"}, {10, 11, 12}, JoinStr({bbH, {"TT"}}), 0.99)
	     ({"mt"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 0.99)
	     ({"mt"}, {13, 14}, {bbH}, 1.01)
	     ({"mt"}, {13, 14}, {"ZJ"}, 0.980)
	     ({"mt"}, {13, 14}, {"ZL"}, 0.980)
	     ({"mt"}, {13, 14}, {"TT"}, 0.920)
	     ({"mt"}, {13, 14}, {"VV"}, 0.980)
	     ({"et"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 1.03)
	     ({"et"}, {13, 14}, {bbH}, 1.01)
	     ({"et"}, {13, 14}, {"ZJ"}, 1.060)
	     ({"et"}, {13, 14}, {"ZL"}, 0.960)
	     ({"et"}, {13, 14}, {"TT"}, 0.900)
	     ({"et"}, {13, 14}, {"VV"}, 0.940));

  src.cp()
    .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({10, 11, 12, 13, 14}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.99)
	     ({10, 11, 12, 13, 14}, {"ZJ", "ZL", "TT"}, 1.010)
	     ({13, 14}, {"W"}, 1.010));
  
  src.cp()
    .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	     ({"et", "mt"}, {10, 11, 12}, {bbH}, 0.99)
	     ({"et", "mt"}, {10, 11, 12}, {"TT"}, 0.950)
	     ({"mt"}, {10, 11, 12}, {"VV"}, 0.980)
	     ({"et"}, {10, 11, 12}, {"VV"}, 0.990)
	     ({"mt"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 1.01)
	     ({"mt"}, {13, 14}, {bbH}, 1.03)
	     ({"mt"}, {13, 14}, {"ZL"}, 1.040)
	     ({"mt"}, {13, 14}, {"TT"}, 1.020)
	     ({"mt"}, {13, 14}, {"VV"}, 1.040)
	     ({"et"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 1.01)
	     ({"et"}, {13, 14}, {bbH}, 1.02)
	     ({"et"}, {13, 14}, {"ZL"}, 1.020)
	     ({"et"}, {13, 14}, {"ZJ"}, 1.040)
	     ({"et"}, {13, 14}, {"TT"}, 1.040)
	     ({"et"}, {13, 14}, {"VV"}, 1.040));
	       
  src.cp()
    .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	     ({"mt", "et"}, {10, 11, 12}, {"TT"}, 0.970)
	     ({"mt", "et"}, {10, 11, 12}, {"VV"}, 0.990)
	     ({"mt"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 1.05)
	     ({"mt"}, {13, 14}, {"ZL"}, 1.050)
	     ({"mt"}, {13, 14}, {"ZJ"}, 1.090)
	     ({"mt"}, {13, 14}, {"TT", "VV"}, 1.010)
	     ({"et"}, {13, 14}, JoinStr({ggH, {"ggH_SM125"}}), 1.03)
	     ({"et"}, {13, 14}, {"ZL"}, 1.020)
	     ({"et"}, {13, 14}, {"ZJ"}, 1.090)
	     ({"et"}, {13, 14}, {"TT", "VV"}, 1.010));

  src.cp().process({"ZTT", "ZJ", "ZL"})
    .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.030));
  
  src.cp().process({"ZTT"})
    .AddSyst(cb, "CMS_htt_extrap_ztt_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({11, 12, 13, 14}, 1.050));
  
  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.100));
  
  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarPtReweight_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarJetFake_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbar_emb_$ERA", "lnN", SystMap<bin_id>::init({13, 14}, 1.140));
  
  src.cp().process({"VV"})
    .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.150));
  
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WNorm_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.200)
	     ({13}, 1.300)
	     ({14}, 1.500));
  
  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDSyst_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.100)
	     ({13, 14}, 1.200));
  
  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDfrShape_mutau_$ERA", "shape", SystMap<channel>::init({"mt"}, 1.000));
  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDfrShape_etau_$ERA", "shape", SystMap<channel>::init({"et"}, 1.000));
  
  src.cp().process({"ZJ"})
    .AddSyst(cb, "CMS_htt_ZJetFakeTau_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.200));
  
  src.cp().process({"ZL"})
    .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_low_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init
	     ({"mt"}, {10, 13}, 1.300)
	     ({"et"}, {10, 13}, 1.200));
  
  src.cp().process({"ZL"})
    .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_medium_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init
	     ({"mt"}, {11, 14}, 1.300)
	     ({"et"}, {11, 14}, 1.200));

  src.cp().process({"ZL"})
    .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_high_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init
	     ({"mt"}, {12}, 1.300)
	     ({"et"}, {12}, 1.200));
  
  src.cp().process({"ZL"}).channel({"mt"})
    .AddSyst(cb, "CMS_htt_ZLScale_mutau_$ERA", "shape", SystMap<>::init(1.000));
  src.cp().process({"ZL"}).channel({"et"})
    .AddSyst(cb, "CMS_htt_ZLScale_etau_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_mutau_nobtag_low_$ERA", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_mutau_nobtag_medium_$ERA", "shape", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_mutau_nobtag_high_$ERA", "shape", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_mutau_btag_low_$ERA", "shape", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_mutau_btag_high_$ERA", "shape", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_etau_nobtag_low_$ERA", "shape", SystMap<channel, bin_id>::init({"et"}, {10}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_etau_nobtag_medium_$ERA", "shape", SystMap<channel, bin_id>::init({"et"}, {11}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_etau_nobtag_high_$ERA", "shape", SystMap<channel, bin_id>::init({"et"}, {12}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_etau_btag_low_$ERA", "shape", SystMap<channel, bin_id>::init({"et"}, {13}, 1.000));
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_etau_btag_high_$ERA", "shape", SystMap<channel, bin_id>::init({"et"}, {14}, 1.000));
  
  src.cp().process({"ggH_SM125", "qqH_SM125", "VH_SM125"})
    .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init(1.300));
  
  src.cp()
    .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<process>::init
	     ({"qqH_SM125"}, 1.036)
	     ({"VH_SM125"}, 1.040));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));
  
  src.cp()
    .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id, process>::init
	     ({10, 11, 12}, {"ggH_SM125"}, 1.013)
	     ({10, 11, 12}, {"qqH_SM125", "VH_SM125"}, 1.050)
	     ({13, 14}, {"ggH_SM125"}, 0.946)
	     ({13, 14}, {"qqH_SM125", "VH_SM125"}, 1.007));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<channel, bin_id>::init
	     ({"mt", "et"}, {10, 11, 12}, 1.080)
	     ({"mt"}, {13, 14}, 1.105)
	     ({"et"}, {13, 14}, 1.125));
  
  src.cp().process({"qqH_SM125"})
    .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.022)
	     ({13, 14}, 1.015));
  
  src.cp().process({"VH_SM125"})
    .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.010)
	     ({13, 14}, 1.040));
  
  src.cp().process({ggH})
    .AddSyst(cb, "CMS_htt_higgsPtReweight_$ERA", "shape", SystMap<>::init(1));
  
  src.cp().process({ggH})
    .AddSyst(cb, "CMS_htt_higgsPtReweight_scale_$ERA", "shape", SystMap<channel, bin_id>::init
	     ({"mt", "et"}, {10, 11, 12, 13}, 1)
	     ({"et"}, {14}, 1));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "CMS_htt_higgsPtReweightSM_$ERA", "shape", SystMap<>::init(1.000));
}

void AddMSSMUpdateSystematics_et_mt(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_et_mt(cb, src);

}

void AddMSSMUpdateSystematics_em(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();
  src.channel({"em"});
  
  std::vector<std::string> ggH = {"ggH", "ggH_Htautau", "ggA_Atautau", "ggh_htautau"};
  std::vector<std::string> bbH = {"bbH", "bbH_Htautau", "bbA_Atautau", "bbh_htautau"};

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().process(JoinStr({signal,{"EWK", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init({"8TeV"}, 1.026));
  
  src.cp().process(JoinStr({signal,{"Ztt", "ttbar", "EWK", "Fakes", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "CMS_eff_e_$ERA", "lnN", SystMap<>::init(1.02));
  
  src.cp().process(JoinStr({signal,{"Ztt", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "CMS_scale_e_$ERA", "shape", SystMap<>::init(1));
  
  src.cp().process({"EWK"})
    .AddSyst(cb, "CMS_shift1_emu_nobtag_$ERA_EWK_fine_binning", "shape", SystMap<bin_id>::init({8}, 1.000));

  src.cp().process({"EWK"})
    .AddSyst(cb, "CMS_shift1_emu_btag_$ERA_EWK_fine_binning", "shape", SystMap<bin_id>::init({9}, 1.000));
  
  src.cp().process({"EWK"})
    .AddSyst(cb, "CMS_shift2_emu_nobtag_$ERA_EWK_fine_binning", "shape", SystMap<bin_id>::init({8}, 1.000));
  src.cp().process({"EWK"})
    .AddSyst(cb, "CMS_shift2_emu_btag_$ERA_EWK_fine_binning", "shape", SystMap<bin_id>::init({9}, 1.000));
    
  src.cp().process(JoinStr({signal,{"Ztt", "ttbar", "EWK", "Fakes", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "CMS_eff_m_$ERA", "lnN", SystMap<>::init(1.02));

  src.cp()
    .AddSyst(cb, "CMS_scale_j_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.01)
	     ({8}, {"ttbar", "EWK"}, 0.990)
	     ({9}, JoinStr({ggH, {"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.04)
	     ({9}, {bbH}, 1.01)
	     ({9}, {"ttbar"}, 0.930)
	     ({9}, {"EWK"}, 0.970));

  src.cp()
    .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8, 9}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({8}, {"ttbar"}, 0.990)
	     ({9}, {"ttbar"}, 1.010));
  
  src.cp()
    .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"EWK", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({8}, {"ttbar"}, 0.950)
	     ({9}, JoinStr({ggH, {"ggH_SM125"}}), 1.01)
	     ({9}, {bbH}, 1.05)
	     ({9}, {"ttbar"}, 1.020)
	     ({9}, {"EWK"}, 1.030));

  src.cp()
    .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"ttbar", "EWK", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({9}, JoinStr({ggH, {"ggH_SM125"}}), 1.05)
	     ({9}, {"EWK"}, 1.030));

  src.cp().process({"Ztt"})
    .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.030));
  
  src.cp().process({"Ztt"})
    .AddSyst(cb, "CMS_htt_extrap_ztt_$CHANNEL_btag_$ERA", "lnN", SystMap<bin_id>::init({9}, 1.010));
  
  src.cp().process({"ttbar"})
    .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.100));
  
  src.cp().process({"EWK"})
    .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.150));

  src.cp().process({"Fakes"})
    .AddSyst(cb, "CMS_htt_fakes_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.300));
  
  src.cp().process({"Fakes"})
    .AddSyst(cb, "CMS_htt_fakes_$CHANNEL_btag_$ERA", "lnN", SystMap<bin_id>::init({9}, 1.090));
  
  src.cp().process({"ttbar"})
    .AddSyst(cb, "CMS_htt_ttbar_emb_$ERA", "lnN", SystMap<bin_id>::init({9}, 1.020));
  
  src.cp().process({"Fakes"})
    .AddSyst(cb, "CMS_htt_FakeShape_$CHANNEL_nobtag_$ERA", "shape", SystMap<bin_id>::init({8}, 1.000));
  src.cp().process({"Fakes"})
    .AddSyst(cb, "CMS_htt_FakeShape_$CHANNEL_btag_$ERA", "shape", SystMap<bin_id>::init({9}, 1.000));
  
  src.cp().process({"ttbar"})
    .AddSyst(cb, "CMS_htt_TTbarShape_$CHANNEL_nobtag_$ERA", "shape", SystMap<bin_id>::init({8}, 1.000));
  src.cp().process({"ttbar"})
    .AddSyst(cb, "CMS_htt_TTbarShape_$CHANNEL_btag_$ERA", "shape", SystMap<bin_id>::init({9}, 1.000));
  
  src.cp().process({"ggH_SM125", "qqH_SM125", "VH_SM125"})
    .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init(1.300));
  
  src.cp()
    .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<bin_id, process>::init
	     ({8, 9}, {"qqH_SM125"}, 1.036)
	     ({8}, {"VH_SM125"}, 1.010)
	     ({9}, {"VH_SM125"}, 1.020));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<bin_id>::init
	     ({8}, 1.080)
	     ({9}, 1.105));
  
  src.cp().process({"qqH_SM125"})
    .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
	     ({8}, 1.034)
	     ({9}, 1.008));

  src.cp().process({"VH_SM125"})
    .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init(1.040));

  src.cp()
    .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id, process>::init
	     ({8}, {"ggH_SM125"}, 1.035)
	     ({9}, {"ggH_SM125"}, 0.984)
	     ({8}, {"qqH_SM125", "VH_SM125"}, 1.089));
}

void AddMSSMUpdateSystematics_em(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_em(cb, src);

}

void AddMSSMUpdateSystematics_mm(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();
  src.channel({"mm"});

  std::vector<std::string> ggH = {"ggH", "ggH_Htautau", "ggA_Atautau", "ggh_htautau"};
  std::vector<std::string> bbH = {"bbH", "bbH_Htautau", "bbA_Atautau", "bbh_htautau"};

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp()
    .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<bin_id, process, era>::init
	     ({8, 9}, JoinStr({signal,{"Dibosons", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), {"8TeV"}, 1.026)
	     ({8}, {"WJets"}, {"8TeV"}, 1.026));

  src.cp()
    .AddSyst(cb, "CMS_eff_m_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8, 9}, JoinStr({signal,{"ZTT", "TTJ", "Dibosons", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.06)
	     ({8}, {"WJets"}, 1.060));
  
  src.cp()
    .AddSyst(cb, "CMS_scale_j_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.02)
	     ({8}, {"TTJ", "WJets", "Dibosons"}, 0.990)
	     ({9}, JoinStr({ggH,{"ggH_SM125"}}), 0.98)
	     ({9}, {bbH}, 1.01)
	     ({9}, {"TTJ"}, 0.920)
	     ({9}, {"Dibosons"}, 0.950));

  src.cp()
    .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({8}, {"TTJ"}, 0.940)
	     ({8}, {"WJets", "Dibosons"}, 0.970)
	     ({9}, JoinStr({ggH, {"ggH_SM125"}}), 1.01)
	     ({9}, {bbH}, 1.05)
	     ({9}, {"TTJ"}, 1.020)
	     ({9}, {"Dibosons"}, 1.030));

  src.cp()
    .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({8}, JoinStr({signal,{"TqTJ", "WJets", "Dibosons", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({9}, JoinStr({ggH, {"ggH_SM125"}}), 1.06)
	     ({9}, {"Dibosons"}, 1.050));

  src.cp().process({"ZTT"})
    .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.050));
  
  src.cp().process({"TTJ"})
    .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.100));
  
  src.cp().process({"Dibosons"})
    .AddSyst(cb, "CMS_htt_$CHANNEL_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.300));
  
  src.cp().process({"ZMM"})
    .AddSyst(cb, "CMS_htt_$CHANNEL_zmmNorm_$ERA", "lnN", SystMap<>::init(1.050));

  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_$CHANNEL_QCDNorm_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({8}, 1.100)
	     ({9}, 1.250));
  
  src.cp().process({"WJets"})
    .AddSyst(cb, "CMS_htt_$CHANNEL_WJetsNorm_nobtag_$ERA", "lnN", SystMap<bin_id>::init({8}, 1.220));
  
  src.cp().process({"ZMM"})
    .AddSyst(cb, "CMS_htt_$CHANNEL_res_met_$ERA", "shape", SystMap<bin_id>::init({8}, 1.000));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_$CHANNEL_ztt_extrap_btag_$ERA", "lnN", SystMap<bin_id>::init({9}, 1.050));

  src.cp().process({"ZMM"})
      .AddSyst(cb, "CMS_htt_$CHANNEL_zmm_extrap_btag_$ERA", "lnN", SystMap<bin_id>::init({9}, 1.050));
    
  src.cp().process({"ggH_SM125", "qqH_SM125", "VH_SM125"})
    .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init(1.300));
  
  src.cp().process({"qqH_SM125"})
    .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<>::init(1.036));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));
  
  src.cp().process({"VH_SM125"})
    .AddSyst(cb, "pdf_vh", "lnN", SystMap<>::init(1.010));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<bin_id>::init
	     ({8}, 1.103)
	     ({9}, 1.109));
  
  src.cp().process({"qqH_SM125"})
    .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
	     ({8}, 1.034)
	     ({9}, 1.008));
  
  src.cp().process({"VH_SM125"})
    .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init(1.040));
  
  src.cp()
    .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id, process>::init
	     ({8}, {"ggH_SM125"}, 1.035)
	     ({8}, {"qqH_SM125", "VH_SM125"}, 1.089)
	     ({9}, {"ggH_SM125"}, 0.984)
	     ({9}, {"qqH_SM125", "VH_SM125"}, 1.000));
}

void AddMSSMUpdateSystematics_mm(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_mm(cb, src);

}

void AddMSSMUpdateSystematics_tt(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();
  src.channel({"tt"});

  std::vector<std::string> ggH = {"ggH", "ggH_Htautau", "ggA_Atautau", "ggh_htautau"};
  std::vector<std::string> bbH = {"bbH", "bbH_Htautau", "bbA_Atautau", "bbh_htautau"};

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().process(JoinStr({signal,{"ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init({"8TeV"}, 1.026));
  
  src.cp().process(JoinStr({signal,{"ZTT", "TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}}))
    .AddSyst(cb, "CMS_eff_t_tautau_$ERA", "lnN", SystMap<>::init(1.19));
  
  src.cp().process(JoinStr({signal}))
    .AddSyst(cb, "CMS_eff_t_mssmHigh_tautau_$ERA", "shape", SystMap<>::init(1));
  
  src.cp().process(JoinStr({signal,{"ZTT"}}))
    .AddSyst(cb, "CMS_scale_t_tautau_$ERA", "shape", SystMap<>::init(1));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_tauTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_tauTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_tauTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_tauTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift1_tauTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({14}, 1.000));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_tauTau_nobtag_low_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({10}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_tauTau_nobtag_medium_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({11}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_tauTau_nobtag_high_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({12}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_tauTau_btag_low_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({13}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_shift2_tauTau_btag_high_$ERA_QCD_fine_binning", "shape", SystMap<bin_id>::init({14}, 1.000));

  src.cp()
    .AddSyst(cb, "CMS_scale_j_$ERA", "lnN", SystMap<process>::init
	     ({ggH}, 1.05)
	     ({bbH}, 1.06)
	     ({"TT"}, 1.010)
	     ({"VV"}, 1.030)
	     ({"ggH_SM125"}, 1.050));

  src.cp()
    .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({10, 11, 12}, JoinStr({signal,{"ZJ", "TT", "VV", "ZL", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({13, 14}, JoinStr({signal,{"TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.09));

  src.cp()
    .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<bin_id, process>::init
	     ({10, 11, 12}, JoinStr({signal,{"ZJ", "TT", "VV", "ZL", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 0.98)
	     ({13, 14}, JoinStr({signal,{"TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}}), 1.02));
  
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WNorm_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12, 13}, 1.300)
	     ({14}, 1.500));
  
  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDSyst_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.100)
	     ({13, 14}, 1.200));
  
  src.cp().process({"QCD"})
    .AddSyst(cb, "CMS_htt_QCDfrShape_tautau_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"ZTT", "ZJ", "ZL"})
    .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.033));

  src.cp().process({"ZTT"})
    .AddSyst(cb, "CMS_htt_extrap_ztt_$CHANNEL_$BIN_$ERA", "lnN", SystMap<bin_id>::init
	     ({10, 11, 12}, 1.050)
	     ({13}, 1.090)
	     ({14}, 1.180));

  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.100));

  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarNorm_$CHANNEL_$bin_$ERA", "lnN", SystMap<>::init(1.050));
  
  src.cp().process({"TT"})
    .AddSyst(cb, "CMS_htt_ttbarPtReweight_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"VV"})
    .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.150));
  
  src.cp().process({"VV"})
    .AddSyst(cb, "CMS_htt_DiBosonNorm_$CHANNEL_$BIN_$ERA", "lnN", SystMap<>::init(1.150));
  
  src.cp().process({"ZJ"})
    .AddSyst(cb, "CMS_htt_ZJetFakeTau_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.200));
  
  src.cp().process({"ZL"})
    .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.200));
  
  src.cp().process({"W"})
    .AddSyst(cb, "CMS_htt_WShape_tautau_$ERA", "shape", SystMap<>::init(1.000));
  
  src.cp().process({"ggH_SM125", "qqH_SM125", "VH_SM125"})
    .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init(1.300));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));
  
  src.cp()
    .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<process>::init
	     ({"qqH_SM125"}, 1.036)
	     ({"VH_SM125"}, 1.020));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<>::init(1.205));
  
  src.cp().process({"qqH_SM125"})
    .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<>::init(1.012));
  
  src.cp().process({"VH_SM125"})
    .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init(1.040));
  
  src.cp()
    .AddSyst(cb, "UEPS", "lnN", SystMap<process>::init
	     ({"ggH_SM125"}, 0.975)
	     ({"qqH_SM125", "VH_SM125"}, 1.025));
  
  src.cp().process({ggH})
    .AddSyst(cb, "CMS_htt_higgsPtReweight_$ERA", "shape", SystMap<>::init(1));
  
  src.cp().process({"ggH_SM125"})
    .AddSyst(cb, "CMS_htt_higgsPtReweightSM_$ERA", "shape", SystMap<>::init(1.000));
}

void AddMSSMUpdateSystematics_tt(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_tt(cb, src);

}

}
