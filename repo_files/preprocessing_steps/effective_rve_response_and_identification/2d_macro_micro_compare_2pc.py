# images = np.zeros((4, rve_side_length, rve_side_length))
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
    # f_chi0 = fft2(1 - binary_img)
    # c00 = (ifft2(f_chi0.conj() * f_chi0).real / binary_img.size)
    # c01 = (ifft2(f_chi0.conj() * f_chi1).real / binary_img.size)
    c11 = (ifft2(f_chi1.conj() * f_chi1).real / binary_img.size)
    return c11


digital_image_cleaned = np.load('~/src/pyrve/segmentation/segmentation_2d/digital_image_cleaned.npy')
cutimage = digital_image_cleaned[:800, :]
particles = np.load('~/src/pyrve/segmentation/segmentation_2d/particles.npy')
# particles = np.load('~/src/pyrve/output_py/particles.npy')

#%% RVE generation 2D
cout = iter(range(50))

volume_fraction = 0.4
# for ll in [150]:  # [75, 100, 125]:
rows = 2
cols = 1

min_radius = np.min(particles[:, -1])
max_radius = np.max(particles[:, -1])

r0list = [10, 20, 50, 75, 100]

fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 1.3)])
itx = iter(ax.flatten())

c11ref = two_point_correlation(cutimage)
next(itx).imshow(cutimage)
pos = next(itx).imshow(c11ref, vmin=0, vmax=0.4, cmap='jet')
# fig.colorbar(pos)
plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
for aa in ax.flatten():
    aa.axis('off')
# plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/original_correlation.pdf', dpi=600)
plt.show()

#%% one particle
rows = 3
ll = 151
rve_side_length = ll
rve_area = rve_side_length**2
xy_center = rve_side_length // 2 + 1

# fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
# itx = iter(ax.flatten())
# rve_image = np.zeros((rve_side_length, rve_side_length))
# r0 = radius_area_disc(volume_fraction * rve_area - 0)
# # radius is not checked here
# positions = [(xy_center, xy_center)]
# rads = [r0]
# rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
# # generate_2d_rve(ll, positions, rads, next(cout))
# rve_image = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
# rve_image = rve_image[:cutimage.shape[0], :cutimage.shape[1]]
# c11 = two_point_correlation(rve_image)
# plt.title(
#     f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
# )
# next(itx).imshow(rve_image)
# next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
# next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
# plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
# for aa in ax.flatten():
#     aa.axis('off')
# plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_1particle_{0}.pdf', dpi=600)
# plt.show()
# #TODO check volume_fraction * rve_area - area_disc(r0) - area_disc(r1)

# %% two particles
for ii in range(15):
    fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
    itx = iter(ax.flatten())
    rve_image = np.zeros((rve_side_length, rve_side_length))
    r0 = np.random.uniform(min_radius, max_radius)
    while (volume_fraction * rve_area - area_disc(r0)) < area_disc(min_radius):
        r0 *= 0.9
    r1 = radius_area_disc((volume_fraction * rve_area - area_disc(r0)))
    # if min_radius <= r0 <= max_radius and min_radius <= r1 <= max_radius:
    positions = [(xy_center, xy_center)]
    rads = [r0, r1, r1, r1, r1]
    rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
    for i, j in itertools.product([0, rve_side_length + 1], [0, rve_side_length + 1]):
        positions.append((i, j))
        rve_image = cv.circle(rve_image, (i, j), int(r1), 1, -1)
    # else:
    #     raise RuntimeError
    # generate_2d_rve(ll, positions, rads, next(cout))
    rve_image = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
    rve_image = rve_image[:cutimage.shape[0], :cutimage.shape[1]]
    c11 = two_point_correlation(rve_image)
    plt.title(
        f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
    )
    next(itx).imshow(rve_image)
    next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
    next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    for aa in ax.flatten():
        aa.axis('off')
    plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_2particle_{ii}.pdf')
    plt.show()

