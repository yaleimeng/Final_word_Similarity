#!/usr/bin/env python3
#*- coding: utf-8*-
#
# Copyright (C) 2016 ashengtx <linls@whu.edu.cn>
# under MIT License

import math


class CilinSimilarity(object):
    """
    基于哈工大同义词词林扩展版计算语义相似度
    """

    def __init__(self):
        """
        'code_word' 以编码为key，单词list为value的dict，一个编码有多个单词
        'word_code' 以单词为key，编码为value的dict，一个单词可能有多个编码
        'vocab' 所有的单词
        'N' N为单词总数，包括重复的词
        """
        self.a = 0.65
        self.b = 0.8
        self.c = 0.9
        self.d = 0.96
        self.e = 0.5
        self.f = 0.1
        self.degree = 180
        self.code_word = {}
        self.word_code = {}
        self.vocab = set()
        self.N = 0
        self.read_cilin()

    def read_cilin(self):
        """
        读入同义词词林，编码为key，词群为value，保存在self.code_word
        单词为key，编码为value，保存在self.word_code
        所有单词保存在self.vocab
        """
        with open('./cilin.txt', 'r', encoding='gbk') as f:
            for line in f.readlines():
                res = line.split()
                code = res[0]
                words = res[1:]
                self.vocab.update(words)
                self.code_word[code] = words
                self.N += len(words)
                for w in words:
                    if w in self.word_code.keys():
                        self.word_code[w].append(code)
                    else:
                        self.word_code[w] = [code]

    def get_common_str(self, c1, c2):
        """
        获取两个字符的公共部分
        """
        res = ''
        for i, j in zip(c1, c2):
            if i == j:
                res += i
            else:
                break
        if 3 == len(res) or 6 == len(res):
            res = res[0:-1]
        return res

    def get_layer(self, common_str):
        """
        根据common_str返回两个编码所在的层数。
        如果没有共同的str，则位于第一层，用0表示；
        如果第1个字符相同，则位于第二层，用1表示；
        这里第一层用0表示。
        """
        length = len(common_str)
        table = {1: 1, 2: 2, 4: 3, 5: 4, 7: 5}
        if length in table.keys():
            return table[length]
        return 0

    def code_layer(sefl, c):
        """
        将编码按层次结构化
        Aa01A01=
        第三层和第五层是两个数字表示；
        第一、二、四层分别是一个字母；
        最后一个字符用来区分所有字符相同的情况。
        """
        return [c[0], c[1], c[2:4], c[4], c[5:7], c[7]]

    def get_k(self, c1, c2):
        """
        返回两个编码对应分支的距离，相邻距离为1
        """
        if c1[0] != c2[0]:
            return abs(ord(c1[0]) ord(c2[0]))
        elif c1[1] != c2[1]:
            return abs(ord(c1[1]) ord(c2[1]))
        elif c1[2] != c2[2]:
            return abs(int(c1[2]) int(c2[2]))
        elif c1[3] != c2[3]:
            return abs(ord(c1[3]) ord(c2[3]))
        else:
            return abs(int(c1[4]) int(c2[4]))

    def get_n(self, common_str):
        """
        计算所在分支层的分支数
        即计算分支的父节点总共有多少个子节点
        两个编码的common_str决定了它们共同处于哪一层
        例如，它们的common_str为前两层，则它们共同处于第三层，则我们统计前两层为common_str的第三层编码个数就好了
        """
        if 0 == len(common_str):
            return 0
        siblings = set()
        layer = self.get_layer(common_str)
        for c in self.code_word.keys():
            if c.startswith(common_str):
                clayer = self.code_layer(c)
                siblings.add(clayer[layer])
        return len(siblings)

    # sim2016 begin ====================================
    def sim2016(self, w1, w2):
        """
        根据以下论文提出的改进方法计算：
        《基于知网与词林的词语语义相似度计算》，朱新华，马润聪， 孙柳，陈宏朝（ 广西师范大学 计算机科学与信息工程学院，广西 桂林541004）
        """
        # 如果有一个词不在词林中，则相似度为0
        if w1 not in self.vocab or w2 not in self.vocab:
            return 0

        sim_max = 0
        # 获取两个词的编码
        code1 = self.word_code[w1]
        code2 = self.word_code[w2]

        for c1 in code1:
            for c2 in code2:
                cur_sim = self.sim2016_by_code(c1, c2)
                # print(c1, c2, cur_sim)
                if cur_sim > sim_max:
                    sim_max = cur_sim
        return sim_max

    def sim2016_by_code(self, c1, c2):
        """
        根据编码计算相似度
        """

        # 先把code的层级信息提取出来
        clayer1 = self.code_layer(c1)
        clayer2 = self.code_layer(c2)

        common_str = self.get_common_str(c1, c2)
        # print('common_str: ', common_str)
        length = len(common_str)

        # 如果有一个编码以'@'结尾，那么表示自我封闭，这个编码中只有一个词，直接返回f
        if c1.endswith('@') or c2.endswith('@') or 0 == length:
            return self.f

        cur_sim = 0
        if 7 <= length:
            # 如果前面七个字符相同，则第八个字符也相同，要么同为'='，要么同为'#''
            if c1.endswith('=') and c2.endswith('='):
                cur_sim = 1
            elif c1.endswith('#') and c2.endswith('#'):
                cur_sim = self.e
        else:
            # 从这里开始要改，这之前都一样
            k = self.get_k(clayer1, clayer2)
            n = self.get_n(common_str)
            d = self.dist2016(common_str)
            e = math.sqrt(self.epow(-1 * k / (2 * n)))
            cur_sim = (1.05 0.05 * d) * e

        return cur_sim

    def dist2016(self, common_str):
        """
        计算两个编码的距离
        """
        w1, w2, w3, w4, = 0.5, 1, 2.5, 2.5
        weights = [w1, w2, w3, w4]

        layer = self.get_layer(common_str)

        try:
            if 0 == layer:
                return 18
            else:
                return 2 * sum(weights[0:4 layer + 1])
        except Exception as e:
            print('dist2016 errer, 共有的层数不能大于5')

    def epow(self, x):
        """        e^x        """
        return pow(math.e, x)
    # sim2016 end ====================================
