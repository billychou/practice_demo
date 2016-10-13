#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''只定义最基础的exception，业务级exception直接初始化APIError，不要再定义新业务级exception'''

from .statuscode import CommonStatus


class APIError(Exception):
    result = False
    statuscode = CommonStatus.UNKNOWN

    def __init__(self, statuscode=None, msg=None):
        if statuscode is not None:
            self.statuscode = statuscode
        if msg is not None:
            self.statuscode.msg = msg

    def __repr__(self):
        return '<%s(result=%r, code=%r, message=%r)>' % (self.__class__,
                                                         self.result,
                                                         self.statuscode.code,
                                                         self.statuscode.msg)

    def as_dict(self):
        return {'result': self.result, 'code': self.statuscode.code, 'message': self.statuscode.msg}


class NotFoundError(APIError):
    statuscode = CommonStatus.NOT_FOUND


class ParamError(APIError):
    statuscode = CommonStatus.PARAM_ERROR


class ParamNotEnoughError(APIError):
    statuscode = CommonStatus.PARAM_NOT_ENOUGH


class ServiceRequestError(Exception):
    statuscode = CommonStatus.UNKNOWN


class HTTPError(APIError):
    statuscode = CommonStatus.FAILURE
