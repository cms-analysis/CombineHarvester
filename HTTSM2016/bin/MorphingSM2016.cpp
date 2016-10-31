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
#include "CombineHarvester/HTTSM2016/interface/HttSystematics_SMRun2.h"
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

bool BinIsControlRegion(ch::Object const* obj)
{
    return (boost::regex_search(obj->bin(),boost::regex{"_cr$"}) || (obj->channel() == std::string("zmm")));
}

// Useful to have the inverse sometimes too
bool BinIsNotControlRegion(ch::Object const* obj)
{
    return !BinIsControlRegion(obj);
}



int main(int argc, char** argv) {
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    string SM125= "";
    string mass = "mA";
    string output_folder = "sm_run2";
    // TODO: option to pick up cards from different dirs depending on channel?
    // ^ Something like line 90?
    string input_folder_em="USCMS/";
    string input_folder_et="USCMS/";
    string input_folder_mt="USCMS/";
    string input_folder_tt="USCMS/";
    string input_folder_zmm="USCMS/";
    string postfix="";
    bool auto_rebin = false;
    bool manual_rebin = false;
    bool real_data = false;
    int control_region = 0;
    bool check_neg_bins = false;
    bool poisson_bbb = false;
    bool do_w_weighting = false;
    bool zmm_fit = false;
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("input_folder_em", po::value<string>(&input_folder_em)->default_value("USCMS"))
    ("input_folder_et", po::value<string>(&input_folder_et)->default_value("USCMS"))
    ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("USCMS"))
    ("input_folder_tt", po::value<string>(&input_folder_tt)->default_value("USCMS"))
    ("input_folder_zmm", po::value<string>(&input_folder_zmm)->default_value("USCMS"))
    ("postfix", po::value<string>(&postfix)->default_value(""))
    ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(false))
    ("real_data", po::value<bool>(&real_data)->default_value(false))
    ("manual_rebin", po::value<bool>(&manual_rebin)->default_value(false))
    ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125))
    ("control_region", po::value<int>(&control_region)->default_value(0))
    ("zmm_fit", po::value<bool>(&zmm_fit)->default_value(true))
    ("check_neg_bins", po::value<bool>(&check_neg_bins)->default_value(false))
    ("poisson_bbb", po::value<bool>(&poisson_bbb)->default_value(false))
    ("w_weighting", po::value<bool>(&do_w_weighting)->default_value(false));
    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);
    
    
    ch::CombineHarvester cb;
    
    
    typedef vector<string> VString;
    VString chns = {"mt","et"};
    if (zmm_fit) chns.push_back("zmm");
    
    map<string, VString> bkg_procs;
    bkg_procs["et"] = {"W", "QCD", "ZL", "ZJ","TT", "ZTT"};
    bkg_procs["mt"] = {"W", "QCD", "ZL", "ZJ", "TT","ZTT"};
    bkg_procs["tt"] = {"W", "QCD", "ZL", "ZJ", "ZTT"};
    bkg_procs["em"] = {"W", "QCD", "ZLL", "TT", "VV", "ZTT"};
    
    
    // Or equivalently, specify the mass points explicitly:
    vector<string> sig_procs = {"ggH","qqH"};
    //    vector<string> masses = ch::MassesFromRange("120-130:5");
    vector<string> masses = {"125"};
    
    
    
    typedef vector<pair<int, string>> Categories;
    map<string, Categories> cats;
    cats["et"] = {
        {1, "et_0jet_low"},
        {2, "et_1jet_low"},
        {3, "et_vbf_low"},
        {4, "et_0jet_high"},
        {5, "et_1jet_high"},
        {6, "et_vbf_high"}
    };
    
    cats["mt"] = {
        {1, "mt_0jet_low"},
        {2, "mt_1jet_low"},
        {3, "mt_vbf_low"},
        {4, "mt_0jet_high"},
        {5, "mt_1jet_high"},
        {6, "mt_vbf_high"}
    };
    
    cats["em"] = {
        {1, "em_0jet_low"},
        {2, "em_1jet_low"},
        {3, "em_vbf_low"},
        {4, "em_0jet_high"},
        {5, "em_1jet_high"},
        {6, "em_vbf_high"}};
    
    cats["tt"] = {
        
        {1, "tt_1jet_low"},
        {2, "tt_1jet_high"},
        {3, "tt_vbf_low"},
        {4, "tt_vbf_high"},
        {5, "tt_0jet"}};

    
    
    
    if (control_region > 0){
        // for each channel use the categories >= 10 for the control regions
        // the control regions are ordered in triples (10,11,12),(13,14,15)...
        for (auto chn : chns){
            // for em or tt do nothing
            if (ch::contains({"em", "tt", "zmm"}, chn)) {
                std::cout << " - Skipping extra control regions for channel " << chn << "\n";
                continue;
            }
            // if ( chn == "em") continue;
            Categories queue;
            int binid = 10;
            for (auto cat:cats[chn+"_13TeV"]){
//                queue.push_back(make_pair(binid,cat.second+"_wjets_cr"));
//                queue.push_back(make_pair(binid+1,cat.second+"_qcd_cr"));
//                queue.push_back(make_pair(binid+2,cat.second+"_wjets_ss_cr"));
                
                queue.push_back(make_pair(binid,cat.second+"_wjets_0jet_cr"));
                queue.push_back(make_pair(binid+1,cat.second+"_wjets_1jet_cr"));
                queue.push_back(make_pair(binid+2,cat.second+"_wjets_vbf_cr"));
                queue.push_back(make_pair(binid+3,cat.second+"_antiiso_0jet_cr"));
                queue.push_back(make_pair(binid+4,cat.second+"_antiiso_1jet_cr"));
                queue.push_back(make_pair(binid+5,cat.second+"_antiiso_vbf_cr"));
                
                
                binid += 6;
            }
            cats[chn+"_13TeV"].insert(cats[chn+"_13TeV"].end(),queue.begin(),queue.end());
        }
    }
    
    
    
    
    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
