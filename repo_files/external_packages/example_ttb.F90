#define NOR4
#include 'ttb/ttb_library.F'
      program test_ttb

      use Tensor

      implicit none

      real(kind=8) :: deps(6), sig(6), es(4)
      real(kind=8) :: young_modulus, poisson_ratio
      real(kind=8) :: bulk_modulus, shear_modulus, sqrt2
      type(Tensor2s) :: stress_n, d_eps
      type(Tensor2s) :: I2
      type(Tensor4s) :: I4, IxI, P1, P2, C4, C0

      deps = [1, 2, 3, 2*8, 2*10, 2*12] ! assumed in voigt notation
      sig = [1, 2, 3, 4, 5, 6]
      d_eps = str2ten_2s(deps, 3, 3, 6)
      stress_n = symstore_2sa(sig)

      young_modulus = 3.2
      poisson_ratio = 0.34

      shear_modulus = young_modulus/(2.*(1.+poisson_ratio))
      bulk_modulus = young_modulus/(3.*(1.-2.*poisson_ratio))

      I2 = identity2(I2)
      I4 = identity4(I2)
      IxI = I2.dya.I2
      P1 = IxI/3.0
      P2 = I4 - P1
      
      ! C0 in Mandel notation
      C0 = bulk_modulus*IxI + 2.*shear_modulus*P2

      ! Mandel to Voigt notation
      sqrt2 = sqrt(2.)
      C0%a6b6(1, 4:6) = C0%a6b6(1, 4:6)/sqrt2
      C0%a6b6(2, 4:6) = C0%a6b6(2, 4:6)/sqrt2
      C0%a6b6(3, 4:6) = C0%a6b6(3, 4:6)/sqrt2
      C0%a6b6(4:6, 1) = C0%a6b6(4:6, 1)/sqrt2
      C0%a6b6(4:6, 2) = C0%a6b6(4:6, 2)/sqrt2
      C0%a6b6(4:6, 3) = C0%a6b6(4:6, 3)/sqrt2
      C0%a6b6(4, 4:6) = C0%a6b6(4, 4:6)/2.
      C0%a6b6(5, 4:6) = C0%a6b6(5, 4:6)/2.
      C0%a6b6(6, 4:6) = C0%a6b6(6, 4:6)/2.

      write (*, '(6(ES11.4,3x))') d_eps%a6(1:6)
      print *, '-----------------------------------'
      write (*, '(6(ES11.4,3x))') C0
      print *, '-----------------------------------'
      write (*, '(6(ES11.4,3x))') C0**d_eps
      print *, '-----------------------------------'
      
      es = [1, 2, 3, 2*8]
      print *, RESHAPE(es, (/2, 2/))
      print *, pack(RESHAPE(es, [2, 2]), .true.)

      end program test_ttb