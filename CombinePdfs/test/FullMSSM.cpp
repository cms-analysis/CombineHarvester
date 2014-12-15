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
using namespace std::placeholders;

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
  RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mA("mA", "mA", 344., 90., 1000.);
  RooRealVar tanb("tanb", "tanb", 9., 1., 60.);

  TFile inputs("out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root");

  // Masses
  TH2F h_mH = ch::OpenFromTFile<TH2F>(&inputs, "h_mH");
  TH2F h_mh = ch::OpenFromTFile<TH2F>(&inputs, "h_mh");
  RooDataHist dh_mH("dh_mH", "dh_mH", RooArgList(mA, tanb),
                    RooFit::Import(h_mH));
  RooDataHist dh_mh("dh_mh", "dh_mh", RooArgList(mA, tanb),
                    RooFit::Import(h_mh));
  RooHistFunc mH("mH", "mH", RooArgList(mA, tanb), dh_mH);
  RooHistFunc mh("mh", "mh", RooArgList(mA, tanb), dh_mh);
  // mH.setInterpolationOrder(1);
  // mh.setInterpolationOrder(1);

  // Cross Sections
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

  // Branching Ratios
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

  vector<pair<int, string>> mt_cats = {
      make_pair(8, "muTau_nobtag"),
      make_pair(9, "muTau_btag")};

  vector<string> masses = {"90",  "100", "120", "130", "140", "160", "180",
                           "200", "250", "300", "350", "400", "450", "500",
                           "600", "700", "800", "900", "1000"};

  cout << "Adding observations...";
  cb.AddObservations({"*"}, {"htt"}, {"7TeV", "8TeV"}, {"mt"}, mt_cats);
  cout << " done\n";

  cout << "Adding background processes...";
  cb.AddProcesses({"*"}, {"htt"}, {"7TeV", "8TeV"}, {"mt"},
                  {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, mt_cats, false);
  cout << " done\n";

  cout << "Adding signal processes...";
  // Here we will declare each Higgs contribution separately
  cb.AddProcesses(masses, {"htt"}, {"7TeV", "8TeV"}, {"mt"},
                  {"ggh", "ggH", "ggA"}, {mt_cats[0]}, true);
  cb.AddProcesses(masses, {"htt"}, {"7TeV", "8TeV"}, {"mt"},
                  {"bbh", "bbH", "bbA"}, {mt_cats[1]}, true);
  cout << " done\n";

  cout << "Adding systematic uncertainties...";
  ch::AddMSSMSystematics(cb);
  cout << " done\n";

  cout << "Extracting histograms from input root files...";
  cb.cp().era({"7TeV"}).backgrounds().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-7TeV-0.root", "$CHANNEL/$PROCESS",
      "$CHANNEL/$PROCESS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).backgrounds().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-8TeV-0.root", "$CHANNEL/$PROCESS",
      "$CHANNEL/$PROCESS_$SYSTEMATIC");
  // We have to map each Higgs signal process to the same histogram, i.e:
  // {ggh, ggH, ggA} --> ggH
  // {bbh, bbH, bbA} --> bbH
  cb.cp().era({"7TeV"}).process({"ggh", "ggH", "ggA"}).ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-7TeV-0.root", "$CHANNEL/ggH$MASS",
      "$CHANNEL/ggH$MASS_$SYSTEMATIC");
  cb.cp().era({"7TeV"}).process({"bbh", "bbH", "bbA"}).ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-7TeV-0.root", "$CHANNEL/bbH$MASS",
      "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).process({"ggh", "ggH", "ggA"}).ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-8TeV-0.root", "$CHANNEL/ggH$MASS",
      "$CHANNEL/ggH$MASS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).process({"bbh", "bbH", "bbA"}).ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-8TeV-0.root", "$CHANNEL/bbH$MASS",
      "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  cout << " done\n";

  cout << "Scaling signal process rates for acceptance...\n";
  map<string, TGraph> xs;
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : {"ggH", "bbH"}) {
      ch::ParseTable(&xs, "data/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt",
                     {p + "_" + e});
    }
  }
  for (string const& e : {"7TeV", "8TeV"}) {
    for (string const& p : {"ggH", "bbH"}) {
      cout << "Scaling for process " << p << " and era " << e << "\n";
      vector<string> p_chain;
      if (p == "ggH") p_chain = {"ggh", "ggH", "ggA"};
      if (p == "bbH") p_chain = {"bbh", "bbH", "bbA"};
      cb.cp().process({p_chain}).era({e}).ForEachProc([&](ch::Process *proc) {
        ch::ScaleProcessRate(proc, &xs, p+"_"+e, "");
      });
    }
  }

  cout << "Setting standardised bin names...";
  cb.ForEachObs(ch::SetStandardBinName<ch::Observation>);
  cb.ForEachProc(ch::SetStandardBinName<ch::Process>);
  cb.ForEachSyst(ch::SetStandardBinName<ch::Systematic>);
  cout << " done\n";

  RooWorkspace ws("htt", "htt");

  bool do_morphing = true;
  string postfix = "_eff_acc";
  if (do_morphing) {
    set<string> bins =
        cb.GenerateSetFromObs<string>(mem_fn(&ch::Observation::bin));
    set<string> procs = {"ggh", "bbh", "ggH", "bbH", "ggA", "bbA"};
    vector<vector<string>> sig_lists;
    sig_lists.push_back({"ggh", "bbh"});
    sig_lists.push_back({"ggH", "bbH"});
    sig_lists.push_back({"ggA", "bbA"});
    vector<RooAbsReal *> m_terms = {&mh, &mH, &mA};
    for (unsigned s = 0; s < sig_lists.size(); ++s) {
      ch::CombineHarvester cb_sig = move(cb.cp().process(sig_lists[s]));
      ch::BuildRooMorphing(ws, cb_sig, *(m_terms[s]), false, postfix);
    }


    cb.FilterSysts([&](ch::Systematic const* p) {
      return p->type() == "shape" && p->signal();
    });
    cb.mass({"120", "*"});
    cb.cp().signals().ForEachProc([&](ch::Process* p) {
      p->set_shape(nullptr, false);
      p->set_rate(1.0);
      p->set_mass("*");
    });
    cb.cp().signals().ForEachSyst([&](ch::Systematic* n) {
      n->set_mass("*");
    });
    cb.cp().signals().ForEachProc([&](ch::Process* p) {
      std::string base_name =
          p->bin() + "_" + p->process() + "_mpdf";
      std::string prod_name = base_name + postfix;
      RooAbsReal *norm =  ws.function(prod_name.c_str());
      RooProduct full_norm((base_name + "_norm").c_str(), "",
                           RooArgList(*norm, *(xs_map[p->process()])));
      ws.import(full_norm, RooFit::RecycleConflictNodes());
    });
    cb.AddWorkspace(&ws);
    cb.cp().signals().ExtractPdfs("htt", "$CHANNEL_$PROCESS_mpdf", &cb);
  }


  // cout << "Adding bbb...\n";
  // cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
  //     .MergeBinErrors(0.05, 0.4);
  // cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
  //     .AddBinByBin(0.05, true, &cb);
  // cout << "...done\n";

  ch::CombineHarvester gg_plot = std::move(cb.cp().era({"8TeV"}).bin_id({8}));
  ch::CombineHarvester bb_plot = std::move(cb.cp().era({"8TeV"}).bin_id({9}));
  TH1F gg_dat = gg_plot.GetObservedShape();
  TH1F bb_dat = bb_plot.GetObservedShape();
  TH1F ggh = RestoreBinning(gg_plot.cp().process({"ggh"}).GetShape(), gg_dat);
  TH1F ggH = RestoreBinning(gg_plot.cp().process({"ggH"}).GetShape(), gg_dat);
  TH1F ggA = RestoreBinning(gg_plot.cp().process({"ggA"}).GetShape(), gg_dat);
  TH1F ggX = RestoreBinning(gg_plot.cp().process({"ggh", "ggH", "ggA"}).GetShape(), gg_dat);
  TH1F bbh = RestoreBinning(bb_plot.cp().process({"bbh"}).GetShape(), bb_dat);
  TH1F bbH = RestoreBinning(bb_plot.cp().process({"bbH"}).GetShape(), bb_dat);
  TH1F bbA = RestoreBinning(bb_plot.cp().process({"bbA"}).GetShape(), bb_dat);
  TH1F bbX = RestoreBinning(bb_plot.cp().process({"bbh", "bbH", "bbA"}).GetShape(), bb_dat);

  // cb.PrintAll();
  TFile output("htt_mt.input.mssm.root", "RECREATE");
  ggh.Write("ggh");
  ggH.Write("ggH");
  ggA.Write("ggA");
  ggX.Write("ggX");
  bbh.Write("bbh");
  bbH.Write("bbH");
  bbA.Write("bbA");
  bbX.Write("bbX");
  cb.cp().mass({"*"}).WriteDatacard("htt_mt_mssm.txt", output);
  output.Close();
}


