#include <vector>
#include <string>
#include <set>
#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TLine.h"
#include "TLegend.h"
#include "TString.h"
#include "TLatex.h"

#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/JsonTools.h"
#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"

std::vector<double> GetCrossings(TGraph const& g, double cross) {
  std::vector<double> result;
  unsigned n = g.GetN();
  double x1 = 0;
  double y1 = 0;
  double x2 = 0;
  double y2 = 0;
  for (unsigned i = 0; i < (n-1); ++i) {
    g.GetPoint(i, x1, y1);
    g.GetPoint(i+1, x2, y2);
    if ( (y2-cross)*(y1-cross) < 0.0 ) {
      double m = (y2-y1)/(x2-x1);
      double c = (y1 - m * x1);
      double xc = (cross - c) / m;
      result.push_back(xc);
      std::cout << "Crossing at " << xc << std::endl;
    }
  }
  return result;
}

// The settings for drawing each scan component
struct Scan {
  std::string file;
  std::string tree;
  std::string label;
  int color;
  TGraph * gr;
  double bestfit;
  double uncert;
};

int main(int argc, char* argv[]) {
  Json::Value const js = ch::MergedJson(argc, argv);

  TH1::AddDirectory(0);
  ModTDRStyle();
  TCanvas canv(js.get("output", "scan").asCString(), "");
  std::vector<TPad*> pads = OnePad();
  std::vector<TLine *> lines;


  std::vector<Scan> scans;


  for (auto it = js["env"].begin(); it != js["env"].end(); ++it) {
    std::cout << (*it).asString() << "\n";
  }

  std::string xvar = js.get("xvar", "r").asString();
  std::string yvar = js.get("yvar", "2. * deltaNLL").asString();
  bool re_zero_graphs = js.get("rezero", true).asBool();
  double cross = js.get("crossing", 1.0).asFloat();
  int precision = js.get("precision", 2).asInt();

  std::set<std::string> draw;
  for (unsigned i = 0; i < js["draw"].size(); ++i) {
    draw.insert(js["draw"][i].asString());
  }


  for (unsigned i = 0; i < js["scans"].size(); ++i) {
    Json::Value const sc_js = js["scans"][i];
    if (!draw.count(sc_js["label"].asString())) continue;
    Scan scan;
    scan.file = sc_js["file"].asString();
    scan.tree = sc_js["tree"].asString();
    scan.color = sc_js["color"].asInt();
    scan.label = sc_js["legend"].asString();
    scans.push_back(scan);
  }
  if (scans.size() == 0) return 1;

  TLegend *leg =
      PositionedLegend(0.4, 0.15 * float(scans.size()) / 1.7, 2, 0.03);
  leg->SetTextSize(0.035);

  for (unsigned i = 0; i < scans.size(); ++i) {
    Scan & sc = scans[i];
    TFile f(sc.file.c_str());
    TTree *t = static_cast<TTree*>(f.Get(sc.tree.c_str()));
    sc.gr = new TGraph(TGraphFromTree(t, xvar, yvar));
    sc.gr->Sort();
    for (int j = 0; j < sc.gr->GetN(); ++j) {
      if (std::fabs(sc.gr->GetY()[j] - 0.) < 1E-5) sc.bestfit = sc.gr->GetX()[j];
    }
    if (re_zero_graphs) ReZeroTGraph(sc.gr);
    auto x1 = GetCrossings(*(sc.gr), 1.0);
    TString res;
    if (x1.size() == 2) {
      sc.uncert = (x1[1]-x1[0])/2.0;
      std::cout << "Best fit is: " << sc.bestfit << " +/- " << sc.uncert << "\n";
      lines.push_back(new TLine(x1[0], 0, x1[0], 1.0));
      lines.back()->SetLineColor(sc.color);
      lines.back()->SetLineWidth(2);
      lines.push_back(new TLine(x1[1], 0, x1[1], 1.0));
      lines.back()->SetLineColor(sc.color);
      lines.back()->SetLineWidth(2);
      res = TString::Format(
          TString::Format("%%.%if#pm%%.%if", precision, precision), sc.bestfit,
          sc.uncert);
      TString leg_text = "#splitline{"+sc.label+"}{"+res+"}";
      sc.gr->SetLineColor(sc.color);
      sc.gr->SetLineWidth(3);
      leg->AddEntry(sc.gr, leg_text, "L");
    }
  }


  TH1 *axis = CreateAxisHist(scans[0].gr, true);
  axis->GetXaxis()->SetTitle(js["x_axis_title"].asCString());
  axis->GetYaxis()->SetTitle(js["y_axis_title"].asCString());
  axis->Draw();

  for (unsigned i = 0; i < scans.size(); ++i) {
    Scan & sc = scans[i];
    sc.gr->Draw("LSAME");
  }

  leg->Draw();

  double xmin = axis->GetXaxis()->GetXmin();
  double xmax = axis->GetXaxis()->GetXmax();

  lines.push_back(new TLine(xmin, cross, xmax, cross));
  lines.back()->SetLineColor(2);
  for (auto l : lines) l->Draw();

  DrawCMSLogo(pads[0], "CMS", js["cms_label"].asString(), 0);
  DrawTitle(pads[0], js["title_right"].asString(), 3);

  canv.Update();
  canv.SaveAs(".pdf");
  canv.SaveAs(".png");
  return 0;
}
