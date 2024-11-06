ezh5: Easy HDF5 C++ Library
===========================

An easy to use c++ wrapper for HDF5 library

Features
--------

- Single-header library, just copy into your source code folder
- Very simple API so that knowledge of HDF5 is not required
- Work with std::complex which the original library does not provide
- Easy to mix with original library for customized need


Example
-------

```C++

#include "ezh5.hpp"
#include <complex>

using namespace ezh5;  // this library is defined in namespace ezh5

int main(){
    File fh5 ("Gradebook.h5", H5F_ACC_TRUNC);
    fh5["n_students"] = 120;                     // number of students
    fh5["students"]["a_score"] = 82.7;           // average score
    fh5["students"]["John"]["score"] = 92;     
    auto gr= fh5["teachers"];                    // gr: group
    gr["a_age"] = 45;                            // average age
    gr["z"] = std::complex<double> (1.2, 3.5);   // z: a complex number 1.2+3.5I
    return 0;
}

```

Compare with original library
-----------------------------


### Save an integer

#### original library

steals from [tutorial](http://www.hdfgroup.org/HDF5/Tutor/index.html) of HDF5 ([h5crtdat.c](http://www.hdfgroup.org/ftp/HDF5/current/src/unpacked/examples/h5crtdat.c) [h5_rdwt.c](http://www.hdfgroup.org/ftp/HDF5/current/src/unpacked/examples/h5_rdwt.c))

```C++

	hid_t file, dataset_id, dataspace_id;
	herr_t status;
	int data = 7;
	hsize_t dim = 1;
	
	file_id = H5Fcreate("test.h5", H5F_ACC_TRUNC);
	dataspace_id = H5Screate_simple(1, &dim, NULL);
	dataset_id = H5Dcreate2(file_id, "/dset", H5T_STD_I32BE, dataspace_id,
	                   H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	status = H5Dwrite(dataset_id, H5T_NATIVE_INT, H5S_ALL, H5S_ALL, H5P_DEFAULT, &data);
	
	status = H5Dclose(dataset_id);
	status = H5Sclose(dataspace_id);
	status = H5Fclose(file_id);
	
```

#### ezh5

```C++
	File fh5 ("test.h5", H5F_ACC_TRUNC);
	fh5["dset"] = 7;
	// not need to close, resource is released in destructors of intermediate classes
```


Implementation Details for Other Developers
-------------------------------------------

Two techniques (template and lazy evaluation) to simplify this implementation.

I use template to provide type traits and construct composited datatype such as complex number.

Lazy evaluation is used to improve the performance, and it happens to greatly simplify creating groups.



TODOs
-----

[//]: # (improve as https://github.com/garrison/eigen3-hdf5/blob/master/eigen3-hdf5.hpp)
