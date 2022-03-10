$# LS-DYNA Keyword file created by LS-PrePost(R) V4.9 (Beta) - 07Mar2022
$# Created on Mar-9-2022 (17:03:07)
*KEYWORD
*TITLE
$#                                                                         title
LS-DYNA keyword deck by LS-PrePost
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         1         0         0         1         0         0
*SET_NODE_LIST_TITLE
x_sym
$#     sid       da1       da2       da3       da4    solver       its         -
         1       0.0       0.0       0.0       0.0MECH      1                   
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         8         5         1         4         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         2         0         0         1         0         0         1         0
*SET_NODE_LIST_TITLE
y_sym
$#     sid       da1       da2       da3       da4    solver       its         -
         2       0.0       0.0       0.0       0.0MECH      1                   
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         2         6         5         1         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         3         0         0         0         1         0         0         1
*SET_NODE_LIST_TITLE
z_sym
$#     sid       da1       da2       da3       da4    solver       its         -
         3       0.0       0.0       0.0       0.0MECH      1                   
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1         2         4         3         0         0         0         0
*NODE
$#   nid               x               y               z      tc      rc  
       1             0.0             0.0             0.0       0       0
       2             1.0             0.0             0.0       0       0
       3             1.0             1.0             0.0       0       0
       4             0.0             1.0             0.0       0       0
       5             0.0             0.0             1.0       0       0
       6             1.0             0.0             1.0       0       0
       7             1.0             1.0             1.0       0       0
       8             0.0             1.0             1.0       0       0
       9             0.5             0.0             0.0       0       0
      10             1.0             0.5             0.0       0       0
      11             0.5             1.0             0.0       0       0
      12             0.0             0.5             0.0       0       0
      13             0.5             0.0             1.0       0       0
      14             1.0             0.5             1.0       0       0
      15             0.5             1.0             1.0       0       0
      16             0.0             0.5             1.0       0       0
      17             0.0             0.0             0.5       0       0
      18             1.0             0.0             0.5       0       0
      19             1.0             1.0             0.5       0       0
      20             0.0             1.0             0.5       0       0
      21             0.5             0.5             0.0       0       0
      22             0.5             0.5             1.0       0       0
      23             0.5             0.0             0.5       0       0
      24             1.0             0.5             0.5       0       0
      25             0.5             1.0             0.5       0       0
      26             0.0             0.5             0.5       0       0
      27             0.5             0.5             0.5       0       0
*ELEMENT_SOLID
$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8
       2       1       1       9      21      12      17      23      27      26
       3       1       2      10      21       9      18      24      27      23
       4       1       3      11      21      10      19      25      27      24
       5       1       4      12      21      11      20      26      27      25
       6       1      17      23      27      26       5      13      22      16
       7       1      18      24      27      23       6      14      22      13
       8       1      19      25      27      24       7      15      22      14
       9       1      20      26      27      25       8      16      22      15
$$ uncomment below to clamp the block from the top
$ *BOUNDARY_SPC_SET
$ $#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
$          4         0         1         1         1         0         0         0
$ *DEFINE_CURVE
$ 10
$ 0.0, 0.0
$ 1.0, 0.01
$ 2.0, 0.01
$ *BOUNDARY_PRESCRIBED_MOTION_SET
$ $#    nsid       dof       vad      lcid        sf       vid     death     birth
$          4         3         2        10       1.0         01.00000E28       0.0
*SET_NODE_LIST_TITLE
z_top
$#     sid       da1       da2       da3       da4    solver       its         -
         4       0.0       0.0       0.0       0.0MECH      1                   
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         5         8         7         6         0         0         0         0
*END
