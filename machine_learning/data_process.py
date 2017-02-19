# -*- coding: utf-8 -*-
from natto import MeCab as mecab
import pandas
import numpy as np
import argparse
import re
import collections
import pickle
"""
This program is used for data cleansing
"""
def read_data(p_data):
    df = pandas.read_csv(p_data,delimiter=" ",quoting=2,encoding="utf-8")
    header = df.columns
    values = df.values
    return header,values
def train_test_split(values):
    

#data structure to make
#dictionary which contains {word:[num_of_occur,...,num_of_occur]}

def parse_an_article(string):
    mc = mecab()
    result = mc.parse(string).split("\n")
    result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
    result = [word[0] for word in result[:-1] if word[1]=="名詞"]
    return result

def make_word_number_dict(counters):
    prob_dic={}
    for word,num in counters[9].items():
        word_num = np.ones(9)
        if word in counters[0]:
            word_num[0] += counters[0][word]
        elif word in counters[1]:
            word_num[1] += counters[1][word]  
        elif word in counters[2]:
            word_num[2] += counters[2][word]
        elif word in counters[3]:
            word_num[3] += counters[3][word]
        elif word in counters[4]:
            word_num[4] += counters[4][word]
        elif word in counters[5]:
            word_num[5] += counters[5][word]
        elif word in counters[6]:
            word_num[6] += counters[6][word]
        elif word in counters[7]:
            word_num[7] += counters[7][word]
        elif word in counters[8]:
            word_num[8] += counters[8][word]
        else:
            print(word)
            raise Exception("Something is wrong with your dictionary")
        word_num=np.log(word_num/num)
        prob_dic[word]=word_num

    return prob_dic

def save_data(filename,obj):
    with open(filename,"wb") as f:
        pickle.dump(obj,f)

def make_counters(values):
    #Order of value [title,source,sentence,label]
    counters = [collections.Counter() for i in range(10)]
    for value in values:
        parse_noun = parse_an_article(value[2])
        if value[3] ==1:
            counters[0].update(parse_noun)
        elif value[3] ==2:
            counters[1].update(parse_noun)
        elif value[3] ==3:
            counters[2].update(parse_noun)
        elif value[3] ==4:
            counters[3].update(parse_noun)
        elif value[3] ==5:
            counters[4].update(parse_noun)
        elif value[3] ==6:
            counters[5].update(parse_noun)
        elif value[3] ==7:
            counters[6].update(parse_noun)
        elif value[3] ==8:
            counters[7].update(parse_noun)
        elif value[3] ==9:
            counters[8].update(parse_noun)

    for counter in counters:
        counters[9] += counter
    return counters



if __name__ == '__main__':
    p_data = "../crawling/data-2017-02-18-15-28.csv"
    header,values = read_data(p_data)
    import sys
    import io
    import os 
    os.system("chcp 65001")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    counters = make_counters(values)
    save_data("counters",counters)
    dictionary = make_word_number_dict(counters)
    save_data("dictionary",dictionary)

    
    

    
