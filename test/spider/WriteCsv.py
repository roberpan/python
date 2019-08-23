# -*- coding: utf-8 -*
#CSV文件写入，比较重要
import csv
with open('test.csv','w',encoding='GB2312',newline="") as file: #要加newline，否则会写一行空一行
    fieldnames=['id','name','age']
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id':'10001', 'name':'王伟','age':20})
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': 21})
    writer.writerow({'id': '10003', 'name': 'Jordan', 'age': 22})
    file.close()