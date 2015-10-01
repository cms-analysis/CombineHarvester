#include <iostream>
#include <vector>
#include <map>

#include "TSystem.h"

#include "boost/algorithm/string.hpp"
#include "boost/format.hpp"
#include "boost/program_options.hpp"

#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/SOverBTools.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"

namespace po = boost::program_options;

using namespace std;

int main() {
  TH1::AddDirectory(0);
  ModTDRStyle();
  // string cfg;                                   // The configuration file

  // bool do_ratio = false;
  // bool do_logy = true;

  // vector<string> datacards;
  // string fitresult_file = "";
  // string parse_rule = "";

  // string output           = "";
  // string text1            = "";
  // string text2            = "";
  // bool postfit            = true;

  gSystem->Load("libHiggsAnalysisCombinedLimit.dylib");

  ch::CombineHarvester cmb;
  // cmb.SetVerbosity(2);
  // cmb.ParseDatacard(
  //     "output/cmshcg/summer2013/searches/hzz4l/125/hzz4l_4muS_8TeV_0.txt",
  //     "$MASS/$ANALYSIS_$CHANNEL_$ERA_$BINID.txt");
  cmb.ParseDatacard(
      "output/cmshcg/summer2013/searches/hzz4l/125/hzz4l_4muS_8TeV_1.txt",
      "$MASS/$ANALYSIS_$CHANNEL_$ERA_$BINID.txt");
  // cmb.ParseDatacard(
  //     "output/cmshcg/summer2013/searches/hzz4l/125/hzz4l_4muS_7TeV_0.txt",
  //     "$MASS/$ANALYSIS_$CHANNEL_$ERA_$BINID.txt");
  // cmb.ParseDatacard(
  //     "output/cmshcg/summer2013/searches/hzz4l/125/hzz4l_4muS_7TeV_1.txt",
  //     "$MASS/$ANALYSIS_$CHANNEL_$ERA_$BINID.txt");

  ch::SetStandardBinNames(cmb);

  RooFitResult fitresult = ch::OpenFromTFile<RooFitResult>(
      "output/cmshcg/summer2013/searches/hzz4l/125/mlfit.root:fit_s");
  auto fitparams = ch::ExtractFitParameters(fitresult);
  cmb.UpdateParameters(fitparams);

  cmb.process_rgx({".*SM"}, false);
  // cmb.PrintAll();

  TH1F sig_shape = cmb.cp().signals().GetShape();
  TH1F bkg_shape = cmb.cp().backgrounds().GetShape();
  bkg_shape.Print("range");
  std::cout << bkg_shape.Integral() << "\n";
  TH1F data = cmb.GetObservedShape();
  data.Print("range");
  int rebin = 1;
  sig_shape.Rebin(rebin);
  bkg_shape.Rebin(rebin);
  data.Rebin(rebin);

  sig_shape.Scale(data.GetBinWidth(1) / sig_shape.GetBinWidth(1));
  bkg_shape.Scale(data.GetBinWidth(1) / bkg_shape.GetBinWidth(1));

  TCanvas* canv = new TCanvas("hzz4l", "hzz4l");
  canv->cd();

  std::vector<TPad*> pads = OnePad();
  std::vector<TH1*> h = CreateAxisHists(1, &data);
  StandardAxes(h[0]->GetXaxis(), h[0]->GetYaxis(), "m_{4l}", "GeV");
  h[0]->Draw("axis");

  sig_shape.Add(&bkg_shape);
  sig_shape.SetLineColor(4);
  sig_shape.SetLineWidth(3);
  sig_shape.Draw("SAME HIST C");

  bkg_shape.SetLineColor(2);
  bkg_shape.SetLineWidth(3);
  bkg_shape.Draw("SAME HIST C");

  data.Draw("esamex0");

  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.15);
  DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "19.7 fb^{-1} (8 TeV)", 3);
  DrawTitle(pads[0], "H#rightarrowZZ", 1);
  canv->Update();
  pads[0]->RedrawAxis();
  pads[0]->GetFrame()->Draw();
  canv->SaveAs("hzz4l.pdf");

  return 0;
}

