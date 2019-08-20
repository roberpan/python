import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time,datetime
import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dbnames=['USO','UNG']
dbname=dbnames[1]
def connectDB():
    db = pymysql.connect(host='localhost', user='root', password='pan19900901', port=3306, db='spiders')
    return db

def get_url():
    db=connectDB()
    cursor=db.cursor()
    sql='select UNIX_TIMESTAMP(date) from {} order by id DESC limit 1'.format(dbname)
    cursor.execute(sql)
    stimestamp=cursor.fetchone()[0]*1000+1
    ltimestamp=int(time.time()*1000)
    url='https://xueqiu.com/stock/forchartk/stocklist.json?symbol={0}&period=1day&type=before&begin={1}' \
        '&end={2}&_={2}'.format(dbname,stimestamp,ltimestamp)
    return url

def get_data(url):
    url_ini='https://xueqiu.com/'
    driver=webdriver.Chrome()
    driver.get(url_ini)
    time.sleep(2)
    driver.get(url)
    content=driver.page_source
    soup=BeautifulSoup(content,'lxml')
    data=soup.pre.get_text()
    time_list = []
    value_list = []
    dics=json.loads(data)['chartlist']
    for dic in dics:
        timestamp=dic['timestamp']/1000
        times=datetime.datetime.fromtimestamp(timestamp)
        time_list.append(times)
        value_list.append(dic['close'])
    if len(time_list)!=0:
        return [time_list,value_list]
    else:
        print('The database has latest data')
        draw()
        exit()

def writeSql(url):
    data=get_data(url)
    timedata=data[0]
    valuedata=data[1]
    length=len(timedata)
    db=connectDB()
    cursor=db.cursor()
    sql='insert into {}(date,closeprice) values(%s,%s)'.format(dbname)
    try:
        for i in range(0,length):
            cursor.execute(sql,(timedata[i],valuedata[i]))
            db.commit()
        print('success')
    except:
        db.rollback()
        print('failed')
    db.close()

def readSql(date1,date2):
    datelist = []
    pricelist = []
    db=connectDB()
    cursor=db.cursor()
    sql="select * from {} where date between '{}' and '{}'".format(dbname,date1,date2)
    cursor.execute(sql)
    row=cursor.fetchone()
    while row:
        datelist.append(row[1])
        pricelist.append(row[2])
        row=cursor.fetchone()
    return [datelist,pricelist]

def draw():
    fig = plt.figure()
    for i in range(1,5):
        j=i+2015
        syear=str(j)+'-01-01'
        lyear=str(j)+'-12-31'
        list=readSql(syear,lyear)
        xs = list[0]
        ys = list[1]
        ax = fig.add_subplot(4, 1, i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 设置时间标签显示格式
        plt.xticks(pd.date_range(xs[0], xs[-1], freq='M'))
        ax.plot(xs, ys)
    plt.show()

#url=get_url()
#writeSql(url)
draw()