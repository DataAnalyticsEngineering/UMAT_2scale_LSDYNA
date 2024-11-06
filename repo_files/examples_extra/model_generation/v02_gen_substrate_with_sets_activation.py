""" build a substrate of any dimension with given number of weld beads.
Each bead is divided into sections that are activated in a sequenctial order.
Separate sets are extracted for boundary nodes and segements to be used for BC specification.

A set of elements is extracted for all the lower bead parts, these elements are always active but their response will
 change from single phase to composite when the temperature is high.
 
Other sets of elements are extracted for each top bead sections, these sets will be activated based on time.

set_id: 1 all node/segments, 2 outer nodes/segments, 3 x-, 4 x+, 5 y-, ...
trajectory sets start with the id 10
"""

import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo
import LsPrePost
import numpy as np
import json 
from math import sqrt
from dyna_utils import *

execute_command('recordorient off')
execute_command('mesh off')
execute_command('genselect clear')
execute_command('assembly del all 1')
execute_command('model remove 1')
execute_command('home')
execute_command('ac')

substrate_length, substrate_width, substrate_height = 10, 20, 10
shift = 0.01 # small number used for node selection // should be smaller than element size
bead_width, bead_h, bead_d = 2, 0.8, 0.5
bead_spacing = 2
n_beads = 2

part_length = 5
n_elements_per_part = 2

# assert(substrate_length >= 2*part_length)
assert(substrate_width - n_beads * bead_width - (n_beads - 1) * bead_spacing > 0)
assert(bead_h < 1)
assert(bead_d < 1)

n_parts = int(substrate_length / part_length)

# welding parameters
initial_time = 1
heating_time = 4
cooling_time = 0.01
transition_time = 2
track_length = n_parts * part_length
laser_speed = 1.666666667
track_time = track_length / laser_speed

first_curve_id = 101
first_trajectory_id = 10

bead_depth = substrate_height - bead_d
bead_height = substrate_height + bead_h
bead_starting_point = (substrate_width - n_beads * bead_width - (n_beads - 1) * bead_spacing) / 2

min_x = -part_length
max_x = substrate_length + part_length
    
# substrate corner points
execute_command(f'pnt param 0.0 0.0 0.0')
p_south_west = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 {substrate_width} 0.0')
p_south_east = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 {substrate_width} {substrate_height}')
p_north_east = dc.get_data('largest_vertex_id')
execute_command(f'pnt param 0.0 0.0 {substrate_height}')
p_north_west = dc.get_data('largest_vertex_id')

# generate all beads
bead_points = []
bead_surfaces = []
bead_arc_bottoms = []
starting_point = bead_starting_point
midpoint = starting_point + bead_width/2
bead_start_points = [0]*n_beads
bead_mid_points = [0]*n_beads

for i in range(n_beads):
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
for i in range(n_beads - 1):
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
    execute_command(f'elgenerate solid solidfacedrag {part_id} {elem_id} {part_length} {n_elements_per_part} 0 0 0 {normal_x} 0 0')
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

n_parts_per_section = len(bead_surfaces) + 1 # 1 corresponds to the substrate surface
# generate copies of solid parts
for i in range(1, n_parts):
    for solid_part_plus in solid_parts:
        gen_copies(solid_part_plus, i * part_length,n_parts_per_section)
# generate extra sides of substrate
for solid_part in [substrate_part,*bottom_parts]:
    gen_copies(solid_part, -part_length,n_parts_per_section)
    gen_copies(solid_part, n_parts * part_length,n_parts_per_section)

all_substrate_parts = np.stack([substrate_part+i*(n_beads*2+1) for i in range(n_parts)]).T.flatten()
all_bottom_parts = np.stack([np.asarray(bottom_parts)+i*(n_beads*2+1) for i in range(n_parts)]).T.flatten()
all_top_parts = np.stack([np.asarray(top_parts)+i*(n_beads*2+1) for i in range(n_parts)]).T.flatten()

# delete duplicate nodes [the command has to be repeated twice with lspp4.9]
execute_command('genselect target node')
execute_command('dupnode open 1')
execute_command('dupnode showdup 0.004000')
execute_command('dupnode merge 0.004000')
execute_command('genselect clear')
execute_command('genselect target node')
execute_command('dupnode open 1')
execute_command('dupnode showdup 0.004000')
execute_command('dupnode merge 0.004000')
execute_command('genselect clear')

set_id = 0
# 1 all node, 2 outer node, 3 x-, 4 x+, 5 y-, ...
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

