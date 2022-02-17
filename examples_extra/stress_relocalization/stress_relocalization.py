# file:///home/alameddin/LSTC/LS-PrePost4.8/lsppconf
# pythonhome = /home/alameddin/.dontsync/packages/pyenv/versions/3.6.5/
# or setpythonhome /home/alameddin/.dontsync/packages/pyenv/versions/3.6.5/

# runpython ex1.py

import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo,switch_state
import LsPrePost

import matplotlib.pyplot as plt
import numpy as np
import h5py

sqrt2 = np.sqrt(2)
scaling_factor = 1

# file = "/home/alameddin/simkom/src_dyna/lsdyna_added_files_ref/examples/two_scale/homogeneous_single_track/coupled.d3plot"
# execute_command(f'model remove 1')
# execute_command(f'open d3plot {file}')
# execute_command(f'ac')


switch_state(100)
nodal_temperatures0 = dc.get_data("nodal_temperatures")

switch_state(101)
nodal_temperatures1 = dc.get_data("nodal_temperatures")
strain_x = dc.get_data("strain_x", type=Type.SOLID)
strain_y = dc.get_data("strain_y", type=Type.SOLID)
strain_z = dc.get_data("strain_z", type=Type.SOLID)
strain_xy = dc.get_data("strain_xy", type=Type.SOLID)
strain_yz = dc.get_data("strain_yz", type=Type.SOLID)
strain_zx = dc.get_data("strain_zx", type=Type.SOLID)

macro_strain = np.vstack((strain_x,strain_y,strain_z,strain_xy/sqrt2,strain_yz/sqrt2,strain_zx/sqrt2))

# print(np.min(nodal_temperatures0))
# print(np.max(nodal_temperatures1))
# TODO: this is only an approximation. Should calculate d_theta for each integration point
d_theta = np.max(nodal_temperatures1) - np.min(nodal_temperatures0)

file_name = 'new_simple_3d_rve_localization.h5'

with h5py.File(file_name, 'r') as file:
    # TODO should consider the actual temperature
    mat_id = np.squeeze(file['/ms_9p/dset2_sol/mat_id'][:])
    combo_vol_frac0 = np.squeeze(file['/ms_9p/dset2_sol/combo_vol_frac0'][:])
    stress_localization = file[f'/ms_9p/dset2_sol/stress_localization_{"0293.00"}'][:]/scaling_factor
    stress_localization0 = file[f'/ms_9p/dset2_sol/stress_localization0_{"0293.00"}'][:]/scaling_factor
    stress_localization1 = file[f'/ms_9p/dset2_sol/stress_localization1_{"0293.00"}'][:]/scaling_factor
    eigen_stress = file[f'/ms_9p/dset2_sol/eigen_stress_{"0293.00"}'][:]/scaling_factor
    eigen_stress0 = file[f'/ms_9p/dset2_sol/eigen_stress0_{"0293.00"}'][:]/scaling_factor
    eigen_stress1 = file[f'/ms_9p/dset2_sol/eigen_stress1_{"0293.00"}'][:]/scaling_factor

combo_vol_frac1 = 1-combo_vol_frac0

stress_field = np.einsum('ijk,jl->ikl',stress_localization,macro_strain,optimize='optimal')
stress_field0 = np.einsum('ijk,jl->ikl',stress_localization0,macro_strain,optimize='optimal')
stress_field1 = np.einsum('ijk,jl->ikl',stress_localization1,macro_strain,optimize='optimal')
print(stress_localization.shape)
print(macro_strain.shape)
print(stress_field.shape) # RVE_ngp, 6, macro_ngp

macro_ngp = macro_strain.shape[1]
x=[]
for macro_gp in range(macro_ngp):
    mean_stress = stress_field[:,:,macro_gp].mean(axis=0)
    mean_stress0 = (stress_field[mat_id==0,:,macro_gp].sum(axis=0) + combo_vol_frac0 @ stress_field0[:,:,macro_gp])/(np.sum(mat_id==0)+np.sum(combo_vol_frac0))
    mean_stress1 = (stress_field[mat_id==1,:,macro_gp].sum(axis=0) + combo_vol_frac1 @ stress_field1[:,:,macro_gp])/(np.sum(mat_id==1)+np.sum(combo_vol_frac1))
    # with np.printoptions(precision=4, suppress=True, formatter={'float': '{:>2.2e}'.format}, linewidth=100):
    #     print(mean_stress)
    #     print(mean_stress0)
    #     print(mean_stress1)
    # print(np.linalg.norm(mean_stress))
    # print(np.linalg.norm(mean_stress0))
    # print(np.linalg.norm(mean_stress1))
    x.append(np.linalg.norm(mean_stress1))

plt.hist(x)
plt.show()

# TODO: eigenval: principal stresses, von Mises, average, ...

# TODO compare with effective ...
# mean(stress_localization,3)

# hom_stress0 = (sum(squeeze(stress(:,:,find(G.ms==0))),2) + sum(stress0.*reshape(G.vol_frac0,[1,1,size(stress0,3)]),[2,3]))/(length(find(G.ms==0))+sum(G.vol_frac0));
# hom_stress1 = (sum(squeeze(stress(:,:,find(G.ms==1))),2) + sum(stress1.*reshape((1-G.vol_frac0),[1,1,size(stress1,3)]),[2,3]))/(length(find(G.ms==1))+sum(1-G.vol_frac0));