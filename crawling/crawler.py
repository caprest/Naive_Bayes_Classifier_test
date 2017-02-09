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
    for i in range(1,8):
        urls =[]
        for j in range(1):
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
    f = open(save_name,"w")
    start = time.time()
    df = pd.read_csv(url_list,skiprows=None,delimiter=" ")
    for i, row in df.iterrows():
        value_dict = article.process_article(row)
        if value_dict !=None:
            jsonstring = json.dump(value_dict,f)
    used_time = time.time()-start
    if used_time < 1:
        time.sleep(1-used_time)
    f.close()
        



if __name__ == '__main__':
    time_now = time.strftime("%Y-%m-%d-%H-%M",time.localtime())
    p_save_url = "urls-"+time_now+".csv"
    p_save_data = "data-"+time_now+".csv"
    temp_name = "urls-2017-02-09-21-43.csv"
    #make_url_list(save_name)
    clawling(temp_name,"save_file")
