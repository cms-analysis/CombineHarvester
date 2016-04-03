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
      {"mt","et"};
   //   {"mt","et"};


  map<string, VString> bkg_procs;
  bkg_procs["et"] = {"W", "ZL", "ZJ", "TT", "VV", "ZTT"};
  bkg_procs["mt"] = {"W", "ZL", "ZJ", "TT", "VV", "ZTT"};
  //bkg_procs["tt"] = {"W", "QCD", "ZL", "ZJ", "TT", "VV","ZTT"};

  map<string,Categories> cats;
  
  cats["mt_13TeV"] = {
    {1, "mt_inclusive"},
    {8, "mt_nobtag"},
    {9, "mt_btag"}
    };
  cats["et_13TeV"] = {
    {1, "et_inclusive"},
    {8, "et_nobtag"},
    {9, "et_btag"}
    };
 
  map<string, vector<double> > binning;
  binning["mt_inclusive"] = {0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,220,240,260};
  binning["et_inclusive"] = {0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,220,240,260};
  
  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;


  for(auto chn : chns){
    cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn+"_13TeV"]);

    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn+"_13TeV"], false);
  
    cb.AddProcesses({"*"}, {"htt"}, {"13TeV"}, {chn}, {"QCD"}, cats[chn+"_13TeV"], true);
    }


  auto signal = Set2Vec(cb.cp().signals().SetFromProcs(
      std::mem_fn(&Process::process)));

  cb.cp().process({"ZTT", "TT","VV","W"}).channel({"em","mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"ZLL"}).channel({"em"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"ZL","ZJ"}).channel({"mt"})
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));


 // cb.cp().process(ch::JoinStr({signal, {"TT","VV","ZLL","ZTT","W"}})).channel({"em"})
 //     .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"TT","VV","ZL","ZJ","ZTT","W"}).channel({"et"})
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"TT","VV","ZL","W","ZJ","ZTT","ZLL"}).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.027));

  cb.cp().channel({"et","tt","mt"}).process({"ZL","ZJ","ZTT"}).AddSyst(cb, "CMS_htt_zttNorm_13TeV", "lnN", SystMap<>::init(1.20));
 
  cb.cp().channel({"et"}).process({"ZTT", "TT", "VV"})
      .AddSyst(cb, "CMS_eff_t_et_13TeV", "lnN", SystMap<>::init(1.08));
  
  cb.cp().channel({"mt"}).process({"ZTT", "TT", "VV"})
      .AddSyst(cb, "CMS_eff_t_mt_13TeV", "lnN", SystMap<>::init(1.08));

//  cb.cp().process({"QCD"}).channel({"et","em","tt","mt"}).AddSyst(cb,
//      "CMS_htt_QCD_13TeV","lnN",SystMap<>::init(1.3));

  cb.cp().process({"VV"}).AddSyst(cb,
      "CMS_htt_VVNorm_13TeV", "lnN", SystMap<>::init(1.30));

  cb.cp().process({"W"}).channel({"mt"}).AddSyst(cb,
     "CMS_htt_WNorm_13TeV","lnN",SystMap<>::init(1.30));

  
  //! [part7]
  for (string chn:chns){
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        input_dir + "datacard_m_vis_"+chn+"_2015_iso0p2-0p5.root",
        "$BIN/$PROCESS",
        "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).process({"QCD"}).ExtractShapes(
        input_dir + "datacard_m_vis_"+chn+"_2015_iso0p2-0p5.root",
        "$BIN/QCD",
        "$BIN/QCD_$SYSTEMATIC");
   }

  auto bins = cb.cp().bin_set();
  bool manual_rebin = false;  
  if(manual_rebin) {
      for(auto b : bins) {
        std::cout << "Rebinning by hand for bin: " << b <<  std::endl;
        cb.cp().bin({b}).VariableRebin(binning[b]);    
      }
  }
  

  
  cout << "Generating bbb uncertainties...";
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.4)
    .SetFixNorm(true);
  bbb.MergeAndAdd(cb.cp().process({"ZTT","W", "ZJ", "ZL", "TT", "VV", "ttbar", "EWK", "Fakes", "ZMM", "TTJ", "WJets", "Dibosons"}), cb); 
  cout << " done\n";

  // This function modifies every entry to have a standardised bin name of
  
  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]
  
  //! [part9]
  // First we generate a set of bin names:
/*  RooWorkspace ws("htt", "htt");

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
  cb.PrintAll();*/
  
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

