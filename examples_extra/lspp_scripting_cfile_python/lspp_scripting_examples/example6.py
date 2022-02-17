# Example 6:
# Scrpte to get x,y,z, global stress component and compute the average stress
#    then fringe the computed result and write it out to file
   
import DataCenter as dc
from DataCenter import Type, Ipt
import LsPrePost as lspp

num_states = dc.get_data('num_states')
num_shell_elements = dc.get_data('num_shell_elements')

for i in range(num_states):
    stress_x = dc.get_data(
        'stress_x', type=Type.SHELL, ipt=Ipt.MIDDLE, ist=i+1
    )
    stress_y = dc.get_data(
        'stress_y', type=Type.SHELL, ipt=Ipt.MIDDLE, ist=i+1
    )
    stress_z = dc.get_data(
        'stress_z', type=Type.SHELL, ipt=Ipt.MIDDLE, ist=i+1
    )

    # Do something user want to do
    results=[]
    for j in range(num_shell_elements):
        results.append((stress_x[j]+stress_y[j]+stress_z[j])/3.0)
    buf = 'state_stress_shellonly{}.pydata'.format(str(i+1))
    lspp.save_dc_to_file(buf, num_shell_elements, results)
    lspp.fringe_dc_to_model(
        Type.SHELL, 1, num_shell_elements, results, i+1, buf
    )
