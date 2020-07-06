#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
from intelligent_service import getBestAnswer
import time


async def handle(request):
    '''
    处理GET请求
    :param request:
    :return:
    '''
    varDict = request.query
    question = varDict['question']
    question = clean_text(question)
    sys_reply, QA_que, QA_ans = getBestAnswer(question)  # 比较余弦相似度查找相似问题
    reply_json = {'系统回复': sys_reply, '相似问题': QA_que, '推荐答案': QA_ans}
    print('Current time is:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return web.json_response(reply_json)


def clean_text(word):
    '''
    问题文本清理
    :param word:
    :return:
    '''
    res = ''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            res += ch
    return res


async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port='9010')
