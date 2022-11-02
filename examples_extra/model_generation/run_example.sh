# /usr/bin/time -v 

### Step 1
lsprepost c=gen.cfile -nographics
# output: parts.k, mesh.k, info.json

### Step 2
# open mesh.k and save without its parts (this was done automatically in python)
python3 remove_parts.py
# lsprepost mesh.k
# check if duplicate nodes are merged

### Step 3
rm -rf sim* && /usr/bin/time -v lsdynaumat i=input_file.k ncpu=4 jobid=sim

### Step 4
lsprepost sim.d3plot
# rm temp0.csv
# lsprepost c=plot_temp.cfile -nographics
# python compare_thermal_cycles.py
