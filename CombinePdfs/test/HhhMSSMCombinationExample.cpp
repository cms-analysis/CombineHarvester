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
#include "CombinePdfs/interface/MorphFunctions.h"
#include "CombineTools/interface/TFileIO.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "RooDataHist.h"
#include "RooHistFunc.h"
#include "RooFormulaVar.h"
#include "RooProduct.h"

using namespace std;

TH2F SantanderMatching(TH2F const& h4f, TH2F const& h5f, TH2F const* mass) {
  TH2F res = h4f;
  for (int x = 1; x <= h4f.GetNbinsX(); ++x) {
    for (int y = 1; y <= h4f.GetNbinsY(); ++y) {
      double mh =
          mass ? mass->GetBinContent(x, y) : h4f.GetXaxis()->GetBinCenter(x);
      double t = log(mh / 4.75) - 2.;
      double fourflav = h4f.GetBinContent(x, y);
      double fiveflav = h5f.GetBinContent(x, y);
      double sigma = (1. / (1. + t)) * (fourflav + t * fiveflav);
      res.SetBinContent(x, y, sigma);
    }
  }
  return res;
}

TH1F RestoreBinning(TH1F const& src, TH1F const& ref) {
  TH1F res = ref;
  res.Reset();
  for (int x = 1; x <= res.GetNbinsX(); ++x) {
    res.SetBinContent(x, src.GetBinContent(x));
  }
  return res;
}

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
    // Extra histograms needed for MSSM part
    TH2F h_ggF_xsec_h = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_h");
    RooDataHist dh_ggF_xsec_h("dh_ggF_xsec_h", "dh_ggF_xsec_h",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_h));
    RooHistFunc ggF_xsec_h("ggF_xsec_h", "ggF_xsec_h", RooArgList(mA, tanb),
                         dh_ggF_xsec_h);
    TH2F h_ggF_xsec_A = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_A");
    RooDataHist dh_ggF_xsec_A("dh_ggF_xsec_A", "dh_ggF_xsec_A",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_A));
    RooHistFunc ggF_xsec_A("ggF_xsec_A", "ggF_xsec_A", RooArgList(mA, tanb),
                         dh_ggF_xsec_A);

    // And the same for the b-associated production - but with the caveat that
    // we must first do the Santander-matching of the 4FS and 5FS.
    TH2F h_bbH5f_xsec_h = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH_xsec_h");
    TH2F h_bbH5f_xsec_H = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH_xsec_H");
    TH2F h_bbH5f_xsec_A = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH_xsec_A");
    TH2F h_bbH4f_xsec_h = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH4f_xsec_h");
    TH2F h_bbH4f_xsec_H = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH4f_xsec_H");
    TH2F h_bbH4f_xsec_A = ch::OpenFromTFile<TH2F>(&inputs, "h_bbH4f_xsec_A");
    TH2F h_bbH_xsec_h = SantanderMatching(h_bbH4f_xsec_h, h_bbH5f_xsec_h, &h_mh);
    TH2F h_bbH_xsec_H = SantanderMatching(h_bbH4f_xsec_H, h_bbH5f_xsec_H, &h_mH);
    TH2F h_bbH_xsec_A = SantanderMatching(h_bbH4f_xsec_H, h_bbH5f_xsec_H, nullptr);
    RooDataHist dh_bbH_xsec_h("dh_bbH_xsec_h", "dh_bbH_xsec_h",
                            RooArgList(mA, tanb), RooFit::Import(h_bbH_xsec_h));
    RooDataHist dh_bbH_xsec_H("dh_bbH_xsec_H", "dh_bbH_xsec_H",
                            RooArgList(mA, tanb), RooFit::Import(h_bbH_xsec_H));
    RooDataHist dh_bbH_xsec_A("dh_bbH_xsec_A", "dh_bbH_xsec_A",
                            RooArgList(mA, tanb), RooFit::Import(h_bbH_xsec_A));
    RooHistFunc bbH_xsec_h("bbH_xsec_h", "bbH_xsec_h", RooArgList(mA, tanb),
                         dh_bbH_xsec_h);
    RooHistFunc bbH_xsec_H("bbH_xsec_H", "bbH_xsec_H", RooArgList(mA, tanb),
                         dh_bbH_xsec_H);
    RooHistFunc bbH_xsec_A("bbH_xsec_A", "bbH_xsec_A", RooArgList(mA, tanb),
                         dh_bbH_xsec_A);

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
    // Extra histograms needed for MSSM part
    TH2F h_brtautau_H = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_H");
    TH2F h_brtautau_A = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_A");
    RooDataHist dh_brtautau_H("dh_brtautau_H", "dh_brtautau_H",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_H));
    RooDataHist dh_brtautau_A("dh_brtautau_A", "dh_brtautau_A",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_A));
    RooHistFunc brtautau_H("brtautau_H", "brtautau_H", RooArgList(mA, tanb),
                         dh_brtautau_H);
    RooHistFunc brtautau_A("brtautau_A", "brtautau_A", RooArgList(mA, tanb),
                         dh_brtautau_A);
    
    
    // We can build the xsec * BR products
    RooProduct ggF_xsec_br_H_hh("ggF_xsec_br_H_hh", "",
                           RooArgList(ggF_xsec_H, brh0h0_H, brtautau_h, brbb_h));
    RooProduct ggF_xsec_br_h("ggF_xsec_br_h", "",
                           RooArgList(ggF_xsec_h, brtautau_h));
    RooProduct ggF_xsec_br_H("ggF_xsec_br_H", "",
                           RooArgList(ggF_xsec_H, brtautau_H));
    RooProduct ggF_xsec_br_A("ggF_xsec_br_A", "",
                           RooArgList(ggF_xsec_A, brtautau_A));
    RooProduct bbH_xsec_br_h("bbH_xsec_br_h", "",
                           RooArgList(bbH_xsec_h, brtautau_h));
    RooProduct bbH_xsec_br_H("bbH_xsec_br_H", "",
                           RooArgList(bbH_xsec_H, brtautau_H));
    RooProduct bbH_xsec_br_A("bbH_xsec_br_A", "",
                           RooArgList(bbH_xsec_A, brtautau_A));
    
    
    // Let's print out the values of all of these objects
    cout << "mA: " << mA.getVal() << "\n";
    cout << "tanb: " << tanb.getVal() << "\n\n";
    cout << "mH: " << mH.getVal() << "\n";
    cout << "mh: " << mh.getVal() << "\n";
    cout << "ggF_xsec_H: " << ggF_xsec_H.getVal() << "\n";
    cout << "brh0h0_H: " << brh0h0_H.getVal()/2<< "\n";
    cout << "brtautau_h: " << brtautau_h.getVal() << "\n";
    cout << "brbb_h: " << brbb_h.getVal() << "\n";
    cout << "ggF_xsec_br_H_hh: " << ggF_xsec_br_H_hh.getVal() << "\n";
    cout << "ggF_xsec_h: " << ggF_xsec_h.getVal() << "\n";
    cout << "ggF_xsec_H: " << ggF_xsec_H.getVal() << "\n";
    cout << "ggF_xsec_A: " << ggF_xsec_A.getVal() << "\n";
    cout << "bbH_xsec_h: " << bbH_xsec_h.getVal() << "\n";
    cout << "bbH_xsec_H: " << bbH_xsec_H.getVal() << "\n";
    cout << "bbH_xsec_A: " << bbH_xsec_A.getVal() << "\n";
    cout << "brtautau_h: " << brtautau_h.getVal() << "\n";
    cout << "brtautau_H: " << brtautau_H.getVal() << "\n";
    cout << "brtautau_A: " << brtautau_A.getVal() << "\n\n";
    cout << "ggF_xsec_br_h: " << ggF_xsec_br_h.getVal() << "\n";
    cout << "ggF_xsec_br_H: " << ggF_xsec_br_H.getVal() << "\n";
    cout << "ggF_xsec_br_A: " << ggF_xsec_br_A.getVal() << "\n\n";
    cout << "bbH_xsec_br_h: " << bbH_xsec_br_h.getVal() << "\n";
    cout << "bbH_xsec_br_H: " << bbH_xsec_br_H.getVal() << "\n";
    cout << "bbH_xsec_br_A: " << bbH_xsec_br_A.getVal() << "\n\n";
  
    map<string, RooAbsArg *> xs_map;
    xs_map["ggHTohhTo2Tau2B"] = &ggF_xsec_br_H_hh;
    xs_map["ggh"] = &ggF_xsec_br_h;
    xs_map["ggH"] = &ggF_xsec_br_H;
    xs_map["ggA"] = &ggF_xsec_br_A;
    xs_map["bbh"] = &bbH_xsec_br_h;
    xs_map["bbH"] = &bbH_xsec_br_H;
    xs_map["bbA"] = &bbH_xsec_br_A;
    
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


	map<string, Categories> cats;
	cats["et_8TeV"] = {
		{0, "eleTau_2jet0tag"}, {1, "eleTau_2jet1tag"},
		{2, "eleTau_2jet2tag"}};

	cats["mt_8TeV"] = {
		{0, "muTau_2jet0tag"}, {1, "muTau_2jet1tag"},
//		{2, "muTau_2jet2tag"}};
		{2, "muTau_2jet2tag"},
        {8, "muTau_nobtag"},
        {9, "muTau_btag"}};

	  cats["tt_8TeV"] = {
	    {0, "tauTau_2jet0tag"}, {1, "tauTau_2jet1tag"},
	    {2, "tauTau_2jet2tag"}};
	
	VString sig_procs = {"ggHTohhTo2Tau2B"};

	vector<string> masses = ch::MassesFromRange("260-350:10");

	// Create the backgrounds and observations for all categories
    cout << ">> Creating processes and observations...\n";
	for (string era : {"8TeV"}) {
		for (auto chn : chns) {
			cb.AddObservations(
					{"*"}, {"htt"}, {era}, {chn}, cats[chn+"_"+era]);
			cb.AddProcesses(
					{"*"}, {"htt"}, {era}, {chn}, bkg_procs[chn], cats[chn+"_"+era], false);
		}
	}
	// Create the H->hh signal for the H->hh categories 
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"et"},
                  sig_procs, {cats["et_8TeV"]}, true);
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"tt"},
                  sig_procs, {cats["tt_8TeV"]}, true);
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  sig_procs, {cats["mt_8TeV"][0]}, true);
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  sig_procs, {cats["mt_8TeV"][1]}, true);
    cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  sig_procs, {cats["mt_8TeV"][2]}, true);
    
	// create the phi->tautau signal for the MSSM categories 
    map<string, VString> signal_types = {
      {"ggH", {"ggh", "ggH", "ggA"}},
      {"bbH", {"bbh", "bbH", "bbA"}}
    };
    auto mssm_masses = ch::MassesFromRange(
      "90,100,120-140:10,140-200:20,200-500:50,600-1000:100");
    cb.AddProcesses(mssm_masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["ggH"], {cats["mt_8TeV"][3]}, true);
    cb.AddProcesses(mssm_masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["bbH"], {cats["mt_8TeV"][4]}, true);
    cb.AddProcesses(mssm_masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["bbH"], {cats["mt_8TeV"][3]}, true);
    cb.AddProcesses(mssm_masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["ggH"], {cats["mt_8TeV"][4]}, true);

    //Remove W background from 2jet1tag and 2jet2tag categories for tt channel
    cb.FilterProcs([](ch::Process const* p) {
      return (p->bin() == "tauTau_2jet1tag") && p->process() == "W";
    });
    cb.FilterProcs([](ch::Process const* p) {
      return (p->bin() == "tauTau_2jet2tag") && p->process() == "W";
    });
	
    cout << ">> Adding systematic uncertainties...\n";
	ch::AddSystematics_hhh_et_mt(cb,cb.cp().bin_id({0,1,2}));
    ch::AddSystematics_hhh_tt(cb,cb.cp().bin_id({0,1,2}));
    ch::AddMSSMSystematics(cb,cb.cp().bin_id({8,9}));

	cout << ">> Extracting histograms from input root files...\n";
	for (string era : {"8TeV"}) {
		for (string chn : chns) {
			string file = aux_shapes + input_folders[chn] + "/htt_" + chn +
				".inputs-Hhh-" + era + ".root";
			cb.cp().channel({chn}).era({era}).bin_id({0,1,2}).backgrounds().ExtractShapes(
					file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
			cb.cp().channel({chn}).era({era}).bin_id({0,1,2}).signals().ExtractShapes(
					file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
		}
	}
    //Read the MSSM part, just for mutau for now
    // We have to map each Higgs signal process to the same histogram, i.e:
    // {ggh, ggH, ggA} --> ggH
    // {bbh, bbH, bbA} --> bbH
	for (string era : {"8TeV"}) {
	    string file = aux_shapes + input_folders["mt"] + "/htt_mt.inputs-mssm-" + era + "-0.root";
		cb.cp().channel({"mt"}).era({era}).bin_id({8,9}).backgrounds().ExtractShapes(
				file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
		cb.cp().channel({"mt"}).era({era}).bin_id({8,9}).process(signal_types["ggH"]).ExtractShapes(
				file, "$CHANNEL/ggH$MASS", "$CHANNEL/ggH$MASS_$SYSTEMATIC");
		cb.cp().channel({"mt"}).era({era}).bin_id({8,9}).process(signal_types["bbH"]).ExtractShapes(
				file, "$CHANNEL/bbH$MASS", "$CHANNEL/bbH$MASS_$SYSTEMATIC");
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
      {"ggHTohhTo2Tau2B", &mH}, {"ggh", &mh}, {"ggH", &mH}, {"ggA", &mA},
      {"bbh", &mh}, {"bbH", &mH}, {"bbA", &mA}
    };
    
    if (do_morphing) {
      auto bins = cb.bin_set();
      for (auto b : bins) {
        auto procs = cb.cp().bin({b}).signals().process_set();
        std::cout << "morphing bin: " << b << std::endl;
        for (auto p : procs) {
          std::cout << "morphing process: " << p << std::endl;
          string pdf_name = b + "_" + p + "_morph";
          ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),
                               "eff_acc", true, true, &demo);
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
    

	string folder = "output/mssm_hhh_cards";
	boost::filesystem::create_directories(folder);
  
    TFile output((folder + "/htt_input.mssm.Hhh.root").c_str(), "RECREATE");
    cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_cmb_mssm_Hhh.txt", output);
    auto bins = cb.bin_set();
    for (auto b : bins) {
      std::cout << "Writing datacard for bin: " << b << std::endl; 
      cb.cp().bin({b}).mass({"*"}).WriteDatacard(
      folder + "/" + b + ".txt", output);
    }



    output.Close();

	cout << "\n>> Done!\n";
}
