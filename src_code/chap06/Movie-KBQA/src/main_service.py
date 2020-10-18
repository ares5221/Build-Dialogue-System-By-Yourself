#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from question_preprocess import text_processing
from rule_based_reply import rule_based_reply
from text_pos_tagging import jieba_pos_tagging
from compose_question_template import get_question_template
from query_template import query_template


def main():
    # 获取用户输入
    user_input = input('您好，请输入您要查询的电影相关信息，如李连杰演过什么电影？：')
    # print(user_input)
    # 文本预处理
    clean_question = text_processing(user_input)
    # 基于规则的问答回复
    is_active_rule_base, sys_reply = rule_based_reply(clean_question)
    if is_active_rule_base:
        return sys_reply
    else:
        # 词性标注获取关键信息及句子模板分类
        result, text_word, text_pos = jieba_pos_tagging(clean_question)
        # 获取问题模板信息
        question_template_id_str = get_question_template(text_word, text_pos)
        # 查询图数据库，根据答案生成模板获取答案
        answer = query_template(result, question_template_id_str)
        print(answer)


if __name__ == '__main__':
    main()
