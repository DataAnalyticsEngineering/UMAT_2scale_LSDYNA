! *MAT_USER_DEFINED_MATERIAL_MODELS
! These are Material Types 41 - 50
! mid: A number between 41 and 50 must be chosen. TODO If MT < 0, subroutine rwumat in dyn21.f is
! called, where the material parameter reading can be modified.
! If IORTHO = 0, LMC must be ≤ 48. If IORTHO = 1, LMC must be ≤ 40.
! There is no limit on the size of LMCA
! itherm: element temperature -> if (ishrmp(mt).lt.0) then in dyn21umat.f
! ibulk: Address of bulk modulus in material constants array (use the maximum)
! ig: Address of shear modulus in material constants array (use the maximum)
! ihyper: 10, enforces full integration of element -2
! $#     mid        ro        mt       lmc       nhv    iortho     ibulk        ig
!          1    8933.0        44         8        40         0         4         3
! $#   ivect     ifail    itherm    ihyper      ieos      lmca    unused    unused
!          0         0         1        10         0         0
! $#      p1        p2        p3        p4        p5        p6        p7        p8
!   128.85e9      0.34 4.808e+10 1.342e+11         0         0         0         0

subroutine umat44(cm, eps, sig, epsp, hsv, dt1, capa, etype, tt, temper, failel, crv, nnpcrv, cma, qmat, elsiz, idele, reject)
   use Tensor
   use forpy_mod
   use iso_fortran_env, only: real64
   use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan, ieee_is_nan

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

   ! plane strain
   ! if (etype .eq. 'shell') then
   !    ! xx,yy,zz,xy,yz,xz
   !    eps(3) = 0
   !    eps(5) = 0
   !    eps(6) = 0
   ! end if

   ! if (sum(eps(1:6)) > 0) then
   !   write(*,'(6(ES11.4,3x))') eps(1:6)
   ! endif

   if (ncycle .eq. 0) then
      hsv(1) = temper
      hsv(2:70) = 0.0
      hsv(70) = temper ! reference temperature for the thermal strain
      return
   end if

   do idx = 1, 6
      hsv(idx + 50) = hsv(idx + 50) + eps(idx)
   end do

   if (int(cm(6)) == 0) then
  call umat_cpp_mechanical(cm(8), temper, temper - hsv(1), hsv(51:56), sig, hsv(2:37), cm(7), hsv(61:66), epsp, hsv(38:43), hsv(70))

   elseif (int(cm(6)) == 1) then

      call cppcallpython_mechanical(cm(8), temper, temper, eps, stress, hsv(2:37))
      sig(1:6) = sig(1:6) + stress(1:6)

   elseif (int(cm(6)) == 2) then

      ierror = import_py(py_module, "umat")

      ierror = tuple_create(args, 16)
      ierror = args%setitem(0, 1) ! -> mechanical
      ierror = args%setitem(1, cm(8)) ! mat_id
      ierror = args%setitem(2, temper)
      ierror = args%setitem(3, temper - hsv(1))
      do idx = 1, 6 ! previous_therma_strain
         ierror = args%setitem(idx + 3, hsv(idx + 37))
      end do

      do idx = 1, 6
         ierror = args%setitem(idx + 9, hsv(idx + 50))
      end do

      ierror = call_py(return_value, py_module, "rve_solver_factory", args)

      ierror = cast(output_list, return_value)
      do idx = 1, 6 ! stress
         ierror = output_list%getitem(item, idx - 1)
         ierror = cast(sig(idx), item)
         call item%destroy
      end do
      do idx = 1, 36 ! stiffness
         ierror = output_list%getitem(item, idx + 5)
         ierror = cast(hsv(idx + 1), item)
         call item%destroy
      end do
      do idx = 1, 6 ! thermal_strain
         ierror = output_list%getitem(item, idx + 41)
         ierror = cast(hsv(idx + 37), item)
         call item%destroy
      end do

      ! hsv(2:37) = pack(stiffness, .true.)

   else

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

   end if

   hsv(1) = temper

   ! write (*, '(6(ES11.4,3x))') hsv(1:66)
   ! write (*, *) "------------"
   ! write (*, '(6(ES11.4,3x))') hsv(51:56)
   ! write (*, '(6(ES11.4,3x))') hsv(61:66)
   ! stop "message"

   call args%destroy
   call py_module%destroy
   call return_value%destroy
   call output_list%destroy

   return
end

