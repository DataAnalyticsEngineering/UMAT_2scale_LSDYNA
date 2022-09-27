# 3D microstructure data

This repository acts as an extension to the 2D microstructure dataset provided by Julian Lißner in https://doi.org/10.18419/darus-1151. Here, image data of 3D microstructures with nonoverlapping spherical inclusions and variable volume fraction, from 25% to 45%, is provided. 

Temperature dependent thermo-mechanical effective properties are computed and stored in one single hdf5 file based on finite element simulations using a Fourier accelerated nodal solver code provided by Sanath Keshav.

The microstructure is defined with a representative volume element (RVE) with periodic boundary conditions. 10000 images are generated using the files in `rve_generation`. Further details are provided in the "details & how to use" section below.

## Details & how to use?
- `data` directory
  - Thermo-elastic temperature-dependent material parameters are provided in `material_parameters.xlsx`
  - The 10000 RVEs and their corresponding effective properties are stored in `random_3d_rve.h5` with the a structure similar to what is shown in the image below
  ![](h5ll.png)
  As illustrated above, for each dataset starting with `dset`, the dataset itself such as `dset0` contains the image/microstructure data then `dset0_sim` contains all relevant simulation results and metadata such as volume fraction, convergence tolerance and so on.
  
- `rve_generation` directory
  - `gen_rve.sh` is a bash script to run `gen_microstructure.py` and pipe the terminal output to `random_3d_rve.txt`
  - `gen_xdmf.py` is used to generate `random_3d_rve.xdmf` that can be opened using Paraview to visualize the microstructures. *It is advisable to load a few RVEs/datasets at a time, in order not overload your hardware*
  - `gen_microstructure.py` is the main file used to generate `random_3d_rve.h5`
  
- `h5ll.py` is used as `python h5ll.py hdf5_file.h5/group0` to investigate the content of the hdf5 file, as illustrated in the image above

- `effective_rve_response.ipynb` is an interactive jupyter notebook that provide all necessary tools to investigate the generated raw image data and the resulting simulation response thereof
