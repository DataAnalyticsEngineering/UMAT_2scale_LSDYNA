#include <iostream>
#include <Python.h>

extern "C" {
bool pywrapper_();
}

// C++ call Python module
bool pywrapper_()
{
    // Python initialize
    Py_Initialize();
    if (!Py_IsInitialized())
    {
        std::cout << "Python initialization failed!\n";
        return false;
    }

    // umat.py should be in PYTHONPATH
    // std::wstring path = L"repo_files/umat/umat.py";
    // PySys_SetPath(&path[0u]);

    // Import umat.py module
    PyObject* pModule = PyImport_ImportModule("python_example");
    if (!pModule)
    {
        std::cout << "Cannot open Python file!\n";
        return false;
    }

    // Get the py_fun() function in the module
    PyObject* py_fun = PyObject_GetAttrString(pModule, "py_fun");
    if (!py_fun)
    {
        std::cout << "Failed to get this function!";
        return false;
    }

    PyObject* args = PyTuple_Pack(3, PyFloat_FromDouble(2.0), PyFloat_FromDouble(4.0), PyUnicode_FromString((char*)"Greg"));

    // PyObject_CallFunction(py_fun, NULL);
    PyObject* res = PyObject_CallFunctionObjArgs(py_fun, args, NULL);
    int size = Py_SIZE(res);
    std::cout << size << std::endl;
    std::cout << PyFloat_AsDouble(PyList_GetItem(res, 0)) << std::endl;
    std::cout << PyFloat_AsDouble(PyList_GetItem(res, 1)) << std::endl;

    // Finalize
    Py_Finalize();

    return true;
}