import  numpy as np
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt


path='example.txt'
records=[json.loads(line) for line in open(path)]
time_zones=[rec['tz'] for rec in records if 'tz' in rec]

df=pd.DataFrame(records)
tz_full=df['tz'].fillna('Missing')  #使用fillna方法将自定义词汇'Missing'补充进不含'tz'索引的项
tz_full[tz_full == ''] = 'Unknown'  #对于tz_full索引为空的项补充内容为'Unknown'
tz_count=tz_full.value_counts() #使用value_counts()方法对Series类型中的值按项进行统计
#print(tz_count[:10])    #输出Series的前十个值，使用方法与列表一致

browser=pd.Series([a.split()[0] for a in df['a'].dropna()]) #使用dropna()方法去除NA值
browser_count=browser.value_counts()
#print(browser_count[:10])

os=np.where((df.a.dropna()).str.contains('Windows'),'Windows', 'Not Windows')
cdf=df[df.a.notnull()]
cdf=cdf.copy()
cdf['os']=os

by_tz_os=cdf.groupby(['tz','os'])
print(by_tz_os)
agg_counts=by_tz_os.size().unstack().fillna(0)
#print(agg_counts[:10])

indexer=agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer[-10:])

count_subset=count_subset.stack()
count_subset.name='total'
count_subset=count_subset.reset_index()

def norm_total(group):
    group['normed_total']=group.total/group.total.sum()
    return group

results=count_subset.groupby('tz').apply(norm_total)
sns.barplot(x='normed_total',y='tz',hue='os',data=results)
plt.show()
