import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo
import LsPrePost

execute_command('recordorient off')
execute_command('mesh off')
execute_command('genselect clear')
execute_command('assembly del all 1')
execute_command('model remove 1')
execute_command('home')
execute_command('ac')

substrate_length, substrate_width, substrate_height = 50, 20, 10
bead_width, bead_height, bead_depth = 2, 0.8, 0.5
bead_spacing = 2
number_of_beads = 5

part_length = 5
number_of_elements_per_part = 2

number_of_parts = int((substrate_length - 2 * part_length) / part_length / 2)
bead_depth = substrate_height - bead_depth
bead_height = substrate_height + bead_height
bead_starting_point = (substrate_width - number_of_beads * bead_width - (number_of_beads - 1) * bead_spacing) / 2

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
def gen_bead(starting_pont, width, h0, h_top, h_bottom, space):
    execute_command(f'pnt param 0.0 {starting_pont} {h0}')
    p_left = dc.get_data('largest_vertex_id')
    execute_command(f'pnt param 0.0 {starting_pont+width} {h0}')
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
    return [p_left, p_right, p_top, p_bottom], [surface_bottom, surface_top], arc_bottom, starting_pont + width + space

# generate all beads
bead_points = []
bead_surfaces = []
bead_arc_bottom = []
end = bead_starting_point
bead_mdpoint_flex = bead_starting_point + bead_width/2
mid_point_bead_section = [0]*number_of_beads

for i in range (number_of_beads):
    mid_point_bead_section[i] = bead_mdpoint_flex 
    bead_mdpoint_flex = bead_mdpoint_flex + bead_width + bead_spacing
    
for i in range(number_of_beads):
    bead_i_points, bead_i_surfaces, arc_bottom, end = gen_bead(end, bead_width, substrate_height, bead_height, bead_depth,
        bead_spacing)
    bead_points.append(bead_i_points)
    bead_arc_bottom.append(arc_bottom)
    bead_surfaces.extend(bead_i_surfaces)

# generate substrate section: lines and surface
lines = ''
execute_command(f'line pntpnt  0 0 2 {p_north_west}v {p_south_west}')
lines += str(dc.get_data('largest_edge_id')) + 'e '
execute_command(f'line pntpnt  0 0 2 {p_south_west}v {p_south_east}')
lines += str(dc.get_data('largest_edge_id')) + ' '
execute_command(f'line pntpnt  0 0 2 {p_south_east}v {p_north_east}')
lines += str(dc.get_data('largest_edge_id')) + ' '
for arc_bottom in bead_arc_bottom:
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
for surface in [*bead_surfaces, substrate_surface]:
    execute_command(f'genselect target occobject')
    execute_command(f'occfilter clear')
    execute_command(f'occfilter add Face')
    execute_command(f'genselect occobject add occobject  {surface}f')
    execute_command(f'occmesh mesh 0, 1 0 1 0.4 0 0')
    execute_command(f'occmesh accept 1 0.0001 10 1')
    execute_command(f'genselect clear')
    execute_command(f'occfilter clear')

# generate solid elements from surface meshes
solid_parts_plus = []
solid_parts_minus = []
for surface in [*bead_surfaces, substrate_surface]:
    for n_x in [1, -1]:
        execute_command(f'genselect target segment')
        execute_command(f'genselect element add part {surface}/0')
        part_id = dc.get_data('num_validparts') + 1
        elem_id = dc.get_data('largest_element_id') + 1
        execute_command(
            f'elgenerate solid solidfacedrag {part_id} {elem_id} {part_length} {number_of_elements_per_part} 0 0 0 {n_x} 0 0')
        execute_command(f'genselect clear')
        execute_command(f'elgenerate accept')
        if n_x == 1:
            solid_parts_plus.append(part_id)
        else:
            solid_parts_minus.append(part_id)

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
for solid_part_minus, solid_part_plus in zip(solid_parts_minus, solid_parts_plus):
    for i in range(1, number_of_parts):
        gen_copies(solid_part_minus, -i * part_length)
        gen_copies(solid_part_plus, i * part_length)
# generate sides of substrate
for solid_part_minus, solid_part_plus in zip(solid_parts_minus[0:-1:2], solid_parts_plus[0:-1:2]):
    gen_copies(solid_part_minus, -number_of_parts * part_length)
    gen_copies(solid_part_plus, number_of_parts * part_length)
gen_copies(solid_parts_minus[-1], -number_of_parts * part_length)
gen_copies(solid_parts_plus[-1], number_of_parts * part_length)

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

# TODO: improve using element nodal coordinates + smallest element size
#execute_command(
#    f'genselect solid add box in {substrate_length/2+1} {substrate_width+1} {substrate_height+1} #{substrate_length/2-part_length/number_of_elements_per_part-0.1} {substrate_width-0.4} {substrate_height-0.4}'
#)
num_selected = dc.get_data("num_selection")
element_ids = dc.get_data("selection_ids", type=Type.SOLID)
element_id = int(element_ids[0])

# LOOP TO CREATE SET OF NODES FOR TRAJECTORIES
for hh in range(number_of_beads):
    applied_midpoint = mid_point_bead_section[hh]
    execute_command('setnode')
    execute_command('genselect target node')
    execute_command('genselect clear')
    execute_command('genselect clear')
    execute_command('ident echo off')
    execute_command(f'genselect node add circle2 in -20 {applied_midpoint} 10 0.1 1 0 0 40')
    execute_command(f'setnode createset {hh+1} 1 0 0 0 0 "traj"')
    execute_command('genselect clear')
    
#BLOCK OF CODE TO CREATE SET FOR INITIAL CONDITION

execute_command('setnode')
execute_command('genselect target node')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
execute_command(f'genselect node add circle2 in -25 10 10 20 1 0 0 100')
execute_command(f'setnode createset {7} 1 0 0 0 0 "traj"')
execute_command('genselect clear')

#BLOCK OF CODE TO CREATE SEGMENT SET FOR BOUNDARY CONDITIONS
execute_command('setsegment')
execute_command('genselect target segment')
execute_command('genselect clear')
execute_command('genselect clear')
execute_command('ident echo off')
#execute_command('genselect segment add box out -24.900000 0.100000 0.100000 24.900000 19.900000 9.900000')
execute_command('genselect whole')
execute_command('genselect segment remove box in -24.900000 0.100000 0.100000 24.900000 19.900000 9.900000')
execute_command('setsegment createset 1 1 0 0 0 0 "outside_segments"')
execute_command('genselect clear')

#BLOCK OF CODE TO CREATE THERMAL MATERIAL FOR SUBSTRATE

execute_command(f'keyword input {1}')
#execute_command(char* MAT_THERMAL_ISOTROPIC)
#$#    tmid       tro     tgrlc    tgmult      tlat      hlat    
#         1    1000.0       0.0       0.0       0.0       0.0
#$#      hc        tc  
#      0.01    2200.0
#execute_command(char* END)
#execute_command('keyword updatekind')
#execute_command('MAT_THERMAL_ISOTROPIC')

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
execute_command('save keyword "MESH1.k"')
# execute_command('open keyword "temp_model.key"')
