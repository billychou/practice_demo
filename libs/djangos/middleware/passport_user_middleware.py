#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from importlib import import_module
from django.conf import settings
from django.core.cache import get_cache
from django.contrib.auth import SESSION_KEY
from django.utils.functional import SimpleLazyObject

from redis.exceptions import RedisError

from ..misc import FakeUser

SessionStore = import_module(settings.PASSPORT_SESSION_ENGINE).SessionStore


class PassportSessionStore(SessionStore):

    def __init__(self, session_key=None):
        super(PassportSessionStore, self).__init__(session_key)
        self._cache = get_cache(settings.PASSPORT_SESSION_CACHE_ALIAS)


class AuthenticationMiddleware(object):
    def _get_user(self, request):
        from django.contrib.auth.models import AnonymousUser
        # (60, 20, 3)表示#60#s时间内错误达到#20#次，就再接下来#3#s时间内不访问
        protect_rate = getattr(settings, 'PASSPORT_SESSION_PROTECT_RATE', None)
        cache_name = getattr(settings, 'PASSPORT_SESSION_PROTECT_CACHE', None)
        rate_cache = get_cache(cache_name) if cache_name else None
        if protect_rate and rate_cache:
            count = rate_cache.get('count', 0)
            if count >= protect_rate[1]:
                if count == protect_rate[1]:
                    rate_cache.set('count', count + 1, protect_rate[2])
                return AnonymousUser()
        try:
            session_key = request.COOKIES.get(settings.PASSPORT_SESSION_COOKIE_NAME, None)
            session = PassportSessionStore(session_key)
            user_id = int(session[SESSION_KEY])
            user = FakeUser(user_id)
        except (KeyError, RedisError, ValueError):
            # cache连接异常返回匿名用户
            user = AnonymousUser()
            if protect_rate and rate_cache:
                count = rate_cache.incr('count')
                if count == 1:
                    rate_cache.set('count', 1, protect_rate[0])
        return user

    def _get_cached_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = self._get_user(request)
        return request._cached_user

    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = SimpleLazyObject(lambda: self._get_cached_user(request))
