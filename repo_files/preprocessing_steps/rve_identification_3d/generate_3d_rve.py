import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from pyhdf.SD import SD, SDC
import pyvista as pv
from scipy.sparse import coo_matrix
import cv2

from scipy import signal
from numpy.fft import fft2, ifft2, fft, ifft
from scipy.spatial.distance import cdist

#%% read and visualise data
# 500 x 500 x 800 micrometers
micro_to_voxel_scaling_factor = 400 / 500
micro_to_voxel_scaling_factor_2d = 185 / 200
file = SD('~/src/0data/simkom_input_images/WS_2a.hdf', SDC.READ)
print(file.info())
print(file.datasets())
# 23: uint16 DFNT_UINT16 (23) 16-bit unsigned integer type

kt = file.select('Not specified')
print(kt.dimensions())
d3img = np.copy(kt[:, :, :])

rng = d3img < 30987
d3img[rng] = 0
d3img[~rng] = 1
d3img = d3img.astype(np.uint8)

xmax, ymax, zmax = d3img.shape
xmin, ymin, zmin = 0, 0, 0

xx, yy, zz = np.nonzero(d3img)
xmax = np.minimum(xx.max(), xmax)
xmin = np.maximum(xx.min(), xmin)

ymax = np.minimum(yy.max(), ymax)
ymin = np.maximum(yy.min(), ymin)

zmax = np.minimum(zz.max(), zmax)
zmin = np.maximum(zz.min(), zmin)

# d3img[1:xmin, 1:ymin, 1:zmin].sum()
# d3img[xmax:, ymax:, zmax:].sum()

sub_imag = d3img[xmin:xmax, ymin:ymax, zmin:zmax]

plt.imshow(d3img[:, 600, :])
plt.show()

#%% fix orientation / rotate images
# https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html

# TODO: angle is already returned by cv2.minAreaRect()
#  OpenCV provides a function cv2.minAreaRect() for finding the minimum area rotated rectangle. This takes as input a 2D point set and returns a Box2D structure which contains the following details – (center(x, y), (width, height), angle of rotation). The syntax is given below.

