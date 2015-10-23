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
    
    // RooFit will be quite noisy if we don't set this
    RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

	
    string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
	string aux_shapes   = auxiliaries +"shapes/";
	string aux_pruning  = auxiliaries +"pruning/";

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
    //TH2F h_mH = ch::OpenFromTFile<TH2F>(&inputs, "h_mH");
    //TH2F h_mh = ch::OpenFromTFile<TH2F>(&inputs, "h_mh");
    // Now two more steps are needed: we have to convert each TH2F to a
    // RooDataHist, then build a RooHistFunc from the RooDataHist. These steps
    // will be repeated for every TH2F we import below.
    //RooDataHist dh_mH("dh_mH", "dh_mH", RooArgList(mA, tanb),
                //    RooFit::Import(h_mH));
    //RooDataHist dh_mh("dh_mh", "dh_mh", RooArgList(mA, tanb),
     //               RooFit::Import(h_mh));
    //RooHistFunc mH("mH", "mH", RooArgList(mA, tanb), dh_mH);
    //RooHistFunc mh("mh", "mh", RooArgList(mA, tanb), dh_mh);
    // There is also the possibility to interpolate mass values rather than just
    // take the value of the enclosing histogram bin, but we'll leave this off for
    // now.
    // mH.setInterpolationOrder(1);

    // Now we'll do the same for the cross section
    TH2F h_ggF_xsec_A = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_A");
    RooDataHist dh_ggF_xsec_A("dh_ggF_xsec_A", "dh_ggF_xsec_A",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_A));
    RooHistFunc ggF_xsec_A("ggF_xsec_A", "ggF_xsec_A", RooArgList(mA, tanb),
                         dh_ggF_xsec_A);

    // Now the branching ratios to hh, tau tau and bb
    TH2F h_brZh0_A = ch::OpenFromTFile<TH2F>(&inputs, "h_brZh0_A");
    // Add factor of 2 here for h->tautau, h->bb and reverse
    h_brZh0_A = 0.10099*h_brZh0_A;
    TH2F h_brtautau_h = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_h");
    RooDataHist dh_brZh0_A("dh_brZh0_A", "dh_brZh0_A",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brZh0_A));
    RooDataHist dh_brtautau_h("dh_brtautau_h", "dh_brtautau_h",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_h));
    RooHistFunc brZh0_A("brZh0_A", "brZh0_A", RooArgList(mA, tanb),
                         dh_brZh0_A);
    RooHistFunc brtautau_h("brtautau_h", "brtautau_h", RooArgList(mA, tanb),
                         dh_brtautau_h);
    // We can build the xsec * BR products
    RooProduct ggF_xsec_br_A("ggF_xsec_br_A", "",
                           RooArgList(ggF_xsec_A, brZh0_A, brtautau_h));
    // Let's print out the values of all of these objects
    cout << "mA: " << mA.getVal() << "\n";
    cout << "tanb: " << tanb.getVal() << "\n\n";
    cout << "ggF_xsec_A: " << ggF_xsec_A.getVal() << "\n";
    cout << "brZh0_A: " << brZh0_A.getVal()/0.10099<< "\n";
    cout << "brtautau_h: " << brtautau_h.getVal() << "\n";
    cout << "ggF_xsec_br_A: " << ggF_xsec_br_A.getVal() << "\n";

    map<string, RooAbsArg *> xs_map;
    xs_map["AZh"] = &ggF_xsec_br_A;

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
    string postfix = "_eff_acc";
    map<string, RooAbsReal *> mass_var = {
      {"AZh", &mA}
    };
    if (do_morphing) {
      auto bins = cb.bin_set();
      for (auto b : bins) {
        auto procs = cb.cp().bin({b}).signals().process_set();
        for (auto p : procs) {
          string pdf_name = b + "_" + p + "_morph";
          ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),
                               "eff_acc", true, true, false, &demo);
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
    
    
	string folder = "output/AZh_cards";
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
