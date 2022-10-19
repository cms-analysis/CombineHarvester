#include <vector>
#include <set>
#include <map>
#include "boost/python.hpp"
#include "boost/python/type_id.hpp"
#include "TPython.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombinePdfs/interface/CMSHistFuncFactory.h"

namespace bp = boost::python;

void BuildRooMorphingPy(bp::object & ws, ch::CombineHarvester& cb,
                      std::string const& bin, std::string const& process,
                      bp::object & mass_var, std::string norm_postfix,
                      bool allow_morph, bool verbose, bool force_template_limit, bp::object & file);

void BuildCMSHistFuncFactoryPy(bp::object &ws, ch::CombineHarvester& cb, bp::object & mass_var, std::string const& process);
