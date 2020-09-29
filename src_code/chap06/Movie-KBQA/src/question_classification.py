#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
from pandas import Series, DataFrame
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import jieba


class Question_classify():
    '''
    定义用于问题模板分类的类函数
    '''

    # 类的初始化
    def __init__(self):
        # 读取训练数据及标签信息
        self.train_x, self.train_y = self.read_train_data()
        # 训练分类模型
        self.model = self.train_model_NB()

    def read_train_data(self):
        '''
        获取训练数据
        :return:
        '''
        # 存储训练数据
        train_x = []
        # 存储类别信息
        train_y = []
        # 训练数据文件存储地址
        train_data_path = './../data/question/'
        # 读取训练数据文件
        file_list = getfilelist(train_data_path)
        # 遍历所有文件
        for fname in file_list:
            # 正则匹配文件名中的数字
            num = re.sub(r'\D', '', fname)
            # 若该文件名有数字，则读取该文件
            if str(num).strip() != '':
                # 将文件名中的数字作为分类标签信息
                label_num = int(num)
                # 读取文件内容
                with(open(fname, 'r', encoding='utf-8')) as fr:
                    data_list = fr.readlines()
                    for one_line in data_list:
                        # 对文本进行分词
                        word_list = list(jieba.cut(str(one_line).strip()))
                        # 将文本存储为训练数据
                        train_x.append(" ".join(word_list))
                        train_y.append(label_num)
        return train_x, train_y

    def train_model_NB(self):
        '''
        训练朴素贝叶斯分类器
        :return:
        '''
        # 获取训练数据
        X_train, y_train = self.train_x, self.train_y
        # 初始化TfidfVectorizer实例
        self.tv = TfidfVectorizer()
        # 通过TF-IDF对文本数据进行向量化处理
        train_data = self.tv.fit_transform(X_train).toarray()
        # 初始化贝叶斯分类器并设置参数alpha为0.01
        clf = MultinomialNB(alpha=0.01)
        # 训练模型
        clf.fit(train_data, y_train)
        return clf

    def predict(self, question):
        '''
        使用训练好的模型对文本进行预测
        :param question:
        :return:
        '''
        # 对输入文本分词
        question = [" ".join(list(jieba.cut(question)))]
        # 将文本转换为向量
        test_data = self.tv.transform(question).toarray()
        # 对文本向量进行预测
        y_predict = self.model.predict(test_data)[0]
        print("predict type:", y_predict)
        return y_predict


def getfilelist(root_path):
    '''
    获取该路径下全部文件的路径信息
    :param root_path:
    :return:
    '''
    # 存储文件路径信息
    file_path_list = []
    # 存储文件名信息
    file_name = []
    # 遍历文件目录
    walk = os.walk(root_path)
    for root, dirs, files in walk:
        for name in files:
            filepath = os.path.join(root, name)
            file_name.append(name)
            file_path_list.append(filepath)
    print('文件名信息：', file_name)
    print('文件路径信息：', file_path_list)
    return file_path_list


if __name__ == '__main__':
    qc = Question_classify()
    qc.predict("张学友的个人信息")
