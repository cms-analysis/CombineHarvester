#include <iostream>
#include <vector>
#include <map>
#include <string>
#include "TGraph.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TLatex.h"
#include "boost/lexical_cast.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/format.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/Plotting.h"
#include "CombineHarvester/CombineTools/interface/Plotting_Style.h"
// #include "Core/interface/TextElement.h"
// #include "Utilities/interface/SimpleParamParser.h"
// #include "Utilities/interface/FnRootTools.h"

namespace po = boost::program_options;

using namespace std;

void SetTGraphStyle(TGraph * gr, int color) {
    gr->SetLineStyle(11.);
    gr->SetLineWidth( 3.);
    gr->SetLineColor(color);
    gr->SetMarkerStyle(20);
    gr->SetMarkerSize(1.3);
    gr->SetMarkerColor(color);
}

// "mh:limit","quantileExpected==0.5"

TGraph ExtractExpected(TTree *limit) {
  int n = limit->Draw("mh:limit", "quantileExpected==0.5", "goff");
  TGraph gr(n, limit->GetV1(), limit->GetV2());
  gr.Sort();
  return gr;
}

struct Infos {
  std::string file;
  std::string label;
  int color;
};

int main(int /*argc*/, char* argv[]) {

  std::string ch = argv[1];
  vector<Infos> input;
  input.push_back({"parametric/higgsCombineExpected"+ch+".Asymptotic.All.root", "Parametric", 2});
  input.push_back({"parametric-binned/higgsCombineExpected"+ch+".Asymptotic.All.root", "Binned", 4});
  // input.push_back({"parametric-asimov/higgsCombineExpected"+ch+".Asymptotic.All.root", "Parametric (asimov)", 5});
  // input.push_back({"parametric-binned-asimov/higgsCombineExpected"+ch+".Asymptotic.All.root", "Binned (asimov)", 6});


  vector<TGraph> graphs;

  for (auto const& in : input) {
    TFile f(in.file.c_str());
    TTree *tree = (TTree*)f.Get("limit");
    graphs.push_back(ExtractExpected(tree));
  }

  for (unsigned i = 0; i < input.size(); ++i) {
    SetTGraphStyle(&graphs[i], input[i].color);
  }


  ModTDRStyle();
  TCanvas canv("canv","canv",600,600);
  canv.SetLogy(true);
  gStyle->SetNdivisions(505);
  canv.SetGridx(1);
  canv.SetGridy(1);
  TGraph & exp1 = graphs[0];
  exp1.GetXaxis()->SetLimits(exp1.GetX()[0]-.1, exp1.GetX()[exp1.GetN()-1]+.1);

  double min = 9999.;
  double max = 0.;
  for (int i = 0; i < exp1.GetN(); ++i) {
    double x, y;
    exp1.GetPoint(i, x, y);
    if (y < min) min = y;
    if (y > max) max = y;
  }
  exp1.SetMaximum(max*2.);
  exp1.SetMinimum(min*0.5);
  exp1.GetYaxis()->SetTitleSize(0.055);
  exp1.GetYaxis()->SetTitleOffset(1.200);
  exp1.GetYaxis()->SetLabelOffset(0.014);
  exp1.GetYaxis()->SetLabelSize(0.040);
  exp1.GetYaxis()->SetLabelFont(42);
  exp1.GetYaxis()->SetTitleFont(42);
  exp1.GetXaxis()->SetTitleSize(0.055);
  exp1.GetXaxis()->SetTitleOffset(1.100);
  exp1.GetXaxis()->SetLabelOffset(0.014);
  exp1.GetXaxis()->SetLabelSize(0.040);
  exp1.GetXaxis()->SetLabelFont(42);
  exp1.GetXaxis()->SetTitleFont(42);
  exp1.Draw("APL");

  exp1.GetXaxis()->SetTitle("m_{#Phi} [GeV]");
  exp1.GetYaxis()->SetTitle("95% CL Limit on #sigma #times B [pb]");
  for (unsigned i = 1; i < input.size(); ++i) {
    graphs[i].Draw("PLsame");
  }
  // SetTGraphStyle(&obs1, 6);
  // SetTGraphStyle(&exp2, 7);
  // SetTGraphStyle(&obs2, 8);

  // obs1.Draw("PLsame");
  // // exp2.Draw("PLsame");
  // // obs2.Draw("PLsame");

  TLegend *legend = new TLegend(0.62, 0.62, 0.93, 0.78, "", "brNDC");
  for (unsigned i = 0; i < input.size(); ++i) {
    legend->AddEntry(&graphs[i], input[i].label.c_str(), "lP");
  }
  legend->SetBorderSize(1);
  legend->SetTextFont(42);
  legend->SetLineColor(0);
  legend->SetLineStyle(1);
  legend->SetLineWidth(1);
  legend->SetFillColor(0);
  legend->SetFillStyle(1001);
  legend->Draw();

  TLatex *title_latex = new TLatex();
  title_latex->SetNDC();
  title_latex->SetTextSize(0.035);
  title_latex->SetTextFont(62);
  title_latex->SetTextAlign(31);
  double height = 0.94;
  title_latex->DrawLatex(0.95,height,"19.7 fb^{-1} (8 TeV)");
  title_latex->SetTextAlign(11);
  title_latex->DrawLatex(0.17,height,"H#rightarrow#tau#tau");
  title_latex->SetTextSize(0.06);
  title_latex->DrawLatex(0.78, 0.84, "#mu#tau_{h}");

  canv.SaveAs((ch+"_comparison.pdf").c_str());

  return 0;
}

