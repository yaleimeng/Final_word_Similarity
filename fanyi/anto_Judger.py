# -*- coding: utf-8 -*-
'''
Author: Yalei Meng  yaleimeng@sina.com
License: Created with VS Code, (C) Copyright 2022
Description: 读取反义词典（暂无十分完善的反义词典），判断是否反义词对。
Date: 2022-02-15 23:11:36
LastEditTime: 2022-02-16 08:54:06
FilePath: \Final_word_Similarity\fanyi\anto_Judger.py
'''


class AntonymJudger(object):    

    def __init__(self):
        """
        'code_word' 以编码为key，单词list为value的dict，一个编码有多个单词        
        """
        self.fanyi = {} 
        self.file = './fanyi/antonym.txt'       
        self.read_fan()

    def read_fan(self):
        """
        读入反义词库，
        单词为key，反义词为value， 保存在self.vocab
        """       
        with open(self.file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                res = line.strip().split('@')
                code = res[0]  # 原始词
                word = res[1]  # 反义词词

                if code in self.fanyi:
                    self.fanyi[code].append(word)  # 如果已存在，就添加到列表
                else:
                    self.fanyi[code] = [word,]  # 如果不存在，构造一个列表

    def is_anti_pair(self,w1,w2):
        if w1 in self.fanyi and w2 in self.fanyi[w1]:
            return True
        else:
            return False
