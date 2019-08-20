import pymysql
from bs4 import BeautifulSoup
import json
import requests
import traceback
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time,datetime

def connectDB():
    db = pymysql.connect(host='localhost', user='root', password='pan19900901', port=3306, db='spiders')
    return db

def get_url(sdate,days):    #sdate is start date,days is number of days
    url='https://dsx.weather.com/wxd/v2/PastObsAvg/zh_CN/{0}/{1}/USNY0996:1:US?' \
        'api=7bb1c920-7027-4289-9c96-ae5e263980bc&format=json'.format(sdate,days)
    print(url)
    return url

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'}
    response=requests.get(url=url,headers=headers)
    content=response.content
    soup=BeautifulSoup(content,features='lxml')
    data=json.loads(soup.get_text())
    len_data=len(data)
    date=[]
    highTemp_today=[]
    lowTemp_today=[]
    history_high=[]
    history_low=[]
    avg_high=[]
    avg_low=[]
    for i in range(0,len_data):
        data_today_temp=data[i]['Temperatures']
        data_history_temp=data[i]['Climatology']
        date.append(datetime.datetime.strptime(str(data_today_temp['highTmISO']).split('T')[0],'%Y-%m-%d'))
        highTemp_today.append(float(data_today_temp['highC']))
        lowTemp_today.append(float(data_today_temp['lowC']))
        history_high.append(float(data_history_temp['recordHighC']))
        history_low.append(float(data_history_temp['recordLowC']))
        avg_high.append(float(data_history_temp['avgHiC']))
        avg_low.append(float(data_history_temp['avgLowC']))
    return date,highTemp_today,lowTemp_today,history_high,history_low,avg_high,avg_low

def write_mysql(url):
    date, highTemp_today, lowTemp_today, history_high, history_low, avg_high, avg_low=get_data(url)
    db=connectDB()
    cursor=db.cursor()
    try:
        for i in range(0,len(date)):
            sql='insert into weather(date,place,high_temp,low_temp,history_high,history_low,avg_high,avg_low) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(date[i],'New York',highTemp_today[i],lowTemp_today[i],history_high[i],history_low[i], avg_high[i], avg_low[i]))
            db.commit()
        print('success')
    except:
        traceback.print_exc()
        db.rollback()
        print('failed')
    db.close()

def readSql(sdate,ldate):
    datelist = []
    highTemp_today = []
    lowTemp_today = []
    history_high = []
    history_low = []
    avg_high = []
    avg_low = []
    db=connectDB()
    cursor=db.cursor()
    sql="select * from weather where date between '{}' and '{}' order by date".format(sdate,ldate)
    cursor.execute(sql)
    row=cursor.fetchone()
    while row:
        datelist.append(row[1])
        highTemp_today.append(row[3])
        lowTemp_today.append(row[4])
        history_high.append(row[5])
        history_low.append(row[6])
        avg_high.append(row[7])
        avg_low.append(row[8])
        row=cursor.fetchone()
    return [datelist,highTemp_today,lowTemp_today,history_high,history_low,avg_high,avg_low]

def draw():
    list1=readSql('2017-01-01','2017-12-18')
    list2 = readSql('2018-01-01', '2018-12-18')
    plt.title('Weather Analysis')
    xs_axix = list1[0]
    highTemp_today1 = list1[1]
    lowTemp_today1=list1[2]
    avg_high1 = list1[5]
    avg_low1 = list1[6]
    highTemp_today2 = list2[1]
    lowTemp_today2 = list2[2]

    #plt.plot(xs_axix, highTemp_today1, color='red', label='highTemp_2017')
    plt.plot(xs_axix, lowTemp_today1, color='green', label='lowTemp_2017')
    #plt.plot(xs_axix, avg_high1, color='purple', label='avg_high_2017')
    plt.plot(xs_axix, avg_low1, color='blue', label='avg_low_2017')
    #plt.plot(xs_axix, highTemp_today2, color='skyblue', label='highTemp_2018')
    plt.plot(xs_axix, lowTemp_today2, color='red', label='lowTemp_2018')

    plt.legend()
    plt.xlabel('date')
    plt.ylabel('℃')
    plt.show()

sdate='2019-04-20'
days=10
url=get_url(sdate,days)
print(url)