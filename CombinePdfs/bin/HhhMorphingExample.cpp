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
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"

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

	string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
	string aux_shapes   = auxiliaries +"shapes/";
	string aux_pruning  = auxiliaries +"pruning/";

    // RooFit will be quite noisy if we don't set this
    RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
  
    // In the first part of this code we will construct our MSSM signal model.
    // This means declaring mA and tanb as our free parameters, and defining all
    // other Higgs masses, cross sections and branching ratios as a function of
    // these. Note that this example is very verbose and explicit in the
    // construction - one could imagine developing a more generic and efficient
    // tool to do this.

    // Define mA and tanb as RooRealVars
    // Here I do not declare a range and it is decided automatically from 
    // the inputs once the first RooDataHist is created. 
    // There were some issues found with declaring a range by hand.
    RooRealVar mA("mA", "mA", 300.);
    RooRealVar tanb("tanb", "tanb", 1.);

    // All the other inputs we need to build the model can be found in one of the
    // LHCXSWG scans. Here we use the low-tanb-high scenario. This file contains a
    // large number of 2D histograms, all binned in mA and tanb, that each provide
    // a different mass, xsec or BR.
    TFile inputs(TString(auxiliaries) +
               "models/out.low-tb-high-8TeV-tanbAll-nnlo.root");
    // Get the TH2Fs for the masses of the h and H bosons.
    TH2F h_mH = ch::OpenFromTFile<TH2F>(&inputs, "h_mH");
    TH2F h_mh = ch::OpenFromTFile<TH2F>(&inputs, "h_mh");
    // Now two more steps are needed: we have to convert each TH2F to a
    // RooDataHist, then build a RooHistFunc from the RooDataHist. These steps
    // will be repeated for every TH2F we import below.
    RooDataHist dh_mH("dh_mH", "dh_mH", RooArgList(mA, tanb),
                    RooFit::Import(h_mH));
    RooDataHist dh_mh("dh_mh", "dh_mh", RooArgList(mA, tanb),
                    RooFit::Import(h_mh));
    RooHistFunc mH("mH", "mH", RooArgList(mA, tanb), dh_mH);
    RooHistFunc mh("mh", "mh", RooArgList(mA, tanb), dh_mh);
    // There is also the possibility to interpolate mass values rather than just
    // take the value of the enclosing histogram bin, but we'll leave this off for
    // now.
    // mH.setInterpolationOrder(1);

    // Now we'll do the same for the cross section
    TH2F h_ggF_xsec_H = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_H");
    RooDataHist dh_ggF_xsec_H("dh_ggF_xsec_H", "dh_ggF_xsec_H",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_H));
    RooHistFunc ggF_xsec_H("ggF_xsec_H", "ggF_xsec_H", RooArgList(mA, tanb),
                         dh_ggF_xsec_H);

    // Now the branching ratios to hh, tau tau and bb
    TH2F h_brh0h0_H = ch::OpenFromTFile<TH2F>(&inputs, "h_brh0h0_H");
    // Add factor of 2 here for h->tautau, h->bb and reverse
    h_brh0h0_H = 2*h_brh0h0_H;
    TH2F h_brtautau_h = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_h");
    TH2F h_brbb_h = ch::OpenFromTFile<TH2F>(&inputs, "h_brbb_h");
    RooDataHist dh_brh0h0_H("dh_brh0h0_H", "dh_brh0h0_H",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brh0h0_H));
    RooDataHist dh_brtautau_h("dh_brtautau_h", "dh_brtautau_h",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_h));
    RooDataHist dh_brbb_h("dh_brbb_h", "dh_brbb_h",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brbb_h));
    RooHistFunc brh0h0_H("brh0h0_H", "brh0h0_H", RooArgList(mA, tanb),
                         dh_brh0h0_H);
    RooHistFunc brtautau_h("brtautau_h", "brtautau_h", RooArgList(mA, tanb),
                         dh_brtautau_h);
    RooHistFunc brbb_h("brbb_h", "brbb_h", RooArgList(mA, tanb),
                         dh_brbb_h);
    // We can build the xsec * BR products
    RooProduct ggF_xsec_br_H("ggF_xsec_br_H", "",
                           RooArgList(ggF_xsec_H, brh0h0_H, brtautau_h, brbb_h));
    // Let's print out the values of all of these objects
    cout << "mA: " << mA.getVal() << "\n";
    cout << "tanb: " << tanb.getVal() << "\n\n";
    cout << "mH: " << mH.getVal() << "\n";
    cout << "mh: " << mh.getVal() << "\n";
    cout << "ggF_xsec_H: " << ggF_xsec_H.getVal() << "\n";
    cout << "brh0h0_H: " << brh0h0_H.getVal()/2<< "\n";
    cout << "brtautau_h: " << brtautau_h.getVal() << "\n";
    cout << "brbb_h: " << brbb_h.getVal() << "\n";
    cout << "ggF_xsec_br_H: " << ggF_xsec_br_H.getVal() << "\n";
  
    map<string, RooAbsArg *> xs_map;
    xs_map["ggHTohhTo2Tau2B"] = &ggF_xsec_br_H;
    
    VString chns =
	{"et", "mt","tt"};

	map<string, string> input_folders = {
		{"et", "Imperial"},
		{"mt", "Imperial"},
		{"tt", "Italians"}
	};

	map<string, VString> bkg_procs;
	bkg_procs["et"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	bkg_procs["mt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV"};

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

	  cats["tt_8TeV"] = {
	    {0, "tauTau_2jet0tag"}, {1, "tauTau_2jet1tag"},
	    {2, "tauTau_2jet2tag"}};
	 


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

    //Remove W background from 2jet1tag and 2jet2tag categories for tt channel
    cb.FilterProcs([](ch::Process const* p) {
      return (p->bin() == "tauTau_2jet1tag") && p->process() == "W";
    });
    cb.FilterProcs([](ch::Process const* p) {
      return (p->bin() == "tauTau_2jet2tag") && p->process() == "W";
    });
	
    cout << ">> Adding systematic uncertainties...\n";
	ch::AddSystematics_hhh_et_mt(cb);
    ch::AddSystematics_hhh_tt(cb);

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
		cb_et.cp().era({era}).bin_id({0, 1, 2}).process({"QCD","W","ZL","ZJ","VV","ZTT","TT"})
			.MergeBinErrors(0.1, 0.5);
	}
	ch::CombineHarvester cb_mt = move(cb.cp().channel({"mt"}));
	for (string era : {"8TeV"}) {
		cb_mt.cp().era({era}).bin_id({0, 1, 2}).process({"QCD","W","ZL","ZJ","VV","ZTT","TT"})
			.MergeBinErrors(0.1, 0.5);
	}
	ch::CombineHarvester cb_tt = move(cb.cp().channel({"tt"}));
	for (string era : {"8TeV"}) {
		cb_tt.cp().era({era}).bin_id({0, 1, 2}).process({"QCD","W","ZLL","VV","ZTT","TT"})
			.MergeBinErrors(0.1, 0.5);
	}

	cout << ">> Generating bbb uncertainties...\n";
	cb_mt.cp().bin_id({0, 1, 2}).process({"ZL","ZJ","W", "QCD","TT", "ZTT","VV"})
		.AddBinByBin(0.1, true, &cb);

	cb_et.cp().bin_id({0, 1, 2}).process({"ZL", "ZJ", "QCD", "W", "TT","ZTT","VV"})
		.AddBinByBin(0.1, true, &cb);

	cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"ZL", "ZJ","W", "TT", "QCD", "ZTT","VV"})
	   .AddBinByBin(0.1, true, &cb);

	cout << ">> Setting standardised bin names...\n";
	ch::SetStandardBinNames(cb);


    RooWorkspace ws("htt", "htt");
 
    TFile demo("Hhh_demo.root", "RECREATE");

    bool do_morphing = true;
    string postfix = "_eff_acc";
    map<string, RooAbsReal *> mass_var = {
      {"ggHTohhTo2Tau2B", &mH}
    };
    if (do_morphing) {
      auto bins = cb.bin_set();
      for (auto b : bins) {
        auto procs = cb.cp().bin({b}).signals().process_set();
        for (auto p : procs) {
          string pdf_name = b + "_" + p + "_morph";
          ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),
                               "eff_acc", true, true, true, &demo);
          std::string prod_name = pdf_name + "_eff_acc";
          RooAbsReal *norm =  ws.function(prod_name.c_str());
          RooProduct full_norm((pdf_name + "_norm").c_str(), "",
                                 RooArgList(*norm, *(xs_map[p])));
          ws.import(full_norm, RooFit::RecycleConflictNodes());
        }
      }
    }
    demo.Close();
    cb.AddWorkspace(ws);
    cb.cp().signals().ExtractPdfs(cb, "htt", "$BIN_$PROCESS_morph");
    cb.PrintAll();
    

	string folder = "output/hhh_cards";
	boost::filesystem::create_directories(folder);
  
    TFile output((folder + "/htt_input.Hhh.root").c_str(), "RECREATE");
    cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_cmb_Hhh.txt", output);
    auto bins = cb.bin_set();
    for (auto b : bins) {
      cb.cp().bin({b}).mass({"*"}).WriteDatacard(
      folder + "/" + b + ".txt", output);
    }
    output.Close();

	cout << "\n>> Done!\n";
}
