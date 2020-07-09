# -*- coding: utf-8 -*-
# 根据链家数据来源，对二手房信息进行统计

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling

#pd.set_option('display.max_columns',None)

'''对爬虫后的原始数据进行简单处理'''
'''
names=['id','total_price', 'unit_price', 'roomtype', 'height', 'direction', 'decorate', 'area', 'age'
       , 'garden', 'district', 'house_id']
data=pd.read_csv('data/lianjia_rawdata.csv',names=names)    #读取原始数据，并加上names数组表头
data=data.drop(['id'],axis=1)[['house_id','district', 'garden','unit_price', 'area','total_price', 'roomtype',
                               'height', 'direction', 'decorate', 'age']]   #删除第一列id，改变列的顺序
data.to_csv('data/lianjiadata.csv')     #输出调整后的数据至lianjiadata.csv中
'''

'''对数据进行预处理，去除重复值'''
data=pd.read_csv('data/lianjiadata.csv')
data=data.drop_duplicates(['house_id'])     #删除重复值

'''将数据集的总价都转换为纯数字，方便分析'''
get_value = lambda x: x.split('万')[0]
price=data['total_price'].apply(get_value)
data['total_price']=price

'''用pandas_profiling生成分析报告'''
profile=data.profile_report(title='Lianjia Dataset')
profile.to_file(output_file='lianjia_report.html')


'''
#显示每个行政区房源数量，并按顺序排名
group=data['district'].value_counts() #value_counts()实现数据统计并按从高到低顺序排序
dic={'district':group.index,'size':group.values}
df=pd.DataFrame(dic)
sns.set()
sns.barplot(x='district',y='size',data=df)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()
'''

'''
plt.figure(figsize=(12,8)) #设置画布大小
grid=plt.GridSpec(2,3)  #划分画布，这样可以调节每个子图的大小

#绘制北京各行政区房价排名
fig1=plt.subplot(grid[0,0:3])
datagroup1 = data.groupby(['district'], as_index=False)
unit_price_mean=datagroup1.unit_price.mean().sort_values(by='unit_price',ascending=False)
sns.barplot(x='district',y='unit_price',data=unit_price_mean)
plt.suptitle('北京各行政区房价排名')


#绘制总价排前列小区中，各个行政区的拥有量
datagroup = data.groupby(['district','garden'], as_index=False)
price_mean = datagroup['total_price'].mean()
print(price_mean)

price_mean = price_mean.sort_values(by='total_price', ascending=False)
max_data1 = price_mean[:10]
max_data2 = price_mean[:50]
max_data3 = price_mean[:100]
print(max_data1)
sns.set()
#fig=plt.subplot()
sns.countplot(x='district', data=max_data1).set_title('总价排名前10小区各行政区占有量')
fig3=plt.subplot(grid[1,1])
sns.countplot(x='District', data=max_data2).set_title('总价排名前50小区各行政区占有量')
fig4=plt.subplot(grid[1,2])
sns.countplot(x='District', data=max_data3).set_title('总价排名前100小区各行政区占有量')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()
'''