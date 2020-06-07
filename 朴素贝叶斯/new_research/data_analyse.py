import pickle
import numpy as np

def data_split(datas, labels):
    spam_data=[]
    ham_data=[]
    for i in range(len(datas)):
        if(labels[i]==1):
            spam_data.append(datas[i])
        else:
            ham_data.append(datas[i])
    return spam_data, ham_data

def word_dict(data):
    dict = {}
    word_num=0
    for i in range(len(data)):
        word_num += len(data[i])
        for j in range(len(data[i])):
            dict[data[i][j]]=dict.get(data[i][j], 0)+1
    word_list = sorted(dict.items(), key=lambda x:x[1], reverse=True)
    word_list_2 = [[x[0], x[1]] for x in word_list]
    word_list_2 = [[x[0], x[1]/word_num] for x in word_list_2]
    word_dict = {}
    for x in word_list_2:
        word_dict[x[0]]=x[1]
    return word_dict, word_num, word_list_2




datas = []
labels = []
file_data='./par'
file_data_op = open(file_data, 'rb')
datas=pickle.load(file_data_op)
file_data_op.close()

file_label='./index_label'
file_label_op = open(file_label, 'rb')
labels=pickle.load(file_label_op)
file_label_op.close()

print(len(datas))#51000
print(len(labels))#51000
'''
labels_array = np.array(labels)
a = labels_array.sum()
print(a)#31826/51000=0.6240
0.6240+0.3759=1
'''
word_num_dict={}
total_num=0

for i in range(len(datas)):
    total_num+=len(datas[i])
    for j in range(len(datas[i])):
        word_num_dict[datas[i][j]]=word_num_dict.get(datas[i][j], 0)+1

word_list1 = sorted(word_num_dict.items(), key=lambda x:x[1], reverse=True)
word_list2 = [[x[0], x[1]] for x in word_list1]
word_list2 = [[x[0], x[1]/total_num] for x in word_list2]
#print(total_num)#6573715 一共词数
#print(word_list2[:10])#[['公司', 0.012615697516548861], ['发票', 0.006576342296555297], ['说', 0.005733896282391311], ['一个', 0.00556352077934623], ['没有', 0.004108027196189673],

#all_word_pro_file = './all_word_times'
#all_word_pro_file_op = open(all_word_pro_file, 'wb')
#pickle.dump(word_list2,all_word_pro_file_op, 2)
#all_word_pro_file_op.close()

spam_data, ham_data = data_split(datas, labels)
spam_dict, spam_word_num, spam_word_list = word_dict(spam_data)
ham_dict, ham_word_num, ham_word_list = word_dict(ham_data)

print('word', word_list2[:10])
'''[['公司', 0.012615697516548861], ['发票', 0.006576342296555297], ['说', 0.005733896282391311],
 ['一个', 0.00556352077934623], ['没有', 0.004108027196189673], ['有限公司', 0.0038174761151038646],
  ['合作', 0.0038059149202543767], ['企业', 0.003528446243866672], ['管理', 0.003466076640073383], 
  ['会', 0.003353963474230325]]
'''
print('spam_word', spam_word_list[:10])
'''[['公司', 0.019333123659587167], ['发票', 0.010691381443972445], ['有限公司', 0.006105118802612789], 
['合作', 0.006021232807392063], ['企业', 0.005463477547133907], ['管理', 0.005363507216546376], 
['优惠', 0.005305108706599205], ['服务', 0.005103930788857465], ['贵', 0.004354895663390989], 
['网站', 0.004180937390116151]]
'''
print(spam_word_num)#4041199
print('ham_word', ham_word_list[:10])
'''[['说', 0.013906723590295185], ['一个', 0.010523921665253053], ['没有', 0.008378229397168665], 
['会', 0.005750013030519847], ['想', 0.005117835385837642], ['知道', 0.0050337293031909765], 
['觉得', 0.004887629535213203], ['现在', 0.004505006088806547], ['做', 0.003970754775093227], 
['没', 0.003451903166653241]]
'''
print(ham_word_num)#2532516





