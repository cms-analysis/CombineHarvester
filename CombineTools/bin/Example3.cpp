#include <string>
#include <iostream>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"

using namespace std;

int main() {
  //! [part1]
  // Define four categories labelled A, B, C and D, and
  // set the observed yields in a map.
  ch::Categories cats = {
      {0, "A"},
      {1, "B"},
      {2, "C"},
      {3, "D"}
    };
  std::map<std::string, float> obs_rates = {
    {"A", 10.},
    {"B", 50.},
    {"C", 100.},
    {"D", 500.}
  };
  //! [part1]

  //! [part2]
  ch::CombineHarvester cb;
  cb.SetVerbosity(3);

  cb.AddObservations({"*"}, {""}, {"13TeV"}, {""},          cats);
  cb.AddProcesses(   {"*"}, {""}, {"13TeV"}, {""}, {"bkg"}, cats, false);

  cb.ForEachObs([&](ch::Observation *x) {
    x->set_rate(obs_rates[x->bin()]);
  });
  cb.ForEachProc([](ch::Process *x) {
    x->set_rate(1);
  });
  //! [part2]

  //! [part3]
  using ch::syst::SystMap;
  using ch::syst::SystMapFunc;
  using ch::syst::bin;

  // Add a traditional lnN systematic
  cb.cp().bin({"D"}).AddSyst(cb, "DummySys", "lnN", SystMap<>::init(1.0001));
  
  // Create a unqiue floating parameter in each bin
  cb.cp().bin({"B", "C", "D"}).AddSyst(cb, "scale_$BIN", "rateParam", SystMap<bin>::init
          ({"B"}, obs_rates["B"])
          ({"C"}, obs_rates["C"])
          ({"D"}, obs_rates["D"])
      );

  // Create a function that sets the yield in A as a function of B, C and D
  cb.cp().bin({"A"}).AddSyst(cb, "scale_$BIN", "rateParam", SystMapFunc<>::init
          ("(@0*@1/@2)", "scale_B,scale_C,scale_D")
      );
  //! [part3]

  //! [part4]
  cb.PrintAll();
  cb.WriteDatacard("example3.txt");
  //! [part4]
}





