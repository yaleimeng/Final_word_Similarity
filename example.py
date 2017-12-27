# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2017
@desc:    混合采用词林和知网的相似度计算方法。得到更加符合人们感觉的相似度数值。
@DateTime: Created on 2017/12/28, at 18:28 by PyCharm
'''

from howNet import WordSimilarity
from cilin import CilinSimilarity




if __name__ == '__main__':
    cs = CilinSimilarity()  # 先使用词林进行计算
    w1, w2 = '起重机', '器械'
    print(w1, w2)
    print('2016年词林改进版相似度为：', cs.sim2016(w1, w2))
    # 判断词是否在词林中收录，只需要判断是否 in  cs.vocab即可。

    obj = WordSimilarity()  # 实例化一个相似度计算对象
    ci_sim = obj.calc(w1, w2)
    print(ci_sim)