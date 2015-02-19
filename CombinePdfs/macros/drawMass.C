#include "Plotting_Style.h"
#include "Plotting.h"
#include "TH2F.h"
#include "TPad.h"

using namespace std;

void drawMass() {
  ModTDRStyle(700, 600, 0.06, 0.12, 0.14, 0.22);
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
  TH2F *h_var = (TH2F*)gDirectory->Get("h_mH");
  // h_var->Smooth();
  // h_var->Smooth();

  double p_ma = 800;
  double p_tanb = 20;

  std::cout << "mA: " << p_ma << ", tanb: " << p_tanb << " = " << h_var->GetBinContent(h_var->GetXaxis()->FindBin(p_ma), h_var->GetYaxis()->FindBin(p_tanb)) << "\n";

  // pads[0]->SetLogz(true);
  h_var->GetXaxis()->SetTitle("m_{A} (GeV)");
  h_var->GetYaxis()->SetTitle("tan#beta");
  h_var->GetZaxis()->SetTitle("m_{H} (GeV)");
  h_var->GetZaxis()->SetTitleOffset(1.3);
  h_var->GetZaxis()->SetNdivisions(510);
  std::cout << h_var->GetMinimum() << "\t" << h_var->GetMaximum() << "\n";
  h_var->Draw("COLZ");
  DrawTitle(pads[0], "m_{h}^{mod+} Scenario", 1);
  FixOverlay();
  canv_h_var.SaveAs(TString(h_var->GetTitle())+".png");
  f_in.Close();
}
