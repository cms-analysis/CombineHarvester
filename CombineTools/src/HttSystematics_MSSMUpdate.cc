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

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init({"8TeV"}, 1.026));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel>::init({"mt"}, 1.010));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel>::init({"et"}, 1.020));

  src.cp()
      .AddSyst(cb, "CMS_eff_t_mutau_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	({"mt"}, {10, 11, 12, 13, 14}, {"ggH", "bbH"}, 1.08)
	({"mt"}, {10, 11, 12, 13, 14}, {"ZTT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.080)
	({"mt"}, {10, 11, 12}, {"TT"}, 1.080)
	);
  src.cp()
      .AddSyst(cb, "CMS_eff_t_etau_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	({"et"}, {10, 11, 12, 13}, {"ggH", "bbH"}, 1.08)
	({"et"}, {10, 11, 12, 13}, {"ZTT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.080)
	({"et"}, {10, 11, 12}, {"TT"}, 1.080)
	);

  src.cp()
      .AddSyst(cb, "CMS_eff_t_mssmHigh_mutau_$ERA", "shape", SystMap<channel, process>::init
	({"mt"}, {"ggH", "bbH"}, 1)
	({"mt"}, {"ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.000)
	);
  src.cp()
      .AddSyst(cb, "CMS_eff_t_mssmHigh_etau_$ERA", "shape", SystMap<channel, process>::init
	({"et"}, {"ggH", "bbH"}, 1)
	({"et"}, {"ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.000)
	);

  src.cp()
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<channel, process>::init
	({"mt"}, {"ggH", "bbH"}, 1)
	({"mt"}, {"ZTT", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.000)
	);
  src.cp()
      .AddSyst(cb, "CMS_scale_t_etau_$ERA", "shape", SystMap<channel, process>::init
	({"et"}, {"ggH", "bbH"}, 1)
	({"et"}, {"ZTT", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.000)
	);

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_shift1_muTau_nobtag_low_$ERA_W_fine_binning", "shape", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.000));
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
	({"mt", "et"}, {10, 11, 12}, {"bbH"}, 0.99)
	({"mt", "et"}, {10, 11, 12}, {"TT"}, 0.990)
	({"mt"}, {13, 14}, {"ggH"}, 0.99)
	({"mt"}, {13, 14}, {"bbH"}, 1.01)
	({"mt"}, {13, 14}, {"ZJ"}, 0.980)
	({"mt"}, {13, 14}, {"ZL"}, 0.980)
	({"mt"}, {13, 14}, {"TT"}, 0.920)
	({"mt"}, {13, 14}, {"VV"}, 0.980)
	({"mt"}, {13, 14}, {"ggH_SM125"}, 0.990)
	({"et"}, {13, 14}, {"ggH"}, 1.03)
	({"et"}, {13, 14}, {"bbH"}, 1.01)
	({"et"}, {13, 14}, {"ZJ"}, 1.060)
	({"et"}, {13, 14}, {"ZL"}, 0.960)
	({"et"}, {13, 14}, {"TT"}, 0.900)
	({"et"}, {13, 14}, {"VV"}, 0.940)
	({"et"}, {13, 14}, {"ggH_SM125"}, 1.030)
	);

  src.cp()
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN", SystMap<bin_id, process>::init
	({10, 11, 12, 13, 14}, {"ggH", "bbH"}, 0.99)
	({10, 11, 12, 13, 14}, {"ZJ", "ZL", "TT"}, 1.010)
	({10, 11, 12, 13, 14}, {"ggH_SM125", "qqH_SM125", "VH_SM125"}, 0.990)
	({13, 14}, {"W"}, 1.010)
	);

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	({"et", "mt"}, {10, 11, 12}, {"bbH"}, 0.99)
	({"et", "mt"}, {10, 11, 12}, {"TT"}, 0.950)
	({"mt"}, {10, 11, 12}, {"VV"}, 0.980)
	({"et"}, {10, 11, 12}, {"VV"}, 0.990)
	({"mt"}, {13, 14}, {"ggH"}, 1.01)
	({"mt"}, {13, 14}, {"bbH"}, 1.03)
	({"mt"}, {13, 14}, {"ZL"}, 1.040)
	({"mt"}, {13, 14}, {"TT"}, 1.020)
	({"mt"}, {13, 14}, {"VV"}, 1.040)
	({"mt"}, {13, 14}, {"ggH_SM125"}, 1.010)
	({"et"}, {13, 14}, {"ggH"}, 1.01)
	({"et"}, {13, 14}, {"bbH"}, 1.02)
	({"et"}, {13, 14}, {"ZL"}, 1.020)
	({"et"}, {13, 14}, {"ZJ"}, 1.040)
	({"et"}, {13, 14}, {"TT"}, 1.040)
	({"et"}, {13, 14}, {"VV"}, 1.040)
	({"et"}, {13, 14}, {"ggH_SM125"}, 1.010)
	);

  src.cp()
      .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<channel, bin_id, process>::init
	({"mt", "et"}, {10, 11, 12}, {"TT"}, 0.970)
	({"mt", "et"}, {10, 11, 12}, {"VV"}, 0.990)
	({"mt"}, {13, 14}, {"ggH"}, 1.05)
	({"mt"}, {13, 14}, {"ZL"}, 1.050)
	({"mt"}, {13, 14}, {"ZJ"}, 1.090)
	({"mt"}, {13, 14}, {"TT"}, 1.010)
	({"mt"}, {13, 14}, {"VV"}, 1.010)
	({"mt"}, {13, 14}, {"ggH_SM125"}, 1.050)
	({"et"}, {13, 14}, {"ggH"}, 1.03)
	({"et"}, {13, 14}, {"ZL"}, 1.020)
	({"et"}, {13, 14}, {"ZJ"}, 1.090)
	({"et"}, {13, 14}, {"TT"}, 1.010)
	({"et"}, {13, 14}, {"VV"}, 1.010)
	({"et"}, {13, 14}, {"ggH_SM125"}, 1.030)
	);

  src.cp().process({"ZTT", "ZJ", "ZL"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.030));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_mutau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_mutau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_mutau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_mutau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_etau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {11}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_etau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {12}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_etau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {13}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_etau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {14}, 1.050));

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
      .AddSyst(cb, "CMS_htt_WNorm_mutau_nobtag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_mutau_nobtag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {10}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_mutau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_mutau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {11}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_mutau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_mutau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_mutau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.300));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_mutau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {13}, 1.200));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_mutau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.500));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_mutau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {14}, 1.200));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_etau_nobtag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {10}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_etau_nobtag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {10}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_etau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {11}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_etau_nobtag_medium_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {11}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_etau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {12}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_etau_nobtag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {12}, 1.100));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_etau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {13}, 1.300));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_etau_btag_low_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {13}, 1.200));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_etau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {14}, 1.500));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_etau_btag_high_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {14}, 1.200));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDfrShape_mutau_$ERA", "shape", SystMap<channel>::init({"mt"}, 1.000));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDfrShape_etau_$ERA", "shape", SystMap<channel>::init({"et"}, 1.000));

  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_mutau_$ERA", "lnN", SystMap<channel>::init({"mt"}, 1.200));
  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_etau_$ERA", "lnN", SystMap<channel>::init({"et"}, 1.200));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_mutau_low_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {10, 13}, 1.300));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_mutau_medium_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {11, 14}, 1.300));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_mutau_high_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"mt"}, {12}, 1.300));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_etau_low_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {10, 13}, 1.200));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_etau_medium_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {11, 14}, 1.200));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_etau_high_pTtau_$ERA", "lnN", SystMap<channel, bin_id>::init({"et"}, {12}, 1.200));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLScale_mutau_$ERA", "shape", SystMap<channel>::init({"mt"}, 1.000));
  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLScale_etau_$ERA", "shape", SystMap<channel>::init({"et"}, 1.000));

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
	({"VH_SM125"}, 1.040)
	);

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  src.cp()
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id, process>::init
	({10, 11, 12}, {"ggH_SM125"}, 1.013)
	({10, 11, 12}, {"qqH_SM125", "VH_SM125"}, 1.050)
	({13, 14}, {"ggH_SM125"}, 0.946)
	({13, 14}, {"qqH_SM125", "VH_SM125"}, 1.007)
	);

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<channel, bin_id>::init
	({"mt", "et"}, {10, 11, 12}, 1.080)
	({"mt"}, {13, 14}, 1.105)
	({"et"}, {13, 14}, 1.125)
	);

  src.cp().process({"qqH_SM125"})
      .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
	({10, 11, 12}, 1.022)
	({13, 14}, 1.015)
	);

  src.cp().process({"VH_SM125"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<bin_id>::init
	({10, 11, 12}, 1.010)
	({13, 14}, 1.040)
	);

  src.cp().process({"ggH"})
      .AddSyst(cb, "CMS_htt_higgsPtReweight_$ERA", "shape", SystMap<>::init(1));

  src.cp().process({"ggH"})
      .AddSyst(cb, "CMS_htt_higgsPtReweight_scale_$ERA", "shape", SystMap<channel, bin_id>::init
	({"mt", "et"}, {10, 11, 12, 13}, 1)
	({"et"}, {14}, 1)
	);

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "CMS_htt_higgsPtReweightSM_$ERA", "shape", SystMap<>::init(1.000));

}

