rm temp0.csv
rm -rf bottom_substrate* && lsdyna i=input_file.k ncpu=6 jobid=bottom_substrate
lsprepost2 c=plot_temp.cfile -nographics
python compare_thermal_cycles.py
