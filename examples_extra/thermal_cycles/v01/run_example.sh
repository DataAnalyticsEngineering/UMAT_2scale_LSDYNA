rm temp0.csv
rm -rf bottom_substrate* && /usr/bin/time -v lsdyna i=input_file.k ncpu=6 jobid=bottom_substrate
lsprepost c=plot_temp.cfile -nographics
python compare_thermal_cycles.py
