# -*- coding: utf-8 -*
#猜大小，人和电脑分别轮流
from random import randint
import time
score1,score2=100,100
turn=1
g=['小','大']
while True:
    num1,num2,num3=randint(1,6),randint(1,6),randint(1,6)
    sum=num1+num2+num3
    if 3<=sum<=10:
        result='小'
    else:
        result='大'
    if turn%2==1:
        guess=input("轮到你了，你猜大还是小:")
        if guess in g and guess==result:
            score1*=2
            print("猜对了!你现在的分数是", score1)
        elif guess in g and guess!=result:
            print("你没猜对")
        print("你现在的分数是 {},电脑的分数是 {}".format(score1, score2))
    if turn % 2 == 0:
        print("轮到电脑了!电脑正在猜...")
        time.sleep(2)
        guess_c=g[randint(0,1)]
        if guess_c==result:
            score2 *= 2
            print("电脑猜对啦!电脑现在的分数是", score2)
        else:
            print("电脑没猜对.")
        print("你现在的分数是 {},电脑的分数是 {}".format(score1, score2))
    turn += 1