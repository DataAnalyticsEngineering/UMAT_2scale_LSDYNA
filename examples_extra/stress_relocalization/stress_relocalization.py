# file:///home/alameddin/LSTC/LS-PrePost4.8/lsppconf
# pythonhome = /home/alameddin/.dontsync/packages/pyenv/versions/3.6.5/
# or setpythonhome /home/alameddin/.dontsync/packages/pyenv/versions/3.6.5/

import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo, switch_state
import LsPrePost

import matplotlib.pyplot as plt
import numpy as np
import h5py

sqrt2 = np.sqrt(2)

file = "/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/examples/two_scale/homogeneous_single_track/coupled.d3plot"
execute_command(f'model remove 1')
execute_command(f'open d3plot {file}')
execute_command(f'ac')

num_states = dc.get_data("num_states")
switch_state(num_states)
# TODO: we need the temperature at the integration points
nodal_temperatures = dc.get_data("nodal_temperatures")

# TODO only consider part 1
strain_x = dc.get_data("strain_x", type=Type.SOLID)
strain_y = dc.get_data("strain_y", type=Type.SOLID)
strain_z = dc.get_data("strain_z", type=Type.SOLID)
strain_xy = dc.get_data("strain_xy", type=Type.SOLID)
strain_yz = dc.get_data("strain_yz", type=Type.SOLID)
strain_zx = dc.get_data("strain_zx", type=Type.SOLID)

# global_strain = dc.get_data("global_strain", type=Type.SOLID, ist=num_states)
# print(np.array(global_strain).shape)
# print(type(global_strain))

macro_strain = np.vstack((strain_x, strain_y, strain_z, strain_xy / sqrt2, strain_yz / sqrt2, strain_zx / sqrt2))
# TODO only consider part 1
# macro_strain = macro_strain[:,:100]
macro_ngp = macro_strain.shape[1]

print(f'elemofpart_ids: {dc.get_data("elemofpart_ids",id=0,type=Type.SOLID), np.asarray(dc.get_data("elemofpart_ids",id=0,type=Type.SOLID)).shape}')
print(f'partofmat_ids: {dc.get_data("partofmat_ids", id=0), np.asarray(dc.get_data("partofmat_ids", id=0)).shape}')
print(f'element_connectivity: {dc.get_data("element_connectivity",id=1,type=Type.SOLID), np.asarray(dc.get_data("element_connectivity",id=1,type=Type.SOLID)).shape}')
print(f'element_connectivity: {np.asarray(dc.get_data("element_connectivity",id=1,type=Type.SOLID))}')
print(f'historyvar: {dc.get_data("historyvar",type=Type.SOLID), np.asarray(dc.get_data("historyvar",type=Type.SOLID)).shape}')

print(f'is_full_integrated: {dc.get_data("is_full_integrated") }')
print(f'elements: {dc.get_data("num_elements") }')
print(f'num_nodes: {dc.get_data("num_nodes") }')
print(f'num_parts: {dc.get_data("num_parts") }')
print(f'materials: {dc.get_data("num_materials") }')
print(f'nodal_temperatures {np.asarray(nodal_temperatures).shape}')
print(f'macro_strain {macro_strain.shape}')

file_name = 'simple_3d_rve_physical_32normal_voxels.h5'

with h5py.File(file_name, 'r') as file:
    E0 = file['/ms_9p/dset0_sim/localization_strain_0293.15'][:]
    mat_ids = file['/ms_9p/dset0_sim/mat_id'][:].flatten()
    element = file['/ms_9p/dset0_sim'].attrs['element'][0]
    mat_stiffness = file['/ms_9p/dset0_sim/localization_mat_stiffness_0293.15'][:]
    mat_thermal_strain = file['/ms_9p/dset0_sim/localization_mat_thermal_strain_0293.15'][:]

activation = np.vstack((macro_strain, np.repeat(1, macro_ngp)))

exit()

micro_ngp = int(element[-1])
n_element = mat_ids.shape
S0 = np.empty_like(E0)
for idx, mat_id in enumerate(mat_ids):
    idx_rng = range(idx * micro_ngp, (idx + 1) * micro_ngp)
    # mat_stiffness has to transposed because it's coming from MATLAB
    S0[idx_rng] = np.einsum('kl,ijk->ijl', mat_stiffness[mat_id], (E0[idx_rng] - np.vstack(
        (-np.eye(6), mat_thermal_strain[mat_id]))), optimize='optimal')

# stress = np.einsum('ijk,jl->ilk', S0, activation, optimize='optimal')
# print(stress.shape)
# av_stress_phase0 = np.mean(stress[np.repeat(mat_ids == 0, micro_ngp)], axis=(0, 1))
# av_stress_phase1 = np.mean(stress[np.repeat(mat_ids == 1, micro_ngp)], axis=(0, 1))
#
# with np.printoptions(precision=4, suppress=True, formatter={'float': '{:>2.2e}'.format}, linewidth=100):
#     print(av_stress_phase0)
#     print(av_stress_phase1)

x = []
# TODO remove 1000 from the next line range(macro_ngp)
for macro_gp in range(1000):
    act = activation[:, macro_gp]
    stress = np.einsum('ijk,j->ik', S0, act, optimize='optimal')

    av_stress = np.mean(stress, axis=0)
    av_stress_phase0 = np.mean(stress[np.repeat(mat_ids == 0, micro_ngp)], axis=0)
    av_stress_phase1 = np.mean(stress[np.repeat(mat_ids == 1, micro_ngp)], axis=0)

    x.append(np.linalg.norm(av_stress_phase1))

plt.hist(x)
plt.savefig('del.pdf', dpi=300)

# plt.xlim([0, 25])
# plt.ylim([700, 1025])
# plt.xlabel('Time [Sec]', fontsize=18)
# plt.ylabel('Temperature [K]', fontsize=18)
#
# plt.grid('on')
# plt.legend()
# plt.tight_layout()
# plt.show()

# TODO: eigenval: principal stresses, von Mises, average, ...

# Average value (×), minimum and maximum over all realizations and ±3σ(G a )
# error indicators; gray area: 5-
#
# Histogram of the Young’s modulus for aggregates of 100 grains with comparison
# to a normal distribution with same first and second moment
#
# eq_stress over time
