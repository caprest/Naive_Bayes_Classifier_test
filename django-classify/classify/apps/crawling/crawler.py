# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import csv
import pandas as pd 
import time
from time import sleep
import article
import argparse
import json

import sys
import io # 追加
import os
#os.system("chcp 65001")
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # 追加



time_now = time.strftime("%Y-%m-%d-%H-%M",time.localtime())
save_url = "urls-"+time_now+".csv"

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

def make_url_list(save_name):
    f = open(save_url,'w')
    for i in range(1,9):
        urls =[]
        for j in range(1,2):
            address = "https://gunosy.com/categories/{i}?page={j}".format(i=i,j=j)
            data = requests.get(address)
            content = data.content
            soup = BeautifulSoup(content,"lxml")
            samples  =soup.select(".list_title")
            for sample in samples:
                sample = sample.find("a")
                f.write(sample["href"]+" "+str(i)+"\n")
    f.close()

def clawling(url_list,save_name):
    df = pd.read_csv(url_list,skiprows=None,delimiter=" ")
    values = []
    for i,url in df.iterrows():
        start = time.time()
        value = article.process_article(url)
        #Order of value [title,source,sentence,label]
        if value !=None:
            values.append(value)
        used_time = time.time()-start
        if used_time < 1:
            time.sleep(1-used_time)
    f = open(save_name,"w",encoding="utf-8")
    csv_writer = csv.writer(f,delimiter = " ",quoting = csv.QUOTE_NONNUMERIC)
    order_of_value = ["title","source","sentence","label"]
    csv_writer.writerow(order_of_value)
    for value in values:
        csv_writer.writerow(value)    
    f.close()
        
def test_clawler():
    clawling("urls-2017-02-09-21-43.csv","save_test")


if __name__ == '__main__':
    time_now = time.strftime("%Y-%m-%d-%H-%M",time.localtime())
    p_save_url = "urls-"+time_now+".csv"
    p_save_data = "data-"+time_now+".csv"
    #I'll make branch if you don't need to make url list using argparse
    #temp_name = "urls-2017-02-09-21-43.csv"
    #test_clawler()
    make_url_list(p_save_url)
    print("url_list_make_done")
    clawling(p_save_url,p_save_data)
