#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import jieba


def Jaccrad(model, reference):
    '''
    计算jaccard系数
    :param model: 候选句子
    :param reference: 源句子
    :return:
    '''
    # 对句子分词 默认精准模式
    terms_reference = jieba.cut(reference)
    terms_model = jieba.cut(model)
    # 去重，如果不需要就改为list
    grams_reference = set(terms_reference)
    grams_model = set(terms_model)
    # 两个句子的并集
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    # 两个句子的交集
    fenmu = len(grams_model) + len(grams_reference) - temp
    # 两个句子Jaccard距离
    jaccard_coefficient = float(temp / fenmu)
    return jaccard_coefficient


if __name__ =='__main__':
    a = "香农在信息论中提出的信息熵定义为自信息的期望"
    b = "信息熵作为自信息的期望"
    jaccard_coefficient = Jaccrad(a, b)
    print(jaccard_coefficient)