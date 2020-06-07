import os
import numpy as np
import jieba
import pickle
def clean_data(a):
    '''index = 0
    for i in range(len(a)):
        index+=1
        if(0x4e00<=ord(a[i])<0x9fa6):
            break
    index-=1'''
    a = [a[i] for i in range(len(a)) if(0x4e00<=ord(a[i])<0x9fa6)]
    a = ''.join(a)
    return a

def word_count(a,b):
    for  i in a:
        b[i]=b.get(i,0)+1
    return

def single_data(file, stop_words1, my_stop_words):
    f = open(file)
    par = f.read()
    par = clean_data(par)
    f.close()
    seg_list = jieba.cut(par, cut_all=False)
    seg_list = '\\'.join(seg_list)
    list_b = seg_list.split('\\')
    list_b = [x for x in list_b if(x not in stop_words1)]
    list_b = [x for x in list_b if(x not in my_stop_words)]
    return list_b



index_file = './new/newindex'
f = open(index_file)
index_s = f.readlines()
#index_s[0]=index_s[0].replace('..', '.')
#index_s[0]=index_s[0].split(' ')[1]
#index_s[0]=index_s[0].strip('\n')
index_label = []
for i in range(len(index_s)):
    index_s[i]=index_s[i].replace('..', '.')
    index_buf, index_s[i]=(index_s[i].split(' ')[0],index_s[i].split(' ')[1])
    index_label.append(index_buf)
    index_s[i]=index_s[i].strip('\n')

#print(index_s)
#print(index_label)
index_label = [1 if(x=='spam') else 0 for x in index_label]
#print(index_label)

index_s = index_s[:50000]
index_label = index_label[:50000]

#index_label_file_after = 'datas/index_label'
#index_label_file_after_op = open(index_label_file_after, 'wb')
#pickle.dump(index_label, index_label_file_after_op,2)
#index_label_file_after_op.close()



num = len(index_label)
'''print('num', num)
num_array = np.array(index_label)
spam_num = num_array.sum(axis=0)
print(spam_num)'''#31096/50000


stop_word_file = '中文停用词表.txt'
stop_word_file_op = open(stop_word_file, encoding='utf-8')
stop_words = stop_word_file_op.readlines()
for i in range(len(stop_words)):
    stop_words[i]=stop_words[i].strip('\n')
my_stop_words = ['\n', '\t', ' ']
stop_word_file_op.close()

file_datas = 'datas/par'
file_datas_op = open(file_datas, 'wb')
datas = []

for i in range(len(index_s)):
    file1 = index_s[i]
    list_b = single_data(file1, stop_words, my_stop_words)
    datas.append(list_b)
    if((i+1)%1000==0):
        print('done %d/50000' %(i))

print(datas)
pickle.dump(datas, file_datas_op,2)
file_datas_op.close()


'''
f = open(file1)
par = f.read()
print('par\n',par)
par = clean_data(par)
print(par)
f.close()

seg_list = jieba.cut(par, cut_all=False)
seg_list = '\\'.join(seg_list)
print(seg_list)
list_b = seg_list.split('\\')
print(list_b)
num1 = len(list_b)
''''''word_dict = {}
word_count(par,word_dict)
print('word_dict1', word_dict)''''''
stop_word_file = '中文停用词表.txt'
stop_word_file_op = open(stop_word_file,encoding='utf-8')
stop_words=stop_word_file_op.readlines()
for i in range(len(stop_words)):
    stop_words[i]=stop_words[i].strip('\n')
print(stop_words)
stop_word_file_op.close()
list_b = [x for x in list_b if(x not in stop_words)]
my_stop_words = ['\n', '\t', ' ']
print(list_b)
num2 = len(list_b)
list_b = [x for x in list_b if(x not in my_stop_words)]
num3 = len(list_b)
print('num1', num1, 'num2', num2,'num3', num3)
'''









