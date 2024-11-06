program test_cpp_call

implicit none

real*8 :: eps(6), sig(6),alpha
integer :: int

eps = [1, 2, 3, 2*8, 2*10, 2*12]

call cppfun(eps,sig,alpha)

write(*,*) 'output'
write(*,*) sig
write(*,*) alpha

end program test_cpp_call