void AddMSSMUpdateSystematics_et_mt(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_et_mt(cb, src);

}

void AddMSSMUpdateSystematics_em(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"7TeV"}, 1.026)
      ({"8TeV"}, 1.026));

  src.cp().process(JoinStr({signal, {"ZTT", "ZL", "ZJ", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.08));

  src.cp().process(JoinStr({signal, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp().process(JoinStr({signal})).AddSyst(
      cb, "CMS_eff_t_mssmHigh_mutau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {9},     {"ggH"},            1.05)
        ({"7TeV"}, {9},     {"bbH"},            0.96)
        ({"7TeV"}, {9},     {"TT"},             1.10)
        ({"7TeV"}, {9},     {"VV"},             1.03)
        ({"8TeV"}, {8},     {"bbH", "TT"},      0.99)
        ({"8TeV"}, {9},     {"ggH"},            0.99)
        ({"8TeV"}, {9},     {"bbH"},            1.01)
        ({"8TeV"}, {9},     {"TT"},             0.92)
        ({"8TeV"}, {9},     {"VV", "ZL", "ZJ"}, 0.98)
        );

  src.cp()
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN",
        SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                1.05)
        ({"7TeV"}, {8},  {"ZL", "ZJ"},            1.05)
        ({"7TeV"}, {8},  {"TT", "VV"},            1.07)
        ({"7TeV"}, {9},  {signal},                1.05)
        ({"7TeV"}, {9},  {"TT", "VV"},            1.07)
        ({"8TeV"}, {8},  {signal},                0.99)
        ({"8TeV"}, {8},  {"TT", "ZL", "ZJ"},      1.01)
        ({"8TeV"}, {9},  {signal},                0.99)
        ({"8TeV"}, {9},  {"TT", "W", "ZL", "ZJ"}, 1.01));

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                  0.99)
        ({"7TeV"}, {8},  {"ZL", "ZJ", "TT", "VV"},  0.99)
        ({"7TeV"}, {9},  {signal},                  1.06)
        ({"7TeV"}, {9},  {"ZL", "ZJ", "TT", "VV"},  1.06)
        ({"8TeV"}, {8},  {"bbH"},                   0.99)
        ({"8TeV"}, {8},  {"VV"},                    0.98)
        ({"8TeV"}, {8},  {"TT"},                    0.95)
        ({"8TeV"}, {9},  {"bbH"},                   1.03)
        ({"8TeV"}, {9},  {"ggH"},                   1.01)
        ({"8TeV"}, {9},  {"ZL", "VV"},              1.04)
        ({"8TeV"}, {9},  {"TT"},                    1.02));

  src.cp()
      .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                  0.99)
        ({"7TeV"}, {8},  {"ZL", "ZJ", "TT", "VV"},  0.99)
        ({"7TeV"}, {9},  {signal},                  1.01)
        ({"7TeV"}, {9},  {"ZL", "ZJ", "TT", "VV"},  1.01)
        ({"8TeV"}, {8},  {"VV"},                    0.99)
        ({"8TeV"}, {8},  {"TT"},                    0.97)
        ({"8TeV"}, {9},  {"ggH"},                   1.05)
        ({"8TeV"}, {9},  {"TT", "VV"},              1.01)
        ({"8TeV"}, {9},  {"ZL"},                    1.05)
        ({"8TeV"}, {9},  {"ZJ"},                    1.09));

  src.cp().process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.03));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({9},   1.03));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8, 9},  1.08)
        ({"8TeV"}, {8, 9},  1.10));

  src.cp().process({"TT"})
      .AddSyst(cb,
      "CMS_htt_ttbar_emb_$ERA", "lnN", SystMap<era, bin_id>::init
      ({"7TeV", "8TeV"}, {9},     1.14));

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8},    1.10)
        ({"7TeV"}, {9},    1.30)
        ({"8TeV"}, {8},    1.10)
        ({"8TeV"}, {9},    1.30));

  src.cp().process({"W"}).bin_id({8})
      .AddSyst(cb, "CMS_htt_WShape_mutau_nobtag_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"W"}).bin_id({9})
      .AddSyst(cb, "CMS_htt_WShape_mutau_btag_$ERA", "shape",
        SystMap<>::init(1.00));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.15));

  src.cp().process({"QCD"})
      .AddSyst(cb,
      "CMS_htt_QCDSyst_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8},               1.10)
        ({"7TeV"}, {9},               1.20)
        ({"8TeV"}, {8},               1.10)
        ({"8TeV"}, {9},               1.20));

  src.cp().process({"QCD"}).bin_id({8})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_nobtag_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"QCD"}).bin_id({9})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_btag_$ERA", "shape",
        SystMap<>::init(1.00));

  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({8},     1.20)
        ({9},     1.20));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_$ERA", "lnN",
        SystMap<>::init(1.30));

  src.cp().process({"ZL"})
      .AddSyst(cb,
      "CMS_htt_ZLScale_mutau_$ERA", "shape", SystMap<>::init(1.00));
}