! $The thermal user materials are thermal material types 11-15.
! *MAT_THERMAL_USER_DEFINED
! $lmc: Length of material constants array, must not be greater than 32.
! $nhv: Number of history variables
!       Thermal history variables are output to the tprint file, see *DATABASE_TPRINT.
!       Thermal history variables are not output to d3plot.
! $ihve: activate exchange (read only) of history variables between mechanical and thermal user material models
!        ihve = 1 only supported for
!        Solid elements: ELFORM = 1, 2, 10, 13.
!         Shell elements: ELFORM = 2, 3, 4, 16.
!         user-defined integration rules are not supported.
! The thermal solver includes not only the plastically dissipated energy as a heat
! source but also wrongly the elastic energy. The latter however is in most cases not of practical importance.
! $#     mid        ro        mt       lmc       nhv      aopt orthotrop      ihve
!          1    8933.0        14         8        13         0         1         1
!
!
!      400.0     400.0     400.0     383.0         0         0         0         0
subroutine thumat14(c1, c2, c3, cvl, dcvdtl, hsrcl, dhsrcdtl, hsv, hsvm, nmecon, r_matp, crv, nnpcrv, nel, nep, iep, eltype, dt, atime, ihsrcl, temp, ttconv, ttnext, tmconv, tmnext, inithis)
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

   if (int(r_matp(8 + 6)) == 0) then

      call umat_cpp_thermal(r_matp(8 + 8), temp, c1, c2, c3, cvl)
      ihsrcl = 0

   elseif (int(r_matp(8 + 6)) == 1) then

      call cppcallpython_thermal(r_matp(8 + 8), temp, c1, c2, c3, cvl)
      ihsrcl = 0 !1 if heat source is to be taken into account for this material

   elseif (int(r_matp(8 + 6)) == 2) then

      ierror = import_py(py_module, "umat")

      ierror = tuple_create(args, 3)
      ierror = args%setitem(0, 0) ! 0 -> thermal
      ierror = args%setitem(1, r_matp(8 + 8)) ! material_id
      ierror = args%setitem(2, temp)

      ierror = call_py(return_value, py_module, "rve_solver_factory", args)

      ierror = cast(output_list, return_value)
      ierror = output_list%getitem(item0, 0)
      ierror = cast(c1, item0)
      ierror = output_list%getitem(item1, 1)
      ierror = cast(c2, item1)
      ierror = output_list%getitem(item2, 2)
      ierror = cast(c3, item2)
      ierror = output_list%getitem(item3, 3)
      ierror = cast(cvl, item3)

      ihsrcl = 0 !1 if heat source is to be taken into account for this material
      ! hsrcl = 0. !heat source (Energy/Time/Volume)

   else

      c1 = r_matp(8 + 1)
      c2 = r_matp(8 + 2)
      c3 = r_matp(8 + 3)
      cvl = r_matp(8 + 4) !specific heat capacity (Energy/Mass/Temperature)

      ihsrcl = 0 !1 if heat source is to be taken into account for this material
      ! hsrcl = 0. !heat source (Energy/Time/Volume)

   end if

   call args%destroy
   call py_module%destroy
   call return_value%destroy
   call output_list%destroy
   call item0%destroy
   call item1%destroy
   call item2%destroy
   call item3%destroy

   return
end

subroutine utan44(cm, eps, sig, epsp, hsv, dt1, unsym, capa, etype, tt, temper, es, crv, nnpcrv, failel, cma, qmat)
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

subroutine umat44v(cm, d1, d2, d3, d4, d5, d6, sig1, sig2, sig3, sig4, sig5, sig6, epsps, hsv, lft, llt, dt1siz, capa, etype, tt, temps, failels, nlqa, crv, nnpcrv, cma, qmat, elsizv, idelev, reject)
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

   stop "Not implemented: umat44v"

   return
end

subroutine utan44v(cm, d1, d2, d3, d4, d5, d6, sig1, sig2, sig3, sig4, sig5, sig6, epsps, hsvs, unsym, lft, llt, dt1siz, capa, etype, tt, temps, dsave, nlqa, crv, nnpcrv, failels, cma, qmat)
   include 'nlqparm'
   dimension d1(*), d2(*), d3(*), d4(*), d5(*), d6(*)
   dimension sig1(*), sig2(*), sig3(*), sig4(*), sig5(*), sig6(*)
   dimension epsps(*), hsvs(nlq, *), dt1siz(*), cm(*), qmat(nlq, 3, 3)
   dimension temps(*), dsave(nlq, 6, *), crv(lq1, 2, *), cma(*)
   integer nnpcrv(*)
   logical failels(*), unsym
   character*5 etype

   stop "Not implemented: utan44v"

   return
end
