import subprocess
import numpy as np
import pathlib as path
import re

dynaint = np.uint32  # TODO check these types
dynafloat = np.float64
direction = {'x': 1, 'y': 2, 'z': 3}
idx_max = 99999999
scheme_explicit = 0
scheme_implicit = 1
solver_linear = 1
solver_bfgs = 12

bc_periodic = 0
bc_displacement = 1
mesh_mathcing = 1
mesh_not_mathcing = 0

from enum import Enum


class dim(Enum):
    threeD = 3
    twoD = 2


class element3D(Enum):
    brick_constant_stress = 1
    brick_b_bar = 2
    tetra_constant_stress = 10
    tetra_10noded = 16


class element2D(Enum):
    tri_3noded_belytschko_Tsay = 2
    plane_stress = 12
    plane_strain = 13
    tri_6noded = 24


def update_keyword(fun_b):
    def fun_c(obj, *args, **kwargs):
        obj.data.pop('*end')
        output = fun_b(obj, *args, **kwargs)
        obj.data['*end'] = ''
        return output

    return fun_c


class dyna_file:
    def __init__(self):
        self.idx_sec = iter(range(1, idx_max))
        # idx_part = iter(np.unique(mesh['elements'][:, 1]))
        self.idx_part = iter(range(1, idx_max))
        self.idx_curve = iter(range(1, idx_max))
        self.idx_mat = iter(range(1, idx_max))
        self.idx_thermal_mat = iter(range(1, idx_max))

        self.data = {'*keyword': [], '*end': []}
        self.nodes = np.array([])
        self.elements = np.array([])
        self.parts = 0

    def update(self, data, nodes, elements, parts):
        self.data = data
        self.nodes = nodes
        self.elements = elements
        self.parts = parts
        return self

    def write_keyfiles(self, output_file):
        with open(output_file, 'w') as file:
            for key, val in self.data.items():
                print(key)
                file.write(key + '\n')
                for line in val:
                    # if key == '*node':
                    #     lin = line + (6 - len(line)) * ['']
                    #     print(oline := '{:>8}{:>16}{:>16}{:>16}{:>8}{:>8}'.format(*lin))
                    #     file.write(oline + '\n')
                    # elif key.startswith('*elem'):
                    #     print(oline := ''.join([f'{li:>8}' for li in line]))
                    #     file.write(oline + '\n')
                    # elif key.startswith('*DEFINE_CURVE'):
                    #     print(oline := ''.join([f'{li:},' for li in line])[:-1])  #TODO better implementation
                    #     file.write(oline + '\n')
                    # else:
                    #     print(oline := ''.join([f'{li:>10}' for li in line]))
                    #     file.write(oline + '\n')
                    print(oline := ''.join([f'{li:},' for li in line])[:-1])  #TODO better implementation // csv?
                    file.write(oline + '\n')
        return

    @update_keyword
    def add_section(self, element_type, thickness=0.5):
        sec_id = next(self.idx_sec)
        if isinstance(element_type, element3D):
            self.data[f'*section_solid ${sec_id}'] = [[sec_id, element_type.value]]
            dimension = dim.threeD
        else:
            self.data[f'*section_shell ${sec_id}'] = [[sec_id, element_type.value], [thickness]]
            dimension = dim.twoD
        return sec_id, dimension.value

    @update_keyword
    def add_implicit(self, solution_scheme, time_step, solver, displacement_rel_tol, energt_rel_tol, residual_rel_tol):

        key = self.data['*CONTROL_ACCURACY'] = list()
        key.append([1, '', '', 1])

        # activates the implicit solver
        key = self.data['*control_implicit_general'] = list()
        key.append([solution_scheme, time_step])

        key = self.data['*control_implicit_solution'] = list()
        key.append([solver, '', '', displacement_rel_tol, energt_rel_tol, residual_rel_tol])

        # *control_implicit_solver
        # here you can extract the stiffness and rhs [MTXDMP]
        # EMXDMP: Flag for dumping elemental stiffness and mass matrices

        # *control_implicit_auto
        # automatic time stepping

        # *control_implicit_termination
        # terminate when there is no change in displacement or low energy. This keyword provides the ability to specify such a
        # stopping criteria to terminate the simulation prior to ENDTIM.

        # arc length an line search may be activated here

    @update_keyword
    def add_output(self, output_time_step):
        self.data[f'*DATABASE_BINARY_D3PLOT '] = [[output_time_step]]

    @update_keyword
    def add_termination(self, endtime, nosol=False):
        self.data[f'*control_termination '] = [[endtime, '', '', '', '', nosol * 1]]

    @update_keyword
    def add_part(self, sec_id, mat_id=0, thermal_mat_id=0, part_id=0):
        part_id = next(self.idx_part)
        self.data[f'*part ${part_id}'] = [[], [part_id, sec_id, mat_id, '', '', '', '', thermal_mat_id]]
        return part_id

    @update_keyword
    def add_mat_mooney_rivlin(self, aa=1e-3, bb=0.49, cc=1000, dd=500):
        mat_id = next(self.idx_mat)
        self.data[f'*MAT_MOONEY-RIVLIN_RUBBER ${mat_id}'] = [[mat_id, aa, bb, cc, dd, 1], []]
        return mat_id

    @update_keyword
    def add_rve(self, rve_mesh, dimension, bc, mesh, time_step, endtime):
        curve_id = next(self.idx_curve)
        # https://www.lstc-cmmg.org/kw-rve
        # https://zeliangliu.com/project/4-rve/
        rve_input_strain = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # xx yy zz yz xz xy
        key = self.data['*RVE_ANALYSIS_FEM'] = list()
        key.append([rve_mesh])
        key.append([0, 1, curve_id, dimension, bc, mesh])
        key.append(rve_input_strain)
        self.data['*DATABASE_RVE'] = [[time_step]]
        self.data['*DEFINE_CURVE'] = [[curve_id], [0, 0], [endtime, 1]]

    def split_rve_bc(self, rve_mesh_with_include, bc_file, dimension):
        bc_obj = dyna_file()
        bc_obj.data = {
            '*keyword': [],
            '*boundary_prescribed_motion_node': self.data['*boundary_prescribed_motion_node'],
            '*end': []
        }
        self.data.pop('*rve_info')
        self.data.pop('*boundary_prescribed_motion_node')
        self.data.pop('*end')
        self.data['*include'].append([bc_file.name])
        # self.data['*boundary_spc_node'][0].extend([1,1,1])

        if dimension == dim.twoD.value:
            # quad elements: *** Warning 60056 (IMP+56)
            #      *          8 Unconstrained degrees of freedom have
            self.data['*boundary_spc_node'].append([self.data['*node'][0][0], 0, 0, 0, 1, 1, 1, 1])
            self.data['*boundary_spc_node'].append([self.data['*node'][1][0], 0, 0, 0, 1, 1, 1, 1])

        self.data['*end'] = ''
        self.write_keyfiles(rve_mesh_with_include)
        bc_obj.write_keyfiles(bc_file)
        return bc_obj

    def update_rve_bc(self, strain, dimension,rve_length):
        if dimension == dim.threeD.value:
            for xx in range(6):
                self.data['*boundary_prescribed_motion_node'][xx][-1] = [
                    rve_length * strain[i] if strain[i] > 0 else 0.1e-15 for i in [0, 5, 4, 1, 3, 2]
                ][xx]
        else:
            for xx in range(3):
                self.data['*boundary_prescribed_motion_node'][xx][-1] = [
                    rve_length * strain[i] if strain[i] > 0 else 0.1e-15 for i in [0, 5, 1]
                ][xx]
        return

    def clean_rve(self, filename):
        self.data.pop('*RVE_ANALYSIS_FEM')
        self.data.pop('*DATABASE_RVE')
        self.data.pop('*end')
        self.data['*include'] = [[filename]]
        self.data['*end'] = ''


