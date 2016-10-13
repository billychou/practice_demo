#!/usr/bin/env python
# -*- coding: utf-8  -*-
import zlib
import string
import json
import time
from hashlib import md5
from random import choice

from convert import safestr
from ..error import CommonStatus


def gen_secret_key(length=40):
    KEY_CHARACTERS = string.letters + string.digits
    return ''.join([choice(KEY_CHARACTERS) for _ in range(length)])


def data_compress(_buffer, _level=6, _mixup=False):
    if (_buffer is None) or (_buffer == ""):
        return 0, ""
    _c = zlib.compress(_buffer, _level)
    _l = len(_c)
    if _mixup and _l >= 100:
        # swap _h<>_t
        _h = 11
        _t = -51
        _converted = _c[:_h] + _c[_t] + _c[_h + 1:_t] + _c[_h] + _c[_t + 1:]
    else:
        _converted = _c
    return len(_buffer), _converted


def build_signature(channel_conf=None, channel="", raw_str="", channel_key=""):
    '''根据channel对raw_str计算签名

    :param channel_conf: channel配置对象
    :param channel:
    :param raw_str:
    :param channel_key:
    :return:
    '''

    if raw_str and ((channel_conf and channel) or channel_key):
        if not channel_key:
            channelobj = channel_conf.get(channel)
            try:
                channel_key = channelobj["key"]
            except:
                return None

        return md5("%s@%s" % (safestr(raw_str), channel_key)).hexdigest().upper()
    return None


class _Storage(dict):
    """
    from web.py
    对字典进行扩展，使其支持通过 dict.a形式访问以代替dict['a']
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError(str(k))

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError(str(k))

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


storage = _Storage


class ResponseBuilder(object):
    def response_json(self, context, ensure_ascii=True, indent=0):
        return json.dumps(context, ensure_ascii=ensure_ascii, indent=indent)

    def __call__(self, context=None, statuscode=None, code=None, msg=None, version='', result=None,
                 add_response=False):
        if not context:
            context = {}

        if result is None:
            if statuscode is not None:
                result = True if statuscode == CommonStatus.SUCCESS else False
            else:
                result = True if code == CommonStatus.SUCCESS.code else False

        response = {
            "version": version,
            "code": code if code is not None else statuscode.code,
            "message": msg or statuscode.msg,
            "timestamp": int(time.time()),
            "result": result
        }
        if add_response:
            response.update({"response": context})
        else:
            response.update(context)
        return response
