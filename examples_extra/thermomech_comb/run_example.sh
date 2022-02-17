# /usr/bin/time -v 

rm -rf temp0.csv
# rm -rf thermal* && rm -rf coupled* && rm -rf thermomech*

# rm -rf thermal* && lsdyna i=input_file.k ncpu=6 jobid=thermal
# rm -rf coupled* && lsdyna i=input_coupled.k ncpu=6 t=thermal.d3plot jobid=coupled

rm -rf thermomech* && lsdyna i=input_thermomech.k ncpu=6 jobid=thermomech

# lsprepost2 c=plot_temp.cfile -nographics
# python compare_thermal_cycles.py


# restart simulation
# lsdyna r=thermal.d3dump05 
# lsdyna i=input_restart.k r=thermal.d3dump05 
