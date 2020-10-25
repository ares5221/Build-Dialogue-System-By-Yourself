#!/usr/bin/env python
# _*_ coding:utf-8 _*_


#from question_classifier import *
from question_parser import *
from answer_search import *
from question_analysis import *


class ChatBotGraph:
    '''
    问答系统类
    '''
    def __init__(self):
        #self.classifier = QuestionClassifier()
        self.classifier = question_ays()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '抱歉，您的问题暂时没有找到答案，我会将您的问题记录下来。'
        res_classify = self.classifier.analysis(sent)
        # print(res_classify)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    question= '##'
    print('您好，我是小艾医生，请问您哪里不舒服？希望我的回答可以帮到您！')
    while(question!="" and question!=" "):
        question = input('用户:')
        if question == "quit" or question=="" or question == " ":break
        answer = handler.chat_main(question)
        print('小艾医生:', answer)
    print("再见！")

