
#include <TFile.h>
#include <TString.h>
#include <TH1.h>
#include <THStack.h>
#include <TAxis.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TMath.h>
#include <TROOT.h>
#include <TStyle.h>

#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <iomanip>
#include <assert.h>

TH1* loadHistogram(TFile* inputFile, const std::string& directory, const std::string& histogramName)
{
  std::string histogramName_full = Form("%s/%s", directory.data(), histogramName.data());
  TH1* histogram = dynamic_cast<TH1*>(inputFile->Get(histogramName_full.data()));
  if ( !histogram ) {
    std::cerr << "Failed to load histogram = " << histogramName_full << " from file = " << inputFile->GetName() << " !!" << std::endl;
    assert(0);
  }
  if ( !histogram->GetSumw2N() ) histogram->Sumw2();
  return histogram;
}

void checkCompatibleBinning(const TH1* histogram1, const TH1* histogram2)
{
  if ( histogram1 && histogram2 ) {
    if ( !(histogram1->GetNbinsX() == histogram2->GetNbinsX()) ) {
      std::cerr << "Histograms " << histogram1->GetName() << " and " << histogram2->GetName() << " have incompatible binning !!" << std::endl;
      std::cerr << " (NbinsX: histogram1 = " << histogram1->GetNbinsX() << ", histogram2 = " << histogram2->GetNbinsX() << ")" << std::endl;
      assert(0);
    }
    const TAxis* xAxis1 = histogram1->GetXaxis();
    const TAxis* xAxis2 = histogram2->GetXaxis();
    int numBins = xAxis1->GetNbins();
    for ( int iBin = 1; iBin <= numBins; ++iBin ) {
      double binWidth = 0.5*(xAxis1->GetBinWidth(iBin) + xAxis2->GetBinWidth(iBin));
      double dBinLowEdge = xAxis1->GetBinLowEdge(iBin) - xAxis2->GetBinLowEdge(iBin);
      double dBinUpEdge = xAxis1->GetBinUpEdge(iBin) - xAxis2->GetBinUpEdge(iBin);
      if ( !(dBinLowEdge < (1.e-3*binWidth) && dBinUpEdge < (1.e-3*binWidth)) ) {
	std::cerr << "Histograms " << histogram1->GetName() << " and " << histogram2->GetName() << " have incompatible binning !!" << std::endl;
	std::cerr << " (bin #" << iBin << ": histogram1 = " << xAxis1->GetBinLowEdge(iBin) << ".." << xAxis1->GetBinUpEdge(iBin) << ","
		  << " histogram2 = " << xAxis2->GetBinLowEdge(iBin) << ".." << xAxis2->GetBinUpEdge(iBin) << "" << std::endl;
	assert(0);
      }
    }
  }
}

TH1* divideHistogramByBinWidth(TH1* histogram)
{
  std::string histogramDensityName = Form("%s_density", histogram->GetName());
  TH1* histogramDensity = (TH1*)histogram->Clone(histogramDensityName.data());
  TAxis* xAxis = histogram->GetXaxis();
  int numBins = xAxis->GetNbins();
  for ( int iBin = 1; iBin <= numBins; ++iBin ) {
    double binContent = histogram->GetBinContent(iBin);
    double binError = histogram->GetBinError(iBin);
    double binWidth = xAxis->GetBinWidth(iBin);
    histogramDensity->SetBinContent(iBin, binContent/binWidth);
    histogramDensity->SetBinError(iBin, binError/binWidth);
  }
  return histogramDensity;
}

void addLabel_CMS_luminosity(double x0_cms, double y0, double x0_luminosity)
{
  TPaveText* label_cms = new TPaveText(x0_cms, y0 + 0.050, x0_cms + 0.1900, y0 + 0.100, "NDC");
  label_cms->AddText("CMS Preliminary");
  label_cms->SetTextFont(61);
  label_cms->SetTextAlign(23);
  label_cms->SetTextSize(0.055);
  label_cms->SetTextColor(1);
  label_cms->SetFillStyle(0);
  label_cms->SetBorderSize(0);
  label_cms->Draw();
  
  TPaveText* label_luminosity = new TPaveText(x0_luminosity, y0 + 0.050, x0_luminosity + 0.1900, y0 + 0.100, "NDC");
  label_luminosity->AddText("2.26 fb^{-1} (13 TeV)");
  label_luminosity->SetTextAlign(13);
  label_luminosity->SetTextSize(0.050);
  label_luminosity->SetTextColor(1);
  label_luminosity->SetFillStyle(0);
  label_luminosity->SetBorderSize(0);
  label_luminosity->Draw();
}

