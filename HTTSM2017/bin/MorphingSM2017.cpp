#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/Algorithm.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"
#include "TF1.h"
#include "TH2.h"
#include "boost/algorithm/string/predicate.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/program_options.hpp"
#include "boost/regex.hpp"
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <utility>
#include <vector>
#include <math.h>

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char **argv) {
  typedef vector<string> VString;
  typedef vector<pair<int, string>> Categories;
  using ch::syst::bin_id;
  using ch::JoinStr;

  // Define program options
  string output_folder = "sm_run2";
  string base_path = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSM2017/shapes";
  string input_folder_em = "Vienna/";
  string input_folder_et = "Vienna/";
  string input_folder_mt = "Vienna/";
  string input_folder_tt = "Vienna/";
  string chan = "all";
  string postfix = "-ML";
  bool regional_jec = true;
  bool ggh_wg1 = true;
  bool auto_rebin = false;
  bool real_data = false;
  bool jetfakes = true;
  bool embedding = false;
  bool classic_bbb = false;
  bool binomial_bbb = false;
  bool verbose = false;
  string stxs_signals = "stxs_stage0"; // "stxs_stage0" or "stxs_stage1"
  string categories = "stxs_stage0"; // "stxs_stage0", "stxs_stage1" or "gof"
  string gof_category_name = "gof";
  int era = 2016; // 2016 or 2017
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
      ("base_path", po::value<string>(&base_path)->default_value(base_path))
      ("input_folder_em", po::value<string>(&input_folder_em)->default_value(input_folder_em))
      ("input_folder_et", po::value<string>(&input_folder_et)->default_value(input_folder_et))
      ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value(input_folder_mt))
      ("input_folder_tt", po::value<string>(&input_folder_tt)->default_value(input_folder_tt))
      ("postfix", po::value<string>(&postfix)->default_value(postfix))
      ("channel", po::value<string>(&chan)->default_value(chan))
      ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(auto_rebin))
      ("regional_jec", po::value<bool>(&regional_jec)->default_value(regional_jec))
      ("ggh_wg1", po::value<bool>(&ggh_wg1)->default_value(ggh_wg1))
      ("real_data", po::value<bool>(&real_data)->default_value(real_data))
      ("verbose", po::value<bool>(&verbose)->default_value(verbose))
      ("output_folder", po::value<string>(&output_folder)->default_value(output_folder))
      ("stxs_signals", po::value<string>(&stxs_signals)->default_value(stxs_signals))
      ("categories", po::value<string>(&categories)->default_value(categories))
      ("gof_category_name", po::value<string>(&gof_category_name)->default_value(gof_category_name))
      ("jetfakes", po::value<bool>(&jetfakes)->default_value(jetfakes))
      ("embedding", po::value<bool>(&embedding)->default_value(embedding))
      ("classic_bbb", po::value<bool>(&classic_bbb)->default_value(classic_bbb))
      ("binomial_bbb", po::value<bool>(&binomial_bbb)->default_value(binomial_bbb))
      ("era", po::value<int>(&era)->default_value(era));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  // Define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  std::map<string, string> input_dir;
  input_dir["mt"] = base_path + "/" + input_folder_mt + "/";
  input_dir["et"] = base_path + "/" + input_folder_et + "/";
  input_dir["tt"] = base_path + "/" + input_folder_tt + "/";
  input_dir["em"] = base_path + "/" + input_folder_em + "/";

  // Define channels
  VString chns;
  if (chan.find("mt") != std::string::npos)
    chns.push_back("mt");
  if (chan.find("et") != std::string::npos)
    chns.push_back("et");
  if (chan.find("tt") != std::string::npos)
    chns.push_back("tt");
  if (chan.find("em") != std::string::npos)
    chns.push_back("em");
  if (chan == "all")
    chns = {"mt", "et", "tt", "em"};

  // Define background processes
  map<string, VString> bkg_procs;
  VString bkgs, bkgs_em;
  bkgs = {"W", "ZTT", "QCD", "ZL", "ZJ", "TTT", "TTL", "TTJ", "VVJ", "VVT", "VVL", "WH125", "ZH125", "ttH125"};
  bkgs_em = {"W", "ZTT", "QCD", "ZL", "TT", "VV", "ST", "WH125", "ZH125", "ttH125","ggHWW125","qqHWW125"};
  if(embedding){
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "ZTT"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "TTT"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "VVT"), bkgs.end());
    bkgs = JoinStr({bkgs,{"EMB"}});
    bkgs_em.erase(std::remove(bkgs_em.begin(), bkgs_em.end(), "ZTT"), bkgs_em.end());
    bkgs_em = JoinStr({bkgs_em,{"EMB"}});
  }
  if(jetfakes){
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "QCD"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "W"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "VVJ"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "TTJ"), bkgs.end());
    bkgs.erase(std::remove(bkgs.begin(), bkgs.end(), "ZJ"), bkgs.end());
    bkgs = JoinStr({bkgs,{"jetFakes"}});
  }

  std::cout << "[INFO] Considerung the following processes:\n";
  if (chan.find("em") != std::string::npos) {
    std::cout << "For em channel : \n";
    for (unsigned int i=0; i < bkgs_em.size(); i++) std::cout << bkgs_em[i] << std::endl;
  }
  if (chan.find("mt") != std::string::npos || chan.find("et") != std::string::npos || chan.find("tt") != std::string::npos) {
    std::cout << "For et,mt,tt channels : \n";
    for (unsigned int i=0; i < bkgs.size(); i++) std::cout << bkgs[i] << std::endl;
  }
  bkg_procs["et"] = bkgs;
  bkg_procs["mt"] = bkgs;
  bkg_procs["tt"] = bkgs;
  bkg_procs["em"] = bkgs_em;

  // Define categories
  map<string, Categories> cats;
  // STXS stage 0 categories (optimized on ggH and VBF)
  if(categories == "stxs_stage0"){
    cats["et"] = {
        { 1, "et_ggh"},
        { 2, "et_qqh"},
        {11, "et_w"},
        {12, "et_ztt"},
        {13, "et_tt"},
        {14, "et_ss"},
        {15, "et_zll"},
        {16, "et_misc"},
    };
     cats["mt"] = {
        { 1, "mt_ggh"},
        { 2, "mt_qqh"},
        {11, "mt_w"},
        {12, "mt_ztt"},
        {13, "mt_tt"},
        {14, "mt_ss"},
        {15, "mt_zll"},
        {16, "mt_misc"},
    };
     cats["tt"] = {
        { 1, "tt_ggh"},
        { 2, "tt_qqh"},
        {12, "tt_ztt"},
        {16, "tt_misc"},
        {17, "tt_noniso"},
    };
     cats["em"] = {
        { 1, "em_ggh"},
        { 2, "em_qqh"},
        {12, "em_ztt"},
        {13, "em_tt"},
        {14, "em_ss"},
        {16, "em_misc"},
        {18, "em_st"},
        {19, "em_vv"},
    };
  }
  // STXS stage 1 categories (optimized on STXS stage 1 splits of ggH and VBF)
  else if(categories == "stxs_stage1"){
    cats["et"] = {
        { 1, "et_ggh_unrolled"},
        { 2, "et_qqh_unrolled"},
        {11, "et_w"},
        {12, "et_ztt"},
        {13, "et_tt"},
        {14, "et_ss"},
        {15, "et_zll"},
        {16, "et_misc"},
    };
     cats["mt"] = {
        { 1, "mt_ggh_unrolled"},
        { 2, "mt_qqh_unrolled"},
        {11, "mt_w"},
        {12, "mt_ztt"},
        {13, "mt_tt"},
        {14, "mt_ss"},
        {15, "mt_zll"},
        {16, "mt_misc"},
    };
     cats["tt"] = {
        { 1, "tt_ggh_unrolled"},
        { 2, "tt_qqh_unrolled"},
        {12, "tt_ztt"},
        {16, "tt_misc"},
        {17, "tt_noniso"},
    };
     cats["em"] = {
        { 1, "em_ggh_unrolled"},
        { 2, "em_qqh_unrolled"},
        {12, "em_ztt"},
        {13, "em_tt"},
        {14, "em_ss"},
        {16, "em_misc"},
        {18, "em_st"},
        {19, "em_vv"},
    };
  }
  else if(categories == "gof"){
    cats["et"] = {
        { 100, gof_category_name.c_str() },
    };
    cats["mt"] = {
        { 100, gof_category_name.c_str() },
    };
    cats["tt"] = {
        { 100, gof_category_name.c_str() },
    };
    cats["em"] = {
        { 100, gof_category_name.c_str() },
    };
  }
  else throw std::runtime_error("Given categorization is not known.");

  // Specify signal processes and masses
  vector<string> sig_procs;
  // STXS stage 0: ggH and VBF processes
  if(stxs_signals == "stxs_stage0") sig_procs = {"ggH", "qqH"};
  // STXS stage 1: Splits of ggH and VBF processes
  // References:
  // - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGFiducialAndSTXS
  // - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWG2
  else if(stxs_signals == "stxs_stage1") sig_procs = {
      // ggH
      "ggH_0J", "ggH_1J_PTH_0_60", "ggH_1J_PTH_60_120", "ggH_1J_PTH_120_200",
      "ggH_1J_PTH_GT200", "ggH_GE2J_PTH_0_60", "ggH_GE2J_PTH_60_120",
      "ggH_GE2J_PTH_120_200", "ggH_GE2J_PTH_GT200", "ggH_VBFTOPO_JET3VETO",
      "ggH_VBFTOPO_JET3",
      // VBF
      "qqH_VBFTOPO_JET3VETO", "qqH_VBFTOPO_JET3", "qqH_REST",
      "qqH_PTJET1_GT200", "qqH_VH2JET"};
  else throw std::runtime_error("Given STXS signals are not known.");
  vector<string> masses = {"125"};

  // Create combine harverster object
  ch::CombineHarvester cb;

  // Add observations and processes
  std::string era_tag;
  if (era == 2016) era_tag = "Run2016";
  else if (era == 2017) era_tag = "Run2017";
  else std::runtime_error("Given era is not implemented.");

  for (auto chn : chns) {
    cb.AddObservations({"*"}, {"htt"}, {era_tag}, {chn}, cats[chn]);
    cb.AddProcesses({"*"}, {"htt"}, {era_tag}, {chn}, bkg_procs[chn], cats[chn],
                    false);
    cb.AddProcesses(masses, {"htt"}, {era_tag}, {chn}, sig_procs, cats[chn],
                    true);
  }

  // Add systematics
  ch::AddSMRun2Systematics(cb, jetfakes, embedding, regional_jec, ggh_wg1, era);

  // Extract shapes from input ROOT files
  for (string chn : chns) {
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
        input_dir[chn] + "htt_" + chn + ".inputs-sm-" + era_tag + postfix + ".root",
        "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
        input_dir[chn] + "htt_" + chn + ".inputs-sm-" + era_tag + postfix + ".root",
        "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  }

  // Delete processes with 0 yield
  cb.FilterProcs([&](ch::Process *p) {
    bool null_yield = !(p->rate() > 0.0);
    if (null_yield) {
      std::cout << "[WARNING] Removing process with null yield: \n ";
      std::cout << ch::Process::PrintHeader << *p << "\n";
      cb.FilterSysts([&](ch::Systematic *s) {
        bool remove_syst = (MatchingProcess(*p, *s));
        return remove_syst;
      });
    }
    return null_yield;
  });

  // Delete systematics with 0 yield since these result in a bogus norm error in combine
  cb.FilterSysts([&](ch::Systematic *s) {
    if (s->type() == "shape") {
      if (s->shape_u()->Integral() == 0.0) {
        std::cout << "[WARNING] Removing systematic with null yield in up shift:" << std::endl;
        std::cout << ch::Systematic::PrintHeader << *s << "\n";
        return true;
      }
      if (s->shape_d()->Integral() == 0.0) {
        std::cout << "[WARNING] Removing systematic with null yield in down shift:" << std::endl;
        std::cout << ch::Systematic::PrintHeader << *s << "\n";
        return true;
      }
    }
    return false;
  });
  
  int count_lnN = 0;
  int count_all = 0;
  cb.cp().ForEachSyst([&count_lnN, &count_all](ch::Systematic *s) {
    if (TString(s->name()).Contains("scale")||TString(s->name()).Contains("CMS_htt_boson_reso_met")){
      count_all++;
      double err_u = 0.0;
      double err_d = 0.0;
      int nbins = s->shape_u()->GetNbinsX();
      double yield_u = s->shape_u()->IntegralAndError(1,nbins,err_u);
      double yield_d = s->shape_d()->IntegralAndError(1,nbins,err_d);
      double value_u = s->value_u();
      double value_d = s->value_d();
      if (std::abs(value_u-1.0)+std::abs(value_d-1.0)<err_u/yield_u+err_d/yield_d){
          count_lnN++;
          std::cout << "[WARNING] Replacing systematic by lnN:" << std::endl;
          std::cout << ch::Systematic::PrintHeader << *s << "\n";
          s->set_type("lnN");
          bool up_is_larger = (value_u>value_d);
          if (value_u < 1.0) value_u = 1.0 / value_u;
          if (value_d < 1.0) value_d = 1.0 / value_d;
          if (up_is_larger){
              value_u = std::sqrt(value_u*value_d);
              value_d = 1.0 / value_u;
          }else{
              value_d = std::sqrt(value_u*value_d);
              value_u = 1.0 / value_d;
          }
          std::cout << "Former relative integral up shift: " << s->value_u() << "; New relative integral up shift: " << value_u << std::endl;
          std::cout << "Former relative integral down shift: " << s->value_d() << "; New relative integral down shift: " << value_d << std::endl;
          s->set_value_u(value_u);
          s->set_value_d(value_d);
      }
    }
  });
  std::cout << "[WARNING] Turned " << count_lnN << " of " << count_all << " checked systematics into lnN:" << std::endl;

  // Replacing observation with the sum of the backgrounds (Asimov data)
  // useful to be able to check this, so don't do the replacement
  // for these
  if (!real_data) {
    for (auto b : cb.cp().bin_set()) {
      std::cout << "[INFO] Replacing data with asimov in bin " << b << "\n";
      cb.cp().bin({b}).ForEachObs([&](ch::Observation *obs) {
        obs->set_shape(cb.cp().bin({b}).backgrounds().GetShape() +
                           cb.cp().bin({b}).signals().GetShape(),
                       true);
      });
    }
  }

  // Rebin categories to predefined binning

  // Rebin background categories
  for (auto b : cb.cp().bin_set()) {
    TString bstr = b;
    if (bstr.Contains("unrolled")) continue;
    std::cout << "[INFO] Rebin background bin " << b << "\n";
    auto shape = cb.cp().bin({b}).backgrounds().GetShape();
    auto min = shape.GetBinLowEdge(1);
    cb.cp().bin({b}).VariableRebin({min, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0});
  }
  // Rebin ggh categories
  for (auto b : cb.cp().bin_set()) {
    TString bstr = b;
    if (bstr.Contains("ggh_unrolled")) {
      std::cout << "[INFO] Rebin ggh signal bin " << b << "\n";
      auto shape = cb.cp().bin({b}).backgrounds().GetShape();
      auto min = shape.GetBinLowEdge(1);
      auto range = 1.0 - min;
      vector<double> raw_binning = {0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 1.0};
      vector<double> binning = {min};
      int n_stage1cats = 9;
      if (bstr.Contains("et_")||bstr.Contains("mt_")) n_stage1cats = 7;
      for (int i=0; i<n_stage1cats; i++){
        for (auto border : raw_binning) {
          binning.push_back(i*range+border);
        }
      }
      cb.cp().bin({b}).VariableRebin(binning);
    }
  }
  // Rebin qqh categories
  for (auto b : cb.cp().bin_set()) {
    TString bstr = b;
    if (bstr.Contains("qqh_unrolled")) {
      std::cout << "[INFO] Rebin qqh signal bin " << b << "\n";
      auto shape = cb.cp().bin({b}).backgrounds().GetShape();
      auto min = shape.GetBinLowEdge(1);
      auto range = 1.0 - min;
      vector<double> raw_binning = {0.4, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95, 1.0};
      vector<double> binning = {min};
      for (int i=0; i<5; i++){
        for (auto border : raw_binning) {
          binning.push_back(i*range+border);
        }
      }
      cb.cp().bin({b}).VariableRebin(binning);
    }
  }

  // At this point we can fix the negative bins
  std::cout << "[INFO] Fixing negative bins.\n";
  cb.ForEachProc([](ch::Process *p) {
    if (ch::HasNegativeBins(p->shape())) {
      auto newhist = p->ClonedShape();
      ch::ZeroNegativeBins(newhist.get());
      p->set_shape(std::move(newhist), false);
    }
  });

  cb.ForEachSyst([](ch::Systematic *s) {
    if (s->type().find("shape") == std::string::npos)
      return;
    if (ch::HasNegativeBins(s->shape_u()) ||
        ch::HasNegativeBins(s->shape_d())) {
      auto newhist_u = s->ClonedShapeU();
      auto newhist_d = s->ClonedShapeD();
      ch::ZeroNegativeBins(newhist_u.get());
      ch::ZeroNegativeBins(newhist_d.get());
      s->set_shapes(std::move(newhist_u), std::move(newhist_d), nullptr);
    }
  });

  // Perform auto-rebinning
  if (auto_rebin) {
    const auto threshold = 1.0;
    const auto tolerance = 1e-4;
    for (auto b : cb.cp().bin_set()) {
      std::cout << "[INFO] Rebin bin " << b << "\n";
      // Get shape of this category with sum of backgrounds
      auto shape = cb.cp().bin({b}).backgrounds().GetShape();
      // Push back last bin edge
      vector<double> binning;
      const auto num_bins = shape.GetNbinsX();
      binning.push_back(shape.GetBinLowEdge(num_bins + 1));
      // Now, go backwards through bins (from right to left) and merge a bin if
      // the background yield is below a given threshold.
      auto offset = shape.GetBinLowEdge(1);
      auto width = 1.0 - offset;
      auto c = 0.0;
      for(auto i = num_bins; i > 0; i--) {
        // Determine whether this is a boundary of an unrolled category
        // if it's a multiple of the width between minimum NN score and 1.0.
        auto low_edge = shape.GetBinLowEdge(i);
        auto is_boundary = fabs(fmod(low_edge - offset, width)) < tolerance ? true : false;
        c += shape.GetBinContent(i);
        if (is_boundary) { // If the lower edge is a boundary, set a bin edge.
          if (c <= threshold && !(fabs(fmod(binning[0] - offset, width)) < tolerance || fabs(fmod(binning[0] - offset, width)) - width < tolerance)) { // Special case: If this bin is at a boundary but it is below the threshold and the bin above is not again a boundary, merge to the right.
            binning.erase(binning.begin());
          }
          binning.insert(binning.begin(), low_edge);
          c = 0.0;
        } else { // If this is not a boundary, check whether the content is above the threshold.
          if (c > threshold) { // Set lower edge if the bin content is above the threshold.
            binning.insert(binning.begin(), low_edge);
            c = 0.0;
          }
        }
      }
      cb.cp().bin({b}).VariableRebin(binning);
    }
    // blind subcategories with to little events
    for (auto b : cb.cp().bin_set()) {
      // Get shape of this category with sum of backgrounds
      auto shape = cb.cp().bin({b}).backgrounds().GetShape();
      const auto num_bins = shape.GetNbinsX();
      for(auto i = num_bins; i > 0; i--) {
        if(shape.GetBinContent(i) < threshold){
          std::cout << "[INFO] Blind bin " << i << " in " << b << " due to insufficient population!" << "\n";
          cb.cp().bin({b}).ForEachProc([i](ch::Process *p) {
            auto newhist = p->ClonedShape();
            newhist->SetBinContent(i, 0.0);
            newhist->SetBinError(i, 0.0);
            p->set_shape(std::move(newhist), false);
          });
          cb.cp().bin({b}).ForEachObs([i](ch::Observation *p) {
            auto newhist = p->ClonedShape();
            newhist->SetBinContent(i, 0.0);
            newhist->SetBinError(i, 0.0);
            p->set_shape(std::move(newhist), false);
          });
          cb.cp().bin({b}).ForEachSyst([i](ch::Systematic *s) {
            if (s->type().find("shape") == std::string::npos)
                return;
            auto newhist_u = s->ClonedShapeU();
            auto newhist_d = s->ClonedShapeD();
            newhist_u->SetBinContent(i, 0.0);
            newhist_u->SetBinError(i, 0.0);
            newhist_d->SetBinContent(i, 0.0);
            newhist_d->SetBinError(i, 0.0);
            s->set_shapes(std::move(newhist_u), std::move(newhist_d), nullptr);
          });
        }
      }
    }
  }

  // Merge bins and set bin-by-bin uncertainties if no autoMCStats is used.
  if (classic_bbb) {
    auto bbb = ch::BinByBinFactory()
                   .SetAddThreshold(0.0)
                   .SetMergeThreshold(0.5)
                   .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  }
  if (binomial_bbb) {
    auto bbb = ch::BinByBinFactory()
                   .SetPattern("CMS_$ANALYSIS_$CHANNEL_$BIN_$ERA_$PROCESS_binomial_bin_$#")
                   .SetBinomialP(0.022)
                   .SetBinomialErrors(true)
                   .SetBinomialN(1000.0)
                   .SetFixNorm(false);
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  }


  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  ch::SetStandardBinNames(cb, "$ANALYSIS_$CHANNEL_$BINID_$ERA");

  // Write out datacards. Naming convention important for rest of workflow. We
  // make one directory per chn-cat, one per chn and cmb. In this code we only
  // store the individual datacards for each directory to be combined later.
  string output_prefix = "output/";
  ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
                        output_prefix + output_folder +
                            "/$TAG/common/htt_input_" + era_tag + ".root");

  // We're not using mass as an identifier - which we need to tell the
  // CardWriter
  // otherwise it will see "*" as the mass value for every object and skip it
  //    writer.SetWildcardMasses({});

  // Set verbosity
  if (verbose)
    writer.SetVerbosity(1);

  // Write datacards combined and per channel
  writer.WriteCards("cmb", cb);

  for (auto chn : chns) {
    writer.WriteCards(chn, cb.cp().channel({chn}));
  }

  if (verbose)
    cb.PrintAll();

  cout << "[INFO] Done producing datacards.\n";
}
