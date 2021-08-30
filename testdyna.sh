# carefull when editing files included via include, use make -B to force updating the binary

# ngp through thickness
# *SECTION_TSHELL
# NIP

# one element test before incresing #ngp or element order
# double check that the imposed gradient is recovered ...

# fprettify umat_elastic_44_14.F90 umat_elastic_43_13.F90 -l 200

# 43 micro
# 44 macro

# meld /home/alameddin/.dontsync/arch_usrmat/ref_ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160/usermat src/pyrve/lsdyna_object_version/
# updateintel
# /bin/bash -c updateintel
source /home/alameddin/.dontsync/packages/intel/oneapi/setvars.sh --force
make
rm -rf /tmp/del_keyfiles
cp -r keyfiles /tmp/del_keyfiles
# cp -r cp01 /tmp/del_keyfiles
# cd /tmp/del_keyfiles && rm -rf d3* && ./../lsdyna i=simple_block_input.k | tee output.txt && cat output.txt | grep --color=always -i 'fail\|err\|war' && lsprepost d3plot && cd ..

# cd /tmp/del_keyfiles/2d_rve && umatdyna i=geo_2d_input.k && cd ../..
cd /tmp/del_keyfiles/macro_simple_block && umatdyna i=macro_simple_block_input.k && cd ../..

# cd /tmp/del_keyfiles/2d_rve && umatdyna i=geo_2d_input.k && lsprepost d3plot && cd ../..
# cd /tmp/del_keyfiles/2d_rve && umatdyna i=geo_2d_input.k && cd ../..
# ####cd /tmp/del_keyfiles && rm -rf d3* && ./../lsdyna i=cp02_macro.k && cd ..
# cd /tmp/del_keyfiles && rm -rf d3* && ./../lsdyna i=thermal-stress2.k && cd ..
# cd /tmp/del_keyfiles && rm -rf d3* && ./../lsdyna i=thermal-stress.k && cat dae_rve.txt && cd ..


# search for incore & outofcore (bad:/ add memory)


# thermoelastic
# Periodic three-dimensional mesh generation for particle reinforced composites with application to metal matrix composites

# plastic
# the_finite_element_square_reduced_fe2r_method_with_gpu_acceleratio

# tangent
# spahn_A multiscale approach for modeling progressive damage of.pdf
# Kouznetsova2001_Article_AnApproachToMicro-macroModelin


# tumat
# common/blk_thermal/thermalhsv
# real thermalhsv(nlq,10)
# include 'nhisparm.inc'
# common/bel7loc/ixsld(nlq,8,5),ixshl(nlq,4,5)
# .,bmtrx(nlq,3,3,8*(3+NXDOFUE))
# c
#  200  continue
#       if (.not.(eltype.eq.'soliddt'.or.eltype.eq.'shelldt'.or.
#      1     eltype.eq.'solid_ie'.or.eltype.eq.'shell_ie'.or.
#      2     eltype.eq.'tshell_ie'.or.eltype.eq.'flux')) then
#         do i=1,nvh
#           hsv(iphsv(nel)+(iep-1)*nvh+i)=hstored(i)
#           thermalhsv(iphsv(nel)+(iep-1)*nvh+1,i) = hstored(i)
#         enddo
#       endif
# 
# 
#       ! write(*,*) bmtrx(1,1,1,1:24)
#       ! write(*,*) '----'
#       ! write(*,*) '--tumat--'
#        !    ,
#        ! .  -a(ntmp0+1:ntmp0+8)),dot_product(bmtrx(1,2,2,2:24:3),
#        ! .
#        !    common/bel7loc/ixsld(nlq,8,5),ixshl(nlq,4,5)
#        !   .,bmtrx(nlq,3,3,8*(3+NXDOFUE)),
#       ! 3     time-dt,time,tt-dt1,tt
#       ! write(*,*) '1**', hsv(1:3)
#       ! write(*,*) '2**', hstored(1:3)
#       ! ! write(*,*) '3**', r_matp(1:10)
#       ! write(*,*) '7**', hsv2(1:3)