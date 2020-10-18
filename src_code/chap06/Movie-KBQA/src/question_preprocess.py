#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import re


def text_processing(text):
    '''
    对用户输入的问题文本进行清理
    :param text:
    :return:
    '''
    text = text.replace(' ', '')
    clean_text = clean_punctuation(text)
    # 过滤非中文字符
    pattern = re.compile("[^\u4e00-\u9fa5]")
    clean_text = re.sub(pattern, '', clean_text)
    # print(clean_text)
    return clean_text


def clean_punctuation(text):
    '''
    清理标点符号
    :param text:
    :return:
    '''
    # 清理中文标点符号
    cn_punctuation = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
    cn_re_punctuation = "[{}]+".format(cn_punctuation)
    text = re.sub(cn_re_punctuation, "", text)
    # 清理英文标点符号
    en_punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    en_re_punctuation2 = "[{}]+".format(en_punctuation)
    text = re.sub(en_re_punctuation2, "", text)
    return text


if __name__ == '__main__':
    # test
    user_input = '你好，请问电影卧虎藏龙的评分是多少？'
    text_processing(user_input)
