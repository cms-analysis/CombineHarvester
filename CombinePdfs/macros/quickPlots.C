#include "Plotting.h"
#include "Plotting_Style.h"

void makeMassPlot() {
  ModTDRStyle();
  TH1F *m90 = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_90");
  m90->Scale(1./m90->Integral(), "width");
  m90->SetLineWidth(2);
  m90->SetLineColor(kRed);

  TH1F *m90hi = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_90_CMS_scale_t_mutau_8TeVUp");
  TH1F *m90lo = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_90_CMS_scale_t_mutau_8TeVDown");
  m90hi->Scale(1./m90hi->Integral(), "width");
  m90hi->SetLineWidth(2);
  m90hi->SetLineColor(kRed);
  m90hi->SetLineStyle(2);
  m90lo->Scale(1./m90lo->Integral(), "width");
  m90lo->SetLineWidth(2);
  m90lo->SetLineColor(kRed);
  m90lo->SetLineStyle(2);


  TH1F *m400 = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_400");
  m400->Scale(1./m400->Integral(), "width");
  m400->SetLineWidth(2);
  m400->SetLineColor(kBlue);

  TH1F *m400hi = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_400_CMS_scale_t_mutau_8TeVUp");
  TH1F *m400lo = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_400_CMS_scale_t_mutau_8TeVDown");
  m400hi->Scale(1./m400hi->Integral(), "width");
  m400hi->SetLineWidth(2);
  m400hi->SetLineColor(kBlue);
  m400hi->SetLineStyle(2);
  m400lo->Scale(1./m400lo->Integral(), "width");
  m400lo->SetLineWidth(2);
  m400lo->SetLineColor(kBlue);
  m400lo->SetLineStyle(2);

  TH1F *m1000 = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_1000");
  m1000->Scale(1./m1000->Integral(), "width");
  m1000->SetLineWidth(2);
  m1000->SetLineColor(kGreen);

  TH1F *m1000hi = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_1000_CMS_scale_t_mutau_8TeVUp");
  TH1F *m1000lo = (TH1F*)gDirectory->Get("htt_mt_8_8TeV_ggH_1000_CMS_scale_t_mutau_8TeVDown");
  m1000hi->Scale(1./m1000hi->Integral(), "width");
  m1000hi->SetLineWidth(2);
  m1000hi->SetLineColor(kGreen);
  m1000hi->SetLineStyle(2);
  m1000lo->Scale(1./m1000lo->Integral(), "width");
  m1000lo->SetLineWidth(2);
  m1000lo->SetLineColor(kGreen);
  m1000lo->SetLineStyle(2);

  TCanvas * canv = new TCanvas("massPlot", "massPlot");
  canv->cd();
  std::vector<TPad*> pads = OnePad();
  pads[0]->SetLogy();
  m90->Draw("HIST");
  m90->GetXaxis()->SetTitle("m_{#tau#tau} (GeV)");
  m90->GetYaxis()->SetTitle("A.U");
  m1000->Draw("HISTSAME");
  m400->Draw("HISTSAME");
  m400hi->Draw("HISTSAME");
  m400lo->Draw("HISTSAME");
  m90hi->Draw("HISTSAME");
  m90lo->Draw("HISTSAME");
  m1000hi->Draw("HISTSAME");
  m1000lo->Draw("HISTSAME");
  m90->SetMinimum(0.0001);
  m90->SetMaximum(10.);
  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], "ggH, No B-Tag", 3);
  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.1);
  FixOverlay();
  TLegend *leg = PositionedLegend(0.3, 0.3, 3, 0.025);
  leg->AddEntry(m90, "m_{#Phi} = 90 GeV", "L");
  leg->AddEntry(m400, "m_{#Phi} = 400 GeV", "L");
  leg->AddEntry(m1000, "m_{#Phi} = 1000 GeV", "L");
  leg->AddEntry(m90hi, "Tau ES Variation", "L");
  leg->Draw();
  canv->SaveAs("massPlot.pdf");
}

void makeRatePlot() {
  ModTDRStyle(600, 300, 0.10, 0.12, 0.16, 0.04);
  TGraph *gr = (TGraph*)gDirectory->Get("interp_rate_htt_mt_8_8TeV_ggH");

  TH1 *axis = CreateAxisHist(gr, false);
  axis->GetXaxis()->SetTitle("m_{#Phi} (GeV)");
  axis->GetYaxis()->SetTitle("Event Yield [#sigma#timesBR = 1]");
  gr->SetLineColor(kRed);
  TCanvas * canv = new TCanvas("ratePlot", "ratePlot");
  canv->cd();
  std::vector<TPad*> pads = OnePad();
  // pads[0]->SetLogy();
  axis->Draw();
  gr->Draw("LPSAME");
  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], "ggH, No B-Tag", 3);
  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.1);
  FixOverlay();
  // TLegend *leg = PositionedLegend(0.3, 0.3, 3, 0.025);
  // leg->AddEntry(m90, "m_{#Phi} = 90 GeV", "L");
  // leg->AddEntry(m400, "m_{#Phi} = 400 GeV", "L");
  // leg->AddEntry(m1000, "m_{#Phi} = 1000 GeV", "L");
  // leg->AddEntry(m90hi, "Tau ES Variation", "L");
  // leg->Draw();
  canv->SaveAs("ratePlot.pdf");
}

void makeKappaPlot() {
  ModTDRStyle(600, 300, 0.10, 0.12, 0.16, 0.04);
  TGraph *grhi = (TGraph*)gDirectory->Get("spline_hi_htt_mt_8_8TeV_ggH_CMS_eff_t_mssmHigh_mutau_8TeV");
  TGraph *grlo = (TGraph*)gDirectory->Get("spline_lo_htt_mt_8_8TeV_ggH_CMS_eff_t_mssmHigh_mutau_8TeV");

  TH1 *axis = CreateAxisHist(grhi, false);
  axis->GetXaxis()->SetTitle("m_{#Phi} (GeV)");
  axis->GetYaxis()->SetTitle("Uncertainty");
  grhi->SetLineColor(kRed);
  grlo->SetLineColor(kRed);
  axis->SetMinimum(0.9);
  axis->SetMaximum(1.1);
  TCanvas * canv = new TCanvas("ratePlot", "ratePlot");
  canv->cd();
  std::vector<TPad*> pads = OnePad();
  // pads[0]->SetLogy();
  axis->Draw();
  grhi->Draw("LPSAME");
  grlo->Draw("LPSAME");
  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], "ggH, No B-Tag", 3);
  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.1);
  FixOverlay();
  TLine line;
  line.SetLineStyle(2);
  DrawHorizontalLine(pads[0], &line, 1.0);
  // TLegend *leg = PositionedLegend(0.3, 0.3, 3, 0.025);
  // leg->AddEntry(m90, "m_{#Phi} = 90 GeV", "L");
  // leg->AddEntry(m400, "m_{#Phi} = 400 GeV", "L");
  // leg->AddEntry(m1000, "m_{#Phi} = 1000 GeV", "L");
  // leg->AddEntry(m90hi, "Tau ES Variation", "L");
  // leg->Draw();
  canv->SaveAs("kappaPlot.pdf");
}

void quickPlots() {
  TFile f("htt_mt_mssm_demo.root");
  makeMassPlot();
  makeRatePlot();
  makeKappaPlot();



}

