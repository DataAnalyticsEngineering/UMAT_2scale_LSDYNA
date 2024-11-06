$ power make it minus
$ BOUNDARY_CONVECTION_SET -> only sides?
$ elem size -> refine
$ CONTROL_THERMAL_TIMESTEP
$ *BOUNDARY_RADIATION

$ thermo-mech -> change eqheat and fwrok, *MAT_CWM
$ solver -> 12
$ tlstart     tlend    of the material
*KEYWORD
*PARAMETER
Rendtim, 30
Rpower, 0.56e9
Rdepth, 0.3
Rradius, 0.95
Rtemp_0, 673.15
Rf_f, 1.0
Rn, 3
*PARAMETER_EXPRESSION
Rf_r, 2-f_f
*CONTROL_ACCURACY
$#     osu       inn    pidosu      iacc    
                                       1         1
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         1         0         0       500         0         1         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
   &endtim         0      1e-2       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver         -       gpt    eqheat     fwork       sbc
         1         1        12                   0       1.0       1.0       0.0
$#  msglvl    maxitr    abstol    reltol     omega    unused    unused       tsf

*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         1       1.0      1e-1      1e-9      1e-1     200.0       0.5         0
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.5
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         0   &temp_0         0
$ *BOUNDARY_TEMPERATURE_SET
$          2         0   &temp_0
*BOUNDARY_CONVECTION_SET
$#    ssid    pserod      
         1         0
$#   hlcid     hmult     tlcid     tmult       loc   
         0      20.0         0   &temp_0         0
*BOUNDARY_CONVECTION_SET
$#    ssid    pserod      
         2         0
$#   hlcid     hmult     tlcid     tmult       loc   
         0      20.0         0    483.15         0
*BOUNDARY_CONVECTION_SET
$#    ssid    pserod      
         3         0
$#   hlcid     hmult     tlcid     tmult       loc   
         0      20.0         0    293.15         0
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
*MAT_THERMAL_CWM_TITLE
copper
$#    tmid       tro     tgrlc    tgmult     hdead     tdead      tlat      hlat
         1         1       0.0       0.0       0.0       0.0   1356.15    206e09
$#    lchc      lctc   tlstart     tlend   tistart     tiend    hghost    tghost
         3         4         0         0       0.0       0.0       0.0       0.0
*SECTION_SOLID
$#   secid    elform       aet    unused    unused    unused    cohoff   gaskeit
         1         2         0                                     0.0          
*PART
$#                                                                         title
substrate
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         0         0         0         0         0         1
*PART
$#                                                                         title
bead
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         2         1         0         0         0         0         0         1
*SET_PART_LIST_TITLE
part_list
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         0         0         0         0         0         0         0
*INCLUDE
mesh.k
curves.k
*END