//    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/AllROOT_20fb/";
    std::map<string, string> input_dir;
    input_dir["em"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2016/shapes/"+input_folder_em+"/";
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2016/shapes/"+input_folder_mt+"/";
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2016/shapes/"+input_folder_et+"/";
    input_dir["tt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2016/shapes/"+input_folder_tt+"/";
    input_dir["zmm"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2016/shapes/"+input_folder_zmm+"/";
    

 
    //! [part2]
    for (auto chn : chns) {
        cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn]);
        cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn], false);
        cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
        
    }
    
    //! [part4]
    
    
    //Some of the code for this is in a nested namespace, so
    // we'll make some using declarations first to simplify things a bit.
    using ch::syst::SystMap;
    using ch::syst::era;
    using ch::syst::channel;
    using ch::syst::bin_id;
    using ch::syst::process;
    

  ch::AddSMRun2Systematics(cb, control_region, zmm_fit);

    
    
    
    //! [part7]
    for (string chn:chns){
        cb.cp().channel({chn}).backgrounds().ExtractShapes(
                                                           input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                           "$BIN/$PROCESS",
                                                           "$BIN/$PROCESS_$SYSTEMATIC");
        //    if(SM125==string("signal_SM125")) cb.cp().channel({chn}).process(SM_procs).ExtractShapes(
        //         input_dir[chn] + "htt_"+chn+".inputs-mssm-13TeV"+postfix+".root",
        //         "$BIN/$PROCESS",
        //         "$BIN/$PROCESS_$SYSTEMATIC");
        cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
                                                                input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                "$BIN/$PROCESS$MASS",
                                                                "$BIN/$PROCESS$MASS_$SYSTEMATIC");
        //    cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
        //        input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
        //        "$BIN/qqH$MASS",
        //        "$BIN/qqH$MASS_$SYSTEMATIC");
    }
    
    
    
    
    
    
    
    //! [part8]
    auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.1)
    .SetMergeThreshold(0.5)
    .SetFixNorm(true);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
    
    
    // This function modifies every entry to have a standardised bin name of
    // the form: {analysis}_{channel}_{bin_id}_{era}
    // which is commonly used in the htt analyses
    ch::SetStandardBinNames(cb);
    //! [part8]
    
    //! [part9]
    // First we generate a set of bin names:
//    set<string> bins = cb.bin_set();
    // This method will produce a set of unique bin names by considering all
    // Observation, Process and Systematic entries in the CombineHarvester
    // instance.
    
    // We create the output root file that will contain all the shapes.
    // Here we define a CardWriter with a template for how the text datacard
    // and the root files should be named.
//    ch::CardWriter writer("$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt",
//                          "$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root");
//    // writer.SetVerbosity(1);
//    writer.WriteCards("output/htt_cards8_20fb_22Sep/cmb", cb);
//    for (auto chn : cb.channel_set()) {
//        writer.WriteCards("output/htt_cards8_20fb_22Sep/" + chn, cb.cp().channel({chn}));
//    }
//    TFile output("output/htt_cards8_20fb_22Sep/htt.input.root", "RECREATE");
    
    
    
    
    
    
    //! [part9]
    // First we generate a set of bin names:

    
    //Write out datacards. Naming convention important for rest of workflow. We
    //make one directory per chn-cat, one per chn and cmb. In this code we only
    //store the individual datacards for each directory to be combined later, but
    //note that it's also possible to write out the full combined card with CH
    string output_prefix = "output/";
    if(output_folder.compare(0,1,"/") == 0) output_prefix="";
    ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$BIN.txt",
                          output_prefix + output_folder + "/$TAG/htt_input.root");
    // We're not using mass as an identifier - which we need to tell the CardWriter
    // otherwise it will see "*" as the mass value for every object and skip it
    writer.SetWildcardMasses({});
    writer.SetVerbosity(1);
    
    writer.WriteCards("cmb", cb);
    for (auto chn : chns) {
        if(chn == std::string("zmm"))
        {
            continue;
        }
        // per-channel
        writer.WriteCards(chn, cb.cp().channel({chn, "zmm"}));
        // And per-channel-category
        writer.WriteCards("htt_"+chn+"_1_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({1,10,13}));
        writer.WriteCards("htt_"+chn+"_2_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({2,10,13}));
        writer.WriteCards("htt_"+chn+"_3_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({3,11,14}));
        writer.WriteCards("htt_"+chn+"_4_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({4,11,14}));
        writer.WriteCards("htt_"+chn+"_5_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({5,12,15}));
        writer.WriteCards("htt_"+chn+"_6_13TeV", cb.cp().channel({chn,"zmm"}).bin_id({6,12,15}));
    }
    // For btag/nobtag areas want to include control regions. This will
    // work even if the extra categories aren't there.
//    writer.WriteCards("htt_cmb_1_13TeV", cb.cp().bin_id({1, 10, 11, 12}));
//    writer.WriteCards("htt_cmb_2_13TeV", cb.cp().bin_id({1, 13, 14, 15}));
//    writer.WriteCards("htt_cmb_3_13TeV", cb.cp().bin_id({1, 17, 17, 18}));
    
    cb.PrintAll();
    cout << " done\n";
    
    
    
    
    
    
    
    
    
}
