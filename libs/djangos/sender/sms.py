#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import uuid
import json
from urllib import urlencode
from ..misc import unicode2utf8, build_signature
from ...common.crypt import aes_cbc_encrypt_base64
from ..logger import SysLogger
from ..httpclient import RequestClient
from ..config import TaobaoSMSTemplateConfig, SMS_HOLE_URL


class UnknownSMSTypeException(ValueError):
    msg = "unknown sms_type"

    def __str__(self):
        return '%s<msg:%s>' % (self.__class__, self.msg)


def send_sms_via_hole(number, sms_type, crypt_conf, **kwargs):
    """
    通过淘宝通道发送短信
    crypt_conf对象格式：

    class CryptKeys(ConfigBase):
    BASE = 0
    HOLE = BASE + 13  # 淘宝MC转发代理

    DICT = [
        {
            "id": HOLE,
            "channel": "aos",
            "channel_key": "<key>",
            "aes_key": "<aes_key>",
            "is_encrypt": True  # 是否加密
        },
    ]

    :param number:
    :param sms_conf: 短信配置
    :param crypt_conf: 加密配置
    :param url:
    :param kwargs:
    :return:
    """

    if number.startswith('T'):  # T开头的手机号（T替换1）用于自动化测试，不发短信
        return True, u"自动化测试"

    sms_conf = TaobaoSMSTemplateConfig.get(sms_type)
    if sms_conf is None:
        raise UnknownSMSTypeException
    content = ''
    for key in sms_conf['keywords']:
        content += '%s:%s;' % (key, kwargs[key])
    content = content[:-1]  # 去除末尾的';'
    # try:
    post_dict = {
        "channel": crypt_conf["channel"],
        "mobile": unicode2utf8(number),
        "content": unicode2utf8(content),
        "source_id": sms_conf['source_id'],
        "template_id": sms_conf['template_id'],
        "message_type_id": sms_conf['message_type_id'],
        "sign": ''
    }
    # 计算签名
    assign_list = ['channel', 'mobile', 'content', 'source_id', 'template_id', 'message_type_id']
    raw_str = ''
    for item in assign_list:
        raw_str += post_dict.get(item, '')
    sign = build_signature(channel_key=crypt_conf['channel_key'], raw_str=raw_str)
    post_dict.update({'sign': sign})
    uuid_hex = uuid.uuid4().hex  # 用于标记请求、响应的标号，只是记日志使用
    SysLogger.info("send sms request %s: %s" % (uuid_hex, json.dumps(post_dict, ensure_ascii=False)))
    # 计算加密
    if crypt_conf['is_encrypt']:
        query_string = urlencode(post_dict)
        _in = aes_cbc_encrypt_base64(query_string, crypt_conf['aes_key'])
        post_dict = {"ent": 1, "in": _in}

    response = RequestClient.query(url=SMS_HOLE_URL, method='POST', params=post_dict)
    SysLogger.info("send sms response %s: http code--%s, http data--%s" % (uuid_hex, response.status_code, response.text))
    if response.status_code == 200:
        try:
            r_dict = response.json()
            return int(r_dict['code']) == 1, content
        except Exception as e:
            SysLogger.exception(e)
            return False, content
    else:
        SysLogger.error('request %s error, http code is %s' % (SMS_HOLE_URL, response.status_code))
        return False, content
