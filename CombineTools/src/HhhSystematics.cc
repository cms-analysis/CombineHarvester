#include "CombineTools/interface/HttSystematics.h"
#include <vector>
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



void AddSystematics_hhh_et_mt(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();
  src.channel({"et","mt"});

  auto signal = Set2Vec(cb.cp().signals().process_set());

  src.cp().signals()
      .AddSyst(cb, "lumi_8TeV", "lnN", SystMap<>::init
      (1.026));

  src.cp().process(JoinStr({signal,{"ZTT","ZJ","ZL","TT","VV"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init
      (1.02));

   src.cp().process(JoinStr({signal,{"ZTT","ZJ","ZL","TT","VV"}})).channel({"mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init
      (1.01));

  src.cp().process(JoinStr({signal,{"ZTT","TT","VV"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_t_etau_8TeV", "lnN", SystMap<bin_id,process>::init
      ({0,1,2},JoinStr({signal,{"ZTT","VV"}}),1.08)
      ({0},{"TT"},1.08));

  src.cp().process(JoinStr({signal,{"ZTT","TT","VV"}})).channel({"mt"})
      .AddSyst(cb, "CMS_eff_t_mutau_8TeV", "lnN", SystMap<bin_id,process>::init
      ({0,1,2},JoinStr({signal,{"ZTT","VV"}}),1.08)
      ({0},{"TT"},1.08));

  src.cp().signals()
      .AddSyst(cb, "CMS_htt_scale_met_8TeV", "lnN", SystMap<>::init
      (0.99));

  src.cp().process(JoinStr({signal,{"ZTT"}})).channel({"et"})
      .AddSyst(cb, "CMS_scale_t_etau_8TeV", "shape", SystMap<>::init
      (1.00));

  src.cp().process(JoinStr({signal,{"ZTT"}})).channel({"mt"})
      .AddSyst(cb, "CMS_scale_t_mutau_8TeV", "shape", SystMap<>::init
      (1.00));

 

 src.cp().process(JoinStr({signal,{"ZTT","ZJ","ZL","TT","VV"}}))
    .AddSyst(cb, "CMS_scale_j_8TeV","shape",SystMap<>::init(1.00));
 
 src.cp().process({"TT","ZL","ZJ","W"})
         .AddSyst(cb,"CMS_htt_scale_met_8TeV","lnN",SystMap<bin_id,process>::init
         ({0,1,2},{"TT"},1.01)
         ({0,1,2},{"ZL"},1.01)
         ({0,1,2},{"ZJ"},1.01)
         ({1,2},{"W"},1.01));

 src.cp().process(JoinStr({signal,{"TT","W","VV","QCD","ZL","ZJ"}}))
         .AddSyst(cb,"CMS_eff_b_8TeV","lnN",SystMap<channel,bin_id,process>::init
         ({"et","mt"},{0},{"TT"}, 0.95)
         ({"et","mt"},{0},{"W"}, 1.01)
         ({"et"},{0},{signal},0.93)
         ({"mt"},{0},{signal},0.92)
         ({"mt"},{0},{"VV"},0.99)
         ({"et"},{1},{"VV","QCD"},0.97)
         ({"et"},{1},{"W"},0.99)
         ({"mt"},{1},JoinStr({signal,{"ZJ"}}),0.99)
         ({"mt"},{1},{"VV"},1.02)
         ({"mt"},{1},{"W"},1.01)
         ({"mt"},{1},{"QCD"},0.98)
         ({"mt"},{1},{"ZL"},1.05)
         ({"et"},{2},JoinStr({signal,{"TT"}}),1.04)
         ({"et"},{2},{"VV"},1.13)
         ({"et"},{2},{"W"},0.68)
         ({"et"},{2},{"ZL"},1.07)
         ({"mt"},{2},JoinStr({signal,{"TT"}}),1.05)
         ({"mt"},{2},{"VV"},1.01)
         ({"mt"},{2},{"W"},0.28)
         ({"mt"},{2},{"ZJ"},1.41));

src.cp().process({"ZTT","ZL","ZJ"})
        .AddSyst(cb,"CMS_htt_zttNorm_8TeV","lnN",SystMap<>::init(1.03));

src.cp().process({"TT"})
        .AddSyst(cb,"CMS_htt_ttbarNorm_8TeV","lnN",SystMap<>::init(1.10));

src.cp().process({"VV"})
        .AddSyst(cb,"CMS_htt_DiBosonNorm_8TeV","lnN",SystMap<>::init(1.15));

src.cp().process({"ZL"}).channel({"et"})
        .AddSyst(cb,"CMS_htt_ZLeptonFakeTau_etau_8TeV","lnN",SystMap<bin_id>::init
        ({0,1},1.20)
        ({2},1.40));

src.cp().process({"ZL"}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_ZLeptonFakeTau_mutau_8TeV","lnN",SystMap<bin_id>::init
        ({0},1.30)
        ({1},1.60)
        ({2},1.40));

src.cp().process({"ZL","ZJ","W","VV"})
        .AddSyst(cb,"CMS_fake_b_8TeV","lnN",SystMap<channel,bin_id,process>::init
        ({"mt"},{0},{"VV"},0.99)
        ({"et"},{1},{"ZL"},1.01)
        ({"et"},{1},{"ZJ"},1.04)
        ({"mt"},{1},{"VV"},1.03)
        ({"mt"},{1},{"ZL"},1.04)
        ({"mt"},{1},{"ZJ"},1.02)
        ({"et"},{2},{"W"},0.95)
        ({"mt"},{2},{"VV"},1.01)
        ({"mt"},{2},{"W"},0.96));

src.cp().process({"W"}).bin_id({0}).channel({"et"})
        .AddSyst(cb,"CMS_htt_WNorm_etau_2jet0tag_8TeV","lnN",SystMap<>::init(1.10));

src.cp().process({"ZTT"}).bin_id({0}).channel({"et"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_etau_2jet0tag_8TeV","lnN",SystMap<>::init(1.05));

src.cp().process({"QCD"}).bin_id({0}).channel({"et"})
        .AddSyst(cb,"CMS_htt_QCDSyst_etau_2jet0tag_8TeV","lnN", SystMap<>::init(1.20));

src.cp().process({"ZJ"}).bin_id({0}).channel({"et"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_etau_2jet0tag_8TeV","lnN",SystMap<>::init(1.20));

src.cp().process({"W"}).bin_id({0}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_WNorm_mutau_2jet0tag_8TeV","lnN",SystMap<>::init(1.10));

src.cp().process({"ZTT"}).bin_id({0}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_mutau_2jet0tag_8TeV","lnN",SystMap<>::init(1.05));

src.cp().process({"QCD"}).bin_id({0}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_QCDSyst_mutau_2jet0tag_8TeV","lnN", SystMap<>::init(1.20));

src.cp().process({"ZJ"}).bin_id({0}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_mutau_2jet0tag_8TeV","lnN",SystMap<>::init(1.20));


src.cp().process({"W"}).bin_id({1}).channel({"et"})
        .AddSyst(cb,"CMS_htt_WNorm_etau_2jet1tag_8TeV","lnN",SystMap<>::init(1.40));

src.cp().process({"ZTT"}).bin_id({1}).channel({"et"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_etau_2jet1tag_8TeV","lnN",SystMap<>::init(1.05));

src.cp().process({"ZTT"})
        .AddSyst(cb,"CMS_htt_ttbar_emb_8TeV","lnN",SystMap<channel,bin_id>::init
        ({"et","mt"},{1},1.08)
        ({"et"},{2},1.32)
        ({"mt"},{2},1.27));

src.cp().process({"QCD"}).bin_id({1}).channel({"et"})
        .AddSyst(cb,"CMS_htt_QCDSyst_etau_2jet1tag_8TeV","lnN",SystMap<>::init(1.40));

src.cp().process({"ZJ"}).bin_id({1}).channel({"et"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_etau_2jet1tag_8TeV","lnN",SystMap<>::init(1.25));

src.cp().process({"W"}).bin_id({1}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_WNorm_mutau_2jet1tag_8TeV","lnN",SystMap<>::init(1.40));

src.cp().process({"ZTT"}).bin_id({1}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_mutau_2jet1tag_8TeV","lnN",SystMap<>::init(1.05));

src.cp().process({"QCD"}).bin_id({1}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_QCDSyst_mutau_2jet1tag_8TeV","lnN",SystMap<>::init(1.40));

src.cp().process({"ZJ"}).bin_id({1}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_mutau_2jet1tag_8TeV","lnN",SystMap<>::init(1.20));


src.cp().process({"W"}).bin_id({2}).channel({"et"})
        .AddSyst(cb,"CMS_htt_WNorm_etau_2jet2tag_8TeV","lnN",SystMap<>::init(2.00));

src.cp().process({"ZTT"}).bin_id({2}).channel({"et"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_etau_2jet2tag_8TeV","lnN",SystMap<>::init(1.06));

src.cp().process({"QCD"}).bin_id({2}).channel({"et"})
        .AddSyst(cb,"CMS_htt_QCDSyst_etau_2jet2tag_8TeV","lnN",SystMap<>::init(2.00));

src.cp().process({"ZJ"}).bin_id({2}).channel({"et"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_etau_2jet2tag_8TeV","lnN",SystMap<>::init(1.70));

src.cp().process({"W"}).bin_id({2}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_WNorm_mutau_2jet2tag_8TeV","lnN",SystMap<>::init(2.00));

src.cp().process({"ZTT"}).bin_id({2}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_extrap_ztt_mutau_2jet2tag_8TeV","lnN",SystMap<>::init(1.06));

src.cp().process({"QCD"}).bin_id({2}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_QCDSyst_mutau_2jet2tag_8TeV","lnN",SystMap<>::init(1.60));

src.cp().process({"ZJ"}).bin_id({2}).channel({"mt"})
        .AddSyst(cb,"CMS_htt_ZJetFakeTau_mutau_2jet2tag_8TeV","lnN",SystMap<>::init(1.90));

}



 void AddSystematics_hhh_tt(CombineHarvester & cb) {
  CombineHarvester src = cb.cp();
  src.channel({"tt"});

  auto signal = Set2Vec(cb.cp().signals().process_set());
//Systematics for fully hadronic not up to date yet
 }
}
