subroutine umat43(cm, eps, sig, epsp, hsv, dt1, capa, etype, tt, temper, failel, crv, nnpcrv, cma, qmat, elsiz, idele, reject)
   use Tensor
   use forpy_mod
   use iso_fortran_env, only: real64

   implicit none

   include 'nlqparm'
   include 'bk06.inc'
   include 'iounits.inc'
   real*8, dimension(*) :: cm(*), eps(*), sig(*), hsv(*), crv(lq1, 2, *), cma(*), qmat(3, 3)
   integer nnpcrv(*)
   character*5 etype
   logical failel, reject
   integer*8 idele

   integer*8 lft, llt, nip, ipt_thk, ipt

   real*8 epsp, dt1, capa, tt, temper, elsiz
   real*8 young_modulus, poisson_ratio, shear_modulus, bulk_modulus
   type(Tensor2s) I2, stress_n, d_eps, eps_p_n
   type(Tensor2s) stress_ttb
   type(Tensor4s) I4, IxI, P1, P2, C0

   integer :: ierror
   type(tuple) :: args
   type(module_py) :: py_module
   type(object) :: return_value
   type(list) :: output_list
   type(object) :: item
   real*8 :: stress(6)
   integer idx

   if (etype .eq. 'shell') then
      ! xx,yy,zz,xy,yz,xz
      ! plane strain
      eps(3) = 0
      eps(5) = 0
      eps(6) = 0
   end if

   ! if (sum(eps(1:6)) > 0) then
   !   write(*,'(6(ES11.4,3x))') eps(1:6)
   ! endif

   young_modulus = cm(1)
   poisson_ratio = cm(2)

   shear_modulus = young_modulus/(2.*(1.+poisson_ratio))
   bulk_modulus = young_modulus/(3.*(1.-2.*poisson_ratio))

   I2 = identity2(I2)
   I4 = identity4(I2)
   IxI = I2.dya.I2
   P1 = IxI/3.0
   P2 = I4 - P1
   C0 = bulk_modulus*IxI + 2.*shear_modulus*P2

   d_eps = str2ten_2s(eps(1:6), 3, 3, 6)

   stress_n = symstore_2sa(sig(1:6))
   stress_ttb = stress_n + (C0**(d_eps))
   sig(1:6) = asarray(voigt(stress_ttb), 6)

   hsv(2:37) = pack(asarray(voigt(C0), 6, 6), .true.)

   hsv(1) = temper

   return
end

subroutine thumat13(c1, c2, c3, cvl, dcvdtl, hsrcl, dhsrcdtl, hsv, hsvm, nmecon, r_matp, crv, nnpcrv, nel, nep, iep, eltype, dt, atime, ihsrcl, temp, ttconv, ttnext, tmconv, tmnext, inithis)
   use forpy_mod
   use iso_fortran_env, only: real64
   ! iso_fortran_env: http://fortranwiki.org/fortran/show/iso_fortran_env
   ! called for every integration point

   implicit none

   include 'nlqparm'
   include 'iounits.inc'
   include 'nhisparm.inc'
   character*(*) eltype
   logical inithis
   real*8 hsv(*), hsvm(*), crv(lq1, 2, *)
   integer nnpcrv(*), ihsrcl
   real*8 c1, c2, c3, cvl, dcvdtl, hsrcl, dhsrcdtl, nmecon
   integer nel, nep, iep
   real*8 temp, r_matp(*), dt, atime
   real*8 ttconv, ttnext, tmconv, tmnext

   integer :: ierror
   type(tuple) :: args
   type(module_py) :: py_module
   type(object) :: return_value
   type(list) :: output_list
   type(object) :: item0, item1, item2, item3

   c1 = r_matp(8 + 1)
   c2 = r_matp(8 + 2)
   c3 = r_matp(8 + 3)
   cvl = r_matp(8 + 4) !specific heat capacity (Energy/Mass/Temperature)

   ihsrcl = 0 !1 if heat source is to be taken into account for this material
   ! hsrcl = 0. !heat source (Energy/Time/Volume)

   return
end

subroutine utan43(cm, eps, sig, epsp, hsv, dt1, unsym, capa, etype, tt, temper, es, crv, nnpcrv, failel, cma, qmat)
   implicit none

   include 'nlqparm'
   real*8, dimension(*) :: cm(*), eps(*), sig(*), hsv(*), crv(lq1, 2, *), cma(*)
   integer nnpcrv(*)
   real*8, dimension(*) :: es(6, *), qmat(3, 3)
   logical failel, unsym
   character*5 etype

   real*8 epsp, dt1, capa, tt, temper

   es(1:6, 1:6) = reshape(hsv(2:37), [6, 6])

   return
end

subroutine umat43v(cm, d1, d2, d3, d4, d5, d6, sig1, sig2, sig3, sig4, sig5, sig6, epsps, hsv, lft, llt, dt1siz, capa, etype, tt, temps, failels, nlqa, crv, nnpcrv, cma, qmat, elsizv, idelev, reject)
   include 'nlqparm'
   include 'iounits.inc'
   dimension d1(*), d2(*), d3(*), d4(*), d5(*), d6(*)
   dimension sig1(*), sig2(*), sig3(*), sig4(*), sig5(*), sig6(*)
   dimension cm(*), epsps(*), hsv(nlq, *), dt1siz(*)
   dimension temps(*), crv(101, 2, *), cma(*), qmat(nlq, 3, 3), elsizv(*)
   integer nnpcrv(*)
   integer*8 idelev(*)
   logical failels(*), reject
   character*5 etype

   stop "Not implemented: umat43v"

   return
end

subroutine utan43v(cm, d1, d2, d3, d4, d5, d6, sig1, sig2, sig3, sig4, sig5, sig6, epsps, hsvs, unsym, lft, llt, dt1siz, capa, etype, tt, temps, dsave, nlqa, crv, nnpcrv, failels, cma, qmat)
   include 'nlqparm'
   dimension d1(*), d2(*), d3(*), d4(*), d5(*), d6(*)
   dimension sig1(*), sig2(*), sig3(*), sig4(*), sig5(*), sig6(*)
   dimension epsps(*), hsvs(nlq, *), dt1siz(*), cm(*), qmat(nlq, 3, 3)
   dimension temps(*), dsave(nlq, 6, *), crv(lq1, 2, *), cma(*)
   integer nnpcrv(*)
   logical failels(*), unsym
   character*5 etype

   stop "Not implemented: utan43v"

   return
end
