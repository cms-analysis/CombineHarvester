#include "Plotting.h"
#include "Plotting_Style.h"
#include "Plotting_Contours.h"
#include "TH2F.h"
#include "TGraphAsymmErrors.h"

std::vector<TGraph *> SetupHist(TH2D *hist, TGraph2D *graph) {
  for (int i = 1; i <= hist->GetXaxis()->GetNbins(); ++i) {
    for (int j = 1; j <= hist->GetYaxis()->GetNbins(); ++j) {
      hist->SetBinContent(
          i, j, graph->Interpolate(hist->GetXaxis()->GetBinCenter(i),
                                   hist->GetYaxis()->GetBinCenter(j)));
      if (hist->GetBinContent(i, j) == 0.) hist->SetBinContent(i, j, 1E-6);
    }
  }
  TList *conts = contourFromTH2(hist, 0.05);
  std::vector<TGraph *> cgraphs;
  for (int i = 0; i < conts->GetSize(); ++i) {
    cgraphs.push_back((TGraph *)conts->At(i));
  }
  return cgraphs;
}

void plotCLs() {
  ModTDRStyle(2800, 2400, 0.06, 0.12, 0.14, 0.22);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const unsigned Number = 2;
  Double_t Red[Number] =    {1.00, 0.17};
  Double_t Green[Number] =  {1.00, 0.16};
  Double_t Blue[Number] =   {1.00, 0.47};
  Double_t Length[Number] = {0.00, 1.00};
  Int_t nb = 255;
  TColor::CreateGradientColorTable(Number, Length, Red, Green, Blue, nb);
  gStyle->SetNumberContours(nb);

  TFile f("combined_output.root");

  TTree *t =(TTree*)gDirectory->Get("limit");

  TGraph2D graph =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       //"quantileExpected > -1.1 && quantileExpected < -0.9");
                       "quantileExpected > 0.49 && quantileExpected < 0.51");

  TGraph2D graph_exp =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       "quantileExpected > 0.49 && quantileExpected < 0.51");

  TGraph2D graph_lo68 =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       "quantileExpected > 0.15 && quantileExpected < 0.16");
  TGraph2D graph_hi68 =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       "quantileExpected > 0.83 && quantileExpected < 0.84");

  TGraph2D graph_lo95 =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       "quantileExpected > 0.02 && quantileExpected < 0.03");
  TGraph2D graph_hi95 =
      TGraph2DFromTree(t, "mA", "tanb", "limit",
                       "quantileExpected > 0.97 && quantileExpected < 0.98");

  TH2D hist("hist", "hist", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> cgraphs = SetupHist(&hist, &graph);

  TH2D h_exp("h_exp", "h_exp", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> g_exp = SetupHist(&h_exp, &graph_exp);

  TH2D h_lo68("h_lo68", "h_lo68", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> g_lo68 = SetupHist(&h_lo68, &graph_lo68);

  TH2D h_hi68("h_hi68", "h_hi68", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> g_hi68 = SetupHist(&h_hi68, &graph_hi68);

  TH2D h_lo95("h_lo95", "h_lo95", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> g_lo95 = SetupHist(&h_lo95, &graph_lo95);

  TH2D h_hi95("h_hi95", "h_hi95", 91, 90, 1000, 91, 1, 59);
  std::vector<TGraph *> g_hi95 = SetupHist(&h_hi95, &graph_hi95);

  TCanvas * canv = new TCanvas("cls", "cls");
  canv->cd();
  std::vector<TPad*> pads = OnePad();
  hist.SetMinimum(0.);
  hist.SetMaximum(1.);
  hist.Draw("COLZ");

  for (unsigned i = 0; i < g_exp.size(); ++i) {
    g_exp[i]->SetLineStyle(1);
    g_exp[i]->SetLineColor(kBlue);
    g_exp[i]->SetLineWidth(3);
    g_exp[i]->Draw("L SAME");
  }

  for (unsigned i = 0; i < g_hi68.size(); ++i) {
    g_hi68[i]->SetLineStyle(7);
    g_hi68[i]->SetLineColor(kBlue);
    g_hi68[i]->SetLineWidth(3);
    g_hi68[i]->Draw("L SAME");
  }

  for (unsigned i = 0; i < g_lo68.size(); ++i) {
    g_lo68[i]->SetLineStyle(7);
    g_lo68[i]->SetLineColor(kBlue);
    g_lo68[i]->SetLineWidth(3);
    g_lo68[i]->Draw("L SAME");
  }

  for (unsigned i = 0; i < g_hi95.size(); ++i) {
    g_hi95[i]->SetLineStyle(2);
    g_hi95[i]->SetLineColor(kBlue);
    g_hi95[i]->SetLineWidth(3);
    g_hi95[i]->Draw("L SAME");
  }

  for (unsigned i = 0; i < g_lo95.size(); ++i) {
    g_lo95[i]->SetLineStyle(2);
    g_lo95[i]->SetLineColor(kBlue);
    g_lo95[i]->SetLineWidth(3);
    g_lo95[i]->Draw("L SAME");
  }

  for (unsigned i = 0; i < cgraphs.size(); ++i) {
    cgraphs[i]->SetLineStyle(1);
    cgraphs[i]->SetLineColor(kRed);
    cgraphs[i]->SetLineWidth(4);
    cgraphs[i]->Draw("L SAME");
  }

  hist.GetXaxis()->SetTitle("m_{A} (GeV)");
  hist.GetYaxis()->SetTitle("tan#beta");
  hist.GetZaxis()->SetTitle("Observed CLs");

  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], "MSSM h/H/A#rightarrow#tau#tau, #mu_{}#tau_{h} 8 TeV", 3);

  TLegend *leg = PositionedLegend(0.25, 0.20, 1, 0.025);
  leg->AddEntry(cgraphs[0], "95% CL Observed", "L");
  leg->AddEntry(g_exp[0], "Expected", "L");
  leg->AddEntry(g_lo68[0], " #pm1#sigma Expected", "L");
  leg->AddEntry(g_lo95[0], " #pm2#sigma Expected", "L");
  leg->Draw();


  FixOverlay();
  canv->Print("cls.png");
}
