import  numpy  as np
from pyhdf.SD import SD, SDC
file = SD('/home/alameddin/src/0data/simkom_input_images/WS_2a.hdf', SDC.READ)
print(file.info())
print(file.datasets())

kt = file.select('Not specified')
print(kt.dimensions())

print(np.count_nonzero(kt[0:200,0:200,0:200]))

print(np.unique(kt[0:200,0:200,0:200]))
# print(kt[0:200,0:200,0:200])

from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt

for i in [0,50,100,150,200,250,350,450,550,650,750,850,900,950,980]:
    plt.figure()
    imshow(kt.get()[i,:,:])

plt.show()

img = kt.get()
#%%
for i in [850,860,870,880,885,900,950,980]:
    imshow(img[i,:,:])
    plt.show()


# datasets_dic = file.datasets()
#
# for idx,sds in enumerate(datasets_dic.keys()):
#     print( idx,sds)
