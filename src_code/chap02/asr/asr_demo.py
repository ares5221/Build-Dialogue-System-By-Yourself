#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
import json
import base64
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

timer = time.perf_counter

# 从应用中获取的信息
API_KEY = 'o4j7S1PUSsUgbc6bw2GbEIMA'
SECRET_KEY = 'OvugM7Liw8rlTF1C6luhOd3WMyBiVxrR'

# 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
SCOPE = 'audio_voice_assistant_get'


class DemoError(Exception):
    pass


"""  TOKEN start """
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    '''
    获取token
    :return:
    '''
    # 设置获取token的参数
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    # 通过post方式传递参数
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()

    # 获取token结果
    result = json.loads(result_str)
    # 校验token结果是否正确
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        # print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def asr(AUDIO_FILE):
    # 以下为参数设置
    # 文件格式
    FORMAT = AUDIO_FILE[-3:]

    CUID = '123456PYTHON'

    # 采样率
    RATE = 16000  # 固定值

    # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
    DEV_PID = 1537

    # asr服务地址信息
    ASR_URL = 'http://vop.baidu.com/server_api'

    # 获取token
    token = fetch_token()
    # 获取要识别的音频文件
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    # 若文件内容为空则抛出异常
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    # 使用base64加密编码
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    # 设置参数
    params = {'dev_pid': DEV_PID,
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    # 设置请求格式
    post_data = json.dumps(params, sort_keys=False)
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_json = f.read()
        # 计算服务响应实践
        # print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_json = err.read()
    # 获取语音识别结果
    result_str = str(result_json, 'utf-8')
    # print(result_strresult_str)
    # 保存语音识别结果
    with open("result.txt", "w") as of:
        of.write(result_str)
    result_data = json.loads(result_json)['result'][0]
    return result_data


if __name__ == '__main__':
    # 待识别的音频文件
    AUDIO_FILE = './audio/166k.pcm'  # 支持 pcm/wav/amr 格式
    res = asr(AUDIO_FILE)
    print(res)
