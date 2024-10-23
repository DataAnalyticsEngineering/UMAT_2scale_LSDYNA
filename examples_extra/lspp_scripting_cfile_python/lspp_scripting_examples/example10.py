# Example 10:
# Script to read a file that contains node coordinates which define the outline of a region.
# Then create a geometry surface from the outline, and then mesh it with shell element,
# drag the shell elements in the Z direction to form a solid block. 
# Delete the shell element part, and keep the solid part,
# Write the solid part to a file. 
# This example uses a lsprepost command file (example10.cfile) to call the SCL file, with the input file, 
# output file and a few parameters defined in the command file and pass them to the script
  
from LsPrePost import cmd_result_get_value_count, echo
from LsPrePost import cmd_result_get_value, execute_command
import sys

try:
    ret = cmd_result_get_value_count()
    if not ret:
        raise ValueError

    ''' arg1 node input file name 
        arg2 keyword output file name 
        arg3 2D shell mesh size 
        arg4 3D extrusion length 
        arg5 3D extrusion no. of elements
    '''
    input_name = cmd_result_get_value(0)
    output_name = cmd_result_get_value(1)
    meshsize = cmd_result_get_value(2)
    zlength = cmd_result_get_value(3)
    zelem = cmd_result_get_value(4)
    message = 'meshzie={}, zlength={}, zelem={}'.format(
        meshsize, zlength, zelem
    )
    echo(message)
    # read the input file and count no. of nodes
    f = open(input_name, 'r')
    nnode = 0
    while True:
        lines = f.readline()
        if not lines:
            break
        if lines[0] == '$' or lines[0] == '#' or lines[0] =='*':
            continue
        nnode += 1    
    f.close()
    echo('Number of nodes: {}'.format(nnode))
    cmd = 'open keyword {}'.format(input_name)
    execute_command(cmd)
    execute_command('save keywordoutversion 9')
    execute_command('genselect target occobject')
    execute_command('occfilter clear')
    execute_command('occfilter add Node')
    execute_command('undogeom enter')
    execute_command(
        'genselect occobject add region in '
        '0.01 0.99 0.99 0.01'
    )

    cmd = 'splcur fit piecewise {}e 1n \"2--{}\"'.format(
        nnode, nnode
    )
    execute_command(cmd)

    execute_command('undogeom leave')
    execute_command('genselect target occobject')
    execute_command('occfilter clear')
    execute_command('occfilter add Edge Wire')
    execute_command('undogeom enter')
    execute_command('genselect occobject add occobject  1e')
    execute_command('fillplane 0 0 1e')
    execute_command('undogeom leave')
    execute_command('genselect target occobject')
    execute_command('occfilter clear')
    execute_command(
        'genselect node add region in 0.01 '
        '0.95 0.95 0.01'
    )
    execute_command('elemedit delenode delete')
    execute_command('genselect clear')
    execute_command('elemedit delenode accept 1')
    execute_command('occfilter add Face')
    execute_command('genselect allvis')

    cmd = 'occmesh mesh 0 1 0 1 {} 0 0'.format(meshsize)
    echo(cmd)
    execute_command(cmd)
    
    execute_command('occmesh accept 1 0.0001 0 1')
    execute_command('genselect clear')
    execute_command('occfilter clear')
    execute_command('occfilter add Face')
    execute_command('genselect target shell')
    execute_command('genselect allvis')
    execute_command('genselect shell add part 1/0 ')
    execute_command('occview hide')

    cmd = (
        'elgenerate solid shelldrag 2 0 {} {} '
        '0 0 0 0 0 10000'.format(zlength, zelem)
    )
    execute_command(cmd)

    execute_command('genselect clear')
    execute_command('elgenerate accept')
    execute_command('partdata delete 1')
    execute_command('delelement accept')
    execute_command('save keywordabsolute 0')
    execute_command('save keywordbylongfmt 0')
    execute_command('save outversion 7')

    cmd = 'save keyword {}'.format(output_name)
    execute_command(cmd)

except ValueError as error:
    echo('Warning: No parameters!')
