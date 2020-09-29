#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from question_template import QuestionTemplate

# 根据问题模板的具体类容，构造cql语句，并查询
def query_template(text_pos,question_template_id_str):
    # 调用问题模板类中的获取答案的方法
    try:
        questiontemplate = QuestionTemplate()
        answer = questiontemplate.get_question_answer(text_pos,question_template_id_str)
    except:
        answer = "我也还不知道！"
    # answer = self.questiontemplate.get_question_answer(self.pos_quesiton, self.question_template_id_str)
    return answer