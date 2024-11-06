# get jacobian and integration ... // getDerivative //

import numpy as np
import cv2 as cv
import itertools
import gmsh

#%% 3D

xmin, ymin, zmin = [0, 0, 0]
dx = dy = dz = 1

pos_and_r = [[0.5,0.5,0.5,0.3634]]
r2 = 0.3621
for xyz in itertools.product([0,dx], [0,dy], [0,dz]):
    pos_and_r.append([*xyz,r2])


dim_0d, dim_1d, dim_2d, dim_3d = [0, 1, 2, 3]

gmsh.initialize()
model = gmsh.model
geo = model.occ

matrix = geo.addBox(xmin, ymin, zmin, dx, dy,dz)
matrix2 = geo.addBox(xmin, ymin, zmin, dx, dy,dz)

inclusions = []
for pos_r in pos_and_r:
    inclusions.append((dim_3d,geo.addSphere(*pos_r)))

# spherical/circular inclusions, whose mesh should be conformal with the mesh of the cube/square
# i.e. intersects all volumes/areas in a conformal manner (without creating duplicate interfaces)
# geo.cut([(dim_2d, matrix)], [(dim_2d, cir)], removeTool=False) # same as fuse?
outDimTags, _ = geo.fragment([(dim_3d, matrix)], inclusions)
outDimTags, _ = geo.intersect([(dim_3d, matrix2)], outDimTags)

geo.synchronize()  # this is a must before defining pyysical groups

gmsh.option.setNumber("Mesh.SaveAll", 0)
gmsh.option.setNumber("Mesh.SaveGroupsOfElements", 1)
gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)

# gmsh.option.setNumber("Mesh.RecombineAll", 1)
# gmsh.option.setNumber("Mesh.Algorithm", 8)
# # gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)
# gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 2)  # or 3
# gmsh.option.setNumber("Mesh.Smoothing", 10)

# gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.2)
# gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
gmsh.option.setNumber("Mesh.MeshSizeMin", dx/50)
gmsh.option.setNumber("Mesh.MeshSizeMax", dx/20)
# model.mesh.setSize(model.getBoundary(inclusions, False, False, True), dx/50)

# gmsh.option.setNumber('Mesh.Algorithm3D', 10) # faster
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)

# model.mesh.generate(dim_3d)
gmsh.write("geo_3d_rve_mesh2.geo_unrolled")

gmsh.fltk.run()
gmsh.finalize()






#%% 2D
# fix the z component in 2D
# save pixel and voxel versions ... cadquery
xmin, ymin, zmin = [0, 0, 0]
dx, dy = [1, 1]

pos1 = [0.08, 0.35, 0.0]
pos2 = [0.5, 0.5, 0.0]

dim_0d, dim_1d, dim_2d, dim_3d = [0, 1, 2, 3]

gmsh.initialize()
model = gmsh.model
geo = model.occ

rec = geo.addRectangle(xmin, ymin, zmin, dx, dy)

cir = geo.addDisk(pos1[0], pos1[1], pos1[2], 0.05, 0.05)
cir2 = geo.addDisk(pos2[0], pos2[1], pos2[2], 0.1, 0.1)
inclusions = [(dim_2d, cir2), (dim_2d, cir)]

# spherical/circular inclusions, whose mesh should be conformal with the mesh of the cube/square
# i.e. intersects all volumes/areas in a conformal manner (without creating duplicate interfaces)
# geo.cut([(dim_2d, rec)], [(dim_2d, cir)], removeTool=False) # same as fuse?
outDimTags, _ = geo.fragment([(dim_2d, rec)], inclusions)

geo.synchronize()  # this is a must before defining pyysical groups
group_matrix = model.addPhysicalGroup(dim_2d, [outDimTags[-1][-1]])
model.setPhysicalName(dim_2d, group_matrix, "matrix")
# Not working as expected TODO open an issue:
# https://gitlab.onelab.info/gmsh/gmsh/-/issues?scope=all&utf8=%E2%9C%93&state=opened&search=physical
# the output is correct in gmsh but not in the extracted .key file
group_inclusions = model.addPhysicalGroup(dim_2d, [cir, cir2])
model.setPhysicalName(dim_2d, group_inclusions, "inclusions")
geo.synchronize()

