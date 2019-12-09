import pandas as pd
import numpy as np

index=pd.Index(data=["Tom", "Bob", "Mary", "James", "Andy", "Alice"],name='name')
data = {
    "age": [18, 30, 35, 18, 22, 30],
    "city": ["Bei Jing ", "Shang Hai ", "Guang Zhou", "Shen Zhen", "Zhe Jiang", "Su Zhou"],
    "sex": ["male", "male", "female", "male", "male", "female"],
    "income": [3000, 8000, 8000, 4000, 6000, 7000]
}
user_df=pd.DataFrame(data=data,index=index)
print(user_df)
'''
       age        city     sex  income
name                                  
Tom     18   Bei Jing     male    3000
Bob     30  Shang Hai     male    8000
Mary    35  Guang Zhou  female    8000
James   18   Shen Zhen    male    4000
Andy    22   Zhe Jiang    male    6000
Alice   30     Su Zhou  female    7000
'''
print('\n')

gp1=user_df.groupby(['sex'])    #按照sex类型进行分组
print(gp1)
#是一个对象<pandas.core.groupby.groupby.DataFrameGroupBy object at 0x000001F9D4F624E0>,不能直接输出内容
'''
对象的内部结构应该类似于字典，key-value格式，有两个键：按照sex类型分类后的male和female，每一个键有对应的值，
值的类型为DataFrame，有四个索引和值
'''
print(gp1['income'])
#也是一个对象<pandas.core.groupby.groupby.SeriesGroupBy object at 0x000001F5498E8748>,不能直接输出内容
print('\n')

for name,group in gp1:  #通过for循环输出内容，输出方式类似字典
    print("type: {}".format(name))
    print("{}".format(group))
    print("----------------")
'''
type: female
       age        city     sex  income
name                                  
Mary    35  Guang Zhou  female    8000
Alice   30     Su Zhou  female    7000
-------------
type: male
       age        city   sex  income
name                                
Tom     18   Bei Jing   male    3000
Bob     30  Shang Hai   male    8000
James   18   Shen Zhen  male    4000
Andy    22   Zhe Jiang  male    6000
-------------
'''
print('\n')

print(gp1.get_group('male'))    #通过get_group方法获取分类后的一类
'''
       age        city   sex  income
name                                
Tom     18   Bei Jing   male    3000
Bob     30  Shang Hai   male    8000
James   18   Shen Zhen  male    4000
Andy    22   Zhe Jiang  male    6000
'''

max_age=gp1['age'].agg(max)     #通过agg(max)方法，每一类中，按照age索引，求得age索引中的最大值
print(max_age)
'''
sex
female    35
male      30
Name: age, dtype: int64
'''
print('\n')

len=user_df.groupby(['sex','age'],as_index=False).agg(len)
#添加as_index=False，使限定的键与列索引在同一行，通过agg(len)方法，求得按照['sex','age']进行分类后，每一类中的值个数
print(len)
'''
      sex  age  city  income
0  female   30     1       1
1  female   35     1       1
2    male   18     2       2    
3    male   22     1       1
4    male   30     1       1
'''
#以上结果可看出，除['sex','age']为['male','18']的人有两个（Tom，James）外，其他如['female','30']等类都只对应一个人
print('\n')

income_cal=gp1['income'].agg([np.mean,np.max])
print(income_cal)
'''
        mean  amax
sex               
female  7500  8000
male    5250  8000
'''

age_income_cal=gp1.agg({'age':np.mean,'income':np.sum})
print(age_income_cal)
'''
         age  income
sex                 
female  32.5   15000
male    22.0   21000
'''

def f(ser,num=2):
    return ser.nlargest(num).tolist()
print(gp1['income'].apply(f))
'''
female    [8000, 7000]
male      [8000, 6000]
'''