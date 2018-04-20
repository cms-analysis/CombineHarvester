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
    string input_folder_mt="Imperial/TauID/";
    string input_folder_et="Imperial/TauID/";
    string postfix="";
    bool useMC = false;
    bool fitEff = false;
    bool embed_yield_from_data = false;
    int mode = 0; //mode = 0 is for ID measurments, mode = 1 is for trigger measurments
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
    ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("Imperial/TauID"))
    ("input_folder_et", po::value<string>(&input_folder_et)->default_value("Imperial/TauID"))
    ("postfix", po::value<string>(&postfix)->default_value(postfix))
    ("mode", po::value<int>(&mode)->default_value(mode))
    ("useMC", po::value<bool>(&useMC)->default_value(false))
    ("fitEff", po::value<bool>(&fitEff)->default_value(false))
    ("embed_yield_from_data", po::value<bool>(&embed_yield_from_data)->default_value(false))
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
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";  
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";
    
    
    VString chns = {"mt","et"};
    
    map<string, VString> bkg_procs;
    VString sig_procs;

    if(!useMC){
       bkg_procs["mt"] = {"QCD","W","ZL","ZJ","TTT","TTJ","VVT","VVJ"};
       bkg_procs["et"] = {"QCD","W","ZL","ZJ","TTT","TTJ","VVT","VVJ"};
    } else {
      bkg_procs["mt"] = {"QCD","W","ZL","ZJ","TTJ","VVJ"};
      bkg_procs["et"] = {"QCD","W","ZL","ZJ","TTJ","VVJ"};
    }
    if(!(useMC || fitEff)) sig_procs = {"EmbedZTTpass","EmbedZTTfail"};
    if(useMC)sig_procs = {"ZTTpass","ZTTfail","TTTpass","TTTfail","VVTpass","VVTfail"};    
    if(fitEff && !useMC) sig_procs = {"EmbedZTTpass","EmbedZTTfail","TTTpass","TTTfail","VVTpass","VVTfail"};

    ch::CombineHarvester cb;
    
    map<string,Categories> cats;
    
    cats["mt"] = {
        {1, "mt_pass"},
        {2, "mt_fail"}
    }; 
    cats["et"] = {
        {1, "et_pass"},
        {2, "et_fail"}
    }; 
    
    using ch::syst::bin_id;
    
    //! [part2]
    for (auto chn : chns) {
        cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn]);
        cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn], false);
        cb.AddProcesses(   {"*"},   {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
    }

    std::vector<std::string> embed = {"EmbedZTTpass","EmbedZTTfail"};
    std::vector<std::string> real_tau = {"TTT","VVT","TTTpass","TTTfail","VVTpass","VVTfail"};
    std::vector<std::string> jetfake = {"W","VVJ","TTJ","ZJ"};
    std::vector<std::string> jetfake_noW = {"VVJ","TTJ","ZJ"};
    std::vector<std::string> zl = {"ZL"};
    
    // Add all systematics here
    
    cb.cp().process(JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));
    if(!embed_yield_from_data) {
      cb.cp().process({"EmbedZTT","EmbedZTTpass","EmbedZTTfail"}).AddSyst(cb,
                                            "lumi_13TeV", "lnN", SystMap<>::init(1.025));    
    }

    
    cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init
                        ({"mt"}, JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"}}),  1.02));
    cb.cp().AddSyst(cb, "CMS_eff_e", "lnN", SystMap<channel, process>::init
                        ({"et"}, JoinStr({real_tau,jetfake_noW,zl,{"ZTT","ZTTpass","ZTTfail"},embed}),  1.02));   
 
    if(embed_yield_from_data) {
      cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init  
                          ({"mt"}, embed,  0.98)
                          ({"et"}, embed,  0.96)
                          );    
    } else {
      cb.cp().AddSyst(cb, "CMS_eff_m", "lnN", SystMap<channel, process>::init  
                          ({"mt"}, embed,  1.02));    
    }
    //cb.cp().AddSyst(cb, "CMS_embed_norm_13TeV", "lnN", SystMap<channel, process>::init
    //                    ({"mt"}, embed,  1.02));
    
    if(mode==0){
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
                                                        "CMS_htt_eFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
    }
    if(mode==1){
      cb.cp().process(JoinStr({real_tau,embed})).AddSyst(cb,
                                               "CMS_eff_t_$ERA", "lnN", SystMap<>::init(1.05));
      cb.cp().process(JoinStr({real_tau,embed})).AddSyst(cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.02));
      cb.cp().process(jetfake).AddSyst(cb,
                                               "CMS_htt_jetToTauFake_$ERA", "shape", SystMap<>::init(1.00));  
      cb.cp().process(jetfake).AddSyst(cb,
                                                        "CMS_htt_jFakeTau_13TeV", "lnN", SystMap<>::init(1.20));
      cb.cp().process(zl).AddSyst(cb,
                                                        "CMS_htt_mFakeTau_13TeV", "lnN", SystMap<>::init(1.20));    
    }
    
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({real_tau,embed,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                            "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process(embed).channel({"mt"}).AddSyst(cb,
                                                 "CMS_scale_m_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process(embed).channel({"et"}).AddSyst(cb,
                                                 "CMS_scale_e_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                                  "CMS_scale_met_clustered_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({real_tau,jetfake,zl,{"ZTT","ZTTpass","ZTTfail"}})).AddSyst(cb,
                                                  "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process(zl).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(zl).AddSyst(cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process({"VVT","VVJ","VVTpass","VVTfail"}).AddSyst(cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", SystMap<>::init(1.05));
    
    cb.cp().process({"TTT","TTJ","TTTpass","TTTfail"}).AddSyst(cb,
					  "CMS_htt_tjXsec_13TeV", "lnN", SystMap<>::init(1.06));
    
    cb.cp().process({"W"}).bin_id({1,3,5,7,9,11,13,15,17,19}).AddSyst(cb,
                                                   "CMS_htt_W_Extrap_pass_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.1));

    cb.cp().process({"W"}).bin_id({2,4,6,8,10,12,14,16,18,20}).AddSyst(cb,
                                                   "CMS_htt_W_Extrap_fail_$CHANNEL_13TeV", "lnN", SystMap<>::init(1.05));
    
    cb.cp().process({"ZTT","ZTTpass","ZTTfail","ZL","ZJ"}).AddSyst(cb,
                                                       "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
    if(!embed_yield_from_data){
      cb.cp().process({"EmbedZTT","EmbedZTTpass","EmbedZTTfail"}).AddSyst(cb,
                                                       "CMS_htt_zjXsec_13TeV", "lnN", SystMap<>::init(1.04));
    }

    
    cb.cp().process({"ZTT","ZTTpass","ZTTfail","ZJ","ZL"}).AddSyst(cb,
                                             "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"TTJ","TTT","TTTpass","TTTfail"}).AddSyst(cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process({"QCD"}).bin_id({1,3,5,7,9,11,13,15,17,19}).AddSyst(cb,
                                             "CMS_QCD_OSSS_pass_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.05));
    cb.cp().process({"QCD"}).bin_id({2,4,6,8,10,12,14,16,18,20}).AddSyst(cb,
                                             "CMS_QCD_OSSS_fail_$CHANNEL_$ERA", "lnN", SystMap<>::init(1.05));


            
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
    .SetMergeThreshold(0.4)
    .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);

    ch::SetStandardBinNames(cb);
    
    string output_prefix = "output/";
    if(output_folder.compare(0,1,"/") == 0) output_prefix="";
    ch::CardWriter writer(output_prefix + output_folder + "/$TAG/125/$BIN.txt",
                          output_prefix + output_folder + "/$TAG/common/htt_input.root");
    // We're not using mass as an identifier - which we need to tell the CardWriter
    // otherwise it will see "*" as the mass value for every object and skip it
    writer.SetWildcardMasses({});
    writer.SetVerbosity(1);
    writer.WriteCards("mt_pass", cb.cp().channel({"mt"}).bin_id({1}));     
    writer.WriteCards("mt_fail", cb.cp().channel({"mt"}).bin_id({2}));
    writer.WriteCards("mt_combined", cb.cp().channel({"mt"}).bin_id({1,2}));
    
    writer.WriteCards("et_pass", cb.cp().channel({"et"}).bin_id({1}));
    writer.WriteCards("et_fail", cb.cp().channel({"et"}).bin_id({2}));
    writer.WriteCards("et_combined", cb.cp().channel({"et"}).bin_id({1,2}));
    writer.WriteCards("combined", cb.cp().channel({"et","mt"}).bin_id({1,2}));

    cb.PrintAll();
    cout << " done\n";
    
    
}
