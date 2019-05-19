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
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombineTools/interface/JsonTools.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "TF1.h"

using namespace std;
using ch::JoinStr;
using ch::syst::SystMap;
using ch::syst::SystMapAsymm;
using ch::syst::era;
using ch::syst::channel;
using ch::syst::bin_id;
using ch::syst::process;
using ch::syst::bin;
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

bool BinIsControlRegion(ch::Object const* obj)
{
    return (boost::regex_search(obj->bin(),boost::regex{"_cr$"}) || (obj->channel() == std::string("mm")));
}

// Useful to have the inverse sometimes too
bool BinIsNotControlRegion(ch::Object const* obj)
{
    return !BinIsControlRegion(obj);
}


int main(int argc, char** argv) {

    string output_folder = "sm_run2";
    string input_folder_mt="Imperial/TauID2017/";
    string input_folder_et="Imperial/TauID/";
    string postfix="-2D";
    bool useMC = false;
    bool fitEff = false;
    bool ff_fracs = false;
    int mode = 0; //mode = 0 is for ID measurments, mode = 1 is for trigger measurments
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
    ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("Imperial/TauID2017"))
    ("input_folder_et", po::value<string>(&input_folder_et)->default_value("Imperial/TauID"))
    ("postfix", po::value<string>(&postfix)->default_value(postfix))
    ("mode", po::value<int>(&mode)->default_value(mode))
    ("useMC", po::value<bool>(&useMC)->default_value(false))
    ("fitEff", po::value<bool>(&fitEff)->default_value(false))
    ("ff_fracs", po::value<bool>(&ff_fracs)->default_value(false))
    ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"));

    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);
    
    
    typedef vector<string> VString;
    typedef vector<pair<int, string>> Categories;
    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    //    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/AllROOT_20fb/";
    std::map<string, string> input_dir;
    if(ff_fracs) input_folder_mt = "Imperial/FFFracs";
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";  
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";
    input_dir["tt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";
    
    
    VString chns = {"mt"};
    if(ff_fracs) chns = {"mt","et","tt"};
    
    map<string, VString> bkg_procs;
    VString sig_procs;
    
    if(ff_fracs) {
      bkg_procs["mt"] = {"QCD","W","ZJ","TTJ","VVJ"};
      bkg_procs["et"] = {"QCD","W","ZJ","TTJ","VVJ"};    
      bkg_procs["tt"] = {"QCD","W","ZJ","TTJ","VVJ"};
      sig_procs = {"ZTT","ZL","TTT","VVT","EWKZ"};
    }
    else if(!useMC){
       bkg_procs["mt"] = {"QCD","W","ZL","ZJ","TTT","TTJ","VVT","VVJ"};
       bkg_procs["et"] = {"QCD","W","ZL","ZJ","TTT","TTJ","VVT","VVJ"};
    } else {
      bkg_procs["mt"] = {"QCD","W","ZL","ZJ","TTJ","VVJ"};
      bkg_procs["et"] = {"QCD","W","ZL","ZJ","TTJ","VVJ"};
    }
    if(!(useMC || fitEff) && !ff_fracs) sig_procs = {"EmbedZTT_pass","EmbedZTT_fail"};
    if(useMC && !ff_fracs)sig_procs = {"ZTTpass","ZTTfail","TTTpass","TTTfail","VVTpass","VVTfail"};    
    if(fitEff && !useMC && !ff_fracs) sig_procs = {"EmbedZTT_pass","EmbedZTT_fail","TTTpass","TTTfail","VVTpass","VVTfail"};

    ch::CombineHarvester cb;
    
    map<string,Categories> cats;
    
    if(ff_fracs){
      cats["mt"] = {
          {1, "mt_0jet"},
          {2, "mt_0jet"},
          {3, "mt_boosted_low"},
          {4, "mt_boosted_high"},
          {5, "mt_dijet_lowboost"},
          {6, "mt_dijet_boosted"},
          {7, "mt_btag"}
      };
      cats["et"] = {
          {1, "et_0jet"},
          {2, "et_0jet"},
          {3, "et_boosted_low"},
          {4, "et_boosted_high"},
          {5, "et_dijet_lowboost"},
          {6, "et_dijet_boosted"},
          {7, "et_btag"}
      };
      cats["tt"] = {
          {1, "tt_inclusive_1"},
          {2, "tt_0jet_1"},
          {3, "tt_boosted_low_1"},
          {4, "tt_boosted_high_1"},
          {5, "tt_dijet_lowboost_1"},
          {6, "tt_dijet_boosted_1"},
          {7, "tt_inclusive_2"},
          {8, "tt_0jet_2"},
          {9, "tt_boosted_low_2"},
          {10, "tt_boosted_high_2"},
          {11, "tt_dijet_lowboost_2"},
          {12, "tt_dijet_boosted_2"}
      };
    } else { 
      cats["mt"] = {
          {1, "mt_pass"},
          {2, "mt_fail"}
      }; 
      cats["et"] = {
          {1, "et_pass"},
          {2, "et_fail"}
      }; 
    }
    
    using ch::syst::bin_id;
    
    //! [part2]
    for (auto chn : chns) {
        cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn]);
        cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn], false);
        cb.AddProcesses(   {"*"},   {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
    }

    std::vector<std::string> embed = {"EmbedZTT_pass","EmbedZTT_fail"};
    std::vector<std::string> real_tau = {"TTT","VVT","TTTpass","TTTfail","VVTpass","VVTfail","ZTT", "EWKZ"};
    std::vector<std::string> jetfake = {"W","VVJ","TTJ","ZJ"};
    std::vector<std::string> jetfake_noW = {"VVJ","TTJ","ZJ"};
    std::vector<std::string> zl = {"ZL"};
    
    // Add all systematics here
    
    cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
    
    cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));

    
    cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mt"}, JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}}),  1.02));
    cb.cp().AddSyst(cb, "CMS_eff_embedded_m", "lnN", SystMap<channel, process>::init
                        ({"mt"}, embed,  1.02));
    cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"},embed}),  1.02));   
    cb.cp().AddSyst(cb, "CMS_embed_norm_13TeV", "lnN", SystMap<channel, process>::init
                        ({"mt"}, embed,  1.04));
   
 
    //##############################################################################
    //  trigger   
    //##############################################################################
    
    cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}})).channel({"mt"}).AddSyst(cb,
                                         "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
    cb.cp().process(embed).channel({"mt"}).AddSyst(cb,
                                         "CMS_eff_embedded_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
    
    cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"},embed})).channel({"et"}).AddSyst(cb,
                                         "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));

    cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"},embed})).channel({"tt"}).AddSyst(cb,
                                        "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.10));

    // btag efficiencies
    //cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}})).channel({"et","mt"}).AddSyst(cb,
    //                                           "CMS_fake_b_$ERA", "shape", SystMap<>::init(1.00));
    //cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}})).channel({"et","mt"}).AddSyst(cb,
    //                                           "CMS_eff_b_$ERA", "shape", SystMap<>::init(1.00));
    
    if(mode==0 && !ff_fracs){
        // id uncertainties for j->tau and l->tau will be added in physics model
        cb.cp().process(jetfake).bin_id({1,3,5,7,9,11,13,15,17,19}).AddSyst(cb,
                                               "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));
        if(!(useMC||fitEff)) cb.cp().process(real_tau).bin_id({1,3,5,7,9,11,13,15,17,19}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.1));
        cb.cp().process(jetfake_noW).bin_id({1,3,5,7,9,11,13,15,17,19}).AddSyst(cb,
                                                        "CMS_htt_jFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        cb.cp().process(zl).channel({"mt"}).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
        cb.cp().process(zl).channel({"et"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.10));
    }
    if(mode==1 || ff_fracs){
      cb.cp().process(JoinStr({real_tau,embed})).channel({"mt","et"}).AddSyst(cb,
                                               "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.07));
      cb.cp().process(JoinStr({real_tau,embed})).channel({"mt","et"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
      
      cb.cp().process(JoinStr({real_tau,embed})).channel({"tt"}).AddSyst(cb,
                                               "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.145));
      cb.cp().process(JoinStr({real_tau,embed})).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.04));
      
      cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.07));
        
      cb.cp().process({"TTJ","ZJ","VVJ","W"}).channel({"tt"}).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
      
      cb.cp().process(jetfake).AddSyst(cb,
                                               "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));  
      cb.cp().process({"VVJ","TTJ","ZJ"}).AddSyst(cb,
                                                        "CMS_htt_jFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
      cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                                        "CMS_htt_jFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
      cb.cp().process(zl).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
      cb.cp().process(zl).channel({"et"}).AddSyst(cb,
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.10));
      cb.cp().process(zl).channel({"tt"}).AddSyst(cb,
                                                        "CMS_htt_lFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
    }
    
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.0));
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.0));
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.0));
    

    //cb.cp().process(embed).channel({"mt"}).AddSyst(cb,
    //                                             "CMS_scale_m_$ERA", "shape", SystMap<>::init(1.00));
    //
    //cb.cp().process(embed).channel({"et"}).AddSyst(cb,
    //                                             "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));
    

    //cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
    //                                              "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,"CMS_scale_j_$ERA", "shape", SystMap<>::init(1.00));
    //cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,"CMS_scale_j_eta0to3_$ERA", "shape", SystMap<>::init(1.00));
    //cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,"CMS_scale_j_eta3to5_$ERA", "shape", SystMap<>::init(1.00)); 
    //cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,"CMS_scale_j_RelativeBal_$ERA", "shape", SystMap<>::init(1.00));

    cb.cp().process(zl).channel({"et","mt"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(zl).channel({"et","mt"}).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process({"VVT","VVJ","VVTpass","VVTfail"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
    
    cb.cp().process({"TTT","TTJ","TTTpass","TTTfail"}).AddSyst(cb,
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));


    cb.cp().process({"ZTT","ZTTpass","ZTTfail","ZL","ZJ"}).AddSyst(cb,
                                                       "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
    
    cb.cp().process({"W"}).channel({"tt"}).AddSyst(cb,
                                                   "CMS_htt_wjXsec_13TeV", "lnN", SystMap<>::init(1.04));

    cb.cp().process({"ZTT","ZTTpass","ZTTfail","ZJ","ZL"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"TTJ","TTT","TTTpass","TTTfail"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
    
    if(!ff_fracs){
      cb.cp().process({"QCD"}).AddSyst(cb,
                                             "CMS_QCD_OSSS_$CHANNEL_$BIN_$ERA", "lnN", SystMap<>::init(1.10));
    
      cb.cp().process({"W"}).AddSyst(cb,
                                                   "CMS_htt_W_Extrap_$CHANNEL_$BIN_13TeV", "lnN", SystMap<>::init(1.10));    
    } else {
    
      cb.cp().process({"QCD"}).channel({"et"}).bin_id({1,2}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_0JET_$ERA", "lnN", SystMap<>::init(1.21));
      cb.cp().process({"QCD"}).channel({"et"}).bin_id({3,4}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_BOOSTED_$ERA", "lnN", SystMap<>::init(1.33));
      cb.cp().process({"QCD"}).channel({"et"}).bin_id({5,6}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_DIJET_$ERA", "lnN", SystMap<>::init(1.48));
      cb.cp().process({"QCD"}).channel({"et"}).bin_id({7}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_BTAG_$ERA", "lnN", SystMap<>::init(1.27));
      cb.cp().process({"QCD"}).channel({"mt"}).bin_id({1,2}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_0JET_$ERA", "lnN", SystMap<>::init(1.1));
      cb.cp().process({"QCD"}).channel({"mt"}).bin_id({3,4}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_BOOSTED_$ERA", "lnN", SystMap<>::init(1.1));
      cb.cp().process({"QCD"}).channel({"mt"}).bin_id({5,6}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_DIJET_$ERA", "lnN", SystMap<>::init(1.1));
      cb.cp().process({"QCD"}).channel({"mt"}).bin_id({7}).AddSyst(cb,
                                               "CMS_QCD_OSSS_$CHANNEL_BTAG_$ERA", "lnN", SystMap<>::init(1.32));
      
      
      // based on the Ersatz study
      cb.cp().process({"W"}).channel({"et","mt"}).bin_id({1,2}).AddSyst(cb,
                                           "WHighMTtoLowMT_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.033));
      cb.cp().process({"W"}).channel({"et","mt"}).bin_id({3,4}).AddSyst(cb,
                                           "WHighMTtoLowMT_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.067));
      cb.cp().process({"W"}).channel({"et","mt"}).bin_id({5,6}).AddSyst(cb,
                                           "WHighMTtoLowMT_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.182));
      cb.cp().process({"W"}).channel({"et","mt"}).bin_id({5,6}).AddSyst(cb,
                                           "WlowPTtoHighPT_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.279));
      cb.cp().process({"W"}).channel({"et","mt"}).bin_id({5,6}).AddSyst(cb,
                                           "WHighMTtoLowMT_btag_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.2));
      
      // W OS/SS systematic uncertainties 
      cb.cp().process({"W"}).channel({"et"}).bin_id({1,2}).AddSyst(cb,
                                           "WOSSS_syst_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.002));
      cb.cp().process({"W"}).channel({"et"}).bin_id({3,4}).AddSyst(cb,
                                           "WOSSS_syst_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.029));
      cb.cp().process({"W"}).channel({"et"}).bin_id({5,6}).AddSyst(cb,
                                           "WOSSS_syst_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.131));
      cb.cp().process({"W"}).channel({"2t"}).bin_id({7}).AddSyst(cb,
                                           "WOSSS_syst_btag_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.019));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({1,2}).AddSyst(cb,
                                           "WOSSS_syst_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.012));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({3,4}).AddSyst(cb,
                                           "WOSSS_syst_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.049));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({5,6}).AddSyst(cb,
                                           "WOSSS_syst_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.086));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({7}).AddSyst(cb,
                                           "WOSSS_syst_btag_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.024));
      
      // W OS/SS statistical uncertainties
      cb.cp().process({"W"}).channel({"et"}).bin_id({1,2}).AddSyst(cb,
                                           "WOSSS_stat_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.035));
      cb.cp().process({"W"}).channel({"et"}).bin_id({3,4}).AddSyst(cb,
                                           "WOSSS_stat_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.026));
      cb.cp().process({"W"}).channel({"et"}).bin_id({5,6}).AddSyst(cb,
                                           "WOSSS_stat_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.082));
      cb.cp().process({"W"}).channel({"et"}).bin_id({7}).AddSyst(cb,
                                           "WOSSS_stat_btag_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.029));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({1,2}).AddSyst(cb,
                                           "WOSSS_stat_0jet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.026));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({3,4}).AddSyst(cb,
                                           "WOSSS_stat_boosted_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.020));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({5,6}).AddSyst(cb,
                                           "WOSSS_stat_dijet_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.066));
      cb.cp().process({"W"}).channel({"mt"}).bin_id({7}).AddSyst(cb,
                                           "WOSSS_stat_btag_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.022));
      
    }  
    
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({1,2}).AddSyst(cb,
                                         "CMS_htt_QCD_0jet_1_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.02));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({3,4}).AddSyst(cb,
                                         "CMS_htt_QCD_boosted_1_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.04));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({5}).AddSyst(cb,
                                         "CMS_htt_QCD_dijet_lowboost_1_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.08));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({6}).AddSyst(cb,
                                         "CMS_htt_QCD_dijet_boosted_1_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.48));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({7,8}).AddSyst(cb,
                                         "CMS_htt_QCD_0jet_2_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.02));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({9,10}).AddSyst(cb,
                                         "CMS_htt_QCD_boosted_2_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.04));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({11}).AddSyst(cb,
                                         "CMS_htt_QCD_dijet_lowboost_2_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.08));
    cb.cp().process({"QCD"}).channel({"tt"}).bin_id({12}).AddSyst(cb,
                                         "CMS_htt_QCD_dijet_boosted_2_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.48));
    
            
    //! [part7]
    for (string chn : cb.channel_set()){
        string channel = chn;
        if(chn == "ttbar") channel = "em"; 
        cb.cp().channel({chn}).backgrounds().ExtractShapes(
                                                           input_dir[chn] + "htt_"+channel+".inputs-sm-13TeV"+postfix+".root",
                                                           "$BIN/$PROCESS",
                                                           "$BIN/$PROCESS_$SYSTEMATIC");
        cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
                                                                  input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                  "$BIN/$PROCESS",
                                                                  "$BIN/$PROCESS_$SYSTEMATIC");

    }
    

    vector<string> es_uncerts = {
      "t_1prong_13TeV",
      "t_1prong1pizero_13TeV",
      "t_3prong_13TeV",
    };
    for (auto name : es_uncerts) {
      auto cb_syst = cb.cp().syst_name({"CMS_scale_"+name});
      ch::CloneSysts(cb.cp().process({"EmbedZTT"}).syst_name({"CMS_scale_"+name}), cb, [&](ch::Systematic *s) {
        s->set_name("CMS_scale_embedded_"+name);
        if (s->type().find("shape") != std::string::npos) {
          s->set_scale(s->scale() * 0.707);
        }
      });

      ch::CloneSysts(cb.cp().process({"EmbedZTT"},false).syst_name({"CMS_scale_"+name}), cb, [&](ch::Systematic *s) {
        s->set_name("CMS_scale_mc_"+name);
        if (s->type().find("shape") != std::string::npos) {
          s->set_scale(s->scale() * 0.707);
        }
      });

      cb_syst.ForEachSyst([](ch::Systematic *syst) {
        if (syst->type().find("shape") != std::string::npos) {
          syst->set_scale(syst->scale() * 0.707);
        }
      });

    }


    
    //Now delete processes with 0 yield
    cb.FilterProcs([&](ch::Process *p) {
        bool null_yield = !(p->rate() > 0. || BinIsControlRegion(p));
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
        
  
  
    // At this point we can fix the negative bins
    std::cout << "Fixing negative bins\n";
    cb.ForEachProc([](ch::Process *p) {
      if (ch::HasNegativeBins(p->shape())) {
         std::cout << "[Negative bins] Fixing negative bins for " << p->bin()
                   << "," << p->process() << "\n";
         std::cout << "[Negative bins] Before:\n";
         p->shape()->Print("range");
        auto newhist = p->ClonedShape();
        ch::ZeroNegativeBins(newhist.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        p->set_shape(std::move(newhist), false);
         std::cout << "[Negative bins] After:\n";
         p->shape()->Print("range");
      }
    });
  
    cb.ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos) return;            
      if (ch::HasNegativeBins(s->shape_u()) || ch::HasNegativeBins(s->shape_d())) {
         std::cout << "[Negative bins] Fixing negative bins for syst" << s->bin()
               << "," << s->process() << "," << s->name() << "\n";
         std::cout << "[Negative bins] Before:\n";
         s->shape_u()->Print("range");
         s->shape_d()->Print("range");
        auto newhist_u = s->ClonedShapeU();
        auto newhist_d = s->ClonedShapeD();
        ch::ZeroNegativeBins(newhist_u.get());
        ch::ZeroNegativeBins(newhist_d.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        s->set_shapes(std::move(newhist_u), std::move(newhist_d), nullptr);
         std::cout << "[Negative bins] After:\n";
         s->shape_u()->Print("range");
         s->shape_d()->Print("range");
      }
  });
      
    
    ////! [part8]
    auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.)
    .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
    
    auto bbb_sig = ch::BinByBinFactory()
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.4)
    .SetFixNorm(false);
    bbb_sig.AddBinByBin(cb.cp().signals(), cb); 

    ch::SetStandardBinNames(cb);
    
    string output_prefix = "output/";
    if(output_folder.compare(0,1,"/") == 0) output_prefix="";
    ch::CardWriter writer(output_prefix + output_folder + "/$TAG/125/$BIN.txt",
                          output_prefix + output_folder + "/$TAG/common/htt_input.root");
    // We're not using mass as an identifier - which we need to tell the CardWriter
    // otherwise it will see "*" as the mass value for every object and skip it
    writer.SetWildcardMasses({});
    writer.SetVerbosity(1);
    if(!ff_fracs){
      writer.WriteCards("mt_pass", cb.cp().channel({"mt"}).bin_id({1}));     
      writer.WriteCards("mt_fail", cb.cp().channel({"mt"}).bin_id({2}));
      writer.WriteCards("mt_combined", cb.cp().channel({"mt"}).bin_id({1,2}));
      
      writer.WriteCards("et_pass", cb.cp().channel({"et"}).bin_id({1}));
      writer.WriteCards("et_fail", cb.cp().channel({"et"}).bin_id({2}));
      writer.WriteCards("et_combined", cb.cp().channel({"et"}).bin_id({1,2}));
      writer.WriteCards("combined", cb.cp().channel({"et","mt"}).bin_id({1,2}));
    } else {
      for (auto chn : chns) {   
        if(chn != "tt"){  
          writer.WriteCards(chn+"_inclusive", cb.cp().channel({chn}).bin_id({1}));     
          writer.WriteCards(chn+"_0jet", cb.cp().channel({chn}).bin_id({2}));
          writer.WriteCards(chn+"_boosted_low", cb.cp().channel({chn}).bin_id({3}));
          writer.WriteCards(chn+"_boosted_hi", cb.cp().channel({chn}).bin_id({4}));
          writer.WriteCards(chn+"_dijet_lowboost", cb.cp().channel({chn}).bin_id({5}));
          writer.WriteCards(chn+"_dijet_boosted", cb.cp().channel({chn}).bin_id({6}));
          writer.WriteCards(chn+"_btag", cb.cp().channel({chn}).bin_id({7}));
          writer.WriteCards(chn+"_combined", cb.cp().channel({chn}).bin_id({2,3,4,5,6,7}));
        } else {
          writer.WriteCards(chn+"_inclusive", cb.cp().channel({chn}).bin_id({1,7}));     
          writer.WriteCards(chn+"_0jet", cb.cp().channel({chn}).bin_id({2,8}));
          writer.WriteCards(chn+"_boosted_low", cb.cp().channel({chn}).bin_id({3,9}));
          writer.WriteCards(chn+"_boosted_hi", cb.cp().channel({chn}).bin_id({4,10}));
          writer.WriteCards(chn+"_dijet_lowboost", cb.cp().channel({chn}).bin_id({5,11}));
          writer.WriteCards(chn+"_dijet_boosted", cb.cp().channel({chn}).bin_id({6,12}));
          writer.WriteCards(chn+"_combined", cb.cp().channel({chn}).bin_id({2,3,4,5,6,8,9,10,11,12}));
        }
      }
  
    }

    cb.PrintAll();
    cout << " done\n";
    
    
}
