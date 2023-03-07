#include <map>
#include <regex>

#include "boost/program_options.hpp"
#include "boost/format.hpp"
#include "TSystem.h"
#include "TH2F.h"
#include "RooRealVar.h"
#include "TMath.h"
#include "TString.h"
#include "RooMsgService.h"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/ParseCombineWorkspace.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/Logging.h"

namespace po = boost::program_options;

using namespace std;

void ReverseBins(TH1F & h) {
  std::vector<float> contents(h.GetNbinsX());
  std::vector<float> errors(h.GetNbinsX());
  for (int i = 0; i < h.GetNbinsX(); ++i) {
    contents[i] = h.GetBinContent(i + 1);
    errors[i] = h.GetBinError(i + 1);
  }
  for (int i = 0; i < h.GetNbinsX(); ++i) {
    h.SetBinContent(h.GetNbinsX() - i, contents[i]);
    h.SetBinError(h.GetNbinsX() - i, errors[i]);
  }
  // return h;
}

void load_shapes_and_yields(
  ch::CombineHarvester& cmb, 
  map<string, TH1F>& shape_container, 
  const std::string& proc,
  vector<RooRealVar>* yield_container=nullptr, 
  const bool& skip_proc_errs=true,
  const bool& no_sampling=true,
  const int& samples=0,
  RooFitResult* res=nullptr,
  const bool& verbose=false){
  TString helper;
  if (skip_proc_errs) {
    shape_container[proc] =
        cmb.GetShape();
  } else {
    shape_container[proc] =
        no_sampling ? cmb.GetShapeWithUncertainty()
                   : cmb.GetShapeWithUncertainty(*res, samples);
  }
  // fill the yield container if there is one
  if(yield_container != nullptr){
    helper.Form("%s_%s", "yield" , proc.c_str());
    yield_container->push_back(RooRealVar(helper, helper, 
          cmb.GetRate()));
    yield_container->back().setError(no_sampling ? cmb.GetUncertainty()
                    : cmb.GetUncertainty(*res, samples));
  }
}

