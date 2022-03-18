# git clone https://gitlab.com/libeigen/eigen.git
# gcc -c compiles source files without linking. -> generate .o object file

icc -Wall -c cpp_example.cpp
ifort example_call_cpp.F90 -o del_example_cpp cpp_example.o -lstdc++ && ./del_example_cpp
