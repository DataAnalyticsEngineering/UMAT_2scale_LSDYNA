# /usr/bin/time -v 

rm -rf sim* 

/usr/bin/time -v lsdynaumat i=input_file.k ncpu=12 jobid=thermal

/usr/bin/time -v lsdynaumat ncpu=1 i=input_coupled.k t=thermal.d3plot jobid=sim

lsprepost c=post_process.cfile -nographics
