# updateintel
export PYTHONPATH=<simkom_path>/src_pyrve/dyna/repo_files:$PYTHONPATH

rm -rf thermal.*
/usr/bin/time -v lsdyna ncpu=12 i=input.k jobid=thermal

rm -rf coupled.*
/usr/bin/time -v lsdyna ncpu=12 i=input_coupled.k t=thermal.d3plot jobid=coupled
