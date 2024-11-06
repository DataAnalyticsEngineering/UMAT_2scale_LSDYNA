import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from pyhdf.SD import SD, SDC
import pyvista as pv
from scipy.sparse import coo_matrix

def sphere(dx, dy, dz, pos_x, pos_y, pos_z, r):
    dx = dx - 1
    dy = dy - 1
    dz = dz - 1
    # given dx,dy,dz as dimensions of 3D array
    # return the indices of all pixels in a sphere centered at pos_x _y _z
    # and has a diameter r
    discretisation = np.linspace(-1, 1, 2 * r)
    z, y, x = np.meshgrid(discretisation, discretisation, discretisation)
    coords = np.nonzero(x**2 + y**2 + z**2 <= 1 + 1e-13)
    yy = coords[1] + (pos_y - r)
    xx = coords[0] + (pos_x - r)
    zz = coords[2] + (pos_z - r)
    xx[xx < 0] = dx + xx[xx < 0]
    yy[yy < 0] = dy + yy[yy < 0]
    zz[zz < 0] = dz + zz[zz < 0]
    xx[xx > dx] = xx[xx > dx] - dx
    yy[yy > dy] = yy[yy > dy] - dy
    zz[zz > dz] = zz[zz > dz] - dz
    return xx, yy, zz

def circle(dx, dy, pos_x, pos_y, r):
    dx = dx - 1
    dy = dy - 1
    # given dx,dy as dimensions of 2D array
    # return the indices of all pixels in a disk centered at pos_x _y
    # and has a diameter r

    # y = np.tile(np.linspace(-1, 1, 2 * r + 1)[:, None], [1, 2 * r + 1])
    # x = np.tile(np.linspace(-1, 1, 2 * r + 1), [2 * r + 1, 1])
    discretisation = np.linspace(-1, 1, 2 * r)
    y, x = np.meshgrid(discretisation, discretisation)
    coords = np.nonzero(x**2 + y**2 <= 1 + 1e-13)
    xx = coords[0] + (pos_x - r)
    yy = coords[1] + (pos_y - r)
    xx[xx < 0] = dx + xx[xx < 0]
    yy[yy < 0] = dy + yy[yy < 0]
    xx[xx > dx] = xx[xx > dx] - dx
    yy[yy > dy] = yy[yy > dy] - dy
    return xx, yy

#%% load 3d image and use watershed to label its pixels and save all peaks/centers

data = np.load('/home/alameddin/src/0data/simkom_input_images/WS_2a.npz')
d3img = data['d3img']

distance = ndi.distance_transform_edt(d3img)
# distance[distance < 0] = 0
coords = peak_local_max(distance, footprint=np.ones((30, 30, 30)), labels=d3img)
# coords = peak_local_max(distance, labels=d3img)
np.savez('/home/alameddin/src/0data/simkom_input_images/centers_3d.npz', centers=coords)
# distance[distance < 0] = 0
# mask = np.zeros(distance.shape, dtype=bool)
# mask[tuple(coords.T)] = True
# markers, _ = ndi.label(mask)
# labels = watershed(-distance, markers, mask=d3img)

# print(len(coords))
# labels.max()
# len(np.unique(labels))
# plt.imshow(labels[:, 600, :])
# plt.show()

#%% draw spheres at the extracted centers and check if they meet the inclusions
data = np.load('/home/alameddin/src/0data/simkom_input_images/WS_2a.npz')
d3img = data['d3img']
f = np.load('/home/alameddin/src/0data/simkom_input_images/centers_3d.npz')
centers = f['centers']
f.close()
out = []
vol = 0.6
for pos in centers:
    old_vol = 0
    old_r = 0
    old_idx = 0
    for r in range(17, 130):
        xx, yy, zz = sphere(*d3img.shape, pos[0], pos[1], pos[2], r)
        if (current_volume := np.sum(d3img[xx, yy, zz]) / xx.shape[0]) < old_vol:
            break
        if current_volume == 0 or current_volume < vol:
            break
        old_vol = np.copy(current_volume)
        old_r = r
        old_idx = (xx, yy, zz)
        print(old_vol, current_volume)
    if old_vol > vol:
        d3img[old_idx] = 0
        out.append([*pos, old_r])

