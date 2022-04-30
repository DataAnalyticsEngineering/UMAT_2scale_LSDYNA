# /usr/bin/time -v 

rm -rf sim* && lsdyna i=input.k ncpu=6 jobid=sim

lsprepost c=post_process.cfile -nographics
