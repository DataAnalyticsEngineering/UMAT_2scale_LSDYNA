"""
Generate two phase periodic RVEs with spherical inclusions
for visualization check gen_xdmf.py
"""
import numpy as np
import h5py
import itertools
from scipy.spatial.distance import cdist
import pyvista as pv
import matplotlib.pyplot as plt


def volume_sphere(radius):
    return 4 / 3 * np.pi * radius**3


def radius_sphere(volume):
    return np.cbrt(3 / 4 * volume / np.pi)


def gen_rve(center_list, radius_list, rve_length, micro_to_voxels):
    """
    Generate and save a voxelized image of an RVE with spherical inclusions

    :param center_list: list of centers
    :param radius_list: list of radiuses
    :param n_volxels_x: number of voxels in x direction
    :param n_volxels_y: number of voxels in y direction
    :param n_volxels_z: number of voxels in z direction
    :return: image as 3D array
    """
    dx = int(round(rve_length * micro_to_voxels))

    image = np.zeros((dx, dx, dx), dtype=np.uint8)
    for c, r in zip(center_list, radius_list):
        pos_x = int(round(c[0] * micro_to_voxels))
        pos_y = int(round(c[1] * micro_to_voxels))
        pos_z = int(round(c[2] * micro_to_voxels))
        xyz = sphere(dx, dx, dx, pos_x, pos_y, pos_z,
                     int(round(r * micro_to_voxels)))
        image[xyz[:, 0], xyz[:, 1], xyz[:, 2]] = 1
    return image


def sphere(dx, dy, dz, pos_x, pos_y, pos_z, r):
    """
    Given dimensions of 3D array as dx,dy,dz
    return the indices of all voxels in a sphere centered at pos_x pos_y pos_z and has a diameter r
    :param dx: number of voxels in the first dimension
    :param dy: number of voxels in the second dimension
    :param dz: number of voxels in the third dimension
    :param pos_x: x coordinates of the center
    :param pos_y: x coordinates of the center
    :param pos_z: x coordinates of the center
    :param r: radius of the sphere
    :return: x,y,z indices of all voxels in the sphere
    """

    discretisation = np.linspace(-1, 1, 2 * r)
    z, y, x = np.meshgrid(discretisation, discretisation, discretisation)
    coords = np.nonzero(x**2 + y**2 + z**2 <= 1 + 1e-13)
    xx = coords[0] + (pos_x - r)
    yy = coords[1] + (pos_y - r)
    zz = coords[2] + (pos_z - r)
    xx[xx < 0] += dx
    yy[yy < 0] += dy
    zz[zz < 0] += dz
    xx[xx > dx - 1] -= dx
    yy[yy > dy - 1] -= dy
    zz[zz > dz - 1] -= dz
    return np.vstack((xx, yy, zz)).T

# %%
# fix random number seed in order to obtain same results with multiple runs of the code
np.random.seed(0)
rve_length = dy = dz = 150.0  # physical dimension
r_min, r_max = 40.0 / 2, 130.0 / 2
n_volxels = int(256)  # number of voxels in each dimension
micro_to_voxels = n_volxels / rve_length
half_length = rve_length / 2
center = np.asarray([rve_length / 2, rve_length / 2, rve_length / 2])
corner = np.asarray([rve_length, rve_length, rve_length])

# generate random number in [r_min, r_max] with a scaling factor <= 1.0 to favor radius close to r_min
get_rnd = lambda scale: r_min + (r_max - r_min) * np.random.rand() * scale
# return true if the calculated radius is not in [r_min, r_max] to break from for loops for example
check_radius = lambda r: True if r < r_min or r > r_max else False

# %% Generate periodic random 3D RVEs
hf = h5py.File('random_3d_rve.h5', 'w')
set_id = 0

for volume_fraction in np.linspace(0.25, 0.45, 100):

    print('volume fraction:', volume_fraction)
    # the volume that has to be covered with spheres
    missing_volume_ref = volume_fraction * rve_length**3

    rve_id = 0
    while rve_id < 100:
        missing_volume = volume_fraction * rve_length**3
        err = 1
        n_particles = 0
        trial = 0
        c_list = []
        c_list_ghost = []
        r_list = []
        r_list_ghost = []
        while err > 0.01 and trial < 3000:
            trial += 1
            r = get_rnd(1.0)
            c = [rve_length, rve_length, rve_length] * np.random.rand(3)

            # modify r if it'll result in high volume fraction
            if volume_sphere(r) / missing_volume > 1:
                r = radius_sphere(missing_volume)
                if check_radius(r):
                    break

            # periodic boundary conditions to be used for analytical collision check
            c_temp = np.zeros((27, 3))
            for idx, xyz in enumerate(
                    itertools.product([-rve_length, 0, rve_length],
                                      [-rve_length, 0, rve_length],
                                      [-rve_length, 0, rve_length])):
                c_temp[idx] = c + xyz

            # overlapping/collision check
            if n_particles > 0:
                if np.any(
                        cdist(np.asarray(c_list_ghost), c_temp) -
                    (np.asarray(r_list_ghost) + r)[:, None] <= 0):
                    continue
            c_list.append(c)
            c_list_ghost.extend(c_temp)
            r_list.append(r)
            r_list_ghost.extend(np.repeat(r, 27))

            missing_volume -= volume_sphere(r)
            err = missing_volume / missing_volume_ref
            n_particles += 1

        v = 0
        for r in r_list:
            v += volume_sphere(r)
        current_volume_fraction = v / (rve_length**3)

        # accept RVE that has an error less than 1% in the volume fraction
        if (np.abs(current_volume_fraction - volume_fraction) /
                volume_fraction) < 0.01:
            D = cdist(np.asarray(c_list), np.asarray(c_list))
            if n_particles > 1:
                np.fill_diagonal(D, np.nan)
            D_side = D - np.asarray(r_list)[:,
                                            None] - np.asarray(r_list)[None, :]
            surface_distance = np.nanmin(D)
            surface_distance_max = np.nanmax(D)
            print(
                f'RVE {set_id:03d} with {n_particles} random particles of radiuses '
                + ('{:.2f}, ' * len(r_list)).format(*r_list) +
                f' and min surface-surface distance {surface_distance:.2f}' +
                f' and max surface-surface distance {surface_distance_max:.2f}'
            )
            # generate and save a voxelized image of the RVE
            img = gen_rve(c_list, r_list, rve_length, micro_to_voxels)
            # np.sum(img) / img.size
            # pv.wrap(img).plot(volume=True)
            hf.create_dataset(f'/ms_random/dset{set_id}',
                              data=img,
                              compression=9)
            rve_id += 1
            set_id += 1

hf.close()
