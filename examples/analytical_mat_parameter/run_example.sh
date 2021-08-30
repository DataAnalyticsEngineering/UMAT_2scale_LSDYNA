/usr/bin/time -v lsdynaumat i=input_thermal_interface.key ncpu=6 jobid=thermal

/usr/bin/time -v lsdynaumat ncpu=1 i=input_coupled_interface.key t=thermal.d3plot jobid=coupled

/usr/bin/time -v lsdynaumat ncpu=1 i=input_thermomech_interface.key jobid=thermomech
