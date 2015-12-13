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

using namespace std;

int main() {
	ch::CombineHarvester cb;

	// cb.SetVerbosity(1);

	typedef vector<pair<int, string>> Categories;
	typedef vector<string> VString;

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
					masses, {"htt"}, {era}, {chn}, sig_procs, cats[chn+"_"+era], true);
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
			cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
					file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
		}
	}

    //This part is rather hacky, but needed to reproduce the legacy results. 
    //The legacy results are set in fb, so the signal processes are all divided
    //by 1000. Here the precision is also explicitly set to match that
    //in the legacy datacards.
    
    cb.cp().process({"AZh"}).ForEachProc([&](ch::Process *proc) {
        proc->set_rate(std::roundf(((proc->rate() / 1000)*10000.0))/10000.0 );
        
    });

    cout << ">> Generating bbb uncertainties...\n";
    auto bbb = ch::BinByBinFactory()
      .SetAddThreshold(0.1)
      .SetFixNorm(true);

    bbb.AddBinByBin(cb.cp().process({"Zjets"}), cb);  
	
    
    cout << ">> Setting standardised bin names...\n";
	ch::SetStandardBinNames(cb);

	string folder = "output/AZh_cards_fb";
	boost::filesystem::create_directories(folder);
	for (string chn :chns){
		boost::filesystem::create_directories(folder+"/"+chn);
		for (auto m:masses){
			boost::filesystem::create_directories(folder+"/"+chn+"/"+m);
			boost::filesystem::create_directories(folder+"/cmb/"+m);
		}
	}


	for (string chn : chns) {
		TFile output((folder+ "/htt_" + chn + ".input.root").c_str(),
				"RECREATE"); 
		auto bins = cb.cp().channel({chn}).bin_set();

		for (auto b : bins) {
			for (auto m : masses) {
				cout << ">> Writing datacard for bin: " << b << " and mass: " << m
					<< "\r" << flush;
				cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
						folder+"/"+chn+"/"+m+"/"+b + ".txt", output);
				cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
						folder+"/cmb/"+m+"/"+b + ".txt", output);
			}
		}
		  output.Close();
	}

	for (string chn:chns) {
		for (auto m:masses) {
			boost::filesystem::copy_file((folder+"/htt_"+chn+".input.root").c_str(),(folder+"/"+chn+"/"+m+"/htt_"+chn+".input.root").c_str(),boost::filesystem::copy_option::overwrite_if_exists);
		}
	} 

	cout << "\n>> Done!\n";
}
