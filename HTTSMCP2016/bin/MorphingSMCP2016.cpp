#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/regex.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/Algorithm.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/HTTSMCP2016/interface/HttSystematics_SMRun2.h"
#include "CombineHarvester/CombineTools/interface/JsonTools.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "TF1.h"
#include "TMatrix.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

template <typename T>
void To1Bin(T* proc)
{
    std::unique_ptr<TH1> originalHist = proc->ClonedScaledShape();
    TH1F *hist = new TH1F("hist","hist",1,0,1);
    double err = 0;
    double rate =
    originalHist->IntegralAndError(0, originalHist->GetNbinsX() + 1, err);
    hist->SetDirectory(0);
    hist->SetBinContent(1, rate);
    hist->SetBinError(1, err);
    proc->set_shape(*hist, true);  // True means adjust the process rate to the
    // integral of the hist
}


unsigned Get1DBinNumFrom2D(TH2 *h2d, unsigned xbin, unsigned ybin) {
    unsigned Nxbins = h2d->GetNbinsX();
    return (ybin-1)*Nxbins + xbin -1;
}

TH1D* UnrollHistogram(TH2 *h2d){
    unsigned n = 0;
    unsigned Nbins = (h2d->GetNbinsY()+n)*(h2d->GetNbinsX());
    TH1D *h1d = new TH1D(((std::string)h2d->GetName()+"_unroll").c_str(), "", Nbins, 0, Nbins);
    for(unsigned i=1; i<=(unsigned)h2d->GetNbinsX(); ++i){
      for(unsigned j=1; j<=(unsigned)h2d->GetNbinsY()+n; ++j){
        unsigned glob_bin = Get1DBinNumFrom2D(h2d,i,j);
        double content = h2d->GetBinContent(i,j);
        double error = h2d->GetBinError(i,j);
        h1d->SetBinContent(glob_bin+1,content);
        h1d->SetBinError(glob_bin+1,error);
       }
     }
     return h1d;
}

TH2D* RollHistogram(TH1D *h1d, unsigned nxbins) {
  unsigned nybins = h1d->GetNbinsX()/nxbins; 
  TH2D *h2d = new TH2D(((std::string)h1d->GetName()+"_roll").c_str(), "", nxbins, 0, nxbins, nybins, 0, nybins);
  unsigned j=0;
  for(unsigned nx=1; nx<=(unsigned)h1d->GetNbinsX(); ++nx){
   if((nx-1) % nxbins == 0) j++;
   unsigned i = nx - (j-1)*nxbins;
   double content = h1d->GetBinContent(nx);
   double error = h1d->GetBinError(nx);
   h2d->SetBinContent(i,j,content);
   h2d->SetBinError(i,j,error);
  }
  return h2d;
}

TH1D *Lowess1D(TH1D *h, double bandwidth) {

  double h1 = bandwidth*(h->GetBinLowEdge(1)-h->GetBinLowEdge(h->GetNbinsX()+1));
  TH1D *hout = (TH1D*)h->Clone();

  for(unsigned i=1; i<=(unsigned)h->GetNbinsX(); ++i) {
    double x0 = h->GetBinLowEdge(i);
  
    double sumW=0., sumWR=0., sumWX=0., sumWX2=0., sumWXR=0.;

    for(unsigned j=1; j<=(unsigned)h->GetNbinsX(); ++j) {
      double xi = h->GetBinLowEdge(j); 
      double ri  = h->GetBinContent(j);

      double xtrans = (xi-x0);
      double d=xtrans/h1;
 
      if(xtrans > 1.) continue;
      double wt = std::max(0., pow((1.-pow(d,3)),3));

      sumW+=wt;
      sumWX+=wt*xtrans;
      sumWR+=wt*ri;
      sumWXR+=wt*xtrans*ri;
      sumWX2+=wt*xtrans*xtrans;

    }

    double meanX2 = sumWX2 /= sumW;
    double meanR = sumWR /= sumW;
    double meanX = sumWX /= sumW;
    double meanXR = sumWXR /= sumW;  
    double rnew = (meanX2 * meanR - meanX * meanXR) / (meanX2 - meanX*meanX);
    rnew = std::max(0.,rnew);
    hout->SetBinContent(i, rnew); 
  }
  
  return hout;

}

TH2D* Lowess2D(TH2D *h, double bandwidth2, double bandwidth1) {

  TH2D *hout = (TH2D*)h->Clone();
  double h1 = bandwidth1*(h->GetXaxis()->GetBinLowEdge(1)-h->GetXaxis()->GetBinLowEdge(h->GetNbinsX()+1));
  double h2 = bandwidth2*(h->GetYaxis()->GetBinLowEdge(1)-h->GetYaxis()->GetBinLowEdge(h->GetNbinsY()+1));
  
  for(unsigned i1=1; i1<=(unsigned)h->GetNbinsX(); ++i1) {
    for(unsigned j1=1; j1<=(unsigned)h->GetNbinsY(); ++j1) {
      double x0 = h->GetXaxis()->GetBinLowEdge(i1);
      double y0 = h->GetYaxis()->GetBinLowEdge(j1);
      double r0 = h->GetBinContent(j1);
      double sumW=0., sumWXY=0., sumWR=0., sumWX=0., sumWY=0., sumWX2=0., sumWY2=0., sumWXR=0., sumWYR=0.;

      for(unsigned i2=1; i2<=(unsigned)h->GetNbinsX(); ++i2) {
        for(unsigned j2=1; j2<=(unsigned)h->GetNbinsY(); ++j2) {
          double xi = h->GetXaxis()->GetBinLowEdge(i2);
          double yi = h->GetYaxis()->GetBinLowEdge(j2);
          double ri = h->GetBinContent(i2,j2);
          
          double xtrans = (xi-x0)/h1;
          double ytrans = (yi-y0)/h2;
 
          double d = sqrt(xtrans*xtrans + ytrans*ytrans);

          if(d > 1. or ri <= 0.) continue;
          double wt = std::max(0., pow((1-pow(d,3)),3));

          sumW+=wt;
          sumWXY+=wt*xtrans*ytrans;  
          sumWR+=wt*ri;

          sumWX+=wt*xtrans;
          sumWY+=wt*ytrans;

          sumWX2+=wt*xtrans*xtrans;
          sumWY2+=wt*ytrans*ytrans;
  
          sumWXR+=wt*xtrans*ri;
          sumWYR+=wt*ytrans*ri;

        }
    }


    double a1[9] = {1.,         sumWX/sumW, sumWY/sumW, sumWX/sumW,  sumWX2/sumW, sumWXY/sumW, sumWY/sumW,  sumWXY/sumW, sumWY2/sumW};
    double a2[9] = {sumWR/sumW, sumWX/sumW, sumWY/sumW, sumWXR/sumW, sumWX2/sumW, sumWXY/sumW, sumWYR/sumW, sumWXY/sumW, sumWY2/sumW};

    TMatrix m1 = TMatrixD(3, 3, a1);
    TMatrix m2 = TMatrixD(3, 3, a2);

    double rnew = r0;  
    if(m1.Determinant()!=0) rnew = m2.Determinant()/m1.Determinant();
   

    hout->SetBinContent(i1,j1,rnew);
 
    }
  }
  return hout;
}

