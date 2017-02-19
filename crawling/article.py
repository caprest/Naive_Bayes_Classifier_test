# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import csv
import pandas
import time
from time import sleep

def process_article(row):
    url = row[0]
    label = row[1]
    print("GET "+url+" ...")
    data = requests.get(url)
    content = data.content
    soup = BeautifulSoup(content,"lxml")
    try:
        title = soup.select(".article_header_title")[0].string
        source = soup.select(".article_header_lead_by")[0].string
        articles =soup.select("div.article.gtm-click > p")
        for paragraph in articles:
            if paragraph.string !=None:
                pass
            else:
                a =paragraph.get_text()
        paragraphs = [paragraph.string if paragraph.string !=None else paragraph.get_text() for paragraph in articles]
        sentence = (" ").join(paragraphs).replace("\n", " ")
        return [title,source,sentence,label]
    except:
        print("Error Occurred at try to get "+row[0])
        return None
    
     

if __name__ == '__main__':
    print("Module Test")
    ret = process_article("https://gunosy.com/articles/RFSxD")
    
