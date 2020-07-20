#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from asr.asr_demo import asr
from dialogue_demo.dialogue_demo import getTulingResponse
from tts.tts_demo import tts


def main():
    '''
    语音助手实现代码
    :return:
    '''
    # 获取用户输入的语音信息
    user_input = './asr/audio/16k.pcm'
    # 将语音信息转为文字表示
    user_text = asr(user_input)
    print('用户输入语音信息为：',user_text)
    # 获取用户输入信息的对话反馈信息
    sys_reply = getTulingResponse(user_text)
    # 将系统反馈信息转换为语音格式
    tts(sys_reply)


if __name__ == '__main__':
    main()
