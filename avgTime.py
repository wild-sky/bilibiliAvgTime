'''
author:野漫横江 (wildsky)
date:2020/09/18
'''

import requests as rq
import json

BV2AV_API = 'https://api.bilibili.com/x/web-interface/view'  # ?bvid=
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/80.0.3987.149 Safari/537.36'}


def bvToAid(bv):
    '''
    根据BV返回对应的Aid
    :param bv: BV号
    :return: 返回BV对应的aid
    '''
    r = rq.get(BV2AV_API, {'bvid': bv}, headers=HEADER)
    response = json.loads(r.text)
    try:
        return str(response['data']['aid'])
    except (KeyError, TypeError):
        return None


def getVideoMsg(aid):
    '''
    根据aid信息得到对于视频集的json数据
    :param aid:
    :return:
    '''
    url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
    try:
        res = rq.request(url=url, method='get')
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return "err"


def getTimeCount(aid):
    '''
    根据json数据计算出相应视频个数及总时长
    :param aid:
    :return:返回一个元组 包含总时间及总视频个数
    '''
    jsonMsg = getVideoMsg(aid)
    data = json.loads(jsonMsg)['data']
    title = data['title']
    time = data["duration"]
    length = data['videos']
    return title, time, length


if __name__ == '__main__':
    aid = bvToAid('BV14J4114768')
    title, t, l = getTimeCount(aid)
    print('视频标题：%s' % title)
    print('视频个数： %d 个\n视频平均时长: %.2f 分钟' % (l, t / l / 60))
