# -*- coding: utf-8 -*-
from natto import MeCab as mecab
import pandas
import numpy as np

import argparse
import re
import collections
import pickle
import random
random.seed(111)

def read_data(p_data):
    df = pandas.read_csv(p_data,delimiter=" ",quoting=2,encoding="utf-8")
    header = df.columns
    values = df.values
    return header,values

def train_test_split(values):
    train = []
    test = []
    train_rate = 0.9
    train_num = np.floor(len([value for value in values if value[3] == 1])*0.9)
    for label in range(1,9):
        values_label = [value for value in values if value[3] == label]
        length = len(values_label)
        if length<train_num:
            print("something wrong with label"+str(label))
            pass
        else:
            random.shuffle(values_label)
            train.extend(values_label[0:int(train_num)])
            test.extend(values_label[int(train_num):])

    return train,test,train_num

def make_vocab_from_article(string):
    mc = mecab()
    result = mc.parse(string).split("\n")
    result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
    result = [word[0] for word in result[:-1] if word[1]=="名詞"]
    vocab = set(result)
    return vocab

def make_counters(values):
    #Order of value [title,source,sentence,label]
    counters = [collections.Counter() for i in range(10)]
    for value in values:
        vocab = make_vocab_from_article(value[2])
        if value[3] ==1:
            counters[0].update(vocab)
        elif value[3] ==2:
            counters[1].update(vocab)
        elif value[3] ==3:
            counters[2].update(vocab)
        elif value[3] ==4:
            counters[3].update(vocab)
        elif value[3] ==5:
            counters[4].update(vocab)
        elif value[3] ==6:
            counters[5].update(vocab)
        elif value[3] ==7:
            counters[6].update(vocab)
        elif value[3] ==8:
            counters[7].update(vocab)
        elif value[3] ==9:
            counters[8].update(vocab)
    for counter in counters:
        counters[9] += counter
    return counters

def make_word_number_dict(counters,train_num):
    prob_dic={}
    for word,num in counters[9].items():
        word_num = np.ones(9)
        if word in counters[0]:
            word_num[0] += counters[0][word]
        if word in counters[1]:
            word_num[1] += counters[1][word]  
        if word in counters[2]:
            word_num[2] += counters[2][word]
        if word in counters[3]:
            word_num[3] += counters[3][word]
        if word in counters[4]:
            word_num[4] += counters[4][word]
        if word in counters[5]:
            word_num[5] += counters[5][word]
        if word in counters[6]:
            word_num[6] += counters[6][word]
        if word in counters[7]:
            word_num[7] += counters[7][word]
        if word in counters[8]:
            word_num[8] += counters[8][word]
        prob=np.log(word_num/(train_num+1))
        prob_dic[word]=prob
    return prob_dic

def save_data(filename,obj):
    with open(filename,"wb") as f:
        pickle.dump(obj,f)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script process data for machine learning")
    parser.add_argument("path",type=str,help="path of your learning data")
    parser.add_argument("-s","--split",action ="store_true",help="Whether you want to split the data")
    args =parser.parse_args()
    p_data = args.path
    n_data = "".join(p_data.split(".")[:-1])
    header,values = read_data(p_data)
    train,test,train_num = train_test_split(values)
    counters = make_counters(train)
    save_data("train"+n_data,train)
    save_data("test"+n_data,test)
    if args.split == False:
        dictionary = make_word_number_dict(counters,train_num)
        save_data("dictionary_"+n_data,dictionary)

    
    

    
