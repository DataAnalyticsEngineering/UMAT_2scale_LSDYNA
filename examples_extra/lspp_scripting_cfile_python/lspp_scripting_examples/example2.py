# Example 2:
# Script to create a plate with 25 shell elements, then extract the following:
# 1. number of nodes/elements in the model,
# 2. largest node/element ids,
# 3. the array of the node ids.
# 4. get the element connectivity for the last element
# 

import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import execute_command, echo

# Build command to create the plate with 5x5 elements
execute_command(
    'meshing 4pshell create 5 5 0 0 0 10 0 '
    '0 10 10 0 0 10  0'
)
# command to accept the mesh with element ID starting 101, 
# node ID starting 501
execute_command('meshing 4pshell accept 1 101 501 shell_4p')
execute_command('ac')

num_nodes = dc.get_data('num_nodes')
cmd = 'No. of nodes in model = {}'.format(str(num_nodes))
echo(cmd)
num_elem = dc.get_data('num_elem')
cmd = 'No. of elements in model = {}'.format(str(num_elem))
echo(cmd)

largest_node_id = dc.get_data('largest_node_id')
cmd = 'Largest node id = {}'.format(str(largest_node_id))
echo(cmd)
largest_elem_id = dc.get_data('largest_elem_id')
cmd = 'Largest element id = {}'.format(str(largest_elem_id))
echo(cmd)

node_ids = dc.get_data('node_ids')
echo('Node Ids: ')
for i in range(0, node_ids.__len__()):
    cmd = 'inode={}, uid={}'.format(str(i), str(node_ids[i]))
    echo(cmd)

# Build command to get the last element connectivity
ele_conn = dc.get_data('element_connectivity', type=Type.SHELL, 
                        id=largest_elem_id)
cmd = 'element ids={}, connectivity={}, {}, {}, {}'.format(
    str(largest_elem_id), str(ele_conn[0]), str(ele_conn[1]),
    str(ele_conn[2]), str(ele_conn[3])
)
echo(cmd)