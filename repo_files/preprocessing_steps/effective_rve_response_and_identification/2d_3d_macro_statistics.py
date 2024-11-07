# TODO change units * 200 / 185

import numpy as np
import cv2 as cv
import itertools
from numpy.fft import fft2, ifft2
import sys
sys.path.append('~/src/numerical_tools_and_friends/python/python_templates')
import matplotlib.pyplot as plt
from scipy import signal
from scipy.spatial.distance import cdist

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


def ecdf(data):
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n + 1) / n
    return (x, y)


def volume_sphere(radius):
    return 4 / 3 * np.pi * radius**3


def radius_volume_sphere(volume):
    return np.cbrt(3 / 4 * volume / np.pi)


def area_disc(radius):
    return np.pi * radius**2


def radius_area_disc(area):
    return np.sqrt(area / np.pi)


def two_point_correlation(binary_img):
    f_chi1 = fft2(binary_img)
    f_chi0 = fft2(1 - binary_img)
    c00 = (ifft2(f_chi0.conj() * f_chi0).real / binary_img.size)
    c01 = (ifft2(f_chi0.conj() * f_chi1).real / binary_img.size)
    c11 = (ifft2(f_chi1.conj() * f_chi1).real / binary_img.size)
    return c00, c01, c11


digital_image_cleaned = np.load('~/src/pyrve/segmentation/segmentation_2d/digital_image_cleaned.npy')
cutimage = digital_image_cleaned[:800, :]
particles = np.load('~/src/pyrve/segmentation/segmentation_2d/particles.npy')

#%% RVE size based on local volume fraction
# plt.imshow(cutimage)
# plt.savefig('micrograph.pdf', dpi=400)
# plt.show()
#
# nlist = [3, 25, 50, 75, 100, 125, 150, 175]
# outlist = []
# for nint in nlist:
#     volfilter = np.ones((nint, nint)) / nint**2
#     filteredimg = signal.convolve2d(volfilter, cutimage, boundary='wrap', mode='valid')
#     outlist.append(filteredimg.mean())
#
# plt.plot(nlist, outlist)
# plt.xlabel('rve length [px]')
# plt.ylabel('local volume fraction')
# plt.savefig('rve_length_vol_frac.pdf', dpi=400)
# plt.show()

#%% RVE size based on temperature
# # TODO the image is slightly modified
# ypx = digital_image_cleaned.shape[0]
# xpx = digital_image_cleaned.shape[1]
# from lasso.dyna import D3plot
# d3plot = D3plot("~/.dontsync/arch_dyna_simulations/6_padx/d3plot")
# x = d3plot.arrays['node_coordinates'][:, 0]
# y = d3plot.arrays['node_coordinates'][:, 1]
# t = d3plot.arrays['node_temperature'][1, :]
# plt.scatter(x, y, c=t)
# plt.colorbar()
# plt.show()
#
# nelementsx = xpx
# nelementsy = ypx
# from scipy.interpolate import griddata
# xr = np.arange(x.min(), x.max(), dx := abs(x.max() - x.min()) / nelementsx)
# yr = np.arange(y.min(), y.max(), dy := abs(y.max() - y.min()) / nelementsy)
# xx, yy = np.meshgrid(xr, yr, indexing='ij')
# zz = griddata((x, y), t, (xx, yy), method='linear')
# plt.imshow(zz.squeeze())
# plt.show()
#
# n = 50
#
# plt.contourf(xx, yy, zz, n)
# # gradx, grady = np.gradient(zz, dx, dy)
# # plt.contour(xx, yy, zz, levels=n, colors='k', linewidths=1, linestyles='solid')
# # plt.quiver(xx, yy, gradx, grady)
# # plt.colorbar()
# plt.show()
#
# nlist = [3, 25, 50, 75, 100, 125, 150,175,200]
# # nlist = [3, 5]
# outlistmean = []
# outlistmedian = []
# for n in nlist:
#     volfilter = np.ones((nint, nint)) / nint**2
#     filteredimg = signal.convolve2d(volfilter, zz, boundary='wrap', mode='valid')
#     zcut = zz[:filteredimg.shape[0], :filteredimg.shape[1]]
#     # filteredimg.reshape(nint, nint, -1)
#     outlistmean.append(np.mean((filteredimg - zcut) / zcut) * 100)
#     outlistmedian.append(np.mean((filteredimg - zcut) / zcut) * 100)
#
# plt.plot(nlist, outlistmean)
# plt.xlabel('rve length in \mu m')
# plt.ylabel('relative error [%]')
# plt.savefig('rve_length_temperature_mean.pdf')
# plt.show()
#
# plt.plot(nlist, outlistmedian)
# plt.xlabel('rve length in \mu m')
# plt.ylabel('relative error [%]')
# plt.savefig('rve_length_temperature_median.pdf')
# plt.show()

