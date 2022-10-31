import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo
import LsPrePost
import numpy as np
import json 
from math import sqrt

def write_keyfile(input_dictionary, output_file):
    with open(output_file, 'w') as file:
        for key, val in input_dictionary.items():
            if 'del' in key:
                key = key.split('_del', 1)[0]
            # print(key)
            file.write(key + '\n')
            for line in val:
                output_line =''.join([f'{li:},' for li in line])[:-1]
                # print(output_line)
                file.write(output_line + '\n')

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def vector_to_list(vec):
    # from a fortran vector to a list
    return [int(vec[j]) for j in range(len(vec))]
    
# generate bead: points, arcs, surfaces
def gen_bead(starting_pont, width, h_mid, h_top, h_bottom):
    execute_command(f'pnt param 0.0 {starting_pont} {h_mid}')
    p_left = dc.get_data('largest_vertex_id')
    execute_command(f'pnt param 0.0 {starting_pont+width} {h_mid}')
    p_right = dc.get_data('largest_vertex_id')
    execute_command(f'pnt param 0.0 {starting_pont+width/2} {h_top}')
    p_top = dc.get_data('largest_vertex_id')
    execute_command(f'pnt param 0.0 {starting_pont+width/2} {h_bottom}')
    p_bottom = dc.get_data('largest_vertex_id')

    # create line: number of points, point numbers (#v: vetrex)
    execute_command(f'line pntpnt  0 0 2 {p_left}v {p_right}')
    mid_line = dc.get_data('largest_edge_id')
    # create arc
    execute_command(f'cirarc 3pnts  {p_left}v {p_bottom} {p_right}')
    arc_bottom = dc.get_data('largest_edge_id')
    execute_command(f'cirarc 3pnts  {p_left}v {p_top} {p_right}')
    arc_top = dc.get_data('largest_edge_id')

    # create surface (n-side surface), order doesn't matter
    execute_command(f'nsurf 0 0 0 0 {mid_line}e {arc_bottom}')
    surface_bottom = dc.get_data('largest_surface_id')
    execute_command(f'nsurf 0 0 0 0 {mid_line}e {arc_top}')
    surface_top = dc.get_data('largest_surface_id')
    
    return [p_left, p_right, p_top, p_bottom], [surface_bottom, surface_top], arc_bottom

def gen_copies(part, space,n_parts_per_section):
    part_id = dc.get_data('num_validparts') + n_parts_per_section + 1
    elem_id = dc.get_data('largest_element_id') + 1
    node_id = dc.get_data('largest_node_id') + 1
    execute_command(f'genselect target node')
    execute_command(f'genselect transfer 0')
    execute_command(f'genselect node add part {part}/0 ')
    execute_command(f'translate_model {space} 0 0 copy 1 {part_id}')
    execute_command(f'translate_model accept {part_id} {elem_id} {node_id}')
    execute_command(f'genselect clear')

def create_node_set(x0,y0,z0,x1,y1,z1,name,idx):
    execute_command('setnode')
    execute_command('genselect target node')
    execute_command('genselect clear')
    execute_command('genselect clear')
    execute_command('ident echo off')
    execute_command('genselect whole')
    execute_command(f'genselect node remove box in {x0} {y0} {z0} {x1} {y1} {z1}')
    execute_command(f'setnode createset {idx} 1 0 0 0 0 {name}')
    execute_command('genselect clear')

def create_segment_set(x0,y0,z0,x1,y1,z1,name,idx):
    execute_command('setsegment')
    execute_command('genselect target segment')
    execute_command('genselect clear')
    execute_command('genselect clear')
    execute_command('ident echo off')
    execute_command('genselect whole')
    execute_command(f'genselect segment remove box in {x0} {y0} {z0} {x1} {y1} {z1}')
    execute_command(f'setsegment createset {idx} 1 0 0 0 0 {name}')
    execute_command('genselect clear')
    
# https://stackoverflow.com/questions/52990094/calculate-circle-given-3-points-code-explanation
def findCircle(b,c,d):
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        raise RuntimeError('problem with the inputs to findCircle')

    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det
    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5

    # print(cx,cy,radius)
    return cx,cy,radius