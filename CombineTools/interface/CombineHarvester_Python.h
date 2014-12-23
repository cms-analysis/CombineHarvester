#include <vector>
#include <set>
#include "boost/python.hpp"
#include "boost/python/type_id.hpp"
#include "TPython.h"
namespace bp = boost::python;

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
