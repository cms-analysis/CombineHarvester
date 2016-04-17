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
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char** argv) {
  string SM125= "";
  string mass = "mA";
  bool project=false;
  bool no_shape_systs=false;
  string output_folder = "projection_update";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125))
    ("no_shape_systs,s", po::value<bool>(&no_shape_systs)->default_value(false))
    ("output_folder", po::value<string>(&output_folder)->default_value("projection_update"))
    ("project,p", po::value<bool>(&project)->default_value(false));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);
  
  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  // We will need to source some inputs from the "auxiliaries" repo
  //string SM125        = "";
  //if(argc>1) SM125    = string(argv[1]);
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_shapes   = auxiliaries +"shapes/";
  string aux_pruning  = auxiliaries +"pruning/";
  string input_dir    = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/input";

  VString chns =
      {"mt", "et", "tt", "em"};

  map<string, string> input_folders = {
      {"mt", "LLR"},
      {"et", "LLR"},
      {"tt", "LLR"},
      {"em", "MIT"},
      {"mm", "DESY-KIT"},
  };

  // RooFit will be quite noisy if we don't set this
  // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mA(mass.c_str(), mass.c_str(), 90., 1000.);
  mA.setConstant(true);
  RooRealVar mH("mH", "mH", 90., 1000.);
  RooRealVar mh("mh", "mh", 90., 1000.);
  
  map<string, VString> bkg_procs;
  bkg_procs["mt"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  bkg_procs["et"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  bkg_procs["tt"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  bkg_procs["em"] = {"Ztt", "ttbar", "EWK", "Fakes"};
  bkg_procs["mm"] = {"ZTT", "ZMM", "QCD", "TTJ", "WJets", "Dibosons"};

  TH1::AddDirectory(false);
  ch::CombineHarvester cb;

  VString SM_procs = {"ggH_SM125", "qqH_SM125", "VH_SM125"};

  map<string, Categories> cats;
  cats["mt_8TeV"] = {
    {10, "muTau_nobtag_low"}, {11, "muTau_nobtag_medium"}, {12, "muTau_nobtag_high"}, {13, "muTau_btag_low"}, {14, "muTau_btag_high"}};
  cats["et_8TeV"] = {
    {10, "eleTau_nobtag_low"}, {11, "eleTau_nobtag_medium"}, {12, "eleTau_nobtag_high"}, {13, "eleTau_btag_low"}, {14, "eleTau_btag_high"}};
  cats["tt_8TeV"] = {
    {10, "tauTau_nobtag_low"}, {11, "tauTau_nobtag_medium"}, {12, "tauTau_nobtag_high"}, {13, "tauTau_btag_low"}, {14, "tauTau_btag_high"}};
  cats["em_8TeV"] = {
    {8, "emu_nobtag"}, {9, "emu_btag"}};
  cats["mm_8TeV"] = {
    {8, "mumu_nobtag"}, {9, "mumu_btag"}};

  auto masses = ch::MassesFromRange(
      "90,100,120-140:10,140-200:20,200-500:50,600-1000:100");

  cout << "Adding observations and backgrounds...";
  for (auto chn : chns) {
    cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {chn}, cats[chn+"_8TeV"]);
    cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, bkg_procs[chn], cats[chn+"_8TeV"], false);
    if(SM125==string("signal_SM125")) cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, SM_procs, cats[chn+"_8TeV"], true);  
    else if(SM125==string("bkg_SM125")) cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, SM_procs, cats[chn+"_8TeV"], false);  
  }
  cout << " done\n";
  
  cout << "Adding signal processes...";
  //! [part1]
  // Unlike in previous MSSM H->tautau analyses we will create a separate
  // process for each Higgs in the datacards
  map<string, VString> signal_types = {
    {"ggH", {"ggh_htautau", "ggH_Htautau", "ggA_Atautau"}},
    {"bbH", {"bbh_htautau", "bbH_Htautau", "bbA_Atautau"}}
  };
  //! [part1]
  if(mass=="MH"){
    signal_types = {
      {"ggH", {"ggH"}},
      {"bbH", {"bbH"}}
    };
  }
  //! [part2]
  for (auto chn : chns) {
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {chn}, signal_types["ggH"], cats[chn+"_8TeV"], true);
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {chn}, signal_types["bbH"], cats[chn+"_8TeV"], true);
  }
  //! [part2]
  cout << " done\n";

  cout << "Adding systematic uncertainties...";
  ch::AddMSSMUpdateSystematics_et_mt(cb);
  ch::AddMSSMUpdateSystematics_em(cb);
  ch::AddMSSMUpdateSystematics_mm(cb);
  ch::AddMSSMUpdateSystematics_tt(cb);
  cout << " done\n";   
  
  cb.SetFlag("filters-use-regex", true);
  for(string ms:masses) {
    //Disable shape systs if required (can be useful to compare with 13 TeV without shape systs)
    if(no_shape_systs) cb.syst_type({"shape"},false);
    //Run without tail fits or bbb to make fairest comparison between the 3 sets
    //of limits
    cb.syst_name({".*fine_binning*"},false);
  }

  cout << "Extracting histograms from input root files...";
  for (string chn : chns) {
    string file = aux_shapes + input_folders[chn] + "/htt_" + chn +
      ".inputs-mssm-" + "8TeV" + "-0-CH-HIG-14-029.root";
    cb.cp().channel({chn}).era({"8TeV"}).backgrounds().ExtractShapes
      (file, "$CHANNEL/$PROCESS", "$CHANNEL/$PROCESS_$SYSTEMATIC");   
    if(SM125==string("signal_SM125")) cb.cp().channel({chn}).era({"8TeV"}).process(SM_procs).ExtractShapes(file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
    // We have to map each Higgs signal process to the same histogram, i.e:
    // {ggh, ggH, ggA} --> ggH
    // {bbh, bbH, bbA} --> bbH
  //! [part3]
    cb.cp().channel({chn}).era({"8TeV"}).process(signal_types["ggH"]).ExtractShapes
      (file, "$CHANNEL/ggH$MASS", "$CHANNEL/ggH$MASS_$SYSTEMATIC");
    cb.cp().channel({chn}).era({"8TeV"}).process(signal_types["bbH"]).ExtractShapes
      (file, "$CHANNEL/bbH$MASS", "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  //! [part3]
  }
  cout << " done\n";

  cout << "Scaling signal process rates for acceptance...\n";
  for (string e : {"8TeV"}) {
    for (string p : {"ggH", "bbH"}) {
      cout << "Scaling for process " << p << " and era " << e << "\n";
      auto gr = ch::TGraphFromTable(
          input_dir+"/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt", "mPhi",
          "accept");
      cb.cp().process(signal_types[p]).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * gr.Eval(m));
      });
    }
  }
  cout << "done\n";

