# usermat_2scale_lsdyna

Basics to implement user-defined material routines in LS-Dyna with Python and C++. This repo realizes two scale simulation schemes in LS-DYNA.

## External dependencies

Dependencies below are included in the `external_packages` directory. They may be included as submodules but for the sake of reproducablity a frozen version of their corresponding repositories is included here.

- `ttb`: Tensor Toolbox for Modern Fortran (ttb), hosted at https://github.com/adtzlr/ttb

- `forpy`: A library for Fortran-Python interoperability, hosted at https://github.com/ylikx/forpy

- `ezh5`: Easy HDF5 C++ Library, hosted at https://github.com/mileschen360/ezh5

  Test cases of these packages are included in `external_packages/test_*.sh`
  
## Licensing
See the `license` file for the project license and the licenses of the included dependencies.


## Citations
Shadi Sharba, Felix Fritzen, Julius Herb. *LS-DYNA two-scale homogenization extension*. Version 1.0.0 (2021).

```
@software{sharba2021,
  author       = {Shadi Sharba, Felix Fritzen, Julius Herb},
  title        = {LS-DYNA two-scale homogenization extension},
  month        = Aug,
  year         = 2021,
  version      = {v1.0.0},
  url          = {https://github.com/DataAnalyticsEngineering/UMAT_2scale_LSDYNA}
}
```

## Compiling using docker

- Obtain the new interface files from GitHub to `UMAT_2scale_LSDYNA` folder via
```
git clone https://github.com/DataAnalyticsEngineering/UMAT_2scale_LSDYNA.git && cd UMAT_2scale_LSDYNA
```

- Obtain `ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz` usermat package/object version of LS-DYNA from your local distributor of LS-DYNA. Here are some helpful links [[lsdyna-ansys](https://lsdyna.ansys.com/downloader-filter/),[](https://innovationspace.ansys.com/forum/forums/reply/235696/)]. Move `ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz` to `UMAT_2scale_LSDYNA`

- Using a terminal, run one of the following commands to build the docker image, compile the new executable and enter the running container:
  - `docker-compose up --build -d && docker-compose run UMAT_2scale_LSDYNA && docker-compose down`
  - `docker compose build --progress plain && docker run -it my_umat_lsdyna_image && docker-compose down`

- The new executable will be placed inside the docker container in `UMAT_2scale_LSDYNA/lsdyna_object_version/lsdynaumat`

## Test cases:
- External packages: test cases of these packages are included in `external_packages/test_*.sh`
  - `test_ttb.sh`
  - `test_forpy.sh`
  - `test_ezh5.sh`
- Mixed language programming
  - `test_call_cpp.sh`: compiles and runs a Fortran function that calls a C++ one
  - `test_call_py.sh`: compiles and runs a Fortran function that calls a Python one via C++
  
## Examples:
- `examples/two_scale/analytical_mat_parameter`

  Temperature dependent material parameters are considered here and given as lambda functions in `material_parameters.py`.
  
  To get an idea about the implementation check:
  - `umat_elastic_44_14.F90`
  - `material_parameters.py`
  - `umat.py`
  
- `examples/two_scale/homogeneous_single_track`
  
  Here, an RVE effective response under different load temperatures is assumed to exist and stored in a tabulated format in an HDF5 file. Linear interpolation is used to evaluate effective properties at current temperature given the stored response at one higher and one lower temperatures.
  
  To get an idea about the implementation check:
    - `umat_elastic_44_14.F90`
    - `umat.py`
    - `rve_elastic.py`

- __Discontinued__
  
  - `examples/two_scale/3d_rve`
  - `examples/two_scale/2d_rve` 

  Here, a thermo-mechanical response of a representative volume element is computed using LS-DYNA.


