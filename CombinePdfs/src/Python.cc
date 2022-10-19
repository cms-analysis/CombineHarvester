#include "CombineHarvester/CombinePdfs/interface/Python.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombinePdfs/interface/CMSHistFuncFactory.h"
#include "boost/python.hpp"
#include "TFile.h"
namespace py = boost::python;


void BuildRooMorphingPy(bp::object & ws, ch::CombineHarvester& cb,
                      std::string const& bin, std::string const& process,
                      bp::object & mass_var, std::string norm_postfix,
                      bool allow_morph, bool verbose, bool force_template_limit, bp::object & file) {
  RooWorkspace *ws_ = (RooWorkspace*)(TPython::ObjectProxy_AsVoidPtr(ws.ptr()));
  RooAbsReal *mass_var_ = (RooAbsReal*)(TPython::ObjectProxy_AsVoidPtr(mass_var.ptr()));
  TFile *file_ = nullptr;
  if (!file.is_none()) {
    file_ = (TFile*)(TPython::ObjectProxy_AsVoidPtr(file.ptr()));
  }
  BuildRooMorphing(*ws_, cb, bin, process, *mass_var_, norm_postfix, allow_morph, verbose, force_template_limit, file_);
}


void BuildCMSHistFuncFactoryPy(bp::object &ws, ch::CombineHarvester& cb, bp::object &mass_var, std::string const& process){
  RooWorkspace *ws_ = (RooWorkspace*)(TPython::ObjectProxy_AsVoidPtr(ws.ptr()));
  RooAbsReal *mass_var_ = (RooAbsReal*)(TPython::ObjectProxy_AsVoidPtr(mass_var.ptr()));
  ch::CMSHistFuncFactory f;
  std::map<std::string, RooAbsReal*> morphVars = {{process, mass_var_}};
  f.SetHorizontalMorphingVariable(morphVars);
  f.Run(cb, *ws_);
}

BOOST_PYTHON_MODULE(libCombineHarvesterCombinePdfs)
{
  py::def("BuildRooMorphingX", BuildRooMorphingPy);
  py::def("BuildCMSHistFuncFactoryX", BuildCMSHistFuncFactoryPy);
}