void SmoothShapes(ch::CombineHarvester& cb, string name, double nxbins, bool smooth, bool merge_xbins, bool merge_ybins) {

  auto cb_syst = cb.cp().syst_name({name});
  cb_syst.ForEachSyst([&](ch::Systematic *syst) {
    if (syst->type().find("shape") != std::string::npos) {
      TH1D *shape_u = (TH1D*)syst->ClonedShapeU().get()->Clone();
      TH1D *shape_d = (TH1D*)syst->ClonedShapeD().get()->Clone();
      TH1D* nominal = new TH1D();

      cb.cp().ForEachProc([&](ch::Process *proc){
        bool match_proc = (MatchingProcess(*proc,*syst));
        if(match_proc) nominal = (TH1D*)proc->ClonedShape().get()->Clone();
      });


      TH1D *shape_u_smooth = new TH1D();
      TH1D *shape_d_smooth = new TH1D(); 

      if(syst->bin().find("0jet") != std::string::npos) {
        shape_u_smooth = Lowess1D(shape_u,0.2); 
        shape_d_smooth = Lowess1D(shape_d,0.2);
      } else {
        TH2D *shape_u_2d = RollHistogram(shape_u,nxbins); 
        TH2D *nominal_2d = RollHistogram(nominal,nxbins);
        TH2D *shape_d_2d = RollHistogram(shape_d,nxbins);

        if(merge_xbins) {
          for (unsigned j=1; j<=(unsigned)shape_u_2d->GetNbinsY(); ++j){
           double bin_content = nominal_2d->Integral(-1,-1,j,j);
           for (unsigned i=1; i<=(unsigned)nominal_2d->GetNbinsX(); ++i) nominal_2d->SetBinContent(i,j,bin_content);
           double bin_content_u = shape_u_2d->Integral(-1,-1,j,j);
           for (unsigned i=1; i<=(unsigned)shape_u_2d->GetNbinsX(); ++i) shape_u_2d->SetBinContent(i,j,bin_content_u);
           double bin_content_d = shape_d_2d->Integral(-1,-1,j,j);
           for (unsigned i=1; i<=(unsigned)shape_d_2d->GetNbinsX(); ++i) shape_d_2d->SetBinContent(i,j,bin_content_d);
          }
        }

        if(merge_ybins) {
          for (unsigned i=1; i<=(unsigned)shape_u_2d->GetNbinsX(); ++i){
           double bin_content = nominal_2d->Integral(i,i,-1,-1);
           for (unsigned j=1; j<=(unsigned)nominal_2d->GetNbinsY(); ++j) nominal_2d->SetBinContent(i,j,bin_content);
           double bin_content_u = shape_u_2d->Integral(i,i,-1,-1);
           for (unsigned j=1; j<=(unsigned)shape_u_2d->GetNbinsY(); ++j) shape_u_2d->SetBinContent(i,j,bin_content_u);
           double bin_content_d = shape_d_2d->Integral(i,i,-1,-1);
           for (unsigned j=1; j<=(unsigned)shape_d_2d->GetNbinsY(); ++j) shape_d_2d->SetBinContent(i,j,bin_content_d);
          }
        }

        shape_u_2d->Divide(nominal_2d); 
        if(smooth) shape_u_2d = Lowess2D(shape_u_2d, 1.,0.2);
        shape_u_smooth = UnrollHistogram(shape_u_2d);

        shape_d_2d->Divide(nominal_2d);
        if(smooth) shape_d_2d = Lowess2D(shape_d_2d, 1.,0.2);
        shape_d_smooth = UnrollHistogram(shape_d_2d); 
      }

      shape_u_smooth->Multiply(nominal);
      shape_d_smooth->Multiply(nominal);

      syst->set_shapes(std::unique_ptr<TH1>(static_cast<TH1*>(shape_u_smooth)),std::unique_ptr<TH1>(static_cast<TH1*>(shape_d_smooth)),nullptr);

    }

  });

}

void ConvertShapesToLnN (ch::CombineHarvester& cb, string name, double min_ks) {
  auto cb_syst = cb.cp().syst_name({name});
  cb_syst.ForEachSyst([&](ch::Systematic *syst) {
    if (syst->type().find("shape") != std::string::npos) {
      if(min_ks<=0) {
        std::cout << "Converting systematic " << syst->name() << " for process " << syst->process() << " in bin " << syst->bin() << " to lnN." <<std::endl;
        syst->set_type("lnN");
        return;
      }
      auto shape_u = syst->ClonedShapeU();
      auto shape_d = syst->ClonedShapeD();

      // set uncertainties of up and down templates to zero so they are not concidered in ks test
      for(unsigned i=0; i<=(unsigned)shape_u->GetNbinsX(); ++i) {
        shape_u->SetBinError(i,0.);
        shape_d->SetBinError(i,0.);
      }

      std::unique_ptr<TH1> nominal;

      double ks_u = 0., ks_d = 0.;

      cb.cp().ForEachProc([&](ch::Process *proc){
        bool match_proc = (MatchingProcess(*proc,*syst));
        if(match_proc) nominal = proc->ClonedScaledShape(); 
      });

      if(shape_u && nominal){
        ks_u = nominal.get()->KolmogorovTest(shape_u.get()); 
      }
      if(shape_d && nominal){
        ks_d = nominal.get()->KolmogorovTest(shape_d.get());
      } 
      if(ks_u > min_ks && ks_d > min_ks){
        std::cout << "Converting systematic " << syst->name() << " for process " << syst->process() << " in bin " << syst->bin() << " to lnN. KS scores (u,d) = (" << ks_u << "," << ks_d << ")" <<std::endl;
        syst->set_type("lnN");
      }
      else {
        std::cout << "Not converting systematic " << syst->name() << " for process " << syst->process() << " in bin " << syst->bin() << " to lnN. KS scores (u,d) = (" << ks_u << "," << ks_d << ")" <<std::endl;
      }
    }
  }); 

}

