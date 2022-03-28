- In case of thermal steady state analysis, don't use automatic time stepping
- In case of transient analysis, increase &endtime to allow all nodes to cool down to the initial temperature
  `test case in results_v02_transient_fix_timestep_cwm: stresses aren't exactly zero due to the temperature field at the last time step`
  - keep auto time stepping in CONTROL_THERMAL_TIMESTEP on but with fixed min_dt = max_dt
    otherwise dtemp doesn't have an effect
  - dtemp should be small to get reasonable results
  - A test case here could be to drop the temperature dependency of the stiffness and thermal expansion

- In scenarios where the temperature of all nodes change simultaneously, there's no issue with the residual stresses 


- themomech_cube_fixed_timestep_sent.zip

heat then cooldown a cube, stresses never go back to zero 

  - The stresses are not zero even after cooling down the cube and the absence of plasticity (I confirmed using elout files not only LSPP)
  - The value of the "artificial" residual stresses is proportional to the temperature gradient when heating the cube (curves 111 and 222 in the attached files)
  - Total strain and elastic strain do not match even though thermal and plastic strains are zero
  
- test1_themomech_cube_fixed_timestep_thermalstrain
  - strain matches thermal strain but
  - thermal strain in prepost is shown as zero ???!!!
  
  
  
- test2_themomech_cube_fixed_timestep_v01_clamped
  - zero displacement and zero strain
  - stresses are not zero due to thermal strain but
  - thermal strain in prepost is shown as zero ???!!!
  
  
  
  
ASK:
- thermal strain in prepost is shown as zero ???!!!
- can be tested with umat


LS-DYNA bug, boundary conditions aren't satisfied
strain and elastic strain aren't matching??!!