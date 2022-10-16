""" build a substrate of any dimension with given number of weld beads.
Each bead is divided into sections that are activated in a sequenctial order.
Separate sets are extracted for boundary nodes and segements to be used for BC specification.

A set of elements is extracted for all the lower bead parts, these elements are always active but their response will
 change from single phase to composite when the temperature is high.
 
Other sets of elements are extracted for each top bead sections, these sets will be activated based on time.
"""

import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo
import LsPrePost
import numpy as np
import json 
from math import sqrt


execute_command('recordorient off')
execute_command('mesh off')
execute_command('genselect clear')
execute_command('assembly del all 1')
execute_command('model remove 1')
execute_command('home')
execute_command('ac')

substrate_length, substrate_width, substrate_height = 15, 20, 10
shift = 0.01 # small number used for node selection // should be smaller than element size
bead_width, bead_h, bead_d = 2, 0.8, 0.5
bead_spacing = 2
number_of_beads = 3

part_length = 5
number_of_elements_per_part = 5

assert(substrate_length >= 2*part_length)
assert(substrate_width - number_of_beads * bead_width - (number_of_beads - 1) * bead_spacing > 0)
assert(bead_h < 1)
assert(bead_d < 1)

number_of_parts = int(substrate_length / part_length)
bead_depth = substrate_height - bead_d
bead_height = substrate_height + bead_h
bead_starting_point = (substrate_width - number_of_beads * bead_width - (number_of_beads - 1) * bead_spacing) / 2

min_x = -part_length
max_x = substrate_length + part_length

# welding parameters
weld_velocity = 5
weld_time_bead = substrate_length/weld_velocity
weld_time_part = weld_time_bead/number_of_parts
time_between_deposition = 20
activation_time = []
parts_dictionary = {}

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
    
# substrate corner points
execute_command(f'pnt param 0.0 0.0 0.0')
p_south_west = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 {substrate_width} 0.0')
p_south_east = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 {substrate_width} {substrate_height}')
p_north_east = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 0.0 {substrate_height}')
p_north_west = dc.get_data('largest_vertex_id')

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

# generate all beads
bead_points = []
bead_surfaces = []
bead_arc_bottoms = []
starting_point = bead_starting_point
midpoint = starting_point + bead_width/2
bead_start_points = [0]*number_of_beads
bead_mid_points = [0]*number_of_beads

for i in range(number_of_beads):
    bead_mid_points[i] = midpoint
    bead_start_points[i] = starting_point

    bead_i_points, bead_i_surfaces, bead_i_bottom = gen_bead(starting_point, bead_width, substrate_height, bead_height, bead_depth)
    bead_points.append(bead_i_points)
    bead_surfaces.extend(bead_i_surfaces)
    bead_arc_bottoms.append(bead_i_bottom)

    midpoint += bead_width + bead_spacing
    starting_point += bead_width + bead_spacing
    
# generate substrate section: lines and surface
lines = ''
execute_command(f'line pntpnt  0 0 2 {p_north_west}v {p_south_west}')
lines += str(dc.get_data('largest_edge_id')) + 'e '
execute_command(f'line pntpnt  0 0 2 {p_south_west}v {p_south_east}')
lines += str(dc.get_data('largest_edge_id')) + ' '
execute_command(f'line pntpnt  0 0 2 {p_south_east}v {p_north_east}')
lines += str(dc.get_data('largest_edge_id')) + ' '
for arc_bottom in bead_arc_bottoms:
    lines += str(arc_bottom) + ' '
execute_command(f'line pntpnt  0 0 2 {p_north_west}v {bead_points[0][0]}')
lines += str(dc.get_data('largest_edge_id')) + ' '
execute_command(f'line pntpnt  0 0 2 {bead_points[-1][1]}v {p_north_east}')
lines += str(dc.get_data('largest_edge_id')) + ' '
for i in range(number_of_beads - 1):
    execute_command(f'line pntpnt  0 0 2 {bead_points[i][1]}v {bead_points[i+1][0]}')
    lines += str(dc.get_data('largest_edge_id')) + ' '

execute_command(f'nsurf 0 0 0 0 {lines}')
substrate_surface = dc.get_data('largest_surface_id')

