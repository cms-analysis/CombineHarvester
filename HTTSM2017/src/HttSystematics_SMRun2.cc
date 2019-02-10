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

void AddSMRun2Systematics(CombineHarvester &cb, bool jetfakes, bool embedding, bool regional_jec, bool ggh_wg1, int era) {

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
      "qqH",
      // STXS stage 1
      "qqH_VBFTOPO_JET3VETO", "qqH_VBFTOPO_JET3", "qqH_REST",
      "qqH_PTJET1_GT200", "qqH_VH2JET"};
  std::vector<std::string> signals_VH = {
      // STXS stage 0
      "WH125", "ZH125", "ttH125"};
  std::vector<std::string> signals_ggHToWW = {
     // STXS stage 0
     "ggHWW125"};
  std::vector<std::string> signals_qqHToWW = {
     // STXS stage 0
     "qqHWW125"};
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
              signals_ggHToWW,
              signals_qqHToWW,
              {"ZTT", "TT", "TTT", "TTL", "TTJ", "W", "ZJ", "ZL", "VV", "VVT", "VVL", "VVJ", "ST"}
              });
  // ##########################################################################
  // Uncertainty: Lumi
  // References:
  // - "CMS Luminosity Measurements for the 2016 Data Taking Period"
  //   (PAS, https://cds.cern.ch/record/2257069)
  // Notes:
  // - FIXME: Adapt for fake factor and embedding
  // ##########################################################################

  float lumi_unc = 1.0;
  if (era == 2016) {
      lumi_unc = 1.025;
  } else if (era == 2017) {
      lumi_unc = 1.023;
  }
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<>::init(lumi_unc));

  // ##########################################################################
  // Uncertainty: Trigger efficiency
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  if (era == 2016) {
    cb.cp()
      .channel({"et"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_et_$ERA", "lnN", SystMap<>::init(1.02));
    // 100% uncorrelated for embedded
    cb.cp()
      .channel({"et"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_et_$ERA", "lnN", SystMap<>::init(1.02));
  } else if (era == 2017) {
    cb.cp()
      .channel({"et"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_et_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_xtrigger_et_$ERA", "shape", SystMap<>::init(1.00));
    // 100% uncorrelated for embedded
    cb.cp()
      .channel({"et"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_et_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_xtrigger_emb_et_$ERA", "shape", SystMap<>::init(1.00));
  }

  cb.cp()
      .channel({"mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_mt_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_xtrigger_mt_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_tt_$ERA", "lnN", SystMap<>::init(1.0707));
      
  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_tt", "lnN", SystMap<>::init(1.0707));

  cb.cp()
      .channel({"em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_trigger_em_$ERA", "lnN", SystMap<>::init(1.02));

  // 100% uncorrelated for embedded
  cb.cp()
      .channel({"mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_mt_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_xtrigger_emb_mt_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_tt_$ERA", "lnN", SystMap<>::init(1.0707));

  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_tt", "lnN", SystMap<>::init(1.0707));

  cb.cp()
      .channel({"em"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_trigger_emb_em_$ERA", "lnN", SystMap<>::init(1.02));

  // ##########################################################################
  // Uncertainty: Electron, muon and tau ID efficiency
  // References:
  // Notes:
  // - FIXME: Adapt for fake factor and embedding
  // - FIXME: Handling of ZL in fully-hadronic channel?
  // - FIXME: References?
  // ##########################################################################

  float tauID_corr = 1.0; //correlated between channels
  float tauID_uncorr = 1.0;
  float ditauID_corr = 1.0;
  float ditauID_uncorr = 1.0;
  if (era == 2016) {
      tauID_corr = 1.0275; //using recommendation divided by 2 for 50% correlation between eras as well as 50% correlation between embedded and mc
      tauID_uncorr = 1.01;
      ditauID_corr = 1.045;
      ditauID_uncorr = 1.02;
  } else if (era == 2017) {
      tauID_corr = 1.0135;
      tauID_uncorr = 1.006;
      ditauID_corr = 1.027;
      ditauID_uncorr = 1.012;
  }

  // MC uncorrelated uncertainty
  
  // Electron ID
  cb.cp()
      .channel({"et", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_e", "lnN", SystMap<>::init(1.014));

  // Muon ID
  cb.cp()
      .channel({"mt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_m", "lnN", SystMap<>::init(1.014));

  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$ERA", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$ERA", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(ditauID_uncorr));

  // Embedded uncorrelated uncertainty

  // Electron ID
  cb.cp()
      .channel({"et", "em"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_e", "lnN", SystMap<>::init(1.014));

  // Muon ID
  cb.cp()
      .channel({"mt", "em"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_m", "lnN", SystMap<>::init(1.014));

  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$ERA", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$ERA", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(ditauID_uncorr));


  // MC + embedded correlated uncertainty

  // Electron ID
  cb.cp()
      .channel({"et", "em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.014));

  // Muon ID
  cb.cp()
      .channel({"mt", "em"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.014));

  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(ditauID_uncorr));

  // Tau ID: tt with 1 real taus and 1 jet fake
  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.06));

  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));


  // repeat tt channel for correlated part between 2016 and 2017
  
  // MC uncorrelated uncertainty
  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$CHANNEL", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_eff_mc_t_$CHANNEL", "lnN", SystMap<>::init(ditauID_uncorr));

  // Embedded uncorrelated uncertainty
  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$CHANNEL", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_eff_emb_t_$CHANNEL", "lnN", SystMap<>::init(ditauID_uncorr));

  // MC + embedded correlated uncertainty
  // Tau ID: et and mt with 1 real tau
  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t", "lnN", SystMap<>::init(tauID_corr));

  cb.cp()
      .channel({"et", "mt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL", "lnN", SystMap<>::init(tauID_uncorr));

  // Tau ID: tt with 2 real taus
  cb.cp()
      .channel({"tt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t", "lnN", SystMap<>::init(ditauID_corr));

  cb.cp()
      .channel({"tt"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_eff_t_$CHANNEL", "lnN", SystMap<>::init(ditauID_uncorr));

  // Tau ID: tt with 1 real taus and 1 jet fake
  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t", "lnN", SystMap<>::init(1.06));

  cb.cp()
      .channel({"tt"})
      .process({"W", "ZJ", "TTJ", "VVJ"})
      .AddSyst(cb, "CMS_eff_t_$CHANNEL", "lnN", SystMap<>::init(1.02));

  // ##########################################################################
  // Uncertainty: b-tag and mistag efficiency
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_htt_eff_b_$ERA", "shape", SystMap<>::init(1.00));

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_htt_mistag_b_$ERA", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Electron energy scale
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  // MC uncorrelated uncertainty

  cb.cp()
      .channel({"em", "et"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_scale_mc_e", "shape", SystMap<>::init(0.71));
      
  // Embedded uncorrelated uncertainty
      
  cb.cp()
      .channel({"em", "et"})
      .process({"EMB"})
      .AddSyst(cb, "CMS_scale_emb_e", "shape", SystMap<>::init(0.71));

  // MC + embedded correlated uncertainty

  cb.cp()
      .channel({"em", "et"})
      .process(JoinStr({mc_processes, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_e", "shape", SystMap<>::init(0.71));


  // ##########################################################################
  // Uncertainty: Tau energy scale
  // References:
  // Notes:
  // - Tau energy scale is splitted by decay mode.
  // - FIXME: References?
  // ##########################################################################


  //// per ERA
  // MC uncorrelated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_1prong_$ERA", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_1prong1pizero_$ERA", "shape",
               SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_3prong_$ERA", "shape", SystMap<>::init(0.5));

  // Embedded uncorrelated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_1prong_$ERA", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_1prong1pizero_$ERA", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_3prong_$ERA", "shape", SystMap<>::init(0.5));

  // MC + embedded correlated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(0.5));

  //// correlated part between ERAs
  // MC uncorrelated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_1prong", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_1prong1pizero", "shape",
               SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}}))
      .AddSyst(cb, "CMS_scale_mc_t_3prong", "shape", SystMap<>::init(0.5));

  // Embedded uncorrelated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_1prong", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_1prong1pizero", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"EMB", "jetFakes"})
      .AddSyst(cb, "CMS_scale_emb_t_3prong", "shape", SystMap<>::init(0.5));

  // MC + embedded correlated uncertainty

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_1prong1pizero", "shape", SystMap<>::init(0.5));

  cb.cp()
      .channel({"et", "mt", "tt"})
      .process(JoinStr({signals, {"ZTT", "TTT", "TTL", "VVT", "VVL", "jetFakes"}, {"EMB"}}))
      .AddSyst(cb, "CMS_scale_t_3prong", "shape", SystMap<>::init(0.5));

  // ##########################################################################
  // Uncertainty: Jet energy scale
  // References:
  // - Talk in CMS Htt meeting by Daniel Winterbottom about regional JES splits:
  //   https://indico.cern.ch/event/740094/contributions/3055870/
  // Notes:
  // ##########################################################################

  if (!regional_jec) {
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_scale_j_$ERA", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(mc_processes)
      .AddSyst(cb, "CMS_scale_j", "shape", SystMap<>::init(0.71));
  }

  // Regional JES
  else {
    // uncorrelated between eras
    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta0to3_$ERA", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta0to5_$ERA", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta3to5_$ERA", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(0.71));
    // correlated between eras
    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta0to3", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta0to5", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_eta3to5", "shape", SystMap<>::init(0.71));

    cb.cp()
        .channel({"et", "mt", "tt", "em"})
        .process(mc_processes)
        .AddSyst(cb, "CMS_scale_j_RelativeBal", "shape", SystMap<>::init(0.71));
        
    if (era == 2017) {
      cb.cp()
	  .channel({"et", "mt", "tt", "em"})
          .process(mc_processes)
          .AddSyst(cb, "CMS_scale_j_RelativeSample_$ERA", "shape", SystMap<>::init(1.00));
    }
  }

  // ##########################################################################
  // Uncertainty: MET energy scale and Recoil
  // References:
  // Notes:
  // - FIXME: Clustered vs unclustered MET? Inclusion of JES splitting?
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZTT", "TT", "TTT", "TTL", "TTJ", "W", "ZJ", "ZL", "VV", "VVT", "VVL", "VVJ", "ST"})  //Z and W processes are only included due to the EWK fraction. Make sure that there is no contribution to the shift from the DY or Wjets samples.
      .AddSyst(cb, "CMS_scale_met_unclustered", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process(JoinStr({signals, signals_ggHToWW, signals_qqHToWW, {"ZTT", "ZL", "ZJ", "W"}}))
      .AddSyst(cb, "CMS_htt_boson_scale_met_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
     .process(JoinStr({signals, signals_ggHToWW, signals_qqHToWW,{"ZTT", "ZL", "ZJ", "W"}}))
      .AddSyst(cb, "CMS_htt_boson_reso_met_$ERA", "shape", SystMap<>::init(1.00));

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
      .process({"VVT", "VVJ", "VVL", "VV", "ST"})
      .AddSyst(cb, "CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));

  // TT
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"TTT", "TTL", "TTJ", "TT"})
      .AddSyst(cb, "CMS_htt_tjXsec", "lnN", SystMap<>::init(1.06));

  // W
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"W"})
      .AddSyst(cb, "CMS_htt_wjXsec", "lnN", SystMap<>::init(1.04));

  // Z
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_zjXsec", "lnN", SystMap<>::init(1.04));

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

  cb.cp()
      .channel({"em"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_htt_qcd_0jet_rate_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"em"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_htt_qcd_0jet_shape_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"em"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_htt_qcd_1jet_shape_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"em"})
      .process({"QCD"})
      .AddSyst(cb, "CMS_htt_qcd_iso", "shape", SystMap<>::init(1.00));

  // ##########################################################################
  // Uncertainty: Drell-Yan LO->NLO reweighting
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZTT", "ZL", "ZJ"})
      .AddSyst(cb, "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(0.10));

  // ##########################################################################
  // Uncertainty: TT shape reweighting
  // References:
  // Notes:
  // - FIXME: References?
  // ##########################################################################

  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"TTT", "TTL", "TTJ", "TT"})
      .AddSyst(cb, "CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));

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
  if (era == 2016) {
      cb.cp()
          .channel({"et"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_eFakeTau_$ERA", "lnN", SystMap<>::init(1.11)); //unsplitted 1.155
      cb.cp()
          .channel({"et"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_eFakeTau", "lnN", SystMap<>::init(1.11));
  } else if (era == 2017) {
      cb.cp()
          .channel({"et"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_eFakeTau_$ERA", "lnN", SystMap<>::init(1.113)); //unsplitted 1.16
      cb.cp()
          .channel({"et"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_eFakeTau", "lnN", SystMap<>::init(1.113));
  }

  // Muon fakes
  if (era == 2016) {
      cb.cp()
          .channel({"mt"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_mFakeTau_$ERA", "lnN", SystMap<>::init(1.192)); //unsplitted 1.272
      cb.cp()
          .channel({"mt"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_mFakeTau", "lnN", SystMap<>::init(1.192));
  } else if (era == 2017) {
      cb.cp()
          .channel({"mt"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_mFakeTau_$ERA", "lnN", SystMap<>::init(1.184)); //unsplitted 1.26
      cb.cp()
          .channel({"mt"})
          .process({"ZL"})
          .AddSyst(cb, "CMS_mFakeTau", "lnN", SystMap<>::init(1.184));
  }

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
  // - FIXME: Check VH QCD scale uncertainty
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
  // Uncertainty on branching ratio for HWW at 125 GeV
  cb.cp()
     .channel({"em"})
     .process(JoinStr({signals_ggHToWW,signals_qqHToWW}))
     .AddSyst(cb, "BR_hww_THU", "lnN", SystMap<>::init(1.0099));   
  cb.cp()
     .channel({"em"})
     .process(JoinStr({signals_ggHToWW,signals_qqHToWW}))
     .AddSyst(cb, "BR_hww_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp()
     .channel({"em"})
     .process(JoinStr({signals_ggHToWW,signals_qqHToWW}))
     .AddSyst(cb, "BR_hww_PU_alphas", "lnN", SystMap<>::init(1.0066));
  // QCD scale
  if (!ggh_wg1) {
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
     .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "QCDScale_ggH", "lnN", SystMap<>::init(1.039));
  }
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
     .process(JoinStr({signals_qqH,signals_qqHToWW}))
      .AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZH125"})
      .AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"WH125"})
      .AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ttH125"})
      .AddSyst(cb, "QCDScale_ttH", "lnN", SystMap<>::init(1.08));

  // PDF
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
     .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
     .process(JoinStr({signals_qqH,signals_qqHToWW}))
      .AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ZH125"})
      .AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"WH125"})
      .AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
  cb.cp()
      .channel({"et", "mt", "tt", "em"})
      .process({"ttH125"})
      .AddSyst(cb, "pdf_Higgs_ttH", "lnN", SystMap<>::init(1.036));

  // Gluon-fusion WG1 uncertainty scheme
  if (ggh_wg1) {
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_Mig01", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_Mig12", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_Mu", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_PT120", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_PT60", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_Res", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_VBF2j", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_VBF3j", "shape", SystMap<>::init(1.00));
    cb.cp()
      .channel({"et", "mt", "tt", "em"})
       .process(JoinStr({signals_ggH,signals_ggHToWW}))
      .AddSyst(cb, "THU_ggH_qmtop", "shape", SystMap<>::init(1.00));
  }

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

  // TTbar contamination in embedded events: 10% shape uncertainty of assumed ttbar->tautau event shape
  cb.cp()
    .channel({"et", "mt", "tt", "em"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_htt_emb_ttbar_$ERA", "shape", SystMap<>::init(1.00));

  // Uncertainty of hadronic tau track efficiency correction
  // uncorrelated between eras
  cb.cp()
    .channel({"et", "mt", "tt"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_3ProngEff_$ERA", "shape", SystMap<>::init(0.71));

  cb.cp()
    .channel({"et", "mt", "tt"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_1ProngPi0Eff_$ERA", "shape", SystMap<>::init(0.71));
  // correlated between eras
  cb.cp()
    .channel({"et", "mt", "tt"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_3ProngEff", "shape", SystMap<>::init(0.71));

  cb.cp()
    .channel({"et", "mt", "tt"})
    .process({"EMB"})
    .AddSyst(cb, "CMS_1ProngPi0Eff", "shape", SystMap<>::init(0.71));

  // ##########################################################################
  // Uncertainty: Jet fakes
  // References:
  // - https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
  // Notes:
  // - FIXME: add 2017 norm uncertainties, and properly correlate across years
  // ##########################################################################

  // QCD shape stat.
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));

  // W shape stat.
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_njet0_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_njet1_$CHANNEL_stat_$ERA", "shape", SystMap<>::init(1.00));

  // TT shape stat.
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_njet1_stat_$ERA", "shape", SystMap<>::init(1.00));

  // Shape syst. of different contributions (QCD/W/tt)
  // uncorrelated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_syst_$ERA", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_syst_$ERA", "shape", SystMap<>::init(0.71));
  // correlated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_qcd_$CHANNEL_syst", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_syst", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"et", "mt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_syst", "shape", SystMap<>::init(0.71));

  // Shape syst. in tautau due to using QCD FF also for W / tt
  // uncorrelated between eras
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_$CHANNEL_syst_$ERA", "shape", SystMap<>::init(0.71));
  // correlated between eras
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_w_$CHANNEL_syst", "shape", SystMap<>::init(0.71));
  cb.cp()
      .channel({"tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_tt_$CHANNEL_syst", "shape", SystMap<>::init(0.71));

  //below: jetFakes norm uncertainties. Current values are for 2016, which are probably a good approx. for 2017. To be updated.

  // Stat. norm (uncorrelated across years)
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_norm_stat_$CHANNEL_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
	       ({"mt"}, {1},   1.035) //ggh
	       ({"mt"}, {2},   1.048) //qqh
	       ({"mt"}, {11},  1.028) //w
	       ({"mt"}, {12},  1.037) //ztt
	       ({"mt"}, {13},  1.036) //tt
	       ({"mt"}, {14},  1.033) //ss
	       ({"mt"}, {15},  1.028) //zll
	       ({"mt"}, {16},  1.042) //misc
	       ({"mt"}, {100}, 1.026) //incl
	       ({"et"}, {1},   1.052) //ggh
	       ({"et"}, {2},   1.079) //qqh
	       ({"et"}, {11},  1.047) //w
	       ({"et"}, {12},  1.067) //ztt
	       ({"et"}, {13},  1.059) //tt
	       ({"et"}, {14},  1.038) //ss
	       ({"et"}, {15},  1.067) //zll
	       ({"et"}, {16},  1.076) //misc
	       ({"et"}, {100}, 1.046) //incl
	       ({"tt"}, {1},   1.029) //ggh
	       ({"tt"}, {2},   1.037) //qqh
	       ({"tt"}, {12},  1.035) //ztt
	       ({"tt"}, {16},  1.020) //misc
	       ({"tt"}, {17},  1.029) //noniso
	       ({"tt"}, {100}, 1.029) //incl
	       );

  // Syst. norm: Bin-correlated
  // uncorrelated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_norm_syst_$CHANNEL_$ERA", "lnN", SystMap<channel, bin_id>::init
	       ({"mt"}, {1},   1.049) //ggh
	       ({"mt"}, {2},   1.041) //qqh
	       ({"mt"}, {11},  1.038) //w
	       ({"mt"}, {12},  1.069) //ztt
	       ({"mt"}, {13},  1.037) //tt
	       ({"mt"}, {14},  1.064) //ss
	       ({"mt"}, {15},  1.048) //zll
	       ({"mt"}, {16},  1.064) //misc
	       ({"mt"}, {100}, 1.042) //incl
	       ({"et"}, {1},   1.042) //ggh
	       ({"et"}, {2},   1.040) //qqh
	       ({"et"}, {11},  1.037) //w
	       ({"et"}, {12},  1.062) //ztt
	       ({"et"}, {13},  1.040) //tt
	       ({"et"}, {14},  1.045) //ss
	       ({"et"}, {15},  1.051) //zll
	       ({"et"}, {16},  1.041) //misc
	       ({"et"}, {100}, 1.042) //incl
	       ({"tt"}, {1},   1.068) //ggh
	       ({"tt"}, {2},   1.067) //qqh
	       ({"tt"}, {12},  1.067) //ztt
	       ({"tt"}, {16},  1.078) //misc
	       ({"tt"}, {17},  1.070) //noniso
	       ({"tt"}, {100}, 1.067) //incl
	       );
  // correlated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_norm_syst_$CHANNEL", "lnN", SystMap<channel, bin_id>::init
	       ({"mt"}, {1},   1.049) //ggh
	       ({"mt"}, {2},   1.041) //qqh
	       ({"mt"}, {11},  1.038) //w
	       ({"mt"}, {12},  1.069) //ztt
	       ({"mt"}, {13},  1.037) //tt
	       ({"mt"}, {14},  1.064) //ss
	       ({"mt"}, {15},  1.048) //zll
	       ({"mt"}, {16},  1.064) //misc
	       ({"mt"}, {100}, 1.042) //incl
	       ({"et"}, {1},   1.042) //ggh
	       ({"et"}, {2},   1.040) //qqh
	       ({"et"}, {11},  1.037) //w
	       ({"et"}, {12},  1.062) //ztt
	       ({"et"}, {13},  1.040) //tt
	       ({"et"}, {14},  1.045) //ss
	       ({"et"}, {15},  1.051) //zll
	       ({"et"}, {16},  1.041) //misc
	       ({"et"}, {100}, 1.042) //incl
	       ({"tt"}, {1},   1.068) //ggh
	       ({"tt"}, {2},   1.067) //qqh
	       ({"tt"}, {12},  1.067) //ztt
	       ({"tt"}, {16},  1.078) //misc
	       ({"tt"}, {17},  1.070) //noniso
	       ({"tt"}, {100}, 1.067) //incl
	       );

  // Syst. norm: Bin-dependent, correlated across years
  // uncorrelated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_sub_syst_$CHANNEL_$BIN_$ERA", "lnN", SystMap<channel, bin_id>::init
	       ({"mt"}, {1},   1.028) //ggh
	       ({"mt"}, {2},   1.028) //qqh
	       ({"mt"}, {11},  1.018) //w
	       ({"mt"}, {12},  1.032) //ztt
	       ({"mt"}, {13},  1.021) //tt
	       ({"mt"}, {14},  1.014) //ss
	       ({"mt"}, {15},  1.028) //zll
	       ({"mt"}, {16},  1.025) //misc
	       ({"mt"}, {100}, 1.025) //incl
	       ({"et"}, {1},   1.028) //ggh
	       ({"et"}, {2},   1.025) //qqh
	       ({"et"}, {11},  1.014) //w
	       ({"et"}, {12},  1.028) //ztt
	       ({"et"}, {13},  1.021) //tt
	       ({"et"}, {14},  1.014) //ss
	       ({"et"}, {15},  1.028) //zll
	       ({"et"}, {16},  1.025) //misc
	       ({"et"}, {100}, 1.025) //incl
	       ({"tt"}, {1},   1.021) //ggh
	       ({"tt"}, {2},   1.021) //qqh
	       ({"tt"}, {12},  1.025) //ztt
	       ({"tt"}, {16},  1.021) //misc
	       ({"tt"}, {17},  1.014) //noniso
	       ({"tt"}, {100}, 1.021) //incl
	       );
  // correlated between eras
  cb.cp()
      .channel({"et", "mt", "tt"})
      .process({"jetFakes"})
      .AddSyst(cb, "CMS_ff_sub_syst_$CHANNEL_$BIN", "lnN", SystMap<channel, bin_id>::init
	       ({"mt"}, {1},   1.028) //ggh
	       ({"mt"}, {2},   1.028) //qqh
	       ({"mt"}, {11},  1.018) //w
	       ({"mt"}, {12},  1.032) //ztt
	       ({"mt"}, {13},  1.021) //tt
	       ({"mt"}, {14},  1.014) //ss
	       ({"mt"}, {15},  1.028) //zll
	       ({"mt"}, {16},  1.025) //misc
	       ({"mt"}, {100}, 1.025) //incl
	       ({"et"}, {1},   1.028) //ggh
	       ({"et"}, {2},   1.025) //qqh
	       ({"et"}, {11},  1.014) //w
	       ({"et"}, {12},  1.028) //ztt
	       ({"et"}, {13},  1.021) //tt
	       ({"et"}, {14},  1.014) //ss
	       ({"et"}, {15},  1.028) //zll
	       ({"et"}, {16},  1.025) //misc
	       ({"et"}, {100}, 1.025) //incl
	       ({"tt"}, {1},   1.021) //ggh
	       ({"tt"}, {2},   1.021) //qqh
	       ({"tt"}, {12},  1.025) //ztt
	       ({"tt"}, {16},  1.021) //misc
	       ({"tt"}, {17},  1.014) //noniso
	       ({"tt"}, {100}, 1.021) //incl
	       );
}
} // namespace ch
