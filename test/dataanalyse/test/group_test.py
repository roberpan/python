'''
groupby 分组练习
'''
import pandas as pd
import numpy as np

df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                   'key2' : ['one', 'two', 'one', 'two', 'one'],
                   'data1' : np.arange(5),
                   'data2' : np.arange(1,6)})
gpkey=df.groupby(['key1','key2'])['data1']  #取出按照['key1','key2']进行分类聚合后的data1列值
mean=gpkey.agg(np.mean) #.agg(np.mean)实现计算平均数，也可写成.mean()。此外.agg(len)实现计算各分组元素数
'''
result:
key1  key2
a     one     2
      two     1
b     one     2
      two     3
'''
mean.unstack()   #unstack()实现转置，将第二个分类参数key2从列转置为行，使得展示更清晰
'''
result:
key2  one  two
key1          
a       2    1
b       2    3
'''
gp=df.groupby(['key1']).mean()    #结果中没有key2列,因为df['key2']不是数值数据，不能计算平均数，自动被排除
'''
         data1     data2
key1                    
a     1.666667  2.666667
b     2.500000  3.500000
'''

#for key,group in df.groupby(['key1']):   #迭代输出
    #print(key)
    #print(group)
'''
  key1 key2  data1  data2
0    a  one      0      1
1    a  two      1      2
4    a  one      4      5
b
  key1 key2  data1  data2
2    b  one      2      3
3    b  two      3      4
'''

people = pd.DataFrame(np.arange(25).reshape(5,5),
                      columns=['a', 'b', 'c', 'd', 'e'],
                      index=['Joe', 'Steve', 'Wes', 'Jimma', 'Travis'])
key_list = ['one', 'one', 'one', 'two', 'two']
#print(people.groupby([len, key_list]).min())
#传入key_list数组，其意义是可将index值与key_list一一对应，如'Joe'->'one'，以此类推，最后还是按照len（姓名字母数），进行分组
# 其用处在于它能够根据轴索引的一个级别进行聚合

columns=pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],[1, 3, 5, 1, 3]],
                                    names=['city', 'tenor'])
#MultiIndex实现多维数组定义，此例中传入两个数组参数，['US', 'US', 'US', 'JP', 'JP']和[1, 3, 5, 1, 3]]，以及names表示分类名
#按照names数组分为两级，第一级'city',第二级'tenor'
# 'city'级值为['US', 'US', 'US', 'JP', 'JP']进行聚合后的分组名，分别为'US'和'JP'
#'tenor'级值为第一级每个分组的值，'US'组的值为1, 3, 5；'JP'组的值为1, 3
hier_df=pd.DataFrame(np.arange(20).reshape(4,5),columns=columns)
#print(hier_df)
'''
city    US          JP    
tenor   1   3   5   1   3
0       0   1   2   3   4
1       5   6   7   8   9
2      10  11  12  13  14
3      15  16  17  18  19
'''
#print(hier_df.groupby(level='city',axis=1).count())
#显示按照'city'级的值（'US'和'JP'），按行计算每个值的数量
'''
city  JP  US
0      2   3
1      2   3
2      2   3
3      2   3
'''
#print(hier_df.groupby(level='tenor',axis=1).count())
#作为比较，显示按照'tenor'级的值（1, 3, 5），按行计算每个值的数量
'''
tenor  1  3  5
0      2  2  1
1      2  2  1
2      2  2  1
3      2  2  1
'''