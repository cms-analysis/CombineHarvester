#include <vector>
#include "boost/program_options.hpp"
#include "TSystem.h"
#include "RooWorkspace.h"
#include "RooBinning.h"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/ParseCombineWorkspace.h"

struct ChannelInfo {
  RooAbsData const* obs;
  RooArgSet const* obs_set;
  unsigned nvars;
  std::vector<RooRealVar*> bin_vars;
  std::vector<std::vector<double>> bin_centers;
  std::vector<std::vector<double>> bin_widths;
  unsigned nbins;
  std::vector<RooAbsReal const*> bkgs;
  std::vector<RooAbsReal const*> sigs;
  std::vector<RooAbsReal const*> c_bkgs;
  std::vector<RooAbsReal const*> c_sigs;
  std::vector<RooRealVar*> pdf_vars;
  RooArgSet *pdf_obs_set;
};

struct SBValues {
  std::vector<double> bkg;
  std::vector<double> sig;
  std::vector<double> dat;
  std::vector<int> ibin;
};

std::map<std::string, ChannelInfo> BuildChannelInfo(ch::CombineHarvester &cb, std::vector<std::string> sig_def) {
  std::map<std::string, ChannelInfo> res;

  for (auto const &b : cb.bin_set()) {
    auto &info = res[b];
    std::cout << ">> " << b << std::endl;
    auto cb_bin = cb.cp().bin({b});
    info.obs = nullptr;
    cb_bin.cp().bin({b}).ForEachObs([&](ch::Observation *o) { info.obs = o->data(); });

    info.obs_set = info.obs->get();
    info.obs_set->Print("v");
    info.nvars = info.obs_set->getSize();

    info.nbins = 1;

    auto it = info.obs_set->createIterator();
    RooRealVar *var = dynamic_cast<RooRealVar *>(it->Next());
    while (var) {
      info.bin_vars.push_back(var);
      info.nbins *= var->getBins();
      std::vector<double> centers(info.nbins);
      std::vector<double> widths(info.nbins);
      var->getBinning().Print();
      RooUniformBinning *binning = dynamic_cast<RooUniformBinning *>(&var->getBinning());
      for (unsigned i = 0; i < unsigned(var->getBins()); ++i) {
        centers[i] = binning->binCenter(i);
        widths[i] = binning->binWidth(i);
      }
      info.bin_centers.push_back(centers);
      info.bin_widths.push_back(widths);
      // var->Print("v");
      var = dynamic_cast<RooRealVar *>(it->Next());
    };
    std::cout << "Total bins = " << info.nbins << std::endl;

    std::vector<double> bkg(info.nbins);
    std::vector<double> sig(info.nbins);
    std::vector<double> dat(info.nbins);

    cb_bin.SetFlag("filters-use-regex", true);
    auto all_procs = cb_bin.cp().process(sig_def, true).process_set();
    for (auto proc : all_procs) std::cout << proc << "\t";
    std::cout << std::endl;
    cb_bin.cp().process(sig_def, false).ForEachProc([&](ch::Process *proc) {
      info.bkgs.push_back(proc->pdf());
      info.c_bkgs.push_back(proc->norm());
    });
    cb_bin.cp().process(sig_def, true).ForEachProc([&](ch::Process *proc) {
      info.sigs.push_back(proc->pdf());
      info.c_sigs.push_back(proc->norm());
    });
    cb_bin.SetFlag("filters-use-regex", false);


    info.pdf_obs_set = info.bkgs[0]->getObservables(info.obs);
    info.pdf_obs_set->Print("v");
    for (unsigned i = 0; i < info.bin_vars.size(); ++i) {
      info.pdf_vars.push_back(
          dynamic_cast<RooRealVar *>(info.pdf_obs_set->find(info.bin_vars[i]->GetName())));
    }

  }

  return res;
}


