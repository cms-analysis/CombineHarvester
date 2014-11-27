#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include "boost/filesystem.hpp"
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Utilities.h"
#include "CombineTools/interface/HttSystematics.h"

using namespace std;

int main() {
  ch::CombineHarvester cb;

  // cb.SetVerbosity(1);

  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_shapes   = auxiliaries +"shapes/";
  string aux_pruning  = auxiliaries +"pruning/";

  VString chns =
      {"et", "mt", "em", "ee", "mm", "tt"};

  map<string, string> input_folders = {
      {"et", "Imperial"},
      {"mt", "Imperial"},
      {"em", "MIT"},
      {"ee", "DESY-KIT"},
      {"mm", "DESY-KIT"},
      {"tt", "CERN"}
  };

  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
  bkg_procs["mt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
  bkg_procs["em"] = {"Ztt", "EWK", "Fakes", "ttbar", "ggH_hww125", "qqH_hww125"};
  bkg_procs["ee"] = {"ZTT", "WJets", "QCD", "ZEE", "TTJ", "Dibosons", "ggH_hww125", "qqH_hww125"};
  bkg_procs["mm"] = {"ZTT", "WJets", "QCD", "ZMM", "TTJ", "Dibosons", "ggH_hww125", "qqH_hww125"};
  bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};

  VString sig_procs = {"ggH", "qqH", "WH", "ZH"};

  map<string, Categories> cats;
  cats["et_7TeV"] = {
      {1, "eleTau_0jet_medium"}, {2, "eleTau_0jet_high"},
      {3, "eleTau_1jet_medium"}, {5, "eleTau_1jet_high_mediumhiggs"},
      {6, "eleTau_vbf"}};

  cats["et_8TeV"] = {
      {1, "eleTau_0jet_medium"}, {2, "eleTau_0jet_high"},
      {3, "eleTau_1jet_medium"}, {5, "eleTau_1jet_high_mediumhiggs"},
      {6, "eleTau_vbf_loose"}, {7, "eleTau_vbf_tight"}};

  cats["mt_7TeV"] = {
      {1, "muTau_0jet_medium"}, {2, "muTau_0jet_high"},
      {3, "muTau_1jet_medium"}, {4, "muTau_1jet_high_lowhiggs"}, {5, "muTau_1jet_high_mediumhiggs"},
      {6, "muTau_vbf"}};

  cats["mt_8TeV"] = {
      {1, "muTau_0jet_medium"}, {2, "muTau_0jet_high"},
      {3, "muTau_1jet_medium"}, {4, "muTau_1jet_high_lowhiggs"}, {5, "muTau_1jet_high_mediumhiggs"},
      {6, "muTau_vbf_loose"}, {7, "muTau_vbf_tight"}};

  cats["em_7TeV"] = {
      {0, "emu_0jet_low"}, {1, "emu_0jet_high"},
      {2, "emu_1jet_low"}, {3, "emu_1jet_high"},
      {4, "emu_vbf_loose"}};

  cats["em_8TeV"] = {
      {0, "emu_0jet_low"}, {1, "emu_0jet_high"},
      {2, "emu_1jet_low"}, {3, "emu_1jet_high"},
      {4, "emu_vbf_loose"}, {5, "emu_vbf_tight"}};

  cats["ee_7TeV"] = {
      {0, "ee_0jet_low"}, {1, "ee_0jet_high"},
      {2, "ee_1jet_low"}, {3, "ee_1jet_high"},
      {4, "ee_vbf"}};
  cats["ee_8TeV"] = cats["ee_7TeV"];

  cats["mm_7TeV"] = {
      {0, "mumu_0jet_low"}, {1, "mumu_0jet_high"},
      {2, "mumu_1jet_low"}, {3, "mumu_1jet_high"},
      {4, "mumu_vbf"}};
  cats["mm_8TeV"] = cats["mm_7TeV"];

  cats["tt_8TeV"] = {
      {0, "tauTau_1jet_high_mediumhiggs"}, {1, "tauTau_1jet_high_highhiggs"},
      {2, "tauTau_vbf"}};

  vector<string> masses = ch::MassesFromRange("110-145:5");

  cout << ">> Creating processes and observations...\n";
  for (string era : {"7TeV", "8TeV"}) {
    for (auto chn : chns) {
      cb.AddObservations(
        {"*"}, {"htt"}, {era}, {chn}, cats[chn+"_"+era]);
      cb.AddProcesses(
        {"*"}, {"htt"}, {era}, {chn}, bkg_procs[chn], cats[chn+"_"+era], false);
      cb.AddProcesses(
        masses, {"htt"}, {era}, {chn}, sig_procs, cats[chn+"_"+era], true);
    }
  }
  // Have to drop ZL from tautau_vbf category
  cb.FilterProcs([](ch::Process const* p) {
    return p->bin() == "tauTau_vbf" && p->process() == "ZL";
  });

  cout << ">> Adding systematic uncertainties...\n";
  ch::AddSystematics_et_mt(cb);
  ch::AddSystematics_em(cb);
  ch::AddSystematics_ee_mm(cb);
  ch::AddSystematics_tt(cb);

  cout << ">> Extracting histograms from input root files...\n";
  for (string era : {"7TeV", "8TeV"}) {
    for (string chn : chns) {
      // Skip 7TeV tt:
      if (chn == "tt" && era == "7TeV") continue;
      string file = aux_shapes + input_folders[chn] + "/htt_" + chn +
                    ".inputs-sm-" + era + "-hcg.root";
      cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
          file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
          file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  }

  cout << ">> Scaling signal process rates...\n";
  map<string, TGraph> xs;
  // Get the table of H->tau tau BRs vs mass
  ch::ParseTable(&xs, "data/xsecs_brs/htt_YR3.txt", {"htt"});
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : sig_procs) {
      // Get the table of xsecs vs mass for process "p" and era "e":
      ch::ParseTable(&xs, "data/xsecs_brs/"+p+"_"+e+"_YR3.txt", {p+"_"+e});
      cout << ">>>> Scaling for process " << p << " and era " << e << "\n";
      cb.cp().process({p}).era({e}).ForEachProc([&](ch::Process *proc) {
        ch::ScaleProcessRate(proc, &xs, p+"_"+e, "htt");
      });
    }
  }
  ch::ParseTable(&xs, "data/xsecs_brs/hww_over_htt.txt", {"hww_over_htt"});
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : {"ggH", "qqH"}) {
     cb.cp().channel({"em"}).process({p+"_hww125"}).era({e})
       .ForEachProc([&](ch::Process *proc) {
         ch::ScaleProcessRate(proc, &xs, p+"_"+e, "htt", "125");
         ch::ScaleProcessRate(proc, &xs, "hww_over_htt", "", "125");
      });
    }
  }

  cout << ">> Merging bin errors...\n";
  ch::CombineHarvester cb_et = move(cb.cp().channel({"et"}));
  for (string era : {"7TeV", "8TeV"}) {
    cb_et.cp().era({era}).bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"})
        .MergeBinErrors(0.1, 0.5);
    cb_et.cp().era({era}).bin_id({3, 5}).process({"W"})
        .MergeBinErrors(0.1, 0.5);
  }
  cb_et.cp().era({"7TeV"}).bin_id({6}).process({"ZL", "ZJ", "W", "ZTT"})
      .MergeBinErrors(0.1, 0.5);
  cb_et.cp().era({"8TeV"}).bin_id({7}).process({"ZL", "ZJ", "W", "ZTT"})
      .MergeBinErrors(0.1, 0.5);
  cb_et.cp().era({"8TeV"}).bin_id({6}).process({"ZL", "ZJ", "W"})
      .MergeBinErrors(0.1, 0.5);

  ch::CombineHarvester cb_mt = move(cb.cp().channel({"mt"}));
  for (string era : {"7TeV", "8TeV"}) {
    cb_mt.cp().era({era}).bin_id({1, 2, 3, 4}).process({"W", "QCD"})
        .MergeBinErrors(0.1, 0.5);
  }
  cb_mt.cp().era({"7TeV"}).bin_id({5}).process({"W"})
      .MergeBinErrors(0.1, 0.5);
  cb_mt.cp().era({"7TeV"}).bin_id({6}).process({"W", "ZTT"})
      .MergeBinErrors(0.1, 0.5);
  cb_mt.cp().era({"8TeV"}).bin_id({5, 6}).process({"W"})
      .MergeBinErrors(0.1, 0.5);
  cb_mt.cp().era({"8TeV"}).bin_id({7}).process({"W", "ZTT"})
      .MergeBinErrors(0.1, 0.5);

  ch::CombineHarvester cb_em = move(cb.cp().channel({"em"}));
  for (string era : {"7TeV", "8TeV"}) {
    cb_em.cp().era({era}).bin_id({1, 3}).process({"Fakes"})
        .MergeBinErrors(0.1, 0.5);
  }
  cb_em.cp().era({"7TeV"}).bin_id({4}).process({"Fakes", "EWK", "Ztt"})
      .MergeBinErrors(0.1, 0.5);
  cb_em.cp().era({"8TeV"}).bin_id({5}).process({"Fakes", "EWK", "Ztt"})
      .MergeBinErrors(0.1, 0.5);
  cb_em.cp().era({"8TeV"}).bin_id({4}).process({"Fakes", "EWK"})
      .MergeBinErrors(0.1, 0.5);

  ch::CombineHarvester cb_ee_mm = move(cb.cp().channel({"ee", "mm"}));
  for (string era : {"7TeV", "8TeV"}) {
    cb_ee_mm.cp().era({era}).bin_id({1, 3, 4})
        .process({"ZTT", "ZEE", "ZMM", "TTJ"})
        .MergeBinErrors(0.0, 0.5);
  }

  ch::CombineHarvester cb_tt = move(cb.cp().channel({"tt"}));
  cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"ZTT", "QCD"})
      .MergeBinErrors(0.1, 0.5);

  cout << ">> Generating bbb uncertainties...\n";
  cb_mt.cp().bin_id({0, 1, 2, 3, 4}).process({"W", "QCD"})
      .AddBinByBin(0.1, true, &cb);
  cb_mt.cp().era({"7TeV"}).bin_id({5}).process({"W"})
      .AddBinByBin(0.1, true, &cb);
  cb_mt.cp().era({"7TeV"}).bin_id({6}).process({"W", "ZTT"})
      .AddBinByBin(0.1, true, &cb);
  cb_mt.cp().era({"8TeV"}).bin_id({5, 6}).process({"W"})
      .AddBinByBin(0.1, true, &cb);
  cb_mt.cp().era({"8TeV"}).bin_id({7}).process({"W", "ZTT"})
      .AddBinByBin(0.1, true, &cb);

  cb_et.cp().bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"})
      .AddBinByBin(0.1, true, &cb);
  cb_et.cp().bin_id({3, 5}).process({"W"})
      .AddBinByBin(0.1, true, &cb);
  cb_et.cp().era({"7TeV"}).bin_id({6}).process({"ZL", "ZJ", "W", "ZTT"})
      .AddBinByBin(0.1, true, &cb);
  cb_et.cp().era({"8TeV"}).bin_id({7}).process({"ZL", "ZJ", "W", "ZTT"})
      .AddBinByBin(0.1, true, &cb);
  cb_et.cp().era({"8TeV"}).bin_id({6}).process({"ZL", "ZJ", "W"})
      .AddBinByBin(0.1, true, &cb);

  cb_em.cp().bin_id({1, 3}).process({"Fakes"})
      .AddBinByBin(0.1, true, &cb);
  cb_em.cp().era({"7TeV"}).bin_id({4}).process({"Fakes", "EWK", "Ztt"})
      .AddBinByBin(0.1, true, &cb);
  cb_em.cp().era({"8TeV"}).bin_id({5}).process({"Fakes", "EWK", "Ztt"})
      .AddBinByBin(0.1, true, &cb);
  cb_em.cp().era({"8TeV"}).bin_id({4}).process({"Fakes", "EWK"})
      .AddBinByBin(0.1, true, &cb);

  cb_ee_mm.cp().bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"})
      .AddBinByBin(0.0, true, &cb);

  cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"QCD", "ZTT"})
      .AddBinByBin(0.1, true, &cb);

  cout << ">> Setting standardised bin names...\n";
  ch::SetStandardBinNames(cb);
  VString droplist = ch::ParseFileLines(
    aux_pruning + "uncertainty-pruning-drop-131128-sm.txt");
  cout << ">> Droplist contains " << droplist.size() << " entries\n";

  set<string> to_drop;
  for (auto x : droplist) to_drop.insert(x);

  auto pre_drop = cb.syst_name_set();
  cb.syst_name(droplist, false);
  auto post_drop = cb.syst_name_set();
  cout << ">> Systematics dropped: " << pre_drop.size() - post_drop.size()
            << "\n";

  // set<string> dropped;
  // set_difference(pre_drop.begin(), pre_drop.end(), post_drop.begin(),
  //                post_drop.end(), inserter(dropped, dropped.end()));

  // set<string> undropped;
  // set_difference(to_drop.begin(), to_drop.end(), dropped.begin(),
  //                dropped.end(), inserter(undropped, undropped.end()));
  // cout << ">> Un-dropped:\n";
  // for (auto const& x : undropped) {
  //   cout << " - " << x << "\n";
  // }

  string folder = "output/sm_cards";
  boost::filesystem::create_directories(folder);

  for (string chn : chns) {
    TFile output((folder + "/htt_" + chn + ".input.root").c_str(),
                 "RECREATE");
    auto bins = cb.cp().channel({chn}).bin_set();
    for (auto b : bins) {
      for (auto m : masses) {
        cout << ">> Writing datacard for bin: " << b << " and mass: " << m
                  << "\r" << flush;
        cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
            folder+"/"+b + "_" + m + ".txt", output);
      }
    }
    cb.cp().channel({chn}).mass({"125", "*"}).WriteDatacard(
        folder+"/htt_" + chn + "_125.txt", output);
    output.Close();
  }

  cout << "\n>> Done!\n";
}
