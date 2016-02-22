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


void AddMSSMRun2Systematics(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();

  auto signal = Set2Vec(src.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  //src.cp().process({"ggH","bbH"})
  //    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

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

  src.cp().process(ch::JoinStr({signal, {"ZTT"}})).channel({"et","mt","tt"})
      .AddSyst(cb, "CMS_scale_t_$CHANNEL_$ERA", "shape", SystMap<>::init(1.00));

//  src.cp().channel({"em"}).process(ch::JoinStr({signal, {"TT","VV","ZLL","ZTT","W"}})).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

//  src.cp().channel({"em"}).AddSyst(cb, "CMS_scale_j_13TeV", "lnN", SystMap<era,process>::init
 //     ({"13TeV"}, {"TT"},          0.91)
  //    ({"13TeV"}, {"VV"},            0.98));


 // src.cp().process(ch::JoinStr({signal, {"TT","VV","ZL","W","ZJ","ZTT"}})).channel({"et"})
 //     .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));
  
  src.cp().process({"TT","VV","ZL","W","ZJ","ZTT","ZLL"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  src.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  src.cp().process(signal).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  src.cp().channel({"em"}).process({"ZLL"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
//  src.cp().channel({"et"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
  src.cp().channel({"et","tt","mt"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  src.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_13TeV", "lnN", SystMap<era>::init
        ({"13TeV"}, 1.10));

/*  src.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
      "CMS_htt_em_QCD_13TeV","lnN",SystMap<>::init(1.3));

 src.cp().process({"QCD"}).channel({"et"}).AddSyst(cb,
      "CMS_htt_et_QCD_13TeV","lnN",SystMap<>::init(1.3));*/

 src.cp().process({"QCD"}).channel({"et","em","tt","mt"}).AddSyst(cb,
      "CMS_htt_QCD_13TeV","lnN",SystMap<>::init(1.3));

  src.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.15));

  src.cp().process({"W"}).channel({"mt"}).AddSyst(cb,
     "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.2));

/*  src.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {1},     {"ggH"},        1.04)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.10)
        ({"8TeV"}, {2},     {"qqH"},        1.04)
        ({"8TeV"}, {2},     {"TT"},         1.05));
*/

//  src.cp().process(ch::JoinStr({signal, {"ZTT"}}))
 //     .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));
  //! [part6]
}
}
