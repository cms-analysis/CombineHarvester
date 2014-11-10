#include "CombineTools/interface/HttSystematics.h"
#include <string>
#include "CombineTools/interface/Systematics.h"
#include "CombineTools/interface/Process.h"
#include "CombineTools/interface/Utilities.h"

namespace ch {

using ch::syst::SystMap;
using ch::syst::SystMapAsymm;
using ch::syst::era;
using ch::syst::channel;
using ch::syst::bin_id;
using ch::syst::process;
using ch::JoinStr;

/**
 * @brief Add systematics for the ee and mm channels
 *
 * @param cb Pointer to the CombineHarvester instance where these uncertainties
 *should be added
 * @param src Pointer to the CombineHarvester instance that contains the subset
 *of relevant processes (e.g. just the ee and mm channels)
 */
void AddSystematics_ee_mm(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();
  src.channel({"ee", "mm"});

  // This regular expression will match any Higgs signal process.
  // It's useful for catching all these processes when we don't know
  // which of them will be signal or background
  std::string higgs_rgx = "^(qq|gg|[WZV])H.*$";

  auto signal = Set2Vec(src.cp().signals().process_set());

  // Lumi not added for ggH_hww125 type processes
  src.cp().process({"qqH", "ggH", "WH", "ZH", "Dibosons", "WJets"})
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
        ({"7TeV"}, 1.022)
        ({"8TeV"}, 1.026));

