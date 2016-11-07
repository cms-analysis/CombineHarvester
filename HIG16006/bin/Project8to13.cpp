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
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
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
  bool no_shape_systs=false;
  bool project=false;
  string output_folder = "projection_legacy";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125))
    ("no_shape_systs,s", po::value<bool>(&no_shape_systs)->default_value(false))
    ("output_folder", po::value<string>(&output_folder)->default_value("projection_legacy"))
    ("project,p", po::value<bool>(&project)->default_value(false));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  RooRealVar mA(mass.c_str(), mass.c_str(), 90., 1000.);
  mA.setConstant(true);
  RooRealVar mH("mH", "mH", 90., 1000.);
  RooRealVar mh("mh", "mh", 90., 1000.);

  typedef vector<string> VString;
  string in_dir = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HIG16006/LIMITS111215-legacymssm-unblind/plain/";


  VString chns = {"mt","et","tt","em"};
  
  VString masses={"90","100","120","130","140","160","180","200","250","300","350","400","450","500","600","700","800","900","1000"};

  map<string, VString> signal_types = {
    {"ggH", {"ggh_htautau", "ggH_Htautau", "ggA_Atautau"}},
    {"bbH", {"bbh_htautau", "bbH_Htautau", "bbA_Atautau"}}
  };
  if(mass=="MH") {
    signal_types = {
      {"ggH", {"ggH"}},
      {"bbH", {"bbH"}}
    };
  }

  ch::CombineHarvester cb;
  for(string ms:masses) {
    for(string chn:chns) {
      for(string bin_id : {"8","9"}) {
        if(boost::filesystem::exists((in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())) {
          cb.ParseDatacard(in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
        } else std::cout<<(in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str() << " Doesn't exist" << std::endl;
      }
    }
    //Disable shape systs if required (can be useful to compare with 13 TeV without shape systs)
    if(no_shape_systs) cb.syst_type({"shape"},false);
  }
  
  if(mass!="MH") {
    // Now clone signal procs to create the others if necessary
    ch::CloneProcsAndSysts(cb.cp().process({"ggH"}), cb, [](ch::Object *p) {
      p->set_process("ggH_htautau");
      p->set_process("ggA_htautau");
      p->set_process("ggh_htautau");
    });
    ch::CloneProcsAndSysts(cb.cp().process({"bbH"}), cb, [](ch::Object *p) {
      p->set_process("bbH_htautau");
      p->set_process("bbA_htautau");
      p->set_process("bbh_htautau");
    });
    // Remove the original signals
    cb.process({"ggH", "bbH"}, false);
  }
  // Tidy the CH instance so the background and data_obs are the same for all masses
  cb.FilterAll([&](ch::Object *obj) {
    return (!obj->signal() && obj->mass() != masses[0]);
  });
  cb.ForEachObj([&](ch::Object *obj) {
    if (!obj->signal()) obj->set_mass("*");
  });

  ch::SetStandardBinNames(cb);
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
      auto procs = cb.cp().bin({b}).process(ch::JoinStr({signal_types["ggH"], signal_types["bbH"]})).process_set();
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
  
     

}
            



