import argparse
import re
import collections
import pickle
import random
import pandas
import numpy as np
import scipy.sparse as sp
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
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





def read_data(p_data):
    df = pandas.read_csv(p_data,delimiter=" ",quoting=2,encoding="utf-8")
    header = df.columns
    values = df.values
    return header,values

def save_data(filename,obj):
    with open(filename,"wb") as f:
        pickle.dump(obj,f)

def make_noun_array_from_article(string):
    mc = mecab()
    mecab_result = mc.parse(string).split("\n")
    mecab_result_array = [re.split(r"\t|,",parsed_word) for parsed_word in mecab_result ]
    noun_array = [word[0] for word in mecab_result_array[:-1] if word[1]=="名詞"]
    return noun_array

def process_dataset(p_csv):
    header,values = read_data(p_csv)
    articles = [value[2] for value in values]
    labels = [value[3] for value in values]
    X_train, X_test, y_train, y_test = train_test_split(articles,labels,test_size = 0.1, random_state=42)
    header,values = read_data(p_csv)
    vectorizer = TfidfVectorizer(max_df=0.5,max_features =3000)
    def generate_article(articles):
        for article in articles:
            noun_array = make_noun_array_from_article(article)
            yield (" ").join(noun_array)
    train_vect = vectorizer.fit_transform(generate_article(X_train))
    test_vect = vectorizer.transform(generate_article(X_test))
    classifier = MultinomialNB().fit(train_vect,y_train)
    pred = classifier.predict(test_vect)
    print(classification_report(y_test, pred,target_names=categories))
    print(confusion_matrix(y_test,pred))
    return vectorizer,classifier



class Classifier():
    def __init__(self,p_model):
        self.categories = categories
        self.vectorizer,self.classifier = self.load_data(p_model)

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

    def make_noun_array_from_article(self,string):
        mc = mecab()
        mecab_result = mc.parse(string).split("\n")
        mecab_result_array = [re.split(r"\t|,",parsed_word) for parsed_word in mecab_result ]
        noun_array = [word[0] for word in mecab_result_array[:-1] if word[1]=="名詞"]
        return noun_array

    def calic_label_from_text(self,text):
        if text:
            noun_array = self.make_noun_array_from_article(text)
            vector = self.vectorizer.transform([" ".join(noun_array)])
            label = self.classifier.predict(vector)[0]
        else:
            label = 9 
        return int(label)

    def calic_label(self,url):
        text = self.get_article_text(url)
        label = self.calic_label_from_text(text)
        return label

    def calic_label_name(self,url):
        label = self.calic_label(url)
        return self.categories[label-1]




if __name__ == "__main__":
    p_csv = "data-2017-03-15-13-31.csv"
    vectorizer,classifier = process_dataset(p_csv)
    save_data("model-"+p_csv,[vectorizer,classifier])
    web_classifier = Classifier("model-"+p_csv)
    a = web_classifier.calic_label("https://gunosy.com/articles/RPddv")
    print(a)
    print(web_classifier.calic_label_name("https://gunosy.com/articles/RPddv"))