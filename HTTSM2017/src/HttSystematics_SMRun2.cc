#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include <string>
#include <vector>

using namespace std;

namespace ch {

using ch::syst::SystMap;
using ch::syst::SystMapAsymm;
using ch::syst::era;
using ch::syst::channel;
using ch::syst::bin_id;
using ch::syst::process;
using ch::syst::bin;
using ch::JoinStr;

void AddSMRun2Systematics(CombineHarvester &cb, bool jetfakes, bool embedding) {

  // ##########################################################################
  // Define groups of processes
  // ##########################################################################

  // Signal processes
  std::vector<std::string> signals_ggH = {
      // STXS stage 0
      "ggH",
      // STXS stage 1
      "ggH_0J", "ggH_1J_PTH_0_60", "ggH_1J_PTH_60_120", "ggH_1J_PTH_120_200",
      "ggH_1J_PTH_GT200", "ggH_GE2J_PTH_0_60", "ggH_GE2J_PTH_60_120",
      "ggH_GE2J_PTH_120_200", "ggH_GE2J_PTH_GT200", "ggH_VBFTOPO_JET3VETO",
      "ggH_VBFTOPO_JET3"};
  std::vector<std::string> signals_qqH = {
      // STXS stage 0
      "qqH"
      // STXS stage 1
      "qqH_VBFTOPO_JET3VETO", "qqH_VBFTOPO_JET3", "qqH_REST",
      "qqH_PTJET1_GT200", "qqH_VH2JET"};
  std::vector<std::string> signals_VH = {
      // STXS stage 0
      "WH_htt", "ZH_htt"};
  std::vector<std::string> signals = JoinStr({signals_ggH, signals_qqH, signals_VH});

  // Background processes
  /* // Not used in the function, keep it for documentation purposes.
  std::vector<std::string> backgrounds = {"ZTT",  "W",   "ZL",      "ZJ",
                                          "TTT",  "TTJ", "VVT",     "VVJ",
                                          "EWKZ", "QCD", "jetFakes", "EMB", "TTL"};
  */

  // All processes being taken from simulation
  // FIXME: Adapt for fake factor and embedding
  std::vector<std::string> mc_processes =
      JoinStr({
              signals,
              {"ZTT", "TTT", "TTL", "VVT", "EWKZ", "W", "ZJ", "ZL", "TTJ", "VVJ"}
              });
  // ##########################################################################
  // Uncertainty: Lumi
  // References:
  // - "CMS Luminosity Measurements for the 2016 Data Taking Period"
  //   (PAS, https://cds.cern.ch/record/2257069)
  // Notes:
  // - FIXME: Adapt for fake factor and embedding
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<>::init(1.025));

  // ##########################################################################
  // Uncertainty: Trigger efficiency
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_trigger_et_$ERA", "lnN", SystMap<>::init(1.02));

  cb.cp()
      .channel({"mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_trigger_mt_$ERA", "lnN", SystMap<>::init(1.02));

  cb.cp()
      .channel({"tt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_trigger_tt_$ERA", "lnN", SystMap<>::init(1.02));

  cb.cp()
      .channel({"em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));

  // ##########################################################################
  // Uncertainty: Electron, muon and tau ID efficiency
  // References:
  // Notes:
  // - FIXME: Adapt for fake factor and embedding
  // - FIXME: Handling of ZL in fully-hadronic channel?
  // - FIXME: References?
  // ##########################################################################

  // Electron ID
  cb.cp()
      .channel({"et", "em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_e_$ERA", "lnN", SystMap<>::init(1.02));

  // Muon ID
  cb.cp()
      .channel({"mt", "em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_m_$ERA", "lnN", SystMap<>::init(1.02));

  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.045));

  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process({"ZTT", "TTT", "VVT", "EWKZ", "EMB"})
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.09));

  cb.cp()
      .channel({"tt"})
      .process({"ZTT", "TTT", "VVT", "EWKZ", "EMB"})
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));

