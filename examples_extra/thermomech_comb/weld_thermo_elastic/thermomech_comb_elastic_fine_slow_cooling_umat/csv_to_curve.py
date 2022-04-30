import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

x_scaling_factor = 1.
y_scaling_factor = 1.
x_offset = 0.
y_offset = 0.

output_file = 'curves.k'

input_dictionary = {'*keyword': []}
for file_name in sorted(glob.glob("*crv*.csv")):
    curve_id = file_name.split('_', 1)[0]

    dataframe = pd.read_csv(file_name, header=None)

    input_dictionary[f'*DEFINE_CURVE_del{curve_id}'] = [[curve_id, 0, x_scaling_factor, y_scaling_factor, x_offset, y_offset],
                                                        *list(np.asarray(dataframe))]

input_dictionary['*end'] = []

with open(output_file, 'w') as file:
    for key, val in input_dictionary.items():
        if 'del' in key:
            key = key.split('_del', 1)[0]

        print(key)
        file.write(key + '\n')

        for line in val:
            output_line = ''.join([f'{li:},' for li in line])[:-1]
            print(output_line)
            file.write(output_line + '\n')
