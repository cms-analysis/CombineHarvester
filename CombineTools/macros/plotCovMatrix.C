#include "../interface/Plotting.h"
#include "../interface/Plotting_Style.h"
#include "TH2F.h"
#include "TGraphAsymmErrors.h"
#include "TMath.h"

// Calculate label1 - labele2


void drawMatrix(TH2D *h, TString output) {
  TCanvas * canv = new TCanvas(output, output);
  canv->cd();
  std::vector<TPad*> pads = OnePad();
  pads[0]->SetBottomMargin(0.15);
  pads[0]->SetLeftMargin(0.22);
  pads[0]->SetRightMargin(0.13);

  h->SetMarkerSize(1.0);
  h->GetXaxis()->SetLabelSize(0.05);
  h->GetYaxis()->SetLabelSize(0.05);
  h->GetXaxis()->LabelsOption("d");
  h->Draw("TEXT");
  // DrawCMSLogo(pads[0], "CMS", "Simulation", 0);
  canv->Print(output+".pdf");
  delete canv;
}

// void printErrors(TH2D *h1, TH2D *h2, TH2D *h3) {
//   for (int i = 1; i <= h1->GetNbinsX(); ++i) {
//     TString var = h1->GetXaxis()->GetBinLabel(i);
//     double err1 = TMath::Sqrt(h1->TH1::GetBinContent(i, h1->GetNbinsX() + 1 - i));
//     double err2 = TMath::Sqrt(h2->TH1::GetBinContent(i, h2->GetNbinsX() + 1 - i));
//     double err3 = TMath::Sqrt(h3->TH1::GetBinContent(i, h3->GetNbinsX() + 1 - i));
//     std::cout << TString::Format("%-10s : %.3f (total) := %.3f (stat) + %.3f (syst)\n", var.Data(), err1, err2, err3);
//   }
// }

void printErrors(TH2D *h1, TH2D *h2) {
  for (int i = 1; i <= h1->GetNbinsX(); ++i) {
    TString var = h1->GetXaxis()->GetBinLabel(i);
    double err1 = TMath::Sqrt(h1->TH1::GetBinContent(i, h1->GetNbinsX() + 1 - i));
    double err2 = TMath::Sqrt(h2->TH1::GetBinContent(i, h2->GetNbinsX() + 1 - i));
    std::cout << TString::Format("%-10s : %.3f (err1) := %.3f (err2)\n", var.Data(), err1, err2);
  }
}


int TranslateToX(int i, int j, int n) {
  return j;
}
int TranslateToY(int i, int j, int n) {
  return n + 1 - i;
}

// void plotCovMatrix(TString file, TString label1, TString label2) {
//   ModTDRStyle();
//   gStyle->SetPaintTextFormat(".3f");

//   TFile f(file);

//   TH2D *h_cov1 = (TH2D*)gDirectory->Get(label1+"_h_cov");
//   TH2D *h_cov2 = (TH2D*)gDirectory->Get(label2+"_h_cov");
//   TH2D *h_cor1 = (TH2D*)gDirectory->Get(label1+"_h_cor");
//   TH2D *h_cor2 = (TH2D*)gDirectory->Get(label2+"_h_cor");

//   TH2D *h_cov3 = (TH2D*)h_cov1->Clone("syst_h_cov");
//   h_cov3->Add(h_cov2, -1);
  
//   TH2D *h_cor3 = (TH2D*)h_cov3->Clone("syst_h_cor");

//   for (int i = 1; i <= h_cov3->GetNbinsX(); ++i) {
//     for (int j = 1; j <= h_cov3->GetNbinsY(); ++j) {
//       int n = h_cov3->GetNbinsX();
//       int bx = TranslateToX(i, j, n);
//       int by = TranslateToY(i, j, n);
//       h_cor3->SetBinContent(bx, by, h_cov3->GetBinContent(bx, by) / (
//          TMath::Sqrt(h_cov3->GetBinContent(TranslateToX(i, i, n), TranslateToY(i, i, n))) 
//        * TMath::Sqrt(h_cov3->GetBinContent(TranslateToX(j, j, n), TranslateToY(j, j, n)))));
//     }
//   }


//   drawMatrix(h_cov1, label1+"_cov");
//   drawMatrix(h_cov2, label2+"_cov");
//   drawMatrix(h_cor1, label1+"_cor");
//   drawMatrix(h_cor2, label2+"_cor");
//   drawMatrix(h_cov3, "syst_cov");
//   drawMatrix(h_cor3, "syst_cor");

//   printErrors(h_cov1, h_cov2, h_cov3);
// }


void plotCovMatrix(TString file, TString label1, TString label2) {
  ModTDRStyle();
  gStyle->SetPaintTextFormat(".3g");

  TFile f(file);

  TH2D *h_cov1 = (TH2D*)gDirectory->Get(label1+"_h_cov");
  TH2D *h_cov2 = (TH2D*)gDirectory->Get(label2+"_h_cov");
  TH2D *h_cor1 = (TH2D*)gDirectory->Get(label1+"_h_cor");
  TH2D *h_cor2 = (TH2D*)gDirectory->Get(label2+"_h_cor");

  // TH2D *h_cov3 = (TH2D*)h_cov1->Clone("syst_h_cov");
  // h_cov3->Add(h_cov2, -1);
  
  // TH2D *h_cor3 = (TH2D*)h_cov3->Clone("syst_h_cor");

  // for (int i = 1; i <= h_cov3->GetNbinsX(); ++i) {
  //   for (int j = 1; j <= h_cov3->GetNbinsY(); ++j) {
  //     int n = h_cov3->GetNbinsX();
  //     int bx = TranslateToX(i, j, n);
  //     int by = TranslateToY(i, j, n);
  //     h_cor3->SetBinContent(bx, by, h_cov3->GetBinContent(bx, by) / (
  //        TMath::Sqrt(h_cov3->GetBinContent(TranslateToX(i, i, n), TranslateToY(i, i, n))) 
  //      * TMath::Sqrt(h_cov3->GetBinContent(TranslateToX(j, j, n), TranslateToY(j, j, n)))));
  //   }
  // }


  drawMatrix(h_cov1, label1+"_cov");
  drawMatrix(h_cov2, label2+"_cov");
  drawMatrix(h_cor1, label1+"_cor");
  drawMatrix(h_cor2, label2+"_cor");
  // drawMatrix(h_cov3, "syst_cov");
  // drawMatrix(h_cor3, "syst_cor");

  printErrors(h_cov1, h_cov2);
}