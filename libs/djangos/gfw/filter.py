#!/usr/bin/env python
# -*- coding: utf-8  -*-
from ...common.gfw.filter import SensitiveFilter as BaseFilter
from ..misc import get_cache


class SensitiveFilter(BaseFilter):
    def load(self):
        cache = get_cache('sensitive_words_cache')
        # _cache = Cache()
        data = cache.get("China_Censor_Words")
        if data:
            self.d = data
        else:
            super(SensitiveFilter, self).load()
        cache.set("China_Censor_Words", self.d, 3600 * 24 * 30)
