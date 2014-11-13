#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Observation.h"
#include "CombineTools/interface/Process.h"
#include "CombineTools/interface/Utilities.h"
#include "CombineTools/interface/Systematics.h"

using namespace std;

int main() {
  // In this example we'll setup a simplified version of the Higgs to tau tau
  // datacards, while exploring the main features of the CombineHarvester tool.

  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // We will define two analysis categories (i.e. two distributions that we want
  // to fit simultaneously). In combine parlance, each is called a "bin". Each
  // bin must have a unique name. CombineHarvester also gives each bin an
  // integer value, called a "bin_id", that does not need to be unique. This can
  // be useful to label a "type-of-category" that might appear more than once.
  // For example, VBF event categories for both the 7TeV and 8TeV datasets might
  // have a common bin_id, but different names "vbf_7TeV" and "vbf_8TeV".
  //
  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  vector<pair<int, string>> cats = {
      {1, "muTau_1jet_medium"},
      {2, "muTau_vbf_loose"}
    };

  // Now we define the signal mass points we will build datacards for, but note
  // these are specified as strings, not floats.
  vector<string> masses = ch::MassesFromRange("110,115-140:5,145");

  // The next step is to add some new entries to the CombineHarvester instance.
  // First we will specifiy the observations (i.e. the actual data). The
  // AddObservations method takes a series of vectors as arguments. Each vector
  // specifies some property, such as the analysis name, the dataset era or the
  // bin information. Every possible combination of elements from these vectors
  // will be used to add a new Observation entry.
  //
  // The arguments are:
  // AddObservations(masses, analyses, eras, channels, categories)
  //
  // Below we specify one mass entry ("*"), which implies we only need one entry
  // that will cover all signal mass hypotheses. Then we specify the
  // higgs-tau-tau analysis ("htt"), the 8TeV dataset ("8TeV"), the mu+tau
  // analysis channel ("mt") and the categories we defined above. If the
  // analysis, era and channel properties aren't relevant for your analysis, you
  // can always leave them as a single emtpy string.
  cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {"mt"}, cats);

  // Next we add the background processes. The arguments are similar to the
  // AddObservations method. An extra argument is added after the channels for
  // the list of background processes, and a final boolean option specifies
  // whether these are signal or background processes.
  // Note that each process name here should correspond to the histogram name
  // in your input file.
  vector<string> bkg_procs = {"ZTT", "W", "QCD", "TT"};
  cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {"mt"}, bkg_procs, cats, false);

  // Similarly we add the signal processes. Here the list of masses hypotheses
  // is given instead of the single "*" entry.
  vector<string> sig_procs = {"ggH", "qqH"};
  cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {"mt"}, sig_procs, cats, true);

  // The next step is to add details of the systematic uncertainties. The
  // details of an uncertainty on a single process in a single bin is called a
  // Nuisance. Some of the code for this is in a nested namespace, so we'll make
  // some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;

  // First, let's just go ahead and add a luminosity uncertainty for the signal
  // samples:
  cb.cp().signals()
      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
      ({"7TeV"}, 1.022)
      ({"8TeV"}, 1.026));
  // We can break this line down into several parts. cb.cp() returns a shallow
  // copy of the CombineHarvester instance - i.e. the Observation and Process
  // entries are shared with the original object. However, removing entries from
  // this shallow copy leaves the entries in the original instance intact. The
  // next method, signals(), acts on this copy. This is one of several filter
  // methods. It removes any non-signal process from the internal entries. We do
  // this because we only want to create Nuisance entries for the signal
  // processes. Like all filter methods this returns a reference to itself. Then
  // we can apply the actual AddSyst method. The first argument is a pointer to
  // the CombineHarvester instance where the new Nuisance entries should be
  // created. In this case we just give it the pointer to our original instance
  // (remember we are calling the AddSyst method on a copy of this instance).
  // The next argument is the Nuisance name. Before the Nuisance entry for each
  // Process is created a number of string substitutions will be made, based on
  // the properties of the process in question. These are:
  //   $BIN       --> proc.bin()
  //   $PROCESS   --> proc.process()  (the process name)
  //   $MASS      --> proc.mass()
  //   $ERA       --> proc.era()
  //   $CHANNEL   --> proc.channel()
  //   $ANALYSIS  --> proc.analysis()
  // So in this example we will expect names like "lumi_8TeV". This substitution
  // provides a quick way of renaming Nuisances to be correlated/uncorrelated
  // between different channels/analyses/bins etc.
  // Next we specifiy the nuisance type, which must be either "lnN" or "shape".
  // The final argument is special map (SystMap) that contains the set of values
  // that should be added (though note for shape this needs to be 1.0 at the
  // moment). The SystMap is a templated class, which can take an arbitrary
  // number of template parameters. Each parameter specifies a Process property
  // that will be used as part of the key to map to the values. In this case we
  // will just use the process era as a key. We initialse a new map with ::init,
  // then provide a series entries. Each entry should consist of a series of
  // vectors, one for each key value, and end in the lnN value that should be
  // assigned. Processes matching any combination of key properties in this map
  // will be assigned the given value. In this map, we assign at process with
  // era "7TeV" a value of 1.022, and any "8TeV" process a value of 1.026. More
  // examples are given below:
  cb.cp().process({"ggH"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  cb.cp().process(JoinStr({sig_procs, {"ZTT", "TT"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {1},     {"ggH"},        1.04)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.10)
        ({"8TeV"}, {2},     {"qqH"},        1.04)
        ({"8TeV"}, {2},     {"TT"},         1.05));

  cb.cp().process(JoinStr({sig_procs, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));

  // Next we populate these Observation, Process and Nuisance entries with the
  // actual histograms (and also yields). The last two arguments are the
  // patterns The give the path the required nominal and systematic shape
  // templates in the given file. Here we must do this separately for signal and
  // background shapes which use a different naming convention.
  // NOTE: In this method only the following substitutions are supported:
  //   $CHANNEL    --> proc.bin()   (NB: different from above!!!)
  //   $PROCESS    --> proc.process()
  //   $MASS       --> proc.mass()
  //   $SYSTEMATIC --> nus.name()
  // Also note that data histogram must be named data_obs to be extracted
  // by this command.
  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "Imperial/htt_mt.inputs-sm-8TeV-hcg.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "Imperial/htt_mt.inputs-sm-8TeV-hcg.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);

  // The next step is optional. This will generate additional shape
  // uncertainties to account for limited template statistics, so-called
  // "bin-by-bin" uncertainties. The first argument is the bin error threshold
  // over which an uncertainty should be created, expressed as a percentage of
  // the bin content. The second argument controls the normalisation of the Up
  // and Down shapes that are created. If set to true, the normalisation is
  // fixed to nominal rate. If false, the normalisation is allowed to vary.
  // Finally a pointer to the CombineHarvester instance where the Nuisance
  // entries should be created is supplied.
  cb.cp().backgrounds().AddBinByBin(0.1, true, &cb);

  // Now we will iterate through the set of bins and masspoints and write
  // a txt datacard file for each. First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This GenerateSetFromObs method will fill a set by applying the supplied
  // function to each Observation entry. The function must be of the form:
  // string Function(Observation *obs)
  // Here we use mem_fn to quickly generate such a function from the
  // Observation::bin class method.

  // Uncomment this line to print all the entries
  // cb.PrintAll();

  // We create the output root file that will contain all the shapes.
  TFile output("htt_mt.input.root", "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
          b + "_" + m + ".txt", output);
    }
  }
}
