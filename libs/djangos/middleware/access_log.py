#!/usr/bin/env python
# -*- coding: utf-8  -*-

'''
访问日志中间件，记录的日志是解密、组装处理后的, 即使POST请求参数也会在日志内
'''

import time
import re
from datetime import datetime
import logging
from django.conf import settings
from ..misc import get_clientip, utf82unicode
from ..logger import SysLogger
from ...common.cifa import replace_cifa_param

ACCESS_LOGGER = logging.getLogger(settings.PROJECT_ACCESS_LOG)
PASSWD_REG = re.compile(r"([&\?]+[old|new]*password=)([^&]*)")


class AccessLogMiddleware(object):
    '''
    class to log access info include post parameters
    '''

    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def _replace_privacy_param(self, url):
        '''replace password to ****** in log
        '''

        if not url:
            return url
        try:
            url = utf82unicode(url)
            url = PASSWD_REG.sub(r"\1******", url)
        except:
            pass
        return url

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        try:
            host = get_clientip(request) or "-"
            method = request.method
            scheme = request.scheme

            # 生成full_url
            path = request.path
            parameters_string = request.parameters.urlencode()
            full_url = '?'.join([path, parameters_string]) if parameters_string else path
            full_url = replace_cifa_param(full_url)  # decode cifa praram
            full_url = self._replace_privacy_param(full_url)  # replace user password
            status_code = "-"
            content_length = "-"
            status_code = "-"
            content_length = "-"
            status_code = response.status_code
            content_length = len(response.content)
            http_refer = request.META.get("HTTP_REFERER", "-")
            agent = request.META.get("HTTP_USER_AGENT", "-")
            self.end_time = time.time()
            time_delta = self.end_time - self.start_time

            now = datetime.now()
            message = '%s - - [%s] "%s %s %s" %s %s "%s" "%s" %sms' %\
                      (utf82unicode(host),
                       utf82unicode(now),
                       utf82unicode(method),
                       utf82unicode(full_url),
                       utf82unicode(scheme),
                       utf82unicode(status_code),
                       utf82unicode(content_length),
                       utf82unicode(http_refer),
                       utf82unicode(agent),
                       utf82unicode(round(time_delta * 1000))
                       )
            ACCESS_LOGGER.info(message)
        except Exception as exp:
            try:
                ACCESS_LOGGER.error("Access logging error",
                                    extra={'when': utf82unicode(now)})
                SysLogger.error(full_url)
                SysLogger.exception(exp, request)
            except:
                pass

        return response
