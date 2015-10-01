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
#include "CombineHarvester/CombineTools/interface/Utilities.h"

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
  bool do_logy = true;

  TH1::AddDirectory(0);
  ModTDRStyle();
  gStyle->SetLineStyleString(11,"20 10");


  string file = "parametric/plots_asimov.root";

  string bin = "htt_mt_8_8TeV_postfit";
  string bin_hm = "htt_mt_8_8TeV_hm_postfit";
  TCanvas* canv = new TCanvas(bin.c_str(), bin.c_str());
  canv->cd();


  map<string, vector<BkgComponent>> bkg_schemes;
  bkg_schemes["mt"] = {
    BkgComponent("QCD",                   {"QCD"},      TColor::GetColor(250,202,255)),
    BkgComponent("t#bar{t}",              {"TT"},       TColor::GetColor(155,152,204)),
    BkgComponent("Electroweak",           {"W","VV"},   TColor::GetColor(222, 90,106)),
    BkgComponent("Z#rightarrow#mu#mu",    {"ZL","ZJ"},  TColor::GetColor(100,182,232)),
    BkgComponent("Z#rightarrow#tau#tau",  {"ZTT"} ,     TColor::GetColor(248,206,104))};

  vector<BkgComponent> & bkg_scheme = bkg_schemes["mt"];

  TFile file_(file.c_str(), "READ");

  TH1F data = ch::OpenFromTFile<TH1F>(&file_, bin + "/data_obs");
  data.Scale(1., "width");

  unsigned hm_rebin = 4;

  TH1F data_hm = ch::OpenFromTFile<TH1F>(&file_, bin_hm + "/data_obs");

  double max = data_hm.GetXaxis()->GetXmax();
  TH1F axis_hist("axis", "axis", static_cast<int>(max), 0, max);

  TH1F total_bkg = ch::OpenFromTFile<TH1F>(&file_, bin + "/TotalBkg");
  total_bkg.Scale(1., "width");

  TH1F total_sig = ch::OpenFromTFile<TH1F>(&file_, bin + "/TotalSig");
  total_sig.Scale(1., "width");


  TH1F total_bkg_hm = ch::RestoreBinning(ch::OpenFromTFile<TH1F>(&file_, bin_hm + "/TotalBkg"), data_hm);
  total_bkg_hm.SetLineWidth(2);

  TH1F total_sig_hm = ch::OpenFromTFile<TH1F>(&file_, bin_hm + "/TotalSig");

  data_hm.Rebin(hm_rebin);
  total_bkg_hm.Rebin(hm_rebin);
  total_sig_hm.Rebin(hm_rebin);

  data_hm.Scale(1., "width");
  total_bkg_hm.Scale(1., "width");
  total_sig_hm.Scale(1., "width");

  TH1F total_bkg_hm_err = total_bkg_hm;
  total_bkg_hm.SetLineColor(8);

  total_sig.SetLineColor(TColor::GetColor(0,18,255));
  total_sig_hm.SetLineColor(TColor::GetColor(0,18,255));
  total_sig.SetFillStyle(1001);
  total_sig_hm.SetFillStyle(1001);
  total_sig.SetLineStyle(11);
  total_sig_hm.SetLineStyle(11);
  total_sig.SetLineWidth(2);
  total_sig_hm.SetLineWidth(2);
  total_sig.Scale(0.01);
  total_sig_hm.Scale(0.01);


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
      do_ratio ? TwoPadSplit(0.29, 0.008, 0.008) : OnePad();

  pads[0]->SetLogy(do_logy);

  // Source histograms
  file_.Close();

  // Derived histograms

  // Axis histogram
  std::vector<TH1*> h = CreateAxisHists(2, &axis_hist);
  if (do_ratio) {
    SetupTwoPadSplitAsRatio(pads, h[0], h[1], "Obs/Exp", true, 0.25, 1.75);
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
  total_bkg_hm_err.SetFillColor(new_idx);
  total_bkg_hm_err.SetMarkerSize(0);

  THStack stack("stack", "stack");
  for (auto & comp : bkg_scheme) {
    stack.Add(new TH1F(comp.hist), "hist");
  }

  stack.Draw("histsame");
  // canv->Update();

  total_sig.Draw("histsame");

  total_bkg.Draw("e2same");

  total_bkg_hm_err.Draw("e3same");
  total_bkg_hm.Draw("histlsame");

  total_sig_hm.Draw("histsame");
  data.Draw("esamex0");
  data_hm.Draw("esamex0");

  TH1F *ratio = reinterpret_cast<TH1F *>(
      MakeRatioHist(&data, &total_bkg, true, false));
  TH1F *ratio_hm = reinterpret_cast<TH1F *>(
      MakeRatioHist(&data_hm, &total_bkg_hm, true, false));
  TH1F *ratio_err = reinterpret_cast<TH1F *>(
      MakeRatioHist(&total_bkg, &total_bkg, true, false));
  TH1F *ratio_err_hm = reinterpret_cast<TH1F *>(
      MakeRatioHist(&total_bkg_hm_err, &total_bkg_hm_err, true, false));
  if (pads[0]->GetLogy()) h[0]->SetMinimum(1E-3);

  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.25);
  DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "19.7 fb^{-1} (8 TeV)", 3);
  DrawTitle(pads[0], "H#rightarrow#tau#tau, #mu_{}#tau_{h}, No B-Tag", 1);

  if (do_ratio) {
    pads[1]->cd();
    h[1]->Draw("axis");
    ratio_err->Draw("e2same");
    ratio_err_hm->Draw("e3same");
    TLine line;
    line.SetLineStyle(2);
    DrawHorizontalLine(pads[1], &line, 1.0);
    ratio->Draw("esamex0");
    ratio_hm->Draw("esamex0");
  }

  pads[0]->cd();
  // pos = 1, 2, 3
  TLegend *legend = PositionedLegend(0.35, 0.35, 3, 0.03);
  legend->SetTextFont(42);
  FixBoxPadding(pads[0], legend, 0.05);
  legend->AddEntry(&data, "Observed", "pe");
  legend->AddEntry(&total_sig, "#Phi(800 GeV)#rightarrow#tau#tau", "l");
  for (auto & comp : boost::adaptors::reverse(bkg_scheme)) {
    legend->AddEntry(&comp.hist, comp.legend.c_str(), "f");
  }
  legend->AddEntry(&total_bkg_hm, "Parametric Bkg.", "l");
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