void makePlot(double canvasSizeX, double canvasSizeY,
	      TH1* histogramTTH, 
	      TH1* histogramData, 
	      TH1* histogramTTV,
	      TH1* histogramWZ,
	      TH1* histogramRares,
	      TH1* histogramFakes,
	      TH1* histogramFlips,
	      TH1* histogramBgrSum,
	      TH1* histogramBgrUncertainty,		
	      const std::string& xAxisTitle, double xAxisOffset,
	      bool useLogScale, double yMin, double yMax, const std::string& yAxisTitle, double yAxisOffset,
	      const std::string& outputFileName)
{
  TH1* histogramTTH_density = 0;
  if ( histogramTTH ) {
    if ( histogramData ) checkCompatibleBinning(histogramTTH, histogramData);
    histogramTTH_density = divideHistogramByBinWidth(histogramTTH);
  }
  TH1* histogramData_density = 0;
  if ( histogramData ) {
    histogramData_density = divideHistogramByBinWidth(histogramData);      
  }
  TH1* histogramTTV_density = 0;
  if ( histogramTTV ) {
    if ( histogramData ) checkCompatibleBinning(histogramTTV, histogramData);
    histogramTTV_density = divideHistogramByBinWidth(histogramTTV);
  }    
  TH1* histogramWZ_density = 0;
  if ( histogramWZ ) {
    if ( histogramData ) checkCompatibleBinning(histogramWZ, histogramData);
    histogramWZ_density = divideHistogramByBinWidth(histogramWZ);
  }
  TH1* histogramRares_density = 0;
  if ( histogramRares ) {
    if ( histogramData ) checkCompatibleBinning(histogramRares, histogramData);
    histogramRares_density = divideHistogramByBinWidth(histogramRares);
  }    
  TH1* histogramFakes_density = 0;
  if ( histogramFakes ) {
    if ( histogramData ) checkCompatibleBinning(histogramFakes, histogramData);
    histogramFakes_density = divideHistogramByBinWidth(histogramFakes);
  }
  TH1* histogramFlips_density = 0;
  if ( histogramFlips ) {
    if ( histogramData ) checkCompatibleBinning(histogramFlips, histogramData);
    histogramFlips_density = divideHistogramByBinWidth(histogramFlips); 
  }
  TH1* histogramBgrSum_density = 0;
  if ( histogramBgrSum ) {
    if ( histogramData ) checkCompatibleBinning(histogramBgrSum, histogramData);
    histogramBgrSum_density = divideHistogramByBinWidth(histogramBgrSum); 
  }
  TH1* histogramBgrUncertainty_density = 0;
  if ( histogramBgrUncertainty ) {
    if ( histogramData ) checkCompatibleBinning(histogramBgrUncertainty, histogramData);
    histogramBgrUncertainty_density = divideHistogramByBinWidth(histogramBgrUncertainty);
  }
  
  TCanvas* canvas = new TCanvas("canvas", "", canvasSizeX, canvasSizeY);
  canvas->SetFillColor(10);
  canvas->SetFillStyle(4000);
  canvas->SetFillColor(10);
  canvas->SetTicky();
  canvas->SetBorderSize(2);  
  canvas->SetLeftMargin(0.12);
  canvas->SetBottomMargin(0.12);
  
  TPad* topPad = new TPad("topPad", "topPad", 0.00, 0.35, 1.00, 1.00);
  topPad->SetFillColor(10);
  topPad->SetTopMargin(0.065);
  topPad->SetLeftMargin(0.15);
  topPad->SetBottomMargin(0.03);
  topPad->SetRightMargin(0.05);
  topPad->SetLogy(useLogScale);
  
  TPad* bottomPad = new TPad("bottomPad", "bottomPad", 0.00, 0.00, 1.00, 0.35);
  bottomPad->SetFillColor(10);
  bottomPad->SetTopMargin(0.02);
  bottomPad->SetLeftMargin(0.15);
  bottomPad->SetBottomMargin(0.31);
  bottomPad->SetRightMargin(0.05);
  bottomPad->SetLogy(false);
  
  canvas->cd();
  topPad->Draw();
  topPad->cd();
  
  TAxis* xAxis_top = histogramData_density->GetXaxis();
  xAxis_top->SetTitle(xAxisTitle.data());
  xAxis_top->SetTitleOffset(xAxisOffset);
  xAxis_top->SetLabelColor(10);
  xAxis_top->SetTitleColor(10);
    
  TAxis* yAxis_top = histogramData_density->GetYaxis();
  yAxis_top->SetTitle(yAxisTitle.data());
  yAxis_top->SetTitleOffset(yAxisOffset);
  yAxis_top->SetTitleSize(0.085);
  yAxis_top->SetLabelSize(0.05);
  yAxis_top->SetTickLength(0.04);  
  
  TLegend* legend = new TLegend(0.19, 0.45, 0.57, 0.92, NULL, "brNDC");
  legend->SetFillStyle(0);
  legend->SetBorderSize(0);
  legend->SetFillColor(10);
  legend->SetTextSize(0.055);
  
  histogramData_density->SetTitle("");
  histogramData_density->SetStats(false);
  histogramData_density->SetMaximum(yMax);
  histogramData_density->SetMinimum(yMin);
  histogramData_density->SetMarkerStyle(20);
  histogramData_density->SetMarkerSize(2);
  histogramData_density->SetMarkerColor(kBlack);
  histogramData_density->SetLineColor(kBlack);
  legend->AddEntry(histogramData_density, "Observed", "p");    
  
  histogramData_density->Draw("ep");
  
  legend->AddEntry(histogramTTH_density, "t#bar{t}H", "l");

  histogramTTV_density->SetTitle("");
  histogramTTV_density->SetStats(false);
  histogramTTV_density->SetMaximum(yMax);
  histogramTTV_density->SetMinimum(yMin);
  histogramTTV_density->SetFillColor(kOrange - 4);
  legend->AddEntry(histogramTTV_density, "t#bar{t}+V", "f");

  histogramWZ_density->SetFillColor(kRed + 2); 
  legend->AddEntry(histogramWZ_density, "WZ", "f");

  histogramRares_density->SetFillColor(kBlue - 8); 
  legend->AddEntry(histogramRares_density, "Rares", "f");

  histogramFakes_density->SetFillColor(kMagenta - 10); 
  legend->AddEntry(histogramFakes_density, "Fakes", "f");

  histogramFlips_density->SetFillColor(628); 
  legend->AddEntry(histogramFlips_density, "Charge flips", "f");

  THStack* histogramStack_density = new THStack("stack", "");
  histogramStack_density->Add(histogramFlips_density);
  histogramStack_density->Add(histogramRares_density);
  histogramStack_density->Add(histogramWZ_density);
  histogramStack_density->Add(histogramFakes_density);
  histogramStack_density->Add(histogramTTV_density);
  histogramStack_density->Draw("histsame");
  
  histogramBgrUncertainty_density->SetFillColor(kBlack);
  histogramBgrUncertainty_density->SetFillStyle(3344);    
  histogramBgrUncertainty_density->Draw("e2same");
  legend->AddEntry(histogramBgrUncertainty_density, "Uncertainty", "f");

  histogramTTH_density->SetLineWidth(2);
  histogramTTH_density->SetLineStyle(1);
  histogramTTH_density->SetLineColor(kBlue);
  histogramTTH_density->Draw("histsame");
  
  histogramData_density->Draw("epsame");
  histogramData_density->Draw("axissame");
  
  legend->Draw();
  
  addLabel_CMS_luminosity(0.2050, 0.9225, 0.6850);
  
  canvas->cd();
  bottomPad->Draw();
  bottomPad->cd();
  
  TH1* histogramRatio = (TH1*)histogramData->Clone("histogramRatio");
  histogramRatio->Reset();
  if ( !histogramRatio->GetSumw2N() ) histogramRatio->Sumw2();
  checkCompatibleBinning(histogramRatio, histogramBgrSum);
  histogramRatio->Divide(histogramData, histogramBgrSum);
  int numBins_bottom = histogramRatio->GetNbinsX();
  for ( int iBin = 1; iBin <= numBins_bottom; ++iBin ) {
    double binContent = histogramRatio->GetBinContent(iBin);
    if ( histogramData && histogramData->GetBinContent(iBin) >= 0. ) histogramRatio->SetBinContent(iBin, binContent - 1.0);
    else histogramRatio->SetBinContent(iBin, -10.);
  }
  histogramRatio->SetTitle("");
  histogramRatio->SetStats(false);
  histogramRatio->SetMinimum(-0.50);
  histogramRatio->SetMaximum(+0.50);
  histogramRatio->SetMarkerStyle(histogramData_density->GetMarkerStyle());
  histogramRatio->SetMarkerSize(histogramData_density->GetMarkerSize());
  histogramRatio->SetMarkerColor(histogramData_density->GetMarkerColor());
  histogramRatio->SetLineColor(histogramData_density->GetLineColor());
  histogramRatio->Draw("ep");
  
  TAxis* xAxis_bottom = histogramRatio->GetXaxis();
  xAxis_bottom->SetTitle(xAxis_top->GetTitle());
  xAxis_bottom->SetLabelColor(1);
  xAxis_bottom->SetTitleColor(1);
  xAxis_bottom->SetTitleOffset(1.20);
  xAxis_bottom->SetTitleSize(0.13);
  xAxis_bottom->SetLabelOffset(0.02);
  xAxis_bottom->SetLabelSize(0.10);
  xAxis_bottom->SetTickLength(0.055);
  
  TAxis* yAxis_bottom = histogramRatio->GetYaxis();
  yAxis_bottom->SetTitle("#frac{Data - Simulation}{Simulation}");
  yAxis_bottom->SetTitleOffset(0.80);
  yAxis_bottom->SetNdivisions(505);
  yAxis_bottom->CenterTitle();
  yAxis_bottom->SetTitleSize(0.09);
  yAxis_bottom->SetLabelSize(0.10);
  yAxis_bottom->SetTickLength(0.04);  
  
  TH1* histogramRatioUncertainty = (TH1*)histogramBgrUncertainty->Clone("histogramRatioUncertainty");
  if ( !histogramRatioUncertainty->GetSumw2N() ) histogramRatioUncertainty->Sumw2();
  checkCompatibleBinning(histogramRatioUncertainty, histogramBgrUncertainty);
  histogramRatioUncertainty->Divide(histogramBgrSum);
  int numBins = histogramRatioUncertainty->GetNbinsX();
  for ( int iBin = 1; iBin <= numBins; ++iBin ) {
    double binContent = histogramRatioUncertainty->GetBinContent(iBin);
    histogramRatioUncertainty->SetBinContent(iBin, binContent - 1.0);
  }
  histogramRatioUncertainty->SetFillColor(histogramBgrUncertainty_density->GetFillColor());
  //histogramRatioUncertainty->SetFillStyle(histogramBgrUncertainty_density->GetFillStyle());    
  histogramRatioUncertainty->SetFillStyle(3644);    
  
  TF1* line = new TF1("line","0", xAxis_bottom->GetXmin(), xAxis_bottom->GetXmax());
  line->SetLineStyle(3);
  line->SetLineWidth(1);
  line->SetLineColor(kBlack);
  line->Draw("same");
  
  histogramRatioUncertainty->Draw("e2same");
  
  histogramRatio->Draw("epsame");
  
  canvas->Update();
  size_t idx = outputFileName.find(".");
  std::string outputFileName_plot(outputFileName, 0, idx);
  if ( useLogScale ) outputFileName_plot.append("_log");
  else outputFileName_plot.append("_linear");
  if ( idx != std::string::npos ) canvas->Print(std::string(outputFileName_plot).append(std::string(outputFileName, idx)).data());
  canvas->Print(std::string(outputFileName_plot).append(".png").data());
  canvas->Print(std::string(outputFileName_plot).append(".pdf").data());
  canvas->Print(std::string(outputFileName_plot).append(".root").data());
  
  delete histogramTTH_density;
  delete histogramData_density;
  delete histogramTTV_density;
  delete histogramWZ_density;
  delete histogramRares_density;
  delete histogramFakes_density;
  delete histogramFlips_density;
  delete histogramBgrSum_density;
  //delete histogramBgrUncertainty_density;
  delete histogramStack_density;
  delete legend;
  delete topPad;
  delete histogramRatio;
  delete histogramRatioUncertainty;
  delete line;
  delete bottomPad;    
  delete canvas;
}

