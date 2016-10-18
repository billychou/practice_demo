#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os

import django
from django.http import HttpResponse
from django.conf import settings

from ...common.misc import ResponseBuilder
from .. import CommonStatus

if django.VERSION >= (1, 7):  # pragma: nocover

    def get_cache(name):
        from django.core.cache import caches
        return caches[name]
else:
    from django.core.cache import get_cache  # pragma: nocover

"""
misc tools
"""


class ResponseContext(ResponseBuilder):
    """
    响应数据构造
    """
    def response_json(self, context, ensure_ascii=True, indent=0):
        """response json"""
        response = super(ResponseContext, self).response_json(context, ensure_ascii=True, indent=0)
        response = HttpResponse(response, content_type="application/json")
        if context.get("code", "") == CommonStatus.NOT_LOGIN.code:
            response["aos-errorcode"] = CommonStatus.NOT_LOGIN.code
        return response

    def response_pb(self, context):
        """response protobuffer"""
        raise NotImplementedError

    def __call__(self, request, context=None, statuscode=None, code=None, msg=None, result=None,
                 add_response=False):
        """
        构造响应数据
        :param request: django请求对象
        :param context: 响应数据字典 type:dict
        :param statuscode: 错误状态对象
        :param code: 自定义错误码，为空则使用状态对象中的错误码
        :param msg: 错误信息，为空则使用错误对象中的msg
        :param result: 响应结果状态，默认为None，自动判断 type: bool
        :return str 序列化json数据或pb流
        """
        response = super(ResponseContext, self).__call__(context, statuscode=statuscode, code=code, msg=msg,
                                                         version=settings.VERSION,
                                                         result=None,
                                                         add_response=add_response)

        output = request.parameters.get('output')
        if output == 'pb':
            return self.response_pb(response)
        else:
            return self.response_json(response)


def get_clientip(request, distinct=True):
    """
    获得客户端ip
    :param request:
    :return: clientip or ''
    """
    serverip = request.META.get("HTTP_NS_CLIENT_IP")  # NAT模式新加的header
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('HTTP_X_FORWARDED_FOR') or ''
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('HTTP_PROXY_CLIENT_IP') or ''
    if not serverip or serverip.lower() == "unknown":
        serverip = request.META.get('HTTP_WL_PROXY_CLIENT_IP') or ''
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('REMOTE_ADDR') or ''
    if serverip and serverip.lower() != "unknown":
        if distinct:
            serverip_list = []
            for ip in serverip.split(','):
                ip = ip.strip()
                if ip and ip not in serverip_list:
                    serverip_list.append(ip)
            serverip = ','.join(serverip_list)
        return serverip
    return ''


def smart_config_import(config_path):
    '''根据settings中的ENV_TYPE自动选择导入的相应环境

    @config_path -- config文件的__file__值.可能为绝对路径，也可能为相对路径
    '''
    abs_path = os.path.abspath(config_path)
    # 获得BASE_DIR后的path
    module_split = os.path.splitext(abs_path)[0].replace(settings.BASE_DIR + '/', '').split('/')
    env_type = getattr(settings, 'ENV_TYPE', 'dev').lower()
    # 拼接待import的module全点路径
    smart_module_name = '%s.%s.%s' % ('.'.join(module_split[:-1]), env_type, module_split[-1])
    # 去除中间的'.dev'
    smart_module_name = smart_module_name.replace('.dev.', '.')
    return 'from %s import *' % smart_module_name