#%% particle distribution
R = 1
y = []
for z in np.linspace(0, R, 50):
    y.append(np.sqrt(R**2 - z**2))
plt.plot(*ecdf(y))
plt.xlabel('normalised radius r/r0')
plt.title('ecdf')
plt.savefig('ecdf_normalised_radius.pdf')
plt.show()

pp = np.vstack(particles)
diameter = 2 * pp[:, -1]
print(np.mean(diameter), np.median(diameter), np.max(diameter), np.min(diameter), np.std(diameter))
# plt.hist(diameter, bins=15)
plt.plot(*ecdf(diameter))
plt.xlabel('diameter [px]')
plt.title('ecdf')
plt.savefig('rve_particle_distribution.pdf')
plt.show()

#%% nearest neighbour # TODO now is based on the center not the boundary
# r0 = 50
# get_z0 = lambda r: np.sqrt(r0**2 - r**2)
# z0list = [get_z0(p[2]) if p[2] < 50 else 0 for p in particles]
#
#
# def r_newlayer(dz, z0):
#     if (r0 > (z0 + dz)) > 0:
#         return np.sqrt((r0**2 - (z0 + dz)**2))
#     else:
#         return np.sqrt((r0**2 - (2 * r0 - np.abs(z0 + dz))**2))
#
#
# newparticles = np.hstack((particles[:, :2], np.zeros((particles.shape[0], 1))))
# newparticles2 = np.hstack((particles[:, :2], np.zeros((particles.shape[0], 1))))
#
# for dz in [*np.linspace(0, 50, 200), *np.linspace(0, -25, 200)]:
#     r_list = [r_newlayer(dz, z0) for z0 in z0list]
#     for idx, r in enumerate(r_list):
#         if r / r0 > 0.91 and newparticles[idx, -1] == 0:
#             newparticles[idx, -1] = dz
# for dz in [*np.linspace(0, -50, 200), *np.linspace(0, 25, 200)]:
#     r_list = [r_newlayer(dz, z0) for z0 in z0list]
#     for idx, r in enumerate(r_list):
#         if r / r0 > 0.91 and newparticles2[idx, -1] == 0:
#             newparticles2[idx, -1] = dz
#
# newp = np.vstack((newparticles, newparticles2))
# D = cdist(newp, newp)
# np.fill_diagonal(D, np.nan)
# D[D < 100] = np.nan
# d = np.nanmin(D, axis=0)
# plt.hist(d, bins=15)
# plt.xlabel('nearest neighbour [px]')
# plt.ylabel('number of particles')
# plt.savefig('rve_nearest_neighbour_distribution.pdf', dpi=400)
# plt.show()
#
# ecdff = ecdf(np.asarray(d))
# plt.plot(ecdff[0], ecdff[1])
# plt.xlabel('center to center distance')
# plt.savefig('rve_nearest_neighbour_ecdf.pdf', dpi=400)
# plt.title('ecdf')
# plt.show()

