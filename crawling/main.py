# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import csv
import pandas
import time
from time import sleep

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

#get_all_url_to_scrape
f = open(save_url,'w')
for i in range(1,8):
    urls =[]
    for j in range(1):
        address = "https://gunosy.com/categories/{i}?page={j}".format(i=i,j=j)
        data = request.get(address)
        content = data.content
        soup = BeautifulSoup(content,"lxml")
        samples  =soup.select(".list_title")
        for sample in samples:
            sample = sample.find("a")
            f.write(sample["href"]+" "+i)
f.close()

filename = save_url
df = pandas.read_csv("filename",header=None)


