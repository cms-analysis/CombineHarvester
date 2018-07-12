#ifndef SM2017_HttSystematics_SMRun2_h
#define SM2017_HttSystematics_SMRun2_h
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

namespace ch {
// Run2 SM analysis systematics
// Implemented in src/HttSystematics_SMRun2.cc
void AddSMRun2Systematics(CombineHarvester& cb, bool jetfakes, bool embedding);
}

#endif
