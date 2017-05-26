#ifndef MSSM2016_HttSystematics_MSSMRun2_h
#define MSSM2016_HttSystematics_MSSMRun2_h
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

namespace ch {
// Run2 MSSM analysis systematics
// Implemented in src/HttSystematics_MSSMRun2.cc
void AddMSSMRun2Systematics(CombineHarvester& cb, int control_region = 0, bool zmm_fit = false, bool ttbar_fit = false);
}

#endif
