#include "interface/Plotting.h"
#include "interface/Plotting_Style.h"

void plot_vhbb(TString file, TString folder, TString output, TString title) {
  ModTDRStyle();
  TFile f(file);

  TH1F *h_data  = (TH1F*)gDirectory->Get(folder+"data_obs");

  TH1F *h_VVHF  = (TH1F*)gDirectory->Get(folder+"VVHF");
  TH1F *h_VVLF  = (TH1F*)gDirectory->Get(folder+"VVLF");
  TH1F *h_QCD   = (TH1F*)gDirectory->Get(folder+"QCD");
  TH1F *h_s_Top = (TH1F*)gDirectory->Get(folder+"s_Top");
  TH1F *h_TT    = (TH1F*)gDirectory->Get(folder+"TT");
  TH1F *h_Zj0b  = (TH1F*)gDirectory->Get(folder+"Zj0b");
  TH1F *h_Zj1b  = (TH1F*)gDirectory->Get(folder+"Zj1b");
  TH1F *h_Zj2b  = (TH1F*)gDirectory->Get(folder+"Zj2b");
  TH1F *h_Wj0b  = (TH1F*)gDirectory->Get(folder+"Wj0b");
  TH1F *h_Wj1b  = (TH1F*)gDirectory->Get(folder+"Wj1b");
  TH1F *h_Wj2b  = (TH1F*)gDirectory->Get(folder+"Wj2b");
  TH1F *h_WH  = (TH1F*)gDirectory->Get(folder+"WH");
  TH1F *h_ZH  = (TH1F*)gDirectory->Get(folder+"ZH");
  h_WH->Add(h_ZH);

  TH1F *h_bkg  = (TH1F*)gDirectory->Get(folder+"TotalBkg");

  h_VVHF->SetFillColor(TColor::GetColor(194, 193, 194));
  h_VVLF->SetFillColor(TColor::GetColor(83, 83, 83));
  h_QCD->SetFillColor(TColor::GetColor(242, 0, 255));
  h_s_Top->SetFillColor(TColor::GetColor(64, 255, 194));
  h_TT->SetFillColor(TColor::GetColor(37, 2, 255));
  h_Zj0b->SetFillColor(TColor::GetColor(194, 197, 8));
  h_Zj1b->SetFillColor(TColor::GetColor(203, 199, 117));
  h_Zj2b->SetFillColor(TColor::GetColor(255, 255, 8));
  h_Wj0b->SetFillColor(TColor::GetColor(43, 139, 1));
  h_Wj1b->SetFillColor(TColor::GetColor(140, 255, 83));
  h_Wj2b->SetFillColor(TColor::GetColor(67, 255, 9));
  h_WH->SetFillColor(TColor::GetColor(244, 0, 8));

  TH1F *h_WHc = (TH1F*)h_WH->Clone();
  h_WHc->SetLineColor(TColor::GetColor(244, 0, 8));
  h_WHc->SetFillStyle(0);
  h_WHc->SetLineWidth(2);

  int new_idx = CreateTransparentColor(12, 0.4);
  h_bkg->SetFillColor(new_idx);
  h_bkg->SetMarkerSize(0);

  THStack stack;
  stack.Add(h_VVHF);
  stack.Add(h_VVLF);
  stack.Add(h_QCD);
  stack.Add(h_s_Top);
  stack.Add(h_TT);
  stack.Add(h_Zj0b);
  stack.Add(h_Zj1b);
  stack.Add(h_Zj2b);
  stack.Add(h_Wj0b);
  stack.Add(h_Wj1b);
  stack.Add(h_Wj2b);
  stack.Add(h_WH);

  TCanvas * canv = new TCanvas(output, output);
  canv->cd();
  std::vector<TPad*> pads = TwoPadSplit(0.29, 0.005, 0.005);

  // Do the axis hist
  std::vector<TH1*> h = CreateAxisHists(2, h_data);
  SetupTwoPadSplitAsRatio(pads, h[0], h[1], "Obs/Exp", true, 0.05, 1.95);
  h[1]->GetXaxis()->SetTitle("BDT output");
  TString w_label = TString::Format("%.2f", h[1]->GetXaxis()->GetBinWidth(1));
  h[0]->GetYaxis()->SetTitle("Events / " + w_label);

  h[0]->Draw("axis");

  // Draw the stack
  stack.Draw("HISTSAME");
  h_bkg->Draw("e2same");
  h_data->Draw("esamex0");

  TH1F *ratio = reinterpret_cast<TH1F *>(
      MakeRatioHist(h_data, h_bkg, true, false));
  TH1F *ratio_err = reinterpret_cast<TH1F *>(
      MakeRatioHist(h_bkg, h_bkg, true, false));

  pads[0]->SetLogy(true);
  h[0]->SetMinimum(0.01);

  // Fix the y-axis range
  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.45);

  // Make the legend
  TLegend *leg = PositionedLegend(0.5, 0.2, 3, 0.025);
  leg->AddEntry(h_data, "Observed", "pe");
  leg->AddEntry(h_TT, "tt", "F");
  leg->AddEntry(h_Wj2b, "W + bb", "F");
  leg->AddEntry(h_s_Top, "Single top", "F");
  leg->AddEntry(h_Wj1b, "W + b", "F");
  leg->AddEntry(h_QCD, "QCD", "F");
  leg->AddEntry(h_Wj0b, "W + udscg", "F");
  leg->AddEntry(h_VVLF, "VZ(udscg)", "F");
  leg->AddEntry(h_Zj2b, "Z + bb", "F");
  leg->AddEntry(h_VVHF, "VZ(bb)", "F");
  leg->AddEntry(h_Zj1b, "Z + b", "F");
  leg->AddEntry(h_WH, "VH", "F");
  leg->AddEntry(h_Zj0b, "Z + udscg", "F");
  leg->AddEntry(h_bkg, "Bkg. Uncertainty", "f");

  leg->SetNColumns(2);
  leg->Draw();

  // Draw labels and text
  // DrawCMSLogo(pads[0], "CombineHarvester", "", 0);
  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], title, 3);

  // Redraw the axis
  FixOverlay();
  h_WHc->Draw("HISTSAME");

  pads[1]->cd();
  h[1]->Draw("axis");
  ratio_err->Draw("e2same");
  TLine line;
  line.SetLineStyle(2);
  DrawHorizontalLine(pads[1], &line, 1.0);
  ratio->Draw("esamex0");

  // Print!
  canv->Print(output+".pdf");
}
