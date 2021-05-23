#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
import os

CORPID = os.environ['CORPID']  # 企业ID，在管理后台获取
CORPSECRET = os.environ['CORPSECRET']  # 自建应用的Secret，每个自建应用里都有单独的secret
AGENTID = os.environ['AGENTID']  # 应用ID，在后台应用中获取
TOUSER = os.environ['TOUSER']  # 接收者用户名,多个用户用|分割

def _get_access_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': CORPID,
              'corpsecret': CORPSECRET,
              }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]

def get_access_token():
    try:
        with open('access_token.conf', 'r') as f:
            t, access_token = f.read().split()
    except:
        with open('access_token.conf', 'w') as f:
            access_token = _get_access_token()
            cur_time = time.time()
            f.write('\t'.join([str(cur_time), access_token]))
            return access_token
    else:
        cur_time = time.time()
        if 0 < cur_time - float(t) < 7260:
            return access_token
        else:
            with open('.access_token.conf', 'w') as f:
                access_token = _get_access_token()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token

def send_data(message):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + get_access_token()
    send_values = {
        "touser": TOUSER,
        "msgtype": "text",
        "agentid": AGENTID,
        "text": {
            "content": str(message)
        },
        "safe": "0"
    }
    send_msges = (bytes(json.dumps(send_values), 'utf-8'))
    respone = requests.post(send_url, send_msges)
    respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
    return respone["errmsg"]


if __name__ == '__main__':
    testms = "test"
    send_data(testms)
