#ifndef CombineTools_HttSystematics_h
#define CombineTools_HttSystematics_h
#include "CombineTools/interface/CombineHarvester.h"

namespace ch {

// Legacy SM analysis systematics
// Implemented in src/HttSystematics_SMLegacy.cc
void AddSystematics_et_mt(CombineHarvester& cb);
void AddSystematics_em(CombineHarvester& cb);
void AddSystematics_ee_mm(CombineHarvester& cb);
void AddSystematics_tt(CombineHarvester& cb);

// Legacy MSSM analysis systematics
// Implemented in src/HttSystematics_MSSMLegacy.cc
void AddMSSMSystematics(CombineHarvester& cb);
}

#endif
