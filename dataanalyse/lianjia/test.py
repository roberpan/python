# -*- coding: utf-8 -*-
# 根据链家数据来源，对二手房信息进行统计测试

import pandas as pd

names=['id','total_price', 'unit_price', 'roomtype', 'height', 'direction', 'decorate', 'area', 'age'
       , 'garden', 'district', 'house_id']
data=pd.read_csv('data/lianjiadata.csv',names=names,encoding = 'GB2312')
#删除第一列id，改变列的顺序
data=data.drop(['id'],axis=1)[['house_id','district', 'garden','unit_price', 'area','total_price', 'roomtype',
                               'height', 'direction', 'decorate', 'age']]
print(data)