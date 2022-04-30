*KEYWORD
*PARAMETER
Rendtim, 1
Rtemp_0, 293.15
Rdtmin, 0.01
Rdtmax, 0.01
Rdt0, 0.01
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
*CONTROL_IMPLICIT_SOLUTION
$#  nsolvr    ilimit    maxref     dctol     ectol     rctol     lstol    abstol
        12                        1.0e-6                           0.9  1.00E-20
$# nlprint: output solver satus ...
$#   dnorm    diverg     istif   nlprint    nlnorm   d3itctl     cpchk
         1         1         1         3         4         0         0
$

$    LSMTD
         5
*CONTROL_STRUCTURED
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         2         0         0       500         0         1         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
   &endtim         0         0       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver         -       gpt    eqheat     fwork       sbc
         1         1        12                   0       1.0 1.000E-15       0.0
$#  msglvl    maxitr    abstol    reltol     omega    unused    unused       tsf

*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         1       1.0      &dt0    &dtmin    &dtmax       1.0       0.5         0
*PART
$#                                                                         title
block
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         1
*SECTION_SOLID
$#   secid    elform       aet    unused    unused    unused    cohoff   gaskeit
         1        -2         0                                     0.0          
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.1
*DATABASE_EXTENT_BINARY
$#   neiph     neips    maxint    strflg    sigflg    epsflg    rltflg    engflg
        14        14        -1       111         1         1         1         1
$#  cmpflg    ieverp    beamip     dcomp      shge     stssz    n3thdt   ialemat
         0         0         0         1         1         1         2         1
$# nintsld   pkp_sen      sclp     hydro     msscl     therm    intout    nodout
         8         0       1.0         0         0         2ALL       ALL
$#    dtdt    resplt     neipb     quadr     cubic     
         1         1         0         0         0
*DATABASE_HISTORY_SOLID
$#     id1       id2       id3       id4       id5       id6       id7       id8
         8         0         0         0         0         0         0         0
*DATABASE_ELOUT
$#      dt    binary      lcur     ioopt   option1   option2   option3   option4
      &dt0         0         0         1         0         0         0         0
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         0   &temp_0         0
*BOUNDARY_TEMPERATURE_NODE
         7       111        1.
*BOUNDARY_TEMPERATURE_SET
         4       222        1.
*DEFINE_CURVE
111
0.0, &temp_0
0.5, 380
0.9, &temp_0
&endtim, &temp_0
*DEFINE_CURVE
222
0.0, &temp_0
0.5, 380
0.9, &temp_0
&endtim, &temp_0
*INCLUDE
mesh_8element.k
mat_44.k
*END
$ @380K thermal strain [0.00135376 0.00135376 0.00135376 0.         0.         0.        ]
