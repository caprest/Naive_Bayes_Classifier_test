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
    "Gourmet",
    "Error"
]


class Classifier():
    def __init__(self,p_file):
        self.categories = categories
        self.prob_dict = self.load_data(p_file)

    def load_data(self,p_file):
        with open(p_file,"rb") as f:
            data = pickle.load(f)
        return data

    def get_article_text(self,url):
        try:
            data = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            print("Failed to Get Article")
            text = None
        else:
            if data.status_code ==requests.codes.ok: 
                content = data.content
                readable_html  = Document(content).summary()
                soup = BeautifulSoup(readable_html,"lxml")
                soup.get_text()
                text = soup.get_text().replace("\n"," ")
            else:
                print("Failed to Get Article")
                text = None
        return text

    def make_vocab_from_article(self,string):
        mc = mecab()
        result = mc.parse(string).split("\n")
        result = [re.split(r"\t|,",parsed_word) for parsed_word in result ]
        result = [word[0] for word in result[:-1] if word[1]=="名詞"]
        vocab = set(result)
        return vocab
    
    def calic_prob_from_text(self,text):
        log_probability = np.zeros(9)
        if text != None:
            vocab = self.make_vocab_from_article(text)
            for word in vocab:
                if word in self.prob_dict:
                    log_probability +=self.prob_dict[word]
        else:
            pass
        return log_probability

    def calic_prob(self,url):
        text = self.get_article_text(url)
        log_probability = self.calic_prob_from_text(text)
        return log_probability

    def calic_label_from_text(self,text):
        prob = self.calic_prob_from_text(text)
        if all(prob == np.zeros(9)):
            return 9
        else:
            return np.argmax(prob)

    def calic_label(self,url):
        text = self.get_article_text(url)
        log_probability = self.calic_label_from_text("text")
        return log_probability

    def calic_label_name(self,url):
        label = self.calic_label(url)
        return self.categories[label]


    def validate_accuracy(self,test):
        correct = 0
        all_number = len(test)
        for line in test:
            label = self.calic_label_from_text(line[2])
            if label == line[3]-1:
                correct +=1
        accuracy = correct / all_number
        print("Accuracy = "+str(accuracy))
        print("Correct Answer {}/{}".format(correct,all_number))
        return accuracy            


test_sentences =[
    "野球人生終わった",
    "お笑いタレントとして知られる山田太郎が死んでしまった。",
    "安倍総理がサンバを踊った。"
    ""
]
test_url = ["https://gunosy.com/articles/RChau","hoge","http://sonzaisinai.com/ningensei/dame"]

def test(test_url,test_sentences,test_dic_path):
    classify = Classifier(test_dic_path)
    def test_calic_prob(url):
        try:
            prob = classify.calic_prob(url)
        except:
            print("Error with Classify.calic_prob")
            print("Input = "+str(url))
            raise 
    def test_calic_label(url):
        try:
            prob = classify.calic_label(url)
        except:
            print("Error with Classify.calic_prob")
            print("Input = "+str(url))
            raise
    def test_calic_label_from_text(sentence):
        try:
            label = classify.calic_label_from_text(sentence)
            print(sentence+classify.categories[int(label)])
        except:
            print("Error with Classify.calic_label_from_text")
            print("Input = "+sentence)
            raise
    for url in test_url:
        test_calic_prob(url)
        test_calic_label(url)
    
    for sentence in test_sentences:
        test_calic_label_from_text(sentence)
    print("NO ERROR OCCURED")

def test_accuracy(test_dic_path,test_data_path):
    classify = Classifier(test_dic_path)
    test = classify.load_data(test_data_path)
    accuracy = classify.validate_accuracy(test)
    return accuracy


if __name__ == '__main__':
    test_dic_path = "dictionary_first"
    test_data_path = "testdata-first"
    test(test_url,test_sentences,test_dic_path)
    print("start Accuracy test")
    accuracy = test_accuracy(test_dic_path,test_data_path)




        
        
