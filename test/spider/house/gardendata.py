# -*- coding: utf-8 -*-
# 爬取链家二手房数据

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import math

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36'}

'''def get_gardenurls():
    districts = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping',
                 'daxing', 'yizhuangkaifaqu', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun',
                 'yanqing']
    urls=[]
    for s in districts:
        for i in range(0,30):
            url='https://bj.lianjia.com/xiaoqu/{}/pg{}'.format(s,i+1)
            urls.append(url)
    return urls

def get_gardens():
    urls = get_urls()
    gardens={}
    dflist=[]
    for url in urls:
        df = pd.DataFrame(columns=['id', 'name'])
        response=requests.get(url=url,headers=headers)
        content=response.content.decode()
        bs=BeautifulSoup(content,features='lxml')
        els=bs.find_all('li',{'class':'clear xiaoquListItem'})
        for el in els:
            gardens['id']=int(el.get('data-id'))
            gardens['name']=el.find('div',{'class':'title'}).a.string
            df=df.append(gardens,ignore_index=True)
        dflist.append(df)
    data=pd.concat(dflist)
    data = data.reset_index(drop=True)
    return data'''

def read_info():
    file='gardeninfo.csv'
    # 删除一列，用axis=1来表示列，默认其值为0，表示一行。Unnamed: 0列表示保存在CSV中的索引列，文件中此列没有列名
    df=pd.read_csv(file).drop(['Unnamed: 0'],axis=1)
    id=df['id']
    return id

def get_houseurls():
    id=read_info()
    urllist=[]
    for i in id:
        url='https://bj.lianjia.com/ershoufang/c{}/'.format(i)
        urllist.append(url)
    return urllist

def get_info(url):
    response = requests.get(url=url, headers=headers)
    content = response.content.decode()
    soup = BeautifulSoup(content, features='lxml')
    count=int(soup.select('.total.fl')[0].find('span').text)
    page=math.ceil(count/30)
    df = pd.DataFrame(columns=('id','district', 'garden', 'unit_price','area','total_price', 'roomtype', 'height',
                               'direction', 'decorate', 'age'))
    if page!=0:
        baseurl = url
        for i in range(page):
            url=baseurl+'pg{}/'.format(i+1)
            response = requests.get(url=url, headers=headers)
            content = response.content.decode()
            soup = BeautifulSoup(content, features='lxml')
            infos = soup.find_all('div', {'class': 'info clear'})
            result = {}
            for info in infos:
                houseurl=info.find('a').get('href')
                doc=requests.get(url=houseurl,headers=headers)
                decontent=doc.content.decode()
                soups=BeautifulSoup(decontent,features='lxml')
                # 获取房源所在小区、地区、环线等信息
                result['district'] = soups.select('.info a')[0].text
                result['garden'] = soups.select('.info')[0].text
                # 获取房源编号
                result['id'] = re.sub("\D", "", soups.select('.houseRecord')[0].text)  # 通过正则方式把字符串中的数字提取出来
                # 获取房屋名、总价和单价
                result['unit_price']=soups.select('.unitPriceValue')[0].text
                result['area'] = soups.select('.mainInfo')[2].text
                result['total_price']=soups.select('.total')[0].text+'万'
                #获取房屋信息，如房型、层高、朝向、装修情况、面积、楼龄
                result['roomtype']=soups.select('.mainInfo')[0].text
                result['height']=soups.select('.subInfo')[0].text
                result['direction']=soups.select('.mainInfo')[1].text
                result['decorate']=soups.select('.subInfo')[1].text
                result['age']=re.sub("\D","",soups.select('.subInfo')[2].text)
                df = df.append(result, ignore_index=True)
    return df

urls=get_houseurls()
dflist=[]
for url in urls:
    df=get_info(url)
    dflist.append(df)
alldata=pd.concat(dflist)
alldata=alldata.reset_index(drop=True)
alldata.to_csv('houseinfo_1.csv')
print('success')