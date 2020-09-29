#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from question_classification import Question_classify


def get_question_template(text_word, text_pos):
    '''
    获取问题模板
    :param text_word:
    :param text_pos:
    :return:
    '''
    # 抽取问题中的名词信息
    for item in ['nr', 'nm', 'ng']:
        while (item in text_pos):
            idx = text_pos.index(item)
            text_word[idx] = item
            text_pos[idx] = item + "ed"
    # 将用户输入问题转换为抽象问题
    str_question = "".join(text_word)
    print("抽象问题为：", str_question)
    # 通过预训练的分类器获取抽象问题相应的模板编号
    classify_model = Question_classify()
    question_template_num = classify_model.predict(str_question)
    print("抽象问题相应模板编号：", question_template_num)
    tmp = get_question_mode()
    question_template = tmp[question_template_num]
    print("问题模板：", question_template)
    question_template_id_str = str(question_template_num) + "\t" + question_template
    return question_template_id_str


def get_question_mode():
    # 读取问题模板
    with(open("./../data/question/question_classification.txt", "r", encoding="utf-8")) as f:
        question_mode_list = f.readlines()
    question_mode_dict = {}
    for one_mode in question_mode_list:
        # 读取一行
        mode_id, mode_str = str(one_mode).strip().split(":")
        # 处理一行，并存入
        question_mode_dict[int(mode_id)] = str(mode_str).strip()
    # print(self.question_mode_dict)
    return question_mode_dict
