#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Utilities.h"
#include "CombineTools/interface/HttSystematics.h"

using namespace std;
using namespace std::placeholders;

int main() {
  ch::CombineHarvester cb;

  // cb.SetVerbosity(1);

  typedef vector<pair<int, string>> Categories;
  map<string, Categories> cats;

  cats["mt_7TeV"] = {
      {1, "muTau_0jet_medium"},
      {2, "muTau_0jet_high"},
      {3, "muTau_1jet_medium"},
      {4, "muTau_1jet_high_lowhiggs"},
      {5, "muTau_1jet_high_mediumhiggs"},
      {6, "muTau_vbf"}};

  cats["mt_8TeV"] = {
      {1, "muTau_0jet_medium"},
      {2, "muTau_0jet_high"},
      {3, "muTau_1jet_medium"},
      {4, "muTau_1jet_high_lowhiggs"},
      {5, "muTau_1jet_high_mediumhiggs"},
      {6, "muTau_vbf_loose"},
      {7, "muTau_vbf_tight"}};

  cats["ee_7TeV"] = {
      {0, "ee_0jet_low"},
      {1, "ee_0jet_high"},
      {2, "ee_1jet_low"},
      {3, "ee_1jet_high"},
      {4, "ee_vbf"}};
  cats["ee_8TeV"] = cats["ee_7TeV"];

  cats["mm_7TeV"] = {
      {0, "mumu_0jet_low"},
      {1, "mumu_0jet_high"},
      {2, "mumu_1jet_low"},
      {3, "mumu_1jet_high"},
      {4, "mumu_vbf"}};
  cats["mm_8TeV"] = cats["mm_7TeV"];

  cats["tt_8TeV"] = {
      {0, "tauTau_1jet_high_mediumhiggs"},
      {1, "tauTau_1jet_high_highhiggs"},
      {2, "tauTau_vbf"}};

  vector<string> masses = ch::MassesFromRange("110-145:5");

  for (string era : {"7TeV", "8TeV"}) {
    cout << ">> Adding observations for " << era << "...\n";
    cb.AddObservations({"*"}, {"htt"}, {era}, {"mt"}, cats["mt_"+era]);
    cb.AddObservations({"*"}, {"htt"}, {era}, {"ee"}, cats["ee_"+era]);
    cb.AddObservations({"*"}, {"htt"}, {era}, {"mm"}, cats["mm_"+era]);
    cb.AddObservations({"*"}, {"htt"}, {era}, {"tt"}, cats["tt_"+era]);
    cout << " done\n";

    cout << ">> Adding background processes for " << era << "...\n";
    cb.AddProcesses({"*"}, {"htt"}, {era}, {"mt"},
      {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, cats["mt_"+era], false);
    cb.AddProcesses({"*"}, {"htt"}, {era}, {"ee"},
        {"ZTT", "WJets", "QCD", "ZEE", "TTJ", "Dibosons",
         "ggH_hww125", "qqH_hww125"}, cats["ee_"+era], false);
    cb.AddProcesses({"*"}, {"htt"}, {era}, {"mm"},
        {"ZTT", "WJets", "QCD", "ZMM", "TTJ", "Dibosons",
         "ggH_hww125", "qqH_hww125"}, cats["mm_"+era], false);
    cb.AddProcesses({"*"}, {"htt"}, {era}, {"tt"},
      {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, cats["tt_"+era], false);
    // Have to drop ZL from tauTau_vbf
    cb.FilterProcs([](ch::Process const* p) {
      return p->bin() == "tauTau_vbf" && p->process() == "ZL";
    });

    cout << ">> Adding signal processes for " << era << "...\n";
    cb.AddProcesses(masses, {"htt"}, {era}, {"mt"},
        {"ggH", "qqH", "WH", "ZH"}, cats["mt_"+era], true);
    cb.AddProcesses(masses, {"htt"}, {era}, {"ee"},
        {"ggH", "qqH", "WH", "ZH"}, cats["ee_"+era], true);
    cb.AddProcesses(masses, {"htt"}, {era}, {"mm"},
        {"ggH", "qqH", "WH", "ZH"}, cats["mm_"+era], true);
    cb.AddProcesses(masses, {"htt"}, {era}, {"tt"},
        {"ggH", "qqH", "WH", "ZH"}, cats["tt_"+era], true);
  }

  cout << ">> Adding systematic uncertainties...\n";
  ch::AddSystematics_et_mt(cb);
  ch::AddSystematics_ee_mm(cb);
  ch::AddSystematics_tt(cb);

  cout << ">> Extracting histograms from input root files...\n";
  for (string era : {"7TeV", "8TeV"}) {
    for (string chn : {"ee", "mm", "mt", "tt"}) {
      cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
          "data/sm-legacy/htt_" + chn + ".inputs-sm-" + era + "-hcg.root",
          "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
          "data/sm-legacy/htt_" + chn + ".inputs-sm-" + era + "-hcg.root",
          "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  }

  cout << ">> Scaling signal process rates...\n";
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : {"ggH", "qqH", "WH", "ZH"}) {
      map<string, TGraph> xs;
      ch::ParseTable(&xs, "data/xsecs_brs/"+p+"_"+e+"_YR3.txt", {p+"_"+e});
      ch::ParseTable(&xs, "data/xsecs_brs/htt_YR3.txt", {"htt"});
      cout << ">>>> Scaling for process " << p << " and era " << e << "\n";
      cb.cp().process({p}).era({e}).ForEachProc(
          bind(ch::ScaleProcessRate, _1, &xs, p+"_"+e, "htt"));
    }
  }

  cout << ">> Setting standardised bin names...\n";
  ch::SetStandardBinNames(cb);

  cout << ">> Merging bin errors...";
  cb.cp().channel({"mt"}).bin_id({0, 1, 2, 3, 4}).process({"W", "QCD"})
      .MergeBinErrors(0.1, 0.4);
  cb.cp().channel({"mt"}).bin_id({5}).era({"7TeV"}).process({"W"})
      .MergeBinErrors(0.1, 0.4);
  cb.cp().channel({"mt"}).bin_id({5, 6}).era({"8TeV"}).process({"W"})
      .MergeBinErrors(0.1, 0.4);
  cb.cp().channel({"mt"}).bin_id({7}).era({"8TeV"}).process({"W", "ZTT"})
      .MergeBinErrors(0.1, 0.4);
  cb.cp().channel({"ee", "mm"}).bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"})
      .MergeBinErrors(0.0, 0.4);
  cb.cp().channel({"tt"}).bin_id({0, 1, 2}).era({"8TeV"}).process({"ZTT", "QCD"})
      .MergeBinErrors(0.1, 0.4);

  cout << ">> Generating bbb uncertainties...\n";
  cb.cp().channel({"mt"}).bin_id({0, 1, 2, 3, 4}).process({"W", "QCD"})
      .AddBinByBin(0.1, true, &cb);
  cb.cp().channel({"mt"}).bin_id({5}).era({"7TeV"}).process({"W"})
      .AddBinByBin(0.1, true, &cb);
  cb.cp().channel({"mt"}).bin_id({5, 6}).era({"8TeV"}).process({"W"})
      .AddBinByBin(0.1, true, &cb);
  cb.cp().channel({"mt"}).bin_id({7}).era({"8TeV"}).process({"W", "ZTT"})
      .AddBinByBin(0.1, true, &cb);
  cb.cp().channel({"ee", "mm"}).bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"})
      .AddBinByBin(0.0, true, &cb);
  cb.cp().channel({"tt"}).bin_id({0, 1, 2}).era({"8TeV"}).process({"QCD", "ZTT"})
      .AddBinByBin(0.1, true, &cb);

  for (string& chn : vector<string>{"ee", "mm", "mt", "tt"}) {
    TFile output(("output/sm_cards/htt_" + chn + ".input.root").c_str(),
                 "RECREATE");
    set<string> bins = cb.cp().channel({chn}).bin_set();
    for (auto b : bins) {
      for (auto m : masses) {
        cout << ">> Writing datacard for bin: " << b << " and mass: " << m
                  << "\r" << flush;
        cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
            "output/sm_cards/"+b + "_" + m + ".txt", output);
      }
    }
    cb.cp().channel({chn}).mass({"125", "*"}).WriteDatacard(
        "output/sm_cards/htt_" + chn + "_125.txt", output);
    output.Close();
  }
  // TFile output("htt_combined.input.root", "RECREATE");
  // cout << "\n>> Writing combined datacard\n";
  // cb.cp().mass({"*", "125"}).WriteDatacard("htt_mt_125_combined.txt", output);
  cout << "\n>> Done!\n";
  // output.Close();
}
