#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import re
import codecs
import math
import jieba

# 测试文本
text = '''
自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
所以它与语言学的研究有着密切的联系，但又有重要的区别。
自然语言处理并不是一般地研究自然语言，
而在于研制能有效地实现自然语言通信的计算机系统，
特别是其中的软件系统。因而它是计算机科学的一部分。
'''


class BM25(object):
    '''
    计算BM25的类
    '''

    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum([len(doc) + 0.0 for doc in docs]) / self.D
        self.docs = docs
        # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.f = []
        # 存储每个词及出现了该词的文档数量
        self.df = {}
        # 存储每个词的idf值
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                # 存储每个文档中每个词的出现次数
                tmp[word] = tmp.get(word, 0) + 1
            self.f.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D - v + 0.5) - math.log(v + 0.5)

    def sim(self, doc, index):
        '''
        根据算法计算BM25
        :param doc:
        :param index:
        :return:
        '''
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            # TF = ((k + 1) * tf) / (k * (1.0 - b + b * L) + tf)
            score += (self.idf[word] * self.f[index][word] * (self.k1 + 1)
                      / (self.f[index][word] + self.k1 * (1 - self.b + self.b * d
                                                          / self.avgdl)))
        return score

    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores


def filter_stop(words):
    '''
    过滤停用词表中的词
    :param words:
    :return:
    '''
    stop = set()
    fr = codecs.open('stopwords.txt', 'r', 'utf-8')
    for word in fr:
        stop.add(word.strip())
    fr.close()
    re_zh = re.compile('([\u4E00-\u9FA5]+)')
    return list(filter(lambda x: x not in stop, words))


def get_sentences(doc):
    '''
    对输入文本进行预处理，将其拆分为多个doc格式
    :param doc:
    :return:
    '''
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[，。？！；]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


if __name__ == '__main__':
    sents = get_sentences(text)
    print(sents)
    doc = []
    for sent in sents:
        words = list(jieba.cut(sent))
        words = filter_stop(words)
        doc.append(words)
    print(doc)
    s = BM25(doc)
    print(s.f)
    print(s.idf)
    print(s.simall(['自然语言', '计算机科学', '领域', '人工智能', '领域']))