# mesh all surfaces
for surface in bead_surfaces:
    execute_command(f'genselect target occobject')
    execute_command(f'occfilter clear')
    execute_command(f'occfilter add Face')
    execute_command(f'genselect occobject add occobject  {surface}f')
    execute_command(f'occmesh mesh 13, 1 0.05 {bead_width/10} 0.1 20 0 0')
    # execute_command(f'occmesh remesh 33 10')
    execute_command(f'occmesh accept 1 0.0001 3 1')
    execute_command(f'genselect clear')
    execute_command(f'occfilter clear')
    
execute_command(f'genselect target occobject')
execute_command(f'occfilter clear')
execute_command(f'occfilter add Face')
execute_command(f'genselect occobject add occobject  {substrate_surface}f')
execute_command(f'occmesh mesh 13, 1 0.05 {substrate_width/15} 0.1 20 0 0')
execute_command(f'occmesh accept 1 0.0001 3 1')
execute_command(f'genselect clear')
execute_command(f'occfilter clear')


# generate solid elements from surface meshes
solid_parts = []
for surface in [substrate_surface,*bead_surfaces]:
    execute_command(f'genselect target segment')
    execute_command(f'genselect element add part {surface}/0')
    part_id = dc.get_data('num_validparts') + 1
    elem_id = dc.get_data('largest_element_id') + 1
    normal_x = 1
    execute_command(f'elgenerate solid solidfacedrag {part_id} {elem_id} {part_length} {number_of_elements_per_part} 0 0 0 {normal_x} 0 0')
    execute_command(f'genselect clear')
    execute_command(f'elgenerate accept')
    solid_parts.append(part_id)
substrate_part = solid_parts[0]
bottom_parts = solid_parts[1::2]
top_parts = solid_parts[2::2]

# delete shell elements
execute_command('delelement unrefn 1')
execute_command('delelement target element')
execute_command('delelement target element')
execute_command('elemcheck clear')
execute_command('delelement target shell')
execute_command('delelement clean 1')
execute_command('genselect whole')
execute_command('delelement delete')
execute_command('delelement accept')
execute_command('genselect clear')
execute_command('elemcheck clear')

def gen_copies(part, space):
    part_id = dc.get_data('num_validparts') + len(bead_surfaces) + 1 + 1 # 1 corresponds to the substrate surface
    elem_id = dc.get_data('largest_element_id') + 1
    node_id = dc.get_data('largest_node_id') + 1
    execute_command(f'genselect target node')
    execute_command(f'genselect transfer 0')
    execute_command(f'genselect node add part {part}/0 ')
    execute_command(f'translate_model {space} 0 0 copy 1 {part_id}')
    execute_command(f'translate_model accept {part_id} {elem_id} {node_id}')
    execute_command(f'genselect clear')

# generate copies of solid parts
for i in range(1, number_of_parts):
    for solid_part_plus in solid_parts:
        gen_copies(solid_part_plus, i * part_length)
# generate extra sides of substrate
for solid_part in [substrate_part,*bottom_parts]:
    gen_copies(solid_part, -part_length)
    gen_copies(solid_part, number_of_parts * part_length)

all_substrate_parts = np.stack([substrate_part+i*(number_of_beads*2+1) for i in range(number_of_parts)]).T.flatten()
all_bottom_parts = np.stack([np.asarray(bottom_parts)+i*(number_of_beads*2+1) for i in range(number_of_parts)]).T.flatten()
all_top_parts = np.stack([np.asarray(top_parts)+i*(number_of_beads*2+1) for i in range(number_of_parts)]).T.flatten()

# delete duplicate nodes
execute_command('genselect target node')
execute_command('dupnode open 1')
execute_command('dupnode showdup 0.004000')
execute_command('dupnode merge 0.004000')
execute_command('genselect clear')

execute_command('genselect clear all')
execute_command('ident select 1')
execute_command('genselect target solid')
execute_command('ident echo off')

set_id = 0

# create sets of nodes
set_id = set_id + 1
execute_command('setnode')
execute_command('genselect target node')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command(f'genselect whole')
execute_command(f'setnode createset {set_id} 1 0 0 0 0 "whole"')
execute_command('genselect clear')

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

