# updateintel
export PYTHONPATH=/home/alameddin/simkom/src_pyrve/dyna/lsdyna_added_files_ref:$PYTHONPATH

rm -rf thermal.*
/usr/bin/time -v lsdyna ncpu=12 i=input.k jobid=thermal

rm -rf coupled.*
/usr/bin/time -v lsdyna ncpu=12 i=input_coupled.k t=thermal.d3plot jobid=coupled
