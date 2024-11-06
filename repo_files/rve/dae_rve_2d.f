      if (ncycle>last_cycle) then
        ! zero all variables
        weights=0.0
        vol_av_sig(:) = 0.
        vol_av_flux(:) = 0.

        last_cycle=ncycle
      endif
      
      do i=lft,llt
        weights = weights+vol(i)
        vol_av_sig = vol_av_sig + vol(i) *
     .    [sig1(i),sig2(i),sig3(i),sig4(i),sig5(i),sig6(i)]
        ! vol_av_tangent = vol_av_tangent + symstore_4sa(hsvs(i,2:37))
        ! * voln(i) / weights

        ! node id ix1(element_id)
        nodal_temperature_2d = [a(ntmp0+ix1(i)), a(ntmp0+ix2(i)),
     .    a(ntmp0+ix3(i)), a(ntmp0+ix4(i))]

        ! TODO: change & read from material ...
        hc1 = 383.0

        ! refer to ushl or usld
        vol_av_flux(1:3) = vol_av_flux(1:3) + [ (
     .    dot_product(bmtrx(i,1,ll,1:24:6),
     .     nodal_temperature_2d),ll=1,3) ] * vol(i) *
     .     [ -hc1,hc1,-hc1 ]
        ! TODO: temporary fix (yy) direction no - sign
      enddo
