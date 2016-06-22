#ifndef CombineTools_HttSystematics_h
#define CombineTools_HttSystematics_h
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

namespace ch {

// Legacy SM analysis systematics
// Implemented in src/HttSystematics_SMLegacy.cc
void AddSystematics_et_mt(CombineHarvester& cb);
void AddSystematics_et_mt(CombineHarvester& cb);
void AddSystematics_em(CombineHarvester& cb);
void AddSystematics_ee_mm(CombineHarvester& cb);
void AddSystematics_tt(CombineHarvester& cb);

// Legacy MSSM analysis systematics
// Implemented in src/HttSystematics_MSSMLegacy.cc
void AddMSSMSystematics(CombineHarvester& cb, CombineHarvester src);
void AddMSSMSystematics(CombineHarvester& cb);

// Update MSSM analysis systematics
// Implemented in src/HttSystematics_MSSMUpdate.cc
void AddMSSMUpdateSystematics_et_mt(CombineHarvester& cb, CombineHarvester src);
void AddMSSMUpdateSystematics_et_mt(CombineHarvester& cb);
void AddMSSMUpdateSystematics_em(CombineHarvester& cb, CombineHarvester src);
void AddMSSMUpdateSystematics_em(CombineHarvester& cb);
void AddMSSMUpdateSystematics_mm(CombineHarvester& cb, CombineHarvester src);
void AddMSSMUpdateSystematics_mm(CombineHarvester& cb);
void AddMSSMUpdateSystematics_tt(CombineHarvester& cb, CombineHarvester src);
void AddMSSMUpdateSystematics_tt(CombineHarvester& cb);

// Hhh systematics
// Implemented in src/HhhSystematics.cc
void AddSystematics_hhh_et_mt(CombineHarvester& cb, CombineHarvester src);
void AddSystematics_hhh_et_mt(CombineHarvester& cb);
void AddSystematics_hhh_tt(CombineHarvester& cb, CombineHarvester  src);
void AddSystematics_hhh_tt(CombineHarvester& cb);
// AZh systematics
// Implemented in src/AZhSystematics.cc
void AddSystematics_AZh(CombineHarvester& cb, CombineHarvester src);
void AddSystematics_AZh(CombineHarvester& cb);
}

#endif