void do_complete_set(
  ch::CombineHarvester& cmb_bin,
  TFile& outfile,
  const std::string& output_prefix,
  map<string, TH1F>& shape_container,
  const std::map<std::string, std::string>& merged_procs,
  const std::set<std::string> skip_procs,
  ch::CombineHarvester& cmb_card,
  bool  save_yields=true,
  const std::string& datacard="",
  const bool& skip_proc_errs=true,
  const bool& factors=false,
  const bool& reverse_bins=false,
  const bool& no_sampling=true,
  const int& samples=0,
  RooFitResult* res=NULL,
  const bool& verbose=false
  ){
    TString helper;
  // ch::CombineHarvester cmb_bin = cmb.cp().bin({bin});
    // This next line is a temporary fix for models with parameteric RooFit pdfs
    // - we try and set the number of bins to evaluate the pdf to be the same as
    // the number of bins in data
    // cmb_bin.SetPdfBins(cmb_bin.GetObservedShape().GetNbinsX());

    // initialize container for yields if necessary
    std::vector<RooRealVar>* yield_container = nullptr;
    if(save_yields) yield_container = new std::vector<RooRealVar>();
    // Fill the data and process histograms
    shape_container["data_obs"] = cmb_bin.GetObservedShape();
    if(yield_container != nullptr){
      yield_container->push_back(RooRealVar("yield_data_obs", "yield_data_obs", cmb_bin.GetObservedRate()));
      yield_container->back().setError(TMath::Power(cmb_bin.GetObservedRate(), 0.5));
    }
    for (auto proc : cmb_bin.process_set()) {
      if(skip_procs.find(proc) == skip_procs.end()){
        std::cout << ">> Doing " << output_prefix.c_str() << "," << proc << std::endl;
        load_shapes_and_yields(cmb_bin.cp().process({proc}), shape_container, proc, yield_container, skip_proc_errs, no_sampling, samples, res, verbose);
      }
      else{
        std::cout << ">> Skipping processes " << proc << std::endl;
      }
    }
    for (auto iter: merged_procs){
      auto proc=iter.first;
      std::cout << ">> Doing " << output_prefix.c_str() << "," << proc << std::endl;
      auto proc_regex = iter.second;
      auto cmb_proc = cmb_bin.cp().process({proc_regex});
      if (cmb_proc.process_set().size() == 0){
        std::cout << ">> WARNING: found no processes matching " << proc << std::endl;
        continue;
      }
      load_shapes_and_yields(cmb_proc, shape_container, proc, yield_container, skip_proc_errs, no_sampling, samples, res, verbose);
    }

    // The fill total signal and total bkg hists
    std::cout << ">> Doing " << output_prefix.c_str() << "," << "TotalBkg" << std::endl;
    load_shapes_and_yields(cmb_bin.cp().backgrounds(), shape_container, "TotalBkg", yield_container, false, no_sampling, samples, res, verbose);

    // Print out the relative uncert. on the bkg
    if (factors && yield_container != nullptr) {
      cout << boost::format("%-25s %-32s\n") % "Bin" %
                  "Total relative bkg uncert.";
      cout << string(58, '-') << "\n";
      
      double rate = yield_container->back().getVal();
      double err = yield_container->back().getError();
      cout << boost::format("%-25s %-10.5f") % output_prefix.c_str() %
                  (rate > 0. ? (err / rate) : 0.) << std::endl;
    }
    
    std::cout << ">> Doing " << output_prefix.c_str() << "," << "TotalSig" << std::endl;
    load_shapes_and_yields(cmb_bin.cp().signals(), shape_container, "TotalSig", yield_container, false, no_sampling, samples, res, verbose);
    
    std::cout << ">> Doing " << output_prefix.c_str() << "," << "TotalProcs" << std::endl;
    load_shapes_and_yields(cmb_bin, shape_container, "TotalProcs", yield_container, false, no_sampling, samples, res, verbose);


    if (datacard != "") {
      TH1F ref = cmb_card.GetObservedShape();
      for (auto & it : shape_container) {
        it.second = ch::RestoreBinning(it.second, ref);
      }
    }

    if(reverse_bins){
      for (auto it = shape_container.begin(); it != shape_container.end(); ++it) {
        ReverseBins(it->second);
      }
    }
    // Can write these straight into the output file
    outfile.cd();
    for (auto& iter : shape_container) {
      ch::WriteToTFile(&(iter.second), &outfile, output_prefix + "/" + iter.first);
    }
    if(yield_container != nullptr){
      for (auto& yield: *yield_container){
        helper.Form("%s/%s", output_prefix.c_str() , yield.GetName());
        ch::WriteToTFile(&(yield), &outfile, helper.Data());
      }
    }
}


