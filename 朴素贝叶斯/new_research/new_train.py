import pickle
import random
import math
import os
from new_data_load import single_data
#1.	比较51000和50000的数据准确率 to do
#2.	尝试去除一些常用词之后的准确率 不行
#3.	进行轮回测试 结果稳定
#4.比较整个数据集中词的频率 重复较少
#5.使用不同的训练词数，比如前1000个单词 影响较小
#6.加入先验 效果还行
#7.加入滑动平均 效果不行
#8.改变训练样本测试 to do
#9.使用自己的邮件测试鲁棒性 to do done



random_list = random.sample(range(51000), 45900)#15300*3=45900
#print(random_list)

test_list = [random_list[:15300], random_list[15300:30600], random_list[30600:45900]]
#print(test_list[0])#分出循环训练的三个列表




def data_create(datas, labels, list):
    train_datas=[]
    train_labels=[]
    test_datas=[]
    test_labels=[]
    for i in range(len(datas)):
        if(i in list):
            test_datas.append(datas[i])
            test_labels.append(labels[i])
        else:
            train_datas.append(datas[i])
            train_labels.append(labels[i])
    return train_datas, train_labels, test_datas, test_labels

def dict_to_list_sort(dict):
    list1 = sorted(dict.items(), key = lambda x:x[1], reverse=True)
    list2 = [[x[0], x[1]] for x in list1]
    return list2

def train(train_datas, train_labels):
    '''
    给训练数据，得到对应的词典和频率(需和label对应)
    :return:
    '''
    word_prob_dict_spam = {}
    word_num_spam = 0
    word_prob_dict_ham={}
    word_num_ham = 0
    for i in range(len(train_datas)):
        if(train_labels[i]==1):
            word_num_spam+=len(train_datas[i])
            for j1 in range(len(train_datas[i])):
                word_prob_dict_spam[train_datas[i][j1]] = word_prob_dict_spam.get(train_datas[i][j1], 0)+1
        else:
            word_num_ham+=len(train_datas[i])
            for j2 in range(len(train_datas[i])):
                word_prob_dict_ham[train_datas[i][j2]]=word_prob_dict_ham.get(train_datas[i][j2], 0)+1

    word_spam_list=dict_to_list_sort(word_prob_dict_spam)
    word_ham_list = dict_to_list_sort(word_prob_dict_ham)
    #增加滑动平均
    #word_spam_list = [[x[0], (x[1]+0.5)/(word_num_spam+0.5*len(word_spam_list))] for x in word_spam_list]
    #word_ham_list = [[x[0], (x[1]+0.5)/(word_num_ham+0.5*len(word_ham_list))] for x in word_ham_list]
    #加入滑动平均反而下降了0.973
    #2倍滑动平均则降到了0.972
    #0.5倍平均到了0.973

    #观察对应list的长度，看使用其中的多少对结果影响较小

    word_spam_list = [[x[0], x[1]/word_num_spam] for x in word_spam_list]
    word_ham_list = [[x[0], x[1]/word_num_ham] for x in word_ham_list]
    #print('spam_prob_test', word_spam_list[1000])#['应', 0.0001480585774856968]
    #print('ham_prob_test', word_ham_list[1000])#['学费', 0.00015576198184622946]
    return word_spam_list, word_ham_list#全部都用0.9743137，只用前1000个0.948，#前100个0.632

def test_dict_create(test_single):
    test_dict = {}
    for x in test_single:
        test_dict[x]=test_dict.get(x, 0)+1
    return test_dict

def single_test_eval(train_spam_dict, train_ham_dict, test_single,less_spam_prob,less_ham_prob):
    spam_prob = 0
    ham_prob = 0
    test_dict = test_dict_create(test_single)
    for x in test_dict:
        spam_prob+=test_dict[x]*math.log(train_spam_dict.get(x, less_spam_prob))
        ham_prob+=test_dict[x]*math.log(train_ham_dict.get(x,less_ham_prob))
    label=0
    #加入先验0.6240+0.3759 的结果是0.97446623 #$加入权重较大的先验概率
    #加入10倍的先验：结果是0.9765
    #加入100倍的先验0.968
    #加入20倍的先验0.9770 0.97666
    #加入30倍的先验0.9766
    #加入25倍的先验0.9766
    #spam_prob += 20*math.log(0.6240)
    #ham_prob += 20*math.log(0.3759)
    if(spam_prob>=ham_prob):
        label=1
    else:
        label=0
    return label, spam_prob, ham_prob




def test(train_spam_dict, train_ham_dict, test_datas, test_labels, less_spam_prob, less_ham_prob):
    accur=0
    for i in range(len(test_datas)):
        label, spam_prob, ham_prob = single_test_eval(train_spam_dict, train_ham_dict, test_datas[i],less_spam_prob, less_ham_prob)
        if(label==test_labels[i]):
            accur+=1
        #else:
            #print(i, 's', spam_prob, 'h', ham_prob)
    accur /= len(test_datas)
    return accur

