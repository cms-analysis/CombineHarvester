#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char** argv) {

  typedef vector<string> VString;
  string in_dir = string(getenv("CMSSW_BASE")) + "/src/MSSM-projection/LIMITS111215-legacymssm-unblind/plain/";


//  VString dirs =  {"mt","et","tt","em","cmb","btag","nobtag","nobtag-em","nobtag-et","nobtag-mt","nobtag-tt","btag-tt","btag-em","btag-et","btag-mt"};
  VString chns = {"mt","et","tt","em"};

  VString masses={"90","100","110","120","130","140","160","180","200","250","300","350","400","450","500","600","700","800","900","1000"};
    


     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/mt/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"mt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"mt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"mt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }

     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/et/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"et/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"et/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"et/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }


     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/tt/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"tt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"tt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"tt/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }
     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/em/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"em/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"em/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"em/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }
     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/cmb/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"cmb/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }


     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/btag/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"btag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"btag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"btag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }

     for(string ms:masses){
        ch::CombineHarvester cb;
        string folder = "LegacyMSSMProjection/nobtag/"+ms+"/";
      for(string chn:chns){
        for(string bin_id : {"8","9"}){
          if(boost::filesystem::exists((in_dir+"nobtag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str())){
            cb.ParseDatacard(in_dir+"nobtag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt","$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
          } else std::cout<<(in_dir+"nobtag/"+ms+"/htt_"+chn+"_"+bin_id+"_8TeV.txt").c_str()<<" Doesn't exist"<<std::endl;
        }
        
        }
boost::filesystem::create_directories(folder);
        ch::SetStandardBinNames(cb);
        cb.cp().process({"QCD"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3./9));//9 = Lumi factor
        });
        cb.cp().process({"ZTT","ZL","ZJ","ZLL"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.706/9));//9 = Lumi factor
        });
        cb.cp().process({"TT"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(3.3/9));//9 = Lumi factor
        });
        cb.cp().process({"VV"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(2./9));//9 = Lumi factor
        });
        cb.cp().process({"W"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1.676/9));//9 = Lumi factor
        });
        cb.cp().process({"ggH","bbH"}).ForEachProc([&](ch::Process *proc){
         proc->set_rate(proc->rate()*(double)(1./9));//9 = Lumi factor
        });


        TFile output((folder + "/htt_mssm_input.root").c_str(), "RECREATE");
        cb.cp().WriteDatacard(folder + "/htt_mssm.txt", output);
     }




  }
            