def clean():
    # TODO should ignore .git
    # [x.unlink() for x in path.Path().rglob('lspost*')]
    # [x.unlink() for x in path.Path().rglob('d3*')]
    # [x.unlink() for x in path.Path().rglob('messag')]
    # [x.unlink() for x in path.Path().rglob('bndout')]
    # [x.unlink() for x in path.Path().rglob('rveout')]
    # [x.unlink() for x in path.Path().rglob('adptmp')]
    # [x.unlink() for x in path.Path().rglob('bg_switch')]
    # [x.unlink() for x in path.Path().rglob('dyna.lsda')]
    # [x.unlink() for x in path.Path().rglob('kill_by_pid')]
    return


def convert_format():
    # TODO: if key == '*node %':
    #     subprocess.call([dyna_path, f'i={input_file_i10}', 'newformat=i10'])
    #     subprocess.call(['mv', f'{input_file_i10}.i10', outfile := f'{input_file_i10.split(".")[0]}_i10.k'])
    raise NotImplementedError(f'please convert input file to the old format [i8 instead of i10]')


def read_meshfiles(input_file_i10):
    data = dict()
    counter = 0
    found_node = False
    found_element = False
    with open(input_file_i10) as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.startswith('*'):
                key = line.lower().rstrip()
                if key.endswith('%'):
                    key = key[:-1]
                if key == '*keyword i10=y':
                    key = '*keyword'
                # TODO: check '*keyword long=y' ?
                if key not in data.keys():
                    data[key] = list()
                else:
                    key += f' ${counter}'
                    data[key] = list()
                    counter += 1
                if key.startswith('*node'):
                    if not found_node:
                        node_key = key
                        found_node = True
                    else:
                        raise NotImplementedError('node keyword appeared more than once')
                if key.startswith('*elem'):
                    if not found_element:
                        element_key = key
                        found_element = True
                    else:
                        raise NotImplementedError('elem keyword appeared more than once')
            elif not line.startswith('$'):
                # data[key].append(line.rstrip().split())
                data[key].append(re.split(r'[;,\s]\s*', line.rstrip().lstrip()))

    nodes = np.array([])
    elements = np.array([])
    parts = 0
    if found_node and found_element:
        nodes = np.asarray(data[node_key], dtype=dynafloat)
        if element_key.startswith('*element_solid'):
            elements = np.hstack((np.asarray(data[element_key][0::2],
                                             dtype=dynaint), np.asarray(data[element_key][1::2], dtype=dynaint)))
        else:
            elements = np.asarray(data[element_key], dtype=dynaint)
        parts = np.unique(elements[:, 1])

    try:
        data.pop('*part')
    except:
        pass

    return dyna_file().update(data, nodes, elements, parts)


