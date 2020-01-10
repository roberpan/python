# -*- coding:utf-8 -*
# 本程序主要用pandas对数据进行基本统计分析#
from test import dbConnect
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 可通过自定义起始和终止时间，将数据库数据写入pricelist、lowtemper、datelist三个列表中
def sqldata(sdate, ldate):
    datelist = []
    pricelist = []
    lowtemper = []
    db = dbConnect.connect()
    cursor = db.cursor()
    sql = "SELECT ung.date,ung.closeprice,weather.low_temp FROM ung INNER JOIN weather ON ung.date=weather.date where ung.date BETWEEN '{}' and '{}'".format(
        sdate, ldate)
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        datelist.append(row[0])
        pricelist.append(row[1])
        lowtemper.append(row[2])
        row = cursor.fetchone()
    return datelist, pricelist, lowtemper


# 绘制天然气价格和最低温的关系图
def draw(date, unglist, templist):
    fig = plt.figure()
    xs = date
    ys1 = unglist
    ys2 = templist
    plt.title('Compare ungprice with lowtemperature')
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 设置时间标签显示格式
    plt.xticks(pd.date_range(xs[0], xs[-1], freq='M'))
    ax.plot(xs, ys1)
    ax.plot(xs, ys2)
    plt.show()


# 计算UNG价格和气温相关系数，采用pearson算法
def correlation_coefficient(sdate, ldate):
    pricelist = sqldata(sdate, ldate)[1]
    lowtemper = sqldata(sdate, ldate)[2]
    data = pd.DataFrame([lowtemper, pricelist])
    s1 = data.loc[0]
    s2 = data.loc[1]
    correlation = s1.corr(s2, method='pearson')
    print(correlation)


# 设定要比较的起止时间
sdate = '2018-01-01'
ldate = '2018-12-31'

# 绘制天然气价格和最低温的关系图
list = sqldata(sdate, ldate)
draw(list[0], list[1], list[2])

# 计算全年UNG价格和气温相关系数

correlation_coefficient(sdate, ldate)
'''
以上结果为：-0.2628412788976146
对于pearson系数r：
若r>0，表明两个变量是正相关，即一个变量的值越大，另一个变量的值也会越大；
若r<0，表明两个变量是负相关，即一个变量的值越大另一个变量的值反而会越小。 
从以上结果可以得出：
（1）气温最低温和UNG价格呈现一定的负相关，即气温越低，UNG价格越高，符合推断
（2）气温最低温和UNG价格关联度似乎不大，猜想可能是因为UNG价格只在冬季才会有较大波动，才能体现与气温的负相关性，
     而在其他时间由于走势平稳，价格波动小，使其与气温的负相关度较小
为证明上述推断,对不同时期的UNG价格和最低温之间的关联度进行计算，间隔两个月进行计算
'''
correlation_coefficient('2018-01-01', '2018-03-01')
correlation_coefficient('2018-03-01', '2018-05-01')
correlation_coefficient('2018-05-01', '2018-07-01')
correlation_coefficient('2018-07-01', '2018-09-01')
correlation_coefficient('2018-09-01', '2018-11-01')
correlation_coefficient('2018-12-01', '2018-12-31')
'''
以上结果为：
-0.2256651138981243
0.23028507750467753
0.45907379036230844
0.08095159804297261
-0.6715912221718108
-0.44634601125958556
可以看出，18年UNG价格在9月至12月期间表现出较大的负相关性，相关系数达到-0.67，而在其他月份则表现不明显，甚至在3月至7月间还呈明显正相关，可利用这种特点采取投资策略
'''
