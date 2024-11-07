import subprocess
import pathlib as path
import dyna_writer as dy
import numpy as np
from pathlib import Path as path
import shutil
import copy


def run_shell(command):
    """
    This is a function.

    Parameters
    ----------
    arg1 : array
        The coordinates of ...
    arg2 : int
        The dimension ...

    Returns
    -------
    out : array
       The resulting array of shape ....
    """
    r"""
    This is a function with :math:`\mbox{\LaTeX}` math:
    :math:`\frac{1}{\pi}`.
    """
    # https://stackoverflow.com/questions/12060863/python-subprocess-call-a-bash-alias
    # subprocess.call(command, shell=True)
    subprocess.call(['/bin/bash', '-i', '-c', command])


dyna_path = '~/.dontsync/packages/lsdyna/lsdyna'

key_files_folder = 'key_files/'
output_mesh = path(key_files_folder + 'tmp_out_mesh.k')
rve_input_file = path(key_files_folder + 'tmp_input.k')
rve_mesh_with_bc = path(key_files_folder + 'rve_' + output_mesh.name)
rve_mesh_with_include = path(key_files_folder + 'rve_include' + output_mesh.name)
gp_input_mesh = path(key_files_folder + 'tmp_gp_input.k')
bc_file = path(key_files_folder + 'tmp_bc_file.k')

dy.clean()

rve_input_obj = dy.dyna_file()
rve_length = 25e-6
input_mesh = path(key_files_folder + 'raw_mesh_2d_0_tri_lin.k')
sec_id, dimension = rve_input_obj.add_section(element_type=dy.element2D.tri_3noded_belytschko_Tsay)

dfile = dy.read_meshfiles(input_mesh)
dfile.write_keyfiles(output_mesh)
# run_shell(f'meld {input_mesh} {output_mesh}')

# %%
time_step = 0.1
endtime = 1
output_time_step = 0.1
dtol = etol = rtol = 1e-5
rve_input_obj.add_termination(endtime=endtime)
rve_input_obj.add_output(output_time_step=output_time_step)

mat_id = rve_input_obj.add_mat_mooney_rivlin(1e-3, 0.49, 500, 100)
rve_input_obj.add_part(sec_id, mat_id)

mat_id = rve_input_obj.add_mat_mooney_rivlin(1e-3, 0.49, 100, 50)
rve_input_obj.add_part(sec_id, mat_id)

rve_input_obj.add_implicit(solution_scheme=dy.scheme_implicit, time_step=time_step, solver=dy.solver_bfgs,
                           displacement_rel_tol=dtol, energt_rel_tol=etol, residual_rel_tol=rtol)

rve_input_obj.add_rve(output_mesh.name, dimension=dimension, bc=dy.bc_periodic, mesh=dy.mesh_mathcing, time_step=time_step,
                      endtime=endtime)

rve_input_obj.write_keyfiles(rve_input_file)
run_shell(f' cd {rve_input_file.parent} && lsdyna i={rve_input_file.name} mcheck=y')

# %%
dfile = dy.read_meshfiles(rve_mesh_with_bc)
bc_obj = dfile.split_rve_bc(rve_mesh_with_include, bc_file, dimension)

rve_input_final_obj = rve_input_obj
rve_input_final_obj.clean_rve(rve_mesh_with_include.name)
rve_input_final_obj.write_keyfiles(gp_input_mesh)

# %%
dy.clean()
sim_folders = [path('output_simulation/1'), path('output_simulation/2')]
strains = [[0.1, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.1]]  # xx yy zz yz xz xy
# TODO what is prescribed is displacement not stain [check]
for sim_folder, strain in zip(sim_folders, strains):
    sim_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(gp_input_mesh, sim_folder)
    shutil.copy(rve_mesh_with_include, sim_folder)
    shutil.copy(output_mesh, sim_folder)
    shutil.copy(bc_file, sim_folder)

    newbc = copy.deepcopy(bc_obj)
    newbc.update_rve_bc(strain, dimension, rve_length)
    newbc.write_keyfiles(sim_folder.joinpath(bc_file.name))

    run_shell(f'cd {sim_folder} && lsdyna i={gp_input_mesh.name} ncpu=8')

# TODO: improve reading files with ['1,1'] e.g. mesh = dy.read_meshfiles(dyna_path, gp_input_mesh)
