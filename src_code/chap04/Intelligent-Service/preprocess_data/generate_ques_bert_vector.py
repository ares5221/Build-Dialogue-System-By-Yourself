#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np
from bert_serving.client import BertClient
import csv


def get_insurance_question():
    '''
    获取问答数据中的问题
    :return:
    '''
    # 保险问答数据存储地址
    source_dir = './insurance_data.csv'
    # 存储保险问答数据中的全部问题
    insurance_question = []
    # 读取保险问答数据中的问题字段信息
    with open(source_dir, 'r', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        for data in read:
            insurance_question.append(data[0])
    print('获取到', len(insurance_question), '条问题')
    return insurance_question


def bertconvert(insurance_question):
    '''
    通过BERT将问题转换为向量表示
    :param insurance_question:
    :return:
    '''
    question_list = []
    # 调用bert-as-service将字符串转换为向量表示
    bc = BertClient()
    for i in range(0, len(insurance_question)):
        curr_ques = insurance_question[i]
        # 清楚问题字符串中的空格
        curr_ques = "".join(curr_ques.split())
        question_list.append(curr_ques)
    # 将问题字符串转换为向量表示
    insurance_ques_vector = bc.encode(question_list)
    # 将向量表示的数据保存为npy格式
    np.save("insurance_ques_vector.npy", insurance_ques_vector)


if __name__ == '__main__':
    print('将保险数据中问答数据中的问题生成向量文件...')
    insurance_question = get_insurance_question()
    bertconvert(insurance_question)
    print('生成向量文件结束！')
