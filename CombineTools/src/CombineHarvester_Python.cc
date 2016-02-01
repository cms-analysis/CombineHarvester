#include "CombineHarvester/CombineTools/interface/CombineHarvester_Python.h"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombineTools/interface/CopyTools.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/ParseCombineWorkspace.h"
#include "boost/python.hpp"
#include "TFile.h"
#include "TH1F.h"
#include "TGraph.h"
#include "RooFitResult.h"
namespace py = boost::python;
using ch::CombineHarvester;
using ch::Object;
using ch::Observation;
using ch::Process;
using ch::Systematic;
using ch::CardWriter;
using ch::BinByBinFactory;
using ch::AutoRebin;

void FilterAllPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Object *obj) -> bool {
      return boost::python::extract<bool>(func(boost::ref(*obj)));
  };
  cb.FilterAll(lambda);
}

void FilterObsPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Observation *obs) -> bool {
      return boost::python::extract<bool>(func(boost::ref(*obs)));
  };
  cb.FilterObs(lambda);
}

void FilterProcsPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Process *proc) -> bool {
      return boost::python::extract<bool>(func(boost::ref(*proc)));
  };
  cb.FilterProcs(lambda);
}

void FilterSystsPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Systematic *sys) -> bool {
      return boost::python::extract<bool>(func(boost::ref(*sys)));
  };
  cb.FilterSysts(lambda);
}

void ForEachObsPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Observation *obs) {
      func(boost::ref(*obs));
  };
  cb.ForEachObs(lambda);
}

void ForEachProcPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Process *proc) {
      func(boost::ref(*proc));
  };
  cb.ForEachProc(lambda);
}

void ForEachSystPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Systematic *sys) {
      func(boost::ref(*sys));
  };
  cb.ForEachSyst(lambda);
}

void ForEachObjPy(ch::CombineHarvester & cb, boost::python::object func) {
      auto lambda = [func](ch::Object *obj) {
      func(boost::ref(*obj));
  };
  cb.ForEachObj(lambda);
}

void CloneObsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                boost::python::object func) {
  auto lambda = [func](ch::Observation *obs) {
    func(boost::ref(*obs));
  };
  ch::CloneObs(src, dest, lambda);
}

void CloneProcsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                  boost::python::object func) {
  auto lambda = [func](ch::Process *proc) {
    func(boost::ref(*proc));
  };
  ch::CloneProcs(src, dest, lambda);
}

void CloneSystsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                boost::python::object func) {
  auto lambda = [func](ch::Systematic *syst) {
    func(boost::ref(*syst));
  };
  ch::CloneSysts(src, dest, lambda);
}

void CloneProcsAndSystsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                        boost::python::object func) {
  auto lambda = [func](ch::Object *obj) {
    func(boost::ref(*obj));
  };
  ch::CloneProcsAndSysts(src, dest, lambda);
}

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

double (CombineHarvester::*Overload2_GetUncertainty)(
    RooFitResult const&, unsigned) = &CombineHarvester::GetUncertainty;

TH1F (CombineHarvester::*Overload1_GetShapeWithUncertainty)(
    void) = &CombineHarvester::GetShapeWithUncertainty;

TH1F (CombineHarvester::*Overload2_GetShapeWithUncertainty)(
    RooFitResult const&, unsigned) = &CombineHarvester::GetShapeWithUncertainty;

void (CombineHarvester::*Overload1_UpdateParameters)(
  RooFitResult const&) = &CombineHarvester::UpdateParameters;

void (CombineHarvester::*Overload_AddBinByBin)(
    double, bool, CombineHarvester &) = &CombineHarvester::AddBinByBin;

void (Observation::*Overload_Obs_set_shape)(
    TH1 const& ,bool) = &Observation::set_shape;

void (Process::*Overload_Proc_set_shape)(
    TH1 const&, bool) = &Process::set_shape;

void (Systematic::*Overload_Syst_set_shapes)(
    TH1 const&, TH1 const&, TH1 const&) = &Systematic::set_shapes;

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

BOOST_PYTHON_FUNCTION_OVERLOADS(defaults_MassesFromRange, ch::MassesFromRange, 1, 2)
BOOST_PYTHON_FUNCTION_OVERLOADS(defaults_ValsFromRange, ch::ValsFromRange, 1, 2)
BOOST_PYTHON_FUNCTION_OVERLOADS(defaults_SetStandardBinNames, ch::SetStandardBinNames, 1, 2)