#%% five particles
for ii in range(15):
    rve_image = np.zeros((rve_side_length, rve_side_length))
    r0 = np.random.uniform(min_radius, max_radius)
    while (volume_fraction * rve_area - area_disc(r0)) < area_disc(min_radius) * 4:
        r0 *= 0.9
    r1 = radius_area_disc((volume_fraction * rve_area - area_disc(r0)) / 4)
    # if min_radius <= r0 <= max_radius and min_radius <= r1 <= max_radius:
    positions = [(xy_center, xy_center)]
    rads = [r0, r1, r1, r1, r1]
    rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
    dx = int((r0 + r1 + np.random.randint(5, 40)) * np.cos(np.pi / 4))
    dy = dx
    for i, j in itertools.product([-dx, dx], [-dy, dy]):
        positions.append((xy_center + i, xy_center + j))
        rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r1), 1, -1)
    # else:
    #     raise RuntimeError
    # generate_2d_rve(ll, positions, rads, next(cout))
    rve_image = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
    rve_image = rve_image[:cutimage.shape[0], :cutimage.shape[1]]
    c11 = two_point_correlation(rve_image)
    fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
    itx = iter(ax.flatten())
    plt.title(
        f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
    )
    next(itx).imshow(rve_image)
    next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
    next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    for aa in ax.flatten():
        aa.axis('off')
    plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_5particle_{ii}.pdf', dpi=600)
    plt.show()

#%% six particles
for ii in range(15):
    images = np.zeros((4, rve_side_length, rve_side_length))
    rve_image = np.zeros((rve_side_length, rve_side_length))
    r0 = np.random.uniform(min_radius, max_radius)
    while (volume_fraction * rve_area - area_disc(r0)) < area_disc(min_radius) * 5:
        r0 *= 0.9
    r1 = radius_area_disc((volume_fraction * rve_area - area_disc(r0)) / 4.3)
    r2 = radius_area_disc(volume_fraction * rve_area - area_disc(r0) - 4 * area_disc(r1))
    # if min_radius <= r0 <= max_radius and min_radius <= r1 <= max_radius:
    positions = [(xy_center, xy_center)]
    rads = [r0, r1, r1, r1, r1]
    rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
    dx = int((r0 + r1 + np.random.randint(5, 40)) * np.cos(np.pi / 4))
    dy = dx
    for i, j in itertools.product([-dx, dx], [-dy, dy]):
        positions.append((xy_center + i, xy_center + j))
        rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r1), 1, -1)
    dx = int(ll / 2)
    dy = dx
    for i, j in ([-dx, 0], [dx, 0]):
        positions.append((xy_center + i, xy_center + j))
        rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r2), 1, -1)
    # else:
    #     raise RuntimeError
    # # generate_2d_rve(ll, positions, rads, next(cout))
    rve_image = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
    rve_image = rve_image[:cutimage.shape[0], :cutimage.shape[1]]
    c11 = two_point_correlation(rve_image)
    fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
    itx = iter(ax.flatten())
    plt.title(
        f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
    )
    next(itx).imshow(rve_image)
    next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
    next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    for aa in ax.flatten():
        aa.axis('off')
    plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_6particle_{ii}.pdf', dpi=600)
    plt.show()

#%% seven particles
for ii in range(15):
    images = np.zeros((4, rve_side_length, rve_side_length))
    rve_image = np.zeros((rve_side_length, rve_side_length))
    r0 = np.random.uniform(min_radius, max_radius)
    while (volume_fraction * rve_area - area_disc(r0)) < area_disc(min_radius) * 5:
        r0 *= 0.9
    r1 = radius_area_disc((volume_fraction * rve_area - area_disc(r0)) / 4.3)
    r2 = radius_area_disc(volume_fraction * rve_area - area_disc(r0) - 4 * area_disc(r1))
    # if min_radius <= r0 <= max_radius and min_radius <= r1 <= max_radius:
    positions = [(xy_center, xy_center)]
    rads = [r0, r1, r1, r1, r1]
    rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
    dx = int((r0 + r1 + np.random.randint(5, 40)) * np.cos(np.pi / 4))
    dy = dx
    for i, j in itertools.product([-dx, dx], [-dy, dy]):
        positions.append((xy_center + i, xy_center + j))
        rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r1), 1, -1)
    dx = int(ll / 2)
    dy = dx
    for i, j in ([-dx, 0], [dx, 0], [0, dy], [0, -dy]):
        positions.append((xy_center + i, xy_center + j))
        rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r2), 1, -1)
    # else:
    #     raise RuntimeError
    # # generate_2d_rve(ll, positions, rads, next(cout))
    rve_image = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
    rve_image = rve_image[:cutimage.shape[0], :cutimage.shape[1]]
    c11 = two_point_correlation(rve_image)
    fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
    itx = iter(ax.flatten())
    plt.title(
        f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
    )
    next(itx).imshow(rve_image)
    next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
    next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    for aa in ax.flatten():
        aa.axis('off')
    plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_7particle_{ii}.pdf', dpi=600)
    plt.show()

