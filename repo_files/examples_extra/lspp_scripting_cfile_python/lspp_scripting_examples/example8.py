# Example 8:
# Script to extract MX, MY, MXY,  QX, QY, NX, NY, NXY at the last state for Shell elements 
# from a set of d3plot files, and write the extracted data out to a file
 
''' LS-SCRIPT:Extract SHELL element data from DataCenter*/
    Script to extract MX, MY, MXY,  QX, QY, NX, NY, NXY at 
    the last state for Shell element from a set of d3plot 
    files, and write the extracted data out to a file
'''
import DataCenter as dc
from DataCenter import Type, Ipt
from LsPrePost import fringe_dc_to_model

num_states = dc.get_data('num_states')
num_elements = dc.get_data('num_elements')

f = open('./MxMyQxQy.dat', 'w+')
# Switch to the last state
# Read data from d3plot file (data center) for 
# shell element only
mx = dc.get_data(
    'mx', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
my = dc.get_data(
    'my', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
mxy = dc.get_data(
    'mxy', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
nx = dc.get_data(
    'nx', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
ny = dc.get_data(
    'ny', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
nxy = dc.get_data(
    'nxy', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
qx = dc.get_data(
    'qx', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
qy = dc.get_data(
    'qy', type=Type.SHELL, ipt=Ipt.MEAN, ist=num_states
)
# Fringe QX for this state
buf = 'QX at state {}'.format(num_states)
fringe_dc_to_model(
    Type.SHELL, 1, mx.__len__(), qx, num_states, buf
)
# Write title to file
f.write('Element ID, Mx, My, Mxy, Qx, Qy, Nx, Ny, Nxy\n')
# Write data to file for each element, with element ID
for i in range(mx.__len__()):
    eid = dc.get_data('user_id', type=Type.SHELL, id=i)
    f.write('{}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(
        eid,mx[i],my[i],mxy[i],qx[i],qy[i],
            nx[i],ny[i],nxy[i]
        )
    )
f.close()
