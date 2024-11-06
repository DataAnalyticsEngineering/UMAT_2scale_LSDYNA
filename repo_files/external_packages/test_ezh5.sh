# gcc -I adds include directory of header files.
# gcc -l links with a library file.
# gcc -L looks in directory for library files.

cd ezh5 && icc example_ezh5.cc -I/usr/include/hdf5/serial/ -L/usr/lib/x86_64-linux-gnu/hdf5/serial/ -lhdf5 -o del_example_ezh5 && ./del_example_ezh5