#%%

# import h5py
# hf = h5py.File('micrograph_full.h5', 'w')
# hf.create_dataset('images', data=image)
# hf.close()

# import h5py
# hf = h5py.File('microstructues.h5', 'w')
# hf.create_dataset('images', data=images)
# hf.close()

import h5py
hf = h5py.File('micrograph_tiles.h5', 'w')
cnt = 1
for x in range(cutimage.shape[0] // 151):
    for y in range(cutimage.shape[1] // 151):
        img = cutimage[x * 151:x * 151 + 151, y * 151:y * 151 + 151]
        cnt = cnt + 1
        hf.create_dataset(f'dset{cnt}', data=img)
hf.close()

#%% delete bwlow this line
r0, r1, r2, dx1 = [34.37191231445061, 20.00979486778368, 10.959816020136223, 45]
simg = []
np.random.seed(50000)
# for ii in range(50):
# for r0,r1,r2,dx in rr:
images = np.zeros((4, rve_side_length, rve_side_length))
rve_image = np.zeros((rve_side_length, rve_side_length))
# r0 = np.random.uniform(min_radius, max_radius)
# while (volume_fraction * rve_area - area_disc(r0)) < area_disc(min_radius) * 5:
#     r0 *= 0.9
# r1 = radius_area_disc((volume_fraction * rve_area - area_disc(r0)) / 4.3)
# r2 = radius_area_disc(volume_fraction * rve_area - area_disc(r0) - 4 * area_disc(r1))
# if min_radius <= r0 <= max_radius and min_radius <= r1 <= max_radius:
positions = [(xy_center, xy_center)]
rads = [r0, r1, r1, r1, r1, r2, r2]
rve_image = cv.circle(rve_image, positions[0], int(rads[0]), 1, -1)
# dx1 = int((r0 + r1 + np.random.randint(5, 40)) * np.cos(np.pi / 4))
dy1 = dx1
for i, j in itertools.product([-dx1, dx1], [-dy1, dy1]):
    positions.append((xy_center + i, xy_center + j))
    rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r1), 1, -1)
dx = int(ll / 2)
dy = dx
for i, j in ([-dx, 0], [dx, 0]):
    positions.append((xy_center + i, xy_center + j))
    rve_image = cv.circle(rve_image, (xy_center + i, xy_center + j), int(r2), 1, -1)
# else:
#     raise RuntimeError
# # generate_2d_rve(ll, positions, rads, next(cout))
rve_image_full = np.tile(rve_image, (x // rve_side_length + 1 for x in cutimage.shape))
rve_image_full = rve_image_full[:cutimage.shape[0], :cutimage.shape[1]]
c11 = two_point_correlation(rve_image_full)

# if np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100 < 15:
simg.append([r0, r1, r2, dx1])
fig, ax = plt.subplots(rows, cols, figsize=[10 * cols, 10 * (rows - 2.)])
itx = iter(ax.flatten())
plt.title(
    f'rel err_Fro {np.linalg.norm(c11 - c11ref) / np.linalg.norm(c11ref) * 100:.2f}%, mean {np.mean(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%, median {np.median(np.abs((c11 - c11ref) / c11ref)) * 100:.2f}%'
)
next(itx).imshow(rve_image_full)
next(itx).imshow(c11, vmin=0, vmax=0.4, cmap='jet')
next(itx).imshow(np.abs(c11 - c11ref), vmin=0, vmax=0.4, cmap='jet')
plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
for aa in ax.flatten():
    aa.axis('off')
# plt.savefig(f'~/src/pyrve/0_geo_and_mesh/rve_2pc/rve_length_{ll}_6particle_{ii}.pdf', dpi=600)
plt.show()

import h5py
hf = h5py.File('rve_identification/selected_rve.h5', 'w')
hf.create_dataset('images', data=rve_image)
hf.close()

generate_2d_rve(ll, ll, positions, rads, 0)
# generate_2d_rve(cutimage.shape[1],cutimage.shape[0], [(x[0],x[1]-(digital_image_cleaned.shape[0]-800)) for x in particles], [x[2] for x in particles], 1)
generate_2d_rve(cutimage.shape[1], -cutimage.shape[0], [(x[0], -1 * x[1] + 380) for x in particles], [x[2] for x in particles], 1)
# 380 because there's a layer that was removed before storing the particles location
