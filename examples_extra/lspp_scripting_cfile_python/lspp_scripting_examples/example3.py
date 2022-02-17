# Example 3:
# Script to create a load curve based on a given equation and some parameters, 
# the script will be called by a command file example3.cfile which passes the parameters to the script
# the created curves will be written to a file called curve.txt
# then load the file back to display in the xy-plot interface as a XY graph

from LsPrePost import cmd_result_get_value_count as crgvc
from LsPrePost import cmd_result_get_value as crgv
from LsPrePost import execute_command, echo
import sys
from math import e

def custom_curve(num, pa, pb, pc, xmin, xmax):
    f = open('./curve.txt', 'w+')
    f.write(str(num)+'\n')
    inc = (1.0/num)*(xmax-xmin)
    echo(str(inc))
    for i in range(0, num):
        if i == 0:
            x =0.0
        else:
            x = x + inc
        y = pa*(1-e**(-pb*x)) + pc
        cmd = str(x)+', '+str(y)
        f.write(cmd+'\n')
    f.close()
    cmd = 'open xydata "curve.txt"'
    execute_command(cmd)
    cmd = 'show "curve.txt~1" 0'
    execute_command(cmd)

ret = crgvc()
if ret == 0:
    echo('Warning: No parameter!')
else:
    num = crgv(0)
    pa = crgv(1)
    pb = crgv(2)
    pc = crgv(3)
    xmin = crgv(4)
    xmax = crgv(5)

    cmd = (
        'ren={}, num={}, pa={}, pb={}, pc={}, '
        'xmin={}, xmax={}'.format(
            ret, num, pa, pb, pc, xmin, xmax
        )
    )
    echo(cmd)
    custom_curve(num, pa, pb, pc, xmin, xmax)