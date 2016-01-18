#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char** argv) {
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string SM125= "";
  string mass = "mA";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);
  
  typedef vector<string> VString;
  typedef vector<pair<int, string>> Categories;
  string input_dir =
      string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/Imperial/";

  VString chns =
      //{"tt"};
      {"mt","et","tt","em"};

  RooRealVar mA(mass.c_str(), mass.c_str(), 90., 1000.);
  RooRealVar mH("mH", "mH", 90., 1000.);
  RooRealVar mh("mh", "mh", 90., 1000.);

  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};
  bkg_procs["mt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};
  bkg_procs["tt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};
  bkg_procs["em"] = {"W", "QCD", "ZLL", "TT", "VV", "ZTT"};


  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  //
  map<string,Categories> cats;
  cats["et_13TeV"] = {
    {8, "et_nobtagnotwoprong"},
    {9, "et_btagnotwoprong"}
    };

  cats["em_13TeV"] = {
    {8, "em_nobtag"},
    {9, "em_btag"}
    };

  cats["tt_13TeV"] = {
    {8, "tt_nobtagnotwoprong"},
    {9, "tt_btagnotwoprong"}
    };
  
  cats["mt_13TeV"] = {
    {8, "mt_nobtagnotwoprong"},
    {9, "mt_btagnotwoprong"}
    };
 

  vector<string> masses = {"90","100","110","120","130","140","160","180", "200", "250", "300", "350", "400", "450", "500", "600", "700", "800", "900","1000"};

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
    vector<string> sig_procs = {"ggH","bbH"};
  for(auto chn : chns){
    cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn+"_13TeV"]);

    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn+"_13TeV"], false);
  
    cb.AddProcesses(masses, {"htt"}, {"13TeV"}, {chn}, signal_types["ggH"], cats[chn+"_13TeV"], true);
    cb.AddProcesses(masses, {"htt"}, {"13TeV"}, {chn}, signal_types["bbH"], cats[chn+"_13TeV"], true);
    }


  ch::AddMSSMRun2Systematics(cb);
  
  //! [part7]
  for (string chn:chns){
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).process(signal_types["ggH"]).ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV.root",
        "$BIN/ggH$MASS",
        "$BIN/ggH$MASS_$SYSTEMATIC");
    cb.cp().channel({chn}).process(signal_types["bbH"]).ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV.root",
        "$BIN/bbH$MASS",
        "$BIN/bbH$MASS_$SYSTEMATIC");
   }
   //Replacing observation with the sum of the backgrounds (asimov) - nice to ensure blinding 
    auto bins = cb.cp().bin_set();
    for (auto b : bins) {
        cb.cp().bin({b}).ForEachObs([&](ch::Observation *obs) {
        obs->set_shape(cb.cp().bin({b}).backgrounds().GetShape(), true);
        });
    } 


  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  RooWorkspace ws("htt", "htt");

  TFile demo("htt_mssm_demo.root", "RECREATE");

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
  //cb.cp().signals().ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.cp().process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.PrintAll();
  
  string folder = "output/mssm_run2/cmb";
  boost::filesystem::create_directories(folder);
  
  cout << "Writing datacards ...";
  TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
  for (string chn : chns) {
    auto bins = cb.cp().channel({chn}).bin_set();
    for (auto b : bins) {
      cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(folder + "/" + b + ".txt", output);
    }
  }
  cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_mssm.txt", output);
  output.Close();

  for (string chn : chns) {
     string folderchn = "output/mssm_run2/"+chn;
     boost::filesystem::create_directories(folderchn);
     TFile outputchn((folderchn + "/htt_"+chn+"_mssm_input.root").c_str(), "RECREATE");
     cb.cp().channel({chn}).mass({"*"}).WriteDatacard(folderchn + "/htt_"+chn+"_mssm.txt", outputchn);
     outputchn.Close();
  }
     
  cout << " done\n";


}

