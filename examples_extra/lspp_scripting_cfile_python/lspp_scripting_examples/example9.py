# Example 9:
# Script to look up number of parts in a model, get the part IDs, for each active part, measure the volume of the part by issuing a 
# "Measure Vol part" command, and obtain the results from the command, then write out the return values from the measure 
# command to a file call postdata.txt 

''' LS-SCRIPT: */
    Script to look up number of parts, get the part IDs, 
    for each active part, measure the volume of the part 
    by issuing a "Measure Vol part" command, and obtain 
    the result from the command, then write out the return 
    values from the measure command to a file call postdata.txt 
'''
import DataCenter as dc
from LsPrePost import echo,check_if_part_is_active_u,execute_command
from LsPrePost import cmd_result_get_value,cmd_result_get_value_count
from LsPrePost import switch_state
from DataCenter import Type, Ipt

part_num = dc.get_data('num_validparts')
buf = 'No .of valid parts = {}'.format(part_num)
echo(buf)
# Set state to a very big number means last state
switch_state(9999)

# part ids
ids = dc.get_data('validpart_ids')
# Write header to the excel file
f = open('./postdata.txt', 'w+')
f.write('Part ID, Vol \n')
for i in range(ids.__len__()):
    id = ids[i]
    ret = check_if_part_is_active_u(id)
    # Process only active parts
    if ret:
        # Issue measure Volume command to LSPP
        buf = 'measure vol part {}'.format(id)
        execute_command(buf)
        # Get no. of data from the measure command
        ret = cmd_result_get_value_count()
        if ret:
            # Write Part ID to a buffer
            buf = str(id)
            # get result value, first value is volume
            fv = cmd_result_get_value(0)
            tmbuf = ',vol={}'.format(fv)
            buf+=tmbuf
            # second value is enclosed volume
            fv = cmd_result_get_value(1)
            tmbuf = ',encl. vol={}'.format(fv)
            buf+=tmbuf
            # third value is area
            fv = cmd_result_get_value(2)
            tmbuf = ',area={}'.format(fv)
            buf+=tmbuf
            echo(buf)
            f.write(buf+'\n')

f.close()


