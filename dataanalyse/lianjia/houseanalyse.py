# -*- coding: utf-8 -*-
# 根据链家数据来源，对二手房信息进行统计

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
#对数据进行预处理
names=['id','total_price', 'unit_price', 'roomtype', 'height', 'direction', 'decorate', 'area', 'age'
       , 'garden', 'district', 'house_id']
data=pd.read_csv('data/lianjiadata.csv',names=names)
#删除第一列id，改变列的顺序
data=data.drop(['id'],axis=1)[['house_id','district', 'garden','unit_price', 'area','total_price', 'roomtype',
                               'height', 'direction', 'decorate', 'age']]
#删除重复值
data=data.drop_duplicates(['house_id'])
#输出干净后的数据至lianjiadata.csv文件中
data.to_csv('data/lianjiadata.csv')
'''

data=pd.read_csv('data/lianjiadata.csv')

'''group=data.groupby('district',as_index=False).unit_price.mean()
group=group.sort_values(by='unit_price',ascending=False)'''
group=data['district'].value_counts()
dic={'district':group.index,'size':group.values}
df=pd.DataFrame(dic)
sns.set()
sns.barplot(x='district',y='size',data=df)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()

'''plt.figure(figsize=(12,8)) #设置画布大小
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
'''