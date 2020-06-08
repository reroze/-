import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

name_list1 = ['公司', '发票', '说', '一个']
num_list1 = [1.26, 0.65, 0.57, 0.55]

name_list2 = ['公司', '发票', '有限公司', '合作']
num_list2 = [1.93, 1.06, 0.61,0.60]

name_list3 = ['说', '一个', '没有', '会']
num_list3 = [1.39, 1.05, 0.83, 0.57]

name_list4 = ['all', '0:1000', '0:500', '0:250','0:100']
num_list4 = [97.42, 94.8, 94.3, 89, 63.2]

#rects=plt.bar(range(len(num_list1)), num_list1, color='rgby', align='center')
rects=plt.bar([0.4,1.4,2.4,3.4, 4.4], num_list4, color='rgby', align='center', width=0.5)
# X轴标题
index=[0,1,2,3,4]
index=[float(c)+0.4 for c in index]
plt.ylim(ymax=100, ymin=0)
plt.xticks(index, name_list4)
plt.ylabel("accur(%)") #X轴标签
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height)+'%', ha='center', va='bottom')
plt.show()
