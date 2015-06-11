#include <string>
#include <map>
#include <vector>
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Utilities.h"
#include "CombineTools/interface/TFileIO.h"
#include "CombineTools/interface/HttSystematics.h"
#include "CombinePdfs/interface/MorphFunctions.h"

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
  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  // We will need to source some inputs from the "auxiliaries" repo
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_shapes   = auxiliaries +"shapes/";

  // RooFit will be quite noisy if we don't set this
  RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  // In the first part of this code we will construct our MSSM signal model.
  // This means declaring mA and tanb as our free parameters, and defining all
  // other Higgs masses, cross sections and branching ratios as a function of
  // these. Note that this example is very verbose and explicit in the
  // construction - one could imagine developing a more generic and efficient
  // tool to do this.

  // Define mA and tanb as RooRealVars
  // Here we fix the valid ranges of these parameters and set their starting
  // values
  RooRealVar mA("mA", "mA", 344., 90., 1000.);
  RooRealVar tanb("tanb", "tanb", 9., 1., 60.);

  // All the other inputs we need to build the model can be found in one of the
  // LHCXSWG scans. Here we use the classic mhmax scenario. This file contains a
  // large number of 2D histograms, all binned in mA and tanb, that each provide
  // a different mass, xsec or BR.
  TFile inputs(TString(auxiliaries) +
               "models/out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root");

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
  // mh.setInterpolationOrder(1);

  // Now we'll do the same for the gluon-fusion cross sections (one TH2F for
  // each Higgs boson)
  TH2F h_ggF_xsec_h = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_h");
  TH2F h_ggF_xsec_H = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_H");
  TH2F h_ggF_xsec_A = ch::OpenFromTFile<TH2F>(&inputs, "h_ggF_xsec_A");
  RooDataHist dh_ggF_xsec_h("dh_ggF_xsec_h", "dh_ggF_xsec_h",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_h));
  RooDataHist dh_ggF_xsec_H("dh_ggF_xsec_H", "dh_ggF_xsec_H",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_H));
  RooDataHist dh_ggF_xsec_A("dh_ggF_xsec_A", "dh_ggF_xsec_A",
                            RooArgList(mA, tanb), RooFit::Import(h_ggF_xsec_A));
  RooHistFunc ggF_xsec_h("ggF_xsec_h", "ggF_xsec_h", RooArgList(mA, tanb),
                         dh_ggF_xsec_h);
  RooHistFunc ggF_xsec_H("ggF_xsec_H", "ggF_xsec_H", RooArgList(mA, tanb),
                         dh_ggF_xsec_H);
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

  // Now the branching ratios to tau tau
  TH2F h_brtautau_h = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_h");
  TH2F h_brtautau_H = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_H");
  TH2F h_brtautau_A = ch::OpenFromTFile<TH2F>(&inputs, "h_brtautau_A");
  RooDataHist dh_brtautau_h("dh_brtautau_h", "dh_brtautau_h",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_h));
  RooDataHist dh_brtautau_H("dh_brtautau_H", "dh_brtautau_H",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_H));
  RooDataHist dh_brtautau_A("dh_brtautau_A", "dh_brtautau_A",
                            RooArgList(mA, tanb),
                            RooFit::Import(h_brtautau_A));
  RooHistFunc brtautau_h("brtautau_h", "brtautau_h", RooArgList(mA, tanb),
                         dh_brtautau_h);
  RooHistFunc brtautau_H("brtautau_H", "brtautau_H", RooArgList(mA, tanb),
                         dh_brtautau_H);
  RooHistFunc brtautau_A("brtautau_A", "brtautau_A", RooArgList(mA, tanb),
                         dh_brtautau_A);

  // We can build the xsec * BR products
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
  cout << "mh: " << mh.getVal() << "\n\n";
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
  xs_map["ggh"] = &ggF_xsec_br_h;
  xs_map["ggH"] = &ggF_xsec_br_H;
  xs_map["ggA"] = &ggF_xsec_br_A;
  xs_map["bbh"] = &bbH_xsec_br_h;
  xs_map["bbH"] = &bbH_xsec_br_H;
  xs_map["bbA"] = &bbH_xsec_br_A;

  TH1::AddDirectory(false);
  ch::CombineHarvester cb;

  Categories mt_cats = {
      make_pair(8, "muTau_nobtag"),
      make_pair(9, "muTau_btag")};

  auto masses = ch::MassesFromRange(
      "90,100,120-140:10,140-200:20,200-500:50,600-1000:100");

  cout << "Adding observations...";
  cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {"mt"}, mt_cats);
  cout << " done\n";

  cout << "Adding background processes...";
  cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {"mt"},
                  {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, mt_cats, false);
  cout << " done\n";

  cout << "Adding signal processes...";
  // Unlike in previous MSSM H->tautau analyses we will create a separate
  // process for each Higgs in the datacards
  map<string, VString> signal_types = {
    {"ggH", {"ggh", "ggH", "ggA"}},
    {"bbH", {"bbh", "bbH", "bbA"}}
  };
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["ggH"], {mt_cats[0]}, true);
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"},
                  signal_types["bbH"], {mt_cats[1]}, true);
  cout << " done\n";

  cout << "Adding systematic uncertainties...";
  ch::AddMSSMSystematics(cb);
  cout << " done\n";

  string file = aux_shapes + "Imperial/htt_mt.inputs-mssm-8TeV-0.root";

  cout << "Extracting histograms from input root files...";
  cb.cp().era({"8TeV"}).backgrounds().ExtractShapes(
      file, "$CHANNEL/$PROCESS", "$CHANNEL/$PROCESS_$SYSTEMATIC");

  // We have to map each Higgs signal process to the same histogram, i.e:
  // {ggh, ggH, ggA} --> ggH
  // {bbh, bbH, bbA} --> bbH
  cb.cp().era({"8TeV"}).process(signal_types["ggH"]).ExtractShapes(
      file, "$CHANNEL/ggH$MASS",
      "$CHANNEL/ggH$MASS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).process(signal_types["bbH"]).ExtractShapes(
      file, "$CHANNEL/bbH$MASS",
      "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  cout << " done\n";

  cout << "Scaling signal process rates for acceptance...\n";
  for (string e : {"8TeV"}) {
    for (string p : {"ggH", "bbH"}) {
      cout << "Scaling for process " << p << " and era " << e << "\n";
      auto gr = ch::TGraphFromTable(
          "input/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt", "mPhi",
          "accept");
      cb.cp().process(signal_types[p]).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * gr.Eval(m));
      });
    }
  }

  cout << "Setting standardised bin names...";
  ch::SetStandardBinNames(cb);
  cout << " done\n";

  RooWorkspace ws("htt", "htt");

  TFile demo("htt_mt_mssm_demo.root", "RECREATE");

  bool do_morphing = true;
  string postfix = "_eff_acc";
  map<string, RooAbsReal *> mass_var = {
    {"ggh", &mh}, {"ggH", &mH}, {"ggA", &mA},
    {"bbh", &mh}, {"bbH", &mH}, {"bbA", &mA}
  };
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).signals().process_set();
      for (auto p : procs) {
        string pdf_name = b + "_" + p + "_morph";
        ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]), "90", "1000",
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

  // cout << "Adding bbb...\n";
  // cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
  //     .MergeBinErrors(0.05, 0.4);
  // cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
  //     .AddBinByBin(0.05, true, &cb);
  // cout << "...done\n";

  // ch::CombineHarvester gg_plot = std::move(cb.cp().era({"8TeV"}).bin_id({8}));
  // ch::CombineHarvester bb_plot = std::move(cb.cp().era({"8TeV"}).bin_id({9}));
  // TH1F gg_dat = gg_plot.GetObservedShape();
  // TH1F bb_dat = bb_plot.GetObservedShape();
  // TH1F ggh = RestoreBinning(gg_plot.cp().process({"ggh"}).GetShape(), gg_dat);
  // TH1F ggH = RestoreBinning(gg_plot.cp().process({"ggH"}).GetShape(), gg_dat);
  // TH1F ggA = RestoreBinning(gg_plot.cp().process({"ggA"}).GetShape(), gg_dat);
  // TH1F ggX = RestoreBinning(gg_plot.cp().process({"ggh", "ggH", "ggA"}).GetShape(), gg_dat);
  // TH1F bbh = RestoreBinning(bb_plot.cp().process({"bbh"}).GetShape(), bb_dat);
  // TH1F bbH = RestoreBinning(bb_plot.cp().process({"bbH"}).GetShape(), bb_dat);
  // TH1F bbA = RestoreBinning(bb_plot.cp().process({"bbA"}).GetShape(), bb_dat);
  // TH1F bbX = RestoreBinning(bb_plot.cp().process({"bbh", "bbH", "bbA"}).GetShape(), bb_dat);

  string folder = "output/mssm_test";
  boost::filesystem::create_directories(folder);


  TFile output((folder + "/htt_mt.input.mssm.root").c_str(), "RECREATE");
  // ggh.Write("ggh");
  // ggH.Write("ggH");
  // ggA.Write("ggA");
  // ggX.Write("ggX");
  // bbh.Write("bbh");
  // bbH.Write("bbH");
  // bbA.Write("bbA");
  // bbX.Write("bbX");
  cb.cp().mass({"*"}).WriteDatacard(folder + "/htt_mt_mssm.txt", output);
  output.Close();
}