int main(int argc, char* argv[]) {
  // Need this to read combine workspaces
  gSystem->Load("libHiggsAnalysisCombinedLimit");

  string datacard   = "";
  string workspace  = "";
  string fitresult  = "";
  string mass       = "";
  bool postfit      = false;
  bool sampling     = false;
  bool no_sampling  = false;
  string output     = "";
  bool factors      = false;
  unsigned samples  = 500;
  std::string freeze_arg = "";
  bool covariance   = false;
  string data       = "data_obs";
  bool skip_prefit  = false;
  bool skip_proc_errs = false;
  bool total_shapes = false;
  bool save_yields = false;
  bool verbose = false;
  std::vector<std::string> reverse_bins_;
  std::vector<std::string> bins_;
  std::set<std::string> skip_procs;
  std::vector<std::string> skip_procs_;
  std::vector<std::string> input_merge_procs_;
  std::map<std::string, std::string> merged_procs;


  po::options_description help_config("Help");
  help_config.add_options()
    ("help,h", "produce help message");

  po::options_description config("Configuration");
  config.add_options()
    ("workspace,w",
      po::value<string>(&workspace)->required(),
      "The input workspace-containing file [REQUIRED]")
    ("dataset",
      po::value<string>(&data)->default_value(data),
      "The input dataset name")
    ("datacard,d",
      po::value<string>(&datacard),
      "The input datacard, only used for rebinning")
    ("output,o ",
      po::value<string>(&output)->required(),
      "Name of the output root file to create [REQUIRED]")
    ("fitresult,f",
      po::value<string>(&fitresult)->default_value(fitresult),
      "Path to a RooFitResult, only needed for postfit")
    ("mass,m",
      po::value<string>(&mass)->default_value(""),
      "Signal mass point of the input datacard")
    ("postfit",
      po::value<bool>(&postfit)
      ->default_value(postfit)->implicit_value(true),
      "Create post-fit histograms in addition to pre-fit")
    ("sampling",
      po::value<bool>(&sampling)->default_value(sampling)->implicit_value(true),
      "Use the cov. matrix sampling method for the post-fit uncertainty (deprecated, this is the default)")
    ("no-sampling",
      po::value<bool>(&no_sampling)->default_value(no_sampling)->implicit_value(true),
      "Do not use the cov. matrix sampling method for the post-fit uncertainty")
    ("save-yields,y",
      po::value<bool>(&save_yields)->default_value(save_yields)->implicit_value(true),
      "Save process yields in addition to the shapes. This will generate RooRealVar objects with the yield as value and the (sampled) uncertainties as error")
    ("samples",
      po::value<unsigned>(&samples)->default_value(samples),
      "Number of samples to make in each evaluate call")
    ("print",
      po::value<bool>(&factors)->default_value(factors)->implicit_value(true),
      "Print tables of background shifts and relative uncertainties")
    ("freeze",
      po::value<string>(&freeze_arg)->default_value(freeze_arg),
      "Format PARAM1,PARAM2=X,PARAM3=Y where the values X and Y are optional")
    ("covariance",
      po::value<bool>(&covariance)->default_value(covariance)->implicit_value(true),
      "Save the covariance and correlation matrices of the process yields")
    ("skip-prefit",
      po::value<bool>(&skip_prefit)->default_value(skip_prefit)->implicit_value(true),
      "Skip the pre-fit evaluation")
    ("skip-proc-errs",
      po::value<bool>(&skip_proc_errs)->default_value(skip_proc_errs)->implicit_value(true),
      "Skip evaluation of errors on individual processes")
    ("verbose,v",
      po::value<bool>(&verbose)->default_value(verbose)->implicit_value(true),
      "Genererate additional output if uncertainties in a given bin are large")
    ("total-shapes",
      po::value<bool>(&total_shapes)->default_value(total_shapes)->implicit_value(true),
      "Save signal- and background shapes added for all channels/categories")
    ("reverse-bins", po::value<vector<string>>(&reverse_bins_)->multitoken(), "List of bins to reverse the order for")
    ("bins", po::value<vector<string>>(&bins_)->multitoken(), "List of bins to produce shapes for (default: all bins")
    ("merge-procs,p", po::value<vector<string>>(&input_merge_procs_)->multitoken(), 
      "Merge these processes. Regex expression allowed. Format: NEWPROCESSNAME='expression'")
    ("skip-procs,s", po::value<vector<string>>(&skip_procs_)->multitoken(), 
      "Skip these processes. Regex expression allowed. Format: 'expression'. Can be called multiple times");

  // if (!no_sampling && !postfit) {
  //   throw logic_error(
  //       "Can't sample the fit covariance matrix for pre-fit!");
  // }

  po::variables_map vm;

  // First check if the user has set the "--help" or "-h" option, and if so
  // just print the usage information and quit
  po::store(po::command_line_parser(argc, argv)
    .options(help_config).allow_unregistered().run(), vm);
  po::notify(vm);
  if (vm.count("help")) {
    cout << config << "\nExample usage:\n";
    cout << "PostFitShapesFromWorkspace.root -d htt_mt_125.txt -w htt_mt_125.root -o htt_mt_125_shapes.root -m 125 "
            "-f mlfit.root:fit_s --postfit --print\n";
    return 1;
  }

  // Parse the main config options
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  if (sampling) {
    std::cout<<"WARNING: the default behaviour of PostFitShapesFromWorkspace is to use the covariance matrix sampling method for the post-fit uncertainty. The option --sampling is deprecated and will be removed in future versions of CombineHarvester"<<std::endl;
  }

  TFile infile(workspace.c_str());

  RooWorkspace *ws = dynamic_cast<RooWorkspace*>(gDirectory->Get("w"));

  if (!ws) {
    throw std::runtime_error(
        FNERROR("Could not locate workspace in input file"));
  }

  // Create CH instance and parse the workspace
  ch::CombineHarvester cmb;
  cmb.SetFlag("workspaces-use-clone", true);
  cmb.SetFlag("filters-use-regex", true);
  ch::ParseCombineWorkspace(cmb, *ws, "ModelConfig", data, false);
  RooMsgService::instance().setSilentMode(true);
  // Only evaluate in case parameters to freeze are provided
  if(! freeze_arg.empty())
  {
    vector<string> freeze_vec;
    boost::split(freeze_vec, freeze_arg, boost::is_any_of(","));
    vector<string> parameters;
    for (auto& par : cmb.GetParameters())
    {
      parameters.push_back(par.name());
    }
    for (auto const& item : freeze_vec) {
      vector<string> parts;
      boost::split(parts, item, boost::is_any_of("="));
      auto current_expr = parts[0];

      // check for regex syntax: rgx{regex}                                                                                                                                     
      if (boost::starts_with(current_expr, "rgx{") && boost::ends_with(current_expr, "}")) {
        bool matched = false;
        
        std::string reg_esp = current_expr.substr(4, current_expr.size()-5);
        std::cout<<"interpreting "<<reg_esp<<" as regex "<<std::endl;
        std::regex rgx( reg_esp, std::regex::ECMAScript);

        
        for (auto& parname: parameters) {
          std::smatch match;
          if (std::regex_match(parname, match, rgx)){
            ch::Parameter *par = cmb.GetParameter(parname.c_str());
            std::cout << "freezing parameter '" << parname.c_str() << "'" << std::endl;
            matched = true;
            if (parts.size() == 2) {
              par->set_val(boost::lexical_cast<double>(parts[1]));
            }
            par->set_frozen(true);
          }
        }
        // if not match is found, throw runtime error
        if(!matched){ 
          throw std::runtime_error(
          FNERROR("Requested variable to freeze does not exist in workspace"));
        }
      } else {
        ch::Parameter *par = cmb.GetParameter(current_expr);
        if (par) {
          std::cout << "freezing parameter '" << par->name() << "'" << std::endl;
          if (parts.size() == 2) {
            par->set_val(boost::lexical_cast<double>(parts[1]));
          }
          par->set_frozen(true);
        }
        else throw std::runtime_error(
            FNERROR("Requested variable to freeze does not exist in workspace"));
      }
    }
  }
  // cmb.GetParameter("r")->set_frozen(true);

  // parse processes that are to be merged
  for (auto& in: input_merge_procs_){
    vector<string> parts;
    boost::split(parts, in, boost::is_any_of("="));
    merged_procs[parts[0]] = parts[1];
  }

  ch::CombineHarvester cmb_card;
  cmb_card.SetFlag("workspaces-use-clone",true);
  if (datacard != "") {
    cmb_card.ParseDatacard(datacard, "", "", "", 0, mass);
  }

  // Drop any process that has no hist/data/pdf
  cmb.FilterProcs([&](ch::Process * proc) {
    bool no_shape = !proc->shape() && !proc->data() && !proc->pdf();
    if (no_shape) {
      cout << "Filtering process with no shape:\n";
      cout << ch::Process::PrintHeader << *proc << "\n";
    }
    return no_shape;
  });
  vector<string> bins;
  if (bins_.size() == 0)
  {
    auto bin_set = cmb.cp().bin_set();
    std::copy(bin_set.begin(), bin_set.end(), std::back_inserter(bins));
  }
  else{
    bins = bins_;
  }

  // parse processes
  std::set<std::string> process_set;
  for(auto& expr: skip_procs_){
    process_set = cmb.cp().process({expr}).process_set();
    skip_procs.insert(process_set.begin(), process_set.end());
  }

  TFile outfile(output.c_str(), "RECREATE");
  TH1::AddDirectory(false);

  // We can always do the prefit version,
  // Loop through the bins writing the shapes to the output file
  map<string, map<string, TH1F>> pre_shapes;
  TString helper;
  if (!skip_prefit) {
    if(total_shapes){
      pre_shapes["total"] = map<string, TH1F>();
      do_complete_set(cmb, outfile, "total_prefit", pre_shapes["total"], merged_procs, skip_procs, cmb_card, save_yields, datacard, skip_proc_errs, factors);
    }
    for (auto bin : bins) {
      pre_shapes[bin] = map<string, TH1F>();
      do_complete_set(
        cmb.cp().bin({bin}), 
        outfile, 
        bin+"_prefit", 
        pre_shapes[bin], 
        merged_procs,
        skip_procs,
        cmb_card.cp().bin({bin}),
        save_yields,
        datacard, 
        skip_proc_errs,
        factors, 
        std::find(reverse_bins_.begin(), reverse_bins_.end(), bin) != reverse_bins_.end());
    }
  }


  // Now we can do the same again but for the post-fit model
  if (postfit) {
    // Get the fit result and update the parameters to the post-fit model
    RooFitResult res = ch::OpenFromTFile<RooFitResult>(fitresult);
    cmb.UpdateParameters(res);

    // Calculate the post-fit fractional background uncertainty in each bin

    map<string, map<string, TH1F>> post_shapes;
    map<string, TH2F> post_yield_cov;
    map<string, TH2F> post_yield_cor;

    map<string, TH1F> post_shapes_tot;
    


    if(total_shapes){
      post_shapes["total"] = map<string, TH1F>();
      do_complete_set(
        cmb,
        outfile, 
        "total_postfit", 
        post_shapes["total"], 
        merged_procs,
        skip_procs,
        cmb_card, 
        save_yields, 
        datacard, 
        skip_proc_errs, 
        factors,
        false,
        no_sampling,
        samples,
        &res, 
        verbose);
    }


    for (auto bin : bins) {
      post_shapes[bin] = map<string, TH1F>();
      auto cmb_bin = cmb.cp().bin({bin});
      do_complete_set(
        cmb_bin,
        outfile, 
        bin+"_postfit", 
        post_shapes[bin], 
        merged_procs,
        skip_procs,
        cmb_card.cp().bin({bin}), 
        save_yields,
        datacard, 
        skip_proc_errs, 
        factors,
        std::find(reverse_bins_.begin(), reverse_bins_.end(), bin) != reverse_bins_.end(),
        no_sampling,
        samples,
        &res, 
        verbose);
      if (!no_sampling && covariance) {
        post_yield_cov[bin] = cmb_bin.GetRateCovariance(res, samples);
        post_yield_cor[bin] = cmb_bin.GetRateCorrelation(res, samples);
      }

      outfile.cd();

      for (auto & iter : post_yield_cov) {
        ch::WriteToTFile(&(iter.second), &outfile,
                         iter.first+"_cov");
      }
      for (auto & iter : post_yield_cor) {
        ch::WriteToTFile(&(iter.second), &outfile,
                         iter.first+"_cor");
      }

    }

    // As we calculate the post-fit yields can also print out the post/pre scale
    // factors
    if (factors && postfit) {
      cout << boost::format("\n%-25s %-20s %-10s\n") % "Bin" % "Process" %
                  "Scale factor";
      cout << string(58, '-') << "\n";
      for (auto bin : bins) {
        ch::CombineHarvester cmb_bin = cmb.cp().bin({bin});

        for (auto proc : cmb_bin.process_set()) {
          // Print out the post/pre scale factors
          TH1 const& pre = pre_shapes[bin][proc];
          TH1 const& post = post_shapes[bin][proc];
          cout << boost::format("%-25s %-20s %-10.5f\n") % bin % proc %
                      (pre.Integral() > 0. ? (post.Integral() / pre.Integral())
                                           : 1.0);
        }
      }
    }
  }
  // And we're done!
  outfile.Close();
  return 0;
}

