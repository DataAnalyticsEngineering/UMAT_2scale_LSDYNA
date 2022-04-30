# /usr/bin/time -v 

rm -rf sim* && lsdynaumat i=input.k ncpu=1 jobid=sim

lsprepost c=post_process.cfile -nographics
