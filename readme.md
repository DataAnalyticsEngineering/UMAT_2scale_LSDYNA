# usermat_2scale_lsdyna

Basics to implement user-defined material routines in LS-Dyna with Python and C++ 
and realize two scale simulation schemes in LS-DYNA.

## External dependencies

Dependencies below are included in the `external_packages` directory. They may be included as submodules but for the sake of reproducablity a frozen version of their corresponding repositories is included here.

- `ttb`: Tensor Toolbox for Modern Fortran (ttb), hosted at https://github.com/adtzlr/ttb

- `forpy`: A library for Fortran-Python interoperability, hosted at https://github.com/ylikx/forpy

- `ezh5`: Easy HDF5 C++ Library, hosted at https://github.com/mileschen360/ezh5

  Test cases of these packages are included in `external_packages/test_*.sh`
  
## Licensing
See the `license` file for the project license and the licenses of the included dependencies.


## Citations
Shadi Alameddin, Felix Fritzen. *LS-DYNA two-scale homogenization extension*. Version 1.0.0 (2021).

```
@software{alameddin2021,
  author       = {Shadi Alameddin, Felix Fritzen},
  title        = {LS-DYNA two-scale homogenization extension},
  month        = Aug,
  year         = 2021,
  version      = {v1.0.0},
  url          = {https://gitlab.com/shadialameddin/dae_umat_2scale_lsdyna}
}
```

## Compiling the base version on Linux (Ubuntu 20.04.2 LTS)
- Start by obtaining `ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz` usermat package/object version of LS-DYNA from your local distributor of LS-DYNA. The directory where `ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz` is placed will be referred to as `dyna_umat_directory`
- Install Intel® C and Fortran compilers that are included in the Intel® oneAPI HPC Toolkit which is available for free. Examples below have been compiled using ifort, icc version 2021.1 and Python 3.7.9 & 3.8.5. In addition, some test use GNU Fortran 9.3.0.

- Obtain the new interface files from GitLab and position it in `dyna_umat_directory` via
```
cd dyna_umat_directory
git clone git@gitlab.com:shadialameddin/dae_umat_2scale_lsdyna.git lsdyna_added_files_ref
```
- Using a terminal, navigate to `dae_umat_2scale_lsdyna` and create a symbolic link to the main setup file via
```
cd dae_umat_2scale_lsdyna
./create_links.sh
cd ..
```
- Edit `set_env.sh` to point to the correct `intel_dir` and add python examples in `lsdyna_added_files_ref` to `PYTHONPATH`.
- Now everything is in place to compile the usermat package, to do that, from `dyna_umat_directory` run `./setup_dyna.sh`.
The new executable will be placed in `dyna_umat_directory/lsdyna_object_version/lsdynaumat`

  ### Note
  
  In case of issues while running from a new shell, setting the correct environmental variables via running `source .env` should fix the problem.

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
  
  `examples/two_scale/3d_rve`

  Here, a thermo-mechanical response of a representative volume element is computed using LS-DYNA.


