#include <string>
#include <iostream>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

using namespace std;

int main() {

  //! [part1]
  // Use the CMSSW_BASE environment variable to get the full path to the auxiliaries folder
  string in_dir = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/datacards/sm/htt_mt/";

  // Create a new CombineHarvester instance
  ch::CombineHarvester cmb1;

  // Call the `ParseDatacard` method specifying the path to the text file and the additional
  // metadata we want to associate with it
  cmb1.ParseDatacard(in_dir + "htt_mt_6_8TeV-125.txt", "htt", "8TeV", "mt", 6, "125");

  // Print the Observation, Process and Systematic entries to the screen
  cmb1.PrintObs().PrintProcs().PrintSysts();
  //! [part1]

  //! [part2]
  ch::CombineHarvester cmb2;
  // Parse a set of datacards into one CombineHarvester instance
  for (string bin_id : {"1", "2", "3", "4", "5", "6", "7"}) {
    cmb2.ParseDatacard(in_dir + "htt_mt_" + bin_id + "_8TeV-125.txt",
                       "$ANALYSIS_$CHANNEL_$BINID_$ERA-$MASS.txt");
  }

  //! [part2]
  //! [part3a]
  // Filter out all objects that do not have bin_id <= 4
  cmb2.FilterAll([](ch::Object const* obj) {
    return obj->bin_id() <= 4;
  });
  //! [part3a]

  //! [part3b]
  // Another way to achieve the same effect
  cmb2.bin_id({5, 6, 7});

  // Filter out all objects that have process name "QCD"
  cmb2.process({"QCD"}, false);
  //! [part3b]

  //! [part4]
  // GetObservedRate() will sum the event yields of all remaining Observation
  // objects
  cout << "Total observed rate:  " << cmb2.GetObservedRate() << "\n";

  // We can get the yield for a single bin by first making a shallow copy of the
  // current instance with the cp() method, then filtering this copy to leave
  // only the bin we're interested in, before finally calling GetObservedRate()
  cout << "Single category rate: "
       << cmb2.cp().bin({"muTau_vbf_loose"}).GetObservedRate() << "\n";

  // It is also possible to generate sets of object properties. Here we print
  // out the expected yield for each process in each bin
  for (auto bin : cmb2.bin_set()) {
    for (auto proc : cmb2.cp().bin({bin}).process_set()) {
      cout << bin << "," << proc << ": "
                        << cmb2.cp().bin({bin}).process({proc}).GetRate()
                        << "\n";
    }
  }
  //! [part4]

}
