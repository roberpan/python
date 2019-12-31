# -*- coding: utf-8 -*-
# 根据安居客数据来源，对二手房信息进行统计

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
data = pd.read_csv('data/anjuke.csv')
get_region = lambda x: x.split('-')[0]
address = data['Region'].apply(get_region)
data['District'] = address
data['Unit_price'] = data['Price'] / data['Size']
datagroup = data.groupby(['District', 'Garden'], as_index=False)

price_mean = datagroup.Price.mean()
price_mean = price_mean.sort_values(by='Price', ascending=False)
max_data1 = price_mean[:10]
max_data2 = price_mean[:50]
max_data3 = price_mean[:100]

sns.set()
fig, axes = plt.subplots(1, 3)
sns.countplot(x='District', data=max_data1, ax=axes[0]).set_title('top 10')
sns.countplot(x='District', data=max_data2, ax=axes[1]).set_title('top 50')
sns.countplot(x='District', data=max_data3, ax=axes[2]).set_title('top 100')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.suptitle('总价排名前列小区各行政区占有量')
plt.show()
