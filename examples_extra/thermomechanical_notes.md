- In case of thermal steady state analysis, don't use automatic time stepping
- In case of transient analysis, increase &endtime to allow all nodes to cool down to the initial temperature
  - keep auto time stepping in CONTROL_THERMAL_TIMESTEP on but with fixed min_dt = max_dt
    otherwise dtemp doesn't have an effect
  - dtemp should be small to get reasonable results
  - A test case here could be to drop the temperature dependency of the stiffness and thermal expansion

- In scenarios where the temperature of all nodes change simultaneously, there's no issue with the residual stresses 

- `2_transient_mat270`

heat then cooldown a cube, stresses never go back to zero 

  - The stresses are not zero even after cooling down the cube and the absence of plasticity (I confirmed using elout files not only LSPP)
  - The value of the "artificial" residual stresses is proportional to the temperature gradient when heating the cube (curves 111 and 222 in the attached files)
  - Total strain and elastic strain do not match even though thermal and plastic strains are zero

  - Try:
    - MAT_270: MAT_CWM: thermo-elastic-plastic model with kinematic hardening that allows for material creation as well as annealing triggered by temperature. The acronym CWM stands for Computational Welding Mechanics.
    The max. residual von Mises stress for the model with MAT_106 is ~3.0e-1 kPa.

    - MAT_106: MAT_ELASTIC_VISCOPLASTIC_THERMAL
      The max. residual von Mises stress for the model with MAT_106 is ~3.4e-8 kPa.

    - UMAT
      The max. residual von Mises stress for the model with MAT_106 is ~2e-7 kPa.
    
- `thermomech_comb/weld_thermo_elastic`  
  Comb simulation using MAT_270, MAT_106 & UMAT & realistic weld scenario
  Results are drastically different between 270 and 106 but still don't meet expectation, ~15 MPa
  Best results are obtained with UMAT, < 0.04 MPa



__Conclusions & options__:
- Best option
  Using UMAT -> everything has to be activated from the beginning so no sections & prepost automation can be used only to show what we intended to do. [in case there's time, we could look at birth/death parameters in prepost to kind of replicate activation/deactivation]
  use C++ version
  fix ncpu=1 issue

- Not recommended: we can approximate activation/deactivation by giving all material parameters as curves with very small parameter values when inactive and the actual values when active but this will require drastic changes in the input file

- Not recommended: we can implement activation/deactivation in UMAT but this might take some time and will require changes in the input file (prob. a new material should be defined for each part)