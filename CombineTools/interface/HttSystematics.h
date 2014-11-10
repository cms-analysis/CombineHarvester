#ifndef CombineTools_HttSystematics_h
#define CombineTools_HttSystematics_h
#include "CombineTools/interface/CombineHarvester.h"

namespace ch {
void AddSystematics_et_mt(CombineHarvester& cb);
void AddSystematics_ee_mm(CombineHarvester& cb);
void AddSystematics_tt(CombineHarvester& cb);
void AddMSSMSystematics(CombineHarvester& cb);
}

#endif
