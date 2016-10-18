#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ...common.config import ConfigBase


class DjangoConfigBase(ConfigBase):
    '''
    for db cache, don't use DATA outside, use all_data() instead
    使用方法：
    继承ConfigBase
    1 如果是 cm.sysconf相关配置,设置好CONF_SYSTEM, CONF_MODULE就可以
    2 如果是一般的配置:
        2.1 只需要DATA数据的，配置好DATA数据就可以(支持list和dict)
        2.1 需要从db等其他地方动态取数据的时候，设置好CONF_CACHE_KEY，CONF_MANAGER
    '''
    # 默认使用的cache 设置
    CONF_CACHE_BACKEND = "systemconfig"

    @classmethod
    def get_cache_client(cls):
        """获取cache client,如果需要cache支持，必须实现该方法 """
        from ..misc import get_cache
        if cls.CONF_CACHE_BACKEND:
            return get_cache(cls.CONF_CACHE_BACKEND)

        return None
