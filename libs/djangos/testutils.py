# -*- coding: utf-8  -*-
'''testing工具'''

import json
from django.test import Client
from .misc import build_signature
from .config import ChannelConf

TEST_CHANNEL = 'aosdev'


def client_request(path, data={}, method="POST", sign_list=[], client=None, **kwargs):
    """ test Client 简单封装，默认返回json格式

    @data -- 请求参数, dict;
    @sign_list -- 计算sign的值和顺序,在有DISABLE_SIGN_CHECK的时随便传个sign就行。
    """
    method = method.lower()
    data.setdefault("channel", TEST_CHANNEL)
    data.setdefault("output", "json")
    if "sign" not in data:
        if sign_list:
            sign = "".join([str(data[k]) for k in sign_list if k in data])
        else:
            sign = "".join([str(v) for k, v in data.items() if k not in ["sign", "output"]])
        data["sign"] = build_signature(ChannelConf, TEST_CHANNEL, sign)

    if not client:
        client = Client()

    response = getattr(client, method)(path=path, data=data, **kwargs)
    if data['output'] == 'json':
        return json.loads(response.content)
