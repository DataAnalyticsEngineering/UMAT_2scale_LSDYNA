      ! type(Tensor4s) vol_av_tangent
      ! common/blk_thermal/thermalhsv
      ! real thermalhsv(nlq,10)

      common/aux9loc/vlrho(nlq),vol(nlq)
c$omp threadprivate (/aux9loc/)
      common/user1loc/last_cycle,weights,
     .vol_av_sig(6),vol_av_flux(3)
c$omp threadprivate (/user1loc/)

      real*8 nodal_temperature_2d(4),nodal_temperature_3d(8)
      real*8 vol_av_sig,vol_av_flux

      common/bel7loc/ixsld(nlq,8,5),ixshl(nlq,4,5)
     .,bmtrx(nlq,3,3,8*(3+NXDOFUE)),
     . cmtrx(nlq,3,3,8*(3+NXDOFUE)),xdof(nlq,8,NXDOFUE),
     . dxdof(nlq,8,NXDOFUE),xhdof(nlq,8,NXDOFUE),
     . bvec(nlq,8*(3+NXDOFUE)),cvec(nlq,8*(3+NXDOFUE)),
     . frc(nlq,8*(3+NXDOFUE)),
     . stiff(nlq,64*(3+NXDOFUE)*(3+NXDOFUE)),
     . sigv(nlq),
     . gmtrx(nlq,3,3),hmtrx(nlq,3,3),cvltot(nlq),
     . xh1(nlq),xh2(nlq),xh3(nlq),xh4(nlq),
     . xh5(nlq),xh6(nlq),xh7(nlq),xh8(nlq),
     . yh1(nlq),yh2(nlq),yh3(nlq),yh4(nlq),
     . yh5(nlq),yh6(nlq),yh7(nlq),yh8(nlq),
     . zh1(nlq),zh2(nlq),zh3(nlq),zh4(nlq),
     . zh5(nlq),zh6(nlq),zh7(nlq),zh8(nlq),
     . hl11(nlq),hl12(nlq),hl13(nlq),hl21(nlq),hl22(nlq),
     . hl23(nlq),hl31(nlq),hl32(nlq),hl33(nlq),
     . xx1(nlq),xx2(nlq),xx3(nlq),xx4(nlq),
     . xx5(nlq),xx6(nlq),xx7(nlq),xx8(nlq),
     . yy1(nlq),yy2(nlq),yy3(nlq),yy4(nlq),
     . yy5(nlq),yy6(nlq),yy7(nlq),yy8(nlq),
     . zz1(nlq),zz2(nlq),zz3(nlq),zz4(nlq),
     . zz5(nlq),zz6(nlq),zz7(nlq),zz8(nlq),vlm(nlq)

c$omp threadprivate (/bel7loc/)
