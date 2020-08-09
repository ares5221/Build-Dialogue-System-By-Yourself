#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np
from collections import defaultdict


class TFIDF(object):
    '''
    用于计算文档TF-IDF的类
    '''

    def __init__(self, corpus, word_sep=' ', smooth_value=0.01, scale=False):
        assert isinstance(corpus, list), 'Not support this type corpus.'
        self.corpus = corpus
        self.vob = defaultdict(int)
        self.word_sep = word_sep
        self.smooth_value = smooth_value
        self.doc_cnt = defaultdict(set)
        self.scale = scale

    def get_tf_idf(self):
        # 获取词表
        for i, line in enumerate(self.corpus):
            if isinstance(line, str):
                line = line.split(self.word_sep)
            for w in line:
                self.vob[f'{i}_{w}'] += 1
                self.doc_cnt[w].add(i)
        # 计算TF-IDF
        output = np.zeros((len(self.corpus), len(self.vob)))
        for i, line in enumerate(self.corpus):
            if isinstance(line, str):
                line = line.split(self.word_sep)
            tmp_size = len(line)
            for j, w in enumerate(self.vob.keys()):
                w_ = w.split('_')[1]
                if w_ in line:
                    output[i, j] = self.vob[w] / tmp_size * np.log(
                        (self.smooth_value + len(self.corpus)) / (self.smooth_value + len(self.doc_cnt[w_])) + 1)
        if self.scale:
            output = (output - output.mean(axis=1).reshape(len(self.corpus), -1)) / output.std(axis=1).reshape(
                len(self.corpus), -1)
        return output


if __name__ == '__main__':
    # 每个列表代表一个文档
    corpus = [['this', 'is', 'a', 'simple', 'tfidf', 'code', 'but', 'code', 'might', 'has', 'bugs'],
              ['python', 'is', 'a', 'code', 'language', 'not', 'human', 'language'],
              ['learning', 'python', 'make', 'things', 'simple', 'but', 'not', 'simple', 'enough']]
    result = TFIDF(corpus)
    print(result.get_tf_idf())
