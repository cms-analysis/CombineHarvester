#include <string>
// #include "boost/filesystem.hpp"
// #include "boost/regex.hpp"
// #include "boost/format.hpp"
#include "boost/bind.hpp"
// #include "boost/assign/list_of.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
// #include "CombinePdfs/interface/RooHttSMPdf.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
// #include "CombineTools/interface/RooHttYield.h"s
// #include "TH1F.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooGenericPdf.h"

using boost::bind;
using std::string;
using std::vector;
using std::pair;
using std::make_pair;
using std::map;
using std::set;

int main() {
  bool create_asimov = true;
  bool do_parametric = true;
  // bool inject_signal = false;
  string inject_mass = "900";


  TH1::AddDirectory(false);
  ch::CombineHarvester cb;

  vector<pair<int, string>> mt_cats = {
      make_pair(8, "muTau_nobtag"),
      make_pair(9, "muTau_btag")};

  vector<string> masses = {"90",  "100", "120", "130", "140", "160", "180",
                           "200", "250", "300", "350", "400", "450", "500",
                           "600", "700", "800", "900", "1000"};

  std::cout << "Adding observations...";
  cb.AddObservations({"*"}, {"htt"}, {"7TeV", "8TeV"}, {"mt"}, mt_cats);
  std::cout << " done\n";

  std::cout << "Adding background processes...";
  cb.AddProcesses({"*"}, {"htt"}, {"7TeV", "8TeV"}, {"mt"},
                  {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"}, mt_cats, false);
  std::cout << " done\n";

  std::cout << "Adding signal processes...";
  cb.AddProcesses(masses, {"htt"}, {"7TeV", "8TeV"}, {"mt"}, {"ggH"}, {mt_cats[0]},
                  true);
  cb.AddProcesses(masses, {"htt"}, {"7TeV", "8TeV"}, {"mt"}, {"bbH"}, {mt_cats[1]},
                  true);
  std::cout << " done\n";

  std::cout << "Adding systematic uncertainties...";
  ch::AddMSSMSystematics(cb);
  std::cout << " done\n";

  std::cout << "Extracting histograms from input root files...";
  cb.cp().era({"7TeV"}).backgrounds().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-7TeV-0.root", "$CHANNEL/$PROCESS_fine_binning",
      "$CHANNEL/$PROCESS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).backgrounds().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-8TeV-0.root", "$CHANNEL/$PROCESS_fine_binning",
      "$CHANNEL/$PROCESS_$SYSTEMATIC");
  cb.cp().era({"7TeV"}).signals().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-7TeV-0.root", "$CHANNEL/$PROCESS$MASS_fine_binning",
      "$CHANNEL/$PROCESS$MASS_$SYSTEMATIC");
  cb.cp().era({"8TeV"}).signals().ExtractShapes(
      "data/demo/htt_mt.inputs-mssm-8TeV-0.root", "$CHANNEL/$PROCESS$MASS_fine_binning",
      "$CHANNEL/$PROCESS$MASS_$SYSTEMATIC");
  std::cout << " done\n";

  std::cout << "Scaling signal process rates for acceptance...\n";
  for (string e : {"8TeV"}) {
    for (string p : {"ggH", "bbH"}) {
      std::cout << "Scaling for process " << p << " and era " << e << "\n";
      auto gr = ch::TGraphFromTable(
          "input/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt", "mPhi",
          "accept");
      cb.cp().process({p}).era({e}).ForEachProc([&](ch::Process *proc) {
        double m = boost::lexical_cast<double>(proc->mass());
        proc->set_rate(proc->rate() * gr.Eval(m));
      });
    }
  }

  cb.era({"8TeV"});

  std::cout << "Setting standardised bin names...";
  ch::SetStandardBinNames(cb);
  std::cout << " done\n";

  // cb.era({"8TeV"}).bin_id({8});
  set<string> lm_bins = cb.SetFromObs(mem_fn(&ch::Observation::bin));

  if (create_asimov) {
    for (auto const& b : lm_bins) {
      ch::CombineHarvester tmp = std::move(
          cb.cp().bin({b}).backgrounds().syst_type({"shape"}, false));
      TH1F tot_bkg = tmp.GetShape();
      // double bkg_rate = tot_bkg.Integral();
      tot_bkg.Scale(tmp.GetObservedRate()/tot_bkg.Integral());
      // tot_bkg.Add(&sig, 0.0);
      // for (int i = 1; i <= tot_bkg.GetNbinsX(); ++i) {
      //   tot_bkg.SetBinContent(i, std::floor(tot_bkg.GetBinContent(i) + 0.5));
      // }
      tot_bkg.Scale(1.0/tot_bkg.Integral());
      tmp.ForEachObs([&](ch::Observation * obs) {
        obs->set_shape(ch::make_unique<TH1F>(tot_bkg), false);
      });
    }
  }

  ch::CombineHarvester cb_hm = cb;

  cb_hm.ForEachObs([&](ch::Observation* in) {
    in->set_bin(in->bin() + "_hm");
  });
  cb_hm.ForEachProc([&](ch::Process* in) {
    in->set_bin(in->bin() + "_hm");
  });
  cb_hm.ForEachSyst([&](ch::Systematic* in) {
    in->set_bin(in->bin() + "_hm");
  });

  set<string> hm_bins = cb_hm.SetFromObs(mem_fn(&ch::Observation::bin));

  cb.cp().bin_id({8}).VariableRebin(
    {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
      130, 140, 150, 160, 170, 180, 190, 200,225,250,275,300});
  cb.cp().bin_id({9}).VariableRebin(
      {0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300});

  // Drop shape uncerts on signal in the hm for now,
  // the fb versions aren't in the datacards and
  // we want to keep the comparison fair
  cb_hm.FilterSysts([&](ch::Systematic const* p) {
    return p->type() == "shape" && p->signal();
  });

  std::cout << "Doing bbb for the low mass...\n";
  cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
      .MergeBinErrors(0.05, 0.4);
  cb.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
      .AddBinByBin(0.05, true, &cb);
  std::cout << "...done\n";



  if (do_parametric) {
    cb_hm.FilterSysts([&](ch::Systematic const* p) {
      return p->type() == "shape";
    });

    std::vector<double> bins_hm;
    double x = 300.;
    while (x < 1501.) {
      bins_hm.push_back(x);
      x += 5.;
    }
    cb_hm.VariableRebin(bins_hm);
    // cb_hm.PrintAll();

    RooWorkspace ws("htt", "htt");
    for (auto const& b : hm_bins) {
      ch::CombineHarvester tmp = std::move(cb_hm.cp().bin({b}).backgrounds());
      TH1F tot_bkg = tmp.GetShape();
      double bkg_error = 0.;
      double bkg_rate = tot_bkg.IntegralAndError(1, tot_bkg.GetNbinsX(), bkg_error);
      double bkg_uncert = tmp.GetUncertainty();
       // tot_bkg.Integral();
      std::cout << "bkg_rate: " << bkg_rate << "\t" << bkg_error << "\t" << tmp.GetUncertainty() <<  "\n";
      // Here we just play a small trick to reduce the background to one process,
      // ZTT, which we then change to the new bkg pdf
      tmp.process({"ZTT"});
      tmp.ForEachProc([&](ch::Process *proc) {
        proc->set_process("bkg");
        proc->set_rate(1.0);
        proc->set_shape(nullptr, false);
      });


      RooRealVar mtt("CMS_th1x", "CMS_th1x", 0,
                     static_cast<float>(tot_bkg.GetNbinsX()));
      RooRealVar lA((b + "_a").c_str(), "", 50, 0.01, 1000);
      RooRealVar lB((b + "_b").c_str(), "", 50, -10500,
                    10500);
      RooRealVar lC((b + "_c").c_str(), "", 50, 0,
                    10500);
      std::string cond = "(("+b+"_a+"+b+"_b*0.001*CMS_th1x) > 0) * ";
      std::string fn = cond += "exp(-CMS_th1x/("+b+"_a+"+b+"_b*0.001*CMS_th1x))";
      std::cout << "fn = " << fn << std::endl;
      RooGenericPdf bkg_pdf((b + "_bkgpdf").c_str(), fn.c_str(),
                            RooArgList(mtt, lA, lB));
      // RooRealVar bkg_norm((b + "_bkgpdf_norm").c_str(), "", bkg_rate, 0., bkg_rate*10.);
      RooRealVar bkg_norm((b + "_bkgpdf_norm").c_str(), "", bkg_rate);
      tmp.cp().process({"bkg"})
          .AddSyst(cb_hm, "CMS_htt_norm_$BIN", "lnN", ch::syst::SystMap<>::init
          (1.0 + (bkg_uncert/bkg_rate)));
      bkg_norm.setConstant();
      ws.import(bkg_pdf);
      ws.import(bkg_norm);
    }
    cb_hm.process({"ggH", "bbH", "bkg"});

    cb_hm.AddWorkspace(ws);
    cb_hm.cp().backgrounds().ExtractPdfs(cb_hm, "htt", "$CHANNEL_bkgpdf");
    // cb_hm.PrintAll();
  } else {
    cb_hm.cp().bin_id({8}).VariableRebin(
        {300, 325, 350, 400, 500, 700, 1000, 1500});
    cb_hm.cp().bin_id({9}).VariableRebin(
        {300, 350, 400, 500, 700, 1000, 1500});
    std::cout << "Doing bbb for the high mass...\n";
    cb_hm.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
        .MergeBinErrors(0.05, 0.4);
    cb_hm.cp().process({"W", "QCD", "ZTT", "ZL", "ZJ", "TT", "VV"})
        .AddBinByBin(0.05, true, &cb_hm);
    std::cout << "...done\n";
  }

  TFile output("parametric/htt_mt.mssm.root", "RECREATE");
  // cb_hm.cp().mass({"900", "*"}).WriteDatacard("htt_mssm_hm.txt", output);
  for (auto b : hm_bins) {
    for (auto m : masses) {
      std::cout << "Writing datacard for bin: " << b << " and mass: " << m
                << "\n";
      cb_hm.cp().bin({b}).mass({m, "*"}).WriteDatacard("parametric/"+
          b + "_" + m + ".txt", output);
    }
  }
  for (auto b : lm_bins) {
    for (auto m : masses) {
      std::cout << "Writing datacard for bin: " << b << " and mass: " << m
                << "\n";
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard("parametric/"+
          b + "_" + m + ".txt", output);
    }
  }

}
