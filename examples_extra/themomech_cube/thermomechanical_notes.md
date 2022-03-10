- In case of thermal steady state analysis, don't use automatic time stepping
- In case of transient analysis, increase &endtime to allow all nodes to cool down to the initial temperature
  `test case in results_v02_transient_fix_timestep_cwm: stresses aren't exactly zero due to the temperature field at the last time step`
  - keep auto time stepping in CONTROL_THERMAL_TIMESTEP on but with fixed min_dt = max_dt
    otherwise dtemp doesn't have an effect
  - dtemp should be small to get reasonable results
  - A test case here could be to drop the temperature dependency of the stiffness and thermal expansion

- In scenarios where the temperature of all nodes change simultaneously, there's no issue with the residual stresses 