set_id = set_id + 1
# create_node_set(min_x+shift,shift,shift,max_x-shift,substrate_width-shift,substrate_height-shift,"outside_nodes",set_id)
execute_command('setnode')
execute_command('genselect target node')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command('genselect whole')
execute_command(f'genselect node remove box in {min_x+shift},{shift},{shift},{max_x-shift},{substrate_width-shift},{substrate_height-shift}')
for bead_idx in range(number_of_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect node remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setnode createset {set_id} 1 0 0 0 0 {"outside_nodessss"}')
execute_command('genselect clear')
set_id = set_id + 1
create_node_set(min_x+shift,-shift,-shift,max_x+shift,substrate_width+shift,bead_height+shift,"x-",set_id)
set_id = set_id + 1
create_node_set(min_x-shift,-shift,-shift,max_x-shift,substrate_width+shift,bead_height+shift,"x+",set_id)
set_id = set_id + 1
create_node_set(min_x-shift,shift,-shift,max_x+shift,substrate_width+shift,bead_height+shift,"y-",set_id)
set_id = set_id + 1
create_node_set(min_x-shift,-shift,-shift,max_x+shift,substrate_width-shift,bead_height+shift,"y+",set_id)
set_id = set_id + 1
create_node_set(min_x-shift,-shift,shift,max_x+shift,substrate_width+shift,bead_height+shift,"z-",set_id)
set_id = set_id + 1
# create_node_set(min_x-shift,-shift,-shift,max_x+shift,substrate_width+shift,substrate_height-shift,"z+",set_id)
execute_command('setnode')
execute_command('genselect target node')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command('genselect whole')
execute_command(f'genselect node remove box in {min_x-shift},{-shift},{-shift},{max_x+shift},{substrate_width+shift},{substrate_height-shift}')
for bead_idx in range(number_of_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect node remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setnode createset {set_id} 1 0 0 0 0 {"z+"}')
execute_command('genselect clear')

# LOOP TO CREATE SET OF NODES FOR TRAJECTORIES
set_id = 9
for bead_idx in range(number_of_beads):
    set_id = set_id + 1
    midpoint_y = bead_mid_points[bead_idx]
    execute_command('setnode')
    execute_command('genselect target node')
    execute_command('genselect clear')
    execute_command('genselect clear')
    execute_command('ident echo off')
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect node add circle2 in 0 {midpoint_y} {bead_height} {shift} 1 0 0 {substrate_length}')
    execute_command(f'setnode createset {set_id} 1 0 0 0 0 "traj{bead_idx}"')
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

set_id = 1
execute_command('setnode')
execute_command('genselect target segment')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command(f'genselect whole')
execute_command(f'setsegment createset {set_id} 1 0 0 0 0 "whole"')
execute_command('genselect clear')

set_id = set_id + 1
# create_segment_set(min_x+shift,shift,shift,max_x-shift,substrate_width-shift,substrate_height-shift,"outside_segments",set_id)
execute_command('setsegment')
execute_command('genselect target segment')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command('genselect whole')
execute_command(f'genselect segment remove box in {min_x+shift},{shift},{shift},{max_x-shift},{substrate_width-shift},{substrate_height-shift}')
for bead_idx in range(number_of_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect segment remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setsegment createset {set_id} 1 0 0 0 0 {"outside_segments"}')
execute_command('genselect clear')
set_id = set_id + 1
create_segment_set(min_x+shift,-shift,-shift,max_x+shift,substrate_width+shift,bead_height+shift,"x-",set_id)
set_id = set_id + 1
create_segment_set(min_x-shift,-shift,-shift,max_x-shift,substrate_width+shift,bead_height+shift,"x+",set_id)
set_id = set_id + 1
create_segment_set(min_x-shift,shift,-shift,max_x+shift,substrate_width+shift,bead_height+shift,"y-",set_id)
set_id = set_id + 1
create_segment_set(min_x-shift,-shift,-shift,max_x+shift,substrate_width-shift,bead_height+shift,"y+",set_id)
set_id = set_id + 1
create_segment_set(min_x-shift,-shift,shift,max_x+shift,substrate_width+shift,bead_height+shift,"z-",set_id)
set_id = set_id + 1
# create_segment_set(min_x-shift,-shift,-shift,max_x+shift,substrate_width+shift,substrate_height-shift,"z+",set_id)
execute_command('setsegment')
execute_command('genselect target segment')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command('genselect whole')
execute_command(f'genselect segment remove box in {min_x-shift},{-shift},{-shift},{max_x+shift},{substrate_width+shift},{substrate_height-shift}')
for bead_idx in range(number_of_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect segment remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setsegment createset {set_id} 1 0 0 0 0 {"z+"}')
execute_command('genselect clear')

def vector_to_list(vec):
    # from a fortran vector to a list
    return [int(vec[j]) for j in range(len(vec))]
    
    
all_other_parts = []
execute_command('setpart')
execute_command('genselect target part')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('genselect whole')
execute_command(f'genselect part remove box in {0} {bead_start_points[0]} {bead_depth} {substrate_length} {bead_start_points[-1]+bead_width} {bead_height}')
# execute_command(f'setpart createset {55} 1 0 0 0 0')
# execute_command('genselect clear')
# parts_bead_id = dc.get_data('ids_inset',type=Type.PART, id = int(55))
parts_bead_id = dc.get_data('selection_ids',type=Type.PART)
all_other_parts = vector_to_list(parts_bead_id)

execute_command('genselect clear')
execute_command(f'genselect target element')
for part in all_bottom_parts:
    execute_command(f'genselect element add part {part}/0 ')
element_ids = dc.get_data("selection_ids", type=Type.SOLID)
parts_dictionary['bottom_element_ids'] = vector_to_list(element_ids)

for part in all_top_parts:
    execute_command('genselect clear')
    execute_command(f'genselect target element')
    execute_command(f'genselect element add part {part}/0 ')
    element_ids = dc.get_data("selection_ids", type=Type.SOLID)
    parts_dictionary[f'top_{part}_element_ids'] = vector_to_list(element_ids)

parts_dictionary['all_top_parts'] = all_top_parts
parts_dictionary['all_bottom_parts'] = all_bottom_parts
parts_dictionary['all_substrate_parts'] = all_substrate_parts
parts_dictionary['all_other_parts'] = all_other_parts

def write_keyfile(dict, output_file):
    with open(output_file, 'w') as file:
        for key, val in dict.items():
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

dumped = json.dumps(parts_dictionary, cls=NumpyEncoder, separators=(',', ':'), sort_keys=True)
# dumped = json.dumps(parts_dictionary, cls=NumpyEncoder, separators=(',', ':'), sort_keys=True, indent=4)
# print(dumped)

with open("info.json", "w") as f:
    json.dump(dumped, f)

keyword_dictionary = {}
sec_id = 0
mat_id = 0
thermal_mat_id = 0
for part_id in [*all_top_parts,*all_bottom_parts,*all_substrate_parts,*all_other_parts]:
    keyword_dictionary[f'*part ${part_id}'] = [[], [part_id, sec_id, mat_id, '', '', '', '', thermal_mat_id]]
write_keyfile(keyword_dictionary, 'parts.k')


# view options
execute_command('assembly off shape 1')
execute_command('clearpick')
execute_command('selectentity None')

execute_command('home')
execute_command('ac')
execute_command('isometric x')
execute_command('mesh on')

# save keyword file
execute_command('save keywordabsolute 0')
execute_command('save keywordbylongfmt 0')
execute_command('save keywordbyi10fmt 0')
execute_command('save outversion 10')
execute_command('save keyword "mesh.k"')
execute_command('open keyword "mesh.k"')



# old parts
# for x in range(number_of_beads):
# 	for y in range(number_of_parts):
# 		RowList_activated_parts[counter] = sequential_list_of_activated_parts[x][y]
# 		counter = counter + 1
# 
# # card for each part cards
# for i in range(n_activated_parts):
# 	id_act_part = RowList_activated_parts[i]
# 	parts_dictionary[f'*MAT_THERMAL_CWM_TITLE $# {id_act_part}']=[]
# 	parts_dictionary[f'$# segment {id_act_part}'] = [[id_act_part, 8.93300E-6,0.0, 0.0, 0.0, 0.0,0.0,0.0],  [11, 12,0.0, 0.0, activation_time[i], activation_time[i]	+0.1,0.0,0.0]]                     
# 	#parts_dictionary[f'*end ${i}'] = []
# 
# sequential_list_of_activated_parts = []
# for i in range(number_of_beads):
#     start_point = bead_start_points[i]
#     execute_command('setpart')
#     execute_command('genselect target part')
#     execute_command('genselect clear')
#     execute_command('genselect clear')
#     execute_command(f'genselect part add box in 0.000000 {start_point} {substrate_height} {substrate_length} {start_point+bead_width+shift} {bead_height+shift}')
#     execute_command(f'setpart createset {i+1} 1 0 0 0 0')
#     execute_command('genselect clear')
#     parts_bead_id = dc.get_data('ids_inset',type=Type.PART, id = int(i+1))
#     sequential_list_of_activated_parts.append(vector_to_list(parts_bead_id))
# print(sequential_list_of_activated_parts)