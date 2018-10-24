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
#include "boost/regex.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/Algorithm.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/HTTSMCP2016/interface/HttSystematics_SMRun2.h"
#include "CombineHarvester/HTTSMCP2016/interface/HttSystematics_SMRun2_2017.h"
#include "CombineHarvester/CombineTools/interface/JsonTools.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "TF1.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

template <typename T>
void To1Bin(T* proc)
{
    std::unique_ptr<TH1> originalHist = proc->ClonedScaledShape();
    TH1F *hist = new TH1F("hist","hist",1,0,1);
    double err = 0;
    double rate =
    originalHist->IntegralAndError(0, originalHist->GetNbinsX() + 1, err);
    hist->SetDirectory(0);
    hist->SetBinContent(1, rate);
    hist->SetBinError(1, err);
    proc->set_shape(*hist, true);  // True means adjust the process rate to the
    // integral of the hist
}


void DecorrelateSyst (ch::CombineHarvester& cb, string name, double correlation, std::vector<string> chans_2016, std::vector<string> chans_2017) {
  if (correlation >= 1.) return;
  auto cb_syst = cb.cp().syst_name({name});
  double val = sqrt(1. - correlation);
  // clone 2016 systs
  ch::CloneSysts(cb.cp().channel(chans_2016).syst_name({name}), cb, [&](ch::Systematic *s) {
      s->set_name(s->name()+"_2016");
      if (s->type().find("shape") != std::string::npos) {
        s->set_scale(s->scale() * val);
      }
      if (s->type().find("lnN") != std::string::npos) {
        s->set_value_u((s->value_u() - 1.) * val + 1.);
        if (s->asymm()){
          s->set_value_d((s->value_d() - 1.) * val + 1.);
        }
      }
  });
  // clone 2017 systs
  ch::CloneSysts(cb.cp().channel(chans_2017).syst_name({name}), cb, [&](ch::Systematic *s) {
      s->set_name(s->name()+"_2017");
      if (s->type().find("shape") != std::string::npos) {
        s->set_scale(s->scale() * val);
      }
      if (s->type().find("lnN") != std::string::npos) {
        s->set_value_u((s->value_u() - 1.) * val + 1.);
        if (s->asymm()){
          s->set_value_d((s->value_d() - 1.) * val + 1.);
        }
      }
  });

  if(correlation>0.) {
    // re-scale un-correlated part
    double val = sqrt(correlation);
    cb_syst.ForEachSyst([val](ch::Systematic *syst) {
      if (syst->type().find("shape") != std::string::npos) {
        syst->set_scale(syst->scale() * val);
      }
      if (syst->type().find("lnN") != std::string::npos) {
        syst->set_value_u((syst->value_u() - 1.) * val + 1.);
        if (syst->asymm()){
          syst->set_value_d((syst->value_d() - 1.) * val + 1.);
        }
      }
    });
  } else {
    // remove uncorrelated part if systs are 100% un-correlated
    cb.FilterSysts([&](ch::Systematic *s){
        return s->name().find(name) != std::string::npos && s->name().find("_2016") == std::string::npos && s->name().find("_2017") == std::string::npos;
    });

  }
}

