# -*- coding: utf-8 -*-
# 练习量化分析

#先引入后面可能用到的包（package）
import pandas as pd
#talib实现证券技术指标获取
import talib as ta
#tushare实现股票数据获取
import tushare as ts
from pylab import mpl
import time

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
#查看包含的技术指标和数学运算函数
#print(ta.get_functions())
#print(ta.get_function_groups())

#基准收益序列，按照股价正常变化的收益
benchmark=[]
#策略收益序列，采取策略后的收益序列
strategyvalue=[]
stocks=['600030','600031','600383']
start='2020-04-01'

def close_value(stock_name,start_time):
    df=ts.get_k_data(stock_name,start='2020-01-01',ktype='30')
    df.index=pd.to_datetime(df.date)
    df=df.sort_index().loc[start_time:]
    return df.close

def macd_cal(close):
    macd=pd.DataFrame()
    macd['macd'], macd['macdsignal'], macd['macdhist'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd['diff']= macd['macd']-macd['macdsignal']

    macd.reset_index('date',inplace=True)
    return macd

def meantime_strategy(stock):

    close = close_value(stock, start)
    macd = macd_cal(close)
    if macd['diff'].iloc[-2]>0 and macd['diff'].iloc[-1]<0:
        print('{}卖空，时间:{}'.format(stock,macd['date'].iloc[-1]))
    if macd['diff'].iloc[-2] < 0 and macd['diff'].iloc[-1] > 0:
        print('{}买多，时间:{}'.format(stock,macd['date'].iloc[-1]))
    else:
        print('{}维持现状,时间:{},macd_diff_pre={},macd_diff_now={}'
                  .format(stock,macd['date'].iloc[-1],macd['diff'].iloc[-2],macd['diff'].iloc[-1]))
    time.sleep(1)

def history_strategy(stock):
    sum=0.0
    close = close_value(stock, start)
    macd = macd_cal(close)
    for i in range(1,len(macd)):
        if macd['diff'].iloc[i-1] > 0 and macd['diff'].iloc[i] < 0:
            print('卖空，时间:{}'.format(macd['date'].iloc[i]))
        if macd['diff'].iloc[i-1] < 0 and macd['diff'].iloc[i] > 0:
            print('买多，时间:{}'.format(macd['date'].iloc[i]))
        if macd['diff'].iloc[i]>0:
            sum=((close[i]-close[i-1])*100/close[i])+sum
#        if macd['diff'].iloc[i]<0:
#            sum=((close[i-1]-close[i])*100/close[i])+sum
    benchmark=(close[-1]-close[0])*100/close[0]
    print("benchmark income:",benchmark)
    print("strategy income:",sum)

if __name__=='__main__':
    while True:
        for stock in stocks:
            meantime_strategy(stock)
        time.sleep(1800)