/*  cout << "Generating bbb uncertainties...";
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.05)
    .SetFixNorm(true);
  bbb.AddBinByBin(cb.cp().process({"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV", "Ztt", "ttbar", "EWK", "Fakes", "ZMM", "TTJ", "WJets", "Dibosons"}), cb); 
  cout << " done\n";
  */
  cout << "Setting standardised bin names...";
  ch::SetStandardBinNames(cb);
  cout << " done\n";

  //Apply appropriate scalings from 8 to 13 TeV if projection is required
  if(project) {  
    cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
    });
    cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
    });
    cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
    });
    cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
    });
    cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
    });
    cb.cp().process(ch::JoinStr({signal_types["ggH"],signal_types["bbH"]})).ForEachProc([&](ch::Process *proc){
      proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
    });
  }
 

  cout << "Pruning bbb uncertainties...\n";
  VString droplist = ch::ParseFileLines(aux_pruning + "uncertainty-pruning-drop-150602-mssm-taupt-CH.txt");
  cout << ">> Droplist contains " << droplist.size() << " entries\n";

  set<string> to_drop;
  for (auto x : droplist) to_drop.insert(x);
  auto pre_drop = cb.syst_name_set();
  cb.syst_name(droplist, false);
  auto post_drop = cb.syst_name_set();
  cout << ">> Systematics dropped: " << pre_drop.size() - post_drop.size() << "\n";
  cout << "done\n";

  cout << "Creating workspace...\n";
  RooWorkspace ws("htt", "htt");

  TFile demo("htt_mssm_demo.root", "RECREATE");

  //! [part4]
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
      auto procs = cb.cp().bin({b}).process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),"norm", true, true, false, &demo);
      }
    }
  }
  demo.Close();
  cb.AddWorkspace(ws);
  cb.cp().process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
  cb.PrintAll();
  cout << "done\n";
  //! [part4]

 //Write out datacards. Naming convention important for rest of workflow. We
 //make one directory per chn-cat, one per chn and cmb. In this code we only
 //store the individual datacards for each directory to be combined later, but
 //note that it's also possible to write out the full combined card with CH
  ch::CardWriter writer("output/" + output_folder + "/$TAG/$BIN.txt",
                        "output/" + output_folder + "/$TAG/$BIN_input.root");
  // We're not using mass as an identifier - which we need to tell the CardWriter
  // otherwise it will see "*" as the mass value for every object and skip it
  writer.SetWildcardMasses({});
  writer.SetVerbosity(1);

  writer.WriteCards("cmb", cb);
  for (auto chn : chns) {
    // per-channel
    writer.WriteCards(chn, cb.cp().channel({chn}));
  }
  
  cout << " done\n";
}