int main(int argc, char** argv) {

    string output_folder = "sm_run2";
    string input_folder_em="Imperial/CP/";
    string input_folder_et="Imperial/CP/";
    string input_folder_mt="Imperial/CP/";
    string input_folder_tt="Imperial/CP/";
    string input_folder_mm="USCMS/";
    string only_init="";
    string scale_sig_procs="";
    string postfix="";
    bool ttbar_fit = false;
    bool real_data = true;
    bool no_shape_systs = false;
    bool do_embedding = true;
    bool auto_rebin = false;
    bool no_jec_split = false;    
    bool do_jetfakes = true;
    bool do_mva = false;    
    bool do_control_plots = false;
    string era;
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
    ("input_folder_em", po::value<string>(&input_folder_em)->default_value("Imperial/CP/mva_241018"))
    ("input_folder_et", po::value<string>(&input_folder_et)->default_value("Imperial/CP/mva_241018"))
    ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("Imperial/CP/mva_241018"))
    ("input_folder_tt", po::value<string>(&input_folder_tt)->default_value("Imperial/CP/mva_241018"))
    ("input_folder_mm", po::value<string>(&input_folder_mm)->default_value("USCMS"))
    ("only_init", po::value<string>(&only_init)->default_value(""))
    ("real_data", po::value<bool>(&real_data)->default_value(real_data))
    ("scale_sig_procs", po::value<string>(&scale_sig_procs)->default_value(""))
    ("postfix", po::value<string>(&postfix)->default_value(postfix))
    ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"))
    ("no_shape_systs", po::value<bool>(&no_shape_systs)->default_value(no_shape_systs))
    ("do_embedding", po::value<bool>(&do_embedding)->default_value(true))
    ("do_jetfakes", po::value<bool>(&do_jetfakes)->default_value(true))
    ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(true))
    ("no_jec_split", po::value<bool>(&no_jec_split)->default_value(true))    
    ("do_mva", po::value<bool>(&do_mva)->default_value(false))
    ("do_control_plots", po::value<bool>(&do_control_plots)->default_value(false))    
    ("era", po::value<string>(&era)->default_value("2016"))
    ("ttbar_fit", po::value<bool>(&ttbar_fit)->default_value(true));

    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);
    typedef vector<string> VString;
 
    VString years;
    if ( era.find("2016") != std::string::npos ) years.push_back("2016");
    if ( era.find("2017") != std::string::npos ) years.push_back("2017");
    if ( era=="all" ) years = {"2016","2017"};
 
    typedef vector<string> VString;
    typedef vector<pair<int, string>> Categories;
    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    //    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/AllROOT_20fb/";
    std::map<string, string> input_dir;
    input_dir["em"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_em+"/";
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_et+"/";
    input_dir["tt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_tt+"/";
    input_dir["ttbar"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_em+"/";    
    
    
    VString chns = {"tt","et","mt","em"};
    if (ttbar_fit) chns.push_back("ttbar");
    
    map<string, VString> bkg_procs;
    bkg_procs["et"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
    bkg_procs["mt"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
    bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT","VVJ", "EWKZ"};
    bkg_procs["em"] = {"ZTT","W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    bkg_procs["ttbar"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    
    if(do_embedding){
      bkg_procs["et"] = {"EmbedZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "W", "EWKZ"};
      bkg_procs["mt"] = {"EmbedZTT", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT", "VVJ", "W", "EWKZ"};
      bkg_procs["tt"] = {"EmbedZTT", "W", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT","VVJ", "EWKZ"};
      bkg_procs["em"] = {"EmbedZTT","W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
      bkg_procs["ttbar"] = {"EmbedZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    }

    if(do_jetfakes){
      bkg_procs["et"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};
      bkg_procs["mt"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};
      bkg_procs["tt"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};

      if(do_embedding){
        bkg_procs["et"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
        bkg_procs["mt"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
        bkg_procs["tt"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
      }

    }

    ch::CombineHarvester cb;
    
    map<string,Categories> cats;

    if (!do_mva) {
      if( era.find("2016") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats["et_2016"] = {
            {1, "et_0jet"},
            {2, "et_boosted"}
        };
        
        cats["mt_2016"] = {
            {1, "mt_0jet"},
            {2, "mt_boosted"}
        }; 
        cats["em_2016"] = {
            {1, "em_0jet"},
            {2, "em_boosted"}
        };
        
        cats["tt_2016"] = {
            {1, "tt_0jet"},
            {2, "tt_boosted"}
        };
        
        cats["ttbar_2016"] = {
            {1, "em_ttbar"}
        };
      }
      if( era.find("2017") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats["et_2017"] = {
            {1, "et_0jet"},
            {2, "et_boosted"}
        };

        cats["mt_2017"] = {
            {1, "mt_0jet"},
            {2, "mt_boosted"}
        };
        cats["em_2017"] = {
            {1, "em_0jet"},
            {2, "em_boosted"}
        };

        cats["tt_2017"] = {
            {1, "tt_0jet"},
            {2, "tt_boosted"}
        };

        cats["ttbar_2017"] = {
            {1, "em_ttbar"}
        };
      }
    }
    else {
      cats["et"] = {
          {31, "et_ggh_lowMjj"},
          {32, "et_qqh_lowMjj"},
          {33, "et_zttEmbed_lowMjj"},
          {34, "et_jetFakes_lowMjj"},
          {35, "et_tt_lowMjj"},
          {36, "et_zll_lowMjj"},

          {43, "et_zttEmbed_highMjj"},
          {44, "et_jetFakes_highMjj"},
          {45, "et_tt_highMjj"},
          {46, "et_zll_highMjj"},
      };
      
      cats["mt"] = {
          {31, "mt_ggh_lowMjj"},
          {32, "mt_qqh_lowMjj"},
          {33, "mt_zttEmbed_lowMjj"},
          {34, "mt_jetFakes_lowMjj"},
          {35, "mt_tt_lowMjj"},
          {36, "mt_zll_lowMjj"},

          {43, "mt_zttEmbed_highMjj"},
          {44, "mt_jetFakes_highMjj"},
          {45, "mt_tt_highMjj"},
      }; 
      cats["em"] = {
          {31, "em_ggh_lowMjj"},
          {32, "em_qqh_lowMjj"},
          {33, "em_zttEmbed_lowMjj"},
          {34, "em_qcd_lowMjj"},
          {35, "em_tt_lowMjj"},

          {43, "em_zttEmbed_highMjj"},
          {44, "em_tt_highMjj"},
      };
      
      cats["tt"] = {
          {31, "tt_ggh_lowMjj"},
          {32, "tt_qqh_lowMjj"},
          {33, "tt_zttEmbed_lowMjj"},
          {34, "tt_jetFakes_lowMjj"},

          {43, "tt_zttEmbed_highMjj"},
          {44, "tt_jetFakes_highMjj"},
      };
    }
    
    map<string,Categories> cats_cp;
    
    if (!do_mva) {
      if( era.find("2016") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats_cp["em_2016"] = {
            {3, "em_dijet_loosemjj_lowboost"},
            {4, "em_dijet_loosemjj_boosted"},
            {5, "em_dijet_tightmjj_lowboost"},
            {6, "em_dijet_tightmjj_boosted"}

        };
        
        cats_cp["et_2016"] = {
            {3, "et_dijet_loosemjj_lowboost"},
            {4, "et_dijet_loosemjj_boosted"},       
            {5, "et_dijet_tightmjj_lowboost"},
            {6, "et_dijet_tightmjj_boosted"}

        };
        
        cats_cp["mt_2016"] = {
            {3, "mt_dijet_loosemjj_lowboost"},
            {4, "mt_dijet_loosemjj_boosted"},
            {5, "mt_dijet_tightmjj_lowboost"},
            {6, "mt_dijet_tightmjj_boosted"}
        };    
        
        cats_cp["tt_2016"] = {
            {3, "tt_dijet_loosemjj_lowboost"},
            {4, "tt_dijet_loosemjj_boosted"},
            {5, "tt_dijet_tightmjj_lowboost"},
            {6, "tt_dijet_tightmjj_boosted"} 
        };   
      } 
      if( era.find("2017") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats_cp["em_2017"] = {
            {3, "em_dijet_loosemjj_lowboost"},
            {4, "em_dijet_loosemjj_boosted"},
            {5, "em_dijet_tightmjj_lowboost"},
            {6, "em_dijet_tightmjj_boosted"}

        };

        cats_cp["et_2017"] = {
            {3, "et_dijet_loosemjj_lowboost"},
            {4, "et_dijet_loosemjj_boosted"},
            {5, "et_dijet_tightmjj_lowboost"},
            {6, "et_dijet_tightmjj_boosted"}

        };

        cats_cp["mt_2017"] = {
            {3, "mt_dijet_loosemjj_lowboost"},
            {4, "mt_dijet_loosemjj_boosted"},
            {5, "mt_dijet_tightmjj_lowboost"},
            {6, "mt_dijet_tightmjj_boosted"}
        };

        cats_cp["tt_2017"] = {
            {3, "tt_dijet_loosemjj_lowboost"},
            {4, "tt_dijet_loosemjj_boosted"},
            {5, "tt_dijet_tightmjj_lowboost"},
            {6, "tt_dijet_tightmjj_boosted"}
        };
      }

    }
    else {
      cats_cp["em"] = {
          /* {41, "em_ggh_loose_highMjj"},
          {42, "em_ggh_tight_highMjj"}, */
          
          {41, "em_ggh_highMjj"},
          {42, "em_qqh_highMjj"},
      };
      
      cats_cp["et"] = {
          /* {41, "et_ggh_loose_highMjj"},
          {42, "et_ggh_tight_highMjj"}, */

          {41, "et_ggh_highMjj"},
          {42, "et_qqh_highMjj"},

      };
      
      cats_cp["mt"] = {
          /* {41, "mt_ggh_loose_highMjj"},
          {42, "mt_ggh_tight_highMjj"}, */

          {41, "mt_ggh_highMjj"},
          {42, "mt_qqh_highMjj"},
      };    
      
      cats_cp["tt"] = {
          /* {41, "tt_ggh_loose_highMjj"},
          {42, "tt_ggh_tight_highMjj"}, */

          {41, "tt_ggh_highMjj"},
          {42, "tt_qqh_highMjj"},
      };
    }

    if(do_control_plots) {
      cats_cp["et"] = {};
      cats_cp["mt"] = {};
      cats_cp["tt"] = {};
      cats_cp["em"] = {};
      cats["et"] = {
        {100, "et_pt_1"},
        {101, "et_pt_2"},
        {102, "et_met"},
        {103, "et_pt_tt"},
        {104, "et_m_vis"},
        {105, "et_mjj"},
        {106, "et_sjdphi"},
        {107, "et_njets"}, 
       };
       cats["mt"] = {
        {100, "mt_pt_1"},
        {101, "mt_pt_2"},
        {102, "mt_met"},
        {103, "mt_pt_tt"},
        {104, "mt_m_vis"},
        {105, "mt_mjj"},
        {106, "mt_sjdphi"},  
        {107, "mt_njets"}     
       };
       cats["tt"] = {
        {100, "tt_pt_1"},
        {101, "tt_pt_2"},
        {102, "tt_met"},
        {103, "tt_pt_tt"},
        {104, "tt_m_vis"},
        {105, "tt_mjj"},
        {106, "tt_sjdphi"},  
        {107, "tt_njets"}     
       };
       cats["em"] = {
        {100, "em_pt_1"},
        {101, "em_pt_2"},
        {102, "em_met"},
        {103, "em_pt_tt"},
        {104, "em_m_vis"},
        {105, "em_mjj"},
        {106, "em_sjdphi"},
        {107, "em_njets"}
       }; 
     }
    
    map<string, VString> sig_procs;
    sig_procs["ggH"] = {"ggH_ph_htt"};
    sig_procs["qqH"] = {"qqH_htt125","WH_htt125","ZH_htt125"}; // using JHU samples for qqH
    //sig_procs["qqH_BSM"] = {"qqHmm_htt","qqHps_htt"};
    sig_procs["ggHCP"] = {"ggHsm_htt", "ggHps_htt", "ggHmm_htt"};
    
    vector<string> masses = {"125"};    

    map<const std::string, float> sig_xsec_aachen;
    map<const std::string, float> sig_xsec_IC;
	
    sig_xsec_aachen["ggHsm_htt"] = 0.921684152;      
    sig_xsec_aachen["ggHmm_htt"] = 1.84349344;    
    sig_xsec_aachen["ggHps_htt"] = 0.909898616;    
    sig_xsec_aachen["qqHsm_htt"] = 0.689482928;    
    sig_xsec_aachen["qqHmm_htt"] = 0.12242788;    
    sig_xsec_aachen["qqHps_htt"] = 0.0612201968;

    sig_xsec_IC["ggHsm_htt"] = 0.3987;    
    sig_xsec_IC["ggHmm_htt"] = 0.7893;    
    sig_xsec_IC["ggHps_htt"] = 0.3858;    
    sig_xsec_IC["qqHsm_htt"] = 2.6707;    
    sig_xsec_IC["qqHmm_htt"] = 0.47421;    
    sig_xsec_IC["qqHps_htt"] = 0.2371314;    
    
    using ch::syst::bin_id;
    
    //! [part2]
    for(auto year: years) {
      for (auto chn : chns) {
          cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, cats[chn+"_"+year]);
          cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, cats_cp[chn+"_"+year]);

          cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, bkg_procs[chn], cats[chn+"_"+year], false);
          cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, bkg_procs[chn], cats_cp[chn+"_"+year], false);

          if(chn == "em" || chn == "et" || chn == "mt" || chn == "tt"){
            cb.AddProcesses({"*"},   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH"], cats[chn+"_"+year], false); // SM VBF/VH are added as backgrounds
            cb.AddProcesses({"*"},   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH"], cats_cp[chn+"_"+year], false);

            //cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH_BSM"], cats[chn+"_"+year], true); // Non-SM VBF/VH are added as signal
            //cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH_BSM"], cats_cp[chn+"_"+year], true);

            cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["ggHCP"], cats[chn+"_"+year], true);
            cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["ggHCP"], cats_cp[chn+"_"+year], true);
          }
      }
    } 
    //! [part4]
    
    
    ch::AddSMRun2Systematics(cb, 0, ttbar_fit, no_jec_split);
    
    if(no_shape_systs){
      cb.FilterSysts([&](ch::Systematic *s){
        return s->type().find("shape") != std::string::npos;
      });
    }
    

    if (! only_init.empty()) {
        std::cout << "Write datacards (without shapes) to directory \"" << only_init << "\" and quit." << std::endl;
        ch::CardWriter tmpWriter("$TAG/$ANALYSIS_$ERA_$CHANNEL_$BINID_$MASS.txt", "$TAG/dummy.root");
        tmpWriter.WriteCards(only_init, cb);
        
        return 0;
    }
            
    //! [part7]
    for(auto year: years) {
      for (string chn : chns){
          string channel = chn;
          string extra = "";
          if (year == "2017") extra = "/2017/";
          if(chn == "ttbar") channel = "em"; 
          cb.cp().channel({chn+"_"+year}).backgrounds().ExtractShapes(
                                                             input_dir[chn] + extra + "htt_"+channel+".inputs-sm-13TeV"+postfix+".root",
                                                             "$BIN/$PROCESS",
                                                             "$BIN/$PROCESS_$SYSTEMATIC");
          if(chn == "em" || chn == "et" || chn == "mt" || chn == "tt"){
            //cb.cp().channel({chn+"_"+year}).process(sig_procs["qqH_BSM"]).ExtractShapes(
            //                                                        input_dir[chn]+ extra + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
            //                                                        "$BIN/$PROCESS$MASS",
            //                                                        "$BIN/$PROCESS$MASS_$SYSTEMATIC");
            cb.cp().channel({chn+"_"+year}).process(sig_procs["ggH"]).ExtractShapes(
                                                                    input_dir[chn] + extra +  "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                    "$BIN/$PROCESS$MASS",
                                                                    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
            cb.cp().channel({chn+"_"+year}).process(sig_procs["ggHCP"]).ExtractShapes(
                                                                    input_dir[chn] + extra + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                    "$BIN/$PROCESS$MASS",
                                                                    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
          }
      }
    }    

    // de-correlate systematics for 2016 and 2017
    if((era.find("2016") != std::string::npos && era.find("2017") != std::string::npos) ||  era.find("all") != std::string::npos){
      std::cout << "Partially Decorrelating systematics for 2016/2017" << std::endl;
      Json::Value js;
      string json_file = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/scripts/correlations.json";
      js = ch::ExtractJsonFromFile(json_file);
      std::vector<std::string> keys = js.getMemberNames();
      for (std::vector<std::string>::const_iterator it = keys.begin(); it != keys.end(); ++it){
        string name = *it;
        double value = js[*it].asDouble();
        std::vector<string> chans_2016 = {"em","em_2016","et","et_2016","mt","mt_2016","tt","tt_2016","ttbar","ttbar_2016"};
        std::vector<string> chans_2017 = {"em_2017","et_2017","mt_2017","tt_2017","ttbar_2017"};
        DecorrelateSyst (cb, name, value, chans_2016, chans_2017);
      }
    }
    
    //Now delete processes with 0 yield
    cb.FilterProcs([&](ch::Process *p) {
        bool null_yield = !(p->rate() > 0.);
        if (null_yield){
            std::cout << "[Null yield] Removing process with null yield: \n ";
            std::cout << ch::Process::PrintHeader << *p << "\n";
            cb.FilterSysts([&](ch::Systematic *s){
                bool remove_syst = (MatchingProcess(*p,*s));
                return remove_syst;
            });
        }
        return null_yield;
    });   
    
    
    // And convert any shapes in the ttbar CRs to lnN:
    // Convert all shapes to lnN at this stage

    cb.cp().channel({"ttbar_2016","ttbar_2017"}).syst_type({"shape"}).ForEachSyst([](ch::Systematic *sys) {
        sys->set_type("lnN");
        if(sys->value_d() <0.001) {sys->set_value_d(0.001);};
        if(sys->value_u() <0.001) {sys->set_value_u(0.001);};
    });

    
    std::vector<std::string> all_prefit_bkgs = {
        "QCD","ZL","ZJ","ZTT","TTJ","TTT","TT",
        "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
        "ggH_hww125","qqH_hww125","EWKZ", "qqHsm_htt125", "qqH_htt125", "WH_htt125", "ZH_htt125"};
    
        ////! Option to scale rate
    std::vector< std::string > sig_processes = {"ggHsm_htt125","ggHmm_htt125","ggHps_htt125","qqHsm_htt125","qqHmm_htt125","qqHps_htt125"};
     
    if (!scale_sig_procs.empty()) {	
    	cb.cp().PrintAll();		
        cb.ForEachProc([sig_xsec_IC, sig_xsec_aachen](ch::Process *p) { if (sig_xsec_IC.count(p->process()) ){std::cout << "Scaling " << p->process() << std::endl;  p->set_rate(p->rate() * sig_xsec_IC.at(p->process())/sig_xsec_aachen.at(p->process()) ); };});                 	
    };
    
    if(!real_data){
         for (auto b : cb.cp().bin_set()) {
             std::cout << " - Replacing data with asimov in bin " << b << "\n";
             cb.cp().bin({b}).ForEachObs([&](ch::Observation *obs) {
               obs->set_shape(cb.cp().bin({b}).backgrounds().process(all_prefit_bkgs).GetShape()+cb.cp().bin({b}).signals().process({"ggHsm_htt", "ggH_htt"}).mass({"125"}).GetShape(), true);
               obs->set_rate(cb.cp().bin({b}).backgrounds().process(all_prefit_bkgs).GetRate()+cb.cp().bin({b}).signals().process({"ggHsm_htt", "ggH_htt"}).mass({"125"}).GetRate());
             });
           }
   }    
    
    
    // can auto-merge the bins with bbb uncertainty > 90% - may be better to merge these bins by hand though!
    auto rebin = ch::AutoRebin()
    .SetBinThreshold(0.)
    .SetBinUncertFraction(0.9)
    .SetRebinMode(1)
    .SetPerformRebin(true)
    .SetVerbosity(1);
    if(auto_rebin) rebin.Rebin(cb, cb);
  
  
    // At this point we can fix the negative bins
    std::cout << "Fixing negative bins\n";
    cb.ForEachProc([](ch::Process *p) {
      if (ch::HasNegativeBins(p->shape())) {
         std::cout << "[Negative bins] Fixing negative bins for " << p->bin()
                   << "," << p->process() << "\n";
        auto newhist = p->ClonedShape();
        ch::ZeroNegativeBins(newhist.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        p->set_shape(std::move(newhist), false);
      }
    });
  
    cb.ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos) return;            
      if (ch::HasNegativeBins(s->shape_u()) || ch::HasNegativeBins(s->shape_d())) {
         std::cout << "[Negative bins] Fixing negative bins for syst" << s->bin()
               << "," << s->process() << "," << s->name() << "\n";
        auto newhist_u = s->ClonedShapeU();
        auto newhist_d = s->ClonedShapeD();
        ch::ZeroNegativeBins(newhist_u.get());
        ch::ZeroNegativeBins(newhist_d.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        s->set_shapes(std::move(newhist_u), std::move(newhist_d), nullptr);
      }
  });

  cb.ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos) return;
      if(!(s->value_d()<0.001 || s->value_u()<0.001)) return;
      std::cout << "[Negative yield] Fixing negative yield for syst" << s->bin()
               << "," << s->process() << "," << s->name() << "\n";
      if(s->value_u()<0.001){
         s->set_value_u(0.001);
         s->set_type("lnN");
      }
      if(s->value_d()<0.001){
         s->set_value_d(0.001);
         s->set_type("lnN");
      }
  });

    // set b-tag uncertainties to lnN
    cb.cp().ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos || s->type().find("CMS_eff_b") == std::string::npos) return;
         s->set_type("lnN");
    });
    
    ////! [part8]
    // add bbb uncertainties for all backgrounds
    auto bbb = ch::BinByBinFactory()
    .SetPattern("CMS_$ANALYSIS_$CHANNEL_$BIN_$ERA_$PROCESS_bin_$#")
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.4)
    .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);

    // add bbb uncertainties for the signal but only if uncertainties are > 5% and only for categories with significant amount of signal events to reduce the total number of bbb uncertainties
   // auto bbb_sig = ch::BinByBinFactory()
   // .SetPattern("CMS_$ANALYSIS_$CHANNEL_$BIN_$ERA_$PROCESS_bin_$#")
   // .SetAddThreshold(0.05)
   // .SetMergeThreshold(0.0)
   // .SetFixNorm(false);
   // bbb_sig.AddBinByBin(cb.cp().signals().process({"qqHmm_htt","qqHps_htt","WHmm_htt","WHps_htt","ZHmm_htt","ZHps_htt"},false).bin_id({1,2,3,4,5,6,31,32,41,42}),cb); 

    
    //// rename embedded energy-scale uncertainties so that they are not correlated with MC energy-scales
    //cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_e_13TeV","CMS_scale_embedded_e_13TeV"); 
    //cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_1prong_13TeV","CMS_scale_embedded_t_1prong_13TeV");
    //cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_1prong1pizero_13TeV","CMS_scale_embedded_t_1prong1pizero_13TeV");
    //cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_3prong_13TeV","CMS_scale_embedded_t_3prong_13TeV");

 
    // This function modifies every entry to have a standardised bin name of
    // the form: {analysis}_{channel}_{bin_id}_{era}
    // which is commonly used in the htt analyses
    ch::SetStandardBinNames(cb);
    //! [part8]
    

    //! [part9]
    // First we generate a set of bin names:
    

    //Write out datacards. Naming convention important for rest of workflow. We
    //make one directory per chn-cat, one per chn and cmb. In this code we only
    //store the individual datacards for each directory to be combined later, but
    //note that it's also possible to write out the full combined card with CH
    string output_prefix = "output/";
    if(output_folder.compare(0,1,"/") == 0) output_prefix="";
    ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
		    output_prefix + output_folder + "/$TAG/common/htt_input.root");
    
    
    writer.WriteCards("cmb", cb);
    //Add all di-jet categories combined
    writer.WriteCards("htt_dijet", cb.cp().bin_id({3,4,5,6}));
    for (auto chn : cb.channel_set()) {

        // per-channel
	    writer.WriteCards(chn, cb.cp().channel({chn}));
        // And per-channel-category
        if (!do_mva) {
          writer.WriteCards("htt_"+chn+"_1_13TeV", cb.cp().channel({chn}).bin_id({1}));
          writer.WriteCards("htt_"+chn+"_2_13TeV", cb.cp().channel({chn}).bin_id({2}));
	  writer.WriteCards("htt_"+chn+"_3_13TeV", cb.cp().channel({chn}).bin_id({3}));
	  writer.WriteCards("htt_"+chn+"_4_13TeV", cb.cp().channel({chn}).bin_id({4}));
          writer.WriteCards("htt_"+chn+"_5_13TeV", cb.cp().channel({chn}).bin_id({5}));
          writer.WriteCards("htt_"+chn+"_6_13TeV", cb.cp().channel({chn}).bin_id({6}));
	}
        else {
          writer.WriteCards("htt_"+chn+"_31_13TeV", cb.cp().channel({chn}).bin_id({31}));
          writer.WriteCards("htt_"+chn+"_32_13TeV", cb.cp().channel({chn}).bin_id({32}));
          writer.WriteCards("htt_"+chn+"_33_13TeV", cb.cp().channel({chn}).bin_id({33}));
          writer.WriteCards("htt_"+chn+"_34_13TeV", cb.cp().channel({chn}).bin_id({34}));
          writer.WriteCards("htt_"+chn+"_35_13TeV", cb.cp().channel({chn}).bin_id({35}));
          writer.WriteCards("htt_"+chn+"_36_13TeV", cb.cp().channel({chn}).bin_id({36}));
          writer.WriteCards("htt_"+chn+"_37_13TeV", cb.cp().channel({chn}).bin_id({37}));
          writer.WriteCards("htt_"+chn+"_38_13TeV", cb.cp().channel({chn}).bin_id({38}));
          writer.WriteCards("htt_"+chn+"_39_13TeV", cb.cp().channel({chn}).bin_id({39}));
          writer.WriteCards("htt_"+chn+"_41_13TeV", cb.cp().channel({chn}).bin_id({41}));
          writer.WriteCards("htt_"+chn+"_42_13TeV", cb.cp().channel({chn}).bin_id({42}));
          writer.WriteCards("htt_"+chn+"_43_13TeV", cb.cp().channel({chn}).bin_id({43}));
          writer.WriteCards("htt_"+chn+"_44_13TeV", cb.cp().channel({chn}).bin_id({44}));
          writer.WriteCards("htt_"+chn+"_45_13TeV", cb.cp().channel({chn}).bin_id({45}));
          writer.WriteCards("htt_"+chn+"_46_13TeV", cb.cp().channel({chn}).bin_id({46}));
          writer.WriteCards("htt_"+chn+"_47_13TeV", cb.cp().channel({chn}).bin_id({47}));
          writer.WriteCards("htt_"+chn+"_48_13TeV", cb.cp().channel({chn}).bin_id({48}));
          writer.WriteCards("htt_"+chn+"_49_13TeV", cb.cp().channel({chn}).bin_id({49}));
          writer.WriteCards("htt_"+chn+"_lowMjj_13TeV", cb.cp().channel({chn}).bin_id({31,32,33,34,35,36,37,38,39}));
          writer.WriteCards("htt_"+chn+"_highMjj_13TeV", cb.cp().channel({chn}).bin_id({41,42,43,44,45,46,47,48,49}));
        }
        
        
    }
    
    writer.WriteCards("htt_cmb_bkgs_13TeV", cb.cp().bin_id({33,34,35,36,37,38,39,43,44,45}));
    writer.WriteCards("htt_cmb_highMjj_13TeV", cb.cp().bin_id({41,42,43,44,45,46,47}));
    
    cb.PrintAll();
    cout << " done\n";
    
    
}
