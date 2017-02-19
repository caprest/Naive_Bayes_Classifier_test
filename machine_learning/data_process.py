# -*- coding: utf-8 -*-
from natto import MeCab as mecab
import pandas
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


#data structure to make
#dictionary which contains {word:[num_of_occur,...,num_of_occur]}

def parse_an_article(string):
    mc = mecab()
    result = mc.parse(string).split("\n")
    result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
    result = [word[0] for word in result[:-1] if word[1]=="名詞"]
    return result

def save_data(filename,obj):
    with open(filename,"wb") as f:
        pickle.dump(obj,f)


if __name__ == '__main__':
    p_data = "../crawling/data-2017-02-18-15-28.csv"
    header,values = read_data(p_data)
    import sys
    import io # 追加
    import os 
    os.system("chcp 65001")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # 追加
    #Order of value [title,source,sentence,label]
    mc = mecab()
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
    save_data("save_name",counters)

    
    

    
