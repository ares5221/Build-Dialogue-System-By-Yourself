#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import jieba.posseg
import re


def jieba_pos_tagging(text):
    '''
    对文本进行词性标记
    :param text:
    :return:
    '''
    # 用户自定义词库路径
    user_dict_path = './../data/userdict3.txt'
    # 导入用户自定义词库
    jieba.load_userdict(user_dict_path)
    # 对文本进行词性分析
    text_pos_seg = jieba.posseg.cut(text)
    # 存储分词及词性分析结果
    result = []
    # 存储分词结果
    text_word = []
    # 存储词性分析结果
    text_pos = []
    # 遍历词性分析结果并返回
    for word_pos in text_pos_seg:
        curr_word_pos = f"{word_pos.word}/{word_pos.flag}"
        result.append(curr_word_pos)
        word = word_pos.word
        flag = word_pos.flag
        text_word.append(str(word).strip())
        text_pos.append(str(flag).strip())
    # 判断分词结果与词性分析结果是否匹配
    assert len(text_pos) == len(text_word)
    # print('词性标注结果：', result)
    return result, text_word, text_pos


if __name__ == '__main__':
    # test
    jieba_pos_tagging('章子怡演过多少部电影')
