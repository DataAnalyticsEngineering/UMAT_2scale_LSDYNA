# Example 5:
# Script to extract the x,y,and z components of the displacement array, then compute the
#    resultant displacement for all the nodes and then fringe the computed result, 
#    also write the computed result to a file for each state. The file written can be loaded back
#    into LSPP as User defined fringe data

 
import DataCenter as dc
from DataCenter import Type as tp
from DataCenter import get_data
from LsPrePost import save_dc_to_file
from LsPrePost import fringe_dc_to_model
from LsPrePost import echo

num_state = get_data('num_states')
numnodes = get_data('num_nodes')

# Loop through all the states
for i in range(1, num_state+1):
    # get displacement array from Data center
    dispx = get_data('disp_x', tp.NODE, ist=i)
    dispy = get_data('disp_y', tp.NODE, ist=i)
    dispz = get_data('disp_z', tp.NODE, ist=i)
    # Do something user what to do
    results=[]
    for j in range(0, numnodes):
        val = (
            dispx[j]*dispx[j] + dispy[j]*dispy[j] +
            dispz[j]*dispz[j]
        )
        results.append(val**0.5)
    buf = 'resultant_disp'+str(i)+'.dat'
    print(results)
    save_dc_to_file(buf, numnodes, results)
    fringe_dc_to_model(tp.NODE, 1, numnodes, dispx, i, buf)