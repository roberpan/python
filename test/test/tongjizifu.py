# -*- coding: utf-8 -*
#统计输入文本中各个字符出现次数，并按照频度进行排序
text=input("input your text:")
key=[]
dict={}
for t in text:
    if t not in key:
        key.append(t)
        dict[t]=1
    else:
        dict[t]+=1
print(dict)
dict=sorted(dict.items(),key=lambda item:item[1])
print(dict)