gmsh.option.setNumber("Mesh.SaveAll", 0)
gmsh.option.setNumber("Mesh.SaveGroupsOfElements", 1)
gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)

gmsh.option.setNumber("Mesh.RecombineAll", 1)
gmsh.option.setNumber("Mesh.Algorithm", 8)
# gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 2)  # or 3
gmsh.option.setNumber("Mesh.Smoothing", 10)

# gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.2)
# gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
gmsh.option.setNumber("Mesh.MeshSizeMin", dx/100)
gmsh.option.setNumber("Mesh.MeshSizeMax", dx/30)
model.mesh.setSize(model.getBoundary(inclusions, False, False, True), dx/50)

# gmsh.option.setNumber('Mesh.Algorithm3D', 10) # faster
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)


bc = model.getBoundary([(2, 4)], combined=False)
bottom = bc[0]
top = bc[2]
right = bc[1]
left = bc[3]

group_top = model.addPhysicalGroup(dim_1d, [top[-1]])
model.setPhysicalName(dim_1d, group_top, "top")
group_left = model.addPhysicalGroup(dim_1d, [left[-1]])
model.setPhysicalName(dim_1d, group_left, "left")
group_right = model.addPhysicalGroup(dim_1d, [right[-1]])
model.setPhysicalName(dim_1d, group_right, "right")
group_bottom = model.addPhysicalGroup(dim_1d, [bottom[-1]])
model.setPhysicalName(dim_1d, group_bottom, "bottom")

# # To impose that the mesh on surface 2 (the right side of the cube) should
# # match the mesh from surface 1 (the left side), the following periodicity
# # constraint is set:
translation_x = [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
translation_y = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
translation_z = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1]
model.mesh.setPeriodic(dim_1d, [right[-1]], [left[-1]], translation_x)
model.mesh.setPeriodic(dim_1d, [top[-1]], [bottom[-1]], translation_y)

model.mesh.generate(dim_2d)
# gmsh.model.mesh.refine()
# gmsh.write("geo_2d_rve_mesh.key")
# gmsh.write("geo_2d_rve_mesh.geo_unrolled")
# gmsh.write("geo_2d_rve_mesh.msh")

# numElem = 0
# for g in [group_top,group_left,group_right,group_bottom]:
#     elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim_1d, g)
#     numElem += sum(len(i) for i in elemTags)

# from qd.cae.dyna import *
# read a keyfile
# kf = KeyFile("geo_2d_rve_mesh.key",read_keywords=True,parse_mesh=False,load_includes=True)
# print(kf['*ELEMENT_SHELL'][0])
# kf.save("geo_2d_rve_mesh2.key")

gmsh.fltk.run()
gmsh.finalize()

# with open("geo_2d_rve_mesh.key") as f:
#     newText = f.read().replace('2000002','2')
#     newText = newText.replace('2000003','2')
#     newText = newText.replace('2000004','1')
#
# with open("geo_2d_rve_mesh.key", 'w') as f:
#     f.write(newText)
#
# import subprocess
# subprocess.call(['/bin/bash', '-i', '-c', 'lsprepost save_with_lsprepost.cfile && rm -rf lspost*'])


# # refine
# # based on an embedded point
# lc = 0.01
# pp = geo.addPoint(3, pos1[1], pos1[2],lc)
# geo.mesh.setSize([(0,pp)],10)
# geo.synchronize()
# gmsh.model.mesh.embed(0, [pp], 2, rec)
# # based on curvature
# gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 20)

# gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
# gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
# gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# v = gmsh.view.add("comments")
# gmsh.view.addListDataString(v, [10, -10], ["Created with Gmsh"])
# gmsh.view.addListDataString(v, [0, 0.11, 0], ["Hole"], ["Align", "Center", "Font", "Helvetica"])


