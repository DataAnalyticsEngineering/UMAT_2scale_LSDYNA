$ change dtemp to get accurate thermal cycles
$ LOAD_THERMAL_D3PLOT
$ thermo-mech -> change eqheat and fwrok, *MAT_CWM
$ *DEFINE_ELEMENT_DEATH_OPTION

$ power make it minus
$ BOUNDARY_CONVECTION_SET -> only sides?
$ elem size -> refine
$ CONTROL_THERMAL_TIMESTEP
$ *BOUNDARY_RADIATION

$ solver -> 12
$ tlstart     tlend    of the material
*KEYWORD
*PARAMETER
Rendtim, 900.0
Rcuttim, 999
Rcuttim2, 999
Rpower, 0.56e9
Rdepth, 0.3
Rradius, 0.95
Rtemp_0, 673.15
Rf_f, 1.0
Rn, 3
Rdtmin, 1e-12
Rdtmax, 50
Rdt0, 1e-12
*PARAMETER_EXPRESSION
Rf_r, 2-f_f
$ *CONTROL_ACCURACY
$ $#     osu       inn    pidosu      iacc    
$ 1,,,1
*CONTROL_IMPLICIT_AUTO
$#   iauto    iteopt    itewin     dtmin     dtmax     dtexp     kfail    kcycle
         2        11         5    &dtmin    &dtmax       0.0         0         0
*CONTROL_IMPLICIT_GENERAL
$#  imflag       dt0    imform      nsbs       igs     cnstn      form    zero_v
         1    &dtmin         2         1         2         0         0         0
*CONTROL_IMPLICIT_SOLVER
$#  lsolvr    lprint     negev     order      drcm    drcprm   autospc   autotol
         2         0         1         0         4       0.0         2       0.0
$#  lcpack    mtxdmp    iparm1    rparm1    rparm2         -         -    rparm5
         2         0       5001.00000E-9     0.001                           0.0
$#  emxdmp    rdcmem    absmem      
         0          
*CONTROL_STRUCTURED
$ *CONTROL_IMPLICIT_DYNAMICS
$ 1
$ *CONTROL_IMPLICIT_EIGENVALUE
$ 12
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         2         0         0      5000         0         1         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
   &endtim         0         0       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver         -       gpt    eqheat     fwork       sbc
         1         1        12                   0       1.0 1.000E-15       0.0
$#  msglvl    maxitr    abstol    reltol     omega    unused    unused       tsf

*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         1       1.0      &dt0    &dtmin    &dtmax    0100.0       0.5         0
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
        50
*DATABASE_EXTENT_BINARY
$#   neiph     neips    maxint    strflg    sigflg    epsflg    rltflg    engflg
        14        14         3       111         1         1         1         1
$#  cmpflg    ieverp    beamip     dcomp      shge     stssz    n3thdt   ialemat
         0         0         0         1         1         1         2         1
$# nintsld   pkp_sen      sclp     hydro     msscl     therm    intout    nodout
         8         0       1.0         0         0         2ALL       ALL
$#    dtdt    resplt     neipb     quadr     cubic     
         1         1         0         0         0
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         0   &temp_0         0
*BOUNDARY_CONVECTION_SET
$#    ssid    pserod      
         1         0
$#   hlcid     hmult     tlcid     tmult       loc   
        10         1         0   &temp_0         0
         2         0
        10         1         0   &temp_0         0
         3         0
        10         1         0   &temp_0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         2         0         1         0         0         0         0         0
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         3         0         0         1         0         0         0         0
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         4         0         0         0         1         0         0         0
*BOUNDARY_SPC_SET_BIRTH_DEATH
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         5         0         1         0         0         0         0         0
$#   birth     death
   &cuttim   &endtim
*DEFINE_ELEMENT_DEATH_SOLID_SET
$#     sid      time     boxid     inout     idgrp       cid   percent       
         1   &cuttim         0         0         0         0       0.0
         2  &cuttim2         0         0         0         0       0.0
$ *BOUNDARY_RADIATION_SET
$ $     ssid      type
$          3         1
$ $    flcid     fmult     tlcid     tmult       loc
$          0      1e-7         0    293.15
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         1         2         1        -1         0       0.0         5         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1         2    &power         0         0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
   &radius    &depth   &radius   &radius      &f_f      &f_r        &n       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*SECTION_SOLID
$#   secid    elform       aet    unused    unused    unused    cohoff   gaskeit
         1         2         0                                     0.0          
*PART
$#                                                                         title
substrate
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         1
*SET_PART_LIST_TITLE
part_list
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         0         0         0         0         0         0         0
$ *LOAD_THERMAL_D3PLOT
*INCLUDE
mesh.k
mat_44.k
curves.k
*END
