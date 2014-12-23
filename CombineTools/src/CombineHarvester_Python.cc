#include "CombineTools/interface/CombineHarvester_Python.h"
#include "CombineTools/interface/CombineHarvester.h"
#include "boost/python.hpp"
#include "TFile.h"
#include "TH1F.h"
#include "RooFitResult.h"
namespace py = boost::python;
using ch::CombineHarvester;

// To resolve overloaded methods we first define some pointers
int (CombineHarvester::*Overload1_ParseDatacard)(
    std::string const&, std::string const&, std::string const&,
    std::string const&, int,
    std::string const&) = &CombineHarvester::ParseDatacard;

int (CombineHarvester::*Overload2_ParseDatacard)(
    std::string const&, std::string) = &CombineHarvester::ParseDatacard;

void (CombineHarvester::*Overload1_WriteDatacard)(
    std::string const&, std::string const&) = &CombineHarvester::WriteDatacard;

double (CombineHarvester::*Overload1_GetUncertainty)(
    void) = &CombineHarvester::GetUncertainty;

TH1F (CombineHarvester::*Overload1_GetShapeWithUncertainty)(
    void) = &CombineHarvester::GetShapeWithUncertainty;

TH1F (CombineHarvester::*Overload2_GetShapeWithUncertainty)(
    RooFitResult const&, unsigned) = &CombineHarvester::GetShapeWithUncertainty;

void (CombineHarvester::*Overload1_UpdateParameters)(
  RooFitResult const&) = &CombineHarvester::UpdateParameters;


// Use some macros for methods with default values
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_bin, bin, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_bin_id, bin_id, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_process, process, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_analysis, analysis, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_era, era, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_channel, channel, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_mass, mass, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_syst_name, syst_name, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_syst_type, syst_type, 1, 2)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(defaults_process_rgx, process_rgx, 1, 2)


BOOST_PYTHON_MODULE(libCHCombineTools)
{
  // Define converters from C++ --> python
  py::to_python_converter<std::set<std::string>,
                          convert_cpp_set_to_py_list<std::string>>();

  py::to_python_converter<std::set<int>,
                          convert_cpp_set_to_py_list<int>>();

  py::to_python_converter<TH1F,
                          convert_cpp_root_to_py_root<TH1F>>();

  // Define converters from python --> C++
  convert_py_seq_to_cpp_vector<std::string>();
  convert_py_seq_to_cpp_vector<int>();
  convert_py_root_to_cpp_root<TFile>();
  convert_py_root_to_cpp_root<TH1F>();
  convert_py_root_to_cpp_root<RooFitResult>();

  py::class_<CombineHarvester>("CombineHarvester")
      // Constructors, destructors and copying
      .def("cp", &CombineHarvester::cp)
      // Logging and printing
      .def("PrintAll", &CombineHarvester::PrintAll,
          py::return_value_policy<py::reference_existing_object>())
      .def("SetVerbosity", &CombineHarvester::SetVerbosity)
      // Datacards
      .def("ParseDatacard", Overload1_ParseDatacard)
      .def("ParseDatacard", Overload2_ParseDatacard)
      .def("WriteDatacard", Overload1_WriteDatacard)
      // Filters
      .def("bin", &CombineHarvester::bin,
          defaults_bin()[py::return_internal_reference<>()])
      .def("bin_id", &CombineHarvester::bin_id,
          defaults_bin_id()[py::return_internal_reference<>()])
      .def("process", &CombineHarvester::process,
          defaults_process()[py::return_internal_reference<>()])
      .def("analysis", &CombineHarvester::analysis,
          defaults_analysis()[py::return_internal_reference<>()])
      .def("era", &CombineHarvester::era,
          defaults_era()[py::return_internal_reference<>()])
      .def("channel", &CombineHarvester::channel,
          defaults_channel()[py::return_internal_reference<>()])
      .def("mass", &CombineHarvester::mass,
          defaults_mass()[py::return_internal_reference<>()])
      .def("syst_name", &CombineHarvester::syst_name,
          defaults_syst_name()[py::return_internal_reference<>()])
      .def("syst_type", &CombineHarvester::syst_type,
          defaults_syst_type()[py::return_internal_reference<>()])
      .def("process_rgx", &CombineHarvester::process_rgx,
          defaults_process_rgx()[py::return_internal_reference<>()])
      .def("signals", &CombineHarvester::signals,
          py::return_internal_reference<>())
      .def("backgrounds", &CombineHarvester::backgrounds,
          py::return_internal_reference<>())
      .def("histograms", &CombineHarvester::histograms,
          py::return_internal_reference<>())
      .def("pdfs", &CombineHarvester::pdfs,
          py::return_internal_reference<>())
      .def("data", &CombineHarvester::data,
          py::return_internal_reference<>())
      // Set producers
      .def("bin_set", &CombineHarvester::bin_set)
      .def("bin_id_set", &CombineHarvester::bin_id_set)
      .def("process_set", &CombineHarvester::process_set)
      .def("analysis_set", &CombineHarvester::analysis_set)
      .def("era_set", &CombineHarvester::era_set)
      .def("channel_set", &CombineHarvester::channel_set)
      .def("mass_set", &CombineHarvester::mass_set)
      .def("syst_name_set", &CombineHarvester::syst_name_set)
      .def("syst_type_set", &CombineHarvester::syst_type_set)
      // Modification
      .def("UpdateParameters", Overload1_UpdateParameters)
      // Evaluation
      .def("GetRate", &CombineHarvester::GetRate)
      .def("GetObservedRate", &CombineHarvester::GetObservedRate)
      .def("GetUncertainty", Overload1_GetUncertainty)
      .def("GetShape", &CombineHarvester::GetShape)
      .def("GetShapeWithUncertainty", Overload1_GetShapeWithUncertainty)
      .def("GetShapeWithUncertainty", Overload2_GetShapeWithUncertainty)
      .def("GetObservedShape", &CombineHarvester::GetObservedShape)
      // Creation
  ;
}