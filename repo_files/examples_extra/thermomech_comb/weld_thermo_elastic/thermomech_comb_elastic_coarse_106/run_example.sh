# /usr/bin/time -v 

rm -rf sim* && /usr/bin/time -v lsdyna i=input_file.k ncpu=20 jobid=sim

lsprepost c=post_process.cfile -nographics