void AddMSSMUpdateSystematics_em(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_em(cb, src);

}

void AddMSSMUpdateSystematics_mm(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"7TeV"}, 1.026)
      ({"8TeV"}, 1.026));

  src.cp().process(JoinStr({signal, {"ZTT", "ZL", "ZJ", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.08));

  src.cp().process(JoinStr({signal, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp().process(JoinStr({signal})).AddSyst(
      cb, "CMS_eff_t_mssmHigh_mutau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {9},     {"ggH"},            1.05)
        ({"7TeV"}, {9},     {"bbH"},            0.96)
        ({"7TeV"}, {9},     {"TT"},             1.10)
        ({"7TeV"}, {9},     {"VV"},             1.03)
        ({"8TeV"}, {8},     {"bbH", "TT"},      0.99)
        ({"8TeV"}, {9},     {"ggH"},            0.99)
        ({"8TeV"}, {9},     {"bbH"},            1.01)
        ({"8TeV"}, {9},     {"TT"},             0.92)
        ({"8TeV"}, {9},     {"VV", "ZL", "ZJ"}, 0.98)
        );

  src.cp()
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN",
        SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                1.05)
        ({"7TeV"}, {8},  {"ZL", "ZJ"},            1.05)
        ({"7TeV"}, {8},  {"TT", "VV"},            1.07)
        ({"7TeV"}, {9},  {signal},                1.05)
        ({"7TeV"}, {9},  {"TT", "VV"},            1.07)
        ({"8TeV"}, {8},  {signal},                0.99)
        ({"8TeV"}, {8},  {"TT", "ZL", "ZJ"},      1.01)
        ({"8TeV"}, {9},  {signal},                0.99)
        ({"8TeV"}, {9},  {"TT", "W", "ZL", "ZJ"}, 1.01));

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                  0.99)
        ({"7TeV"}, {8},  {"ZL", "ZJ", "TT", "VV"},  0.99)
        ({"7TeV"}, {9},  {signal},                  1.06)
        ({"7TeV"}, {9},  {"ZL", "ZJ", "TT", "VV"},  1.06)
        ({"8TeV"}, {8},  {"bbH"},                   0.99)
        ({"8TeV"}, {8},  {"VV"},                    0.98)
        ({"8TeV"}, {8},  {"TT"},                    0.95)
        ({"8TeV"}, {9},  {"bbH"},                   1.03)
        ({"8TeV"}, {9},  {"ggH"},                   1.01)
        ({"8TeV"}, {9},  {"ZL", "VV"},              1.04)
        ({"8TeV"}, {9},  {"TT"},                    1.02));

  src.cp()
      .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {8},  {signal},                  0.99)
        ({"7TeV"}, {8},  {"ZL", "ZJ", "TT", "VV"},  0.99)
        ({"7TeV"}, {9},  {signal},                  1.01)
        ({"7TeV"}, {9},  {"ZL", "ZJ", "TT", "VV"},  1.01)
        ({"8TeV"}, {8},  {"VV"},                    0.99)
        ({"8TeV"}, {8},  {"TT"},                    0.97)
        ({"8TeV"}, {9},  {"ggH"},                   1.05)
        ({"8TeV"}, {9},  {"TT", "VV"},              1.01)
        ({"8TeV"}, {9},  {"ZL"},                    1.05)
        ({"8TeV"}, {9},  {"ZJ"},                    1.09));

  src.cp().process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.03));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({9},   1.03));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8, 9},  1.08)
        ({"8TeV"}, {8, 9},  1.10));

  src.cp().process({"TT"})
      .AddSyst(cb,
      "CMS_htt_ttbar_emb_$ERA", "lnN", SystMap<era, bin_id>::init
      ({"7TeV", "8TeV"}, {9},     1.14));

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8},    1.10)
        ({"7TeV"}, {9},    1.30)
        ({"8TeV"}, {8},    1.10)
        ({"8TeV"}, {9},    1.30));

  src.cp().process({"W"}).bin_id({8})
      .AddSyst(cb, "CMS_htt_WShape_mutau_nobtag_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"W"}).bin_id({9})
      .AddSyst(cb, "CMS_htt_WShape_mutau_btag_$ERA", "shape",
        SystMap<>::init(1.00));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.15));

  src.cp().process({"QCD"})
      .AddSyst(cb,
      "CMS_htt_QCDSyst_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {8},               1.10)
        ({"7TeV"}, {9},               1.20)
        ({"8TeV"}, {8},               1.10)
        ({"8TeV"}, {9},               1.20));

  src.cp().process({"QCD"}).bin_id({8})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_nobtag_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"QCD"}).bin_id({9})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_btag_$ERA", "shape",
        SystMap<>::init(1.00));

  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({8},     1.20)
        ({9},     1.20));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_$ERA", "lnN",
        SystMap<>::init(1.30));

  src.cp().process({"ZL"})
      .AddSyst(cb,
      "CMS_htt_ZLScale_mutau_$ERA", "shape", SystMap<>::init(1.00));
}