std::map<std::string, SBValues> FillSB(std::map<std::string, ChannelInfo> &infomap, TH1* proto, bool fill_data) {
  std::map<std::string, SBValues> res;
  for (auto & it : infomap) {
    // std::cout << ">> " << it.first << "\n";
    SBValues & binres = res[it.first];
    ChannelInfo & info = it.second;
    binres.bkg = std::vector<double>(info.nbins);
    binres.sig = std::vector<double>(info.nbins);
    binres.dat = std::vector<double>(info.nbins);
    binres.ibin = std::vector<int>(info.nbins);

    std::vector<unsigned> current_idx(info.nvars);
    for (unsigned v = 0; v < info.nvars; ++v) {
      current_idx[v] = 0;
    }

    unsigned global_bin = 0;
    for (unsigned v = 0; v < info.nbins; ++v) {
        // std::cout << "Current bin centers:";
        // for (unsigned v2 = 0; v2 < info.nvars; ++v2) {
        //   std::cout << "\t" << info.bin_centers[v2][current_idx[v2]];
        // }
        // std::cout << std::endl;

        double volume = 1.0;
        for (unsigned v2 = 0; v2 < info.nvars; ++v2) {
          volume *= info.bin_widths[v2][current_idx[v2]];
          info.pdf_vars[v2]->setVal(info.bin_centers[v2][current_idx[v2]]);
        }

        for (unsigned bi = 0; bi < info.bkgs.size(); ++bi) {
          binres.bkg[global_bin] += info.bkgs[bi]->getVal(info.pdf_obs_set) * volume * info.c_bkgs[bi]->getVal();
          // std::cout << bi << "\t" << bkgs[bi]->getVal(pdf_obs_set) << std::endl;
        }
        for (unsigned si = 0; si < info.sigs.size(); ++si) {
          // if (v == 0) {
          //   info.sigs[si]->getParameters(info.pdf_obs_set)->Print("v");
          // }
          binres.sig[global_bin] += info.sigs[si]->getVal(info.pdf_obs_set) * volume * info.c_sigs[si]->getVal();
          // std::cout << volume << "\t" << c_sigs[si]->getVal() << "\n";
          // std::cout << bi << "\t" << bkgs[bi]->getVal(pdf_obs_set) << std::endl;
        }

        // Update current indicies
        for (unsigned v2 = 0; v2 < info.nvars; ++v2) {
          if ((current_idx[v2]+1) < info.bin_centers[v2].size()) {
            current_idx[v2] += 1;
            break;
          } else {
            current_idx[v2] = 0;
          }
        }
        ++global_bin;
    }

    std::vector<unsigned> current_data_bin(info.nvars);
    for (unsigned i = 0; i < unsigned(info.obs->numEntries()); ++i) {
      auto args = info.obs->get(i);
      // args->Print("v");
      for (unsigned v = 0; v < info.pdf_vars.size(); ++v) {
        current_data_bin[v] = info.pdf_vars[v]->getBinning().binNumber(dynamic_cast<RooRealVar*>(args->find(info.pdf_vars[v]->GetName()))->getVal());
      }
      // Now calculate the global bin index:
      unsigned global_dat_bin = 0;
      for (unsigned v = 0; v < info.pdf_vars.size(); ++v) {
        unsigned part = current_data_bin[v];
        for (int v2 = (v-1); v2 >= 0; --v2) {
          part *= info.bin_centers[v2].size();
        }
        global_dat_bin += part;
      }
      binres.dat[global_dat_bin] += info.obs->weight();
    }

    double total_bkg = 0.;
    double total_sig = 0.;
    double total_dat = 0.;
    for (unsigned i = 0; i < info.nbins; ++i) {
      // std::cout << "\t" << binres.bkg[i];
      total_bkg += binres.bkg[i];
    }
    // std::cout <<std::endl;
    for (unsigned i = 0; i < info.nbins; ++i) {
      // std::cout << "\t" << binres.sig[i];
      total_sig += binres.sig[i];
    }
    // std::cout << std::endl;
    for (unsigned i = 0; i < info.nbins; ++i) {
      // std::cout << "\t" << binres.dat[i];
      total_dat += binres.dat[i];
    }
    // std::cout << std::endl;
    // std::cout << "Total bkg: " << total_bkg << std::endl;
    // std::cout << "Total sig: " << total_sig << std::endl;
    // std::cout << "Total dat: " << total_dat << std::endl;

    for (unsigned i = 0; i < info.nbins; ++i) {
      int final_bin = 1;
      if (binres.sig[i] > 0. && binres.bkg[i] > 0.) {
        double sb = std::log10(binres.sig[i]/binres.bkg[i]);
        final_bin = proto->GetXaxis()->FindFixBin(sb);
      }
      binres.ibin[i] = final_bin;
    }
  }
  return res;
}

void AppendToHists(std::map<std::string, SBValues> & sbmap_bins, std::map<std::string, SBValues> & sbmap_vals, TH1 *h_bkg, TH1 *h_sig, TH1 *h_dat) {
  for (auto & it : sbmap_bins) {
    auto & sb_bins = it.second;
    auto & sb_vals = sbmap_vals[it.first];
    for (unsigned i = 0; i < sb_bins.bkg.size(); ++i) {
      if (h_bkg) h_bkg->SetBinContent(sb_bins.ibin[i], h_bkg->GetBinContent(sb_bins.ibin[i]) + sb_vals.bkg[i]);
      if (h_sig) h_sig->SetBinContent(sb_bins.ibin[i], h_sig->GetBinContent(sb_bins.ibin[i]) + sb_vals.sig[i]);
      if (h_dat) h_dat->SetBinContent(sb_bins.ibin[i], h_dat->GetBinContent(sb_bins.ibin[i]) + sb_vals.dat[i]);
    }
  }
}