  src.cp().channel({"ee"})
      .process_rgx({higgs_rgx, "ZTT", "TTJ", "WJets", "Dibosons"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<era>::init
        ({"7TeV"}, 1.04)
        ({"8TeV"}, 1.06));

  src.cp().channel({"mm"})
      .process_rgx({higgs_rgx, "ZTT", "TTJ", "WJets", "Dibosons"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<era>::init
        ({"7TeV"}, 1.04)
        ({"8TeV"}, 1.04));

  src.cp().channel({"ee"})
      .process_rgx({higgs_rgx, "ZTT", "TTJ", "Dibosons"})
      .AddSyst(cb, "CMS_scale_e_$ERA", "shape", SystMap<>::init(0.50));

  src.cp().process_rgx({higgs_rgx, "TTJ", "Dibosons"})
      .AddSyst(cb, "CMS_scale_j_$ERA", "shape", SystMap<>::init(0.50));

  src.cp().channel({"ee"}).process_rgx({higgs_rgx, "TTJ", "Dibosons"}).bin_id({4})
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "shape", SystMap<>::init(0.50));

  src.cp().channel({"mm"}).process_rgx({higgs_rgx, "Dibosons"}).bin_id({4})
      .AddSyst(cb, "CMS_htt_scale_met_SignalDibosonWjets_$ERA", "shape", SystMap<>::init(0.50));

  src.cp().channel({"mm"}).process({"TTJ"}).bin_id({4})
      .AddSyst(cb, "CMS_htt_scale_met_TTJ_$ERA", "shape", SystMap<>::init(0.50));


  src.cp().process({"TTJ"})
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"},  {0, 1},     0.96)
        ({"7TeV"},  {2, 3, 4},  0.95)
        ({"8TeV"},  {2, 3},     0.97)
        ({"8TeV"},  {4},        0.99));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  src.cp().process({"ggH"}).bin_id({4})
      .AddSyst(cb, "pdf_gg_Shape", "shape", SystMap<>::init(1.0));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<>::init(1.036));
  src.cp().process({"WH", "ZH"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<channel, bin_id>::init
        ({"ee", "mm"},  {0, 1, 2, 3},   1.01)
        ({"ee"},        {4},            1.01)
        ({"mm"},        {4},            1.04));

  src.cp().process({"qqH"}).bin_id({4})
      .AddSyst(cb, "pdf_qqbar_Shape", "shape", SystMap<>::init(1.0));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<bin_id>::init
        ({0}, 1.103)
        ({1}, 1.100));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "QCDscale_ggH1in", "lnN", SystMap<bin_id>::init
        ({2}, 1.109)
        ({3}, 1.107));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "QCDscale_ggH2in", "lnN", SystMap<bin_id>::init
        ({4}, 1.182));

  src.cp().process({"ggH"}).bin_id({4})
      .AddSyst(cb, "QCDscale_ggH2in_Shape", "shape", SystMap<>::init(1.0));

  src.cp().process_rgx({"^qqH.*$"})
      .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
        ({0}, 1.034)
        ({1}, 1.028)
        ({2}, 1.008)
        ({3}, 1.013)
        ({4}, 1.009));

  src.cp().process({"qqH"}).bin_id({4})
      .AddSyst(cb, "QCDscale_qqH_Shape", "shape", SystMap<>::init(1.0));

  src.cp().process({"WH", "ZH"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init(1.04));

  src.cp().process_rgx({"^ggH.*$"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
        ({0}, 1.035)
        ({1}, 1.042)
        ({2}, 0.984)
        ({3}, 0.978)
        ({4}, 0.926));
  src.cp().process_rgx({"^qqH.*$", "WH", "ZH"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
        ({0}, 1.089)
        ({1}, 1.063)
        ({2}, 1.000)
        ({3}, 1.004)
        ({4}, 0.986));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.03));

  src.cp().channel({"ee"}).process({"ZTT"})
      .AddSyst(cb, "CMS_htt_ee_ztt_extrap_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {1, 2},  1.07)
        ({"7TeV"}, {3},     1.06)
        ({"7TeV"}, {4},     1.09)
        ({"8TeV"}, {1},     1.09)
        ({"8TeV"}, {2, 3},  1.07)
        ({"8TeV"}, {4},     1.09));

  src.cp().channel({"mm"}).process({"ZTT"})
      .AddSyst(cb, "CMS_htt_mm_zttLnN_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {1, 2},  1.07)
        ({"7TeV"}, {3},     1.06)
        ({"7TeV"}, {4},     1.08)
        ({"8TeV"}, {1},     1.09)
        ({"8TeV"}, {2, 3},  1.07)
        ({"8TeV"}, {4},     1.08));

  src.cp().process({"TTJ"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<era>::init
        ({"7TeV"}, 1.08)
        ({"8TeV"}, 1.10));

  src.cp().process({"Dibosons"})
      .AddSyst(cb, "CMS_htt_ee_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.30));

  src.cp().process({"ZEE", "ZMM"})
      .AddSyst(cb, "CMS_htt_$CHANNEL_z$CHANNELNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {0}, 1.01)
        ({"7TeV"}, {1}, 1.0045)
        ({"7TeV"}, {2}, 1.01)
        ({"7TeV"}, {3}, 1.007)
        ({"7TeV"}, {4}, 1.02)
        ({"8TeV"}, {0}, 1.01)
        ({"8TeV"}, {1}, 1.001)
        ({"8TeV"}, {2}, 1.01)
        ({"8TeV"}, {3}, 1.007)
        ({"8TeV"}, {4}, 1.015));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_$CHANNEL_QCDNorm_$BIN_$ERA", "lnN", SystMap<channel, era, bin_id>::init
        ({"ee"}, {"7TeV"}, {0}, 1.19)
        ({"ee"}, {"7TeV"}, {1}, 1.50)
        ({"ee"}, {"7TeV"}, {2}, 1.35)
        ({"ee"}, {"7TeV"}, {3}, 1.34)
        ({"ee"}, {"7TeV"}, {4}, 1.70)
        ({"ee"}, {"8TeV"}, {0}, 1.11)
        ({"ee"}, {"8TeV"}, {1}, 1.09)
        ({"ee"}, {"8TeV"}, {2}, 1.16)
        ({"ee"}, {"8TeV"}, {3}, 1.14)
        ({"ee"}, {"8TeV"}, {4}, 1.55)
        ({"mm"}, {"7TeV"}, {0}, 1.11)
        ({"mm"}, {"7TeV"}, {1}, 1.11)
        ({"mm"}, {"7TeV"}, {2}, 1.25)
        ({"mm"}, {"7TeV"}, {3}, 1.09)
        ({"mm"}, {"7TeV"}, {4}, 2.00)
        ({"mm"}, {"8TeV"}, {0}, 1.10)
        ({"mm"}, {"8TeV"}, {1}, 1.08)
        ({"mm"}, {"8TeV"}, {2}, 1.12)
        ({"mm"}, {"8TeV"}, {3}, 1.09)
        ({"mm"}, {"8TeV"}, {4}, 1.70));

  auto ee_bins = src.cp().channel({"ee"}).bin_set();
  for (auto bin : ee_bins) {
    std::string clip = bin;
    boost::replace_all(clip, "ee_", "");
    for (std::string i : {"0", "1", "2"}) {
      src.cp().process({"ZEE"}).bin({bin}).AddSyst(
          cb, "CMS_htt_$CHANNEL_z$CHANNELShape_" + clip + "_mass" + i + "_$ERA",
          "shape", SystMap<>::init(1.0));
    }
  }

  auto mm_bins = src.cp().channel({"mm"}).bin_set();
  for (auto bin : mm_bins) {
    std::string clip = bin;
    boost::replace_all(clip, "mumu_", "");
    for (std::string i : {"0", "1", "2"}) {
      src.cp().process({"ZMM"}).bin({bin}).AddSyst(
          cb, "CMS_htt_$CHANNEL_z$CHANNELShape_" + clip + "_mass" + i + "_$ERA",
          "shape", SystMap<>::init(1.0));
    }
  }
}

void AddSystematics_et_mt(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();
  src.channel({"et", "mt"});

  auto signal = Set2Vec(cb.cp().signals().process_set());

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"7TeV"}, 1.022)
      ({"8TeV"}, 1.026));

  src.cp().process({"ggH"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init
      (1.097));

  src.cp().process({"qqH", "WH", "ZH"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<process>::init
      ({"qqH"},       1.036)
      ({"WH", "ZH"},  1.040));

  src.cp().process({"ggH"})
      .AddSyst(cb, "QCDscale_ggH", "lnN", SystMap<bin_id>::init
      ({1, 2}, 1.08));

  src.cp().process({"ggH"})
      .AddSyst(cb, "QCDscale_ggH1in", "lnN", SystMap<bin_id>::init
      ({3}, 1.105)
      ({4}, 1.095)
      ({5}, 1.195));

  src.cp().process({"ggH"})
      .AddSyst(cb, "QCDscale_ggH2in", "lnN", SystMap<bin_id>::init
      ({6}, 1.228)
      ({7}, 1.307));

  src.cp().process({"qqH"})
      .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
      ({1}, 1.022)
      ({2}, 1.023)
      ({3}, 1.015)
      ({4}, 1.013)
      ({5}, 1.015)
      ({6}, 1.018)
      ({7}, 1.031));

  src.cp().process({"WH", "ZH"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<bin_id>::init
      ({1, 2},            1.010)
      ({3, 4, 5, 6, 7},   1.040));

  src.cp().process({"qqH", "WH", "ZH"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
      ({1}, 1.050)
      ({2}, 1.060)
      ({3}, 1.007)
      ({4}, 0.996)
      ({5}, 1.006)
      ({6}, 0.988)
      ({7}, 0.986));
  src.cp().process({"ggH"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
      ({1}, 1.013)
      ({2}, 1.028)
      ({3}, 0.946)
      ({4}, 0.954)
      ({5}, 0.983)
      ({6}, 0.893)
      ({7}, 0.881));

  src.cp().process(JoinStr({signal, {"ZTT", "ZL", "ZJ", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.08));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}})).AddSyst(
      cb, "CMS_eff_t_$CHANNEL_medium_$ERA", "lnN",
      SystMap<bin_id>::init({1, 3}, 1.03)({6, 7}, 1.01));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_high_$ERA", "lnN", SystMap<bin_id>::init
        ({2, 4, 5},  1.030)
        ({6},        1.012)
        ({7},        1.015));

  src.cp().process(JoinStr({signal, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {1, 2},  {"ggH"},        0.98)
        ({"7TeV"}, {1, 2},  {"qqH"},        0.86)
        ({"7TeV"}, {1, 2},  {"WH", "ZH"},   0.97)
        ({"7TeV"}, {1, 2},  {"TT"},         0.99)
        ({"7TeV"}, {1, 2},  {"VV"},         0.98)
        ({"7TeV"}, {3},     {"ggH"},        1.05)
        ({"7TeV"}, {3},     {"qqH"},        1.01)
        ({"7TeV"}, {3},     {"WH", "ZH"},   1.05)
        ({"7TeV"}, {3},     {"VV"},         1.02)
        ({"7TeV"}, {4, 5},  {"ggH"},        1.03)
        ({"7TeV"}, {4, 5},  {"qqH"},        1.02)
        ({"7TeV"}, {4, 5},  {"WH", "ZH"},   1.03)
        ({"7TeV"}, {4, 5},  {"TT"},         1.01)
        ({"7TeV"}, {4, 5},  {"VV"},         1.04)
        ({"7TeV"}, {6},     {"ggH"},        1.20)
        ({"7TeV"}, {6},     {"qqH"},        1.05)
        ({"7TeV"}, {6},     {"WH", "ZH"},   1.20)
        ({"7TeV"}, {6},     {"TT"},         1.10)
        ({"7TeV"}, {6},     {"VV"},         1.15)
        ({"8TeV"}, {1},     {"ggH"},        0.98)
        ({"8TeV"}, {1},     {"qqH"},        0.92)
        ({"8TeV"}, {1},     {"WH", "ZH"},   0.96)
        ({"8TeV"}, {1},     {"ZL"},         0.99)
        ({"8TeV"}, {1},     {"ZJ"},         0.98)
        ({"8TeV"}, {1},     {"TT"},         0.95)
        ({"8TeV"}, {1},     {"VV"},         0.98)
        ({"8TeV"}, {2},     {"ggH"},        0.98)
        ({"8TeV"}, {2},     {"qqH"},        0.92)
        ({"8TeV"}, {2},     {"WH", "ZH"},   0.88)
        ({"8TeV"}, {2},     {"ZL"},         0.99)
        ({"8TeV"}, {2},     {"ZJ"},         0.97)
        ({"8TeV"}, {2},     {"TT"},         0.84)
        ({"8TeV"}, {2},     {"VV"},         0.97)
        ({"8TeV"}, {3},     {"ggH"},        1.04)
        ({"8TeV"}, {3},     {"qqH"},        0.99)
        ({"8TeV"}, {3},     {"WH", "ZH"},   1.01)
        ({"8TeV"}, {3},     {"ZL", "ZJ"},   1.02)
        ({"8TeV"}, {3},     {"VV"},         1.03)
        ({"8TeV"}, {4},     {"ggH"},        1.04)
        ({"8TeV"}, {4},     {"WH", "ZH"},   1.03)
        ({"8TeV"}, {4},     {"ZL", "ZJ"},   1.02)
        ({"8TeV"}, {4},     {"VV"},         1.02)
        ({"8TeV"}, {5},     {"ggH"},        1.02)
        ({"8TeV"}, {5},     {"WH", "ZH"},   1.01)
        ({"8TeV"}, {5},     {"TT"},         0.97)
        ({"8TeV"}, {5},     {"VV"},         1.03)
        ({"8TeV"}, {6},     {"ggH"},        1.10)
        ({"8TeV"}, {6},     {"qqH"},        1.04)
        ({"8TeV"}, {6},     {"WH", "ZH"},   1.15)
        ({"8TeV"}, {6},     {"ZL"},         1.05)
        ({"8TeV"}, {6},     {"ZJ"},         1.10)
        ({"8TeV"}, {6},     {"TT"},         1.05)
        ({"8TeV"}, {6},     {"VV"},         1.08)
        ({"8TeV"}, {7},     {"ggH"},        1.06)
        ({"8TeV"}, {7},     {"qqH"},        1.03)
        ({"8TeV"}, {7},     {"WH", "ZH"},   1.15)
        ({"8TeV"}, {7},     {"ZL"},         1.05)
        ({"8TeV"}, {7},     {"TT"},         1.05)
        ({"8TeV"}, {7},     {"VV"},         1.10));

  src.cp()
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN",
        SystMap<era, bin_id, process>::init
        ({"7TeV"}, {1, 2, 3, 4, 5, 6},  {signal},       1.05)
        ({"7TeV"}, {1, 2, 3, 4, 5, 6},  {"TT", "W"},    1.07)
        ({"7TeV"}, {1, 2, 3, 4, 5, 6},  {"ZL", "ZJ"},   1.05)
        ({"8TeV"}, {1},                 {"TT"},         1.05)
        ({"8TeV"}, {1},                 {"W"},          1.01)
        ({"8TeV"}, {2},                 {signal},       1.01)
        ({"8TeV"}, {2},                 {"TT"},         1.04)
        ({"8TeV"}, {2},                 {"W"},          1.01)
        ({"8TeV"}, {2},                 {"ZL"},         1.02)
        ({"8TeV"}, {3},                 {signal},       0.99)
        ({"8TeV"}, {3},                 {"TT"},         1.02)
        ({"8TeV"}, {3},                 {"W"},          1.01)
        ({"8TeV"}, {3},                 {"ZL"},         1.02)
        ({"8TeV"}, {4},                 {signal},       0.99)
        ({"8TeV"}, {4},                 {"TT"},         1.02)
        ({"8TeV"}, {4},                 {"W"},          1.01)
        ({"8TeV"}, {4},                 {"ZL"},         1.03)
        ({"8TeV"}, {5},                 {signal},       0.99)
        ({"8TeV"}, {5},                 {"TT"},         1.01)
        ({"8TeV"}, {5},                 {"W"},          1.03)
        ({"8TeV"}, {5},                 {"ZL"},         1.02)
        ({"8TeV"}, {5},                 {"ZJ"},         0.98)
        ({"8TeV"}, {6},                 {signal},       0.99)
        ({"8TeV"}, {6},                 {"TT", "W"},    1.04)
        ({"8TeV"}, {6},                 {"ZL", "ZJ"},   1.03)
        ({"8TeV"}, {7},                 {signal},       0.99)
        ({"8TeV"}, {7},                 {"TT", "W"},    1.03)
        ({"8TeV"}, {7},                 {"ZL", "ZJ"},   1.03));

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"7TeV"}, {1, 2, 3, 4, 5, 6},  {"TT"},      0.90)
        ({"7TeV"}, {3, 4, 5},           {"VV"},      0.98)
        ({"8TeV"}, {1},                 {"TT"},      0.98)
        ({"8TeV"}, {2, 3, 4},           {"TT"},      0.96)
        ({"8TeV"}, {5, 6, 7},           {"TT"},      0.94));

  src.cp().process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN", SystMap<>::init(1.03));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({1, 2, 3, 4, 5},   1.05)
        ({6},               1.10)
        ({7},               1.13));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {1, 2, 3, 4, 5, 6},    1.08)
        ({"8TeV"}, {1, 2, 3, 4, 5},       1.10)
        ({"8TeV"}, {6, 7},                1.08));

  src.cp().process({"TT"})
      .AddSyst(cb,
      "CMS_htt_ttbarNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
      ({"7TeV"}, {6},     1.20)
      ({"8TeV"}, {6, 7},  1.33));

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {1, 2},    1.20)
        ({"7TeV"}, {3, 4},    1.10)
        ({"7TeV"}, {5},       1.12)
        ({"7TeV"}, {6},       1.20)
        ({"8TeV"}, {1, 2},    1.20)
        ({"8TeV"}, {3},       1.15)
        ({"8TeV"}, {4},       1.11)
        ({"8TeV"}, {5},       1.16)
        ({"8TeV"}, {6},       1.21)
        ({"8TeV"}, {7},       1.51));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.15));

  src.cp().process({"VV"})
      .AddSyst(cb,
      "CMS_htt_DiBosonNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {6},      1.37)
        ({"8TeV"}, {6},      1.50)
        ({"8TeV"}, {7},      1.45));

  src.cp().process({"QCD"})
      .AddSyst(cb,
      "CMS_htt_QCDSyst_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"7TeV"}, {1, 2, 3, 4, 5},   1.10)
        ({"7TeV"}, {6},               1.22)
        ({"8TeV"}, {1, 2},            1.06)
        ({"8TeV"}, {3, 4, 5},         1.10)
        ({"8TeV"}, {6},               1.30)
        ({"8TeV"}, {7},               1.70));

  src.cp().process({"QCD"}).bin_id({3})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_1jet_medium_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"QCD"}).bin_id({4})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_1jet_high_lowhiggs_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"QCD"}).bin_id({6}).era({"7TeV"})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_vbf_$ERA", "shape",
        SystMap<>::init(1.00));
  src.cp().process({"QCD"}).bin_id({6}).era({"8TeV"})
      .AddSyst(cb, "CMS_htt_QCDShape_mutau_vbf_loose_$ERA", "shape",
        SystMap<>::init(1.00));

  src.cp().process({"ZJ"})
      .AddSyst(cb, "CMS_htt_ZJetFakeTau_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({1, 2, 3, 4, 5},   1.20)
        ({6},               1.30)
        ({7},               1.80));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$CHANNEL_$ERA", "lnN",
        SystMap<>::init(1.30));

  src.cp().process({"ZL"})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$BIN_$ERA", "lnN",
        SystMap<era, bin_id>::init
        ({"7TeV"}, {6},       2.00)
        ({"8TeV"}, {5},       1.26)
        ({"8TeV"}, {6},       1.70));

  src.cp().process({"ZL"})
      .AddSyst(cb,
      "CMS_htt_ZLScale_mutau_$ERA", "shape", SystMap<>::init(1.00));
}


