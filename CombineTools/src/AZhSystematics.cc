#include <vector>
#include <string>
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"

namespace ch {

using ch::syst::SystMap;
using ch::syst::SystMapAsymm;
using ch::syst::era;
using ch::syst::channel;
using ch::syst::bin_id;
using ch::syst::process;
using ch::JoinStr;



void AddSystematics_AZh(CombineHarvester & cb, CombineHarvester src) {
  src.channel({"et","mt","em","tt"});
  //category 0 = ee, 1 = mm

  auto signal = Set2Vec(cb.cp().signals().process_set());

  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}}))
      .AddSyst(cb, "lumi_8TeV", "lnN", SystMap<>::init
      (1.026));

  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}}))
      .AddSyst(cb, "CMS_eff_e_8TeV", "lnN", SystMap<channel,bin_id>::init
      ({"et"}, {0}, 1.06)
      ({"et"}, {1}, 1.02)
      ({"em"}, {0}, 1.06)
      ({"em"}, {1}, 1.02)
      ({"mt"}, {0}, 1.04)
      ({"tt"}, {0}, 1.04));

  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}}))
      .AddSyst(cb, "CMS_eff_m_8TeV", "lnN", SystMap<channel,bin_id>::init
      ({"et"}, {1}, 1.04)
      ({"em"}, {0}, 1.02)
      ({"em"}, {1}, 1.06)
      ({"mt"}, {0}, 1.02)
      ({"mt"}, {1}, 1.06)
      ({"tt"}, {1}, 1.04));

  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}})).channel({"et","mt"})
      .AddSyst(cb, "CMS_eff_t_llet_8TeV", "lnN", SystMap<>::init
      (1.06));
  
  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}})).channel({"tt"})
      .AddSyst(cb, "CMS_eff_t_lltt_8TeV", "lnN", SystMap<>::init
      (1.12));
  
  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}})).bin_id({0})
      .AddSyst(cb, "CMS_trigger_e_8TeV", "lnN", SystMap<>::init
      (1.01));
  
  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}})).bin_id({1})
      .AddSyst(cb, "CMS_trigger_m_8TeV", "lnN", SystMap<>::init
      (1.01));

  src.cp().process(JoinStr({signal,{"GGToZZ2L2L","ZH_ww125","ZH_ww125","ZZ","TTZ","WWZ","WZZ","ZZZ"}}))
      .AddSyst(cb, "CMS_fake_b_8TeV", "lnN", SystMap<>::init
      (1.01));
  
  src.cp().process({"ZZ"})
      .AddSyst(cb, "QCDscale_VV", "lnN", SystMap<>::init
      (1.06));
  
  src.cp().process({"ZZ"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<>::init
      (1.05));

  src.cp().process({"ZZ_tt125"})
      .AddSyst(cb, "CMS_htt_SM125_mu", "lnN", SystMap<>::init
      (1.30));
  
  src.cp().process({"ZZ_ww125"})
      .AddSyst(cb, "CMS_hww_SM125_mu", "lnN", SystMap<>::init
      (1.20));
  
  src.cp().process({"ZZ_tt125,ZZ_ww125"})
      .AddSyst(cb, "QCDscale_VH", "lnN", SystMap<>::init
      (1.031));
  
  src.cp().process({"ZZ_tt125,ZZ_ww125"})
      .AddSyst(cb, "pdf_qqbar", "lnN", SystMap<>::init
      (1.025));

  src.cp().process({"Zjets"}).channel({"et","mt"})
      .AddSyst(cb, "CMS_zh2l2tau_ZjetBkg_lt_extrap_8TeV", "lnN", SystMap<>::init
      (1.20));
  
  src.cp().process({"Zjets"}).channel({"em"})
      .AddSyst(cb, "CMS_zh2l2tau_ZjetBkg_emu_extrap_8TeV", "lnN", SystMap<>::init
      (1.50));
  
  src.cp().process({"Zjets"}).channel({"tt"})
      .AddSyst(cb, "CMS_zh2l2tau_ZjetBkg_tt_extrap_8TeV", "lnN", SystMap<>::init
      (1.15));
  
  src.cp().process({"Zjets"}).channel({"mt"})
      .AddSyst(cb, "CMS_zh2l2tau_ZjetBkg_mu_extrap_8TeV", "lnN", SystMap<>::init
      (1.10));
  
  src.cp().process({"Zjets"}).channel({"et"})
      .AddSyst(cb, "CMS_zh2l2tau_ZjetBkg_e_extrap_8TeV", "lnN", SystMap<>::init
      (1.10));
  
  src.cp().process(JoinStr({signal,{"ZZ","GGToZZ2L2L","TTZ","WWZ","WZZ","ZZZ","ZH_ww125","ZH_tt125"}})).channel({"et"})
      .AddSyst(cb, "CMS_scale_t_llet_8TeV", "shape", SystMap<>::init
      (1.00));
  
  src.cp().process(JoinStr({signal,{"ZZ","GGToZZ2L2L","TTZ","WWZ","WZZ","ZZZ","ZH_ww125","ZH_tt125"}})).channel({"mt"})
      .AddSyst(cb, "CMS_scale_t_llmt_8TeV", "shape", SystMap<>::init
      (1.00));
  
  src.cp().process(JoinStr({signal,{"ZZ","GGToZZ2L2L","TTZ","WWZ","WZZ","ZZZ","ZH_ww125","ZH_tt125"}})).channel({"tt"})
      .AddSyst(cb, "CMS_scale_t_lltt_8TeV", "shape", SystMap<>::init
      (1.00));
  
  src.cp().process({"GGToZZ2L2L"})
      .AddSyst(cb, "CMS_zh2l2tau_GGZZ2L2LBkg_8TeV", "lnN", SystMap<>::init
      (1.44));
  
  src.cp().process({"TTZ"})
      .AddSyst(cb, "CMS_zh2l2tau_TTZBkg_8TeV", "lnN", SystMap<>::init
      (1.50));
  
  src.cp().process({"GGToZZ2L2L"}).channel({"em"})
      .AddSyst(cb, "CMS_vhtt_ggZZNorm_em_8TeV", "lnN", SystMap<>::init
      (1.05));
  
  src.cp().process({"TTZ"}).channel({"em"})
      .AddSyst(cb, "CMS_vhtt_ttZNorm_em_8TeV", "lnN", SystMap<>::init
      (1.15));
  
  src.cp().process({"ZZ"}).channel({"em"})
      .AddSyst(cb, "CMS_vhtt_zzNorm_em_8TeV", "lnN", SystMap<>::init
      (1.05));

  src.cp().process({"WWZ"})
      .AddSyst(cb, "CMS_vhtt_wwzNorm_8TeV", "lnN", SystMap<>::init
      (1.50));
  
  src.cp().process({"WZZ"})
      .AddSyst(cb, "CMS_vhtt_wzzNorm_8TeV", "lnN", SystMap<>::init
      (1.50));
  
  src.cp().process({"ZZZ"})
      .AddSyst(cb, "CMS_vhtt_zzzNorm_8TeV", "lnN", SystMap<>::init
      (1.50));

  src.cp().process({"GGToZZ2L2L"}).channel({"mt"})
      .AddSyst(cb, "CMS_vhtt_ggZZNorm_mt_8TeV", "lnN", SystMap<>::init
      (1.05));
  
  src.cp().process({"TTZ"}).channel({"mt"})
      .AddSyst(cb, "CMS_vhtt_ttZNorm_mt_8TeV", "lnN", SystMap<>::init
      (1.30));
  
  src.cp().process({"ZZ"}).channel({"mt"})
      .AddSyst(cb, "CMS_vhtt_zzNorm_mt_8TeV", "lnN", SystMap<>::init
      (1.05));

  src.cp().process({"GGToZZ2L2L"}).channel({"et"})
      .AddSyst(cb, "CMS_vhtt_ggZZNorm_et_8TeV", "lnN", SystMap<>::init
      (1.05));
  
  src.cp().process({"TTZ"}).channel({"et"})
      .AddSyst(cb, "CMS_vhtt_ttZNorm_et_8TeV", "lnN", SystMap<>::init
      (1.30));
  
  src.cp().process({"ZZ"}).channel({"et"})
      .AddSyst(cb, "CMS_vhtt_zzNorm_et_8TeV", "lnN", SystMap<>::init
      (1.05));

  src.cp().process({"GGToZZ2L2L"}).channel({"tt"})
      .AddSyst(cb, "CMS_vhtt_ggZZNorm_tt_8TeV", "lnN", SystMap<>::init
      (1.05));
  
  src.cp().process({"TTZ"}).channel({"tt"})
      .AddSyst(cb, "CMS_vhtt_ttZNorm_tt_8TeV", "lnN", SystMap<>::init
      (1.30));
  
  src.cp().process({"ZZ"}).channel({"tt"})
      .AddSyst(cb, "CMS_vhtt_zzNorm_tt_8TeV", "lnN", SystMap<>::init
      (1.05));

}

void AddSystematics_AZh(CombineHarvester & cb) {

  CombineHarvester src = cb.cp();
  AddSystematics_AZh(cb, src);

}
}

