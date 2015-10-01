#include <iostream>
#include <vector>
#include <map>
#include "boost/lexical_cast.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/format.hpp"
#include "boost/bind.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"

namespace po = boost::program_options;

using namespace std;

// Struct holds info on each column in the table
struct ColInfo {
  string label;             // Latex title, e.g. "No B-Tag"
  vector<string> cats_str;  // Category bin ids as strings
  vector<int> cats_int;     // Category bin ids as ints
  string era;               // e.g. "8TeV"
  double lumi;              // pb-1
};

// Struct holds info on each background row in the table
struct BkgInfo {
  string label;          // Latex title, e.g. "$\\PW$+jets"
  vector<string> procs;  // Datacard processes to combine for this entry
  BkgInfo(string const& l, vector<string> const& p) : label(l), procs(p) {}
};

int main(int argc, char* argv[]) {
  string channel = "";
  vector<string> columns;
  vector<string> eras;
  vector<string> datacards;
  vector<string> sig_datacards;
  string fitresult_file = "";
  string signal_mass    = "";
  string tanb           = "";
  bool postfit          = true;
  std::string header    = "";

  po::options_description config("Configuration");
  config.add_options()
    ("channel",
      po::value<string>(&channel)->required(), "channel")
    ("columns",
      po::value<vector<string>> (&columns)->multitoken()->required(), "labels")
    ("eras",
      po::value<vector<string>> (&eras)->multitoken()->required(), "eras")
    ("datacard,d",
      po::value<vector<string>> (&datacards)->multitoken()->required())
    ("sig_datacard,s",
      po::value<vector<string>> (&sig_datacards)->multitoken()->required())
    ("fitresult,f",
      po::value<string> (&fitresult_file))
    ("signal_mass",
      po::value<string>(&signal_mass)->required(), "signal_mass")
    ("tanb",
      po::value<string>(&tanb)->default_value("8"), "tanb")
    ("header",
      po::value<string>(&header)->default_value(""), "header")
    ("postfit",
      po::value<bool>(&postfit)->required(), "postfit");
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv)
                .options(config)
                .allow_unregistered()
                .run(),
            vm);
  po::notify(vm);

  double d_tanb = boost::lexical_cast<double>(tanb);

  // Signal processes
  vector<string> signal_procs = {"ggH", "bbH"};
  unsigned n_sig = signal_procs.size();

  // Eras
  unsigned n_eras = eras.size();
  vector<string> v_eras;
  vector<string> v_eras_lumi;
  for (unsigned i = 0; i < eras.size(); ++i) {
    vector<string> tmp;
    boost::split(tmp, eras[i], boost::is_any_of(":"));
    v_eras.push_back(tmp.at(0));
    v_eras_lumi.push_back(tmp.at(1));
  }

  // Table columns
  vector<ColInfo> col_info;
  col_info.resize(columns.size() * n_eras);
  for (unsigned k =0; k < n_eras; ++k) {
    for (unsigned i = 0; i < columns.size(); ++i) {
      unsigned idx = k * columns.size() + i;
      ColInfo & info = col_info[idx];
      vector<string> tmp_split;
      boost::split(tmp_split, columns[i], boost::is_any_of(":"));
      info.label = tmp_split[0];
      boost::split(info.cats_str, tmp_split[1], boost::is_any_of("+"));
      for (auto const& str : info.cats_str)
        info.cats_int.push_back(boost::lexical_cast<int>(str));
      info.era = v_eras[k];
      info.lumi = boost::lexical_cast<double>(v_eras_lumi[k]);
    }
  }
  unsigned n_cols = col_info.size();

  // Create some arrays to track to the signal efficiencies
  double signal_den[n_cols][n_sig];
  double signal_num[n_cols][n_sig];
  double signal_eff[n_cols][n_sig];

  // We can fill the denominator already
  for (unsigned i = 0; i < n_sig; ++i) {
    for (unsigned j = 0; j < n_cols; ++j) {
      signal_den[j][i] = col_info[j].lumi;
    }
  }

  // Channel-specific background configuration
  vector<BkgInfo> bkgs;
  vector<string> total_bkg;
  if (channel == "et" || channel == "mt" || channel == "tt") {
    bkgs = {
      BkgInfo("$\\cPZ\\rightarrow \\Pgt\\Pgt$",       {"ZTT"}),
      BkgInfo("QCD",                                  {"QCD"}),
      BkgInfo("$\\PW$+jets",                          {"W"}),
      BkgInfo("$\\cPZ$+jets (l/jet faking $\\Pgt$)",  {"ZL", "ZJ"}),
      BkgInfo("$\\cPqt\\cPaqt$",                      {"TT"}),
      BkgInfo("Di-bosons + single top",               {"VV"})
    };
    total_bkg = {"ZTT", "QCD", "W", "ZL", "ZJ", "TT", "VV"};
  }
  if (channel == "em") {
    bkgs = {
      BkgInfo("$\\cPZ\\rightarrow \\Pgt\\Pgt$",    {"Ztt"}),
      BkgInfo("QCD",                               {"Fakes"}),
      BkgInfo("$\\cPqt\\cPaqt$",                   {"ttbar"}),
      BkgInfo("Di-bosons + single top",            {"EWK"})
    };
    total_bkg = {"Ztt", "Fakes", "ttbar", "EWK"};
  }
  if (channel == "mm") {
    bkgs = {
      BkgInfo("$\\cPZ\\rightarrow \\Pgt\\Pgt$",    {"ZTT"}),
      BkgInfo("$\\cPZ\\rightarrow \\mu\\mu$",      {"ZMM"}),
      BkgInfo("QCD",                               {"QCD"}),
      BkgInfo("$\\cPqt\\cPaqt$",                   {"TTJ"}),
      BkgInfo("Di-bosons + single top",            {"WJets", "Dibosons"})
    };
    total_bkg = {"ZTT", "ZMM", "QCD", "TTJ", "WJets", "Dibosons"};
  }
  unsigned n_bkg = bkgs.size();

  //---------------------------------------------------------------------------
  // Now we parse the datacards and ROOT files
  //---------------------------------------------------------------------------

  ch::CombineHarvester cmb;
  for (auto const& d : datacards) {
    cmb.ParseDatacard(d, "", "", "", 0, signal_mass);
  }

  cmb.ForEachObj(boost::bind(ch::SetFromBinName, _1,
                             "$ANALYSIS_$CHANNEL_$BINID_$ERA"));

  cmb.cp().signals().ForEachProc([&](ch::Process *p) {
    p->set_rate(p->rate() * d_tanb);
  });

  ch::CombineHarvester sig_cmb;
  for (auto const& d : sig_datacards) {
    sig_cmb.ParseDatacard(d, "$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");
  }

  RooFitResult *fitresult = nullptr;
  if (fitresult_file.length() && postfit) {
    fitresult =
        new RooFitResult(ch::OpenFromTFile<RooFitResult>(fitresult_file));
    auto fitparams = ch::ExtractFitParameters(*fitresult);
    cmb.UpdateParameters(fitparams);
    sig_cmb.UpdateParameters(fitparams);
  }
  cmb.channel({channel});

  double bkg_yields[n_cols][n_bkg];
  double bkg_errors[n_cols][n_bkg];
  double tot_yields[n_cols];
  double tot_errors[n_cols];
  double sig_yields[n_cols];
  double sig_errors[n_cols];
  double data_yields[n_cols];

  // Number of times to sample from the fit covariance matrix
  unsigned samples = 500;

  for (unsigned i = 0; i < n_cols; ++i) {
    ch::CombineHarvester tmp_cmb =
        std::move(cmb.cp().era({col_info[i].era}).bin_id(col_info[i].cats_int));
    // tmp_cmb.cp().PrintAll();
    data_yields[i] = tmp_cmb.cp().GetObservedRate();
    sig_yields[i] = tmp_cmb.cp().process(signal_procs).GetRate();
    sig_errors[i] = postfit ?
        tmp_cmb.cp().process(signal_procs).GetUncertainty(fitresult, samples) :
        tmp_cmb.cp().process(signal_procs).GetUncertainty();
    tot_yields[i] = tmp_cmb.cp().process(total_bkg).GetRate();
    tot_errors[i] = postfit ?
        tmp_cmb.cp().process(total_bkg).GetUncertainty(fitresult, samples) :
        tmp_cmb.cp().process(total_bkg).GetUncertainty();
    for (unsigned j = 0; j < n_bkg; ++j) {
      bkg_yields[i][j] = tmp_cmb.cp().process(bkgs[j].procs).GetRate();
      bkg_errors[i][j] = postfit ?
          tmp_cmb.cp().process(bkgs[j].procs).GetUncertainty(fitresult, samples) :
          tmp_cmb.cp().process(bkgs[j].procs).GetUncertainty();
    }
    for (unsigned k = 0; k < n_sig; ++k) {
      signal_num[i][k] = sig_cmb.cp()
                             .era({col_info[i].era})
                             .bin_id(col_info[i].cats_int)
                             .process({signal_procs[k]})
                             .era({col_info[i].era})
                             .GetRate();
      signal_eff[i][k] = signal_num[i][k] / signal_den[i][k];
    }
  }

  cout << "\\begin{tabular}{l";
  for (unsigned i = 0; i < n_cols; ++i) cout << "r@{$ \\,\\,\\pm\\,\\, $}l";
  cout << "}\n\\hline\n";
  cout << boost::format("\\multicolumn{%i}{c}{%s} \\\\\n") %
              (n_cols * 2 + 1) % header;
  cout << "\\hline\n";
  for (unsigned i = 0; i < v_eras.size(); ++i) {
    std::string fmt = v_eras[i];
    boost::replace_all(fmt, "TeV", "~\\TeV");
    std::cout << boost::format("& \\multicolumn{%i}{c}{$\\sqrt{s}$ = %s} ") %
                     (columns.size() * 2) % fmt;
  }
  cout << "\\\\\n";
  cout << "Process";
  for (unsigned i = 0; i < n_cols; ++i)
    cout << " & \\multicolumn{2}{c}{" + col_info[i].label + "}";
  cout << "\\\\\n";
  cout << "\\hline\n";
  string fmt = "& %-10.0f & %-10.0f";
  string fmts = "& %-10.0f & %-10.1f";

  for (unsigned k = 0; k < bkgs.size(); ++k) {
    cout << boost::format("%-38s") % bkgs[k].label;
    for (unsigned i = 0; i < n_cols; ++i)
      cout << boost::format(bkg_errors[i][k] < 1. ? fmts : fmt) %
                  bkg_yields[i][k] % bkg_errors[i][k];
    cout << "\\\\\n";
  }
  cout << "\\hline\n";

  cout << boost::format("%-38s") % "Total Background";
  for (unsigned i = 0; i < n_cols; ++i)
    cout << boost::format(fmt) % tot_yields[i] % tot_errors[i];
  cout << "\\\\\n";

  cout << boost::format("%-38s") % "A+H+h\\,$\\rightarrow\\Pgt\\Pgt$";
  for (unsigned i = 0; i < n_cols; ++i)
    cout << boost::format(sig_errors[i] < 1. ? fmts : fmt) % sig_yields[i] %
                sig_errors[i];

  cout << "\\\\\n";

  cout << boost::format("%-38s") % "Data";
  for (unsigned i = 0; i < n_cols; ++i)
    cout << boost::format("& \\multicolumn{2}{c}{%-10.0f}") % data_yields[i];
  cout << "\\\\\n";
  cout << "\\hline\n";

  cout << boost::format(
              "\\multicolumn{%i}{l}{Efficiency $\\times$ acceptance}\\\\\n") %
              (n_cols*2 + 1);
  cout << "\\hline\n";
  cout << boost::format("%-38s") % "gluon-fusion Higgs (160~\\GeV)";
  for (unsigned i = 0; i < n_cols; ++i) {
    std::string fmte = (boost::format("%.2e") % signal_eff[i][0]).str();
    boost::replace_all(fmte, "e-0", "\\cdot 10^{-");
    fmte = " $" + fmte;
    fmte = fmte + "}$";
    cout << boost::format("& \\multicolumn{2}{c}{%s}") % fmte;
  }

  cout << "\\\\\n";

  cout << boost::format("%-38s") % "b-associated Higgs (160~\\GeV)";
  for (unsigned i = 0; i < n_cols; ++i) {
    std::string fmte = (boost::format("%.2e") % signal_eff[i][1]).str();
    boost::replace_all(fmte, "e-0", "\\cdot 10^{-");
    fmte = " $" + fmte;
    fmte = fmte + "}$";
    cout << boost::format("& \\multicolumn{2}{c}{%s}") % fmte;    }
  cout << "\\\\\n";
  cout << "\\hline\n";

  cout << "\\end{tabular}\n";

  return 0;
}
