*KEYWORD
*ELEMENT_SOLID
$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8
       1       1       1       2       3       4       5       6       7       8
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
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         1         0         0         1         0         0
*SET_NODE_LIST_TITLE
x_sym
$#     sid       da1       da2       da3       da4    solver
         1       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         8         5         1         4         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         2         0         0         1         0         0         1         0
*SET_NODE_LIST_TITLE
y_sym
$#     sid       da1       da2       da3       da4    solver
         2       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         2         6         5         1         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         3         0         0         0         1         0         0         1
*SET_NODE_LIST_TITLE
z_sym
$#     sid       da1       da2       da3       da4    solver
         3       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1         2         4         3         0         0         0         0
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
$#     sid       da1       da2       da3       da4    solver
         4       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         5         8         7         6         0         0         0         0
*END
