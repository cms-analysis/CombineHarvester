#include <iostream>
#include <vector>
#include "boost/lexical_cast.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/format.hpp"
#include "boost/program_options.hpp"
// #include "Core/interface/Plot.h"
// #include "Core/interface/TextElement.h"
// #include "Utilities/interface/FnRootTools.h"
// #include "HiggsTauTau/interface/HTTStatTools.h"
// #include "HiggsTauTau/interface/HTTPlotTools.h"
// #include "HiggsTauTau/interface/HTTAnalysisTools.h"
// #include "HiggsTauTau/interface/mssm_xs_tools.h"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"

namespace po = boost::program_options;

using namespace std;
// using namespace ic;

// HTTAnalysis::HistValuePair FillHistValuePair(ch::CombineHarvester & cmb, RooFitResult * res) {
//   if (res) {
//     return std::make_pair(
//         cmb.GetShape(),
//         std::make_pair(cmb.GetRate(), cmb.GetUncertainty(res, 500)));
//   } else {
//     return std::make_pair(
//         cmb.GetShape(),
//         std::make_pair(cmb.GetRate(), cmb.GetUncertainty()));
//     } 
// }

int main(int /*argc*/, char* /*argv*/[]){
  /*
  string cfg;                                   // The configuration file
  string channel        = "";
  string selection      = "";
  string eras           = "";
  string fitresult_file = "";
  string datacard_path  = "";
  string third_line     = "";
  // string root_file_path = "";
  bool postfit          = true;
  bool mssm             = false;
  po::options_description preconfig("Pre-Configuration");
  preconfig.add_options()("cfg", po::value<std::string>(&cfg)->required());
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv)
    .options(preconfig).allow_unregistered().run(), vm);
  po::notify(vm);
  po::options_description config("Configuration");
  config.add_options()
    ("channel",              po::value<string>(&channel)->required(),         "[REQUIRED] channel, choose one of [et,mt,em,tt]")
    ("selection",            po::value<string>(&selection)->required(),       "[REQUIRED] categories to combine with label, e.g. \"0-jet:0+1\" combines the 0-jet low and high categories")
    ("eras",                 po::value<string>(&eras)->required(),            "[REQUIRED] data-taking periods to combine, e.g. \"7TeV,8TeV\"")
    ("thirdline",             po::value<string>(&third_line),                 "[REQUIRED] data-taking periods to combine, e.g. \"7TeV,8TeV\"")
    ("datacard_path",        po::value<string>(&datacard_path)->required(),   "[REQUIRED] path to the folder containing datacard *.txt files")
    // ("root_file_path",       po::value<string>(&root_file_path)->required(),  "[REQUIRED] path to the folder containing datacard *.root files")
    ("fitresult,f",          po::value<string>(&fitresult_file)->required(),  "[REQUIRED] path to the file containing the pulls from a maximum-likelihood fit")
    ("postfit",              po::value<bool>(&postfit)->required(),           "[REQUIRED] use the pulls file to make a post-fit plot")
    ("mssm",                 po::value<bool>(&mssm)->default_value(false),    "input is an MSSM datacard");
  HTTPlot plot;
  config.add(plot.GenerateOptions(""));
  po::store(po::command_line_parser(argc, argv)
    .options(config).allow_unregistered().run(), vm);
  po::store(po::parse_config_file<char>(cfg.c_str(), config, true), vm);
  po::notify(vm);

  vector<string> signal_procs = {"ggH", "qqH", "VH"};
  if (mssm) signal_procs = {"ggH", "bbH"};

  vector<string> v_eras;
  boost::split(v_eras, eras, boost::is_any_of(","));
  std::string era_file_label;
  for (unsigned i = 0; i < v_eras.size(); ++i) era_file_label += v_eras[i];

  pair<string, vector<string>> v_columns;
  vector<string> tmp_split;
  boost::split(tmp_split, selection, boost::is_any_of(":"));
  if (tmp_split.size() == 2) {
    vector<string> tmp_cats;
    boost::split(tmp_cats, tmp_split[1], boost::is_any_of("+"));
    v_columns = make_pair(tmp_split[0], tmp_cats);
  }

  string signal_mass = plot.draw_signal_mass();
  string tanb = plot.draw_signal_tanb();
  // HTTSetup setup;
  ch::CombineHarvester cmb;
  if (!mssm) {
    for (unsigned j = 0; j < v_eras.size(); ++j) {
      for (unsigned k = 0; k < v_columns.second.size(); ++k) {
        string cat = v_columns.second[k];
        cmb.ParseDatacard(datacard_path+"htt_"+channel+"_"+cat+"_"+v_eras[j]+".txt",
          "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
        // setup.ParseDatacard(datacard_path+"/"+"htt_"+channel+"_"+cat+"_"+v_eras[j]+".txt", channel, boost::lexical_cast<int>(cat), v_eras[j], signal_mass);        
      }
    }
  } else {
    vector<int> bin_ids;
    for (auto id : v_columns.second) bin_ids.push_back(boost::lexical_cast<int>(id));
    cmb.ParseDatacard(datacard_path+"datacard_"+tanb+".txt", "{MASS}/datacard_"+tanb+".txt");
    string bin_pat = "$ANALYSIS_$CHANNEL_$BINID_$ERA";
    cmb.ForEachSyst(boost::bind(ch::SetFromBinName<ch::Systematic>, _1, bin_pat));
    cmb.ForEachObs(boost::bind(ch::SetFromBinName<ch::Observation>, _1, bin_pat));
    cmb.ForEachProc(boost::bind(ch::SetFromBinName<ch::Process>, _1, bin_pat));
    cmb.channel({channel}).era(v_eras).bin_id(bin_ids);
  }
  // for (unsigned i = 0; i < v_eras.size(); ++i) {
  //   if (!mssm) {
  //     setup.ParseROOTFile(root_file_path+"/"+"htt_"+channel+".input_"+v_eras[i]+".root", channel, v_eras[i]);
  //   } else {
  //     setup.ParseROOTFile(root_file_path+"/"+"htt_"+channel+".inputs-mssm-"+v_eras[i]+"-0.root", channel, v_eras[i]);
  //   }
  // }
  // setup.ParsePulls(pulls_file);
  // auto chi2_splusb = setup.GetPullsChi2(true);
  // auto chi2_bonly = setup.GetPullsChi2(false);
  // std::cout << "Chi2 s+b:    " << chi2_splusb.first << " " << chi2_splusb.second << std::endl;
  // std::cout << "Chi2 b-only: " << chi2_bonly.first << " " << chi2_bonly.second << std::endl;
  // if (postfit) setup.ApplyPulls();

  RooFitResult *fitresult = nullptr;
  if (fitresult_file.length() && postfit) {
    fitresult = new RooFitResult(ch::OpenFromTFile<RooFitResult>(fitresult_file));
    auto fitparams = ch::ExtractFitParameters(*fitresult);
    cmb.UpdateParameters(fitparams);
  }
  // cmb.PrintAll();


  HTTAnalysis::HistValueMap hmap;

  hmap["data_obs"] = make_pair(cmb.GetObservedShape(),
    make_pair(cmb.GetObservedRate(), sqrt(cmb.GetObservedRate())));
  HTTAnalysis::PrintValue("data_obs", hmap["data_obs"].second);

  vector<string> samples;
  if (channel != "em") {
    samples = {"ZTT","QCD","W","ZL","ZJ","VV","TT"};
  } else {
    samples = {"Ztt","Fakes","EWK","ttbar"};
    if (!mssm) {
      samples.push_back("ggH_hww125");
      samples.push_back("qqH_hww125");
    }
  }
  RooFitResult * send_res = nullptr;
  for (auto const& s : samples) {
    hmap[s] = FillHistValuePair(cmb.cp().process({s}), send_res);
    HTTAnalysis::PrintValue(s, hmap[s].second);
  }
  for (auto const& s : signal_procs) {
    if (s == "VH") {
      hmap[s+signal_mass] = FillHistValuePair(cmb.cp().process({"WH","ZH"}), send_res);
    } else {
      hmap[s+signal_mass] = FillHistValuePair(cmb.cp().process({s}), send_res);
    }
    HTTAnalysis::PrintValue(s+signal_mass, hmap[s+signal_mass].second);
  }

  string catstring = "";
  for (unsigned i = 0; i < v_columns.second.size(); ++i) catstring += v_columns.second.at(i);
  plot.set_plot_name(channel + "_" + catstring + "_" + era_file_label+ (postfit ? "_postfit":"_prefit"));

  TH1F total_hist = cmb.cp().backgrounds().GetShapeWithUncertainty(fitresult, 500);
  hmap["Bkg"] = make_pair(total_hist, make_pair(0.,0.));

  string channel_str;
  if (channel == "et") channel_str = "e#tau_{h}";
  if (channel == "mt") channel_str = "#mu#tau_{h}";
  if (channel == "em") channel_str = "e#mu";
  if (channel == "tt") channel_str = "#tau_{h}#tau_{h}";
  if (!postfit) channel_str += " (pre-fit)";

  TH1F data_chi2 = hmap["data_obs"].first;
  TH1F bkg_chi2 = hmap["Bkg"].first;
  if (plot.blind()) {
    for (int j = 0; j < data_chi2.GetNbinsX(); ++j) {
      double low_edge = data_chi2.GetBinLowEdge(j+1);
      double high_edge = data_chi2.GetBinWidth(j+1)+data_chi2.GetBinLowEdge(j+1);
      if ((low_edge > plot.x_blind_min() && low_edge < plot.x_blind_max()) || (high_edge > plot.x_blind_min() && high_edge < plot.x_blind_max())) {
        data_chi2.SetBinContent(j+1,0);
        data_chi2.SetBinError(j+1,0);
        bkg_chi2.SetBinContent(j+1,0);
        bkg_chi2.SetBinError(j+1,0);
      }
    }
  }
  // double chi2_prob = data_chi2.Chi2Test(&(bkg_chi2),"UW");
  for (int j = 0; j < data_chi2.GetNbinsX(); ++j) {
    double low_edge = data_chi2.GetBinLowEdge(j+1);
    double high_edge = data_chi2.GetBinWidth(j+1)+data_chi2.GetBinLowEdge(j+1);
    if ((low_edge > -1. && low_edge < 60.) || (high_edge > -1. && high_edge < 60.)) {
      data_chi2.SetBinContent(j+1,0);
      data_chi2.SetBinError(j+1,0);
      bkg_chi2.SetBinContent(j+1,0);
      bkg_chi2.SetBinError(j+1,0);
    }
  }
  // double chi2_prob_cut = data_chi2.Chi2Test(&(bkg_chi2),"UW");

  ic::TextElement text(channel_str,0.05,0.57,0.46);
  if (mssm) text.set_x_pos(0.29);
  if (mssm) text.set_y_pos(0.85);
  ic::TextElement text2(v_columns.first,0.05,0.57,0.38);
  if (mssm) text2.set_x_pos(0.29);
  if (mssm) text2.set_y_pos(0.77);
  ic::TextElement text3(third_line,0.05,0.57,0.32);

  plot.AddTextElement(text);
  plot.AddTextElement(text2);
  if (third_line != "") plot.AddTextElement(text3);
  //plot.set_title_right((boost::format("P(#chi^{2}): %.4f, P(#chi^{2}, M>60 GeV): %.4f")%chi2_prob%chi2_prob_cut).str());

  if (mssm) {
    double dtanb = boost::lexical_cast<double>(tanb);
    ic::TextElement text_ma(
      (boost::format("m^{h}_{max} (m_{A}=%s GeV, tan#beta=%.0f)")
        % signal_mass % dtanb).str(), 0.035, 0.555, 0.945);
    // ic::TextElement text_tanb("tan#beta="+tanb,0.035,0.41,0.81);
    // ic::TextElement text_scen("m^{h}_{max}",0.035,0.41,0.76);
    plot.AddTextElement(text_ma);
    // plot.AddTextElement(text_tanb);
    // plot.AddTextElement(text_scen);
  }

  plot.GeneratePlot(hmap);

  std::string tfile_name = channel + "_" + catstring + "_" + era_file_label+ (postfit ? "_postfit":"_prefit")+".root";
  TFile dc_file(tfile_name.c_str(),"RECREATE");
  dc_file.cd();
  for (auto iter : hmap) {
    iter.second.first.SetTitle(iter.first.c_str());
    iter.second.first.SetName(iter.first.c_str());
    iter.second.first.Write();
  }
  std::cout << "[HiggsTauTauPlot4] Writing datacard input " << tfile_name << std::endl;
  dc_file.Close();
  */

  return 0;
}

