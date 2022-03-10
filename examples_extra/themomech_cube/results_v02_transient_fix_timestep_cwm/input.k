*KEYWORD
*PARAMETER
Rendtim, 1
Rtemp_0, 293.15
Rdtmin, 1e-3
Rdtmax, 1e-3
Rdt0, 1e-3
*CONTROL_ACCURACY
$#     osu       inn    pidosu      iacc    
1,,,1
*CONTROL_IMPLICIT_AUTO
$# 2 auto, 0 fixed
$#   iauto    iteopt    itewin     dtmin     dtmax     dtexp     kfail    kcycle
         2                        &dtmin    &dtmax       0.0         0         0
*CONTROL_IMPLICIT_GENERAL
$# 0 explicit, 1 implicit
$#  imflag       dt0    imform      nsbs       igs     cnstn      form    zero_v
         1      &dt0
$*CONTROL_IMPLICIT_SOLVER
$$#  lsolvr    lprint     negev     order      drcm    drcprm   autospc   autotol
$         2         0         1         0         4       0.0         2       0.0
$$#  lcpack    mtxdmp    iparm1    rparm1    rparm2         -         -    rparm5
$         2         0       5001.00000E-9     0.001                           0.0
$$#  emxdmp    rdcmem    absmem      
$         0          
*CONTROL_IMPLICIT_SOLUTION
$#  nsolvr    ilimit    maxref     dctol     ectol     rctol     lstol    abstol
        12         1       500      1e-9      1e-9      1e-9       0.9 1.000E-20
$# nlprint: output solver satus ...
$#   dnorm    diverg     istif   nlprint    nlnorm   d3itctl     cpchk
         1         1         1         0         0         0         0
*CONTROL_STRUCTURED
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         2         0         0       500         0         1         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
   &endtim         0         0       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver     cgtol       gpt    eqheat     fwork       sbc
         1         1        12                   8       1.0       1.0       0.0
$#  msglvl    maxitr    abstol    reltol     omega    unused    unused       tsf

*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         1       1.0      &dt0    &dtmin    &dtmax     003.0       0.5         0
*PART
$#                                                                         title
block
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         1
*SECTION_SOLID
$#   secid    elform       aet    unused    unused    unused    cohoff   gaskeit
         1         2         0                                     0.0          
*SET_PART_LIST_TITLE
part_list
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         0         0         0         0         0         0         0
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.1
*DATABASE_EXTENT_BINARY
$#   neiph     neips    maxint    strflg    sigflg    epsflg    rltflg    engflg
         0         0         3         0         1         1         1         1
$#  cmpflg    ieverp    beamip     dcomp      shge     stssz    n3thdt   ialemat
         0         0         0         1         1         1         2         1
$# nintsld   pkp_sen      sclp     hydro     msscl     therm    intout    nodout
         8         0       1.0         0         0         2ALL       ALL
$#    dtdt    resplt     neipb     quadr     cubic     
         1         0         0         0         0
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         0   &temp_0         0
*BOUNDARY_TEMPERATURE_NODE
      1331       111        1.
$         4       111        1.
$         6       111        1.
*DEFINE_CURVE
111
0.0, &temp_0
0.05, 500.0
0.1, &temp_0
&endtim, &temp_0
*INCLUDE
mesh_1000element.k
$ mat_thermoelastic.k
$ mat_thermoplastic.k
mat_cwm.k
*END