BOOST_PYTHON_MODULE(libCombineHarvesterCombineTools)
{
  // Define converters from C++ --> python
  py::to_python_converter<std::set<std::string>,
                          convert_cpp_set_to_py_list<std::string>>();

  py::to_python_converter<std::vector<std::string>,
                          convert_cpp_vector_to_py_list<std::string>>();

  py::to_python_converter<std::set<int>,
                          convert_cpp_set_to_py_list<int>>();

  py::to_python_converter<std::map<std::string, CombineHarvester>,
                          convert_cpp_map_to_py_dict<std::string, CombineHarvester>>();

  py::to_python_converter<TH1F,
                          convert_cpp_root_to_py_root<TH1F>>();

  py::to_python_converter<TGraph,
                          convert_cpp_root_to_py_root<TGraph>>();

  py::to_python_converter<RooWorkspace,
                          convert_cpp_root_to_py_root<RooWorkspace>>();

  // Define converters from python --> C++
  convert_py_seq_to_cpp_vector<std::string>();
  convert_py_tup_to_cpp_pair<int, std::string>();
  convert_py_seq_to_cpp_vector<std::pair<int, std::string>>();
  convert_py_seq_to_cpp_vector<int>();
  convert_py_seq_to_cpp_vector<double>();
  convert_py_root_to_cpp_root<TFile>();
  convert_py_root_to_cpp_root<TH1F>();
  convert_py_root_to_cpp_root<TH1>();
  convert_py_root_to_cpp_root<TGraph>();
  convert_py_root_to_cpp_root<RooFitResult>();
  convert_py_root_to_cpp_root<RooWorkspace>();

  py::class_<CombineHarvester>("CombineHarvester")
      // Constructors, destructors and copying
      .def("cp", &CombineHarvester::cp)
      .def("deep", &CombineHarvester::deep)
      .def("SetFlag", &CombineHarvester::SetFlag)
      .def("GetFlag", &CombineHarvester::GetFlag)
      // Logging and printing
      .def("PrintAll", &CombineHarvester::PrintAll,
           py::return_internal_reference<>())
      .def("PrintObs", &CombineHarvester::PrintObs,
           py::return_internal_reference<>())
      .def("PrintProcs", &CombineHarvester::PrintProcs,
           py::return_internal_reference<>())
      .def("PrintSysts", &CombineHarvester::PrintSysts,
           py::return_internal_reference<>())
      .def("PrintParams", &CombineHarvester::PrintParams,
           py::return_internal_reference<>())
      .def("SetVerbosity", &CombineHarvester::SetVerbosity)
      .def("Verbosity", &CombineHarvester::Verbosity)
      // Datacards
      .def("__ParseDatacard__", Overload1_ParseDatacard)
      .def("QuickParseDatacard", Overload2_ParseDatacard)
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
      .def("FilterAll", FilterAllPy,
          py::return_internal_reference<>())
      .def("FilterObs", FilterObsPy,
          py::return_internal_reference<>())
      .def("FilterProcs", FilterProcsPy,
          py::return_internal_reference<>())
      .def("FilterSysts", FilterSystsPy,
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
      .def("RenameParameter", &CombineHarvester::RenameParameter)
      .def("ForEachObj", ForEachObjPy)
      .def("ForEachObs", ForEachObsPy)
      .def("ForEachProc", ForEachProcPy)
      .def("ForEachSyst", ForEachSystPy)
      .def("VariableRebin", &CombineHarvester::VariableRebin)
      .def("SetPdfBins", &CombineHarvester::SetPdfBins)
      // Evaluation
      .def("GetRate", &CombineHarvester::GetRate)
      .def("GetObservedRate", &CombineHarvester::GetObservedRate)
      .def("GetUncertainty", Overload1_GetUncertainty)
      .def("GetUncertainty", Overload2_GetUncertainty)
      .def("GetShape", &CombineHarvester::GetShape)
      .def("GetShapeWithUncertainty", Overload1_GetShapeWithUncertainty)
      .def("GetShapeWithUncertainty", Overload2_GetShapeWithUncertainty)
      .def("GetObservedShape", &CombineHarvester::GetObservedShape)
      // Creation
      .def("__AddObservations__", &CombineHarvester::AddObservations)
      .def("__AddProcesses__", &CombineHarvester::AddProcesses)
      .def("AddSystFromProc", &CombineHarvester::AddSystFromProc)
      .def("ExtractShapes", &CombineHarvester::ExtractShapes)
      .def("AddBinByBin", Overload_AddBinByBin)
      .def("MergeBinErrors",  &CombineHarvester::MergeBinErrors)
      .def("InsertObservation", &CombineHarvester::InsertObservation)
      .def("InsertProcess", &CombineHarvester::InsertProcess)
      .def("InsertSystematic", &CombineHarvester::InsertSystematic)
      ;

    py::class_<Object>("Object")
      .def("set_bin", &Object::set_bin)
      .def("bin", &Object::bin,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_process", &Object::set_process)
      .def("process",&Object::process,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_analysis", &Object::set_analysis)
      .def("analysis", &Object::analysis,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_era", &Object::set_era)
      .def("era", &Object::era,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_channel", &Object::set_channel)
      .def("channel", &Object::channel,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_bin_id", &Object::set_bin_id)
      .def("bin_id", &Object::bin_id)
      .def("set_mass", &Object::set_mass)
      .def("mass", &Object::mass,
          py::return_value_policy<py::copy_const_reference>())
    ;

    py::class_<Observation, py::bases<Object>>("Observation")
      .def("set_rate", &Observation::set_rate)
      .def("rate", &Observation::rate)
      .def("set_shape", Overload_Obs_set_shape)
      .def("ShapeAsTH1F", &Observation::ShapeAsTH1F)
      .def(py::self_ns::str(py::self_ns::self))
    ;

    py::class_<Process, py::bases<Object>>("Process")
      .def("set_rate", &Process::set_rate)
      .def("rate", &Process::rate)
      .def("no_norm_rate", &Process::no_norm_rate)
      .def("set_shape", Overload_Proc_set_shape)
      .def("set_signal", &Process::set_signal)
      .def("signal", &Process::signal)
      .def("ShapeAsTH1F", &Process::ShapeAsTH1F)
      .def(py::self_ns::str(py::self_ns::self))
    ;

    py::class_<Systematic, py::bases<Object>>("Systematic")
      .def("set_signal", &Systematic::set_signal)
      .def("signal", &Systematic::signal)
      .def("set_name", &Systematic::set_name)
      .def("name", &Systematic::name,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_type", &Systematic::set_type)
      .def("type", &Systematic::type,
          py::return_value_policy<py::copy_const_reference>())
      .def("set_value_u", &Systematic::set_value_u)
      .def("value_u", &Systematic::value_u)
      .def("set_value_d", &Systematic::set_value_d)
      .def("value_d", &Systematic::value_d)
      .def("set_scale", &Systematic::set_scale)
      .def("scale", &Systematic::scale)
      .def("set_asymm", &Systematic::set_asymm)
      .def("asymm", &Systematic::asymm)
      .def("set_shapes", Overload_Syst_set_shapes)
      .def(py::self_ns::str(py::self_ns::self))
    ;

    py::class_<CardWriter>("CardWriter", py::init<std::string, std::string>())
      .def("WriteCards", &CardWriter::WriteCards)
      .def("SetVerbosity", &CardWriter::SetVerbosity,
           py::return_internal_reference<>())
      .def("CreateDirectories", &CardWriter::CreateDirectories,
           py::return_internal_reference<>())
      .def("SetWildcardMasses", &CardWriter::SetWildcardMasses,
           py::return_internal_reference<>())
    ;

    py::def("CloneObs", CloneObsPy);
    py::def("CloneProcs", CloneProcsPy);
    py::def("CloneSysts", CloneSystsPy);
    py::def("CloneProcsAndSysts", CloneProcsAndSystsPy);
    py::def("SplitSyst", ch::SplitSyst);

    py::class_<BinByBinFactory>("BinByBinFactory")
      .def("MergeBinErrors", &BinByBinFactory::MergeBinErrors)
      .def("AddBinByBin", &BinByBinFactory::AddBinByBin)
      .def("MergeAndAdd", &BinByBinFactory::MergeAndAdd)
      .def("SetVerbosity", &BinByBinFactory::SetVerbosity,
           py::return_internal_reference<>())
      .def("SetAddThreshold", &BinByBinFactory::SetAddThreshold,
           py::return_internal_reference<>())
      .def("SetMergeThreshold", &BinByBinFactory::SetMergeThreshold,
           py::return_internal_reference<>())
      .def("SetPattern", &BinByBinFactory::SetPattern,
           py::return_internal_reference<>())
      .def("SetFixNorm", &BinByBinFactory::SetFixNorm,
           py::return_internal_reference<>())
    ;
    
    py::class_<AutoRebin>("AutoRebin")
      .def("Rebin", &AutoRebin::Rebin)
      .def("SetVerbosity", &AutoRebin::SetVerbosity,
           py::return_internal_reference<>())
      .def("SetBinThreshold", &AutoRebin::SetBinThreshold,
           py::return_internal_reference<>())
      .def("SetBinUncertFraction", &AutoRebin::SetBinUncertFraction,
           py::return_internal_reference<>())
      .def("SetPerformRebin", &AutoRebin::SetPerformRebin,
           py::return_internal_reference<>())
      .def("SetRebinMode", &AutoRebin::SetRebinMode,
           py::return_internal_reference<>())
    ;

    py::def("TGraphFromTable", ch::TGraphFromTable);
    py::def("MassesFromRange", ch::MassesFromRange, defaults_MassesFromRange());
    py::def("ValsFromRange", ch::ValsFromRange, defaults_ValsFromRange());
    py::def("SetStandardBinNames", ch::SetStandardBinNames, defaults_SetStandardBinNames());
    py::def("ParseCombineWorkspace", ch::ParseCombineWorkspacePy);
}
