#include <string>
#include <vector>
#include <TFile.h>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"
#include "TCanvas.h"
#include "TFrame.h"

using namespace std;

int main() {
  ModTDRStyle();

  ch::CombineHarvester cb;
  cb.SetVerbosity(0);
  cb.ParseDatacard("output/CMSDAS/hgg_8TeV_MVA_cat0145.txt", "hgg", "8TeV",
                   "hgg", 0, "*");

  cb.RenameParameter("pdf_data_pol_model_8TeV_cat0_norm",
                     "shapeBkg_bkg_mass_cat0__norm");
  cb.RenameParameter("pdf_data_pol_model_8TeV_cat1_norm",
                     "shapeBkg_bkg_mass_cat1__norm");
  cb.RenameParameter("pdf_data_pol_model_8TeV_cat4_norm",
                     "shapeBkg_bkg_mass_cat4__norm");
  cb.RenameParameter("pdf_data_pol_model_8TeV_cat5_norm",
                     "shapeBkg_bkg_mass_cat5__norm");

  cb.SetPdfBins(300);

  ch::Parameter mh;
  mh.set_name("MH");
  mh.set_val(125);
  mh.set_err_d(0);
  mh.set_err_u(0);
  cb.UpdateParameters({mh});

  RooFitResult fitresult =
      ch::OpenFromTFile<RooFitResult>("output/CMSDAS/hgg_mlfit.root:fit_s");
  cb.UpdateParameters(&fitresult);

  ch::CombineHarvester cb_sig = cb.cp();
  cb_sig.bin({"cat4"}).signals();

  ch::CombineHarvester cb_bkg = cb.cp();
  cb_bkg.bin({"cat4"}).backgrounds();


  TFile fout("hgg_output.root", "RECREATE");
  TH1F sig_shape = cb_sig.GetShapeWithUncertainty(&fitresult, 500);
  sig_shape.SetName("sig");
  TH1F bkg_shape = cb_bkg.GetShapeWithUncertainty(&fitresult, 500);
  bkg_shape.SetName("bkg");
  TH1F data = cb_sig.GetObservedShape();
  sig_shape.Write();
  bkg_shape.Write();
  data.Write();


  TH1::AddDirectory(0);
  TString canvName = "FigExample";


  TCanvas* canv = new TCanvas(canvName, canvName);
  canv->cd();

  std::vector<TPad*> pads = OnePad();

  data.Rebin(2);
  sig_shape.Scale(data.GetBinWidth(1) / sig_shape.GetBinWidth(1));
  bkg_shape.Scale(data.GetBinWidth(1) / bkg_shape.GetBinWidth(1));

  TH1F err_shape = bkg_shape;

  std::vector<TH1*> h = CreateAxisHists(1, &data);
  h[0]->GetXaxis()->SetTitleOffset(1.0);
  StandardAxes(h[0]->GetXaxis(), h[0]->GetYaxis(), "m_{#gamma#gamma}", "GeV");
  h[0]->Draw("axis");

  err_shape.SetFillColor(17);
  err_shape.SetMarkerSize(0);
  err_shape.Draw("E3SAME");

  sig_shape.Add(&bkg_shape);
  sig_shape.SetLineColor(4);
  sig_shape.SetLineWidth(3);
  sig_shape.Draw("SAME HIST C");

  bkg_shape.SetLineColor(2);
  bkg_shape.SetLineWidth(3);
  bkg_shape.Draw("SAME HIST C");

  data.Draw("esamex0");

  FixTopRange(pads[0], GetPadYMax(pads[0]), 0.15);
  // DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "CombineHarvester", 1);
  DrawTitle(pads[0], "hgg", 3);
  // DrawTitle(pads[0], "H#rightarrow#gamma#gamma", 1);
  TLegend *legend = PositionedLegend(0.35, 0.23, 3, 0.03);
  legend->SetTextFont(42);
  FixBoxPadding(pads[0], legend, 0.05);
  legend->AddEntry(&data, "Observed", "pe");
  legend->AddEntry(&bkg_shape, "Background", "l");
  legend->AddEntry(&err_shape, "Uncertainty", "f");
  legend->AddEntry(&sig_shape, "SM H(125 GeV)#rightarrow#gamma#gamma", "l");
  legend->Draw();

  canv->Update();
  pads[0]->RedrawAxis();
  pads[0]->GetFrame()->Draw();
  canv->SaveAs("hgg.pdf");

  fout.Close();
}
