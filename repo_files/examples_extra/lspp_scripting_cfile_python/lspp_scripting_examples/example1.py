# Example 1:
# Script to get no. of parts in the model, 
# Get all the part IDs, then draw each part by itself and auto center it 
# For each part, capture a picture in png format, and save it to a file which has the part id as the file name.

import DataCenter as dc
import LsPrePost as lspp

part_ids = dc.get_data("validpart_ids")
part_num = part_ids.__len__()
for i in range(part_num):
    # Build command to draw one part, also Auto center it 
    command = 'm {}'.format(part_ids[i])
    lspp.execute_command(command)
    lspp.execute_command('ac')
    # Build command to print the picture with png format
    command = (
        'print png part_{}.png LANDSCAPE nocompress '
        'gamma 1.000 opaque enlisted \"OGL1x1\"'.format(part_ids[i])
    )
    lspp.execute_command(command)