# -*- coding: utf-8 -*-
#下载CSDN关于人工智能的前20条文章内容#
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver=webdriver.Chrome()
url='https://so.csdn.net/so/search/s.do?p=1&q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&t=blog&domain=&o=&s=&u=&l=&f=&rbg=0'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/63.0.3239.132 Safari/537.36'}
driver.get(url)
time.sleep(3)
bs=BeautifulSoup(driver.page_source,'lxml')
docs=bs.findAll('dl',{'class':'search-list J_search'})
for doc in docs:
    url_doc=doc.a.attrs['href']
    res_doc = requests.get(url_doc, headers)
    con_doc = res_doc.content.decode()
    bs = BeautifulSoup(con_doc, 'lxml')
    title_doc = bs.find('h1', {'class': 'title-article'})
    word = bs.find('div', {'class':'htmledit_views'})
    if word is None:
        continue
    if title_doc is None:
        continue
    else:
        with open('text/%s.txt' % title_doc.get_text(), 'w', encoding='utf-8') as f:
            f.write(word.get_text())
    time.sleep(2)