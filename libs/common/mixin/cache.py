#!/usr/bin/env python
# -*- coding: utf-8  -*-

class ComboCacheMixin(object):
    """
    复合二级缓存，配合本地cache，redis|memcache使用的复合cache
    """
    backcache = None
    DEFAULT_TIMEOUT = None

    def get(self, key, default=None, version=None, timeout_set=120, timeout_exc=120):
        """
        get value
        :param key: key
        :param default: default
        :param version: version
        :param timeout_set: 取值时，如果本地没有，默认缓存到本地的过期时间
        :param timeout_exc: 取值时，l2缓存异常时，延长的过期时间
        :return:
        """
        local_key = self.make_key(key, version=version)
        self.validate_key(local_key)
        value = None
        with self._lock.reader():
            value = self._cache.get(local_key, None)

        if self._has_expired(local_key) or value is None:
            # 如果过期或为None

            try:
                # 尝试从backend cache 读取
                back_value = self.backcache.get(key, default=default, version=version)

            except Exception, ex:
                # 如果backend cache异常，且cache值不为None，则重新缓存这个key，并且延长2分钟，可通过timeout_exc设定时间
                # 下次会直接命中本地缓存
                self._printexc(ex)
                if value is not None:
                    self.set(key, value, timeout=timeout_exc, version=version)
                return value
            else:
                # 如果back cache 未抛异常，则正常处理
                self.delete(key, version=version)
                value = back_value
                if back_value is not None:
                    self.set(key, back_value, timeout=timeout_set, version=version)
                return value
        else:
            return value

    def _printexc(self, ex):
        pass

    def setl2(self, key, value, timeout=DEFAULT_TIMEOUT, timeout_l2=DEFAULT_TIMEOUT, version=None):
        # 同步set bl2缓存
        self.set(key, value, timeout, version)
        try:
            self.backcache.set(key, value, timeout_l2, version)
        except Exception, ex:
            self._printexc(ex)