def split_train(datas, labels, test_list):
    accur_all=0
    for list1 in test_list:
        train_datas, train_labels, test_datas, test_labels = data_create(datas, labels, list1)
        train_spam_list, train_ham_list = train(train_datas, train_labels)
        train_spam_dict={}
        train_ham_dict={}
        for x in train_spam_list:
            train_spam_dict[x[0]]=x[1]
        for x in train_ham_list:
            train_ham_dict[x[0]]=x[1]
        less_spam_prob = train_spam_list[-1][1]
        less_ham_prob = train_ham_list[-1][1]
        accur = test(train_spam_dict, train_ham_dict, test_datas, test_labels, less_spam_prob, less_ham_prob)
        print('training', accur)
        accur_all += accur
    accur_all /= 3
    print('train_accur', accur_all)

def test_myself_data(datas, labels, test_list):
    accur_all = 0
    test_file = input('please input the file name:')
    own_dir = '../own_data'
    test_file = os.path.join(own_dir, test_file)

    stop_word_file = '../中文停用词表.txt'
    stop_word_file_op = open(stop_word_file, encoding='utf-8')
    stop_words = stop_word_file_op.readlines()
    for i in range(len(stop_words)):
        stop_words[i] = stop_words[i].strip('\n')
    my_stop_words = ['\n', '\t', ' ']
    stop_word_file_op.close()

    list_b = single_data(test_file, stop_words, my_stop_words)
    print(list_b)
    #raise Exception





    for list1 in test_list:
        train_datas, train_labels, test_datas, test_labels = data_create(datas, labels, list1)
        train_spam_list, train_ham_list = train(train_datas, train_labels)
        train_spam_dict={}
        train_ham_dict={}
        for x in train_spam_list:
            train_spam_dict[x[0]]=x[1]
        for x in train_ham_list:
            train_ham_dict[x[0]]=x[1]
        less_spam_prob = train_spam_list[-1][1]
        less_ham_prob = train_ham_list[-1][1]

        label,spam_prob,ham_prob = single_test_eval(train_spam_dict, train_ham_dict,list_b, less_spam_prob, less_ham_prob)
        if(label==0):
            print('label:ham')
        else:
            print('label:spam')
        print('spam_prob:', spam_prob, 'ham_prob:', ham_prob)




data_file = './par'
label_file = './index_label'

data_file_op = open(data_file, 'rb')
datas = pickle.load(data_file_op)
data_file_op.close()

label_file_op = open(label_file, 'rb')
labels = pickle.load(label_file_op)
label_file_op.close()

#split_train(datas, labels, test_list)
test_myself_data(datas, labels, test_list)


#training 0.9745098039215686
#training 0.9733333333333334
#training 0.9743790849673203
#train_accur 0.974074074074074

'''
train_datas, train_labels, test_datas, test_labels = data_create(datas, labels, test_list[0])
train_spam_list, train_ham_list = train(train_datas, train_labels)
print('spam_list')
print(len(train_spam_list))#41959
#print(train_spam_list[:3])
print('ham_list')
print(len(train_ham_list))#87359
#print(train_ham_list[:3])

train_spam_dict = {}
train_ham_dict = {}
for x in train_spam_list:
    train_spam_dict[x[0]]=x[1]
for x in train_ham_list:
    train_ham_dict[x[0]]=x[1]

less_spam_prob = train_spam_list[-1][1]
#print('less_spam_prob', less_spam_prob)#3.521351184705786e-07
less_ham_prob = train_ham_list[-1][1]
#print('les_ham_prob', less_ham_prob)#5.677047526538778e-07
#raise Exception

#print('统计')'''
'''for i in range(1000):
    if(train_spam_list[i][0]==train_ham_list[i][0]):
        print(train_spam_list[i][0])'''#none
'''for x in train_spam_dict:
    if(train_spam_dict[x]>0.002 and train_ham_dict.get(x, 0)>0.002):#0.003none
        print(x, train_spam_dict[x], train_ham_dict[x])
        #做0.0027:0.0039;，朋友0.0027:0.0020;，工作0.0027:0.00336;，中国0.0026:0.0021;，
        一个0.0024:0.010;，月0.0025:0.0021;，
        中0.0021:0.00289;
'''
'''
#寻找两个词典中相差较小的两对对应词


#print(train_spam_dict['统计'])#0.0003743
#print(train_ham_dict['统计'])#7.0980080e-5

accur = test(train_spam_dict, train_ham_dict, test_datas, test_labels, less_spam_prob, less_ham_prob)
print(accur)
'''
