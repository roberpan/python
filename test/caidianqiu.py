# -*- coding: utf-8 -*
#猜点球，人和电脑分别踢一轮
from random import choice
scoreman=0
scorecomputer=0
turn=0
direction=['left','center','right']
while turn<5:
    if turn%2==0:
        guess = input("your turn!kick the ball:")
        computer = choice(direction)
        if guess!=computer:
            print("you goal!")
            scoreman+=1
    elif turn%2==1:
        guess = input("your turn!catch the ball:")
        computer = choice(direction)
        if guess!=computer:
            print("computer goal!")
            scorecomputer+=1
    turn+=1
if scoreman>scorecomputer:
    print("you win!your score is {:d} and computer's score is{:d}".format(scoreman,scorecomputer))
elif scoreman<scorecomputer:
    print("computer win!your score is {:d} and computer's score is {:d}".format(scoreman,scorecomputer))
else:
    print("no one win!")