void DecorrelateSyst (ch::CombineHarvester& cb, string name, double correlation, std::vector<string> chans_2016, std::vector<string> chans_2017) {
  if (correlation >= 1.) return;
  auto cb_syst = cb.cp().syst_name({name});
  double val = sqrt(1. - correlation);
  // clone 2016 systs
  ch::CloneSysts(cb.cp().channel(chans_2016).syst_name({name}), cb, [&](ch::Systematic *s) {
      s->set_name(s->name()+"_2016");
      if (s->type().find("shape") != std::string::npos) {
        s->set_scale(s->scale() * val);
      }
      if (s->type().find("lnN") != std::string::npos) {
        s->set_value_u((s->value_u() - 1.) * val + 1.);
        if (s->asymm()){
          s->set_value_d((s->value_d() - 1.) * val + 1.);
        }
      }
  });
  // clone 2017 systs
  ch::CloneSysts(cb.cp().channel(chans_2017).syst_name({name}), cb, [&](ch::Systematic *s) {
      s->set_name(s->name()+"_2017");
      if (s->type().find("shape") != std::string::npos) {
        s->set_scale(s->scale() * val);
      }
      if (s->type().find("lnN") != std::string::npos) {
        s->set_value_u((s->value_u() - 1.) * val + 1.);
        if (s->asymm()){
          s->set_value_d((s->value_d() - 1.) * val + 1.);
        }
      }
  });

  if(correlation>0.) {
    // re-scale un-correlated part
    double val = sqrt(correlation);
    cb_syst.ForEachSyst([val](ch::Systematic *syst) {
      if (syst->type().find("shape") != std::string::npos) {
        syst->set_scale(syst->scale() * val);
      }
      if (syst->type().find("lnN") != std::string::npos) {
        syst->set_value_u((syst->value_u() - 1.) * val + 1.);
        if (syst->asymm()){
          syst->set_value_d((syst->value_d() - 1.) * val + 1.);
        }
      }
    });
  } else {
    // remove uncorrelated part if systs are 100% un-correlated
    cb.FilterSysts([&](ch::Systematic *s){
        return s->name().find(name) != std::string::npos && s->name().find("_2016") == std::string::npos && s->name().find("_2017") == std::string::npos;
    });

  }
}