void AddSystematics_tt(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();
  src.channel({"tt"});

  auto signal = Set2Vec(cb.cp().signals().process_set());

  src.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"8TeV"}, 1.026));

  src.cp().process({"ggH"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init
      (1.097));

  src.cp().process({"qqH", "WH", "ZH"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<process>::init
      ({"qqH"},       1.036)
      ({"WH", "ZH"},  1.020));

  src.cp().process({"ggH"})
      .AddSyst(cb, "QCDscale_ggH1in", "lnN", SystMap<bin_id>::init
      ({0}, 1.205)
      ({1}, 1.175));

  src.cp().process({"ggH"})
      .AddSyst(cb, "QCDscale_ggH2in", "lnN", SystMap<bin_id>::init
      ({2}, 1.41));

  src.cp().process({"qqH"})
      .AddSyst(cb, "QCDscale_qqH", "lnN", SystMap<bin_id>::init
      ({0}, 1.012)
      ({1}, 1.014)
      ({2}, 1.013));

  src.cp().process({"WH", "ZH"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<bin_id>::init
      ({0, 1, 2},   1.04));

  src.cp().process({"qqH", "WH", "ZH"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
      ({0}, 1.025)
      ({1}, 0.996));
  src.cp().process({"ggH"})
      .AddSyst(cb, "UEPS", "lnN", SystMap<bin_id>::init
      ({0}, 0.975)
      ({1}, 0.993)
      ({2}, 0.900));

  src.cp().process(JoinStr({signal, {"ZTT", "TT", "VV"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.19));

  src.cp().process(JoinStr({signal, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_tautau_$ERA", "shape", SystMap<>::init(1.00));

  src.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {0},     {"qqH"},        0.99)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.035)
        ({"8TeV"}, {2},     {"qqH"},        1.015)
        ({"8TeV"}, {2},     {"WH", "ZH"},   1.015)
        ({"8TeV"}, {2},     {"ZL", "ZJ"},   1.03)
        ({"8TeV"}, {2},     {"TT"},         1.02)
        ({"8TeV"}, {2},     {"VV"},         1.08));

  src.cp()
      .AddSyst(cb, "CMS_htt_scale_met_$ERA", "lnN",
        SystMap<era, bin_id, process>::init
        ({"8TeV"}, {0},     {"W"},          1.015)
        ({"8TeV"}, {0},     {"TT"},         1.02)
        ({"8TeV"}, {1},     {"TT"},         1.02)
        ({"8TeV"}, {1},     {signal},       1.03)
        ({"8TeV"}, {2},     {"W"},          1.015));

  src.cp()
      .AddSyst(cb, "CMS_eff_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {0},     {"TT"},         0.93)
        ({"8TeV"}, {1},     {"TT"},         0.83)
        ({"8TeV"}, {2},     {"TT"},         0.93));

  src.cp()
      .AddSyst(cb, "CMS_fake_b_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {0},     {"TT"},         0.96)
        ({"8TeV"}, {1},     {"TT"},         0.83)
        ({"8TeV"}, {2},     {"TT"},         0.96));

  src.cp()
      .AddSyst(cb, "CMS_htt_zttNorm_$ERA", "lnN",
        SystMap<era, bin_id, process>::init
        ({"8TeV"}, {0, 1},  {"ZTT", "ZL", "ZJ"},  1.033)
        ({"8TeV"}, {2},     {"ZTT", "ZJ"},        1.03));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_extrap_ztt_$BIN_$ERA", "lnN", SystMap<bin_id>::init
        ({0, 1},   1.03)
        ({2},      1.10));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_$ERA", "lnN", SystMap<>::init(1.10));

  src.cp().process({"TT"})
      .AddSyst(cb,
      "CMS_htt_ttbarNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
      ({"8TeV"}, {0, 1}, 1.05)
      ({"8TeV"}, {2},    1.24));

  src.cp().process({"W"})
      .AddSyst(cb, "CMS_htt_WNorm_$BIN_$ERA", "lnN", SystMap<>::init(1.30));

  src.cp().process({"VV"})
      .AddSyst(cb, "CMS_htt_DiBosonNorm_$ERA", "lnN", SystMap<>::init(1.15));

  src.cp().process({"VV"})
      .AddSyst(cb,
      "CMS_htt_DiBosonNorm_$BIN_$ERA", "lnN", SystMap<era, bin_id>::init
        ({"8TeV"}, {0, 1},   1.15)
        ({"8TeV"}, {2},      1.13));

  src.cp().process({"QCD"})
      .AddSyst(cb, "CMS_htt_QCDSyst_$BIN_$ERA", "lnN", SystMap<>::init(1.35));

  src.cp().process({"ZJ"})
      .AddSyst(cb,
      "CMS_htt_ZJetFakeTau_$BIN_$ERA", "lnN", SystMap<>::init(1.20));

  src.cp().process({"ZL"}).bin_id({0, 1})
      .AddSyst(cb, "CMS_htt_ZLeptonFakeTau_$BIN_$ERA", "lnN",
        SystMap<>::init(1.30));
}


void AddMSSMSystematics(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();

  auto signal = Set2Vec(src.cp().signals().GenerateSetFromProcs<std::string>(
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












}
