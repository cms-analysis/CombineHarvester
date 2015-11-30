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
      string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombinePdfs/";

  VString chns =
      {"mt"};

  RooRealVar mA(mass.c_str(), mass.c_str(), 160., 1000.);
  RooRealVar mH("mH", "mH", 160., 1000.);
  RooRealVar mh("mh", "mh", 160., 1000.);

  map<string, VString> bkg_procs;
  //bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};
  bkg_procs["mt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};
//  bkg_procs["em"] = {"QCD", "ZLL", "TT", "VV", "W","ZTT"};


  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  //
  map<string,Categories> cats;
  /*cats["et_13TeV"] = {
    {8, "et_nobtag"},
    {9, "et_btag"}
    };*/
  
  cats["mt_13TeV"] = {
    {8, "mt_nobtag"},
    {9, "mt_btag"}
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


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


  //cb.cp().process({"ggH","bbH"})
  //    .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT", "TT"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZLL","ZTT","W"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

//  cb.cp().channel({"em"}).process(ch::JoinStr({sig_procs, {"TT","VV","ZLL","ZTT","W"}})).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

//  cb.cp().channel({"em"}).AddSyst(cb, "CMS_scale_j_13TeV", "lnN", SystMap<era,process>::init
 //     ({"13TeV"}, {"TT"},          0.91)
  //    ({"13TeV"}, {"VV"},            0.98));


 // cb.cp().process(ch::JoinStr({sig_procs, {"TT","VV","ZL","W","ZJ","ZTT"}})).channel({"et"})
 //     .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));
  
  cb.cp().process({"TT","VV","ZL","W","ZJ","ZTT","ZLL"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().process({"ZTT"})
      .AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().process(sig_procs).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

//  cb.cp().channel({"em"}).process({"ZLL"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
//  cb.cp().channel({"et"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
  cb.cp().channel({"mt"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));

  cb.cp().process({"TT"})
      .AddSyst(cb, "CMS_htt_ttbarNorm_13TeV", "lnN", SystMap<era>::init
        ({"13TeV"}, 1.10));

/*  cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb,
      "CMS_htt_em_QCD_13TeV","lnN",SystMap<>::init(1.3));

 cb.cp().process({"QCD"}).channel({"et"}).AddSyst(cb,
      "CMS_htt_et_QCD_13TeV","lnN",SystMap<>::init(1.3));*/

 cb.cp().process({"QCD"}).channel({"mt"}).AddSyst(cb,
      "CMS_htt_mt_QCD_13TeV","lnN",SystMap<>::init(1.3));

  cb.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.15));

  cb.cp().process({"W"}).channel({"mt"}).AddSyst(cb,
     "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.2));

/*  cb.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {1},     {"ggH"},        1.04)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.10)
        ({"8TeV"}, {2},     {"qqH"},        1.04)
        ({"8TeV"}, {2},     {"TT"},         1.05));
*/

//  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT"}}))
 //     .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));
  //! [part6]

  //! [part7]
  for (string chn:chns){
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV-new.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).process(signal_types["ggH"]).ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV-new.root",
        "$BIN/ggH$MASS",
        "$BIN/ggH$MASS_$SYSTEMATIC");
    cb.cp().channel({chn}).process(signal_types["bbH"]).ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV-new.root",
        "$BIN/bbH$MASS",
        "$BIN/bbH$MASS_$SYSTEMATIC");
   }

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
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
  //cb.cp().signals().ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.cp().process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.PrintAll();
  
  string folder = "output/mssm_run2_mhmodp";
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
  cout << " done\n";


}

