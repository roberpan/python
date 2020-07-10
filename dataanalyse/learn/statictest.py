# -*- coding: utf-8 -*-
# 基础统计学的Python实现

import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from scipy import stats

'''
几个常见统计项练习
'''
#df=pd.read_excel('data/600000.SH.xls')
#data=df['收盘价(元)']
#print(df['收盘价(元)'].describe())

#用hist画直方图
#plt.hist(data,bins=50,color='g',density=True)
#plt.show()

#偏度和峰度,偏度有负偏，左偏，可以看出数据偏向
#利用skew方法计算偏度，是负偏，左偏。
#print(data.skew())
#利用kurt计算峰度,表征概率密度分布曲线在平均值处峰值高低的特征数,反映了峰部的尖度
#print(data.kurt())

'''
假设检验和区间估计:
某公司研制出一种新的安眠药，要求其平均睡眠时间为23.8h。
为了检验安眠药是否达到要求，收集到一组使用新安眠药的睡眠时间（单位：h）为：26.7,22,24.1,21,27.2,25,23.4。
试问：从这组数据能否说明新安眠药达到疗效（假定睡眠时间服从正态分布，显著性水平为0.05）
'''
data = pd.DataFrame([26.7,22,24.1,21,27.2,25,23.4])
print(data.describe())
# 设定原假设H0：新安眠药平均睡眠时间是23.8h，也就是平均值u=23.8
# 备择假设H1：新安眠药平均睡眠时间不是23.8h，也就是平均值u≠23.8
# 用统计模块stats计算P值,样本数小于30，采用t检验，假设是总体符合正态分布
# t检验主要用于样本含量较小（例如n < 30），总体标准差σ未知的正态分布
