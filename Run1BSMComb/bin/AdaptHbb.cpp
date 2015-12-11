#include <string>
#include <vector>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char* argv[]) {
  std::string mass = "mA";
  po::variables_map vm;
  po::options_description config("configuration");
  bool single_resonance = false;
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("single,s", po::value<bool>(&single_resonance)->implicit_value(true));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  // We will need to source some inputs from the "auxiliaries" repo
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_cards   = "Hbb";

  auto masses = ch::MassesFromRange("100,140,160");

  // RooFit will be quite noisy if we don't set this
  // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mA(mass.c_str(), mass.c_str(), 100., 500.);
  RooRealVar mH("mH", "mH", 100., 500.);
  RooRealVar mh("mh", "mh", 100., 500.);

  TH1::AddDirectory(false);
  ch::CombineHarvester cb;
  for (auto m : masses) {
    cb.ParseDatacard(
        aux_cards + "/Comb_7TeV_HIG14017_HighMass2012_Packed_M"+m+"_card_theoryUnc.txt", "hbb",
        "", "hbb", 0, m);
  }


  // Rename categories and harmonize signal process names
  // ch1 --> inclusive (8 TeV)
  // ch2 --> semileptonic (7 TeV)
  // ch3 --> hadronic (7 TeV)
  // In the 7TeV the analysis is split into low mass (100, 120, 160) and
  // high mass (200,300,250) event selections
  cb.ForEachObj([](ch::Object *obj) {
    double m = boost::lexical_cast<double>(obj->mass());
    if (obj->bin() == "ch1" || obj->bin() == "bbHTo4b") { // it's bbHTo4b if we take the 8 TeV only cards
      obj->set_bin("hbb_inclusive_8TeV");
      obj->set_era("8TeV");
    } else if (obj->bin() == "ch2" && m < 180.) {
      obj->set_bin("hbb_semilept_low_7TeV");
      obj->set_era("7TeV");
    } else if (obj->bin() == "ch2" && m > 180.) {
      obj->set_bin("hbb_semilept_high_7TeV");
      obj->set_era("7TeV");
    } else if (obj->bin() == "ch3" && m < 180.) {
      obj->set_bin("hbb_hadronic_low_7TeV");
      obj->set_era("7TeV");
    } else if (obj->bin() == "ch3" && m > 180.) {
      obj->set_bin("hbb_hadronic_high_7TeV");
      obj->set_era("7TeV");
    }
    if (obj->process() == "sgnBBB" || obj->process() == "bbH") {
      obj->set_process("bbA_Abb");
    }
  });
  
  for (auto const& bin : cb.bin_set()) {
    auto bin_masses = cb.cp().bin({bin}).mass_set();
    if (bin_masses.size() == 0) continue;
    auto collapse = *(bin_masses.begin());
    std::cout << "Collapse procs in bin " << bin << " to mass point " << collapse << "\n";
    cb.FilterAll([&](ch::Object *obj) {
      return (obj->bin() == bin && !obj->signal() && obj->mass() != collapse);
    });
    cb.cp().bin({bin}).ForEachObj([&](ch::Object *obj) {
      if (!obj->signal()) obj->set_mass("*");
    });
  }

  // Unscale the signal cross sections
  TFile model_file(TString(auxiliaries) +
               "models/out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root");
  TH2F *h_xs_bbA = (TH2F*)(gDirectory->Get("h_bbH_xsec_A")->Clone());
  TH2F *h_xs_bbH = (TH2F*)(gDirectory->Get("h_bbH_xsec_H")->Clone());
  TH2F *h_xs_bbh = (TH2F*)(gDirectory->Get("h_bbH_xsec_h")->Clone());
  TH2F *h_br_Abb = (TH2F*)(gDirectory->Get("h_brbb_A")->Clone());
  TH2F *h_br_Hbb = (TH2F*)(gDirectory->Get("h_brbb_H")->Clone());
  TH2F *h_br_hbb = (TH2F*)(gDirectory->Get("h_brbb_h")->Clone());
  double fixed_tanb = 30.;

  cb.cp().signals().ForEachProc([&](ch::Process *p) {
    double m = boost::lexical_cast<double>(p->mass());
    double tot = h_xs_bbA->GetBinContent(h_xs_bbA->FindBin(m, fixed_tanb)) *
                 h_br_Abb->GetBinContent(h_br_Abb->FindBin(m, fixed_tanb));
    if (m < 125.) {
      tot += h_xs_bbh->GetBinContent(h_xs_bbh->FindBin(m, fixed_tanb)) *
             h_br_hbb->GetBinContent(h_br_hbb->FindBin(m, fixed_tanb));
    } else if (m < 135.) {
      tot += h_xs_bbh->GetBinContent(h_xs_bbh->FindBin(m, fixed_tanb)) *
             h_br_hbb->GetBinContent(h_br_hbb->FindBin(m, fixed_tanb));
      tot += h_xs_bbH->GetBinContent(h_xs_bbH->FindBin(m, fixed_tanb)) *
             h_br_Hbb->GetBinContent(h_br_Hbb->FindBin(m, fixed_tanb));
    } else {
      tot += h_xs_bbH->GetBinContent(h_xs_bbH->FindBin(m, fixed_tanb)) *
             h_br_Hbb->GetBinContent(h_br_Hbb->FindBin(m, fixed_tanb));
    }
    p->set_rate(p->rate() / tot);
  });

  // Drop signal theory uncertainties
  cb.syst_name({"QCDscale", "pdf_gg", "QCD_scale", "PDF"}, false);

  // Now clone signal procs to create the H and the h
  ch::CloneProcsAndSysts(cb.cp().process({"bbA_Abb"}), cb, [](ch::Object *p) {
    p->set_process("bbH_Hbb");
  });
  ch::CloneProcsAndSysts(cb.cp().process({"bbA_Abb"}), cb, [](ch::Object *p) {
    p->set_process("bbh_hbb");
  });

  RooWorkspace ws("hbb", "hbb");
  TFile debug("hbb_morphing_debug.root", "RECREATE");

  map<string, RooAbsReal *> mass_var = {
    {"bbh_hbb", &mh}, {"bbH_Hbb", &mH}, {"bbA_Abb", &mA}
  };

  // If we're only doing a one-bump search we will just drop the other signal
  // processes we created
  if (single_resonance) {
    cb.process({"bbh_hbb", "bbH_Hbb"}, false);
  }

  ch::CardWriter writer("$TAG/$MASS/$BIN.txt", "$TAG/common/$BIN.input.root");
  writer.WriteCards("output/hbb", cb);


  bool do_morphing = true;
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).signals().process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, *(mass_var.at(p)),
                             "norm", false, true, false, &debug);
      }
    }
  }
  debug.Close();
  cb.AddWorkspace(ws);
  cb.cp().signals().ExtractPdfs(cb, "hbb", "$BIN_$PROCESS_morph");


  cb.PrintAll();

  ch::CardWriter writer2("$TAG/morphed/$BIN.txt", "$TAG/common/hbb.input.root");
  writer2.SetVerbosity(1);
  writer2.SetWildcardMasses({});
  writer2.WriteCards("output/hbb", cb);
}


