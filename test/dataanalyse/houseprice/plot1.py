# -*- coding: utf-8 -*-
# 根据安居客数据来源，对二手房信息进行统计

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/anjuke.csv')
get_region = lambda x: x.split('-')[0]
address = data['Region'].apply(get_region)
data['District'] = address
data['Unit_price'] = data['Price'] / data['Size']

plt.figure(figsize=(12,8)) #设置画布大小
grid=plt.GridSpec(2,3)  #划分画布，这样可以调节每个子图的大小

#绘制北京各行政区房价排名
fig1=plt.subplot(grid[0,0:3])
datagroup1 = data.groupby(['District'], as_index=False)
unit_price_mean=datagroup1.Unit_price.mean().sort_values(by='Unit_price',ascending=False)
sns.barplot(x='District',y='Unit_price',data=unit_price_mean)
plt.suptitle('北京各行政区房价排名')

#绘制总价排前列小区中，各个行政区的拥有量
datagroup2 = data.groupby(['District','Garden'], as_index=False)
price_mean = datagroup2.Price.mean()
price_mean = price_mean.sort_values(by='Price', ascending=False)
max_data1 = price_mean[:10]
max_data2 = price_mean[:50]
max_data3 = price_mean[:100]
sns.set()
fig2=plt.subplot(grid[1,0])
sns.countplot(x='District', data=max_data1).set_title('总价排名前10小区各行政区占有量')
fig3=plt.subplot(grid[1,1])
sns.countplot(x='District', data=max_data2).set_title('总价排名前50小区各行政区占有量')
fig4=plt.subplot(grid[1,2])
sns.countplot(x='District', data=max_data3).set_title('总价排名前100小区各行政区占有量')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()


