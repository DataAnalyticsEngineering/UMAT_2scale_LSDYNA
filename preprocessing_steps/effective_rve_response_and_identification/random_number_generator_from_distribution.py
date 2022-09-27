import numpy as np
from scipy.spatial.distance import cdist
from scipy.interpolate import interp1d
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# pick random numbers from a distribution
# f = np.load('/home/alameddin/src/0data/simkom_input_images/digital_3d.npz')
# pos_and_r = f['pos_and_r']
# f.close()
# ecdff = ECDF(pos_and_r[:, -1]) + 5
# cdf_interpolated = interp1d(ecdff.x, ecdff.y, bounds_error=False, assume_sorted=True, kind='linear')
# xx = np.linspace(0, ecdff.x[-1], 200)
# plt.plot(xx, cdf_interpolated(xx))
# yy = savgol_filter(cdf_interpolated(xx), window_length=13, polyorder=1)
# plt.plot(xx, yy)
# inv_cdf = interp1d(yy, xx, bounds_error=False, assume_sorted=True, kind='linear')
#
# # r_random = inv_cdf(np.random.uniform(0, 1, int(round(200 * missing_volume / volume_sphere((r_min + r_max) / 2)))))
# r_random = inv_cdf(np.random.uniform(0, 1, 10000))
# r_random = r_random[~np.isnan(r_random)]
# r_random_it = iter(r_random)
# ecdff = ECDF(r_random)
# plt.plot(ecdff.x, ecdff.y)
# plt.show()