  // Tau ID: tt with 1 real taus and 1 jet fake
  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "ZL", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.06));

  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "ZL", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

  // ##########################################################################
  // Uncertainty: b-tag and mistag efficiency
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_htt_eff_b_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_htt_mistag_b_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Electron energy scale
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Tau energy scale
  // References:
  // Notes:
  // - Tau energy scale is splitted by decay mode.
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "EWKZ", "EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "EWKZ", "EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong1pizero_$ERA", "shape",
               SystMap<>::init(1.00));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "EWKZ", "EMB"}}))
      .AddSyst(cb, "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Jet energy scale
  // References:
  // Notes:
  // - Current JES is inclusive. Splitted JES is to be implemented.
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: MET energy scale
  // References:
  // Notes:
  // - FIXME: Clustered vs unclustered MET? Inclusion of JES splitting?
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Background normalizations
  // References:
  // Notes:
  // - FIXME: Remeasure QCD extrapolation factors for SS and ABCD methods?
  //          Current values are measured by KIT.
  // - FIXME: Adapt for fake factor and embedding
  // - FIXME: W uncertainties: Do we need lnN uncertainties based on the Ersatz
  //          study in Run1 (found in HIG-16043 uncertainty model)
  // - FIXME: References?
  // ##########################################################################

  // VV
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"VVT", "VVJ"})
      .AddSyst(cb, "CMS_htt_vvXsec_$ERA", "lnN", SystMap<>::init(1.05));

  // TT
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"TTT", "TTL", "TTJ"})
      .AddSyst(cb, "CMS_htt_tjXsec_$ERA", "lnN", SystMap<>::init(1.06));

  // W
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"W"})
      .AddSyst(cb, "CMS_htt_wjXsec_$ERA", "lnN", SystMap<>::init(1.04));

  // Z
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_zjXsec_$ERA", "lnN", SystMap<>::init(1.04));

  // QCD
  cb.cp()
      .channel({"et"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_ExtrapSSOS_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.05));
  cb.cp()
      .channel({"mt"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_ExtrapSSOS_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.03));
  cb.cp()
      .channel({"tt"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_ExtrapABCD_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.03));

  // ##########################################################################
  // Uncertainty: Drell-Yan LO->NLO reweighting
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: TT shape reweighting
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"TTT", "TTL", "TTJ"})
      .AddSyst(cb, "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Electron/muon to tau fakes and ZL energy scale
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  // ZL energy scale splitted by decay mode
  cb.cp()
      .channel({"et", "mt"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape",
               SystMap<>::init(1.00));

  cb.cp()
      .channel({"et", "mt"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape",
               SystMap<>::init(1.00));

  // Electron fakes
  cb.cp()
      .channel({"et"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_eFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"et"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_eFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));

  // Muon fakes
  cb.cp()
      .channel({"mt"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_mFakeTau_1prong_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"mt"})
      .process({"ZL"})
      .AddSyst(cb, "CMS_mFakeTau_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Jet to tau fakes
  // References:
  // Notes:
  // - FIXME: Adapt for fake factor and embedding
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"W", "TTJ", "ZJ", "VVJ"})
      .AddSyst(cb, "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Theory uncertainties
  // References:
  // - Gluon-fusion WG1 uncertainty scheme:
  //   https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SignalModelingTools
  // Notes:
  // - FIXME: Add TopMassTreatment from HIG-16043 uncertainty model
  // - FIXME: Compare to HIG-16043 uncertainty model:
  //           - PDF uncertainties splitted by category?
  //           - QCDUnc uncertainties?
  //           - UEPS uncertainties?
  // - FIXME: References?
  // ##########################################################################

  // Uncertainty on branching ratio for HTT at 125 GeV
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals)
      .AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals)
      .AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals)
      .AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));

  // QCD scale
  /* Replaced by gluon-fusion WG1 uncertainty scheme
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals_ggH)
      .AddSyst(cb, "QCDScale_ggH", "lnN", SystMap<>::init(1.039));
  */
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals_qqH)
      .AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.004));

  // PDF
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals_ggH)
      .AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(signals_qqH)
      .AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"WH_htt"})
      .AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.019));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZH_htt"})
      .AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.016));

  // Gluon-fusion WG1 uncertainty scheme
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_Mig01_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_Mig12_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_Mu_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_PT120_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_PT60_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_Res_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_VBF2j_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_VBF3j_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process(signals_ggH)
    .AddSyst(cb, "THU_ggH_qmtop_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Embedded events
  // References:
  // - https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauTauEmbeddingSamples2016
  // Notes:
  // ##########################################################################

  // Embedded Normalization: No Lumi, Zjxsec information used, instead derived from data using dimuon selection efficiency
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_htt_doublemutrg_$ERA", "lnN", SystMap<>::init(1.04));

  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_htt_doubletautrg_$ERA", "lnN", SystMap<>::init(1.04));

  // TTbar contamination in embedded events: 10% shape uncertainty of assumed ttbar->tautau event shape
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_htt_emb_ttbar_$ERA", "shape", SystMap<>::init(1.00));

  // Uncertainty of hadronic tau track efficiency correction
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_3ProngEff_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_1ProngPi0Eff_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Jet fakes
  // References:
  // - https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
  // Notes:
  // - FIXME: Add log-normal uncertainties for all categories
  // ##########################################################################

  // QCD norm stat.
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_dm0_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_dm0_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_dm1_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_dm1_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));

  // W norm stat.
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_dm0_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_dm0_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_dm1_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_dm1_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));

  // TT norm stat.
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_dm0_njet0_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_dm0_njet1_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_dm1_njet0_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_dm1_njet1_stat_$ERA", "shape", SystMap<>::init(1.00));

  // Norm syst.
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_syst_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_syst_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(1.00));

  // Stat. norm
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_norm_stat_$CHANNEL_$BIN_$ERA", "lnN", SystMap<>::init(1.05));

  // Syst. norm: Bin-correlated
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_norm_syst_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.05));

  // Syst. norm: Bin-dependent
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_sub_syst_$CHANNEL_$BIN_$ERA", "lnN", SystMap<>::init(1.05));
}
} // namespace ch
