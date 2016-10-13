#!/usr/bin/env python
# -*- coding: utf-8  -*-

'''
请求初始化预处理，包括：
    1. GET、POST参数整合到parameters
    2. 请求参数统一解密
'''

from django.http import HttpResponseBadRequest, QueryDict
from ..crypt import xxtea_decrypt, aes_decrypt_base64
from ..logger import SysLogger
from ..config.crypt_keys import AmapClientKeys


class RequestInitMiddleware(object):
    '''请求初始化预处理'''
    def process_request(self, request):
        try:
            # 1. GET、POST参数整合到parameters
            request.parameters = request.GET.copy()
            raw_body = request.body
            if request.method == "POST":
                request.parameters = request.GET.copy()
                if request.META['CONTENT_TYPE'].startswith('multipart/form-data'):  # multipart
                    raw_body = ''
                elif raw_body.startswith("<") or raw_body.startswith("{"):  # xml or json
                    raw_body = ''
                # body是未加密的query_string字符串
                if '=' in raw_body:
                    request.parameters.update(QueryDict(raw_body))
                for k in request.POST:
                    # 使用setlist以兼容管理后台使用复选控件一个name多个value的情况
                    request.parameters.setlist(k, request.POST.getlist(k))

            # 2. 请求参数统一解密
            ent = request.parameters.get("ent")  # 加密类型
            in_ = request.parameters.get("in")  # 密文
            if ent:
                # body 承载密文
                if raw_body:
                    raw_body = self._aos_decrypt_parameter(request, raw_body)
                    if not (raw_body.startswith("<") or raw_body.startswith("{")):
                        request.parameters.update(QueryDict(raw_body))
                # in_ 承载密文
                if in_:
                    d_in = self._aos_decrypt_parameter(request, in_)
                    request.parameters.update(QueryDict(d_in))

                # 统一在这里pop以后不用的加密参数
                request.parameters.pop('ent', None)
                request.parameters.pop('in', None)
                request.parameters.pop('iniv', None)

        except Exception as ex:
            SysLogger.exception(ex, request)
            response = HttpResponseBadRequest()
            return response
        return None

    def _aos_decrypt_parameter(self, request, cipher):
        '''解密参数, 解密失败返回原文'''
        ent = request.parameters.get("ent")  # 加密类型
        key_conf = AmapClientKeys.get(AmapClientKeys.AMAP7)
        plain = ''
        if ent == '1':  # aes
            iniv = request.parameters.get("iniv")  # 加密iv
            if iniv:
                plain = aes_decrypt_base64(cipher, key_conf['aes_key'], iniv)
        elif ent == '2':  # xxtea
            plain = xxtea_decrypt(cipher, key_conf['xxtea_key'])
        return plain or cipher
