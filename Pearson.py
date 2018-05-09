# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2018
@desc: 
@DateTime: Created on 2018/5/7, at 上午 09:51 by PyCharm '''
from math import sqrt

def multiply(a,b):
    #a,b两个列表的数据一一对应相乘之后求和
    sum_ab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sum_ab+=temp
    return sum_ab

def cal_pearson(x,y):
    n=len(x)
    #求x_list、y_list元素之和
    sum_x=sum(x)
    sum_y=sum(y)
    #求x_list、y_list元素乘积之和
    sum_xy=multiply(x,y)
    #求x_list、y_list的平方和
    sum_x2 = sum([pow(i,2) for i in x])
    sum_y2 = sum([pow(j,2) for j in y])
    molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
    #计算Pearson相关系数，molecular为分子，denominator为分母
    denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
    return molecular/denominator