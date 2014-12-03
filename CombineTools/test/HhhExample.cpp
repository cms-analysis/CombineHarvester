#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include "boost/filesystem.hpp"
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Utilities.h"
#include "CombineTools/interface/HttSystematics.h"

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
	{"et","mt"};
	//{"et", "mt","tt"};

	map<string, string> input_folders = {
		{"et", "Imperial"},
		{"mt", "Imperial"},
		{"tt", "Italians"}
	};

	map<string, VString> bkg_procs;
	bkg_procs["et"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	bkg_procs["mt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	// bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};

	/*map<string,VString> sm_procs;
	  sm_procs["et"] = {"ggH_SM125","VH_SM125","qqH_SM125"};
	  sm_procs["mt"] = {"ggH_SM125","VH_SM125","qqH_SM125"};
	  sm_procs["tt"] = {"ggH_SM125","VH_SM125","qqH_SM125"};
	 */

	VString sig_procs={"ggHTohhTo2Tau2B"};

	map<string, Categories> cats;
	cats["et_8TeV"] = {
		{0, "eleTau_2jet0tag"}, {1, "eleTau_2jet1tag"},
		{2, "eleTau_2jet2tag"}};

	cats["mt_8TeV"] = {
		{0, "muTau_2jet0tag"}, {1, "muTau_2jet1tag"},
		{2, "muTau_2jet2tag"}};

	/*  cats["tt_8TeV"] = {
	    {0, "tauTau_2jet0tag"}, {1, "tauTau_2jet1tag"},
	    {2, "tauTau_2jet2tag"}};
	 */


	vector<string> masses = ch::MassesFromRange("260-350:10");

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
	ch::AddSystematics_hhh_et_mt(cb);
	// ch::AddSystematics_hhh_tt(cb);

	cout << ">> Extracting histograms from input root files...\n";
	for (string era : {"8TeV"}) {
		for (string chn : chns) {
			string file = aux_shapes + input_folders[chn] + "/htt_" + chn +
				".inputs-Hhh-" + era + ".root";
			cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
					file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
			cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
					file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
		}
	}


	cout << ">> Merging bin errors...\n";
	ch::CombineHarvester cb_et = move(cb.cp().channel({"et"}));
	for (string era : {"8TeV"}) {
		cb_et.cp().era({era}).bin_id({0, 1, 2}).process({"ZL", "ZJ", "QCD", "W","TT","ZTT","VV"})
			.MergeBinErrors(0.1, 0.5);
	}
	ch::CombineHarvester cb_mt = move(cb.cp().channel({"mt"}));
	for (string era : {"8TeV"}) {
		cb_mt.cp().era({era}).bin_id({0, 1, 2}).process({"ZL", "ZJ", "QCD", "W", "TT","ZTT","VV"})
			.MergeBinErrors(0.1, 0.5);
	}


	/*ch::CombineHarvester cb_tt = move(cb.cp().channel({"tt"}));
	  cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"ZL","ZJ","QCD","W","TT", "ZTT", "VV"})
	  .MergeBinErrors(0.1, 0.5);
	 */

	cout << ">> Generating bbb uncertainties...\n";
	cb_mt.cp().bin_id({0, 1, 2}).process({"ZL","ZJ","W", "QCD","TT", "ZTT","VV"})
		.AddBinByBin(0.1, true, &cb);

	cb_et.cp().bin_id({0, 1, 2}).process({"ZL", "ZJ", "QCD", "W", "TT","ZTT","VV"})
		.AddBinByBin(0.1, true, &cb);

	//cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"ZL", "ZJ","W", "TT", "QCD", "ZTT","VV"})
	//   .AddBinByBin(0.1, true, &cb);

	cout << ">> Setting standardised bin names...\n";
	ch::SetStandardBinNames(cb);

	string folder = "output/hhh_cards";
	boost::filesystem::create_directories(folder);
	for (string chn :chns){
		boost::filesystem::create_directories(folder+"/"+chn);
		for (auto m:masses){
			boost::filesystem::create_directories(folder+"/"+chn+"/"+m);
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
						folder+"/"+chn+"/"+m+"/"+b + "_" + m + ".txt", output);
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
