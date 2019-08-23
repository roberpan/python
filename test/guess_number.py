from random import randint
num=randint(5,10)
i=0
while True:
    guess = input("input your guess:")
    i+=1
    if int(guess)==num:
        print("Great!you have guessed {:d} times".format(i))
        break
    else:
        print("please guess again!")