#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import re
from bert_serving.client import BertClient
import os
import numpy as np
import csv
import Levenshtein


def getBestAnswer(input_ques):
    '''
    根据用户输入问题，系统给予用户相应回答
    :param input_ques:用户输入问题信息
    :return:
    '''

    # 根据编辑距离计算问题库中是否存在相同问题
    is_exist_same_ques, sys_reply, QA_que, QA_ans = getSameQuestionByEditDistance(input_ques)
    if is_exist_same_ques:
        return sys_reply, QA_que, QA_ans
    else:
        # 保险问答数据中问题的向量表示数据地址
        insurance_data_vector_path = './../preprocess_data/insurance_ques_vector.npy'
        # 导入问答数据中问题的向量表述数据
        insurance_ques_vector = np.load(insurance_data_vector_path)
        # 实例化BERT向量转换工具
        bc = BertClient()
        # 将用户输入问题通过BERT转换为向量表示
        input_vec = bc.encode(["".join(input_ques.split())])
        # 查找问答库中语义最相似的前10个问题
        topk = 10
        # 计算输入问题与问答数据中全部问题的相似度
        score = np.sum(input_vec * insurance_ques_vector, axis=1) / np.linalg.norm(insurance_ques_vector, axis=1)
        # 对相似计算结果排序并返回前10条问题
        topk_idx = np.argsort(score)[::-1][:topk]
        # 根据找到的最相似问题的索引获取其相似问题及答案
        similaryQuestion, bestAns = getSimilaryQuestionByIndex(topk_idx[0] + 1)
        # 计算找到的语义最相似问题与用户输入问题的余弦相似度
        similar_val = cosine_similarity(input_vec[0], insurance_ques_vector[topk_idx[0]])
        # 用户输入问题与问答库中找到的相似问题的阈值设定
        similarity_question_consia_threshold = 0.9
        # 若用户输入问题与找到的最相似问题的相似度小于设定的阈值，则表示系统没有找到答案
        # 否则将找到的相似问题及答案返回给用户
        if similar_val < similarity_question_consia_threshold:
            sys_reply = '啊哦，小助手还没有掌握这方面的知识呢，我会将您的问题记录下来，并尽快找到专业的答案。'
            QA_que, QA_ans = '', ''
            return sys_reply, QA_que, QA_ans
        else:
            sys_reply = '小助手没有这个问题的答案呢，给您推荐以下相似问题及答案以供参考哦~\n'
            QA_que = '相似问题：' + similaryQuestion + '\n'
            QA_ans = '推荐答案：' + bestAns + '\n'
            QA_ans = clean_ans(QA_ans)
            return sys_reply, QA_que, QA_ans


def getSameQuestionByEditDistance(curr_ques):
    '''
    根据编辑距离计算问题库中相同问题，返回相似值及索引
    :param curr_ques:当前用户输入的问题
    :return:
    '''
    same_question_threshold = 0.98
    # 保险问答数据地址
    insurance_data_path = './../preprocess_data/insurance_data.csv'
    # 最大相似值
    max_similarity_val = 0
    # 最相似问题的索引值
    max_similarity_index = 0
    # 读取保险问答数据
    with open(insurance_data_path, 'r', encoding='utf-8') as csvfile:
        ques_ans = csv.reader(csvfile)
        # 当前比较的数据在问答数据中的索引值
        curr_idx = 0
        # 遍历计算用户输入问题与问答题库中全部问题的编辑距离相似度
        for curr in ques_ans:
            curr_idx += 1
            # 去除待比较计算问题文本中的标点符号
            curr_ques = replace_punctuation(curr_ques)
            csv_ques = replace_punctuation(curr[0])
            # 计算待比较的问题文本的编辑距离的相似度
            edit_distance_val = Levenshtein.ratio(csv_ques, curr_ques)
            # 若当前获取的相似度大于已知的最大相似度，则更新最大相似度为当前相似度的值，更新最相似问题的索引为当前索引
            if edit_distance_val > max_similarity_val:
                max_similarity_val = edit_distance_val
                max_similarity_index = curr_idx
    # 是否存在相同问题的标志位
    is_exist_same_ques = False
    # 系统回复信息
    sys_reply = ''
    # 找到的问题信息
    QA_que = ''
    # 找到的答案信息
    QA_ans = ''
    # 若查找到的最相似问题的最大相似度大于设置的阈值，则返回该问题及对应答案
    if max_similarity_val > same_question_threshold:
        similaryQuestion, bestAns = getSimilaryQuestionByIndex(max_similarity_index)
        # 答案信息清理
        QA_ans = clean_ans(bestAns)
        is_exist_same_ques = True
    return is_exist_same_ques, sys_reply, QA_que, QA_ans


def replace_punctuation(curr_string):
    '''
    清理无效标点符号
    :param curr_string:当前待处理字符串
    :return:
    '''
    # 通过正则表达式清理中文标点符号
    punctuation = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
    re_punctuation = "[{}]+".format(punctuation)
    curr_string = re.sub(re_punctuation, "", curr_string)
    # 通过正则表达式清理英文标点符号
    punctuation2 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    re_punctuation2 = "[{}]+".format(punctuation2)
    curr_string = re.sub(re_punctuation2, "", curr_string)
    return curr_string


def cosine_similarity(vector1, vector2):
    '''
    计算余弦相似度
    :param vector1:待比较向量1
    :param vector2:待比较向量2
    :return:
    '''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    # 根据余弦相似度计算公式计算两个向量的余弦相似度
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)), 2)


def getSimilaryQuestionByIndex(index):
    '''
    根据问答数据的问题索引获取其答案信息，返回问答数据中找到问题及答案信息
    :param index:
    :return:
    '''
    # 问答数据地址
    insurance_data_path = './../preprocess_data/insurance_data.csv'
    # 读取问答数据
    with open(insurance_data_path, 'r', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        idx = 0
        # 遍历问答数据
        for curr_data in read:
            idx += 1
            # 根据问题索引查找其答案信息
            if idx == index:
                curr_ques = curr_data[0]
                curr_ans = curr_data[1]
    return curr_ques, curr_ans


def clean_ans(str_ans):
    '''
    清理答案信息中的不合法字符
    :param str_ans:
    :return:
    '''
    # 清理空格及换行字符
    str_ans = str_ans.replace('\n', '').replace(' ', '')
    return str_ans


if __name__ == '__main__':
    testQ = ['天热了，很想去潜水，除了装备、教练以及费用外还要什么保险？',
             '本周末公司组织一次大型户外拓展活动，100人什么HUTS保险合适？',
             '太阳系有几个行星呢'
             ]
    for que in testQ:
        sys_reply, QA_que, QA_ans = getBestAnswer(que)
        print('当前用户输入问题为：', que)
        print('当前智能客服回复为：', sys_reply, QA_que, QA_ans)
        print('------------------------------------------------------')
