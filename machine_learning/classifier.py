import pickle
import numpy as np
from natto import MeCab as mecab
from bs4 import BeautifulSoup
import requests
import re

categories =[
    "Entertainment",
    "Sports",
    "Funny",
    "Domestic",
    "Foreign",
    "Column",
    "Science",
    "Gourmet"
]


def load_data(p_file):
    with open(p_file,"rb") as f:
        counters = pickle.load(f)
    return counters



def get_article_text_without_link(url):
    data = requests.get(url)
    content = data.content
    soup = BeautifulSoup(content,"lxml")
    soup.find("a").extract()
    soup.get_text()
    text = soup.get_text()
    return text

def parse_an_article(string):
    mc = mecab()
    result = mc.parse(string).split("\n")
    result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
    result = [word[0] for word in result[:-1] if word[1]=="名詞"]
    return result


def caliculate_probability(prob_dict,text):
    parsed_text = parse_an_article(text)
    log_probability = np.zeros(9)
    for word in parsed_text:
        if word in prob_dict:
            log_probability +=prob_dict[word]
    return log_probability

def basic_test(prob_dict):
    text1 = "野球人生終わった"
    text2 = "お笑いタレントとして知られる山田太郎が死んでしまった。"
    text3 = "安倍総理がサンバを踊った。"
    prob1 = caliculate_probability(prob_dict,text1)
    prob2 = caliculate_probability(prob_dict,text2)
    prob3 = caliculate_probability(prob_dict,text3)
    print(prob1,categories[np.argmax(prob1)])
    print(prob2,categories[np.argmax(prob2)])
    print(prob3,categories[np.argmax(prob3)])

if __name__ == '__main__':
    counters = load_data("save_name")
    url ="http://www3.nhk.or.jp/news/html/20170219/k10010882411000.html"
    text = get_article_text_without_link(url)
    import sys
    import io # 追加
    import os 
    os.system("chcp 65001")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # 追加
    #print(text)
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
    prob = caliculate_probability(prob_dic,text)
    print(prob,categories[np.argmax(prob)])
    #test
    basic_test(prob_dic)


        
        
