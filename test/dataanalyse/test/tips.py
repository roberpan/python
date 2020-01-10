'''
groupby 聚合练习
'''
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)  #显示所有列

df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                   'key2' : ['one', 'two', 'one', 'two', 'one'],
                   'data1' : np.arange(5),
                   'data2' : np.arange(1,6)})

gp1=df.groupby('key1')
'''
gp1内容：
a
  key1 key2  data1  data2
0    a  one      0      1
1    a  two      1      2
4    a  one      4      5
b
  key1 key2  data1  data2
2    b  one      2      3
3    b  two      3      4
'''
def minus(group):
    return group.max()-group.min()
gp1.data1.agg(minus)
'''
key1
a    4
b    1
'''
content=pd.read_csv('../data/tips.csv')
content['tip_pct']=content['tip']/content['total_bill']
grouped=content.groupby(['day', 'smoker'])
grouped_pct=grouped['tip_pct']
#print(grouped_pct.agg('mean'))  #计算grouped_pct（也即grouped的'tip_pct'列）的平均值（mean）
'''
day   smoker
Fri   No        0.151650
      Yes       0.174783
Sat   No        0.158048
      Yes       0.147906
Sun   No        0.160113
      Yes       0.187250
Thur  No        0.160298
      Yes       0.163863
'''
#print(grouped_pct.agg([('foo', 'mean'), ('bar', np.std)]))
#也可以传入一个列表，包括两个元组，每个元组第一个参数（'foo'和'bar'）表示group中的列名，第二个参数（'mean'和np.std）是计算方法
'''
                  foo       bar
day  smoker                    
Fri  No      0.151650  0.028123
     Yes     0.174783  0.051293
Sat  No      0.158048  0.039767
     Yes     0.147906  0.061375
Sun  No      0.160113  0.042347
     Yes     0.187250  0.154134
Thur No      0.160298  0.038774
     Yes     0.163863  0.039389
'''
functions = ['count', 'mean', 'max']    #可以应用于全部列的函数列表
result = grouped['tip_pct', 'total_bill'].agg(functions)    #对'tip_pct', 'total_bill'列用functions列表中的函数计算
'''
            tip_pct                     total_bill                  
              count      mean       max      count       mean    max
day  smoker                                                         
Fri  No           4  0.151650  0.187735          4  18.420000  22.75
     Yes         15  0.174783  0.263480         15  16.813333  40.17
Sat  No          45  0.158048  0.291990         45  19.661778  48.33
     Yes         42  0.147906  0.325733         42  21.276667  50.81
Sun  No          57  0.160113  0.252672         57  20.506667  48.17
     Yes         19  0.187250  0.710345         19  24.120000  45.35
Thur No          45  0.160298  0.266312         45  17.113111  41.19
     Yes         17  0.163863  0.241255         17  19.190588  43.11
'''

def top(group,n=5,column='tip_pct'):
    return group.sort_values(by=column,ascending=False)[:n]
top(content,n=6)
'''
     total_bill   tip smoker  day    time  size   tip_pct
172        7.25  5.15    Yes  Sun  Dinner     2  0.710345
178        9.60  4.00    Yes  Sun  Dinner     2  0.416667
67         3.07  1.00    Yes  Sat  Dinner     1  0.325733
232       11.61  3.39     No  Sat  Dinner     2  0.291990
183       23.17  6.50    Yes  Sun  Dinner     4  0.280535
109       14.31  4.00    Yes  Sat  Dinner     2  0.279525
'''

smkgroup=content.groupby('smoker')
smkgroup.apply(top) #按照smoker类型分组，并求出各分组中tip_pct排名前五的项，apply(fuc)实现对各分组都应用定义的函数fuc
'''
            total_bill   tip smoker   day    time  size   tip_pct
smoker                                                           
No     232       11.61  3.39     No   Sat  Dinner     2  0.291990
       149        7.51  2.00     No  Thur   Lunch     2  0.266312
       51        10.29  2.60     No   Sun  Dinner     2  0.252672
       185       20.69  5.00     No   Sun  Dinner     5  0.241663
       88        24.71  5.85     No  Thur   Lunch     2  0.236746
Yes    172        7.25  5.15    Yes   Sun  Dinner     2  0.710345
       178        9.60  4.00    Yes   Sun  Dinner     2  0.416667
       67         3.07  1.00    Yes   Sat  Dinner     1  0.325733
       183       23.17  6.50    Yes   Sun  Dinner     4  0.280535
       109       14.31  4.00    Yes   Sat  Dinner     2  0.279525
'''
smkgroup.apply(top,n=3, column='total_bill')  #可以在函数名后加可以传递给函数的参数
'''
            total_bill    tip smoker  day    time  size   tip_pct
smoker                                                           
No     212       48.33   9.00     No  Sat  Dinner     4  0.186220
       59        48.27   6.73     No  Sat  Dinner     4  0.139424
       156       48.17   5.00     No  Sun  Dinner     6  0.103799
Yes    170       50.81  10.00    Yes  Sat  Dinner     3  0.196812
       182       45.35   3.50    Yes  Sun  Dinner     3  0.077178
       102       44.30   2.50    Yes  Sat  Dinner     3  0.056433
'''

frame=pd.DataFrame({'data1':np.arange(10),
                    'data2':np.arange(5,15)})
quartiles=pd.cut(frame.data1,3) #分成三等分进行分组，显示各个元素处在哪个分组
'''
0    (-0.009, 3.0]
1    (-0.009, 3.0]
2    (-0.009, 3.0]
3    (-0.009, 3.0]
4       (3.0, 6.0]
5       (3.0, 6.0]
6       (3.0, 6.0]
7       (6.0, 9.0]
8       (6.0, 9.0]
9       (6.0, 9.0]
'''

