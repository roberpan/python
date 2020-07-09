# -*- coding: utf-8 -*-
# 用Python展示Excel中20个常用操作

import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

df=pd.read_excel('data/excel_pandas/示例数据.xlsx')

#data=pd.DataFrame(np.random.randint(2,5,size=(10,2)))  #可以用np.random.randint中的size方法生成随机整数矩阵
data=pd.DataFrame(np.random.rand(10,2))  #np.random.rand()生成0-1之间满足均匀分布的10*2矩阵
#data.to_excel('测试数据.xlsx') #数据保存

#print(df[df['薪资水平']>5000])

#数据划分
bins=[0,10000,max(df['薪资水平'])]
labels=['low','high']
df['new_col']=pd.cut(df['薪资水平'],bins=bins,labels=labels)
#print(df)

#print(max(df['薪资水平'])) #max(df['薪资水平'])是返回df['薪资水平']列的最大值
#print(df['薪资水平'].max)  #df['薪资水平'].max是返回df['薪资水平']每一行的最大值

#df=df.sort_values(by='薪资水平',ascending=False)
#print(df)

#数据去重
df.drop_duplicates(['创建时间'],inplace=True)    #inplace=True表示在原df上进行操作
#print(df)

#修改df['创建时间']列的格式
df['创建时间']=df['创建时间'].dt.strftime('%Y-%m-%d')
#print(df)

#print(df.columns)  #df.columns格式类似list，可以进行索引操作，可以传入列表参数，更改列的顺序
#new_col=df.columns[[0,2,1,3,4,5,6]]
#print(df[new_col])

df['new']=df['地址'] + df['岗位']   #合并两列内容
#print(df)

#print(df['技能要求'].str.split(',',expand=True))    #df['技能要求'].str经过str转换后，可以用str内置的一些方法进行字符串处理

#print(df.groupby('学历').mean())

#print(len(df[df['薪资水平']>10000]))

#print(df['薪资水平'].describe())

#df['薪资水平'].hist()   #绘制直方图
#plt.show()

#print(df.sample(20))    #数据抽样

#pivot_table，透视表，可以按照自己设定的索引index，并提供值，会生成相应的分析汇总信息
#pivot_table(data, values=None, index=None, columns=None,aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All')
#pivot_table有四个最重要的参数index、values、columns、aggfunc
#index就是层次字段，要通过透视表获取什么信息就按照相应的顺序设置字段
#values可以对需要的计算数据进行筛选
#aggfunc参数可以设置我们对数据聚合时进行的函数操作,默认aggfunc='mean',多运算可以写成aggfunc=[np.sum,np.mean]
#columns类似Index可以设置列层次字段，它不是一个必要参数，作为一种分割数据的可选方式。
#print(pd.pivot_table(df,index=["工作经验","学历"],values=["薪资水平"]))

print(df.head())
print(df.tail())