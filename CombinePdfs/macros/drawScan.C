#include "lotting_Style.h"
#include "Plotting.h"
#include "TH2F.h"
#include "TPad.h"

using namespace std;


TH2F* create_ggA_ggH_Sum(TFile *f);
TH2F* create_ggh(TFile *f);
TH2F* create_bbA_bbH_Sum(TFile *f);

void drawScan() {
  ModTDRStyle(1400, 1200, 0.06, 0.12, 0.14, 0.22);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const unsigned Number = 2;
  Double_t Red[Number] =    {0.17, 1.00};
  Double_t Green[Number] =  {0.16, 1.00};
  Double_t Blue[Number] =   {0.47, 1.00};
  Double_t Length[Number] = {0.00, 1.00};
  Int_t nb = 255;
  // gStyle->SetPalette(56);
  TColor::CreateGradientColorTable(Number, Length, Red, Green, Blue, nb);
  gStyle->SetNumberContours(nb);
  TCanvas canv_h_var;
  vector<TPad *> pads = OnePad();
  TFile f_in("out.mhmodp-8TeV-tanbHigh-nnlo.root");
  //TH2F *h_var = create_ggA_ggH_Sum(&f_in);
  // TH2F *h_var = create_ggh(&f_in);
  TH2F *h_var = create_bbA_bbH_Sum(&f_in);
  h_var->Smooth();
  h_var->Smooth();

  double p_ma = 800;
  double p_tanb = 20;

  std::cout << "mA: " << p_ma << ", tanb: " << p_tanb << " = " << h_var->GetBinContent(h_var->GetXaxis()->FindBin(p_ma), h_var->GetYaxis()->FindBin(p_tanb)) << "\n";

  // pads[0]->SetLogz(true);
  h_var->GetXaxis()->SetTitle("m_{A} (GeV)");
  h_var->GetYaxis()->SetTitle("tan#beta");
  h_var->GetZaxis()->SetTitleOffset(1.3);
  h_var->GetZaxis()->SetNdivisions(510);
  std::cout << h_var->GetMinimum() << "\t" << h_var->GetMaximum() << "\n";
  h_var->Draw("COLZ");
  DrawTitle(pads[0], "m_{h}^{mod+} Scenario", 1);
  FixOverlay();
  canv_h_var.SaveAs(TString(h_var->GetTitle())+".png");
  f_in.Close();
}

TH2F* create_ggA_ggH_Sum(TFile *f) {
  f->cd();
  TH2F *h_var = (TH2F *)gDirectory->Get("h_brtautau_H");
  TH2F *h_2 = (TH2F *)gDirectory->Get("h_ggF_xsec_H");
  TH2F *h_3 = (TH2F *)gDirectory->Get("h_brtautau_A");
  TH2F *h_4 = (TH2F *)gDirectory->Get("h_ggF_xsec_A");
  h_var->Multiply(h_2);
  h_3->Multiply(h_4);
  h_var->Add(h_3);

  for (int x = 1; x < h_var->GetNbinsX(); ++x) {
    for (int y = 1; y < h_var->GetNbinsY(); ++y) {
      double xx = h_var->GetXaxis()->GetBinCenter(x);
      double yy = h_var->GetYaxis()->GetBinCenter(y);
      if (xx > 300. && xx < 360. && yy > 0. && yy < 24.) {
        if (h_var->GetBinContent(x, y) > 0.8) h_var->SetBinContent(x, y, 0);
      }
    }
  }
  for (int x = 1; x < h_var->GetNbinsX(); ++x) {
    for (int y = 1; y < h_var->GetNbinsY(); ++y) {
      double xx = h_var->GetXaxis()->GetBinCenter(x);
      double yy = h_var->GetYaxis()->GetBinCenter(y);
      if (xx > 300. && xx < 360. && yy > 0. && yy < 24.) {
        if (h_var->GetBinContent(x, y) == 0.)
        h_var->SetBinContent(
            x, y, h_var->Interpolate(h_var->GetXaxis()->GetBinCenter(x),
                                    h_var->GetYaxis()->GetBinCenter(y)));
      }
    }
  }
  h_var->GetZaxis()->SetTitle(
      "#sigma(ggH)#timesB(H#rightarrow#tau#tau) + "
      "#sigma(ggA)#timesB(A#rightarrow#tau#tau) (pb)");
  h_var->SetMinimum(1E-6);
  h_var->SetMaximum(1E3);
  h_var->SetTitle("ggH_BR_ggA_BR");
  gPad->SetLogz(true);

  return h_var;
}

TH2F* create_ggh(TFile *f) {
  f->cd();
  TH2F *h_var = (TH2F *)gDirectory->Get("h_brtautau_h");
  TH2F *h_2 = (TH2F *)gDirectory->Get("h_ggF_xsec_h");
  h_var->Multiply(h_2);

  h_var->GetZaxis()->SetTitle("#sigma(ggh)#timesB(h#rightarrow#tau#tau) (pb)");
  h_var->SetTitle("ggh_BR");
  // h_var->SetMinimum(1E2);
  // h_var->SetMaximum(1E4);
    // gPad->SetLogz(true);
  return h_var;
}

TH2F SantanderMatching(TH2F const& h4f, TH2F const& h5f, TH2F const* mass) {
  TH2F res = h4f;
  for (int x = 1; x <= h4f.GetNbinsX(); ++x) {
    for (int y = 1; y <= h4f.GetNbinsY(); ++y) {
      double mh =
          mass ? mass->GetBinContent(x, y) : h4f.GetXaxis()->GetBinCenter(x);
      double t = log(mh / 4.75) - 2.;
      double fourflav = h4f.GetBinContent(x, y);
      double fiveflav = h5f.GetBinContent(x, y);
      double sigma = (1. / (1. + t)) * (fourflav + t * fiveflav);
      res.SetBinContent(x, y, sigma);
    }
  }
  return res;
}


TH2F* create_bbA_bbH_Sum(TFile *f) {
  f->cd();
  TH2F *h_0 = (TH2F *)gDirectory->Get("h_mH");
  TH2F *h_1 = (TH2F *)gDirectory->Get("h_brtautau_H");
  TH2F *h_2 = (TH2F *)gDirectory->Get("h_bbH_xsec_H");
  TH2F *h_3 = (TH2F *)gDirectory->Get("h_bbH4f_xsec_H");
  TH2F *h_4 = (TH2F *)gDirectory->Get("h_brtautau_A");
  TH2F *h_5 = (TH2F *)gDirectory->Get("h_bbH_xsec_A");
  TH2F *h_6 = (TH2F *)gDirectory->Get("h_bbH4f_xsec_A");
  TH2F bbH = SantanderMatching(*h_3, *h_2, h_0);
  TH2F bbA = SantanderMatching(*h_6, *h_5, NULL);
  h_1->Multiply(&bbH);
  h_4->Multiply(&bbA);
  h_1->Add(h_4);

  h_1->GetZaxis()->SetTitle(
      "#sigma(bbH)#timesB(H#rightarrow#tau#tau) + "
      "#sigma(bbA)#timesB(A#rightarrow#tau#tau) (pb)");
  // h_1->SetMinimum(1E-6);
  // h_1->SetMaximum(1E3);
  h_1->SetTitle("bbH_BR_bbA_BR");
  gPad->SetLogz(true);

  return h_1;
}
