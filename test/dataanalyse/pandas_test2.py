import  numpy as np
import pandas as pd


df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                   'key2' : ['one', 'two', 'one', 'two', 'one'],
                   'data1' : np.random.randn(5),
                   'data2' : np.random.randn(5)})

print(df)

group1=df['data1'].groupby([df['key1'],df['key2']])
print(group1.mean())