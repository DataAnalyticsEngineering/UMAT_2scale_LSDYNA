# /usr/bin/time -v 

rm -rf sim* && /usr/bin/time -v lsdynaumat i=input_file.k ncpu=6 jobid=sim

lsprepost c=post_process.cfile -nographics
 
# rm temp0.csv
# lsprepost c=plot_temp.cfile -nographics
# python compare_thermal_cycles.py
