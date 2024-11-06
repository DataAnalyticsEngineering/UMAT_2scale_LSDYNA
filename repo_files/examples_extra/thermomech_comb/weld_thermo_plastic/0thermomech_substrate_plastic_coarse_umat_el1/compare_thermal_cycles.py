import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy.interpolate import interp1d

plt.figure()

min_temp = 670  # 673.15

for file_name in sorted(glob.glob("*.txt")):
    dataframe = pd.read_csv(file_name, header=0, sep='\t')
    df = dataframe[['Zeit [ms]', 'T1']]
    arr = np.array(df.dropna(thresh=2))
    arr[:, 1] += 273.15
    arr = arr[arr[:, 1] >= min_temp]
    arr[:, 0] -= arr[0, 0]
    arr[:, 0] /= 1000
    # arr = arr[arr[:, 0] <= 25]
    if '1.6' in file_name:
        plt.plot(arr[:, 0], arr[:, 1], label=file_name, ls='dashdot', color='green')
    else:
        plt.plot(arr[:, 0], arr[:, 1], label=file_name, ls='--', color='blue')
    if '1.8kW_3' in file_name:
        exp_fun = interp1d(arr[:, 0], arr[:, 1], bounds_error=False, assume_sorted=True)

df = pd.read_csv('temp0.csv', header=1)
arr2 = np.array(df.dropna(thresh=2))
arr2 = arr2[arr2[:, 1] >= min_temp]
idx = np.searchsorted(arr[:, 1][0:50], arr2[0, 1])
# idx = np.searchsorted(arr[:, 1][0:50], arr2[0, 1], side='right')
arr2[:, 0] -= arr2[0, 0]
arr2[:, 0] += arr[:, 0][idx]
plt.plot(arr2[:, 0], arr2[:, 1], label='Simulation', marker="*", markersize=5, color='black')

# compute the maximum error w.r.t experiment
sim_fun = interp1d(arr2[:, 0], arr2[:, 1], bounds_error=False, assume_sorted=True)
x_vec = np.linspace(0, 25, 50)
y_vec_sim = sim_fun(x_vec)
y_vec_exp = exp_fun(x_vec)
# plt.plot(x_vec, y_vec_sim, label='Simulation2', marker="+", ls='--', markersize=5, color='gray')
# plt.plot(x_vec, y_vec_exp, label='Experiment', marker="+", ls='--', markersize=5, color='gray')
print(f'Largest error {np.max(np.abs((y_vec_sim-y_vec_exp)/y_vec_exp)) * 100:.2f}%')

plt.xlim([0, 300])
# plt.ylim([700, 1025])
# plt.xlabel('Time [Sec]', fontsize=18)
# plt.ylabel('Temperature [K]', fontsize=18)

plt.grid('on')
plt.legend()
plt.tight_layout()
plt.savefig('thermal_cycles_v01.pdf', dpi=300)
plt.show()
