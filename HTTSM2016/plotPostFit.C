////////////////////////////////////////////////////
////////////////////////////////////////////////////
TCanvas *getDefaultCanvas(float x=10,float y=30,float w=750,float h=700){

  TCanvas *c1 = new TCanvas("c1","Jet LL",x,y,w,h);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetLeftMargin(0.16);
  c1->SetGrid(1,1);
  c1->SetTicky();
  //c1->SetTickx();

  return c1;

}
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
float getLumi(){

  //./.local/bin/brilcalc lumi --normtag ~lumipro/public/normtag_file/OfflineNormtagV2.json -i lumiSummary_Run2015C_16Dec2015_v1.json
  float run2015C = 17225935.728*1E-6;
  float run2015D = 2114239169.533*1E-6;
  
  //./.local/bin/brilcalc lumi --normtag /afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json -i lumiSummary_Run2016B_PromptReco_v12.json     
  float run2016B = 5879283691.513*1E-6;
  float run2016C = 2645968083.093*1E-6;
  float run2016D = 4353448810.554*1E-6;
  float run2016E = 4049732039.245*1E-6;
  float run2016F = 3121200199.632*1E-6;
  float run2016G = 6320078824.709*1E-6;


  run2016 = 35.87*1E3*1E6; //Updated Run2016 luminosity
  return run2016*1E-6; //pb-1 data for NTUPLES_05_12_2016
  return run2016B+run2016C+run2016D+run2016E+run2016F+run2016G;//pb-1 data for NTUPLES_28_09_2016
}
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
TH1F *get1DHistogram(const std::string &hName, std::string selName, int iCategory, std::string channel){

  TFile *file = new TFile("output/Blinded25112016/postfit_shapes.root");

  std::string dirName = "htt_"+channel+"_"+to_string(iCategory)+"_13TeV_"+selName;
  std::string name = hName;
  
  TH1F *h = (TH1F*)file->Get((dirName+"/"+name).c_str());
  std::cout<<dirName+"/"+name<<std::endl;
  if(!h) std::cout<<"Miss\n";
  return h;  
}
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
void setupLegend(TLegend *leg){

  //leg->SetFillStyle(4000);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.05);
}
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
THStack* plotStack(std::string varName, std::string channel, std::pair<int, std::string> category, std::string selName){

  std::cout<<"--- Drawing THStack for variable: "<<varName
	   <<" selection: "<<selName<<" "<<channel<<" "<<category.second<<std::endl;
	   
  std::string hName = varName;
  category.first += 1;
  if(category.second.find("_")!=std::string::npos) category.first += 6;

  TH1F *hggHiggs115 = 0;
  TH1F *hqqHiggs115 = 0;  
  TH1F *hggHiggs120 = 0;
  TH1F *hqqHiggs120 = 0;  
  TH1F *hggHiggs130 = 0;
  TH1F *hqqHiggs130 = 0;
  TH1F *hggHiggs135 = 0;
  TH1F *hqqHiggs135 = 0;
  
  TH1F *hggHiggs125 = get1DHistogram("ggH",selName, category.first, channel);
  TH1F *hqqHiggs125 = get1DHistogram("qqH",selName, category.first, channel);
  TH1F *hZHiggs125 = get1DHistogram("ZH",selName, category.first, channel);
  TH1F *hWHiggs125 = get1DHistogram("WH",selName, category.first, channel);
  TH1F *hWJets = get1DHistogram("W",selName, category.first, channel);
  TH1F *hTTbarJ = get1DHistogram("TTJ",selName, category.first, channel);
  TH1F *hTTbarT = get1DHistogram("TTT",selName, category.first, channel);
  TH1F *hST = get1DHistogram("T",selName, category.first, channel);
  TH1F *hVV = get1DHistogram("VVJ",selName, category.first, channel);
  if(hVV) hVV->Add(get1DHistogram("VVT",selName, category.first, channel));
  else hVV = get1DHistogram("VV",selName, category.first, channel);
  TH1F *hEWKZ = get1DHistogram("EWKZ",selName, category.first, channel);
  TH1F *hDYJetsLowM = 0;

  TH1F *hDYJetsOther = get1DHistogram("ZJ",selName, category.first, channel);
  TH1F *hDYJetsMuMu = get1DHistogram("ZL",selName, category.first, channel);
  TH1F *hDYJetsEE = 0;
  TH1F *hDYJetsMuTau = get1DHistogram("ZTT",selName, category.first, channel);

  TH1F *hSoup = get1DHistogram("data_obs",selName, category.first, channel);
  TH1F *hQCD = get1DHistogram("QCD",selName, category.first, channel);

  ///Protection against null pointers
  ///Null pointers happen when sample was not read, or there were no
  ///events passing particular selection.
  if(!hSoup) return 0;
  TH1F *hEmpty = (TH1F*)hSoup->Clone("hEmpty");
  hEmpty->Reset();

  ///Set histograms directory, so the histograms are saved
  if(hQCD) hQCD->SetDirectory(hSoup->GetDirectory());
  if(hWJets) hWJets->SetDirectory(hSoup->GetDirectory());
  if(hDYJetsLowM) hDYJetsLowM->SetDirectory(hSoup->GetDirectory());
  if(hDYJetsOther) hDYJetsOther->SetDirectory(hSoup->GetDirectory());
  if(hDYJetsMuTau) hDYJetsMuTau->SetDirectory(hSoup->GetDirectory());
  if(hDYJetsMuMu) hDYJetsMuMu->SetDirectory(hSoup->GetDirectory());
  if(hDYJetsEE) hDYJetsEE->SetDirectory(hSoup->GetDirectory());
  if(hTTbarJ) hTTbarJ->SetDirectory(hSoup->GetDirectory());
  if(hST) hST->SetDirectory(hSoup->GetDirectory());
  if(hVV) hVV->SetDirectory(hSoup->GetDirectory());
  if(hggHiggs115) hggHiggs115->SetDirectory(hSoup->GetDirectory());
  if(hqqHiggs115) hqqHiggs115->SetDirectory(hSoup->GetDirectory());
  if(hggHiggs120) hggHiggs120->SetDirectory(hSoup->GetDirectory());
  if(hqqHiggs120) hqqHiggs120->SetDirectory(hSoup->GetDirectory());
  if(hggHiggs125) hggHiggs125->SetDirectory(hSoup->GetDirectory());
  if(hqqHiggs125) hqqHiggs125->SetDirectory(hSoup->GetDirectory());
  if(hggHiggs130) hggHiggs130->SetDirectory(hSoup->GetDirectory());
  if(hqqHiggs130) hqqHiggs130->SetDirectory(hSoup->GetDirectory());
  if(hggHiggs135) hggHiggs135->SetDirectory(hSoup->GetDirectory());
  if(hqqHiggs135) hqqHiggs135->SetDirectory(hSoup->GetDirectory());  
  if(!hQCD) hQCD = (TH1F*)hEmpty->Clone((hName+"QCD"+selName).c_str()); 
  if(!hWJets) hWJets = (TH1F*)hEmpty->Clone((hName+"WJets"+selName).c_str());  
  if(!hDYJetsLowM) hDYJetsLowM = (TH1F*)hEmpty->Clone((hName+"hDYLowM"+selName).c_str());    
  if(!hDYJetsOther) hDYJetsOther = (TH1F*)hEmpty->Clone((hName+"hDYOtherJets"+selName).c_str());  
  if(!hDYJetsMuTau) hDYJetsMuTau = (TH1F*)hEmpty->Clone((hName+"hDYMuTauJets"+selName).c_str());  
  if(!hDYJetsMuMu) hDYJetsMuMu = (TH1F*)hEmpty->Clone((hName+"hDYMuMuJets"+selName).c_str());  
  if(!hDYJetsEE) hDYJetsEE = (TH1F*)hEmpty->Clone((hName+"hDYEEJets"+selName).c_str());  
  if(!hTTbarJ) hTTbarJ = (TH1F*)hEmpty->Clone((hName+"hTTbarJ"+selName).c_str());  
  if(!hTTbarT) hTTbarT = (TH1F*)hEmpty->Clone((hName+"hTTbarT"+selName).c_str());
  if(!hST) hST = (TH1F*)hEmpty->Clone((hName+"hST"+selName).c_str());
  if(!hVV) hVV = (TH1F*)hEmpty->Clone((hName+"hDiBoson"+selName).c_str()); 
  if(!hEWKZ) hEWKZ = (TH1F*)hEmpty->Clone((hName+"hEWKZ"+selName).c_str()); 
  if(!hggHiggs115) hggHiggs115 = (TH1F*)hEmpty->Clone((hName+"hggH115"+selName).c_str());  
  if(!hqqHiggs115) hqqHiggs115 = (TH1F*)hEmpty->Clone((hName+"hqqH115"+selName).c_str());
  if(!hggHiggs120) hggHiggs120 = (TH1F*)hEmpty->Clone((hName+"hggH120"+selName).c_str());  
  if(!hqqHiggs120) hqqHiggs120 = (TH1F*)hEmpty->Clone((hName+"hqqH120"+selName).c_str());
  if(!hggHiggs125) hggHiggs125 = (TH1F*)hEmpty->Clone((hName+"hggH125"+selName).c_str());  
  if(!hWHiggs125) hWHiggs125 = (TH1F*)hEmpty->Clone((hName+"hWH125"+selName).c_str());
  if(!hZHiggs125) hZHiggs125 = (TH1F*)hEmpty->Clone((hName+"hZH125"+selName).c_str());  
  if(!hqqHiggs125) hqqHiggs125 = (TH1F*)hEmpty->Clone((hName+"hqqH125"+selName).c_str());
  if(!hggHiggs130) hggHiggs130 = (TH1F*)hEmpty->Clone((hName+"hggH130"+selName).c_str());  
  if(!hqqHiggs130) hqqHiggs130 = (TH1F*)hEmpty->Clone((hName+"hqqH130"+selName).c_str());
  if(!hggHiggs135) hggHiggs135 = (TH1F*)hEmpty->Clone((hName+"hggH135"+selName).c_str());  
  if(!hqqHiggs135) hqqHiggs135 = (TH1F*)hEmpty->Clone((hName+"hqqH135"+selName).c_str());  

  TH1F *hHiggs = (TH1F*)hggHiggs125->Clone("hHiggs");
  hHiggs->Reset();
  
  float lumi = getLumi(); 

  hHiggs->Add(hggHiggs125);
  hHiggs->Add(hqqHiggs125);
  hHiggs->Add(hZHiggs125);
  hHiggs->Add(hWHiggs125);
  //////////////////////////////////////////////////////
  hSoup->SetLineColor(1);
  hSoup->SetFillColor(1);
  hSoup->SetMarkerStyle(20);

  hWJets->SetFillColor(kRed+2);
  hEWKZ->SetFillColor(kRed+7);
  hTTbarT->SetFillColor(kBlue+2);
  hTTbarJ->SetFillColor(kBlue+5);
  hST->SetFillColor(kYellow-10);
  hVV->SetFillColor(kRed-10);
  hDYJetsOther->SetFillColor(kOrange-1);
  hDYJetsMuMu->SetFillColor(kOrange-3);
  hDYJetsEE->SetFillColor(kOrange-6);
  hDYJetsMuTau->SetFillColor(kOrange-9);
  hDYJetsLowM->SetFillColor(kOrange-7);
  hQCD->SetFillColor(kMagenta-10);
  hHiggs->SetFillColor(kCyan+4);

  hSoup->SetLineWidth(1);
  int rebinFactor = 1;  
  hSoup->Rebin(rebinFactor);
  hWJets->Rebin(rebinFactor);
  hTTbarJ->Rebin(rebinFactor);
  hVV->Rebin(rebinFactor);
  hST->Rebin(rebinFactor);
  hDYJetsOther->Rebin(rebinFactor);
  hDYJetsMuMu->Rebin(rebinFactor);
  hDYJetsEE->Rebin(rebinFactor);
  hDYJetsMuTau->Rebin(rebinFactor);
  hDYJetsLowM->Rebin(rebinFactor);
  hHiggs->Rebin(rebinFactor);

  THStack *hs = new THStack("hs","Stacked histograms");      
  /////////
  hs->Add(hHiggs,"hist");    
  hs->Add(hQCD,"hist");
  hs->Add(hTTbarJ,"hist");
  hs->Add(hTTbarT,"hist");
  hs->Add(hEWKZ,"hist");
  hs->Add(hST,"hist");
  hs->Add(hVV,"hist");
  hs->Add(hWJets,"hist");
  hs->Add(hDYJetsLowM,"hist");
  hs->Add(hDYJetsOther,"hist");
  hs->Add(hDYJetsMuMu,"hist");
  hs->Add(hDYJetsEE,"hist");
  hs->Add(hDYJetsMuTau,"hist");
  ////////
  TH1F *hMCSum = (TH1F*)hWJets->Clone("hMCSum");
  hMCSum->Reset();
  hMCSum->Add(hDYJetsLowM);
  hMCSum->Add(hDYJetsMuTau);
  hMCSum->Add(hDYJetsMuMu);
  hMCSum->Add(hDYJetsEE);
  hMCSum->Add(hDYJetsOther);  
  hMCSum->Add(hWJets);
  hMCSum->Add(hTTbarJ);
  hMCSum->Add(hTTbarT);
  hMCSum->Add(hEWKZ);
  hMCSum->Add(hST);
  hMCSum->Add(hVV);
  hMCSum->Add(hQCD);
  hMCSum->Add(hHiggs);

  if(!selName.size()) selName = "baseline";
  cout<<"Event count summary for selecion name: "<<selName<<std::endl;
  std::cout<<"Data: "<<hSoup->Integral(0,hSoup->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC: "<<hMCSum->Integral(0,hMCSum->GetNbinsX()+1)<<std::endl;  
  std::cout<<"MC W->l: "<<hWJets->Integral(0,hWJets->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC TTbarJ: "<<hTTbarJ->Integral(0,hTTbarJ->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC TTbarT: "<<hTTbarT->Integral(0,hTTbarT->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC EWKZ: "<<hEWKZ->Integral(0,hEWKZ->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC single T: "<<hST->Integral(0,hST->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC DiBoson: "<<hVV->Integral(0,hVV->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC Z->mu tau: "<<hDYJetsMuTau->Integral(0,hDYJetsMuTau->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC Z->mu mu: "<<hDYJetsMuMu->Integral(0,hDYJetsMuMu->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC Z->e e: "<<hDYJetsEE->Integral(0,hDYJetsEE->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC Z->ll(m<50): "<<hDYJetsLowM->Integral(0,hDYJetsLowM->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC Z->other: "<<hDYJetsOther->Integral(0,hDYJetsOther->GetNbinsX()+1)<<std::endl;
  std::cout<<"MC H(125)->tau tau: "<<hHiggs->Integral(0,hHiggs->GetNbinsX()+1)<<std::endl;  
  std::cout<<"QCD: "<<hQCD->Integral(0,hQCD->GetNbinsX()+1)<<std::endl; 
  std::cout<<"----------------------------------------"<<std::endl;

  TCanvas *c1 = getDefaultCanvas();
  c1->SetName("c1");
  c1->SetTitle("HTauTau analysis");
  c1->Divide(2);

  TPad *pad1 = (TPad*)c1->GetPad(1);
  TPad *pad2 = (TPad*)c1->GetPad(2);
  pad1->SetPad(0.01,0.29,0.99,0.99);
  pad2->SetPad(0.01,0.01,0.99,0.29);
  pad1->SetRightMargin(0.23);
  pad2->SetRightMargin(0.23);
  pad2->SetFillStyle(4000);
  ///
  pad1->Draw();
  pad1->cd();

  if(!selName.size()) selName = "baseline";
  hs->SetTitle(("Variable: "+varName+" selection: "+selName).c_str());
  hs->SetMaximum(4400);
  hs->Draw("hist");
  hs->GetXaxis()->SetTitle(varName.c_str());
  hs->GetYaxis()->SetTitleOffset(1.4);
  hMCSum->SetFillColor(5);
  /////////
  float highEnd = 170;
  float lowEnd = -150;

  if(varName.find("Phi_")!=std::string::npos) lowEnd = 0;
  if(category.second.find("_W")!=std::string::npos) {lowEnd = 81; highEnd = 180;}
  if(category.second.find("antiIso")!=std::string::npos) {lowEnd = 41; highEnd = 180;}
    
  int binHigh = hs->GetXaxis()->FindBin(highEnd);  
  int binLow = hs->GetXaxis()->FindBin(lowEnd);

  if(hs->GetXaxis()->GetXmax()<highEnd || hs->GetXaxis()->GetXmax()>300) binHigh = hs->GetXaxis()->GetNbins();
  if(hs->GetXaxis()->GetXmin()>lowEnd) lowEnd = 1;

  hs->GetXaxis()->SetRange(binLow,binHigh);
  highEnd =  hs->GetXaxis()->GetBinUpEdge(binHigh);

  char yTitle[200];
  sprintf(yTitle,"Events/%2.1f",hSoup->GetXaxis()->GetBinWidth(1));
  hs->GetYaxis()->SetTitle(yTitle);
  
  float max = hs->GetMaximum();
  if(hSoup->GetMaximum()>max) max = hSoup->GetMaximum();

  hs->GetHistogram()->SetTitleOffset(1.0);
  hs->SetMaximum(1.1*max);
  hs->SetMinimum(0.1);

  hSoup->DrawCopy("same");

  TLegend *leg = new TLegend(0.79,0.32,0.99,0.82,NULL,"brNDC");
  setupLegend(leg);
  leg->AddEntry(hSoup,"Data","lep");
  leg->AddEntry(hDYJetsMuTau,"Z#rightarrow #mu #tau_{h}","f");
  leg->AddEntry(hDYJetsMuMu,"Z#rightarrow #mu #mu","f");
  leg->AddEntry(hDYJetsEE,"Z#rightarrow e e","f");
  leg->AddEntry(hDYJetsLowM,"Z#rightarrow ll(m<50)","f");
  leg->AddEntry(hDYJetsOther,"Z#rightarrow other","f");
  leg->AddEntry(hWJets,"W#rightarrow l #nu","f");
  leg->AddEntry(hTTbarJ,"TTbarJ","f");
  leg->AddEntry(hTTbarT,"TTbarT","f");
  leg->AddEntry(hEWKZ,"EWKZ","f");
  leg->AddEntry(hST,"single T","f");
  leg->AddEntry(hVV,"DiBoson","f");
  leg->AddEntry(hQCD,"QCD","f");
  leg->AddEntry(hHiggs,"H(125)#rightarrow #tau #tau","f");
  leg->SetHeader(Form("#int L = %.2f fb^{-1}",lumi/1000));
  leg->Draw();

  float x = 0.6*(hs->GetXaxis()->GetXmax() - 
		 hs->GetXaxis()->GetXmin()) +
    hs->GetXaxis()->GetXmin(); 

  float y = 0.8*(max - 
		 hs->GetMinimum()) +
                 hs->GetMinimum(); 
  c1->cd();
  pad2->Draw();
  pad2->cd();

  hSoup = (TH1F*)hSoup->Clone("hDataMCRatio");
  hSoup->SetDirectory(0);
  hSoup->GetXaxis()->SetRange(binLow,binHigh);
  hSoup->SetTitle("");
  hSoup->SetXTitle("");
  //hSoup->SetYTitle("#frac{N_{obs} - N_{exp}}{#sqrt{N_{obs}}}");
  hSoup->SetYTitle("#frac{N_{obs}}{N_{exp}}");
  hSoup->GetXaxis()->SetLabelSize(0.09);
  hSoup->GetYaxis()->SetLabelSize(0.09);
  hSoup->GetYaxis()->SetTitleSize(0.09);
  hSoup->GetYaxis()->SetTitleOffset(0.5);
  hSoup->Divide(hMCSum);  
  hSoup->SetLineWidth(3);
  hSoup->SetMinimum(0.55);
  hSoup->SetMaximum(1.55);
  hSoup->SetStats(kFALSE);
  hSoup->SetFillStyle(0);
  hSoup->Draw("E1");
  TLine *aLine = new TLine(hSoup->GetXaxis()->GetXmin(),1.0,highEnd,1.0);
  aLine->SetLineColor(1);
  aLine->SetLineWidth(2);
  aLine->Draw();

  string plotName;
  if(hName.find_last_of("/")<string::npos) plotName = "fig_png/" + hName.substr(hName.find_last_of("/")) + ".png";    
  else plotName = "fig_png/h1D_"+channel+Form("_%s_%s_%s",category.second.c_str(),selName.c_str(),hName.c_str())+".png";
  c1->Print(plotName.c_str());
  
  pad1->SetLogy(1);
  if(hName.find_last_of("/")<string::npos) plotName = "fig_png/" + hName.substr(hName.find_last_of("/")) + "_LogY.png";    
  else plotName = "fig_png/h1D_"+channel+Form("_%s_%s_%s",category.second.c_str(),selName.c_str(),hName.c_str())+"_LogY.png";
  c1->Print(plotName.c_str()); 

  std::cout<<"-------------------------------------------------------------"<<std::endl;

  return hs;
}
////////////////////////////////////////////////////
////////////////////////////////////////////////////
void plotPostFit(){
  
  std::unordered_map<std::string, std::vector<std::pair<std::string, std::string>>> categories;
  std::vector<std::pair<std::string,std::string>> mt_categories = {make_pair("0jet","UnRollTauPtMassVis"),  make_pair("boosted","UnRollHiggsPtMassSV"),  make_pair("vbf","UnRollMjjMassSV"),  make_pair("0jet_W","MassTrans"),  make_pair("boosted_W","MassTrans"),  make_pair("vbf_W","MassTrans"),  make_pair("antiIso_0jet","MassVis"),  make_pair("antiIso_boosted","MassSV"),  make_pair("antiIso_vbf","MassSV")};
  std::vector<std::pair<std::string,std::string>> tt_categories = {make_pair("0jet","MassSV"),  make_pair("boosted","UnRollHiggsPtMassSV"),  make_pair("vbf","UnRollMjjMassSV"),  make_pair("0jet_QCD","MassVis"),  make_pair("boosted_QCD","MassVis"),  make_pair("vbf_QCD","MassVis")};
  categories["mt"] = mt_categories;
  categories["tt"] = tt_categories;
  
  for(std::unordered_map<std::string, std::vector<std::pair<std::string, std::string>>>::iterator itMap = categories.begin(); itMap!=categories.end(); itMap++){
  	for(int itVect = 0; itVect<itMap->second.size(); itVect++){
  		plotStack(itMap->second.at(itVect).second, itMap->first, std::make_pair(itVect, itMap->second.at(itVect).first), "prefit");
  		plotStack(itMap->second.at(itVect).second, itMap->first, std::make_pair(itVect, itMap->second.at(itVect).first), "postfit");
  		}
  	}
  
}
////////////////////////////////////////////////////
////////////////////////////////////////////////////
