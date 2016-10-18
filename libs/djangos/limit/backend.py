#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
from django.core.cache import InvalidCacheBackendError

from ..misc import get_cache


# 不需要使用限流的，settings内不配置限流cache不要报错
try:
    CACHE = get_cache('limit_access_request')
    LOCAL_CACHE = get_cache('limit_access_request_local')
except InvalidCacheBackendError:
    pass

LIMIT_KEY_PREFIX = 'limit|path|'
_PERIODS = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 24 * 60 * 60,
}

RATE_RE = re.compile('([\d]+)/([\d]*)([smhd])')


def split_rate(rate):
    count, multi, period = RATE_RE.match(rate).groups()
    count = int(count)
    time = _PERIODS[period.lower()]
    if multi:
        time = time * int(multi)
    return count, time


class LimitBackend(object):
    """
    限流后端
    """

    def _make_key(self, name):
        return LIMIT_KEY_PREFIX + name

    def limit(self, name, count, period, local):
        """查询name identifier是否到达流量限制"""
        cache = LOCAL_CACHE if local else CACHE
        current_count = cache.get(self._make_key(name))
        if not current_count:
            return False
        return int(current_count) >= count

    def count(self, name, count, period, local):
        """为name identifier新增计数"""
        cache = LOCAL_CACHE if local else CACHE
        current_count = cache.incr(self._make_key(name))
        if int(current_count) == 1:
            cache.expire(self._make_key(name), period)
