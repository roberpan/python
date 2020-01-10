# -*- coding: utf-8 -*
#下载壁纸#
from bs4 import BeautifulSoup
import requests
import re

def downpic(url,filename):
    picurl = 'http://desk.zol.com.cn'+url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url=picurl, headers=headers)
    content = response.content.decode('gbk')
    soup=BeautifulSoup(content,features='lxml')
    img=soup.find('img',id='bigImg')
    nexturl = soup.find('a', id='pageNext').attrs['href']
    src = img.attrs['src']
    response = requests.get(url=src, headers=headers)
    contents = response.content
    name = re.sub("\D", "", picurl) #正则法提取数字
    with open('image/%s/%s.jpg'%(filename,name), 'wb') as f:
        f.write(contents)
    if str(nexturl)!='javascript:;':
        downpic(nexturl,filename)

downpic('/bizhi/7287_90150_2.html','daxiong')
