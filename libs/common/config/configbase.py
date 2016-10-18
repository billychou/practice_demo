#!/usr/bin/env python
# -*- coding: utf-8  -*-
import types
from ..misc.sequence import get_sequence_item


class ConfigBase(object):
    '''
     for db cache, don't use DATA outside, use all_data() instead
    '''
    CONF_CACHE_BACKEND = "systemconfig"  # 默认cache配置
    CONF_CACHE_TIME = 3600 * 24  # 默认timeout24小时

    CONF_MANAGER = None
    CONF_CACHE_KEY = ""
    CONF_SYSTEM = ""
    CONF_MODULE = ""
    DATA = [
        {"id": 0, "name_zh": "未知", "name_en": "Unknown", },
    ]  # 设置默认数据，防止无配置时db空转查询;可以是dict也可以是list

    @classmethod
    def get_cache_key(cls):
        if not hasattr(cls, "_CACHE_KEY"):
            if cls.CONF_CACHE_KEY:
                cls._CACHE_KEY = cls.CONF_CACHE_KEY
            elif cls.CONF_SYSTEM and cls.CONF_MODULE:
                cls._CACHE_KEY = "AOS_%s_%s_CONF_DATA" % (cls.CONF_SYSTEM, cls.CONF_MODULE)
            else:
                # TODO raise error
                cls._CACHE_KEY = ""
        return cls._CACHE_KEY

    @classmethod
    def get_from_func_or_obj(cls):
        """
        根据配置CONF_MANAGER导入数据：
          如果CONF_MANAGER是方法，直接调用；
          如果CONF_MANAGER是model，调用它的query_config_dict方法
          如果CONF_MANAGER为空， 如果CONF_SYSTEM或者CONF_MODULE不为空，调用cm.sysconf.backend中得get_sysconfig_by_module方法

        """
        try:
            if cls.CONF_MANAGER:
                if isinstance(cls.CONF_MANAGER, types.FunctionType):
                    result = cls.CONF_MANAGER(system=cls.CONF_SYSTEM, module=cls.CONF_MODULE)
                else:
                    manager = cls.CONF_MANAGER()
                    result = manager.query_config_dict()
            elif cls.CONF_SYSTEM and cls.CONF_MODULE:
                from cm.sysconf.backend import get_sysconfig_by_module
                result = get_sysconfig_by_module(cls.CONF_SYSTEM, cls.CONF_MODULE)
            else:
                result = None
        except:
            result = None
        return result

    @classmethod
    def get_cache_client(cls):
        """获取cache client,如果需要cache支持，必须实现该方法 """
        return None

    @classmethod
    def all_data(cls):
        # 如果没有CONF_MANAGER 且 没有CONF_SYSTEM 就只能用默认的DATA
        if not ((cls.CONF_MANAGER) or (cls.CONF_SYSTEM and cls.CONF_MODULE)):
            return cls.DATA

        cache_key = cls.get_cache_key()
        cache = cls.get_cache_client()
        conf_data = None
        # load from cache
        if cache_key and cache:
            conf_data = cache.get(cache_key)
            if conf_data:
                return conf_data

        # load from db
        conf_data = cls.get_from_func_or_obj()
        if not conf_data:
            # load from DATA
            conf_data = cls.DATA
        # save to cache
        if cache_key and cache:
            cache.set(key=cache_key, value=conf_data, timeout=cls.CONF_CACHE_TIME)
        return conf_data

    @classmethod
    def refresh_cache(cls):
        '''
        use cls.DATA if there is not data in db
        '''
        # 如果没有CONF_MANAGER 且 没有CONF_SYSTEM 就只能用默认的DATA
        if not ((cls.CONF_MANAGER) or (cls.CONF_SYSTEM and cls.CONF_MODULE)):
            return cls.DATA

        cache_key = cls.get_cache_key()
        cache = cls.get_cache_client()
        conf_data = None
        conf_data = cls.get_from_func_or_obj()
        # load from DATA
        if not conf_data:
            conf_data = cls.DATA
        # save to cache
        cache.set(key=cache_key, value=conf_data, timeout=cls.CONF_CACHE_TIME)
        return conf_data

    @classmethod
    def get(cls, value="", key="id", default=None):
        data = cls.all_data()
        if isinstance(data, dict):
            key = value or key  # 方便部分直接调用get(key)
            return data.get(key) or default
        try:  # list
            return get_sequence_item(_seq=data, _key=key, _value=value) or default
        except Exception:
            return default

    @classmethod
    def search(cls, value, key="id"):
        data = cls.all_data()
        if isinstance(data, list):
            result = []
            for item in data:
                if item.get(key) == value:
                    result.append(item)
            return result

        elif isinstance(data, dict):  # dict类型的 不该调用search函数
            if key in data:
                return data
        else:
            return None