set_id = set_id + 1
# create_node_set(min_x+shift,shift,shift,max_x-shift,substrate_width-shift,substrate_height-shift,"outside_nodes",set_id)
execute_command('setnode')
execute_command('genselect target node')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command('genselect whole')
execute_command(f'genselect node remove box in {min_x+shift},{shift},{shift},{max_x-shift},{substrate_width-shift},{substrate_height-shift}')
for bead_idx in range(n_beads):
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
for bead_idx in range(n_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect node remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setnode createset {set_id} 1 0 0 0 0 {"z+"}')
execute_command('genselect clear')

# CREATE SET OF NODES FOR TRAJECTORIES
set_id = first_trajectory_id - 1
for bead_idx in range(n_beads):
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

# 1 all segments, 2 outer segments, 3 x-, 4 x+, 5 y-, ...
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
for bead_idx in range(n_beads):
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
for bead_idx in range(n_beads):
    p1 = (bead_start_points[bead_idx],substrate_height)
    p2 = (bead_mid_points[bead_idx],bead_height)
    p3 = (bead_start_points[bead_idx]+bead_width,substrate_height)
    cy,cz,rad = findCircle(p1,p2,p3)
    # center{x,y,z} radius normal{x,y,z} height
    execute_command(f'genselect segment remove circle2 in {shift} {cy} {cz} {rad-shift} 1 0 0 {substrate_length-2*shift}')
execute_command(f'setsegment createset {set_id} 1 0 0 0 0 {"z+"}')
execute_command('genselect clear')

# extract id of all side parts, these are the parts that are not directly affected by welding
all_side_parts = []
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
all_side_parts = vector_to_list(parts_bead_id)

# extract element id of all lower parts of the beads
info_dictionary = {}
execute_command('genselect clear')
execute_command(f'genselect target element')
for part in all_bottom_parts:
    execute_command(f'genselect element add part {part}/0 ')
element_ids = dc.get_data("selection_ids", type=Type.SOLID)
info_dictionary['bottom_element_ids'] = vector_to_list(element_ids)

# extract element id of all upper parts of the beads
for part in all_top_parts:
    execute_command('genselect clear')
    execute_command(f'genselect target element')
    execute_command(f'genselect element add part {part}/0 ')
    element_ids = dc.get_data("selection_ids", type=Type.SOLID)
    info_dictionary[f'top_{part}_element_ids'] = vector_to_list(element_ids)

info_dictionary['all_top_parts'] = all_top_parts
info_dictionary['all_bottom_parts'] = all_bottom_parts
info_dictionary['all_substrate_parts'] = all_substrate_parts
info_dictionary['all_side_parts'] = all_side_parts

top_parts_per_bead = []
for bead_idx in range(n_beads):
    top_parts_per_bead.append(all_top_parts[bead_idx*n_parts:bead_idx*n_parts+n_parts])
info_dictionary['top_parts_per_bead'] = top_parts_per_bead

dumped = json.dumps(info_dictionary, cls=NumpyEncoder, sort_keys=True)
# print(dumped)
with open("info.json", "w", encoding='utf-8') as f:
    json.dump(info_dictionary, f, cls=NumpyEncoder, sort_keys=True,ensure_ascii=False, indent=4)

# set material id for each part
parts_dictionary = {}
sec_id = 1
mat_id = 1
thermal_mat_id = 1
for part_id in [*all_top_parts,*all_bottom_parts,*all_substrate_parts,*all_side_parts]:
    parts_dictionary[f'*part ${part_id}'] = [[], [part_id, sec_id, mat_id, '', '', '', '', thermal_mat_id]]
write_keyfile(parts_dictionary, 'parts.k')

# generate curves of laser speed and energy
x_scaling_factor = 1.
y_scaling_factor = 1.
x_offset = 0.
y_offset = 0.
curves_dictionary = {'*keyword': []}
last_time_point = initial_time
curve_id = first_curve_id-1
for bead_idx in range(n_beads):
    # velocity curve
    curve_id+=1
    curves_dictionary[f'*DEFINE_CURVE_del{curve_id}'] = [[curve_id, 0, x_scaling_factor, y_scaling_factor, x_offset, y_offset],
                                                        *list([[0.0,0.0],
                                                        [last_time_point,0.0],
                                                        [last_time_point+heating_time,laser_speed],
                                                        [last_time_point+heating_time+track_time,laser_speed],
                                                        [last_time_point+heating_time+track_time+cooling_time,0.0],
                                                        [1000.0,0.0]])]
    # energy curve
    curve_id+=1
    curves_dictionary[f'*DEFINE_CURVE_del{curve_id}'] = [[curve_id, 0, x_scaling_factor, y_scaling_factor, x_offset, y_offset],
                                                        *list([[0.0,0.0],
                                                        [last_time_point,0.0],
                                                        [last_time_point+heating_time,1.0],
                                                        [last_time_point+heating_time+track_time,1.0],
                                                        [last_time_point+heating_time+track_time+cooling_time,0.0],
                                                        [1000.0,0.0]])]
    last_time_point = last_time_point+heating_time+track_time+cooling_time+transition_time
curves_dictionary['*end'] = []
write_keyfile(curves_dictionary, 'curves_trajectories.k')

# generate set of parts that will be used to configure BOUNDARY_THERMAL_WELD_TRAJECTORY
part_list_dictionary = {}
for bead_idx in range(n_beads):
    part_list = [*all_substrate_parts,*all_bottom_parts,*all_side_parts,*top_parts_per_bead[bead_idx]]
    part_list.extend(np.zeros(8-len(part_list)%8))
    part_list_dictionary[f'*SET_PART_LIST ${bead_idx+1}'] = [[bead_idx+1,0,0,0,0,'MECH'], *list(np.asarray(part_list,dtype=int).reshape(-1,8))]
write_keyfile(part_list_dictionary, 'part_list.k')
            
trajectories_dictionary = {}
for bead_idx in range(n_beads):
    trajectories_dictionary[f'*BOUNDARY_THERMAL_WELD_TRAJECTORY ${bead_idx+1}'] = [[bead_idx+1,2,first_trajectory_id+bead_idx,-(first_curve_id+bead_idx*2),0,0.0,5,0], [1 ,first_curve_id+bead_idx*2+1,'&power', 0, 0, 0],['&radius','&depth','&radius','&radius','&f_f','&f_r','&n',0.0],[0.0, 0.0,-1.0]]
write_keyfile(trajectories_dictionary, 'weld_trajectories.k')

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

# execute_command('genselect clear all')
# execute_command('ident select 1')
# execute_command('genselect target solid')
# execute_command('ident echo off')
