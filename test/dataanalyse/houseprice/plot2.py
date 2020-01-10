# -*- coding: utf-8 -*-
# 根据安居客数据来源，对二手房信息进行统计

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv('data/anjuke.csv')
get_region = lambda x: x.split('-')[0]
address = data['Region'].apply(get_region)
data['District'] = address
data['Unit_price'] = data['Price'] / data['Size']
gardengp=data.groupby(['Garden'],as_index=False)
gardenUnitMean=gardengp.Unit_price.mean()
middleunit=np.mean(gardenUnitMean.Unit_price)
gardenPriceMean=gardengp.Price.mean()
middleprice=np.mean(gardenPriceMean.Price)
print(middleunit)
print(middleunit)

fig=plt.figure()
ax1=fig.add_subplot(2,2,1)
sns.distplot(gardenUnitMean.Unit_price,bins=30,kde=True,color='b')
plt.title('各小区单价分布图')

ax2=fig.add_subplot(2,2,2)
sns.distplot(data['Unit_price'],bins=30,kde=True,color='r')
plt.title('各房源单价分布图')

ax3=fig.add_subplot(2,2,3)
sns.distplot(gardenPriceMean.Price,kde=True,color='g')
plt.title('各小区平均总价分布图')

ax4=fig.add_subplot(2,2,4)
sns.distplot(data['Price'],kde=True,color='y')
plt.title('各房源总价分布图')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()

