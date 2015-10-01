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

void AddMSSMSystematics(CombineHarvester & cb, CombineHarvester src) {
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

void AddMSSMSystematics(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddMSSMSystematics(cb, src);

}

}
