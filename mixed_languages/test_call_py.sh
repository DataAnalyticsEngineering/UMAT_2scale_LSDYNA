# Directory containing python file should be included in PYTHONPATH
# export PYTHONPATH=/home/alameddin/simkom/src_pyrve/dyna/lsdyna_added_files_ref/mixed_languages:$PYTHONPATH

icpc -Wall -c cpp_to_py.cpp `python3.8-config --cflags`
ifort example_call_py.F90 -o del_example_py cpp_to_py.o -lstdc++ `python3.8-config --ldflags --embed` && ./del_example_py