void AddMSSMUpdateSystematics_mm(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_mm(cb, src);

}

void AddMSSMUpdateSystematics_tt(CombineHarvester & cb, CombineHarvester src) {
  //CombineHarvester src = cb.cp();
  src.channel({"tt"});

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init({"8TeV"}, 1.026));

  src.cp()
      .AddSyst(cb, "CMS_eff_t_tautau_$ERA", "lnN", SystMap<process>::init
	({"ggH", "bbH"}, 1.19)
	({"ZTT", "TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.190)
	);

  src.cp()
      .AddSyst(cb, "CMS_eff_t_mssmHigh_tautau_$ERA", "shape", SystMap<process>::init({"ggH", "bbH"}, 1));

  src.cp()
      .AddSyst(cb, "CMS_scale_t_tautau_$ERA", "shape", SystMap<process>::init
	({"ggH", "bbH"}, 1)
	({"ZTT"}, 1.000)
	);

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
	({"ggH"}, 1.05)
	({"bbH"}, 1.06)
	({"TT"}, 1.010)
	({"VV"}, 1.030)
	({"ggH_SM125"}, 1.050)
	);

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<bin_id, process>::init
	({10, 11, 12}, {"ggH", "bbH"}, 0.98)
	({10, 11, 12}, {"ZJ", "TT", "VV", "ZL", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 0.980)
	({13, 14}, {"ggH", "bbH"}, 1.09)
	({13, 14}, {"TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.090)
	);

  src.cp()
      .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<bin_id, process>::init
	({10, 11, 12}, {"ggH", "bbH"}, 0.98)
	({10, 11, 12}, {"ZJ", "TT", "VV", "ZL", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 0.980)
	({13, 14}, {"ggH", "bbH"}, 1.02)
	({13, 14}, {"TT", "VV", "ggH_SM125", "qqH_SM125", "VH_SM125"}, 1.020)
	);

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_tautau_nobtag_low_$ERA", "lnN", SystMap<bin_id>::init({10}, 1.300));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_tautau_nobtag_medium_$ERA", "lnN", SystMap<bin_id>::init({11}, 1.300));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_tautau_nobtag_high_$ERA", "lnN", SystMap<bin_id>::init({12}, 1.300));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_tautau_btag_low_$ERA", "lnN", SystMap<bin_id>::init({13}, 1.300));
  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_tautau_btag_high_$ERA", "lnN", SystMap<bin_id>::init({14}, 1.500));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_tautau_nobtag_low_$ERA", "lnN", SystMap<bin_id>::init({10}, 1.100));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_tautau_nobtag_medium_$ERA", "lnN", SystMap<bin_id>::init({11}, 1.100));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_tautau_nobtag_high_$ERA", "lnN", SystMap<bin_id>::init({12}, 1.100));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_tautau_btag_low_$ERA", "lnN", SystMap<bin_id>::init({13}, 1.200));
  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_tautau_btag_high_$ERA", "lnN", SystMap<bin_id>::init({14}, 1.200));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDfrShape_tautau_$ERA", "shape", SystMap<>::init(1.000));

  src.cp().process({"ZTT", "ZJ", "ZL"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.033));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_tautau_nobtag_low_$ERA", "lnN", SystMap<bin_id>::init({10}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_tautau_nobtag_medium_$ERA", "lnN", SystMap<bin_id>::init({11}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_tautau_nobtag_high_$ERA", "lnN", SystMap<bin_id>::init({12}, 1.050));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_tautau_btag_low_$ERA", "lnN", SystMap<bin_id>::init({13}, 1.090));
  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_tautau_btag_high_$ERA", "lnN", SystMap<bin_id>::init({14}, 1.180));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.100));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_tautau_nobtag_low_$ERA", "lnN", SystMap<bin_id>::init({10}, 1.050));
  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_tautau_nobtag_medium_$ERA", "lnN", SystMap<bin_id>::init({11}, 1.050));
  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_tautau_nobtag_high_$ERA", "lnN", SystMap<bin_id>::init({12}, 1.050));
  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_tautau_btag_low_$ERA", "lnN", SystMap<bin_id>::init({13}, 1.050));
  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_tautau_btag_high_$ERA", "lnN", SystMap<bin_id>::init({14}, 1.050));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarPtReweight_$ERA", "shape", SystMap<>::init(1.000));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.150));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_tautau_nobtag_low_$ERA", "lnN", SystMap<bin_id>::init({10}, 1.150));
  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_tautau_nobtag_medium_$ERA", "lnN", SystMap<bin_id>::init({11}, 1.150));
  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_tautau_nobtag_high_$ERA", "lnN", SystMap<bin_id>::init({12}, 1.150));
  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_tautau_btag_low_$ERA", "lnN", SystMap<bin_id>::init({13}, 1.150));
  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_tautau_btag_high_$ERA", "lnN", SystMap<bin_id>::init({14}, 1.150));

  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_tautau_$ERA", "lnN", SystMap<>::init(1.200));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_tautau_$ERA", "lnN", SystMap<>::init(1.200));

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WShape_tautau_$ERA", "shape", SystMap<>::init(1.000));

  src.cp().process({"ggH_SM125", "qqH_SM125", "VH_SM125"})
      .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init(1.300));

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  src.cp()
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<process>::init
	({"qqH_SM125"}, 1.036)
	({"VH_SM125"}, 1.020)
	);

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<>::init(1.205));

  src.cp().process({"qqH_SM125"})
      .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<>::init(1.012));

  src.cp().process({"VH_SM125"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init(1.040));

  src.cp()
      .AddSyst(cb, "UEPS", "lnN", SystMap<process>::init
	({"ggH_SM125"}, 0.975)
	({"qqH_SM125", "VH_SM125"}, 1.025)
	);

  src.cp().process({"ggH"})
      .AddSyst(cb, "CMS_htt_higgsPtReweight_$ERA", "shape", SystMap<>::init(1));

  src.cp().process({"ggH_SM125"})
      .AddSyst(cb, "CMS_htt_higgsPtReweightSM_$ERA", "shape", SystMap<>::init(1.000));

}

void AddMSSMUpdateSystematics_tt(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMUpdateSystematics_tt(cb, src);

}

}