void makePostFitPlots_2lss_1tau()
{
  gROOT->SetBatch(true);

  TH1::AddDirectory(false);

  std::vector<std::string> categories;
  categories.push_back("ttH_2lss_1tau_prefit");
  categories.push_back("ttH_2lss_1tau_postfit");

  std::string inputFilePath = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/ttH_htt/";
  std::map<std::string, std::string> inputFileNames; // key = category
  inputFileNames["ttH_2lss_1tau_prefit"]  = "ttH_2lss_1tau_shapes.root";
  inputFileNames["ttH_2lss_1tau_postfit"] = "ttH_2lss_1tau_shapes.root";
  
  for ( std::vector<std::string>::const_iterator category = categories.begin();
	category != categories.end(); ++category ) {
    std::string inputFileName_full = Form("%s%s", inputFilePath.data(), inputFileNames[*category].data());
    TFile* inputFile = new TFile(inputFileName_full.data());
    if ( !inputFile ) {
      std::cerr << "Failed to open input file = " << inputFileName_full << " !!" << std::endl;
      assert(0);
    }

    TH1* histogramTTH_hww = loadHistogram(inputFile, *category, "ttH_hww");
    TH1* histogramTTH_hzz = loadHistogram(inputFile, *category, "ttH_hzz");
    TH1* histogramTTH_htt = loadHistogram(inputFile, *category, "ttH_htt");
    TString histogramNameTTH = TString(histogramTTH_hww->GetName()).ReplaceAll("_hww", "_sum");
    TH1* histogramTTH = (TH1*)histogramTTH_hww->Clone(histogramNameTTH.Data());
    histogramTTH->Add(histogramTTH_hzz);
    histogramTTH->Add(histogramTTH_htt);

    TH1* histogramData = loadHistogram(inputFile, *category, "data_obs");

    TH1* histogramTTW = loadHistogram(inputFile, *category, "TTW");
    TH1* histogramTTZ = loadHistogram(inputFile, *category, "TTZ");
    TString histogramNameTTV = "TTV";
    TH1* histogramTTV = (TH1*)histogramTTW->Clone(histogramNameTTV.Data());
    histogramTTV->Add(histogramTTZ);

    //TH1* histogramWZ = loadHistogram(inputFile, *category, "WZ");
    TH1* histogramWZ = loadHistogram(inputFile, *category, "EWK");

    TH1* histogramRares = loadHistogram(inputFile, *category, "Rares");

    TH1* histogramFakes = loadHistogram(inputFile, *category, "fakes_data");

    TH1* histogramFlips = loadHistogram(inputFile, *category, "flips_data");

    TH1* histogramBgrSum = loadHistogram(inputFile, *category, "TotalBkg");
    TH1* histogramBgrUncertainty = (TH1*)histogramBgrSum->Clone("TotalBkgErr");

    std::string outputFilePath = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/ttH_htt/macros";
    std::string outputFileName = Form("%s/plots/makePostFitPlots_%s.pdf", outputFilePath.data(), category->data());
    makePlot(800, 900,
	     histogramTTH,
	     histogramData, 
	     histogramTTV,
	     histogramWZ,
	     histogramRares,
	     histogramFakes,
	     histogramFlips,
	     histogramBgrSum,
	     histogramBgrUncertainty,	
	     "Discriminant", 0.9,
	     false, 1.e-2, 1.e+2, "Events", 0.9,
	     outputFileName);

    delete histogramTTH;
    delete histogramTTV;
    delete histogramBgrUncertainty;

    delete inputFile;
  }
}

