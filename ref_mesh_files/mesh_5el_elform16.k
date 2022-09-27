$# LS-DYNA Keyword file created by LS-PrePost(R) V4.9 (Beta) - 10May2021
$# Created on Jun-24-2021 (22:28:54)
*KEYWORD
*TITLE
$#                                                                         title
LS-DYNA keyword deck by LS-PrePost
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         4         0         0         0         0         0         0         0
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         2       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         2        15         4        17         8        19        21         6
        23         0         0         0         0         0         0         0
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         3       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         4        16         3        18         8        17        26         7
        25         0         0         0         0         0         0         0
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         4       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1        11         3        10         2         9        16         4
        15         0         0         0         0         0         0         0
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         5       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         2        15         4        17         8        19        21         6
        23         1         3         5         7         9        10        11
        12        13        14        16        18        20        22        24
        25        26         0         0         0         0         0         0
*ELEMENT_SOLID (ten nodes format)
$#   eid     pid   
       1       1
$#    n1      n2      n3      n4      n5      n6      n7      n8      n9     n10
       1       2       3       5       9      10      11      12      13      14
       2       1
       2       4       3       8      15      16      10      17      18      19
       3       1
       2       5       8       3      12      20      19      13      18      10
       4       1
       2       8       5       6      19      20      12      21      22      23
       5       1
       3       5       8       7      13      20      18      24      25      26
*NODE
$#   nid               x               y               z      tc      rc  
       1             0.0             0.0             0.0       0       0
       2             1.0             0.0             0.0       0       0
       3             0.0             1.0             0.0       0       0
       4             1.0             1.0             0.0       0       0
       5             0.0             0.0             1.0       0       0
       6             1.0             0.0             1.0       0       0
       7             0.0             1.0             1.0       0       0
       8             1.0             1.0             1.0       0       0
       9             0.5             0.0             0.0       0       0
      10             0.5             0.5             0.0       0       0
      11             0.0             0.5             0.0       0       0
      12             0.5             0.0             0.5       0       0
      13             0.0             0.5             0.5       0       0
      14             0.0             0.0             0.5       0       0
      15             1.0             0.5             0.0       0       0
      16             0.5             1.0             0.0       0       0
      17             1.0             1.0             0.5       0       0
      18             0.5             1.0             0.5       0       0
      19             1.0             0.5             0.5       0       0
      20             0.5             0.5             1.0       0       0
      21             1.0             0.5             1.0       0       0
      22             0.5             0.0             1.0       0       0
      23             1.0             0.0             0.5       0       0
      24             0.0             0.5             1.0       0       0
      25             0.5             1.0             1.0       0       0
      26             0.0             1.0             0.5       0       0
*END
