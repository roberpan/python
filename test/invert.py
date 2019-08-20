# -*- coding: utf-8 -*
#查找五位和六位逆序数，满足各位数字和为n
def number_sum(x):
    sum=0
    s=str(x)
    for i in s:
        sum+=int(i)
    return sum
def invert(x):
    s=str(x)
    return s==s[::-1]
def func(n):
    for i in range(10000,100000):
        if number_sum(i)==int(n):
            if invert(i):
                print(i)
        i+=1
n = input("n=")
func(n)

