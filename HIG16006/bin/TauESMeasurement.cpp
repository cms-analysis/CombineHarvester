#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "boost/lexical_cast.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;
using ch::syst::SystMap;
using ch::syst::SystMapAsymm;
using ch::syst::era;
using ch::syst::channel;
using ch::syst::bin_id;
using ch::syst::process;
using ch::JoinStr;
using namespace ch;


int main(int argc, char** argv) {
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string SM125= "";
  string mass = "mA";
  string output_folder = "mssm_run2";
  string input_folder="shapes/Imperial/datacards-76X/";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("input_folder", po::value<string>(&input_folder)->default_value("shapes/Imperial/datacards-76X/"))
    ("output_folder", po::value<string>(&output_folder)->default_value("mssm_run2"))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);
  
  typedef vector<string> VString;
  typedef vector<pair<int, string>> Categories;
  string input_dir =
      "./"+input_folder+"/";

  VString chns =
      //{"tt"};
      {"mt"};
   //   {"mt","et"};

  RooRealVar taues("taues", "taues", -3.0, 3.0);

  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV"};
  bkg_procs["mt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV"};
  //bkg_procs["tt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};

  map<string,Categories> cats;
  
  cats["et_13TeV"] = {
    {1, "et_inclusive"},
    {2, "et_1prong1pi0"},
    {3, "et_1prong1pi0Pt20To30"},
    {4, "et_1prong1pi0Pt30To40"},
    {5, "et_1prong1pi0Pt40To50"},
    {6, "et_1prong1pi0Pt50To60"},
    {7, "et_1prong1pi0Pt60To70"},
    {8, "et_1prong1pi0Pt70ToInf"},
    {9, "et_3prong"},
    {10, "et_3prongPt20To30"},
    {11, "et_3prongPt30To40"},
    {12, "et_3prongPt40To50"},
    {13, "et_3prongPt50To60"},
    {14, "et_3prongPt60To70"},
    {15, "et_3prongPt70ToInf"}
    };

  cats["mt_13TeV"] = {
    //{1, "mt_inclusive"},
    //{2, "mt_1prong1pi0"},
    {3, "mt_1prong1pi0Pt20To30"},
    {4, "mt_1prong1pi0Pt30To40"},
    {5, "mt_1prong1pi0Pt40To50"}
    //{6, "mt_1prong1pi0Pt50To60"},
    //{7, "mt_1prong1pi0Pt60To70"},
    //{8, "mt_1prong1pi0Pt70ToInf"},
    //{9, "mt_3prong"},
  //  {10, "mt_3prongPt20To30"}
    //{11, "mt_3prongPt30To40"},
    //{12, "mt_3prongPt40To50"},
    //{13, "mt_3prongPt50To60"},
    //{14, "mt_3prongPt60To70"},
    //{15, "mt_3prongPt70ToInf"}
    };
 
  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;

  vector<string> masses = {"-3","-2.5","-2","-1.5","-1","-0.5","0","0.5","1","1.5","2","2.5","3"}; 
  //vector<string> masses = {"-3","-2","-1","0","1","2","3"}; 

  for(auto chn : chns){
    cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn+"_13TeV"]);

    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn+"_13TeV"], false);
  
    cb.AddProcesses(masses, {"htt"}, {"13TeV"}, {chn}, {"ZTT"}, cats[chn+"_13TeV"], true);
    }


  auto signal = Set2Vec(cb.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  cb.cp().process(ch::JoinStr({signal, {"ZTT", "TT","VV","W"}})).channel({"em","mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({signal, {"ZLL"}})).channel({"em"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({signal, {"ZL","ZJ"}})).channel({"mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));


 // cb.cp().process(ch::JoinStr({signal, {"TT","VV","ZLL","ZTT","W"}})).channel({"em"})
 //     .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({signal, {"TT","VV","ZL","ZJ","ZTT","W"}})).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"TT","VV","ZL","W","ZJ","ZTT","ZLL"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().channel({"et","tt","mt"}).process({"ZL","ZJ"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.03));
 
  cb.cp().process({"QCD"}).channel({"et","em","tt","mt"}).AddSyst(cb,
      "CMS_htt_QCD_13TeV","lnN",SystMap<>::init(1.3));

  cb.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.30));

  cb.cp().process({"W"}).channel({"mt"}).AddSyst(cb,
     "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.50));

  
  //! [part7]
  for (string chn:chns){
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV-rebin.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).process({"ZTT"}).ExtractShapes(
        input_dir + "htt_"+chn+".inputs-mssm-13TeV-rebin.root",
        "$BIN/ZTT_$MASS",
        "$BIN/ZTT_$MASS_$SYSTEMATIC");
   }

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]
   
  //cb.cp().VariableRebin({0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6});    
  cb.cp().VariableRebin({0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3});    

  //! [part9]
  // First we generate a set of bin names:
  RooWorkspace ws("htt", "htt");

  TFile demo("htt_mssm_demo.root", "RECREATE");

  bool do_morphing = true;
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).signals().process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, taues,
                             "norm", true, true, false, &demo);
      }
    }
  }
  demo.Close();
  cb.AddWorkspace(ws);
  cb.cp().process({"ZTT"}).ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.PrintAll();
  
  string folder = "output/"+output_folder+"/cmb";
  boost::filesystem::create_directories(folder);
 
 //Write out datacards. Naming convention important for rest of workflow. We
 //make one directory per chn-cat, one per chn and cmb. In this code we only
 //store the individual datacards for each directory to be combined later, but
 //note that it's also possible to write out the full combined card with CH
 
 cout << "Writing datacards ...";

  //Individual channel-cats  
  for (string chn : chns) {
     string folderchn = "output/"+output_folder+"/"+chn;
     auto bins = cb.cp().channel({chn}).bin_set();
      for (auto b : bins) {
        string folderchncat = "output/"+output_folder+"/"+b;
        boost::filesystem::create_directories(folderchn);
        boost::filesystem::create_directories(folderchncat);
        TFile output((folder + "/"+b+"_input.root").c_str(), "RECREATE");
        TFile outputchn((folderchn + "/"+b+"_input.root").c_str(), "RECREATE");
        TFile outputchncat((folderchncat + "/"+b+"_input.root").c_str(), "RECREATE");
        cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(folderchn + "/" + b + ".txt", outputchn);
        cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(folderchncat + "/" + b + ".txt", outputchncat);
        cb.cp().channel({chn}).bin({b}).mass({"*"}).WriteDatacard(folder + "/" + b + ".txt", output);
        output.Close();
        outputchn.Close();
        outputchncat.Close();
    }
  }
     
  cout << " done\n";


}