def rotate(seg_slice, iterations=30):
    newimg = seg_slice * 255
    newimg_color = cv2.cvtColor(newimg, cv2.COLOR_GRAY2RGB)

    kernel = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(newimg, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # external contour when extracting many contours: np.argmax(h[:, :, 2] != -1)
    cnt = contours[0]

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(newimg_color, [box], -1, (255, 0, 0), 3)
    plt.imshow(newimg_color)
    plt.savefig('3d_before_rotation.pdf', dpi=400)
    plt.show()

    dd = box[1] - box[2]
    angle = np.rad2deg(np.arctan(dd[1] / dd[0])) if dd[0] != 0 else 0
    print(f'ang= {angle}')
    print(f'box= {box}')
    center = (box.mean(axis=0)[0], box.mean(axis=0)[1])
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    newimg_color = cv2.warpAffine(newimg_color, rot_mat, seg_slice.shape[1::-1], flags=cv2.INTER_LINEAR)

    plt.imshow(newimg_color)
    plt.savefig('3d_after_rotation.pdf', dpi=400)
    plt.show()
    return rot_mat

input_img = d3img[:, 350, :]
rot_mat = rotate(input_img, iterations=30)
for idx in range(d3img.shape[1]):
    if np.max(d3img[:, idx, :]) > 0:
        d3img[:, idx, :] = cv2.warpAffine(d3img[:, idx, :], rot_mat, input_img.shape[1::-1], flags=cv2.INTER_LINEAR)

input_img = d3img[:, :, 350]
rot_mat = rotate(d3img[:, :, 350], iterations=20)
for idx in range(d3img.shape[2]):
    if np.max(d3img[:, :, idx]) > 0:
        d3img[:, :, idx] = cv2.warpAffine(d3img[:, :, idx], rot_mat, input_img.shape[1::-1], flags=cv2.INTER_LINEAR)

#%% visualise and save cleaned data
plt.imshow(d3img[:, 350, :])
plt.show()
plt.imshow(d3img[:, :, 350])
plt.show()

new_d3img = d3img[300:800, 300:600, 300:600]
for i in range(10):
    plt.imshow(new_d3img[:, :, i])
    plt.show()

np.savez_compressed('~/src/0data/simkom_input_images/WS_2a.npz', d3img=new_d3img)

#%% volume average
data = np.load('~/src/0data/simkom_input_images/WS_2a.npz')
d3img = data['d3img']
print(f'global vol_av: {d3img.sum()/d3img.size = :.2f}')
# import pyvista as pv
# data = pv.wrap(d3img)
# data.plot(volume=True)
# data.save("d3img_cleaned.vtk")

nlist = [3, 25, 50, 75, 100, 125, 150, 175, 200, 250, 300]

outlistmean = []
outlistmedian = []
for n in nlist:
    volfilter = np.ones((n, n, n)) / n**3
    filteredimg = signal.fftconvolve(volfilter, d3img, mode='valid')
    print(np.mean(filteredimg))
    outlistmean.append(np.mean(filteredimg) * 100)
    outlistmedian.append(np.median(filteredimg) * 100)

plt.rcParams.update({
    # 'font.size': 14,
    # 'legend.fontsize': 'x-large',
    # 'axes.labelsize': 'x-large',
    # 'axes.titlesize': 'x-large',
    # 'xtick.labelsize': 'x-large',
    # 'ytick.labelsize': 'x-large',
    'axes.linewidth': 2,
    # 'axes.titlepad': 10,
    'lines.color': 'k',
    'lines.linewidth': 2,
    'lines.markeredgecolor': 'black',
    'scatter.edgecolors': 'black',
    # 'lines.markersize': 8,
    # 'xtick.major.size': 10,
    # 'ytick.major.size': 10,
    # 'xtick.major.pad': 3,
    # 'ytick.major.pad': 3,
    # 'xtick.major.width': 2,
    # 'ytick.major.width': 2,
    'axes.grid': True,
    'grid.color': '#AAAAAA',
    'grid.linestyle': ':',
    'grid.linewidth': 2
})
nlist = [x / micro_to_voxel_scaling_factor for x in nlist]
plt.plot(nlist, outlistmean, label='mean')
plt.plot(nlist, outlistmedian, label='median')
plt.xlabel('rve length [$\mu$m]')
plt.ylabel('local volume fraction [%]')
plt.legend()
plt.savefig('rve_length_3d_vol_frac.pdf', dpi=400)
plt.show()

#%%
def ecdf(data):
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n + 1) / n
    return (x, y)

f = np.load('~/src/0data/simkom_input_images/digital_3d.npz')
pos_and_r = f['pos_and_r']
f.close()

pos_and_r = pos_and_r / micro_to_voxel_scaling_factor
# diameter
diameter = 2 * pos_and_r[:, -1]
print(diameter.min())
print(diameter.max())

plt.plot(*ecdf(diameter))
plt.xlabel('diameter [$\mu$m]')
plt.title('ecdf')
plt.ylabel('$P$ [-]')
plt.savefig('rve_particle_distribution_3d.pdf')
plt.show()

newp = pos_and_r[:, :3]
D = cdist(newp, newp)
np.fill_diagonal(D, np.nan)
# D[D < 40] = np.nan
D_side = D - pos_and_r[:, 3][:, None] - pos_and_r[:, 3][None, :]
d = np.nanmin(D, axis=0)
plt.hist(d, bins=15)
plt.xlabel('nearest neighbour, center to center [$\mu$m]')
plt.ylabel('number of particles')
plt.savefig('rve_nearest_neighbour_distribution_3d.pdf', dpi=400)
plt.show()

