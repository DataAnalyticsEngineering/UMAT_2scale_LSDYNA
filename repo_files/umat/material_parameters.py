import scipy.integrate as integrate
import numpy as np

I2 = np.asarray([1., 1., 1., 0, 0, 0])

min_temperature = 293.00
max_temperature = 1300

poisson_ratio_cu = lambda x: 3.40000e-01 * x**0
conductivity_cu = lambda x: 4.20749e+05 * x**0 + -6.84915e+01 * x**1
heat_capacity_cu = lambda x: 2.94929e+03 * x**0 + 2.30217e+00 * x**1 + -2.95302e-03 * x**2 + 1.47057e-06 * x**3
cte_cu = lambda x: 1.28170e-05 * x**0 + 8.23091e-09 * x**1
elastic_modulus_cu = lambda x: 1.35742e+08 * x**0 + 5.85757e+03 * x**1 + -8.16134e+01 * x**2
thermal_strain_cu = lambda x: integrate.quad(cte_cu, min_temperature, x)[0] * I2

yield_cu = lambda x: 1.12133e+02 * x + 3.49810e+04 + 1.53393e+05 * np.tanh(
    (x / 1000 + -6.35754e-01) / -2.06958e-01) if x < 1000 else 1200.0

poisson_ratio_wsc = lambda x: 2.80000e-01 * x**0
conductivity_wsc = lambda x: 2.19308e+05 * x**0 + -1.87425e+02 * x**1 + 1.05157e-01 * x**2 + -2.01180e-05 * x**3
heat_capacity_wsc = lambda x: 2.39247e+03 * x**0 + 6.62775e-01 * x**1 + -2.80323e-04 * x**2 + 6.39511e-08 * x**3
cte_wsc = lambda x: 5.07893e-06 * x**0 + 5.67524e-10 * x**1
elastic_modulus_wsc = lambda x: 4.13295e+08 * x**0 + -7.83159e+03 * x**1 + -3.65909e+01 * x**2 + 5.48782e-03 * x**3
thermal_strain_wsc = lambda x: integrate.quad(cte_wsc, min_temperature, x)[0] * I2

if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    numper_of_points = 20
    temp_end = max_temperature + 1000

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, heat_capacity_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('3_crv_heat_capacity_cu.csv', index=False, header=False, float_format='%.3f')

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, conductivity_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('4_crv_conductivity_cu.csv', index=False, header=False, float_format='%.3f')

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, elastic_modulus_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('5_crv_elastic_modulus_cu.csv', index=False, header=False, float_format='%.3f')

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, cte_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('6_crv_cte_cu.csv', index=False, header=False, float_format='%.6e')

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, poisson_ratio_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('7_crv_poisson_ratio_cu.csv', index=False, header=False, float_format='%.3f')

    df = pd.DataFrame(columns=['temp', 'property'])
    for idx, temp in enumerate(np.linspace(min_temperature, max_temperature, numper_of_points)):
        df.loc[idx] = [temp, yield_cu(temp)]
    df.loc[idx + 1] = [temp_end, df.loc[idx, 'property']]
    df.to_csv('8_crv_yield_cu.csv', index=False, header=False, float_format='%.3f')
