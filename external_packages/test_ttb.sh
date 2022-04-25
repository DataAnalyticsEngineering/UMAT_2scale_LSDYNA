# gcc -I adds include directory of header files.
# gcc -l links with a library file.
# gcc -L looks in directory for library files.

# use:
# ifort example_ttb.F -Ittb -o del_example_ttb && ./del_example_ttb
ifort example_ttb.f -i8 -r8 -o del_example_ttb && ./del_example_ttb

# or if you use #define NOR4
# ifort example_ttb.F -i8 -r8 -o del_example_ttb && ./del_example_ttb