#%% cadquery
# # when using cut, the tool is always removed and adding it again results in duplicate nodes in gmsh
# import cadquery as cq
#
# def generate_2d_rve(dx,dy, positions, rads, count):
#     # dx = dy = dz = ll
#     height = 0.2
#     result = cq.Workplane(origin=(0, 0, 0)).rect(dx, dy, centered=False).extrude(height)
#     box = cq.Workplane(origin=(0, 0, 0)).rect(dx, dy, centered=False).extrude(height)
#     for position, rad in zip(positions, rads):
#         # p = cq.Workplane(origin=(*position, 0)).circle(rad).extrude(height)
#         p = cq.Workplane(origin=position).circle(rad).extrude(height)
#         result = result.cut(p)
#         result = result.add(box.intersect(p))
#     result = result.faces("<Z")
#     cq.exporters.export(result, f'rve_identification/geo_2d_{dx}_{count}.step', 'STEP')
#
#
# def generate_3d_rve(ll, positions, rads, count):
#     dx = dy = dz = ll
#     result = cq.Workplane(origin=(0, 0, 0)).box(dx, dy, dz, centered=(False, False, False))
#     box = cq.Workplane(origin=(0, 0, 0)).box(dx, dy, dz, centered=(False, False, False))
#     for position, rad in zip(positions, rads):
#         p = cq.Workplane(origin=position).sphere(rad)
#         result = result.cut(p)
#         result = result.add(box.intersect(p))
#     cq.exporters.export(result, f'geo_3d_{ll}_{count}.step', 'STEP')
#
# ll=151
# positions=[(70,30)]
# rads=[25]
# generate_2d_rve(ll,positions,rads,0)


#%% pygmsh
#     # ideal to use inside a FEM code but couldn't write dyna key file
#     #     at the moment.
#     #     coudn't do fragment ...
# import pygmsh
#
# with pygmsh.occ.Geometry() as geom:
#     xmin,ymin,zmin = [-3, -2, 0]
#     h,w = [4,8]
#
#     pos1 = [0, 0.0, 0.0]
#     pos2 = [1, 1, 0.0]
#     rectangle = geom.add_rectangle([xmin, ymin, zmin], w, h)
#     disk1 = geom.add_disk(pos1, 0.3)
#     disk2 = geom.add_disk(pos2, 0.3)
#
#     cut = geom.boolean_difference(rectangle, disk1)
#     geom.boolean_difference(rectangle, disk2)
#
#     geom.add_disk(pos1, 0.3)
#     mesh = geom.generate_mesh()
#
#     mesh.write("out.vtk")

#%% netgen
# from ngsolve import *
# from netgen.geom2d import SplineGeometry
#
# geo = SplineGeometry()
# p1,p12a,p12b,p2,p3,p4 = [ geo.AppendPoint(x,y) for x,y in [(-5,5),(-5,2),(-5, -2),(-5,-5),(5,-5),(5,5)] ]
#
# geo.SetMaterial(1, "background")
# geo.SetMaterial(2, "circles")
#
# # In NetGen, regions are defined using 'left' and 'right',
# # For example, leftdomain=2, rightdomain=1  means when moving from a
# # from a point A to B, region 2 is always on the left side and
# # region 1 is on the right.
#
# geo.Append (["line", p1, p12a], leftdomain=1, bc="boundary1")
# geo.Append (["line", p12a, p12b], leftdomain=1, bc="lightsource")
# geo.Append (["line", p12b, p2], leftdomain=1, bc="boundary1")
# geo.Append (["line", p2, p3], leftdomain=1, bc="boundary1")
# geo.Append (["line", p3, p4], leftdomain=1, bc="boundary1")
# geo.Append (["line", p4, p1], leftdomain=1, bc="boundary1")
#
# geo.AddCircle(c=(1,1), r=1, leftdomain=2,rightdomain=1)
# geo.AddCircle(c=(-2,-2), r=2, leftdomain=2,rightdomain=1)
#
# mesh = geo.GenerateMesh(maxh=0.1)
#
# mesh.Save("square_with_two_circles.vol")
