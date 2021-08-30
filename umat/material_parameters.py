density_cu = lambda x: 8.93300e-06
poisson_ratio_cu = lambda x: 3.40000e-01
conductivity_cu = lambda x: 4.20749e+05 - 6.84915e+01 * x
heat_capacity_cu = lambda x: 3.16246e+08 + 3.17858e+05 * x - 3.49795e+02 * x**2 + 1.66327e-01 * x**3
cte_cu = lambda x: 1.28170e-05 + 8.23091e-09 * x
elastic_modulus_cu = lambda x: max(6.4126e+05, 1.35742e+08 + 5.85757e+03 * x - 8.16134e+01 * x**2)

density_wsc = lambda x: 1.93000e-05
poisson_ratio_wsc = lambda x: 2.80000e-01
conductivity_wsc = lambda x: 2.19308e+05 - 1.87425e+02 * x + 1.05157e-01 * x**2 - 2.01180e-05 * x**3
heat_capacity_wsc = lambda x: 1.23958e+08 + 3.44414e+04 * x - 1.25514e+01 * x**2 + 2.87070e-03 * x**3
cte_wsc = lambda x: 5.07893e-06 + 5.67524e-10 * x
elastic_modulus_wsc = lambda x: 4.13295e+08 - 7.83159e+03 * x - 3.65909e+01 * x**2 + 5.48782e-03 * x**3
