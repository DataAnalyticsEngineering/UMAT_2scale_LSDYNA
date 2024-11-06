import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py

file_name = 'simple_3d_rve_physical_32normal_voxels.h5'

with h5py.File(file_name, 'r') as file:
    E0 = file['/ms_9p/dset0_sim/localization_strain_0293.15'][:]
    E1 = file['/ms_9p/dset0_sim/localization_strain_0544.86'][:]
    E2 = file['/ms_9p/dset0_sim/localization_strain_0796.58'][:]
    mat_ids = file['/ms_9p/dset0_sim/mat_id'][:].flatten()
    element = file['/ms_9p/dset0_sim'].attrs['element'][0]
    mat_stiffness = file['/ms_9p/dset0_sim/localization_mat_stiffness_0293.15'][:]
    mat_thermal_strain = file['/ms_9p/dset0_sim/localization_mat_thermal_strain_0293.15'][:]

# E1approx = .5 * E0 + .5 * E2
# print(np.linalg.norm((E1 - E1approx).flatten()) / np.linalg.norm((E1).flatten()) * 100)
#%%

macro_strain = np.asarray([1, 2, 3, 4, 5, 6])
activation = np.hstack((macro_strain, 1))
print(E0.shape)
strain = np.einsum('ijk,j->ik', E0, activation, optimize='optimal')
print(strain.shape)

micro_ngp = int(element[-1])
n_element = mat_ids.shape
S0 = np.empty_like(E0)
for idx, mat_id in enumerate(mat_ids):
    idx_rng = range(idx * micro_ngp, (idx + 1) * micro_ngp)
    # mat_stiffness has to transposed because it's coming from MATLAB
    S0[idx_rng] = np.einsum('kl,ijk->ijl', mat_stiffness[mat_id], (E0[idx_rng] - np.vstack(
        (-np.eye(6), mat_thermal_strain[mat_id]))), optimize='optimal')

stress = np.einsum('ijk,j->ik', S0, activation, optimize='optimal')
av_stress_phase0 = np.mean(stress[np.repeat(mat_ids == 0, micro_ngp)], 0)
av_stress_phase1 = np.mean(stress[np.repeat(mat_ids == 1, micro_ngp)], 0)
