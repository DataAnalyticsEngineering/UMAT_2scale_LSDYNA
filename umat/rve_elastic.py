import h5py
import numpy as np
from material_parameters import *

# Note: only diagonal entries from "conductivity" are returned

with h5py.File('/home/alameddin/simkom/src_dyna/repo_files/umat/effective_response.h5', 'r') as file:
    temperature = file['temperature'][:]
    conductivity = file['conductivity'][:]
    stiffness = file['stiffness'][:]
    thermal_strain = file['thermal_strain'][:]
    heat_capacity = file['heat_capacity'][:]

def extract_support_points(temp):
    assert (temperature[0] <= temp <= temperature[-1]), \
        f"Given temperature {temp} is out of the RVE \n offline training temperatures {temperature[0]} to {temperature[-1]}"
    idx_right = np.searchsorted(temperature, temp)
    idx_left = max(idx_right - 1, 0)
    d_temperature = temperature[idx_right] - temperature[idx_left]
    alpha = (temp - temperature[idx_left]) / d_temperature if d_temperature != 0 else 0.0

    return idx_left, idx_right, alpha

def interpolate(x1, x2, alpha):
    return x1 + alpha * (x2 - x1)

def get_thermal(temp):
    idx_left, idx_right, alpha = extract_support_points(temp)
    out_conductivity = interpolate(conductivity[idx_left], conductivity[idx_right], alpha)
    out_heat_capacity = interpolate(heat_capacity[idx_left], heat_capacity[idx_right], alpha)

    return [*np.diag(out_conductivity)] + [*out_heat_capacity]

def get_mechanical(temp):
    idx_left, idx_right, alpha = extract_support_points(temp)
    out_stiffness = interpolate(stiffness[idx_left], stiffness[idx_right], alpha)
    out_thermal_strain = interpolate(thermal_strain[idx_left], thermal_strain[idx_right], alpha)

    return out_stiffness, out_thermal_strain

if __name__ == '__main__':
    temp = 1300
    print(get_thermal(temp))
    print()
    print(get_mechanical(temp))
