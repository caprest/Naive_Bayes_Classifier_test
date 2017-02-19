import pickle
import numpy as np
from natto import MeCab as mecab
from bs4 import BeautifulSoup
from readability.readability import Document
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


class Classifier():
    def __init__(self,p_file):
        self.categories = categories
        self.prob_dict = self.load_data(p_file)

    def load_data(self,p_file):
        with open(p_file,"rb") as f:
            counters = pickle.load(f)
        return counters

    def get_article_text(self,url):
        data = requests.get(url)
        content = data.content
        readable_html  = Document(content).summary()
        soup = BeautifulSoup(readable_html,"lxml")
        soup.get_text()
        text = soup.get_text().replace("\n"," ")
        return text

    def parse_an_article(self,string):
        mc = mecab()
        result = mc.parse(string).split("\n")
        result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
        result = [word[0] for word in result[:-1] if word[1]=="名詞"]
        return result


    def calic_prob(self,url):
        text = self.get_article_text(url)
        parsed_text = self.parse_an_article(text)
        log_probability = np.zeros(9)
        for word in parsed_text:
            if word in self.prob_dict:
                log_probability +=self.prob_dict[word]
        return log_probability


test_sentences =[
    "野球人生終わった",
    "お笑いタレントとして知られる山田太郎が死んでしまった。",
    "安倍総理がサンバを踊った。"
]




if __name__ == '__main__':
    url ="http://headlines.yahoo.co.jp/hl?a=20170219-00000046-dal-base"
    import sys
    import io # 追加
    import os 
    os.system("chcp 65001")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # 追加
    #print(text)
    classify = Classifier("dictionary")
    prob = classify.calic_prob(url)
    print(prob,classify.categories[np.argmax(prob)])




        
        
