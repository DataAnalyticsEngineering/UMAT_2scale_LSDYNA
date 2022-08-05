$# LS-DYNA Keyword file created by LS-PrePost(R) V4.8.13 - 19Mar2021
$# Created on Jun-30-2021 (18:26:45)
*KEYWORD
*INCLUDE
MESH1.k
Material_Activation.key
Part_Material_assign2.key
*CONTROL_ACCURACY
$#     osu       inn    pidosu      iacc    
         0         1         0         1
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         1         0         0       100         0         1         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
     100.0         0       0.0       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver     cgtol       gpt    eqheat     fwork       sbc
         1         1        111.00000E-4         8       1.0       1.0       0.0
$#  msglvl    maxitr    abstol    reltol     omega    unused    unused       tsf
         0       5001.0000E-101.00000E-4       1.0                           1.0
$#   mxdmp      dtvf    varden      
         0       0.0         0
*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         0       1.0       0.1       0.0       0.0       1.0       0.5         0
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.5         0         0         0         0
$#   ioopt      rate    cutoff    window      type      pset    
         0       0.0       0.0       0.0         0         0
*BOUNDARY_CONVECTION_SET
$#    ssid    pserod      
         1         0
$#   hlcid     hmult     tlcid     tmult       loc   
         0      10.0         0     293.0         0
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         1         2         1        -1         0       0.0        10         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1         22.000000E9         0         0         0       0.0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
       1.0       1.0       1.0       1.0       1.0       1.0       3.0       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         2         2         2        -3         0       0.0        10         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1         42.000000E9         0         0         0       0.0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
       1.0       1.0       1.0       1.0       1.0       1.0       3.0       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         3         2         3        -5         0       0.0        10         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1         62.000000E9         0         0         0       0.0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
       1.0       1.0       1.0       1.0       1.0       1.0       3.0       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         4         2         4        -7         0       0.0        10         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1         82.000000E9         0         0         0       0.0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
       1.0       1.0       1.0       1.0       1.0       1.0       3.0       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*BOUNDARY_THERMAL_WELD_TRAJECTORY
$#     pid      ptyp     nsid1      spd1     nsid2      spd2      ncyc    relvel
         5         2         5        -9         0       0.0        10         0
$#   iform      lcid         q     lcrot     lcmov     lclat      disc     enfor
         1        102.000000E9         0         0         0       0.0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
       1.0       1.0       1.0       1.0       1.0       1.0       3.0       0.0
$#      tx        ty        tz  
       0.0       0.0      -1.0
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         7     293.0         0
*DEFINE_CURVE_TITLE
speed1
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         1         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                 0.1                 5.0
                 7.9                 5.0
                 8.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
energy1
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         2         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                 0.1                 1.0
                 7.9                 1.0
                 8.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
speed2
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         3         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                16.0                 0.0
                16.1                 5.0
                23.9                 5.0
                24.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
energy2
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         4         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                16.0                 0.0
                16.1                 1.0
                23.9                 1.0
                24.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
speed3
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         5         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                32.0                 0.0
                32.1                 5.0
                39.9                 5.0
                40.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
energy3
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         6         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                32.0                 0.0
                32.1                 1.0
                39.9                 1.0
                40.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
speed4
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         7         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                48.0                 0.0
                48.1                 5.0
                55.9                 5.0
                56.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
energy4
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         8         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                48.0                 0.0
                48.1                 1.0
                55.9                 1.0
                56.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
speed5
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         9         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                64.0                 0.0
                64.1                 5.0
                71.9                 5.0
                72.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
energy5
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
        10         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                64.0                 0.0
                64.1                 1.0
                71.9                 1.0
                72.0                 0.0
               100.0                 0.0
*DEFINE_CURVE_TITLE
HeatCapacity
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
        11         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
               293.0    3.8348000000e+08
               400.0    3.9844000000e+08
               500.0    4.0800000000e+08
               600.0    4.1700000000e+08
               700.0    4.2500000000e+08
               800.0    4.3200000000e+08
               900.0    4.4100000000e+08
              1000.0    4.5100000000e+08
              1100.0    4.6400000000e+08
              1200.0    4.8000000000e+08
              1300.0    5.0600000000e+08
              2500.0    5.0600000000e+08
*DEFINE_CURVE_TITLE
HeatCond
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
        12         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
               293.0            400680.0
               400.0            393000.0
               500.0            386500.0
               600.0            379000.0
               700.0            372800.0
               800.0            366000.0
               900.0            359110.0
              1000.0            352000.0
              1100.0            345410.0
              1200.0            339000.0
              1300.0            331710.0
              2500.0            331710.0
*END
