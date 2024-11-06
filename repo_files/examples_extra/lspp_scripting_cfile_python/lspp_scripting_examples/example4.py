# Example 4:
# Script to measure the mass, mass center of gravity and volume of all solid parts in the model
#    the measured information will be written to file example4.txt 
# 
# Example 4a:
# Script to measure the angular velocity, of all solid parts in the model
#    the measured information will be written to file example4a.txt 
# 
from LsPrePost import execute_command, echo
from LsPrePost import check_if_part_is_active_u as check_u
from LsPrePost import cmd_result_get_value_count as crgvc
from LsPrePost import cmd_result_get_value as crgv
import DataCenter as dc

# open the txt file for output
f = open('./exam4.txt', 'w+')
# To keep only Solid part, turn off other type of elements
execute_command("selectpart beam off")
execute_command("selectpart shell off")
execute_command("selectpart tshell off")

part_num = dc.get_data('num_validparts')
cmd = 'No. of valid parts={}'.format(str(part_num))
echo(cmd)
# Set state to last state in case this is post-processing data
# since we don't know no. of states, 
# so set it to a very large number
validpart_ids = dc.get_data('validpart_ids')
part_num = validpart_ids.__len__()
echo('part_num={}'.format(str(part_num)))
# Write header to the excel file
string = 'Part ID, Mass, CGx, CGy, CGz, volume\n'
f.write(string+'\n')
for i in range(0, part_num):
    id = validpart_ids[i]
    # Check if the part is active or not
    ret = check_u(id)
    buf = 'part id=' + str(id) + ', active=' + str(ret)
    echo(buf)
    # Process only active parts
    if ret == 1:
        # built command to measure part inertia
        cmdbuf = 'measure inertia part H'+str(id)
        execute_command(cmdbuf)
        # Get no. of data from the measure command
        noret = crgvc()
        buf = 'No. of result values='+str(noret)
        echo(buf)
        if noret != 0:
            buf = str(id)
            # Only need 4, Mass, CGx, CGy, CGz
            for j in range(0, 4):
                fv = crgv(j)
                tmbuf = ', '+str(fv)
                buf = buf + tmbuf
            echo(buf)
            # built command to measure part volume
            cmdbuf = 'measure vol part '+str(id)
            execute_command(cmdbuf)
            # Get no. of data from the measure command
            noret = crgvc()
            # volume is the first return data 
            # from the measure vol command
            fv = crgv(0)
            buf = buf+', '+str(fv)
            f.write(buf+'\n')

f.close()