#include <string>
#include <map>
#include <vector>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char** argv) {
  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;
  string SM125= "";
  string mass = "mA";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  // We will need to source some inputs from the "auxiliaries" repo
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_shapes   = auxiliaries +"shapes/";

  // RooFit will be quite noisy if we don't set this
  // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mA(mass.c_str(), mass.c_str(), 90., 1000.);
  RooRealVar mH("mH", "mH", 90., 1000.);
  RooRealVar mh("mh", "mh", 90., 1000.);


  TH1::AddDirectory(false);
  ch::CombineHarvester cb;

  Categories mt_cats = {
      make_pair(8, "muTau_nobtag"),
      make_pair(9, "muTau_btag")};

  auto masses = ch::MassesFromRange(
      "90,100,120-140:10,140-200:20,200-500:50,600-1000:100");

  cout << "Adding observations...";
  cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {"mt"}, mt_cats);
  cout << " done\n";

  cout << "Adding background processes...";
  cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {"mt"},
                  {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, mt_cats, false);
  cout << " done\n";

  cout << "Adding signal processes...";
  // Unlike in previous MSSM H->tautau analyses we will create a separate
  // process for each Higgs in the datacards
  map<string, VString> signal_types = {
    {"ggH", {"ggh_htautau", "ggH_Htautau", "ggA_Atautau"}},
    {"bbH", {"bbh_htautau", "bbH_Htautau", "bbA_Atautau"}}
  };
  if(mass=="MH"){
    signal_types = {
      {"ggH", {"ggH"}},
      {"bbH", {"bbH"}}
    };
  }
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["ggH"], {mt_cats[0]}, true);
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["bbH"], {mt_cats[1]}, true);
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["bbH"], {mt_cats[0]}, true);
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["ggH"], {mt_cats[1]}, true);
  cout << " done\n";

  cout << "Adding systematic uncertainties...";
  ch::AddMSSMSystematics(cb);
  cout << " done\n";

  string file = aux_shapes + "Imperial/htt_mt.inputs-mssm-8TeV-0.root";

  cout << "Extracting histograms from input root files...";
  cb.cp().era({"8TeV"}).backgrounds().ExtractShapes(
      file, "$CHANNEL/$PROCESS", "$CHANNEL/$PROCESS_$SYSTEMATIC");

  // We have to map each Higgs signal process to the same histogram, i.e:
  // {ggh, ggH, ggA} --> ggH
  // {bbh, bbH, bbA} --> bbH
  cb.cp().era({"8TeV"}).process(signal_types["ggH"]).ExtractShapes(
      file, "$CHANNEL/ggH$MASS",
      "$CHANNEL/ggH$MASS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).process(signal_types["bbH"]).ExtractShapes(
      file, "$CHANNEL/bbH$MASS",
      "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  cout << " done\n";

  cout << "Scaling signal process rates for acceptance...\n";
  for (string e : {"8TeV"}) {
    for (string p : {"ggH", "bbH"}) {
      cout << "Scaling for process " << p << " and era " << e << "\n";
      auto gr = ch::TGraphFromTable(
          string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/Run1BSMComb/input/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt", "mPhi",
          "accept");
      cb.cp().process(signal_types[p]).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * gr.Eval(m));
      });
    }
  }

  cout << "Setting standardised bin names...";
  ch::SetStandardBinNames(cb);
  cout << " done\n";

  RooWorkspace ws("htt", "htt");

  TFile demo("htt_mt_mssm_demo.root", "RECREATE");

  bool do_morphing = true;
  map<string, RooAbsReal *> mass_var = {
    {"ggh_htautau", &mh}, {"ggH_Htautau", &mH}, {"ggA_Atautau", &mA},
    {"bbh_htautau", &mh}, {"bbH_Htautau", &mH}, {"bbA_Atautau", &mA}
  };
  if(mass=="MH"){
    mass_var = {
      {"ggH", &mA},
      {"bbH", &mA}
    };
  }
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).signals().process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),
                             "norm", true, true, false, &demo);
      }
    }
  }
  demo.Close();
  cb.AddWorkspace(ws);
  cb.cp().process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.PrintAll();

  string folder = "output/mssm_nomodel";
  boost::filesystem::create_directories(folder);

  TFile output((folder + "/htt_mt.input.mssm.root").c_str(), "RECREATE");

  cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_mt_mssm.txt", output);
  auto bins = cb.bin_set();
  for (auto b : bins) {
    cb.cp().bin({b}).mass({"*"}).WriteDatacard(
    folder + "/" + b + ".txt", output);
  }
  output.Close();
}


