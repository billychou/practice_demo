#!/usr/bin/env python
# -*- coding: utf-8  -*-

from datetime import datetime
from functools import wraps
from fnmatch import fnmatch

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

from . import CommonStatus, ResponseContext, APIError
from .misc import get_clientip, build_signature
from .limit.backend import LimitBackend, split_rate
from .logger import SysLogger


def validate_signature(request, assign_list=[]):
    """验证sign的正确性
    """
    channel = request.parameters.get("channel")
    sign = request.parameters.get("sign")
    if not (channel and sign):
        return CommonStatus.PARAM_ERROR

    channelobj = settings.CHANNEL_CONF.get(channel)
    if not channelobj:
        return CommonStatus.SIGNATURE_ERROR

    expiration = datetime.strptime(channelobj["expiration"], "%Y-%m-%d %H:%M:%S")
    if expiration < datetime.now():
        return CommonStatus.CHANNEL_EXPIRED

    sign_list = []
    for item in assign_list:
        value = request.parameters.get(item, "")
        sign_list.append(value)

    checksum = build_signature(settings.CHANNEL_CONF, channel, "".join(sign_list))
    if getattr(settings, 'DISABLE_SIGN_CHECK', False):
        print 'Expected signature: %s' % checksum
        print 'Actual signature: %s' % sign
        sign = checksum

    return CommonStatus.SUCCESS if sign == checksum else CommonStatus.SIGNATURE_ERROR


def webservice_auth_required(assign_list=[], allow_anonymous=False, method="GET"):
    """请求基础校验装饰器；同时支持捕获APIError异常并响应
    assign_list  -- 待签名参数列表
    allow_anonymous  -- 是否允许匿名访问
    method  -- 允许的http method, 为None表示不限制method
    """

    def decorator(view_func):
        @wraps(view_func)
        def _check_authenticate(request, *args, **kwargs):
            if method and (request.method != method.upper()):
                return HttpResponseNotAllowed([method.upper()])

            statuscode = CommonStatus.UNKNOWN
            #sign_check = validate_signature(request, assign_list)
            sign_check = True
            if sign_check == CommonStatus.SUCCESS:
                try:
                    if allow_anonymous:
                        return view_func(request, *args, **kwargs)
                    elif request.user.is_active and request.user.is_authenticated():
                        return view_func(request, *args, **kwargs)
                    else:
                        statuscode = CommonStatus.NOT_LOGIN
                except APIError as ex:
                    statuscode = ex.statuscode
                except Exception as ex:
                    SysLogger.exception(ex, request)
                    statuscode = APIError().statuscode
            else:
                statuscode = sign_check
            return ResponseContext()(request, statuscode=statuscode)

        return _check_authenticate

    return decorator


def restrict_white_page_access(config):
    """view channle、IP校验装饰器

    :param config: 白名单配置项，格式：
                    {
                        'domain': ['127.0.0.1', '10.*.*.*'],
                        'channel': ['*'],
                        'description': u'示例'
                    }
    """

    def decorator(view_func):
        @wraps(view_func)
        def _validate_access(request, *args, **kwargs):
            allowed_ips = config.get('domain', [])
            allowed_channels = config.get('channel', [])
            # 验证IP
            ip_permission = False
            client_ip = get_clientip(request)
            if len(allowed_ips) == 0 or allowed_ips[0] == '*':
                ip_permission = True
            else:
                for ip in set(allowed_ips):
                    if fnmatch(client_ip, ip):
                        ip_permission = True
                        break
            if not ip_permission:
                return HttpResponseForbidden("REQUEST IP IS NOT ALLOWED")

            # 验证channel
            channel_permission = False
            channel = request.parameters.get('channel')
            if len(allowed_channels) == 0 or allowed_channels[0] == '*':
                channel_permission = True
            elif channel in allowed_channels:
                channel_permission = True
            if not channel_permission:
                return HttpResponseForbidden("REQUEST CHANNEL IS NOT ALLOWED")
            response = view_func(request, *args, **kwargs)
            return response

        return _validate_access

    return decorator

_limit_backend = LimitBackend()


def rate_limit(rate=None, rate_func=None, local=True):
    """
    Limit rate decorator.

    @rate_limit('100/5s')
    def my_view(request): pass

    Every 5 seconds 100 requests are allowed.

    Available units for rate:
    - s Second
    - m Minute
    - h Hour
    - d Day

    `rate_func` 实时获取限速参数的函数
    `local` True for using LocMemCache, else RedisCache
    """
    def decorator(fn):
        count, period = split_rate(rate)

        @wraps(fn)
        def _wrapped(request, *args, **kwargs):
            if rate_func:
                count, period = split_rate(rate_func())
            name = request.path
            _limit_backend.count(name, count, period, local)
            limit = _limit_backend.limit(name, count, period, local)
            if limit:
                error = CommonStatus.SERVER_TOO_BUSY
                return ResponseContext()(request, code=error.code, msg=error.msg)
            response = fn(request, *args, **kwargs)

            return response
        return _wrapped
    return decorator
