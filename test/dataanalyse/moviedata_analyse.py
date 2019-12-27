"""
本程序实现对movies文件夹中，影评人数据的统计分析功能
"""
import pandas as pd

pd.options.display.max_rows=10  #设置可显示的数量

unames=['user_id', 'gender', 'age', 'occupation', 'zip']
users=pd.read_table('movies/users.dat',sep="::",header=None,names=unames,
                    engine='python')
#pd.read_table方法的结果是DataFrame格式
#pd.read_table方法需要加上engine='python'，否则会报警告
#sep="::"表示以内容中出现::符号时，前后内容进行分割

rnames=['user_id', 'movie_id', 'rating', 'timestamp']
ratings=pd.read_table('movies/ratings.dat',sep='::',header=None,names=rnames,
                      engine='python')

mnames=['movie_id', 'title', 'genres']
movies=pd.read_table('movies/movies.dat',sep='::',header=None,names=mnames,
                     engine='python')

data=pd.merge(pd.merge(users,ratings),movies)

mean_ratings_by_gender=data.pivot_table('rating',index='title',columns='gender',aggfunc='mean')
#pivot_table实现对所有title的rating值，按照gender类型，显示每个title中不同gender的平均rating
print(mean_ratings_by_gender[:10])
'''
gender                                    F         M
title                                                
$1,000,000 Duck (1971)             3.375000  2.761905
'Night Mother (1986)               3.388889  3.352941
'Til There Was You (1997)          2.675676  2.733333
'burbs, The (1989)                 2.793478  2.962085
...And Justice for All (1979)      3.828571  3.689024
1-900 (1994)                       2.000000  3.000000
10 Things I Hate About You (1999)  3.646552  3.311966
101 Dalmatians (1961)              3.791444  3.500000
101 Dalmatians (1996)              3.240000  2.911215
12 Angry Men (1957)                4.184397  4.328421
'''

ratings_by_title=data.groupby('title').size()
#size()实现对每个title进行计数
print(ratings_by_title[:10])
'''
title
$1,000,000 Duck (1971)                37
'Night Mother (1986)                  70
'Til There Was You (1997)             52
'burbs, The (1989)                   303
...And Justice for All (1979)        199
1-900 (1994)                           2
10 Things I Hate About You (1999)    700
101 Dalmatians (1961)                565
101 Dalmatians (1996)                364
12 Angry Men (1957)                  616
'''

active_titles=ratings_by_title.index[ratings_by_title>=250]
#生成ratings_by_title>=250的索引项
print(active_titles[:10])
'''
Index([''burbs, The (1989)', '10 Things I Hate About You (1999)',
       '101 Dalmatians (1961)', '101 Dalmatians (1996)', '12 Angry Men (1957)',
       '13th Warrior, The (1999)', '2 Days in the Valley (1996)',
       '20,000 Leagues Under the Sea (1954)', '2001: A Space Odyssey (1968)',
       '2010 (1984)'],
      dtype='object', name='title')
'''

mean_ratings=mean_ratings_by_gender.loc[active_titles]
#取出mean_ratings中和active_titles项一致的项
print(mean_ratings[:10])
'''
gender                                      F         M
title                                                  
'burbs, The (1989)                   2.793478  2.962085
10 Things I Hate About You (1999)    3.646552  3.311966
101 Dalmatians (1961)                3.791444  3.500000
101 Dalmatians (1996)                3.240000  2.911215
12 Angry Men (1957)                  4.184397  4.328421
13th Warrior, The (1999)             3.112000  3.168000
2 Days in the Valley (1996)          3.488889  3.244813
20,000 Leagues Under the Sea (1954)  3.670103  3.709205
2001: A Space Odyssey (1968)         3.825581  4.129738
2010 (1984)                          3.446809  3.413712
'''
top_female_ratings=mean_ratings.sort_values(by='F',ascending=False)
#sort_values实现排序，by='F'表示按照F列进行排序，ascending=False表示从大到小
print(top_female_ratings[:10])
'''
gender                                                     F         M
title                                                                 
Close Shave, A (1995)                               4.644444  4.473795
Wrong Trousers, The (1993)                          4.588235  4.478261
Sunset Blvd. (a.k.a. Sunset Boulevard) (1950)       4.572650  4.464589
Wallace & Gromit: The Best of Aardman Animation...  4.563107  4.385075
Schindler's List (1993)                             4.562602  4.491415
Shawshank Redemption, The (1994)                    4.539075  4.560625
Grand Day Out, A (1992)                             4.537879  4.293255
To Kill a Mockingbird (1962)                        4.536667  4.372611
Creature Comforts (1990)                            4.513889  4.272277
Usual Suspects, The (1995)                          4.513317  4.518248
'''

std=data.groupby('title')['rating'].std()
#std()实现对同一title的所有rating项计算方差
std=std.loc[active_titles]
print(std.sort_values(ascending=False)[:10])
'''
title
Dumb & Dumber (1994)                     1.321333
Blair Witch Project, The (1999)          1.316368
Natural Born Killers (1994)              1.307198
Tank Girl (1995)                         1.277695
Rocky Horror Picture Show, The (1975)    1.260177
Eyes Wide Shut (1999)                    1.259624
Evita (1996)                             1.253631
Billy Madison (1995)                     1.249970
Fear and Loathing in Las Vegas (1998)    1.246408
Bicentennial Man (1999)                  1.245533
Name: rating, dtype: float64
'''