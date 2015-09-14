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
#include "CombinePdfs/interface/MorphFunctions.h"
#include "CombineTools/interface/BinByBin.h"

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

  map<string, string> sig_shape_map = {
      {"et", "_fine_binning"},
      {"mt", "_fine_binning"},
      {"em", ""},
      {"ee", ""},
      {"mm", ""},
      {"tt", "_fine_binning"}
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

  vector<string> masses = ch::ValsFromRange("110:145|5");

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
      string ext = sig_shape_map[chn];
      cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
          file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
          file, "$BIN/$PROCESS$MASS"+ext, "$BIN/$PROCESS$MASS_$SYSTEMATIC"+ext);
    }
  }

  cout << ">> Scaling signal process rates...\n";
  map<string, TGraph> xs;
  // Get the table of H->tau tau BRs vs mass
  xs["htt"] = ch::TGraphFromTable("input/xsecs_brs/htt_YR3.txt", "mH", "br");
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : sig_procs) {
      // Get the table of xsecs vs mass for process "p" and era "e":
      xs[p+"_"+e] = ch::TGraphFromTable("input/xsecs_brs/"+p+"_"+e+"_YR3.txt", "mH", "xsec");
      cout << ">>>> Scaling for process " << p << " and era " << e << "\n";
      cb.cp().process({p}).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * xs[p+"_"+e].Eval(m) * xs["htt"].Eval(m));
      });
    }
  }
  xs["hww_over_htt"] = ch::TGraphFromTable("input/xsecs_brs/hww_over_htt.txt", "mH", "ratio");
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : {"ggH", "qqH"}) {
     cb.cp().channel({"em"}).process({p+"_hww125"}).era({e})
       .ForEachProc([&](ch::Process *proc) {
         proc->set_rate(proc->rate() * xs[p+"_"+e].Eval(125.) * xs["htt"].Eval(125.));
         proc->set_rate(proc->rate() * xs["hww_over_htt"].Eval(125.));
      });
    }
  }

  cout << ">> Merging bin errors and generating bbb uncertainties...\n";

  auto bbb = ch::BinByBinFactory()
      .SetAddThreshold(0.1)
      .SetMergeThreshold(0.5)
      .SetFixNorm(true);

  ch::CombineHarvester cb_et = cb.cp().channel({"et"});
  bbb.MergeAndAdd(cb_et.cp().era({"7TeV"}).bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"7TeV"}).bin_id({3, 5}).process({"W"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"8TeV"}).bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"8TeV"}).bin_id({3, 5}).process({"W"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"7TeV"}).bin_id({6}).process({"ZL", "ZJ", "W", "ZTT"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"8TeV"}).bin_id({6}).process({"ZL", "ZJ", "W"}), cb);
  bbb.MergeAndAdd(cb_et.cp().era({"8TeV"}).bin_id({7}).process({"ZL", "ZJ", "W", "ZTT"}), cb);

  ch::CombineHarvester cb_mt = cb.cp().channel({"mt"});
  bbb.MergeAndAdd(cb_mt.cp().era({"7TeV"}).bin_id({1, 2, 3, 4}).process({"W", "QCD"}), cb);
  bbb.MergeAndAdd(cb_mt.cp().era({"8TeV"}).bin_id({1, 2, 3, 4}).process({"W", "QCD"}), cb);
  bbb.MergeAndAdd(cb_mt.cp().era({"7TeV"}).bin_id({5}).process({"W"}), cb);
  bbb.MergeAndAdd(cb_mt.cp().era({"7TeV"}).bin_id({6}).process({"W", "ZTT"}), cb);
  bbb.MergeAndAdd(cb_mt.cp().era({"8TeV"}).bin_id({5, 6}).process({"W"}), cb);
  bbb.MergeAndAdd(cb_mt.cp().era({"8TeV"}).bin_id({7}).process({"W", "ZTT"}), cb);

  ch::CombineHarvester cb_em = cb.cp().channel({"em"});
  bbb.MergeAndAdd(cb_em.cp().era({"7TeV"}).bin_id({1, 3}).process({"Fakes"}), cb);
  bbb.MergeAndAdd(cb_em.cp().era({"8TeV"}).bin_id({1, 3}).process({"Fakes"}), cb);
  bbb.MergeAndAdd(cb_em.cp().era({"7TeV"}).bin_id({4}).process({"Fakes", "EWK", "Ztt"}), cb);
  bbb.MergeAndAdd(cb_em.cp().era({"8TeV"}).bin_id({5}).process({"Fakes", "EWK", "Ztt"}), cb);
  bbb.MergeAndAdd(cb_em.cp().era({"8TeV"}).bin_id({4}).process({"Fakes", "EWK"}), cb);

  ch::CombineHarvester cb_tt = cb.cp().channel({"tt"});
  bbb.MergeAndAdd(cb_tt.cp().era({"8TeV"}).bin_id({0, 1, 2}).process({"ZTT", "QCD"}), cb);

  bbb.SetAddThreshold(0.);  // ee and mm use a different threshold
  ch::CombineHarvester cb_ll = cb.cp().channel({"ee", "mm"});
  bbb.MergeAndAdd(cb_ll.cp().era({"7TeV"}).bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"}), cb);
  bbb.MergeAndAdd(cb_ll.cp().era({"8TeV"}).bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"}), cb);

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


  map<string, bool> can_morph = {
      {"et", true},
      {"mt", true},
      {"em", true},
      {"ee", false},
      {"mm", false},
      {"tt", true}
  };

  RooWorkspace ws("htt", "htt");
  RooRealVar mh("MH", "", 125, 90, 145);

  bool do_morphing = true;
  if (do_morphing) {
    // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
    for (auto chn : chns) {
      auto bins = cb.cp().channel({chn}).bin_set();
      for (auto bin : bins) {
        for (auto p : sig_procs) {
          ch::BuildRooMorphing(ws, cb, bin, p, mh, "110", "145", "norm",
                               can_morph[chn], false);
        }
      }
    }
    cb.AddWorkspace(ws);
    cb.cp().signals().ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");

    string folder = "output/sm_cards_morphed";
    boost::filesystem::create_directories(folder);

    TFile output((folder + "/htt.input.root").c_str(),
                 "RECREATE");
    for (string chn : chns) {
      boost::filesystem::create_directories(folder+"/"+chn);
      //Use CH to create combined card for each channel
      cb.cp().channel({chn}).mass({"*"}).WriteDatacard(
        folder + "/" + chn + "/combinedCard.txt", output);
      auto bins = cb.cp().channel({chn}).bin_set();
      for (auto b : bins) {
        cout << ">> Writing datacard for bin: " << b << "\r" << flush;
        //Also print individual datacards for each category of each channel
        boost::filesystem::create_directories(folder+"/"+chn);
        cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(
        folder + "/" + chn + "/" + b + ".txt", output);
        //Also print individual datacards for each category of each channel in the combined directory
        boost::filesystem::create_directories(folder+"/cmb");
        cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(
            folder + "/cmb/"+ b + ".txt", output);
      }
    }
    //Use CH to create combined card for full combination
    cb.cp().mass({"*"}).WriteDatacard(
        folder + "/cmb/combinedCard.txt", output);
    output.Close();
    cout << "\n>> Done!\n";
  }
}
