import numpy as np
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

x = [30600, 35700, 40800, 45900]
y1 = [0.9737, 0.9739, 0.9742, 0.9746]

name_list4 = ['all', '0:1000', '0:500', '0:250','0:100']
num_list4 = [0.9742, 0.948, 0.943, 0.89, 0.632]

x2 = [0, 10, 20 ,25 ,30, 100]
y2 = [0.9740, 0.9765, 0.9770, 0.9766, 0.9766, 0.968]

x3 = [0, 0.5, 1, 2]
y3 = [0.974, 0.973, 0.973, 0.972]

plt.ylim(ymax=0.980, ymin = 0.970)
plt.xlim(xmax=2.5, xmin=0)

plt.plot(x3, y3, marker='o', mec='r', mfc='w')

plt.title('l-accur')
plt.xlabel('l')
plt.ylabel('accur')

plt.show()
