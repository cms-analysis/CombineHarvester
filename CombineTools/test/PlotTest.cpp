#include <iostream>
#include <string>
#include <vector>
#include <cmath>

#include "TCanvas.h"
#include "TH1F.h"
#include "TFile.h"
#include "TROOT.h"
#include "TFrame.h"
#include "TLegend.h"
#include "THStack.h"

#include "boost/range/adaptor/reversed.hpp"

#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"

// Function prototypes
struct BkgComponent {
  std::string legend;
  std::vector<std::string> plots;
  int color;
  TH1F hist;
  BkgComponent(std::string l, std::vector<std::string> p,
                   int c)
      : legend(l), plots(p), color(c) {}
};

struct SigComponent {
  std::string legend;
  std::vector<std::string> plots;
  int color;
  bool in_stack;
  TH1F hist;
  SigComponent(std::string l, std::vector<std::string> p, int c,
               bool s)
      : legend(l), plots(p), color(c), in_stack(s) {}
};

using namespace std;

int main() {
  bool do_ratio = true;
  bool do_logy = false;

  TH1::AddDirectory(0);
  ModTDRStyle();

  string file = "bus.root";

  string bin = "htt_em_0_8TeV_prefit";
  TCanvas* canv = new TCanvas(bin.c_str(), bin.c_str());
  canv->cd();


  map<string, vector<BkgComponent>> bkg_schemes;
  bkg_schemes["em"] = {
    BkgComponent("Misidentified e/#mu",
      {"Fakes"},  TColor::GetColor(250, 202, 255)),
    BkgComponent("Electroweak",
      {"EWK"},    TColor::GetColor(222, 90, 106)),
    BkgComponent("t#bar{t}",
      {"ttbar"},  TColor::GetColor(155, 152, 204)),
    BkgComponent("Z#rightarrow#tau#tau",
      {"Ztt"},    TColor::GetColor(248, 206, 104)),
    BkgComponent("SM H(125 GeV)#rightarrow WW",
      {"ggH_hww125", "qqH_hww125"}, TColor::GetColor(36, 139, 2))};

  vector<BkgComponent> & bkg_scheme = bkg_schemes["em"];

  TFile file_(file.c_str(), "READ");

  TH1F data = ch::OpenFromTFile<TH1F>(&file_, bin + "/data_obs");
  data.Scale(1., "width");

  TH1F total_bkg = ch::OpenFromTFile<TH1F>(&file_, bin + "/TotalBkg");
  total_bkg.Scale(1., "width");


  for (auto & comp : bkg_scheme) {
    comp.hist = ch::OpenFromTFile<TH1F>(&file_, bin + "/" + comp.plots.at(0));
    for (unsigned i = 1; i < comp.plots.size(); ++i) {
      TH1F tmp = ch::OpenFromTFile<TH1F>(&file_, bin + "/" + comp.plots.at(i));
      comp.hist.Add(&tmp);
    }
    comp.hist.SetTitle(comp.legend.c_str());
    comp.hist.SetFillColor(comp.color);
    comp.hist.Scale(1., "width");
  }

  std::vector<TPad*> pads =
      do_ratio ? TwoPadSplit(0.29, 0.005, 0.005) : OnePad();

  pads[0]->SetLogy(do_logy);

  // Source histograms
  file_.Close();

  // Derived histograms

  // Axis histogram
  std::vector<TH1*> h = CreateAxisHists(2, &data);
  if (do_ratio) {
    SetupTwoPadSplitAsRatio(pads, h[0], h[1], "Obs/Exp", true, 0.65, 1.35);
    UnitAxes(h[1]->GetXaxis(), h[0]->GetYaxis(), "m_{#tau#tau}", "GeV");
  } else {
    // h[0]->GetXaxis()->SetTitleOffset(1.0);
    UnitAxes(h[0]->GetXaxis(), h[0]->GetYaxis(), "m_{#tau#tau}", "GeV");
  }

  // Can draw main axis now
  h[0]->Draw("axis");


  int new_idx = CreateTransparentColor(12, 0.4);
  total_bkg.SetFillColor(new_idx);
  total_bkg.SetMarkerSize(0);

  THStack stack("stack", "stack");
  for (auto & comp : bkg_scheme) {
    stack.Add(new TH1F(comp.hist), "hist");
  }

  stack.Draw("histsame");
  // canv->Update();


  total_bkg.Draw("e2same");
  data.Draw("esamex0");

  TH1F *ratio = reinterpret_cast<TH1F *>(
      MakeRatioHist(&data, &total_bkg, true, false));
  TH1F *ratio_err = reinterpret_cast<TH1F *>(
      MakeRatioHist(&total_bkg, &total_bkg, true, false));

  if (pads[0]->GetLogy()) h[0]->SetMinimum(0.09);

  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.25);
  DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)", 3);
  DrawTitle(pads[0], "H#rightarrow#tau#tau", 1);

  if (do_ratio) {
    pads[1]->cd();
    h[1]->Draw("axis");
    ratio_err->Draw("e2same");
    TLine line;
    line.SetLineStyle(2);
    DrawHorizontalLine(pads[1], &line, 1.0);
    ratio->Draw("esamex0");
  }

  std::cout << "here2\n";
  pads[0]->cd();
  // pos = 1, 2, 3
  TLegend *legend = PositionedLegend(0.35, 0.35, 3, 0.03);
  legend->SetTextFont(42);
  FixBoxPadding(pads[0], legend, 0.05);
  legend->AddEntry(&data, "Observed", "pe");
  for (auto & comp : boost::adaptors::reverse(bkg_scheme)) {
    legend->AddEntry(&comp.hist, comp.legend.c_str(), "f");
  }
  legend->AddEntry(&total_bkg, "Bkg. Uncertainty", "f");
  legend->Draw();

  pads[0]->RedrawAxis();

  pads[0]->GetFrame()->Draw();

  if (do_ratio) {
    pads[1]->cd();
    pads[1]->RedrawAxis();
    pads[1]->GetFrame()->Draw();
  }

  canv->Print(".pdf");
  canv->Print(".png");

  delete legend;

  return 0;
}
