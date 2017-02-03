# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import csv
import pandas
import time
from time import sleep

def process_article(url):
     data = requests.get(url)
     content = data.content
     soup = BeautifulSoup(content,"lxml")
     title = soup.select(".article_header_title")[0].string
     source = soup.select(".article_header_lead_by")[0].string
     articles =soup.select("div.article.gtm-click > p")
     for paragraph in articles:
         if paragraph.string !=None:
             pass
         else:
             a =paragraph.get_text()
             print(a)
     paragraphs = [paragraph.string if paragraph.string !=None else paragraph.get_text() for paragraph in articles]
     return {
         "title":title,\
         "source":source,\
         "paragraphs":paragraphs\
     }
anpan = process_article("https://gunosy.com/articles/RFSxD")
print(anpan)