#include <string>
#include <vector>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char* argv[]) {
  std::string mass = "MH";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  // We will need to source some inputs from the "auxiliaries" repo
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_cards   = auxiliaries +"datacards/HIG-14-020.r6636";

  auto masses = ch::MassesFromRange("80,90,100,120,140,150,155,160");

  // RooFit will be quite noisy if we don't set this
  // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mHp(mass.c_str(), mass.c_str(), 80., 160.);


  TH1::AddDirectory(false);
  ch::CombineHarvester cb;
  for (auto m : masses) {
    cb.ParseDatacard(
        aux_cards + "/combine_datacard_hplushadronic_m" + m + ".txt", "hplus",
        "8TeV", "tauhad", 0, m);
  }

  SetStandardBinNames(cb);

  // backgrounds are the same in each card, so can drop all but one set
  // and make the mass generic
  cb.FilterAll([&](ch::Object *obj) {
    return (!obj->signal() && obj->mass() != masses[0]);
  });
  cb.ForEachObj([&](ch::Object *obj) {
    if (!obj->signal()) obj->set_mass("*");
    if (obj->signal() && starts_with(obj->process(), "HH")) {
      obj->set_process("tt_ttHchHch");
    }
    if (obj->signal() && starts_with(obj->process(), "HW")) {
      obj->set_process("tt_ttHchW");
    }
  });

  // Also need to rename bbb shape systematics on signal as they all
  // have a mass-point specific name, and BuildRooMorphing depends on
  // the names being identical
  cb.ForEachSyst([&](ch::Systematic *obj) {
    if (obj->signal() && starts_with(obj->name(), "HH"+obj->mass())) {
      std::string old_name = obj->name();
      std::string new_name = old_name;
      boost::replace_all(new_name, "HH"+obj->mass(), "tt_ttHchHch");
      obj->set_name(new_name);
      cb.RenameParameter(old_name, new_name);
    }
    if (obj->signal() && starts_with(obj->name(), "HW"+obj->mass())) {
      std::string old_name = obj->name();
      std::string new_name = old_name;
      boost::replace_all(new_name, "HW"+obj->mass(), "tt_ttHchW");
      obj->set_name(new_name);
      cb.RenameParameter(old_name, new_name);
    }
  });

  cb.PrintAll();

  RooWorkspace ws("hplus", "hplus");

  TFile demo("charged_higgs.root", "RECREATE");

  bool do_morphing = true;
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).signals().process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, mHp,
                             "norm", true, true, &demo);
      }
    }
  }
  demo.Close();
  cb.AddWorkspace(ws);
  cb.cp().signals().ExtractPdfs(cb, "hplus", "$BIN_$PROCESS_morph");
  cb.PrintAll();

  string folder = "output/mssm_nomodel";
  boost::filesystem::create_directories(folder);
  TFile output((folder + "/hplus_tauhad.input.mssm.root").c_str(), "RECREATE");
  cb.cp().mass({"*"}).WriteDatacard(folder + "/hplus_tauhad_mssm.txt", output);
  output.Close();
}


