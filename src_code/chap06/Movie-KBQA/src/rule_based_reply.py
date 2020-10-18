#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import random


def rule_based_reply(user_input):
    '''
    对用户的输入信息判定是否需要基于规则进行回复
    :param user_input:
    :return:
    '''
    # 是否激活规则回复
    is_active_rule_base = False
    greeting_user_dia = ['你好', '您好', '早上好', '早安', '哈喽', '嗨']
    greeting_sys_dia = ['你好', '您好', '哈喽', '嗨']
    bye_user_dia = ['再见', '拜拜']
    bye_sys_dia = ['再见']
    chat_user_dia = ['你会做什么', '你会什么', '你能干什么']
    chat_sys_dia = ['您可以查询电影相关信息。', '您可以查询演员相关信息。']
    if user_input in greeting_user_dia:
        greeting_info = '，请输入您要查询的电影相关信息，如李连杰演过什么电影？'
        rule_based_res = random.choice(greeting_sys_dia) + greeting_info
        is_active_rule_base = True
    if user_input in bye_user_dia:
        rule_based_res = random.choice(bye_sys_dia)
        is_active_rule_base = True
    if user_input in chat_user_dia:
        rule_based_res = random.choice(chat_sys_dia)
        is_active_rule_base = True
    if is_active_rule_base:
        return is_active_rule_base, rule_based_res
    else:
        return is_active_rule_base, user_input