int main(int argc, char** argv) {

    string output_folder = "sm_run2";
    string input_folder_em="Imperial/CP/";
    string input_folder_et="Imperial/CP/";
    string input_folder_mt="Imperial/CP/";
    string input_folder_tt="Imperial/CP/";
    string input_folder_mm="USCMS/";
    string only_init="";
    string scale_sig_procs="";
    string postfix="";
    bool ttbar_fit = false;
    bool real_data = true;
    bool no_shape_systs = false;
    bool do_embedding = true;
    bool auto_rebin = false;
    bool no_jec_split = false;    
    bool do_jetfakes = true;
    bool do_mva = false;    
    int do_control_plots = 0;
    bool useJHU = false;
 
    bool cross_check = false;

    string era;
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
    ("input_folder_em", po::value<string>(&input_folder_em)->default_value("Imperial/CP"))
    ("input_folder_et", po::value<string>(&input_folder_et)->default_value("Imperial/CP"))
    ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("Imperial/CP"))
    ("input_folder_tt", po::value<string>(&input_folder_tt)->default_value("Imperial/CP"))
    ("input_folder_mm", po::value<string>(&input_folder_mm)->default_value("USCMS"))
    ("only_init", po::value<string>(&only_init)->default_value(""))
    ("real_data", po::value<bool>(&real_data)->default_value(real_data))
    ("scale_sig_procs", po::value<string>(&scale_sig_procs)->default_value(""))
    ("postfix", po::value<string>(&postfix)->default_value(postfix))
    ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"))
    ("no_shape_systs", po::value<bool>(&no_shape_systs)->default_value(no_shape_systs))
    ("do_embedding", po::value<bool>(&do_embedding)->default_value(true))
    ("do_jetfakes", po::value<bool>(&do_jetfakes)->default_value(true))
    ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(false))
    ("no_jec_split", po::value<bool>(&no_jec_split)->default_value(true))    
    ("do_mva", po::value<bool>(&do_mva)->default_value(false))
    ("do_control_plots", po::value<int>(&do_control_plots)->default_value(0))    
    ("era", po::value<string>(&era)->default_value("2016"))
    ("ttbar_fit", po::value<bool>(&ttbar_fit)->default_value(true))
    ("cross_check", po::value<bool>(&cross_check)->default_value(false))
    ("useJHU", po::value<bool>(&useJHU)->default_value(false));

    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);
    typedef vector<string> VString;

    if(cross_check){
      //no_shape_systs = true;
      ttbar_fit = false;
      input_folder_em="Imperial/CP/cross_check/";
      input_folder_et="Imperial/CP/cross_check/";
      input_folder_mt="Imperial/CP/cross_check/";
      input_folder_tt="Imperial/CP/cross_check/";
    }
 
    if(do_control_plots>0){
      ttbar_fit = false;
      input_folder_em="/Imperial/control_cards_"+era+"/";
      input_folder_et="/Imperial/control_cards_"+era+"/";
      input_folder_mt="/Imperial/control_cards_"+era+"/";
      input_folder_tt="/Imperial/control_cards_"+era+"/";
    }

 
    VString years;
    if ( era.find("2016") != std::string::npos ) years.push_back("2016");
    if ( era.find("2017") != std::string::npos ) years.push_back("2017");
    if ( era=="all" ) years = {"2016","2017"};
 
    typedef vector<string> VString;
    typedef vector<pair<int, string>> Categories;
    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    //    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/AllROOT_20fb/";
    std::map<string, string> input_dir;
    input_dir["em"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_em+"/";
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_mt+"/";
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_et+"/";
    input_dir["tt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_tt+"/";
    input_dir["ttbar"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/shapes/"+input_folder_em+"/";    
    
    
    VString chns = {"em","et","mt","tt"};
    if(cross_check) chns = {"mt"};
    if (ttbar_fit) chns.push_back("ttbar");
    
    map<string, VString> bkg_procs;
    bkg_procs["et"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
    bkg_procs["mt"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
    bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT","VVJ", "EWKZ"};
    bkg_procs["em"] = {"ZTT","W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    bkg_procs["ttbar"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    
    if(do_embedding){
      bkg_procs["et"] = {"EmbedZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "W", "EWKZ"};
      bkg_procs["mt"] = {"EmbedZTT", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT", "VVJ", "W", "EWKZ"};
      bkg_procs["tt"] = {"EmbedZTT", "W", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT","VVJ", "EWKZ"};
      bkg_procs["em"] = {"EmbedZTT","W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
      bkg_procs["ttbar"] = {"EmbedZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    }

    if(do_jetfakes){
      bkg_procs["et"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};
      bkg_procs["mt"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};
      bkg_procs["tt"] = {"ZTT", "ZL", "TTT", "VVT", "EWKZ", "jetFakes"};

      if(do_embedding){
        bkg_procs["et"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
        bkg_procs["mt"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
        bkg_procs["tt"] = {"EmbedZTT", "ZL", "TTT", "VVT", "jetFakes", "EWKZ"};
      }

    }

    if(cross_check){
      bkg_procs["et"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
      bkg_procs["mt"] = {"ZTT", "QCD", "ZL", "ZJ","TTT","TTJ", "VVT", "VVJ", "EWKZ", "W"};
      bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ","TTT","TTJ",  "VVT","VVJ", "EWKZ"};
      bkg_procs["em"] = {"ZTT","W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
      bkg_procs["ttbar"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    } 

    ch::CombineHarvester cb;
    
    map<string,Categories> cats;

    if (!do_mva) {
      if( era.find("2016") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats["et_2016"] = {
            {1, "et_0jet"},
            {2, "et_boosted"}
        };
        
        cats["mt_2016"] = {
            {1, "mt_0jet"},
            {2, "mt_boosted"}
        }; 
        cats["em_2016"] = {
            {1, "em_0jet"},
            {2, "em_boosted"}
        };
        
        cats["tt_2016"] = {
            {1, "tt_0jet"},
            {2, "tt_boosted"}
        };
        
        cats["ttbar_2016"] = {
            {1, "em_ttbar"}
        };
      }
      if( era.find("2017") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats["et_2017"] = {
            {1, "et_0jet"},
            {2, "et_boosted"}
        };

        cats["mt_2017"] = {
            {1, "mt_0jet"},
            {2, "mt_boosted"}
        };
        cats["em_2017"] = {
            {1, "em_0jet"},
            {2, "em_boosted"}
        };

        cats["tt_2017"] = {
            {1, "tt_0jet"},
            {2, "tt_boosted"}
        };

        cats["ttbar_2017"] = {
            {1, "em_ttbar"}
        };
      }
    }
    else {
      cats["et_2016"] = {
          {31, "et_ggh_lowMjj"},
          {32, "et_qqh_lowMjj"},
          {33, "et_zttEmbed_lowMjj"},
          {34, "et_jetFakes_lowMjj"},
          {35, "et_tt_lowMjj"},
          {36, "et_zll_lowMjj"},

          {43, "et_zttEmbed_highMjj"},
          {44, "et_jetFakes_highMjj"},
          {45, "et_tt_highMjj"},
          {46, "et_zll_highMjj"},
      };
      
      cats["mt_2016"] = {
          {31, "mt_ggh_lowMjj"},
          {32, "mt_qqh_lowMjj"},
          {33, "mt_zttEmbed_lowMjj"},
          {34, "mt_jetFakes_lowMjj"},
          {35, "mt_tt_lowMjj"},
          {36, "mt_zll_lowMjj"},

          {43, "mt_zttEmbed_highMjj"},
          {44, "mt_jetFakes_highMjj"},
          {45, "mt_tt_highMjj"},
      }; 
      cats["em_2016"] = {
          {31, "em_ggh_lowMjj"},
          {32, "em_qqh_lowMjj"},
          {33, "em_zttEmbed_lowMjj"},
          {34, "em_qcd_lowMjj"},
          {35, "em_tt_lowMjj"},

          {43, "em_zttEmbed_highMjj"},
          {44, "em_tt_highMjj"},
      };
      
      cats["tt_2016"] = {
          {31, "tt_ggh_lowMjj"},
          {32, "tt_qqh_lowMjj"},
          {33, "tt_zttEmbed_lowMjj"},
          {34, "tt_jetFakes_lowMjj"},

          {43, "tt_zttEmbed_highMjj"},
          {44, "tt_jetFakes_highMjj"},
      };
    }
    
    map<string,Categories> cats_cp;
    
    if (!do_mva) {
      if( era.find("2016") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats_cp["em_2016"] = {
            {3, "em_dijet_loosemjj_lowboost"},
            {4, "em_dijet_loosemjj_boosted"},
            {5, "em_dijet_tightmjj_lowboost"},
            {6, "em_dijet_tightmjj_boosted"}

        };
        
        cats_cp["et_2016"] = {
            {3, "et_dijet_loosemjj_lowboost"},
            {4, "et_dijet_loosemjj_boosted"},       
            {5, "et_dijet_tightmjj_lowboost"},
            {6, "et_dijet_tightmjj_boosted"}

        };
        
        cats_cp["mt_2016"] = {
            {3, "mt_dijet_loosemjj_lowboost"},
            {4, "mt_dijet_loosemjj_boosted"},
            {5, "mt_dijet_tightmjj_lowboost"},
            {6, "mt_dijet_tightmjj_boosted"}
        };    
        
        cats_cp["tt_2016"] = {
            {3, "tt_dijet_loosemjj_lowboost"},
            {4, "tt_dijet_loosemjj_boosted"},
            {5, "tt_dijet_tightmjj_lowboost"},
            {6, "tt_dijet_tightmjj_boosted"} 
        };   
      } 
      if( era.find("2017") != std::string::npos ||  era.find("all") != std::string::npos) {
        cats_cp["em_2017"] = {
            {3, "em_dijet_loosemjj_lowboost"},
            {4, "em_dijet_loosemjj_boosted"},
            {5, "em_dijet_tightmjj_lowboost"},
            {6, "em_dijet_tightmjj_boosted"}

        };

        cats_cp["et_2017"] = {
            {3, "et_dijet_loosemjj_lowboost"},
            {4, "et_dijet_loosemjj_boosted"},
            {5, "et_dijet_tightmjj_lowboost"},
            {6, "et_dijet_tightmjj_boosted"}

        };

        cats_cp["mt_2017"] = {
            {3, "mt_dijet_loosemjj_lowboost"},
            {4, "mt_dijet_loosemjj_boosted"},
            {5, "mt_dijet_tightmjj_lowboost"},
            {6, "mt_dijet_tightmjj_boosted"}
        };

        cats_cp["tt_2017"] = {
            {3, "tt_dijet_loosemjj_lowboost"},
            {4, "tt_dijet_loosemjj_boosted"},
            {5, "tt_dijet_tightmjj_lowboost"},
            {6, "tt_dijet_tightmjj_boosted"}
        };
      }

    }
    else {
      cats_cp["em_2016"] = {
          
          {41, "em_ggh_highMjj"},
          {42, "em_qqh_highMjj"},

      };
      
      cats_cp["et_2016"] = {

          {41, "et_ggh_highMjj"},
          {42, "et_qqh_highMjj"},

      };
      
      cats_cp["mt_2016"] = {

          {41, "mt_ggh_highMjj"},
          {42, "mt_qqh_highMjj"},

      };    
      
      cats_cp["tt_2016"] = {

          {41, "tt_ggh_highMjj"},
          {42, "tt_qqh_highMjj"},

      };
    }

    if(do_control_plots>0) {
      std::string extra="";
      if(do_control_plots==2) extra="lomsv_";
      if(do_control_plots==3) extra="himsv_";
      if(era=="2016"){
        cats_cp["et_2016"] = {};
        cats_cp["mt_2016"] = {};
        cats_cp["tt_2016"] = {};
        cats_cp["em_2016"] = {};
        cats["et_2016"] = {
          {100, "et_"+extra+"pt_1"},
          {101, "et_"+extra+"pt_2"},
          {102, "et_"+extra+"met"},
          {103, "et_"+extra+"pt_tt"},
          {104, "et_"+extra+"m_vis"},
          {105, "et_"+extra+"mjj"},
          {106, "et_"+extra+"sjdphi"},
          {107, "et_"+extra+"n_jets"}, 
          {108, "et_"+extra+"m_sv"}
         };
         cats["mt_2016"] = {
          {100, "mt_"+extra+"pt_1"},
          {101, "mt_"+extra+"pt_2"},
          {102, "mt_"+extra+"met"},
          {103, "mt_"+extra+"pt_tt"},
          {104, "mt_"+extra+"m_vis"},
          {105, "mt_"+extra+"mjj"},
          {106, "mt_"+extra+"sjdphi"},  
          {107, "mt_"+extra+"n_jets"},
          {108, "mt_"+extra+"m_sv"}
         };
         cats["tt_2016"] = {
          {100, "tt_"+extra+"pt_1"},
          {101, "tt_"+extra+"pt_2"},
          {102, "tt_"+extra+"met"},
          {103, "tt_"+extra+"pt_tt"},
          {104, "tt_"+extra+"m_vis"},
          {105, "tt_"+extra+"mjj"},
          {106, "tt_"+extra+"sjdphi"},  
          {107, "tt_"+extra+"n_jets"},
          {108, "tt_"+extra+"m_sv"}
         };
         cats["em_2016"] = {
          {100, "em_"+extra+"pt_1"},
          {101, "em_"+extra+"pt_2"},
          {102, "em_"+extra+"met"},
          {103, "em_"+extra+"pt_tt"},
          {104, "em_"+extra+"m_vis"},
          {105, "em_"+extra+"mjj"},
          {106, "em_"+extra+"sjdphi"},
          {107, "em_"+extra+"n_jets"},
          {108, "em_"+extra+"m_sv"}
         }; 
       }
     if(era=="2017"){
        cats_cp["et_2017"] = {};
        cats_cp["mt_2017"] = {};
        cats_cp["tt_2017"] = {};
        cats_cp["em_2017"] = {};
        cats["et_2017"] = {
          {100, "et_"+extra+"pt_1"},
          {101, "et_"+extra+"pt_2"},
          {102, "et_"+extra+"met"},
          {103, "et_"+extra+"pt_tt"},
          {104, "et_"+extra+"m_vis"},
          {105, "et_"+extra+"mjj"},
          {106, "et_"+extra+"sjdphi"},
          {107, "et_"+extra+"n_jets"},
          {108, "et_"+extra+"m_sv"}
         };
         cats["mt_2017"] = {
          {100, "mt_"+extra+"pt_1"},
          {101, "mt_"+extra+"pt_2"},
          {102, "mt_"+extra+"met"},
          {103, "mt_"+extra+"pt_tt"},
          {104, "mt_"+extra+"m_vis"},
          {105, "mt_"+extra+"mjj"},
          {106, "mt_"+extra+"sjdphi"},
          {107, "mt_"+extra+"n_jets"},
          {108, "mt_"+extra+"m_sv"}
         };
         cats["tt_2017"] = {
          {100, "tt_"+extra+"pt_1"},
          {101, "tt_"+extra+"pt_2"},
          {102, "tt_"+extra+"met"},
          {103, "tt_"+extra+"pt_tt"},
          {104, "tt_"+extra+"m_vis"},
          {105, "tt_"+extra+"mjj"},
          {106, "tt_"+extra+"sjdphi"},
          {107, "tt_"+extra+"n_jets"},
          {108, "tt_"+extra+"m_sv"}
         };
         cats["em_2017"] = {
          {100, "em_"+extra+"pt_1"},
          {101, "em_"+extra+"pt_2"},
          {102, "em_"+extra+"met"},
          {103, "em_"+extra+"pt_tt"},
          {104, "em_"+extra+"m_vis"},
          {105, "em_"+extra+"mjj"},
          {106, "em_"+extra+"sjdphi"},
          {107, "em_"+extra+"n_jets"},
          {108, "em_"+extra+"m_sv"}
         };
       }

     }
    
    map<string, VString> sig_procs;
    sig_procs["ggH"] = {"ggH_ph_htt"};
    if(!useJHU) sig_procs["qqH"] = {"qqH_htt125","WH_htt125","ZH_htt125"};
    else sig_procs["qqH"] = {"qqHsm_htt125","WHsm_htt125","ZHsm_htt125"};
    sig_procs["qqH_BSM"] = {"qqHmm_htt","qqHps_htt","WHps_htt","WHmm_htt","ZHps_htt","ZHmm_htt"};
    sig_procs["ggHCP"] = {"ggHsm_htt", "ggHps_htt", "ggHmm_htt"};
    
    vector<string> masses = {"125"};    

    map<const std::string, float> sig_xsec_aachen;
    map<const std::string, float> sig_xsec_IC;
	
    sig_xsec_aachen["ggHsm_htt"] = 0.921684152;      
    sig_xsec_aachen["ggHmm_htt"] = 1.84349344;    
    sig_xsec_aachen["ggHps_htt"] = 0.909898616;    
    sig_xsec_aachen["qqHsm_htt"] = 0.689482928;    
    sig_xsec_aachen["qqHmm_htt"] = 0.12242788;    
    sig_xsec_aachen["qqHps_htt"] = 0.0612201968;

    sig_xsec_IC["ggHsm_htt"] = 0.3987;    
    sig_xsec_IC["ggHmm_htt"] = 0.7893;    
    sig_xsec_IC["ggHps_htt"] = 0.3858;    
    sig_xsec_IC["qqHsm_htt"] = 2.6707;    
    sig_xsec_IC["qqHmm_htt"] = 0.47421;    
    sig_xsec_IC["qqHps_htt"] = 0.2371314;    
    
    using ch::syst::bin_id;
    
    //! [part2]
    for(auto year: years) {
      for (auto chn : chns) {
          cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, cats[chn+"_"+year]);
          cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, cats_cp[chn+"_"+year]);

          cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, bkg_procs[chn], cats[chn+"_"+year], false);
          cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn+"_"+year}, bkg_procs[chn], cats_cp[chn+"_"+year], false);

          if(chn == "em" || chn == "et" || chn == "mt" || chn == "tt"){
            cb.AddProcesses({"*"},   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH"], cats[chn+"_"+year], false); // SM VBF/VH are added as backgrounds
            cb.AddProcesses({"*"},   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH"], cats_cp[chn+"_"+year], false);
 
            if(useJHU){
              cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH_BSM"], cats[chn+"_"+year], true); // Non-SM VBF/VH are added as signal
              cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["qqH_BSM"], cats_cp[chn+"_"+year], true);
            }

            cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["ggHCP"], cats[chn+"_"+year], true);
            cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn+"_"+year}, sig_procs["ggHCP"], cats_cp[chn+"_"+year], true);
          }
      }
    } 
    //! [part4]
    
    
    ch::AddSMRun2Systematics(cb, 0, ttbar_fit, no_jec_split);
    
    if(no_shape_systs){
      cb.FilterSysts([&](ch::Systematic *s){
        return s->type().find("shape") != std::string::npos;
      });
    }
    

    if (! only_init.empty()) {
        std::cout << "Write datacards (without shapes) to directory \"" << only_init << "\" and quit." << std::endl;
        ch::CardWriter tmpWriter("$TAG/$ANALYSIS_$ERA_$CHANNEL_$BINID_$MASS.txt", "$TAG/dummy.root");
        tmpWriter.WriteCards(only_init, cb);
        
        return 0;
    }
            
    //! [part7]
    for(auto year: years) {
      for (string chn : chns){
          string channel = chn;
          string extra = "";
          if (year == "2017" && !do_control_plots) extra = "/2017/";
          if(chn == "ttbar") channel = "em"; 
          cb.cp().channel({chn+"_"+year}).backgrounds().ExtractShapes(
                                                             input_dir[chn] + extra + "htt_"+channel+".inputs-sm-13TeV"+postfix+".root",
                                                             "$BIN/$PROCESS",
                                                             "$BIN/$PROCESS_$SYSTEMATIC");
          if(chn == "em" || chn == "et" || chn == "mt" || chn == "tt"){
            if(useJHU) {
              cb.cp().channel({chn+"_"+year}).process(sig_procs["qqH_BSM"]).ExtractShapes(
                                                                      input_dir[chn]+ extra + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                      "$BIN/$PROCESS$MASS",
                                                                      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
            }
            cb.cp().channel({chn+"_"+year}).process(sig_procs["ggH"]).ExtractShapes(
                                                                    input_dir[chn] + extra +  "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                    "$BIN/$PROCESS$MASS",
                                                                    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
            cb.cp().channel({chn+"_"+year}).process(sig_procs["ggHCP"]).ExtractShapes(
                                                                    input_dir[chn] + extra + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                                    "$BIN/$PROCESS$MASS",
                                                                    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
          }
      }
    }    

    
    //Now delete processes with 0 yield
    cb.FilterProcs([&](ch::Process *p) {
        bool null_yield = !(p->rate() > 0.);
        if (null_yield){
            std::cout << "[Null yield] Removing process with null yield: \n ";
            std::cout << ch::Process::PrintHeader << *p << "\n";
            cb.FilterSysts([&](ch::Systematic *s){
                bool remove_syst = (MatchingProcess(*p,*s));
                return remove_syst;
            });
        }
        return null_yield;
    });   
    
    
    // And convert any shapes in the ttbar CRs to lnN:
    // Convert all shapes to lnN at this stage

    cb.cp().channel({"ttbar_2016","ttbar_2017"}).syst_type({"shape"}).ForEachSyst([](ch::Systematic *sys) {
        sys->set_type("lnN");
        if(sys->value_d() <0.001) {sys->set_value_d(0.001);};
        if(sys->value_u() <0.001) {sys->set_value_u(0.001);};
    });

    
    std::vector<std::string> all_prefit_bkgs = {
        "QCD","ZL","ZJ","ZTT","TTJ","TTT","TT",
        "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
        "ggH_hww125","qqH_hww125","EWKZ", "qqHsm_htt125", "qqH_htt125", "WH_htt125", "ZH_htt125"};
    
        ////! Option to scale rate
    std::vector< std::string > sig_processes = {"ggHsm_htt125","ggHmm_htt125","ggHps_htt125","qqHsm_htt125","qqHmm_htt125","qqHps_htt125"};
     
    if (!scale_sig_procs.empty()) {	
    	cb.cp().PrintAll();		
        cb.ForEachProc([sig_xsec_IC, sig_xsec_aachen](ch::Process *p) { if (sig_xsec_IC.count(p->process()) ){std::cout << "Scaling " << p->process() << std::endl;  p->set_rate(p->rate() * sig_xsec_IC.at(p->process())/sig_xsec_aachen.at(p->process()) ); };});                 	
    };
    
    if(!real_data){
         for (auto b : cb.cp().bin_set()) {
             std::cout << " - Replacing data with asimov in bin " << b << "\n";
             cb.cp().bin({b}).ForEachObs([&](ch::Observation *obs) {
               obs->set_shape(cb.cp().bin({b}).backgrounds().process(all_prefit_bkgs).GetShape()+cb.cp().bin({b}).signals().process({"ggHsm_htt", "ggH_htt"}).mass({"125"}).GetShape(), true);
               obs->set_rate(cb.cp().bin({b}).backgrounds().process(all_prefit_bkgs).GetRate()+cb.cp().bin({b}).signals().process({"ggHsm_htt", "ggH_htt"}).mass({"125"}).GetRate());
             });
           }
   }   


    
    
    // can auto-merge the bins with bbb uncertainty > 90% - may be better to merge these bins by hand though!
    auto rebin = ch::AutoRebin()
    .SetBinThreshold(0.)
    .SetBinUncertFraction(0.9)
    .SetRebinMode(1)
    .SetPerformRebin(true)
    .SetVerbosity(1);
    if(auto_rebin) rebin.Rebin(cb, cb);
  
  
    // At this point we can fix the negative bins
    std::cout << "Fixing negative bins\n";
    cb.ForEachProc([](ch::Process *p) {
      if (ch::HasNegativeBins(p->shape())) {
         std::cout << "[Negative bins] Fixing negative bins for " << p->bin()
                   << "," << p->process() << "\n";
        auto newhist = p->ClonedShape();
        ch::ZeroNegativeBins(newhist.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        p->set_shape(std::move(newhist), false);
      }
    });
  
    cb.ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos) return;            
      if (ch::HasNegativeBins(s->shape_u()) || ch::HasNegativeBins(s->shape_d())) {
         std::cout << "[Negative bins] Fixing negative bins for syst" << s->bin()
               << "," << s->process() << "," << s->name() << "\n";
        auto newhist_u = s->ClonedShapeU();
        auto newhist_d = s->ClonedShapeD();
        ch::ZeroNegativeBins(newhist_u.get());
        ch::ZeroNegativeBins(newhist_d.get());
        // Set the new shape but do not change the rate, we want the rate to still
        // reflect the total integral of the events
        s->set_shapes(std::move(newhist_u), std::move(newhist_d), nullptr);
      }
  });

  cb.ForEachSyst([](ch::Systematic *s) {
      if (s->type().find("shape") == std::string::npos) return;
      if(!(s->value_d()<0.001 || s->value_u()<0.001)) return;
      std::cout << "[Negative yield] Fixing negative yield for syst" << s->bin()
               << "," << s->process() << "," << s->name() << "\n";
      if(s->value_u()<0.001){
         s->set_value_u(0.001);
         s->set_type("lnN");
      }
      if(s->value_d()<0.001){
         s->set_value_d(0.001);
         s->set_type("lnN");
      }
  });

    if(!cross_check && do_control_plots==0)  {

      // In this part we convert shape uncertainties into lnN where the shape variations are small compared to statistical uncertainties, this helps remove artificial constraints and makes the fit simpler

      // convert b-tag uncertainties to lnN:
      cb.cp().ForEachSyst([](ch::Systematic *s) {
        if (s->type().find("shape") == std::string::npos || s->type().find("CMS_eff_b") == std::string::npos) return;
           s->set_type("lnN");
      });
     

      // if the analysis changes the number of jdphi or mass bins (for boosted) category then these need to be changed here also
      int ndphibins = 12;
      int nmassbins = 10;

      // convert JES uncertainties to lnN:
      std::vector<std::string> systs_lnN = {"CMS_scale_j_eta3to5_13TeV","CMS_scale_j_eta0to5_13TeV","CMS_scale_j_eta0to3_13TeV","CMS_scale_j_RelativeBal_13TeV","CMS_scale_j_RelativeSample_13TeV","CMS_scale_j_13TeV"};
      for (auto i : systs_lnN) {
        // all 0jet JES uncerts to lnN
        ConvertShapesToLnN(cb.cp().bin_id({1}), i, 0.); 
        // all tt channel MC backgrounds except Higgs to lnN
        ConvertShapesToLnN(cb.cp().backgrounds().process({"TTT","VVT","EWKZ","ZL"}).channel({"tt","tt_2017","tt_2016"}), i, 0.);
        // EWKZ and ZLL (em channel) always small so convert to lnN
        ConvertShapesToLnN(cb.cp().backgrounds().process({"EWKZ","ZLL"}), i, 0.);
        // all backgrounds except ttbar and Higgs to lnN for dijet categories
        ConvertShapesToLnN(cb.cp().backgrounds().bin_id({3,4,5,6}).process({"W","VVT","VV","ZLL","ZL","EWKZ"}), i, 0.);
        // Convert VH processes to lnN
        ConvertShapesToLnN(cb.cp().process({"WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125","WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WH_htt","ZH_htt","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt"}), i, 0.);  
        // group mass bins for boosted categories to get smooth templates
        SmoothShapes(cb.cp().bin_id({2}), i, nmassbins, false, true, false);
        // group mass bins for dijet categories to get smooth templates
        SmoothShapes(cb.cp().bin_id({3,4,5,6}), i, ndphibins, false, false, true);
      }
      // convert MET unclustered energy uncertainties to lnN
      ConvertShapesToLnN(cb.cp().backgrounds(), "CMS_scale_met_unclustered_13TeV", 0.);
      //for tt channel lnN uncertainties are not needed for 0 jet and boosted categories as MET is not used in selection cuts so these are removed completly
      cb.cp().backgrounds().channel({"tt","tt_2016","tt_2017"}).FilterSysts([&](ch::Systematic *s){
        bool remove_syst = (s->name().find("CMS_scale_met_unclustered_13TeV") != std::string::npos);
        return remove_syst;
      });

      // MET response and resolution uncertainties for recoil corrected samples
      // EWKZ always small so set to lnN
      ConvertShapesToLnN(cb.cp().backgrounds().process({"EWKZ"}), "CMS_htt_boson_reso_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"EWKZ"}), "CMS_htt_boson_scale_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZLL","W"}).channel({"em","em_2016","em_2017"}), "CMS_htt_boson_reso_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZLL","W"}).channel({"em","em_2016","em_2017"}), "CMS_htt_boson_scale_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZL"}).channel({"tt","tt_2016","tt_2017"}), "CMS_htt_boson_reso_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZL"}).channel({"tt","tt_2016","tt_2017"}), "CMS_htt_boson_scale_met_13TeV", 0.);
      // merge together mass bins for boosted category
      SmoothShapes(cb.cp().bin_id({2}).process({"ZL","ggHsm_htt","ggHmm_htt","ggHps_htt","qqH_htt","qqHsm_htt","qqHps_htt","qqHmm_htt","qqH_htt125","qqHsm_htt125","qqHps_htt125","qqHmm_htt125","WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125","WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WH_htt","ZH_htt","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt"}), "CMS_htt_boson_reso_met_13TeV", nmassbins, false, true, false);
      SmoothShapes(cb.cp().bin_id({2}).process({"ZL","ggHsm_htt","ggHmm_htt","ggHps_htt","qqH_htt","qqHsm_htt","qqHps_htt","qqHmm_htt","qqH_htt125","qqHsm_htt125","qqHps_htt125","qqHmm_htt125","WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125","WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WH_htt","ZH_htt","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt"}), "CMS_htt_boson_scale_met_13TeV", nmassbins, false, true, false);
      // lnN uncertainties for ZL in dijet categories
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZL"}).bin_id({3,4,5,6}), "CMS_htt_boson_reso_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().backgrounds().process({"ZL"}).bin_id({3,4,5,6}), "CMS_htt_boson_scale_met_13TeV", 0.);
      // merge jdphi bins for signal in dijet categories
      SmoothShapes(cb.cp().bin_id({3,4,5,6}).process({"ggHsm_htt","ggHmm_htt","ggHps_htt","qqH_htt","qqHsm_htt","qqHps_htt","qqHmm_htt","qqH_htt125","qqHsm_htt125","qqHps_htt125","qqHmm_htt125"}), "CMS_htt_boson_reso_met_13TeV", ndphibins, false, true, false);
      SmoothShapes(cb.cp().bin_id({3,4,5,6}).process({"ggHsm_htt","ggHmm_htt","ggHps_htt","qqH_htt","qqHsm_htt","qqHps_htt","qqHmm_htt","qqH_htt125","qqHsm_htt125","qqHps_htt125","qqHmm_htt125"}), "CMS_htt_boson_scale_met_13TeV", ndphibins, false, true, false);

      ConvertShapesToLnN(cb.cp().bin_id({3,4,5,6}).process({"WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125","WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WH_htt","ZH_htt","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt"}), "CMS_htt_boson_reso_met_13TeV", 0.);
      ConvertShapesToLnN(cb.cp().bin_id({3,4,5,6}).process({"WH_htt125","ZH_htt125","WHsm_htt125","ZHsm_htt125","WHps_htt125","ZHps_htt125","WHmm_htt125","ZHmm_htt125","WH_htt","ZH_htt","WHsm_htt","ZHsm_htt","WHps_htt","ZHps_htt","WHmm_htt","ZHmm_htt"}), "CMS_htt_boson_scale_met_13TeV", 0.);

      // tau ES / electron uncertainties. Keep these as shape uncertainties but for the dijet categpory group jdphi bins together to improve statistics
      std::vector<std::string> systs_ES = {"CMS_scale_t_1prong_13TeV","CMS_scale_t_1prong1pizero_13TeV","CMS_scale_t_3prong_13TeV","CMS_scale_e_13TeV"};
      for (auto i : systs_ES) {
        SmoothShapes(cb.cp().bin_id({3,4,5,6}), i, ndphibins, false, true, false);
      }
      ConvertShapesToLnN(cb.cp().backgrounds().process({"EWKZ"}).channel({"em","em_2016","em_2017"}), "CMS_scale_e_13TeV", 0.);

    }

    // de-correlate systematics for 2016 and 2017
    if((era.find("2016") != std::string::npos && era.find("2017") != std::string::npos) ||  era.find("all") != std::string::npos){
      std::cout << "Partially Decorrelating systematics for 2016/2017" << std::endl;
      Json::Value js;
      string json_file = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTSMCP2016/scripts/correlations.json";
      js = ch::ExtractJsonFromFile(json_file);
      std::vector<std::string> keys = js.getMemberNames();
      for (std::vector<std::string>::const_iterator it = keys.begin(); it != keys.end(); ++it){
        string name = *it;
        double value = js[*it].asDouble();
        std::vector<string> chans_2016 = {"em","em_2016","et","et_2016","mt","mt_2016","tt","tt_2016","ttbar","ttbar_2016"};
        std::vector<string> chans_2017 = {"em_2017","et_2017","mt_2017","tt_2017","ttbar_2017"};
        DecorrelateSyst (cb, name, value, chans_2016, chans_2017);
      }
    }

 
    ////! [part8]
    // add bbb uncertainties for all backgrounds
    auto bbb = ch::BinByBinFactory()
    .SetPattern("CMS_$ANALYSIS_$CHANNEL_$BIN_$ERA_$PROCESS_bin_$#")
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.4)
    .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);

    //// add bbb uncertainties for the signal but only if uncertainties are > 5% and only for categories with significant amount of signal events to reduce the total number of bbb uncertainties
    //auto bbb_sig = ch::BinByBinFactory()
    //.SetPattern("CMS_$ANALYSIS_$CHANNEL_$BIN_$ERA_$PROCESS_bin_$#")
    //.SetAddThreshold(0.05)
    //.SetMergeThreshold(0.0)
    //.SetFixNorm(false);
    //bbb_sig.AddBinByBin(cb.cp().signals().bin_id({1,2,3,4,5,6,31,32,41,42}),cb); 

	
	//// rename embedded energy-scale uncertainties so that they are not correlated with MC energy-scales
	//cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_e_13TeV","CMS_scale_embedded_e_13TeV"); 
	//cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_1prong_13TeV","CMS_scale_embedded_t_1prong_13TeV");
	//cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_1prong1pizero_13TeV","CMS_scale_embedded_t_1prong1pizero_13TeV");
	//cb.cp().process({"EmbedZTT"}).RenameSystematic(cb,"CMS_scale_t_3prong_13TeV","CMS_scale_embedded_t_3prong_13TeV");

	
	// This function modifies every entry to have a standardised bin name of
	// the form: {analysis}_{channel}_{bin_id}_{era}
	// which is commonly used in the htt analyses
	ch::SetStandardBinNames(cb);
	//! [part8]
	

	//! [part9]
	// First we generate a set of bin names:
	

	//Write out datacards. Naming convention important for rest of workflow. We
	//make one directory per chn-cat, one per chn and cmb. In this code we only
	//store the individual datacards for each directory to be combined later, but
	//note that it's also possible to write out the full combined card with CH
	string output_prefix = "output/";
	if(output_folder.compare(0,1,"/") == 0) output_prefix="";
	ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
	    	    output_prefix + output_folder + "/$TAG/common/htt_input.root");
	
	
	if(do_control_plots==0) writer.WriteCards("cmb", cb);
	//Add all di-jet categories combined
	//
	
        writer.WriteCards("htt_2016", cb.cp().channel({"em_2016","et_2016","mt_2016","tt_2016","ttbar_2016"}));
        writer.WriteCards("htt_2017", cb.cp().channel({"em_2017","et_2017","mt_2017","tt_2017","ttbar_2017"})); 

	writer.WriteCards("htt_0jet", cb.cp().bin_id({1}));
	writer.WriteCards("htt_boosted", cb.cp().bin_id({2}));
	writer.WriteCards("htt_01jet", cb.cp().bin_id({1,2}));
	writer.WriteCards("htt_dijet", cb.cp().bin_id({3,4,5,6}));
	for (auto chn : cb.channel_set()) {
		 writer.WriteCards("htt_"+chn+"_dijet", cb.cp().channel({chn}).bin_id({3,4,5,6}));  

        // per-channel
	    writer.WriteCards(chn, cb.cp().channel({chn}));
        // And per-channel-category
        if (!do_mva) {
          writer.WriteCards("htt_"+chn+"_1_13TeV", cb.cp().channel({chn}).bin_id({1}));
          writer.WriteCards("htt_"+chn+"_2_13TeV", cb.cp().channel({chn}).bin_id({2}));
	  writer.WriteCards("htt_"+chn+"_3_13TeV", cb.cp().channel({chn}).bin_id({3}));
	  writer.WriteCards("htt_"+chn+"_4_13TeV", cb.cp().channel({chn}).bin_id({4}));
          writer.WriteCards("htt_"+chn+"_5_13TeV", cb.cp().channel({chn}).bin_id({5}));
          writer.WriteCards("htt_"+chn+"_6_13TeV", cb.cp().channel({chn}).bin_id({6}));
	}
        else {
          writer.WriteCards("htt_"+chn+"_31_13TeV", cb.cp().channel({chn}).bin_id({31}));
          writer.WriteCards("htt_"+chn+"_32_13TeV", cb.cp().channel({chn}).bin_id({32}));
          writer.WriteCards("htt_"+chn+"_33_13TeV", cb.cp().channel({chn}).bin_id({33}));
          writer.WriteCards("htt_"+chn+"_34_13TeV", cb.cp().channel({chn}).bin_id({34}));
          writer.WriteCards("htt_"+chn+"_35_13TeV", cb.cp().channel({chn}).bin_id({35}));
          writer.WriteCards("htt_"+chn+"_36_13TeV", cb.cp().channel({chn}).bin_id({36}));
          writer.WriteCards("htt_"+chn+"_37_13TeV", cb.cp().channel({chn}).bin_id({37}));
          writer.WriteCards("htt_"+chn+"_38_13TeV", cb.cp().channel({chn}).bin_id({38}));
          writer.WriteCards("htt_"+chn+"_39_13TeV", cb.cp().channel({chn}).bin_id({39}));
          writer.WriteCards("htt_"+chn+"_41_13TeV", cb.cp().channel({chn}).bin_id({41}));
          writer.WriteCards("htt_"+chn+"_42_13TeV", cb.cp().channel({chn}).bin_id({42}));
          writer.WriteCards("htt_"+chn+"_43_13TeV", cb.cp().channel({chn}).bin_id({43}));
          writer.WriteCards("htt_"+chn+"_44_13TeV", cb.cp().channel({chn}).bin_id({44}));
          writer.WriteCards("htt_"+chn+"_45_13TeV", cb.cp().channel({chn}).bin_id({45}));
          writer.WriteCards("htt_"+chn+"_46_13TeV", cb.cp().channel({chn}).bin_id({46}));
          writer.WriteCards("htt_"+chn+"_47_13TeV", cb.cp().channel({chn}).bin_id({47}));
          writer.WriteCards("htt_"+chn+"_48_13TeV", cb.cp().channel({chn}).bin_id({48}));
          writer.WriteCards("htt_"+chn+"_49_13TeV", cb.cp().channel({chn}).bin_id({49}));
          writer.WriteCards("htt_"+chn+"_lowMjj_13TeV", cb.cp().channel({chn}).bin_id({31,32,33,34,35,36,37,38,39}));
          writer.WriteCards("htt_"+chn+"_highMjj_13TeV", cb.cp().channel({chn}).bin_id({41,42,43,44,45,46,47,48,49}));
        }
        
        
    }
    
    writer.WriteCards("htt_cmb_bkgs_13TeV", cb.cp().bin_id({33,34,35,36,37,38,39,43,44,45}));
    writer.WriteCards("htt_cmb_highMjj_13TeV", cb.cp().bin_id({41,42,43,44,45,46,47}));
    
    cb.PrintAll();
    cout << " done\n";
    
    
}
