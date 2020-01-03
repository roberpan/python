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
group_by_year=data.groupby('Year',as_index=False)
mean=group_by_year.Unit_price.mean()
mean=mean[mean['Year']>2000]
sns.barplot(x='Year',y='Unit_price',data=mean)
plt.show()
