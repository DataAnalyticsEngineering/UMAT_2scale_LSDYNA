$# LS-DYNA Keyword file created by LS-PrePost(R) V4.9 (Beta) - 10May2021
$# Created on Jun-22-2021 (14:02:00)
*KEYWORD
*TITLE
$#                                                                         title
LS-DYNA keyword deck by LS-PrePost
$ *CONTROL_IMPLICIT_DYNAMICS
$ 1
$ *CONTROL_IMPLICIT_EIGENVALUE
$ 12
$ *CONTROL_SOLID
$          1
$ *CONTROL_ACCURACY
$ $#     osu       inn    pidosu      iacc    
$          1         1         0         1
*CONTROL_IMPLICIT_AUTO
$#   iauto    iteopt    itewin     dtmin     dtmax     dtexp     kfail    kcycle
         0        11         5       0.0       0.0       0.0         0         0
*CONTROL_IMPLICIT_GENERAL
$#  imflag       dt0    imform      nsbs       igs     cnstn      form    zero_v
         1       0.1         2         1         2         0         0         0
*CONTROL_SOLUTION
$#    soln       nlq     isnan     lcint     lcacc     ncdcf     nocop     
         2         0         0       100         0         1         0
*CONTROL_STRUCTURED
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
       0.3         0       0.0       0.01.000000E8         0
*CONTROL_THERMAL_SOLVER
$#   atype     ptype    solver         -       gpt    eqheat     fwork       sbc
         1         0        12                   1       1.0         1       0.0
*CONTROL_THERMAL_TIMESTEP
$#      ts       tip       its      tmin      tmax     dtemp      tscp      lcts
         1       1.0       0.1       0.1       0.1      50.0       0.5         0
*DATABASE_TPRINT
$#      dt    binary      lcur     ioopt     
       0.1         0         0         1
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.1         0         0         0         0
$#   ioopt      rate    cutoff    window      type      pset    
         0       0.0       0.0       0.0         0         0
*DATABASE_EXTENT_BINARY
$#   neiph     neips    maxint    strflg    sigflg    epsflg    rltflg    engflg
         0         0         3         0         1         1         1         1
$#  cmpflg    ieverp    beamip     dcomp      shge     stssz    n3thdt   ialemat
         0         0         0         1         1         1         2         1
$# nintsld   pkp_sen      sclp     hydro     msscl     therm    intout    nodout
         8         0       1.0         0         0         2                    
$         8         0       1.0         0         0         2ALL       ALL
$#    dtdt    resplt     neipb     quadr     cubic     
         1         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         1         1         1         1         1         1
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         2         0         1         0         0         1         0         0
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         3         0         0         1         0         0         1         0
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         4         0         0         0         1         0         0         1
*BOUNDARY_TEMPERATURE_SET
$#    nsid      lcid     cmult       loc    tdeath    tbirth      
         5        33       1.0         01.00000E20       0.0
$
$---------------  define model geometry and material parameters ----------------
$
*PART
$#                                                                         title
block
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         1
*SECTION_SOLID
$         1         2         0                                       0
$ 1,101
$ 8,0,1
$ -0.5774,-0.5774,-0.5774,1.0
$  0.5774,-0.5774,-0.5774,1.0
$  0.5774, 0.5774,-0.5774,1.0
$ -0.5774, 0.5774,-0.5774,1.0
$ -0.5774,-0.5774, 0.5774,1.0
$  0.5774,-0.5774, 0.5774,1.0
$  0.5774, 0.5774, 0.5774,1.0
$ -0.5774, 0.5774, 0.5774,1.0
$#   secid    elform       aet    unused    unused    unused    cohoff    unused
         1       101         0                                       0          
$#     nip     nxdof      ihgf      itaj       lmc      nhsv    
         1         0         1         0         0         0
$#      xi       eta      zeta       wgt   
       0.0       0.0       0.0       8.0
*MAT_USER_DEFINED_MATERIAL_MODELS
$#     mid        ro        mt       lmc       nhv    iortho     ibulk        ig
         1      2700        41         8        13         0         4         3
$#   ivect     ifail    itherm    ihyper      ieos      lmca    unused    unused
         0         0         1         0         0         0                    
$#      p1        p2        p3        p4        p5        p6        p7        p8
7.00000E10       0.35.83330E102.69230E10         0         0         0         0
*MAT_THERMAL_USER_DEFINED
$#    tmid        ro        mt       lmc       nhv      aopt    iortho      ihve
         1      2700        11         8        13       0.0         0         0
$#      p1        p2        p3        p4        p5        p6        p7        p8
     400.0     400.0     400.0     383.0       0.0       0.0       0.0       0.0
*INITIAL_TEMPERATURE_SET
$#    nsid      temp       loc   
         0       0.5         0
*DEFINE_FUNCTION
$#     fid                                                               heading
        33                                                                      
$#                                                                      function
float f(float x,float y,float z,float vx,float vy,float vz,float time)
{
$ the set is assumed to contain only the surfaces
$ x,y,z are the coordinates at the current time
float gradx,grady,gradz;
gradx=1.0; grady=1.0; gradz=1.0;
return 0.5 + x*gradx + y*grady + z*gradz;
}
*INCLUDE
$#                                                                      filename
mesh_1el.k
*END
