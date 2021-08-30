import h5py
import numpy as np
from material_parameters import *

with h5py.File('/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/umat/effective_response.h5', 'r') as file:
    temperature = file['temperature'][:]
    conductivity = file['conductivity'][:]
    stiffness = file['stiffness'][:]
    thermal_exp = file['thermal_exp'][:]
    heat_capacity = file['heat_capacity'][:]

def get_thermal(temp):
    assert (temperature[0] <= temp <= temperature[-1]), f"Given temperature {temp} is out of the RVE offline training temperatures {temperature[0]} to {temperature[-1]}"
    idx_right = np.searchsorted(temperature, temp)
    if idx_right == 0 or idx_right == len(temperature):
        idx_left = idx_right
    else:
        idx_left = idx_right - 1
    if idx_left < 0:
        idx_left = 0
    if idx_right == len(temperature):
        idx_right -= 1
        idx_left = idx_right
    if temperature[idx_right] != temperature[idx_left]:
        d_theta = temperature[idx_right] - temperature[idx_left]
        out_conductivity = conductivity_cu(temp) * (conductivity[idx_right] *
                                                    (temp - temperature[idx_left]) + conductivity[idx_left] *
                                                    (temperature[idx_right] - temp)) / d_theta
        out_heat_capacity = density_cu(temp) * heat_capacity_cu(temp) * (heat_capacity[idx_right] *
                                                                         (temp - temperature[idx_left]) +
                                                                         heat_capacity[idx_left] *
                                                                         (temperature[idx_right] - temp)) / d_theta
    else:
        out_conductivity = conductivity_cu(temp) * conductivity[idx_right]
        out_heat_capacity = density_cu(temp) * heat_capacity_cu(temp) * heat_capacity[idx_right]

    return [*np.diag(out_conductivity)] + [*out_heat_capacity]

def get_mechanical(temp):
    assert (temperature[0] <= temp <= temperature[-1]), "Given temperature is out of the RVE offline training temperatures"
    idx_right = np.searchsorted(temperature, temp)
    if idx_right == 0 or idx_right == len(temperature):
        idx_left = idx_right
    else:
        idx_left = idx_right - 1
    if idx_left < 0:
        idx_left = 0
    if idx_right == len(temperature):
        idx_right -= 1
        idx_left = idx_right

    if temperature[idx_right] != temperature[idx_left]:
        d_theta = temperature[idx_right] - temperature[idx_left]
        out_stiffness = elastic_modulus_cu(temp) * (stiffness[idx_right] * (temp - temperature[idx_left]) + stiffness[idx_left] *
                                                    (temperature[idx_right] - temp)) / d_theta
        out_thermal_exp = cte_cu(temp) * (thermal_exp[idx_right][0] * (temp - temperature[idx_left]) + thermal_exp[idx_left][0] *
                                          (temperature[idx_right] - temp)) / d_theta
    else:
        out_stiffness = elastic_modulus_cu(temp) * stiffness[idx_right]
        out_thermal_exp = cte_cu(temp) * thermal_exp[idx_right][0]

    return out_stiffness, out_thermal_exp

if __name__ == '__main__':
    temp = 293
    print(get_thermal(temp))
    print()
    print(get_mechanical(temp))
