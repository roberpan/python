# -*- coding: utf-8 -*-
# 练习量化分析

#先引入后面可能用到的包（package）
import pandas as pd
#talib实现证券技术指标获取
import talib as ta
import numpy as np
#tushare实现股票数据获取
import tushare as ts
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
#查看包含的技术指标和数学运算函数
#print(ta.get_functions())
#print(ta.get_function_groups())
ta_fun=ta.get_function_groups()
ta_fun.keys()

#基准收益序列，按照股价正常变化的收益
benchmark=[]
#策略收益序列，采取策略后的收益序列
strategyvalue=[]
df=ts.get_k_data('600100',start='2020-06-01',ktype='60')
df.index=pd.to_datetime(df.date)
df=df.sort_index().loc['2020-05-01':]
close=pd.DataFrame(df.close)
'''
for i in range(len(types)):
    df_ma[types[i]]=ta.MA(df.close,timeperiod=5,matype=i)
'''
macd=pd.DataFrame()
macd['macd'], macd['macdsignal'], macd['macdhist'] = ta.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
macd['diff']= macd['macd']-macd['macdsignal']
difflist=macd['diff'].tolist()
macd.reset_index('date',inplace=True)
print(macd)

for i in range(len(macd)-1):
    if macd['diff'].iloc[i]>0 and macd['diff'].iloc[i+1]<0:
        print('卖空，时间:{}'.format(macd['date'].iloc[i+1]))
    if macd['diff'].iloc[i] < 0 and macd['diff'].iloc[i+1] > 0:
        print('买多，时间:{}'.format(macd['date'].iloc[i+1]))
    if difflist[i]>0:
        benchmark.append((df.close[i+1]-df.close[i])*100/df.close[i])
        valuelist.append(df.close[i+1]-df.close[i])
    if difflist[i]<0:
        sum=(df.close[i]-df.close[i+1])/df.close[i]+sum
        valuelist.append(df.close[i]-df.close[i+1])

print(valuelist)
print(sum)
print((df.close[-1]-df.close[0])/df.close[0])

print(close)
plt.plot(close)
plt.show()
'''plt.figure(figsize=(12,8)) #设置画布大小
grid=plt.GridSpec(2,1)  #划分画布，这样可以调节每个子图的大小
fig1=plt.subplot(grid[0,0])
plt.plot(df.close)
fig2=plt.subplot(grid[1,0])
plt.plot(macd['macd'])
plt.plot(macd['macdsignal'])
plt.show()
'''
'''df_ma.loc['2020-06-01':].plot(figsize=(16,6))
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数各种类型移动平均线',fontsize=15)
plt.xlabel('')
plt.show()
'''



