#!/usr/bin/env python
# -*- coding: utf-8  -*-

""" SysLogger日志 """

import traceback
import logging
import logging.config
import sys

from django.conf import settings


class SysLogger(object):
    ''' system logger '''
    INFO_LOGGER = logging.getLogger(settings.PROJECT_INFO_LOG)
    ERROR_LOGGER = logging.getLogger(settings.PROJECT_ERROR_LOG)
    EXCEPTION_LOGGER = logging.getLogger(settings.PROJECT_EXCEPTION_LOG)

    @classmethod
    def debug(cls, msg):
        '''
        logging debug message
        :param cls:
        :param msg:
        '''
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.INFO_LOGGER.debug(msg, extra=extra)

    @classmethod
    def info(cls, msg):
        '''
        logging info message，info类型不要搜集traceback
        :param cls:
        :param msg:
        '''
        # extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.INFO_LOGGER.info(msg)

    @classmethod
    def warn(cls, msg):
        '''
        logging warn message
        :param cls:
        :param msg:
        '''
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.INFO_LOGGER.warn(msg, extra=extra)

    @classmethod
    def error(cls, msg):
        '''
        logging error message
        :param cls:
        :param msg:
        '''
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.ERROR_LOGGER.error(msg, extra=extra)

    @classmethod
    def exception(cls, exp, request=None):
        '''
        logging exception under both error file and log file.
        :param cls:
        :param exp:
        :param request: 可以为sentry提供request信息，能传尽量传
        '''
        extra = {
            "realLocation": repr(traceback.format_stack(limit=2)[0]),
            "request": request
        }
        cls.INFO_LOGGER.error(exp, extra=extra)
        if sys.version_info >= (2, 7, 7):  # python2.7.7后才支持extra参数
            cls.EXCEPTION_LOGGER.exception(exp, extra=extra)
        else:
            cls.EXCEPTION_LOGGER.exception(exp)
