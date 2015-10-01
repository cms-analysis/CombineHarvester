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
  string base = "htt_em_0_8TeV";
  string bin_pre = base+"_prefit";
  string bin_post = base+"_postfit";
  TCanvas* canv = new TCanvas(base.c_str(), base.c_str());
  canv->cd();


  TFile file_(file.c_str(), "READ");

  TH1F data = ch::OpenFromTFile<TH1F>(&file_, bin_pre + "/data_obs");
  data.Scale(1., "width");

  TH1F bkg_pre = ch::OpenFromTFile<TH1F>(&file_, bin_pre + "/TotalBkg");
  TH1F bkg_post = ch::OpenFromTFile<TH1F>(&file_, bin_post + "/TotalBkg");
  TH1F err_pre = ch::OpenFromTFile<TH1F>(&file_, bin_pre + "/TotalBkg");
  TH1F err_post = ch::OpenFromTFile<TH1F>(&file_, bin_post + "/TotalBkg");
  bkg_pre.Scale(1., "width");
  bkg_post.Scale(1., "width");
  err_pre.Scale(1., "width");
  err_post.Scale(1., "width");

  std::vector<TPad*> pads =
      do_ratio ? TwoPadSplit(0.29, 0.005, 0.005) : OnePad();

  pads[0]->SetLogy(do_logy);

  // Source histograms
  file_.Close();

  // Derived histograms

  // Axis histogram
  std::vector<TH1*> h = CreateAxisHists(2, &data);
  if (do_ratio) {
    SetupTwoPadSplitAsRatio(pads, h[0], h[1], "Ratio/Prefit", true, 0.65, 1.35);
    UnitAxes(h[1]->GetXaxis(), h[0]->GetYaxis(), "m_{#tau#tau}", "GeV");
  } else {
    // h[0]->GetXaxis()->SetTitleOffset(1.0);
    UnitAxes(h[0]->GetXaxis(), h[0]->GetYaxis(), "m_{#tau#tau}", "GeV");
  }

  // Can draw main axis now
  h[0]->Draw("axis");


  int new_pre = CreateTransparentColor(12, 0.4);
  int new_post = CreateTransparentColor(2, 0.4);
  bkg_pre.SetLineColor(12);
  bkg_post.SetLineColor(2);
  err_pre.SetLineColor(12);
  err_post.SetLineColor(2);
  err_pre.SetFillColor(new_pre);
  err_pre.SetMarkerSize(0);
  err_post.SetFillColor(new_post);
  err_post.SetMarkerSize(0);

  bkg_pre.Draw("SAMEHIST");
  bkg_post.Draw("SAMEHIST");

  // canv->Update();


  err_pre.Draw("e2sameL");
  err_post.Draw("e2sameL");
  data.Draw("esamex0");

  TH1F *ratio = reinterpret_cast<TH1F *>(
      MakeRatioHist(&data, &err_pre, true, false));
  TH1F *ratio_err = reinterpret_cast<TH1F *>(
      MakeRatioHist(&err_pre, &err_pre, true, false));
  TH1F *ratio_post = reinterpret_cast<TH1F *>(
      MakeRatioHist(&err_post, &err_pre, true, false));

  if (pads[0]->GetLogy()) h[0]->SetMinimum(0.09);

  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.25);
  DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)", 3);
  DrawTitle(pads[0], "H#rightarrow#tau#tau", 1);

  if (do_ratio) {
    pads[1]->cd();
    h[1]->Draw("axis");
    ratio_err->Draw("e2same");
    ratio_post->Draw("e2same");
    TLine line;
    line.SetLineStyle(2);
    DrawHorizontalLine(pads[1], &line, 1.0);
    ratio->Draw("esamex0");
  }

  std::cout << "here2\n";
  pads[0]->cd();
  // pos = 1, 2, 3
  TLegend *legend = PositionedLegend(0.35, 0.15, 3, 0.03);
  legend->SetTextFont(42);
  FixBoxPadding(pads[0], legend, 0.05);
  legend->AddEntry(&data, "Observed", "pe");
  legend->AddEntry(&err_pre, "Background Prefit", "lf");
  legend->AddEntry(&err_post, "Background Postfit", "lf");
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
