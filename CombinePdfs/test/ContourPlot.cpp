#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Contours.h"
#include <vector>
#include <TFrame.h>

int main() {
  TH1::AddDirectory(0);
  ModTDRStyle();
  TCanvas* canv = new TCanvas("ma-tanb", "ma-tanb");
  std::vector<TPad*> pads = OnePad();
  contour2D("higgsCombinemhmax.MultiDimFit.mH120.root", "ma-tanb-contours.root",
            "mA", 70, 90, 1000, "tanb", 70, 1, 60);
  TLegend *legend = PositionedLegend(0.20, 0.12, 1, 0.03);
  drawContours(pads[0], "ma-tanb-contours.root", "m_{A} (GeV)", "tan#beta", legend);
  legend->Draw();
  GetAxisHist(pads[0])->GetXaxis()->SetTitleOffset(1.);

  DrawCMSLogo(pads[0], "CMS", "Preliminary", 0, 0.045, 0.035, 1.2);
  DrawTitle(pads[0], "19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)", 3);
  // drawTitle(pads[0], "H#rightarrow#tau#tau", 1);
  // pads[0]->SetLogx(1);
  // pads[0]->SetLogy(1);
  canv->Update();
  pads[0]->RedrawAxis();
  pads[0]->GetFrame()->Draw();
  canv->Print(".pdf");
  canv->Print(".png");
  return 0;
}
