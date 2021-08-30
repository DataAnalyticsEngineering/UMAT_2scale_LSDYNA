echo "# diff -u rve_mesh.key rve_mesh_new.key > rve_change_pbc.patch
# patch < rve_change_pbc.patch
# patch -R < rve_change_pbc.patch
--- rve_mesh.key
+++ rve_mesh.key
@@ -3999,10 +3999,10 @@
 *BOUNDARY_SPC_NODE
        400         0         1         1         1
 *BOUNDARY_PRESCRIBED_MOTION_NODE
-      1332         1         2         1 0.100E-01
-      1332         2         2         1 0.100E-15
-      1332         3         2         1 0.100E-15
-      1333         2         2         1 0.100E-15
-      1333         3         2         1 0.100E-15
-      1334         3         2         1 0.100E-15
+      1332         1         2         1 0.100E-01
+      1332         2         2         1 0.100E-02
+      1332         3         2         1 0.100E-03
+      1333         2         2         1 0.100E-04
+      1333         3         2         1 0.100E-05
+      1334         3         2         1 0.100E-06
 *END" > rve_change_pbc.patch && patch < rve_change_pbc.patch
