import DataCenter as dc
from DataCenter import Type as tp
from DataCenter import get_data
from LsPrePost import save_dc_to_file
from LsPrePost import fringe_dc_to_model
from LsPrePost import echo
import LsPrePost as lspp
import numpy as np

num_state = get_data('num_states')
numnodes = get_data('num_nodes')

nodal_temperatures = get_data('nodal_temperatures', tp.NODE, ist=1)

# Loop through all the states
for i in range(1, num_state + 1):
    nodal_temperatures = np.maximum(nodal_temperatures, get_data('nodal_temperatures', tp.NODE, ist=i))

lspp.execute_command('ac')
lspp.execute_command('mesh on')
png_id = iter(range(10))

# save_dc_to_file(buf, numnodes, results)
fringe_dc_to_model(tp.NODE, 1, numnodes, nodal_temperatures, 1, f'max_temp_over_time')
lspp.execute_command(f'print png image_00{next(png_id)}.png gamma 1.00 enlisted OGL1x1')

# bead_temperature = np.copy(nodal_temperatures)
# bead_temperature[bead_temperature < 1356.15 * 1.0] = 0
# fringe_dc_to_model(tp.NODE, 1, numnodes, bead_temperature, 1, f'max_temp_over_time')
# lspp.execute_command(f'print png image_00{next(png_id)}.png gamma 1.00 enlisted OGL1x1')
# 
# bead_temperature = np.copy(nodal_temperatures)
# bead_temperature[bead_temperature < 1356.15 * 1.0] = 0
# bead_temperature[bead_temperature > 0] = 1
# fringe_dc_to_model(tp.NODE, 1, numnodes, bead_temperature, 1, f'max_temp_over_time')
# lspp.execute_command(f'print png image_00{next(png_id)}.png gamma 1.00 enlisted OGL1x1')

print('did you change DATABASE_BINARY_D3PLOT dt to 0.1 ???')