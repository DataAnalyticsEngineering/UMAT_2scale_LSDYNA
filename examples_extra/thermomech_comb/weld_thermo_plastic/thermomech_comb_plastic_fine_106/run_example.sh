# /usr/bin/time -v 

rm -rf sim* && /usr/bin/time -v lsdyna i=input_file.k ncpu=15 jobid=sim

lsprepost c=post_process.cfile -nographics
