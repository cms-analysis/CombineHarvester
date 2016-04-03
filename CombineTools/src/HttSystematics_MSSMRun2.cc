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
       ({"mt"},{8}, {"ZTT","ZL"}, 1.001,0.999)
       ({"mt"},{8}, {"ZJ"}, 1.001,0.997)
       ({"mt"},{8}, {"TT"}, 1.014,0.986)
       ({"mt"},{8}, {"VV"}, 1.004,0.997)
       ({"mt"},{8}, {"ggH","bbH"}, 1.01,0.99) //Placeholder until we can do this a little neater
//       ({"mt"},{8}, {"W"}, (1,1))
       ({"mt"},{9}, {"ZTT"}, 0.980,1.029)
       ({"mt"},{9}, {"ZL"}, 0.993,1.027)
       ({"mt"},{9}, {"ZJ"}, 0.987,1.005)
       ({"mt"},{9}, {"TT"}, 1.111,0.908)
       ({"mt"},{9}, {"VV"}, 1.034,0.951)
       ({"mt"},{9}, {"ggH"}, 1.03,0.84) //Placeholder until we can do this a little neater
       ({"mt"},{9}, {"bbH"}, 1.02,1) //Placeholder until we can do this a little neater
//       ({"mt"},{9}, {"W"}, (1,1))
       ({"em"},{8}, {"ZTT","ZLL"}, 1.001,0.999)
       ({"em"},{8}, {"TT"}, 1.016,0.986)
       ({"em"},{8}, {"VV"}, 1.006,0.995)
       ({"em"},{8}, {"ggH","bbH"}, 1.01,0.99) //Placeholder until we can do this a little neater
//       ({"em"},{8}, {"W"}, (1,1))
       ({"em"},{9}, {"ZTT","ZLL"}, 0.976,1.012)
       ({"em"},{9}, {"TT"}, 1.101,0.903)
       ({"em"},{9}, {"VV"}, 1.053,0.942)
       ({"em"},{9}, {"ggH"}, 1.06,0.81) //Placeholder until we can do this a little neater
       ({"em"},{9}, {"bbH"}, 0.99,0.99) //Placeholder until we can do this a little neater
//       ({"em"},{9}, {"W"}, (1,1))
       ({"et"},{8}, {"ZTT","ZL","ZJ"}, 1.001,0.999)
       ({"et"},{8}, {"TT"}, 1.011,0.988)
       ({"et"},{8}, {"VV"}, 1.003,0.994)
       ({"et"},{8}, {"W"}, 1.003,1)
       ({"et"},{8}, {"ggH"}, 1,0.99) //Placeholder until we can do this a little neater
       ({"et"},{8}, {"bbH"}, 1.01,0.99) //Placeholder until we can do this a little neater
       ({"et"},{9}, {"ZTT"}, 1.002,0.996)
       ({"et"},{9}, {"ZL"}, 0.992,0.994)
       ({"et"},{9}, {"ZJ"}, 1.024,1.023)
       ({"et"},{9}, {"TT"}, 1.122,0.893)
       ({"et"},{9}, {"VV"}, 1.063,0.934)
       ({"et"},{9}, {"W"}, 0.875,0.879)
       ({"et"},{9}, {"ggH"}, 1.11,1.04) //Placeholder until we can do this a little neater
       ({"et"},{9}, {"bbH"}, 1.01,0.97) //Placeholder until we can do this a little neater
       ({"tt"},{8}, {"ZTT"}, 1.001,0.999)
       ({"tt"},{8}, {"ZL"}, 1.002,1)
       ({"tt"},{8}, {"ggH","bbH"}, 0.98,0.99) //Placeholder until we can do this a little neater
//       ({"tt"},{8}, {"ZJ"}, (1,1))
       ({"tt"},{8}, {"TT"}, 1.017,0.977)
       ({"tt"},{8}, {"VV"}, 1.001,0.979)
       ({"tt"},{8}, {"W"}, 1,0.907)
       ({"tt"},{9}, {"ZTT"}, 1.017,0.964)
//       ({"tt"},{9}, {"ZL"}, (1,1))
       ({"tt"},{9}, {"ZJ"}, 1.280,1)
       ({"tt"},{9}, {"TT"}, 1.096,0.901)
       ({"tt"},{9}, {"VV"}, 1.120,0.926)
       ({"tt"},{9}, {"bbH"}, 0.99,0.98) //Placeholder until we can do this a little neater
       ({"tt"},{9}, {"ggH"}, 1.07,0.92)); //Placeholder until we can do this a little neater
//       ({"tt"},{9}, {"W"}, (1,1))

/*  src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"em"})
      .AddSyst(cb, "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));*/

// src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"})
//      .AddSyst(cb, "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

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
      // TODO neeed to adjust this because now we want:
      // 1 rateParam for all W in every region
      // 1 rateParam for QCD in low mT
      // 1 rateParam for QCD in high mT
      // lnN for the QCD OS/SS ratio (stat and syst)
      // lnN for the W+jets OS/SS ratio (MC stat and syst)

      // setup rateParams
      // this map is needed for bookkeeping of the control-region bin-ids
      std::map<std::string,int> base_categories{{"btag",10},{"nobtag",13}};
      for (auto bin:src.cp().bin_id({8,9}).bin_set()){
        // use cb as we need all categories
        // Add rateParam for W in OS
        cb.cp().process({"W"}).channel({bin.substr(0,2)}).AddSyst(cb, "wjets_os_rate_"+bin,"rateParam", SystMap<bin_id>::init({*(src.cp().bin({bin}).bin_id_set().begin()),base_categories[bin.substr(3)]},1.0));
        // Add rateParam for W in SS
        cb.cp().process({"W"}).channel({bin.substr(0,2)}).AddSyst(cb, "wjets_ss_rate_"+bin,"rateParam", SystMap<bin_id>::init({base_categories[bin.substr(3)]+1,base_categories[bin.substr(3)]+2},1.0));
        // Add rateParam for QCD
        cb.cp().process({"QCD"}).channel({bin.substr(0,2)}).AddSyst(cb, "qcd_rate_"+bin,"rateParam", SystMap<bin_id>::init({*(src.cp().bin({bin}).bin_id_set().begin()),base_categories[bin.substr(3)]+1},1.0));
      }
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