np.savez('/home/alameddin/src/0data/simkom_input_images/digital_3d.npz', pos_and_r=np.asarray(out))

#%% 2D hough transform
img = d3img[:, 150, :]

import cv2 as cv
from scipy.sparse import coo_matrix
canny_img = cv.Canny(img.astype(np.uint8), 0, 1)
plt.imshow(canny_img)
plt.show()

centers = np.asarray(np.nonzero(canny_img))
y_centers = centers[0]
x_centers = centers[1]

steps = 70
r = list(range(10, 40))

phi = np.linspace(0, 2 * np.pi, steps)
y_circles = np.int16(np.round(np.outer(r, np.sin(phi))))
x_circles = np.int16(np.round(np.outer(r, np.cos(phi))))

y = (y_circles[:, :, None] + y_centers[None, None, :]).reshape(len(r), -1)
x = (x_circles[:, :, None] + x_centers[None, None, :]).reshape(len(r), -1)
ymin = np.abs(y.min()) if y.min() < 0 else 0
xmin = np.abs(x.min()) if x.min() < 0 else 0
y = y + ymin
x = x + xmin
acc = np.zeros((len(r), y.max() + 1, x.max() + 1))
for i in range(len(r)):
    acc[i] = coo_matrix((np.ones(y[i].shape), (y[i], x[i])), (y.max() + 1, x.max() + 1)).toarray().astype(np.int32)
# plt.imshow(acc[-1])
# plt.show()
acc[acc / steps < 0.3] = 0
# compare with r in each slice
while (acc.sum() > r[0]):
    ind = np.unravel_index(np.argmax(acc, axis=None), acc.shape)
    xx, yy = circle(img.shape[1], img.shape[0], ind[2] - xmin, ind[1] - ymin, r[ind[0]])
    canny_img[yy, xx] = 255
    acc[:, ind[1:]] = 0

plt.imshow(canny_img)
plt.show()

# y_flatten = y.flatten()
# x_flatten = x.flatten()
# rng = np.bitwise_or(np.bitwise_or(y_flatten < 0, y_flatten > 499), np.bitwise_or(x_flatten < 0, x_flatten > 299))
# y = np.delete(y, rng)
# x = np.delete(x, rng)
# hough_img = coo_matrix((np.ones(y.shape), (y,x)), canny_img.shape).toarray().astype(np.int32)
# plt.imshow(hough_img)
# plt.show()

#%% test sphere and circle functions
dx = dy = 20
pos_y = pos_x = 6
r = 5
xx, yy = circle(dx, dy, pos_x, pos_y, r)
hough_img = coo_matrix((np.ones_like(xx), (yy, xx)), (dy, dx)).toarray()

plt.imshow(hough_img)
plt.show()

dx = dy = dz = 15
xx, yy, zz = sphere(dx, dy, dz, 5, 5, 3, 5)
img = np.zeros((dz, dy, dx))
img[zz, yy, xx] += 1
plt.imshow(img[0])
plt.show()

#%% generate a 3d description of the CT scan
f = np.load('/home/alameddin/src/0data/simkom_input_images/digital_3d.npz')
pos_and_r = f['pos_and_r']
f.close()

dx, dy, dz = d3img.shape
img = np.empty((dx, dy, dz), dtype=np.uint8)
for s in pos_and_r:
    xx, yy, zz = sphere(dx, dy, dz, s[0], s[1], s[2], s[3])
    img[xx, yy, zz] = 1

data = pv.wrap(img)
# data.plot(volume=True)
data.save("/home/alameddin/src/0data/simkom_input_images/digital_3d.vtk")

#%% difference
data = np.load('/home/alameddin/src/0data/simkom_input_images/WS_2a.npz')
d3img = data['d3img']
err = np.abs(d3img - 1. * img).astype(np.uint8)
err = img - 1. * d3img
err[err < 0] = 0
data = pv.wrap(err.astype(np.uint8))
# data.plot(volume=True)
data.save("/home/alameddin/src/0data/simkom_input_images/digital_3d_error.vtk")