def write_line(line):
    print(''.join([f'{li:>10}' for li in line]))


def write_node_bc(nodes, dir, idx, output_keyword):
    node_bc = list()
    node_id = np.asarray(nodes[nodes[:, direction[dir]] == 0, 0], dtype=dynaint)
    ss = np.array_split(np.pad(node_id, (0, 8 - len(node_id) % 8), 'constant'), 4)

    node_bc.append([next(idx), 0.0, 0.0, 0.0, 0.0, 'mech      ', '', ''])
    for s in ss:
        node_bc.append(list(s))

    output_keyword['*set_node_list'] = node_bc

    return output_keyword


def write_segment_bc(nodes, elements, dir, idx, output_keyword):
    node_id = np.asarray(nodes[nodes[:, direction[dir]] == 0, 0], dtype=dynaint)
    seg = list()
    seg.append([next(idx), 0.0, 0.0, 0.0, 0.0, 'mech      ', '', ''])

    free_dir = [kk for kk in direction.keys() if kk != dir]
    for el in elements[:, 2:]:
        if new_seg := [x for x in el if x in node_id]:
            x = nodes[new_seg, direction[free_dir[0]]]
            y = nodes[new_seg, direction[free_dir[1]]]
            x -= np.mean(x)
            y -= np.mean(y)
            seg.append([new_seg[i] for i in np.flip(np.argsort(np.arctan2(y, x)))] + [0.0, 0.0, 0.0, 0.0])

    output_keyword['*set_segment'] = seg

    return output_keyword


# TODO:
# user defined
# IHYPER=±10 on *MAT_USER_DE-
# FINED_MATERIAL_MODELS will also invoke full integration of solid form 2