s=frame['data1']
s[::2]=np.nan
'''
s:
0    NaN
1    1.0
2    NaN
3    3.0
4    NaN
5    5.0
6    NaN
7    7.0
8    NaN
9    9.0
'''
s1=s.fillna(s.mean())   #用s.mean(s中除去空值的平均值)填充空值
'''
0    5.0
1    1.0
2    5.0
3    3.0
4    5.0
5    5.0
6    5.0
7    7.0
8    5.0
9    9.0
'''

states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data=pd.Series(np.arange(8),index=states)
data[::2]=np.nan
'''
Ohio          NaN
New York      1.0
Vermont       NaN
Florida       3.0
Oregon        NaN
Nevada        5.0
California    NaN
Idaho         7.0
'''
gp=data.groupby(group_key)  #用列表group_key作为groupby分类参数，可以将列表中相同项对应的数据源分为一组
'''
East
Ohio        NaN
New York    1.0
Vermont     NaN
Florida     3.0
dtype: float64
West
Oregon        NaN
Nevada        5.0
California    NaN
Idaho         7.0
'''
gp.mean()
'''
East    2.0
West    6.0
'''
fill_mean=lambda g:g.fillna(g.mean())
gp.apply(fill_mean)
'''
Ohio          2.0
New York      1.0
Vermont       2.0
Florida       3.0
Oregon        6.0
Nevada        5.0
California    6.0
Idaho         7.0
'''
fill_values = {'East': 0.5, 'West': -1}
fill=lambda g:g.fillna(fill_values[g.name])    #groupby后各分组有一个默认自带的name参数，表示各分组名
gp.apply(fill)
'''
Ohio          0.5
New York      1.0
Vermont       0.5
Florida       3.0
Oregon       -1.0
Nevada        5.0
California   -1.0
Idaho         7.0
'''

df = pd.DataFrame({'category': ['a', 'a', 'a', 'a',
                                'b', 'b', 'b', 'b'],
                   'data': np.arange(8),
                   'weights':[0.1]*4+[0.3]*4})
'''
  category  data  weights
0        a     0      0.1
1        a     1      0.1
2        a     2      0.1
3        a     3      0.1
4        b     4      0.3
5        b     5      0.3
6        b     6      0.3
7        b     7      0.3
'''
group=df.groupby('category')
get_wavg=lambda g:np.average(g['data'],weights=g['weights'])    #求group各分组的加权平均数
group.apply(get_wavg)
'''
category
a    1.5
b    5.5
'''

'''
以下实现美股四只股票与标准普尔指数的相关性计算
'''
close_px = pd.read_csv('../data/stock_px_2.csv', parse_dates=True,
                       index_col=0)
spx_corr=lambda c:c.corrwith(c['SPX'])  #corrwith()实现与c['SPX']相关性计算
rets=close_px.pct_change().dropna()
get_year=lambda x:x.year
by_year=rets.groupby(get_year)  #groupby()也可以用函数名作为参数，将函数返回的结果作为groupby()的分组项
by_year.apply(spx_corr)
'''
          AAPL      MSFT       XOM  SPX
2003  0.541124  0.745174  0.661265  1.0
2004  0.374283  0.588531  0.557742  1.0
2005  0.467540  0.562374  0.631010  1.0
2006  0.428267  0.406126  0.518514  1.0
2007  0.508118  0.658770  0.786264  1.0
2008  0.681434  0.804626  0.828303  1.0
2009  0.707103  0.654902  0.797921  1.0
2010  0.710105  0.730118  0.839057  1.0
2011  0.691931  0.800996  0.859975  1.0
'''

table=content.pivot_table(index=['day', 'smoker'])
#pivot_table()透视表功能和grouped.agg(np.mean)一致，实现分组平均值计算
'''
                 size       tip   tip_pct  total_bill
day  smoker                                          
Fri  No      2.250000  2.812500  0.151650   18.420000
     Yes     2.066667  2.714000  0.174783   16.813333
Sat  No      2.555556  3.102889  0.158048   19.661778
     Yes     2.476190  2.875476  0.147906   21.276667
Sun  No      2.929825  3.167895  0.160113   20.506667
     Yes     2.578947  3.516842  0.187250   24.120000
Thur No      2.488889  2.673778  0.160298   17.113111
     Yes     2.352941  3.030000  0.163863   19.190588
'''
table1=content.pivot_table('tip_pct',index=['time','smoker'],columns='day',margins=True,aggfunc=len,fill_value=0.0)
#aggfunc=len实现分组大小计算，margins=True实现增加一列All显示aggfunc结果,默认情况是显示平均数计算,fill_value实现空值填充
'''
day            Fri  Sat  Sun  Thur    All
time   smoker                            
Dinner No        3   45   57     1  106.0
       Yes       9   42   19     0   70.0
Lunch  No        1    0    0    44   45.0
       Yes       6    0    0    17   23.0
All             19   87   76    62  244.0
'''

stat_crosstab=pd.crosstab(content.time,content.day,margins=True)
stat_pivottable=content.pivot_table('tip',index='time',columns='day',aggfunc=len,margins=True,fill_value=0)
#以上两行代码实现同样功能和结果，分别用crosstab()实现对数量的统计，也可用pivot_table实现
'''
result:
day     Fri  Sat  Sun  Thur  All
time                            
Dinner   12   87   76     1  176
Lunch     7    0    0    61   68
All      19   87   76    62  244
'''