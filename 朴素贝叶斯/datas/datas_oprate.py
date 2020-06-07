import pickle
import math
import numpy as np
import random
#加一个随机算法，增强效果
datas_file = 'par'
datas_file_op = open(datas_file, 'rb')

datas = pickle.load(datas_file_op)
datas_file_op.close()
#print(len(datas))
#print(datas[2])
index_label_file = 'index_label'
index_label_file_op = open(index_label_file, 'rb')
index_label = pickle.load(index_label_file_op)#spam（垃圾邮件）:1 ham:0
index_label_file_op.close()

random_list = 'random_list'
random_list_op = open(random_list, 'wb')

#print(len(index_label))
#
train_data=[]
train_data_label=[]
test_data=[]
test_data_label=[]
index_list = random.sample(range(50000), 35000)#40000:0.9787
pickle.dump(index_list, random_list_op, 2)
random_list_op.close()
for i in range(50000):
    if i in index_list:
        train_data.append(datas[i])
        train_data_label.append(index_label[i])
    else:
        test_data.append(datas[i])
        test_data_label.append(index_label[i])




print('train_data_len', len(train_data))
print('test_data_len', len(test_data))

train_data_array = np.array(train_data_label)
label = train_data_array.sum()
print('label', label)#21778
#21797 :14612,0.974133    21912:14630 21786:14633#0.975
test_data_array = np.array(test_data_label)
label+=test_data_array.sum()
print('all_label', label)#31096
#
#24500

#
test_yuce = []

#分别对垃圾邮件和非垃圾邮件设置两个单词频率词典
def word_pro_tab(data, data_label,label, word_prob_dict):
    num = len(data)
    word_num = 0
    for i in range(num):
        if(data_label[i]==label):
            word_num+=len(data[i])
            for j in range(len(data[i])):
                word_prob_dict[data[i][j]]=word_prob_dict.get(data[i][j], 0)+1
        #if((i+1)%10000==0):
            #print('done %d' %(i))
    return word_num

def word_dict2list_train(data, data_label, sign):
    word_dict={}
    word_pro_tab(data, data_label, sign, word_dict)
    word_list_1 = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
    word_num=0
    word_list_1 = [x for x in word_list_1 if(x[1]>=0)]
    word_reallist = [list(x) for x in word_list_1]
    for x in word_reallist:
        word_num+=x[1]
    for i in range(len(word_reallist)):
        word_reallist[i][1]/=word_num
    return word_reallist

def word_dict2list_test(test_single):
    word_dict={}
    for x in test_single:
        word_dict[x]=word_dict.get(x, 0)+1
    return word_dict

def result(ham_word_dict, spam_word_dict, less_ham_prob, less_spam_prob, test_single):
    spam_prob=0
    ham_prob=0
    for x in test_single:
        spam_prob+=test_single[x]*math.log(spam_word_dict.get(x, less_spam_prob))
        ham_prob+=test_single[x]*math.log(ham_word_dict.get(x,less_ham_prob))
    return spam_prob,ham_prob




train_ham_word_list = word_dict2list_train(train_data, train_data_label, 0)
less_ham_pro = train_ham_word_list[-1][1]
print(less_ham_pro)
print(math.log(less_ham_pro))
train_spam_word_list = word_dict2list_train(train_data, train_data_label, 1)
less_spam_pro = train_spam_word_list[-1][1]
print(less_spam_pro)
print(math.log(less_spam_pro))



train_spam_word_dict={}
for x in train_spam_word_list:
    train_spam_word_dict[x[0]]=x[1]
train_ham_word_dict={}
for x in train_ham_word_list:
    train_ham_word_dict[x[0]]=x[1]

accur=0
for i in range(len(test_data)):
    label_yuce=0
    test_single_dict = word_dict2list_test(test_data[i])
    #print(test_single_dict)
    #print(test_data_label[0])
    spam_prob, ham_prob = result(train_ham_word_dict, train_spam_word_dict, less_ham_pro, less_spam_pro, test_single_dict)
    if(spam_prob>=ham_prob):
        label_yuce=1
    else:
        label_yuce=0
    if(label_yuce==test_data_label[i]):
        accur+=1

    if((i+1)%3000==0):
        #print('done %d' %(i))
        print(accur)
        #print('spam_prob', spam_prob)
        #print('ham_prob', ham_prob)

print('accur', accur)
#print(train_ham_word_list[0])
'''
train_ham_word_dict = {}
train_ham_word_num=word_pro_tab(train_data, train_data_label, 0, train_ham_word_dict)
#print(train_ham_word_dict)
#print('train_ham_word_num1:' ,train_ham_word_num)
train_ham_word_list = sorted(train_ham_word_dict.items(), key = lambda x:x[1], reverse=True)
#print(len(train_ham_word_list))
train_ham_word_list = [x for x in train_ham_word_list if(x[1]>=5)]
train_ham_word_reallist = [list(x) for x in train_ham_word_list]
train_ham_word_num=0
for x in train_ham_word_reallist:
    train_ham_word_num+=x[1]
#print('train_ham_word_num2:', train_ham_word_num)
for i in range(len(train_ham_word_reallist)):
    train_ham_word_reallist[i][1]/=train_ham_word_num
#print(train_ham_word_dict)
#print(len(train_ham_word_list))
#print(train_ham_word_reallist[0])#['说', 0.0140226425176968]

train_spam_word_dict = {}
train_spam_word_num = word_pro_tab(train_data, train_data_label, 1, train_spam_word_dict)#2680620
train_spam_word_list = sorted(train_spam_word_dict.items(), key=lambda x:x[1], reverse=True)
#print(train_spam_word_num)#2680620
train_spam_word_num=0
#print(len(train_spam_word_list))#39043
train_spam_word_list = [x for x in train_spam_word_list if(x[1]>=5)]
#print(len(train_spam_word_list))#21856
train_spam_word_reallist = [list(x) for x in train_spam_word_list]
for x in train_spam_word_reallist:
    train_spam_word_num+=x[1]
#print(train_spam_word_num)#2646900
for i in range(len(train_spam_word_reallist)):
    train_spam_word_reallist[i][1]/=train_spam_word_num
print(train_spam_word_reallist[0])#['公司', 0.02066530658506177]
'''

