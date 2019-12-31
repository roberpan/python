# -*- coding: utf-8 -*-
#本程序实现对1880-2010年间全美婴儿姓名的统计

import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.max_rows=10

'''
读取yob1880.txt文件，按照sex类型进行分组后，统计每个分组的总人数，存入count_by_sex中
'''
file=pd.read_csv('data/babynames/yob1880.txt', names=['name', 'sex', 'births'])
count_by_sex=file.groupby('sex')['births'].sum()

'''
读取1880至2011间所有文档，分为'name','sex','births'三列，以年度为首列，按照sex的不同值（F、M），
显示F和M的人口总数（aggfunc=sum），并新增一列prop，展示按照['year','sex']分组后每个分组所占人数比例
'''
years=range(1880,2011)
pieces=[]
columns=['name','sex','births']
for year in years:
    content=pd.read_csv('babynames/yob%d.txt'%year,names=columns)   #content类型为DataFrame
    content['year']=year
    pieces.append(content)
names=pd.concat(pieces,ignore_index=True)   #concat()默认按行将多个DataFrame组合到一起,ignore_index=True表示重新加序号
count_by_year=names.pivot_table('births',index='year',columns='sex',aggfunc=sum)
def add_grop(group):
    group['prop']=group.births/group.births.sum()
    return group
names=names.groupby(['year','sex']).apply(add_grop) #apply可实现对groupby后的各分组进行统一计算

'''
查看排名前1000位的名字人数占总人数比例
'''
def get_top1000(group):
    return group.sort_values(by='births',ascending=False)[:1000]    #sort_values()中用by表示按哪一列排序
names_top1000=names.groupby(['year','sex']).apply(get_top1000)  #取出names按照'year','sex'分组后名字数量最多的前1000个值
names_top1000.reset_index(inplace=True,drop=True)
boys=names_top1000[names_top1000.sex=='M']  #取出names_top1000中sex值为M的所有行
girls=names_top1000[names_top1000.sex=='F']
total_births=names_top1000.pivot_table('births',index='year',columns='name',aggfunc=sum)
'''
subset=total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True,figsize=(12,10),grid=False,title="Number of births per year")
plt.show()
'''
table=names_top1000.pivot_table('prop',index='year',columns='sex',aggfunc=sum)
#table.plot(title='Sum of table1000.prop by year and sex',yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

df=names[(names.sex=='M')&(names.year==2010)]
prop_cumsum=df.sort_values(by='prop',ascending=False).prop.cumsum()
index=prop_cumsum.values.searchsorted(0.5)   #searchsorted(0.5)可以返回值为0.5的序号

def half_index(group):
    prop_cumsum = group.sort_values(by='prop', ascending=False).prop.cumsum()
    return prop_cumsum.values.searchsorted(0.5)+1
indexlist=names_top1000.groupby(['year', 'sex']).apply(half_index).unstack('sex')
'''
indexlist.plot()
plt.show()
'''

get_last_letter=lambda x:x[-1]
last_letters=names.name.map(get_last_letter)
last_letters.name='last_letter'
last_letter_table=names.pivot_table('births',index=last_letters,columns=['sex', 'year'],aggfunc=sum)
subtable=last_letter_table.reindex(columns=[1910, 1960, 2010], level='year')

letter_prop=subtable/subtable.sum()
fig,axis=plt.subplots(2,1)
letter_prop['M'].plot(kind='bar',rot=0,ax=axis[0],title='Male')
letter_prop['F'].plot(kind='bar',rot=0,ax=axis[1],title='Female')
plt.show()