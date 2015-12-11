#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include "boost/filesystem.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "RooDataHist.h"
#include "RooHistFunc.h"
#include "RooFormulaVar.h"
#include "RooProduct.h"

using namespace std;

int main() {
	ch::CombineHarvester cb;

	// cb.SetVerbosity(1);

	typedef vector<pair<int, string>> Categories;
	typedef vector<string> VString;
    
    // RooFit will be quite noisy if we don't set this
    RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

    //RooRealVar mA("mA", "mA", 260., 350.);
    RooRealVar mA("mA", "mA", 300.);
	
    string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
	string aux_shapes   = auxiliaries +"shapes/";
	string aux_pruning  = auxiliaries +"pruning/";

	VString chns =
	{"et", "mt","tt", "em"};

	string input_folders = "ULB";

	map<string, VString> bkg_procs;
	bkg_procs["et"] = {"ZZ","GGToZZ2L2L","TTZ","WWZ","ZZZ","WZZ","Zjets"};
	bkg_procs["mt"] = {"ZZ","GGToZZ2L2L","TTZ","WWZ","ZZZ","WZZ","Zjets"};
	bkg_procs["em"] = {"ZZ","GGToZZ2L2L","TTZ","WWZ","ZZZ","WZZ","Zjets"};
	bkg_procs["tt"] = {"ZZ","GGToZZ2L2L","TTZ","WWZ","ZZZ","WZZ","Zjets"};

	map<string,VString> sm_procs;
	  sm_procs["et"] = {"ZH_ww125","ZH_tt125"};
	 

	VString sig_procs={"AZh"};
    map<string, VString> signal_types = {
      {"AZh", {"ggA_AZhLLtautau"}}
    };
    
	map<string, Categories> cats;
	cats["et_8TeV"] = {
		{0, "eeet_zh"}, {1, "mmet_zh"}};
	cats["mt_8TeV"] = {
		{0, "eemt_zh"}, {1, "mmmt_zh"}};
	cats["em_8TeV"] = {
		{0, "eeem_zh"}, {1, "mmme_zh"}};
	cats["tt_8TeV"] = {
		{0, "eett_zh"}, {1, "mmtt_zh"}};

	vector<string> masses = ch::MassesFromRange("220-350:10");

	cout << ">> Creating processes and observations...\n";
	for (string era : {"8TeV"}) {
		for (auto chn : chns) {
			cb.AddObservations(
					{"*"}, {"htt"}, {era}, {chn}, cats[chn+"_"+era]);
			cb.AddProcesses(
					{"*"}, {"htt"}, {era}, {chn}, bkg_procs[chn], cats[chn+"_"+era], false);
			//    cb.AddProcesses(
			//    {"*"},{"htt"}, {era}, {chn}, sm_procs[chn], cats[chn+"_"+era],false);
			cb.AddProcesses(
					masses, {"htt"}, {era}, {chn}, signal_types["AZh"], cats[chn+"_"+era], true);
		}
	}

	
    cout << ">> Adding systematic uncertainties...\n";
	ch::AddSystematics_AZh(cb);

	cout << ">> Extracting histograms from input root files...\n";
	for (string era : {"8TeV"}) {
		for (string chn : chns) {
			string file = aux_shapes + input_folders + "/htt_AZh" +
                ".inputs-AZh-" + era + ".root";
			cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
					file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
			cb.cp().channel({chn}).era({era}).process(signal_types["AZh"]).ExtractShapes(
					file, "$BIN/AZh$MASS", "$BIN/AZh$MASS_$SYSTEMATIC");
		}
	}


    cout << ">> Generating bbb uncertainties...\n";
    auto bbb = ch::BinByBinFactory()
      .SetAddThreshold(0.1)
      .SetFixNorm(true);

    bbb.AddBinByBin(cb.cp().process({"Zjets"}), cb);  
	
    
    cout << ">> Setting standardised bin names...\n";
	ch::SetStandardBinNames(cb);


    RooWorkspace ws("htt", "htt");
 
    TFile demo("AZh_demo.root", "RECREATE");

    bool do_morphing = true;
    map<string, RooAbsReal *> mass_var = {
      {"ggA_AZhLLtautau", &mA}
    };
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
    cb.cp().signals().ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
    cb.PrintAll();
    
    
	string folder = "output/AZh_cards_nomodel";
	boost::filesystem::create_directories(folder);
  
    TFile output((folder + "/htt_input.AZh.root").c_str(), "RECREATE");
    cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_cmb_AZh.txt", output);
    auto bins = cb.bin_set();
    for (auto b : bins) {
      cb.cp().bin({b}).mass({"*"}).WriteDatacard(
      folder + "/" + b + ".txt", output);
    }
    output.Close();


	cout << "\n>> Done!\n";
}
