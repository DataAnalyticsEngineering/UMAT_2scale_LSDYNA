# Example 11:
# Script to write nodal coordinate data for nodes in the selection buffer that was performed in the 
# General Selection of nodes, the output file name will be passed from the runscript command:
# 
# runscript example11.scl outputfilename   (for C-Script)
# or 
# runpython example11.scl outputfilename   (for Python-Script)

import LsPrePost as lspp
import DataCenter as dc


ret = lspp.cmd_result_get_value_count()
if ret:
    output_file = lspp.cmd_result_get_value(0)
    print(output_file)
    # Ask for no. of nodes in the model
    num_nodes = dc.get_data("num_nodes")

    # get the current state number
    ist = dc.get_data("current_state")
    # get no. of entities selected
    num_selected = dc.get_data("num_selection")
    print("ist=%d, num_selected=%d" % (ist, num_selected))

    lspp.switch_state(ist)
    # get coord arrays from Data Center
    coord_x = dc.get_data("state_node_x", type=dc.Type.NODE)
    coord_y = dc.get_data("state_node_y", type=dc.Type.NODE)
    coord_z = dc.get_data("state_node_z", type=dc.Type.NODE)

    # get the node IDs of the selection buffer
    node_ids = dc.get_data("selection_ids", type=0)
    with open(output_file, "w+") as f:
        for i in range(0, num_selected):
            nd = node_ids[i]
            nd1 = dc.get_data("internal_id", id=nd, type=dc.Type.NODE)
            dx = coord_x[nd1]
            dy = coord_y[nd1]
            dz = coord_z[nd1]
            f.write("%10d, %13f, %13f, %13f\n" % (nd, dx, dy, dz))
            print("%10d, %13f, %13f, %13f" % (nd, dx, dy, dz))
else:
    print("Output file name not specified")

