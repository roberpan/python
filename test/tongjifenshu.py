# -*- coding: utf-8 -*
#统计文本文档中各人成绩和
results = []
with open('score.txt') as file:
    lines=file.readlines()
    print(lines)
    for line in lines:
        score=0
        seps=line.split()
        for sep in seps[1::]:
            score+=int(sep)
        result="{:s}的总分是{:d}分\n".format(seps[0],score)
        results.append(result)
with open('result.txt','w') as file:
    file.writelines(results)