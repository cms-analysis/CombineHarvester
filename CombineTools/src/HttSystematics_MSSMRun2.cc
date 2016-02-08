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
