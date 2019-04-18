#include <vector>
#include <set>
#include <map>
#include "boost/python.hpp"
#include "boost/python/type_id.hpp"
#include "TPython.h"
namespace bp = boost::python;

namespace ch { class CombineHarvester; }

void FilterAllPy(ch::CombineHarvester & cb, boost::python::object func);
void FilterObsPy(ch::CombineHarvester & cb, boost::python::object func);
void FilterProcsPy(ch::CombineHarvester & cb, boost::python::object func);
void FilterSystsPy(ch::CombineHarvester & cb, boost::python::object func);

void ForEachObjPy(ch::CombineHarvester & cb, boost::python::object func);
void ForEachObsPy(ch::CombineHarvester & cb, boost::python::object func);
void ForEachProcPy(ch::CombineHarvester & cb, boost::python::object func);
void ForEachSystPy(ch::CombineHarvester & cb, boost::python::object func);

void CloneObsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                boost::python::object func);
void CloneProcsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                  boost::python::object func);
void CloneSystsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                boost::python::object func);
void CloneProcsAndSystsPy(ch::CombineHarvester& src, ch::CombineHarvester& dest,
                        boost::python::object func);

void Overload3_WriteDatacard(ch::CombineHarvester & cb, std::string const& name, bp::object& file);

/**
 * Covert a C++ ROOT type to a PyROOT type
 */
template <typename T>
struct convert_cpp_root_to_py_root {
  static PyObject* convert(T const& in) {
    // Make a copy of the input object and give control of it to python
    // (implied by the "true" in the conversion function)
    T* out = new T(in);
    return TPython::ObjectProxy_FromVoidPtr(out, out->ClassName(), true);
  }
};

/**
 * Convert a C++ vector to a python list
 */
template <typename T>
struct convert_cpp_vector_to_py_list {
  static PyObject* convert(const std::vector<T>& in) {
    bp::list out;
    for (T const& ele : in) out.append(ele);
    return bp::incref(out.ptr());
  }
};

/**
 * Convert a C++ set to a python list
 */
template <typename T>
struct convert_cpp_set_to_py_list {
  static PyObject* convert(const std::set<T>& in) {
    bp::list out;
    for (T const& ele : in) out.append(ele);
    return bp::incref(out.ptr());
  }
};

/**
 * Convert a C++ map to a python dict
 */
template <typename TKey, typename TValue>
struct convert_cpp_map_to_py_dict {
  static PyObject* convert(const std::map<TKey, TValue>& in) {
    bp::dict out;
    for (std::pair<TKey, TValue> const& ele : in) out[ele.first] = ele.second;
    return bp::incref(out.ptr());
  }
};

template <typename T>
struct convert_py_root_to_cpp_root {
  convert_py_root_to_cpp_root() {
    bp::converter::registry::push_back(&convertible, &construct,
                                       bp::type_id<T>());
  }
  static void* convertible(PyObject* obj_ptr) { return obj_ptr; }

  static void construct(PyObject* obj_ptr,
                        bp::converter::rvalue_from_python_stage1_data* data) {
    T* TObj = (T*)(TPython::ObjectProxy_AsVoidPtr(obj_ptr));

    // Grab pointer to memory into which to construct the new QString
    // void* storage =
    //     ((boost::python::converter::rvalue_from_python_storage<T>*)data)
    //         ->storage.bytes;

    // in-place construct the new QString using the character data
    // extraced from the python object
    // storage = TObj;

    // Stash the memory chunk pointer for later use by boost.python
    data->convertible = TObj;
  }
};

template <typename T>
struct convert_py_seq_to_cpp_vector {
  convert_py_seq_to_cpp_vector() {
    bp::converter::registry::push_back(&convertible, &construct,
                                   bp::type_id<std::vector<T> >());
  }
  static void* convertible(PyObject* obj_ptr) {
    // the second condition is important, for some reason otherwise there were
    // attempted conversions of Body to list which failed afterwards.
    if (!PySequence_Check(obj_ptr) ||
        !PyObject_HasAttrString(obj_ptr, "__len__"))
      return 0;
    return obj_ptr;
  }
  static void construct(PyObject* obj_ptr,
                        bp::converter::rvalue_from_python_stage1_data* data) {
    void* storage = ((bp::converter::rvalue_from_python_storage<
                         std::vector<T> >*)(data))->storage.bytes;
    new (storage) std::vector<T>();
    std::vector<T>* v = (std::vector<T>*)(storage);
    int l = PySequence_Size(obj_ptr);
    if (l < 0) abort();
    v->reserve(l);
    for (int i = 0; i < l; i++) {
      v->push_back(bp::extract<T>(PySequence_GetItem(obj_ptr, i)));
    }
    data->convertible = storage;
  }
};

// from http://cci.lbl.gov/cctbx_sources/boost_adaptbx/std_pair_conversion.h
template <typename T, typename U>
struct convert_py_tup_to_cpp_pair {
  convert_py_tup_to_cpp_pair() {
    bp::converter::registry::push_back(
        &convertible, &construct, boost::python::type_id<std::pair<T, U> >()
        // #ifdef BOOST_PYTHON_SUPPORTS_PY_SIGNATURES
        // , get_pytype
        // #endif
        );
  }

  // static const PyTypeObject *get_pytype() { return &PyTuple_Type; }

  static void* convertible(PyObject* obj_ptr) {
    if (!PyTuple_Check(obj_ptr) || PyTuple_GET_SIZE(obj_ptr) != 2) return 0;
    return obj_ptr;
  }

  static void construct(PyObject* obj_ptr,
                        bp::converter::rvalue_from_python_stage1_data* data) {
    PyObject* first = PyTuple_GET_ITEM(obj_ptr, 0),
              *second = PyTuple_GET_ITEM(obj_ptr, 1);
    void* storage =
        ((bp::converter::rvalue_from_python_storage<std::pair<T, U> >*)data)
            ->storage.bytes;
    new (storage)
        std::pair<T, U>(bp::extract<T>(first), bp::extract<U>(second));
    data->convertible = storage;
  }
};
