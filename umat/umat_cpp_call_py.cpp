#include <iostream>
#include <Python.h>

extern "C" {
void cppcallpython_thermal_(const double& mat_id, const double& temperature, double& c1, double& c2, double& c3, double& cvl);
}

// C++ call Python module
void cppcallpython_thermal_(const double& mat_id, const double& temperature, double& c1, double& c2, double& c3, double& cvl)
{
    // Python initialize
    Py_Initialize();

    PyObject* pModule = PyImport_ImportModule("umat");

    // Get the rve_solver_factory() function in the module
    PyObject* py_fun = PyObject_GetAttrString(pModule, "rve_solver_factory");

    // PyObject* args = PyTuple_Pack(3, PyFloat_FromDouble(0),PyFloat_FromDouble(mat_id), PyFloat_FromDouble(temperature));

    // std::cout << mat_id << " " << temperature << std::endl;
    // PyObject_CallFunction(py_fun, NULL);
    PyObject* output = PyObject_CallFunctionObjArgs(py_fun, PyFloat_FromDouble(0), PyFloat_FromDouble(mat_id), PyFloat_FromDouble(temperature), NULL);

    // int size = Py_SIZE(output);
    // std::cout << "size " << size << std::endl;
    // std::cout << PyFloat_AsDouble(PyList_GetItem(output,0)) << std::endl;
    // std::cout << PyFloat_AsDouble(PyList_GetItem(output,1)) << std::endl;

    c1 = PyFloat_AsDouble(PyList_GetItem(output, 0));
    c2 = PyFloat_AsDouble(PyList_GetItem(output, 1));
    c3 = PyFloat_AsDouble(PyList_GetItem(output, 2));
    cvl = PyFloat_AsDouble(PyList_GetItem(output, 3));

    // Finalize
    // Py_Finalize();
}

extern "C" {
void cppcallpython_mechanical_(const double& mat_id, const double& temperature, const double& d_temperature, double* strain, double* stress, double* stiffness);
}

// C++ call Python module
void cppcallpython_mechanical_(const double& mat_id, const double& temperature, const double& d_temperature, double* strain, double* stress, double* stiffness)
{
    // Python initialize
    Py_Initialize();

    PyObject* pModule = PyImport_ImportModule("umat");

    // Get the rve_solver_factory() function in the module
    PyObject* py_fun = PyObject_GetAttrString(pModule, "rve_solver_factory");

    // PyObject* args = PyTuple_Pack(3, PyFloat_FromDouble(0),PyFloat_FromDouble(mat_id), PyFloat_FromDouble(temperature));

    // std::cout << mat_id << " " << temperature << std::endl;
    // PyObject_CallFunction(py_fun, NULL);
    PyObject* output = PyObject_CallFunctionObjArgs(py_fun,
                                                    PyFloat_FromDouble(1),
                                                    PyFloat_FromDouble(mat_id),
                                                    PyFloat_FromDouble(temperature),
                                                    PyFloat_FromDouble(d_temperature),
                                                    PyFloat_FromDouble(strain[0]),
                                                    PyFloat_FromDouble(strain[1]),
                                                    PyFloat_FromDouble(strain[2]),
                                                    PyFloat_FromDouble(strain[3]),
                                                    PyFloat_FromDouble(strain[4]),
                                                    PyFloat_FromDouble(strain[5]),
                                                    NULL);

    // int size = Py_SIZE(output);
    // std::cout << "size " << size << std::endl;
    // std::cout << PyFloat_AsDouble(PyList_GetItem(output,0)) << std::endl;
    // std::cout << PyFloat_AsDouble(PyList_GetItem(output,1)) << std::endl;
    // std::cout << PyFloat_AsDouble(PyList_GetItem(output,3)) << std::endl;

    for (int i = 0; i < 6; i++) stress[i] = PyFloat_AsDouble(PyList_GetItem(output, i));
    for (int i = 6; i < 42; i++) stiffness[i - 6] = PyFloat_AsDouble(PyList_GetItem(output, i));

    // Finalize
    // Py_Finalize();
}