ecdff = ecdf(np.asarray(d))
plt.plot(ecdff[0], ecdff[1])
plt.xlabel('center to center distance [$\mu$m]')
plt.ylabel('$P$ [-]')
plt.savefig('rve_nearest_neighbour_ecdf_3d.pdf', dpi=400)
plt.title('ecdf')
plt.show()

d = np.nanmin(D_side, axis=0)
plt.hist(d, bins=15)
plt.xlabel('nearest neighbour, surface to surface [$\mu$m]')
plt.ylabel('number of particles')
plt.savefig('rve_nearest_neighbour_distribution_surface_3d.pdf', dpi=400)
plt.show()

ecdff = ecdf(np.asarray(d))
plt.plot(ecdff[0], ecdff[1])
plt.xlabel('surface to surface distance [$\mu$m]')
plt.ylabel('$P$ [-]')
plt.savefig('rve_nearest_neighbour_ecdf_surface_3d.pdf', dpi=400)
plt.title('ecdf')
plt.show()

#%%
# 2d image -> pickup random radius and calculate center to center ...
def ecdf(data):
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n + 1) / n
    return (x, y)

f = np.load('~/src/0data/simkom_input_images/digital_3d.npz')
pos_and_r = f['pos_and_r']
f.close()

pos_and_r = pos_and_r / micro_to_voxel_scaling_factor
# diameter
diameter = 2 * pos_and_r[:, -1]
print(diameter.min())
print(diameter.max())

# plt.plot(*ecdf(diameter))
# plt.xlabel('diameter [$\mu$m]')
# plt.title('ecdf')
# plt.ylabel('$P$ [-]')
# plt.show()

newp = pos_and_r[:, :3]
D = cdist(newp, newp)
np.fill_diagonal(D, np.nan)
# D[D < 40] = np.nan
# D = D - pos_and_r[:, 3][:, None] - pos_and_r[:, 3][None, :]
D[D < 0] = np.nan
d = np.nanmin(D, axis=0)
ecdff = ecdf(np.asarray(d))
plt.plot(ecdff[0], ecdff[1], label='3D')

plt.xlabel('center to center distance [$\mu$m]')
# plt.xlabel('surface to surface distance [$\mu$m]')
plt.ylabel('$P$ [-]')
plt.title('ecdf')

from scipy.interpolate import interp1d
from statsmodels.distributions.empirical_distribution import ECDF
ecdff = ECDF(diameter)
inv_cdf = interp1d(ecdff.y, ecdff.x, bounds_error=False, assume_sorted=True)
for i in range(1):
    p0 = np.random.uniform(0, 1, 342)
    r0 = inv_cdf(p0)
    # ecdff = ECDF(r0)
    # plt.plot(ecdff.x, ecdff.y)
    # plt.show()

    particles = np.load('~/src/pyrve/segmentation/segmentation_2d/particles.npy')
    particles = particles / micro_to_voxel_scaling_factor_2d
    z_squared = r0**2 - particles[:, 2]**2
    z_squared[z_squared < 0] = 0
    z0list = np.sqrt(z_squared)

    newparticles = np.hstack((particles[:, :2], z0list[:, None]))
    # newparticles2 = np.hstack((particles[:, :2], z0list[:, None]))
    # newp = np.vstack((newparticles, newparticles2))
    newp = newparticles
    D = cdist(newp, newp)
    # D = D - r0[:, None] - r0[None, :]
    np.fill_diagonal(D, np.nan)
    D[D < 0] = np.nan
    d = np.nanmin(D, axis=0)
    ecdff = ecdf(np.asarray(d))
    if i == 0:
        plt.plot(ecdff[0], ecdff[1], label='2D', ls='--')
    else:
        plt.plot(ecdff[0], ecdff[1], label=None, ls='--')

plt.legend()
plt.savefig('rve_nearest_neighbour_ecdf_center_2d_3d.pdf', dpi=400)
# plt.savefig('rve_nearest_neighbour_ecdf_surface_2d_3d.pdf', dpi=400)
plt.show()
