# -*- coding: utf-8 -*-
'''
@author: Yalei Meng
@contact: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@DateTime: Created on 2018/5/3，at 19:13
@desc:使用基于信息内容的算法来计算词语相似度。参考文献：
【1】彭琦, 朱新华, 陈意山,等. 基于信息内容的词林词语相似度计算[J]. 计算机应用研究, 2018(2):400-404.
'''
import math


class CilinSimilarity(object):
    """    基于哈工大同义词词林扩展版计算语义相似度    """

    def __init__(self):
        """
        'code_word' 以编码为key，单词list为value的dict，一个编码有多个单词
        'word_code' 以单词为key，编码为value的dict，一个单词可能有多个编码
        'vocab' 所有不重复的单词，便于统计词汇总数。
        'mydict' 每个大中小类编码对应的下位节点数量。
        """
        self.code_word = {}
        self.word_code = {}
        self.vocab = set()
        self.file = './cilin/V3/new_cilin.txt'
        self.mydict = {}
        self.read_cilin()

    def read_cilin(self):
        """
        读入同义词词林，编码为key，词群为value，保存在self.code_word
        单词为key，编码群为value，保存在self.word_code
        所有单词保存在self.vocab
        """
        head = set()
        with open(self.file, 'r', encoding='gbk') as f:
            for line in f.readlines():
                res = line.split()
                code = res[0]  # 词义编码
                words = res[1:]  # 同组的多个词
                self.vocab.update(words)  # 一组词更新到词汇表中
                self.code_word[code] = words  # 字典，目前键是词义编码，值是一组单词。

                for w in words:
                    if w in self.word_code.keys():  # 最终目的：键是单词本身，值是词义编码。
                        self.word_code[w].append(code)  # 如果单词已经在，就把当前编码增加到字典中
                    else:
                        self.word_code[w] = [code]  # 反之，则在字典中添加该项。
                # 第一次遍历，得到大中小类的代码。
                if len(code) < 6:
                    continue
                fathers = [code[:1], code[:2], code[:4], code[:5], code[:7]]
                head.update(fathers)
            fatherlist = sorted(list(head))

        with open(self.file, 'r', encoding='gbk') as f:
            # 第二次遍历：得到大中小类的数量。更新到字典mydict里面。
            for ele in fatherlist:
                self.mydict[ele] = 0
            for line in f.readlines():
                res = line.split()
                code = res[0]  # 词义编码
                words = res[1:]  # 同组的多个词
                if len(code) > 5 and code[:5] in self.mydict.keys():
                    self.mydict[code[:7]] += len(words)
                    self.mydict[code[:5]] += len(words)
                if len(code) > 4 and code[:4] in self.mydict.keys():
                    self.mydict[code[:4]] += len(words)
                if len(code) > 2 and code[:2] in self.mydict.keys():
                    self.mydict[code[:2]] += len(words)
                if len(code) > 1 and code[:1] in self.mydict.keys():
                    self.mydict[code[:1]] += len(words)

    def get_common_str(self, c1, c2):
        """        获取两个字符的公共部分，注意有些层是2位数字        """
        res = ''
        for i, j in zip(c1, c2):
            if i == j:
                res += i
            else:
                break
        if 3 == len(res) or 6 == len(res):
            res = res[:-1]
        return res

    def Info_Content(self, concept):
        if concept == '':
            return 0
        total =0
        for ele in self.mydict.keys():
            if len(ele)==1:
                total += self.mydict[ele]
        FenMu = math.log(total,2)
        #print('总结点数',total,FenMu)
        hypo = 1
        if concept in self.mydict.keys():
            hypo += self.mydict[concept]
        info = math.log(hypo, 2) / FenMu
        # print(concept, '下位节点数：', hypo,'信息内容：',1-info)
        return 1 - info

    def sim_by_IC(self, c1, c2):
        # 找到公共字符串
        LCS = self.get_common_str(c1, c2)
        distance = self.Info_Content(LCS) - (self.Info_Content(c1) + self.Info_Content(c2)) / 2
        return distance + 1

    def sim2018(self, w1, w2):
        """    按照论文彭琦, 朱新华, 陈意山,等. 基于信息内容的词林词语相似度计算[J]. 计算机应用研究, 2018(2):400-404.计算相似度  """
        for word in [w1, w2]:
            if word not in self.vocab:
                print(word, '未被词林词林收录！')
                return 0  # 如果有一个词不在词林中，则相似度为0
        # 获取两个词的编码列表
        code1 = self.word_code[w1]
        code2 = self.word_code[w2]
        simlist = []
        for c1 in code1:  # 选取相似度最大值
            for c2 in code2:
                cur_sim = self.sim_by_IC(c1, c2)
                simlist.append(cur_sim)
        aver = sum(simlist) / len(simlist)
        # print(sorted(simlist,reverse=True))
        if len(simlist) < 2:
            return simlist[0]
        if max(simlist) > 0.7:
            return max(simlist)
        elif aver > 0.2:
            return  (sum(simlist) - max(simlist)) / (len(simlist) - 1)
        else:
            return min(simlist)