#%% 3D
cout = iter(range(50))

volume_fraction = 0.4
ll = 140
rows = 2
cols = 4
rve_side_length = ll
rve_area = rve_side_length**3

r0 = 50
rve_side_length = np.cbrt(volume_sphere(r0) / volume_fraction)
xy_center = rve_side_length // 2
positions = [(xy_center, xy_center, xy_center)]
rads = [r0]
generate_3d_rve(rve_side_length, positions, rads, next(cout))

rve_side_length = np.cbrt(2 * volume_sphere(r0) / volume_fraction)
xy_center = rve_side_length // 2
positions = [(xy_center, xy_center, xy_center)]
rads = [r0] * 9
for i, j, k in itertools.product([0, rve_side_length + 1], [0, rve_side_length + 1], [0, rve_side_length + 1]):
    positions.append((i, j, k))
generate_3d_rve(rve_side_length, positions, rads, next(cout))

# lengths = [75,100,125]
# particles mean 64 [50-80] # TODO move the relevant code here
# nearest neighbour 20 # TODO move the relevant code here np.min(D,axis=1) gives ...
# vol frac 0.4

# noch etwas, in 3D wir können kein RVE kleine als 100\mu m nutzen weil die parikles sind mindesten ~100
# Das ist klar. Ich hatte eher an so etwas wie 250-400 gedacht

# TODO do the particles in 2D & 3D follow the ecdf from the input image

#%% 3D slice in Z and average
# import numpy as np
# from pyhdf.SD import SD, SDC
# import cv2 as cv
#
# file = SD('~/src/0data/simkom_input_images/WS_2a.hdf', SDC.READ)
# print(file.info())
# print(file.datasets())
# # 23: uint16 DFNT_UINT16 (23) 16-bit unsigned integer type
#
# kt = file.select('Not specified')
# print(kt.dimensions())
#
# seg_slices = kt.get()[250:750, :, :]
# rng = seg_slices < 30987
# seg_slices[rng] = 0
# seg_slices[~rng] = 1
#
# particles = [''] * 500
# for idx, seg_slice in enumerate(seg_slices):
#     img = np.array(seg_slice * 255, dtype=np.uint8)
#     cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
#
#     circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1.7, 40, param1=1e-8, param2=30, minRadius=3, maxRadius=60)
#     circles = np.uint16(np.around(circles))
#
#     from skimage.draw import circle
#     particles[idx] = []
#     for i in circles[0, :]:
#         rr, cc = circle(i[1], i[0], i[2])
#         rr[rr >= img.shape[0]] = img.shape[0] - 1
#         cc[cc >= img.shape[1]] = img.shape[1] - 1
#         if np.count_nonzero(img[rr, cc]) / np.size(img[rr, cc]) > 0.6:
#             img[rr, cc] = 0
#             particles[idx].append(i)
#
# np.save('3d_particles.npy', particles)

#%%
import matplotlib.pyplot as plt
particles = np.load('~/src/pyrve/output_py/3d_particles.npy', allow_pickle=True)
yall = np.zeros(60)
rall = []
for i in range(500):
    rlist = np.asarray(particles[i])[:, -1]
    rall.extend(rlist)
    y, x = np.histogram(rlist, bins=range(1, 62))
    yall += y
plt.bar(x[:-1], yall)
plt.show()

ecdff = ecdf(np.asarray(rall)*2)
plt.plot(*ecdf(np.asarray(rall)*2))
plt.plot(*ecdf(diameter),ls='--')
# plt.plot(ecdff[0], ecdff[1])
plt.legend(['Extracted from 3D data','Extracted from 2D data'])
plt.xlabel('diameter [px]')
plt.title('ecdf')
plt.xlim([4,124])
plt.savefig('rve_particle_distribution_3d.pdf', dpi=400)
plt.savefig('rve_particle_distribution_3d.png', dpi=400)
plt.show()

