#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import logging
import requests

from django.conf import settings
from django.core.cache import InvalidCacheBackendError

from ..logger import SysLogger
from ..misc import timestamp_to_datetime
from ..misc import get_cache


class RequestClient(object):
    @classmethod
    def get_cache_client(cls):
        try:
            return get_cache("httpclient_protect")
        except InvalidCacheBackendError:
            try:
                return get_cache("default")
            except:
                return None

    @classmethod
    def query(cls, url, method="POST", params=None, files={}, timeout=1, retry=1,
              headers=None, add_aos_headers=False):
        """
            query object,
        """
        if not params:
            params = {}
        method = method.lower()
        times, response = 0, None

        if add_aos_headers:
            default_headers = {
                "Accept-Language": "zh_CN",
                "User-Agent": "gdops",
                "Connection": "Keep-Alive",
                "Referer": "gdops.amap.com"
            }
        else:
            default_headers = {}
        if headers and isinstance(headers, dict):
            default_headers.update(headers)

        # (60, 20, 3)表示#60#s时间内错误达到#20#次，就再接下来#3#s时间内不访问
        protect_rate = getattr(settings, "HTTPCLIENT_PROTECT_RATE", None)
        cache = cls.get_cache_client()
        path = url.split("?")[0].rstrip("/")
        if protect_rate and cache:
            count = cache.get(path)
            if count and count >= protect_rate[1]:
                AccessStatus(url=url, params=params, access_time=time.time(), consuming_time=0, error_code=0).log()
                if count == protect_rate[1]:
                    cache.set(path, count + 1, protect_rate[2])
                return None

        if method in ["post", "get", "put", "delete", "options", "head"]:
            while times < retry:
                start_time = time.time()
                try:
                    response = getattr(requests, method)(url=url, params=params, headers=default_headers, files=files, timeout=timeout)
                except Exception, e:
                    SysLogger.exception(e)
                    if times == 0 and protect_rate and cache:  # 错误的话，记录1次
                        if cache.get(path):
                            cache.incr(path)
                        else:
                            cache.set(path, 1, protect_rate[0])

                end_time = time.time()
                # for log
                error_code = response.status_code if response else 599
                consuming_time = round((end_time - start_time) * 1000)  # ms
                times = times + 1 if error_code != 200 else times + retry
                access = AccessStatus(url=url, params=params, access_time=start_time,
                                      consuming_time=consuming_time, error_code=error_code)
                access.log()
        return response


class AccessStatus(object):
    def __init__(self, url, params, access_time, consuming_time,
                 error_code=200, error_message=""):
        self.url = url
        self.params = params
        self.access_time = access_time
        self.consuming_time = consuming_time
        self.error_code = error_code
        self.error_message = error_message
        self.REPORT_FUNCTION_CONF = None

    def log(self, **kwargs):
        query_time = timestamp_to_datetime(self.access_time)
        msg = '[%s] %dms [%d %s] "%s"' % (
            str(query_time), self.consuming_time, self.error_code, self.error_message, self.url)
        _logger = logging.getLogger(settings.PROJECT_BASESERVICE_LOG)
        if _logger:
            # 请求info日志不要记录traceback，会影响性能
            # extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
            _logger.info(msg)
