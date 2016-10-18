#!/usr/bin/env python
# -*- coding: utf-8  -*-
from ...common.mixin import AosLogFileHandlerMixin


class AosLogTimedRotatingFileHandler(AosLogFileHandlerMixin):
    """
    aos 进程安全日志处理handler
    """
    def __init__(self, filename, when='h', interval=1, backupCount=20, encoding=None, delay=False, utc=False):
        self.delay = delay
        super(AosLogTimedRotatingFileHandler, self).__init__(filename, when, interval, backupCount, encoding, delay,
                                                             utc)
