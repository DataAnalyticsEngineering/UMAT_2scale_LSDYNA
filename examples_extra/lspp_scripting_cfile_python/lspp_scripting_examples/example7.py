# Example 7:
# Script to extract the z component of the nodal displacement array, then differentiate it with respect to time, 
# which should gives the z velocity array, then extract the z component of the velocity array that was stored in d3plot file 
# and then compute the difference between differentiated result with stored result and then fringe it.

''' LS-SCRIPT: displacement differentiation
    Script to extract the z component of the 
    nodal displacement array, then differentiate 
    it with respect to time, which should be the 
    z velocity array, then extract the z component 
    of the velocity array that was stored in d3plot 
    file from differentiated result and then fringe it.
'''
import DataCenter as dc
from LsPrePost import echo, fringe_dc_to_model
from DataCenter import Type, Ipt

num_states = dc.get_data('num_states')
num_nodes = dc.get_data('num_nodes')

times = dc.get_data('state_times')
buf = 'num_states={}'.format(str(num_states))
echo(buf)

for i in range(num_states):
    velo_z = dc.get_data('velo_z', type=Type.NODE, ist=i+1)
    if i==0:
    # first state: forward difference error h
        cur = dc.get_data('disp_z', type=Type.NODE, ist=1)
        dispz1 = dc.get_data('disp_z', type=Type.NODE, ist=2)
        h = times[1]-times[0]

        for j in range(num_nodes):
            cur[j] = (dispz1[j]-cur[j])/h
    elif i==num_states-1:
    # last state: backward difference error h
        cur = dc.get_data('disp_z', type=Type.NODE, ist=i+1)
        dispz1 = dc.get_data('disp_z', type=Type.NODE, 
                             ist=num_states-1)
        h = times[num_states-1]-times[num_states-2]

        for j in range(num_nodes):
            cur[j] = (cur[j]-dispz1[j])/h
    else:
    # middle states: centered difference error h**2
        dispz1 = dc.get_data('disp_z', type=Type.NODE, ist=i)
        dispz2 = dc.get_data('disp_z', type=Type.NODE, ist=i+2)
        h = times[i+1]-times[i-1]

        for j in range(num_nodes):
            cur[j] = (dispz2[j]-dispz1[j])/h
    # Compute the difference between differentiated 
    # result with stored result
    for j in range(num_nodes):
        cur[j] = cur[j] - velo_z[j]

    buf = 'Error of Differentiation at state {}'.format(str(i+1))
    fringe_dc_to_model(Type.NODE, 1, num_nodes, cur, i+1, buf)