# Directory containing python file should be included in PYTHONPATH
# export PYTHONPATH=/home/alameddin/simkom/src_pyrve/dyna/repo_files/external_packages:$PYTHONPATH

ifort -c forpy_mod.F90 # -> .o & .mod
ifort example_forpy.F90 forpy_mod.o `python3.8-config --ldflags --embed` -o del_example_forpy && ./del_example_forpy