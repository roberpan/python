# -*- coding: utf-8 -*-
# 爬取链家二手房数据

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

start=time.time()
def get_urls(n):
    urllist=[]
    for i in range(n):
        url='https://bj.lianjia.com/ershoufang/pg'+str(i+1)
        urllist.append(url)
    return urllist

def get_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url=url, headers=headers)   #获取网页编码数据
    content = response.content.decode() #将数据解码
    soup = BeautifulSoup(content, features='lxml')  #用lxml方式解析
    infos = soup.find_all('div', {'class': 'info clear'})   #找到div标签的，class值为info clear的元素
    result = {}
    # 设置DataFrame的列名，为后续添加字典数据做准备，不设置列名，字典无法直接添加
    df=pd.DataFrame(columns=('id','total_price','unit_price','roomtype','height','direction','decorate','area','age'
                             ,'garden','district','id'))
    for info in infos:
        url=info.find('a').get('href')  #用get()方法获取<a>标签中的href属性，get方法可实现对标签中特定属性的获取
        doc=requests.get(url=url,headers=headers)
        decontent=doc.content.decode()
        soups=BeautifulSoup(decontent,features='lxml')
        #获取房屋名、总价和单价
        #用select方法找出括号中对应的类型名，括号中用.+单词来表示class类型名
        result['total_price']=soups.select('.total')[0].text+'万'
        result['unit_price']=soups.select('.unitPriceValue')[0].text
        #获取房屋信息，如房型、层高、朝向、装修情况、面积、楼龄
        result['roomtype']=soups.select('.mainInfo')[0].text
        result['height']=soups.select('.subInfo')[0].text
        result['direction']=soups.select('.mainInfo')[1].text
        result['decorate']=soups.select('.subInfo')[1].text
        result['area']=soups.select('.mainInfo')[2].text
        result['age']=re.sub("\D","",soups.select('.subInfo')[2].text)
        #获取房源所在小区、地区、环线等信息
        result['garden']=soups.select('.info')[0].text
        result['district']=soups.select('.info a')[0].text
        #获取房源编号
        result['id']=re.sub("\D","",soups.select('.houseRecord')[0].text)   #通过正则方式把字符串中的数字提取出来
        # 用append方法向DataFrame中添加字典数据，注意在未设置DataFrame列名的情况下不能直接添加字典数据，会报错
        df=df.append(result,ignore_index=True)
    return df

def write_data(urls):
    dflist=[]
    for url in urls:
        dflist.append(get_info(url))    #生成由DataFrame组成的列表
    result=pd.concat(dflist)    #用concat方法将列表中的DataFrame元素组合起来成为一个大DataFrame
    result=result.reset_index(drop=True)
    result.to_csv('content.csv')  #将DataFrame数据写入CSV文件中

urllist=get_urls(100)
write_data(urllist)
print('success')
end=time.time()
print('time cost:',end-start)