int main(int argc, char* argv[]) {
  bool prefit_assignment = false;
  std::string outname = "sb_weighted_prefit_assignment";
  if (!prefit_assignment) {
    outname = "sb_weighted_post_assignment";
  }

  gSystem->Load("libHiggsAnalysisCombinedLimit");

  ch::CombineHarvester cb;
  cb.SetFlag("workspaces-use-clone", true);
  TFile fin("comb_2017_Hbb_mu_vhonly_plus_run1.root");
  RooWorkspace *w = (RooWorkspace*)fin.Get("w");
  ch::ParseCombineWorkspace(cb, *w, "ModelConfig", "data_obs", true);

  TFile fitres("fitDiagnosticsA1_VHbb_ForSBordered_RH.root");
  RooFitResult *res = (RooFitResult*)fitres.Get("fit_s");

  double xbins[11]={-4,-3,-2.25,-1.75,-1.5,-1.25,-1.0,-0.75,-0.5,0};
  TH1F h_bkg("h_bkg", "h_bkg", 10,xbins);
  TH1F h_bkg_err("h_bkg_err", "h_bkg_err", 10,xbins);
  TH1F h_sig("h_sig", "h_sig", 10, xbins);
  TH1F h_sig_mu1("h_sig_mu1", "h_sig_mu1", 10,xbins);
  TH1F h_dat("h_dat", "h_dat", 10,xbins);

  auto chn_info = BuildChannelInfo(cb, std::vector<std::string>{".*H_h.*",".*H_lep_h.*"});

  double bf = 1.0;

  if (!prefit_assignment) {
    cb.UpdateParameters(res);
    bf = cb.GetParameter("mu_BR_bb")->val();
    cb.GetParameter("mu_BR_bb")->set_val(1.0);
  }


  // Bin assignment will be based on prefit values (mu=1)
  auto initial_sb = FillSB(chn_info, &h_bkg, true);


  // Now update to post-fit values
  cb.UpdateParameters(res);

  // Get the distributions
  auto post_sb = FillSB(chn_info, &h_bkg, true);
  AppendToHists(initial_sb, post_sb, &h_bkg, &h_sig, &h_dat);

  // Do the background sampling
  // -----------------------------------------------------------------------------
  unsigned n_samples = 200;
  auto backup = cb.GetParameters();

  // Calling randomizePars() ensures that the RooArgList of sampled parameters
  // is already created within the RooFitResult
  RooArgList const& rands = res->randomizePars();

  // Now create two aligned vectors of the RooRealVar parameters and the
  // corresponding ch::Parameter pointers
  int n_pars = rands.getSize();
  std::vector<RooRealVar const*> r_vec(n_pars, nullptr);
  std::vector<ch::Parameter*> p_vec(n_pars, nullptr);

  for (int i = 1; i <= h_bkg.GetNbinsX(); ++i) {
    h_bkg.SetBinError(i, 0.);
  }
  for (unsigned n = 0; n < p_vec.size(); ++n) {
    r_vec[n] = dynamic_cast<RooRealVar const*>(rands.at(n));
    p_vec[n] = cb.GetParameter(r_vec[n]->GetName());
  }

  // Main loop through n_samples
  for (unsigned i = 0; i < n_samples; ++i) {
    std::cout << ">> random " << i << "\n";
    // Randomise and update values
    res->randomizePars();
    for (int n = 0; n < n_pars; ++n) {
      if (p_vec[n]) p_vec[n]->set_val(r_vec[n]->getVal());
    }
    auto post_sb_err = FillSB(chn_info, &h_bkg, false);
    h_bkg_err.Reset();
    AppendToHists(initial_sb, post_sb_err, &h_bkg_err, nullptr, nullptr);
    for (int i = 1; i <= h_bkg.GetNbinsX(); ++i) {
      h_bkg.SetBinError(i, h_bkg.GetBinError(i) + std::pow(h_bkg_err.GetBinContent(i) - h_bkg.GetBinContent(i), 2.));
    }
  }
  for (int i = 1; i <= h_bkg.GetNbinsX(); ++i) {
    h_bkg.SetBinError(i, std::sqrt(h_bkg.GetBinError(i)/double(n_samples)));
  }
  cb.UpdateParameters(backup);
  // -----------------------------------------------------------------------------


  // Get the distributions with mu fixed to 1.0
  bf = cb.GetParameter("mu_BR_bb")->val();
  cb.GetParameter("mu_BR_bb")->set_val(1.0);
  // Get the distributions
  auto post_mu1_sb = FillSB(chn_info, &h_bkg, true);
  AppendToHists(initial_sb, post_mu1_sb, nullptr, &h_sig_mu1, nullptr);



  cb.GetParameter("mu_BR_bb")->set_val(bf);



  TFile outfile((outname+".root").c_str(), "RECREATE");
  h_bkg.Write();
  h_sig.Write();
  h_sig_mu1.Write();
  h_dat.Write();
  outfile.Close();
  return 0;
}
