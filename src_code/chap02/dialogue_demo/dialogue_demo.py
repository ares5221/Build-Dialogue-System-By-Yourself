#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import requests

API_KEY = '1752ff4550e84721b132e7611152e5b5'


def getTulingResponse(msg):
    '''
    对话模块
    :param msg: 用户输入信息
    :return:
    '''
    # api 地址信息
    api = 'http://openapi.tuling123.com/openapi/api/v2'
    dat = {
        "perception": {
            "inputText": {
                "text": msg
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": ""
                }
            }
        },
        "userInfo": {
            "apiKey": API_KEY,
            "userId": '136772'
        }
    }
    dat = json.dumps(dat)
    # 发送对话请求
    r = requests.post(api, data=dat).json()
    # 对话返回信息
    mesage = r['results'][0]['values']['text']
    print('系统回复: ', r['results'][0]['values']['text'])
    return mesage


if __name__ == '__main__':

    flag = True
    while flag:
        # 获取用户输入
        user_input = input('User: ')
        # 设置对话结束条件
        if user_input == 'bye':
            flag = False
        else:
            # 对话系统回复信息
            sys_reply = getTulingResponse(user_input)
