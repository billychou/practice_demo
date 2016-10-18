#!/usr/bin/env python
# -*- coding: utf-8  -*-


class Status(object):
    def __init__(self, code, msg, msg_cn=''):
        self._code = int(code)
        self._msg = msg
        self._msgcn = msg_cn

    def __str__(self):
        return self._msg

    def __int__(self):
        return self._code

    def __ne__(self, other):
        if hasattr(other, 'code'):
            return self._code != other.code
        else:
            try:
                return self._code != int(other)
            except:
                return self._code != other

    def __eq__(self, other):
        if hasattr(other, 'code'):
            return self._code == other.code
        else:
            try:
                return self._code == int(other)
            except:
                return self._code == other

    def __getitem__(self, key):
        if key == 'code':
            return self._code
        elif key == 'msg':
            return self._msg
        elif key == 'msgcn':
            return self._msgcn
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 'code':
            self._code = value
        elif key == 'msg':
            self._msg = value
        elif key == 'msgcn':
            self._msgcn = value
        else:
            raise KeyError

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def msgcn(self):
        return self._msgcn

    @msgcn.setter
    def msgcn(self, value):
        self._msgcn = value


class CommonStatus(object):
    '''
    错误码

    规则：子系统编码(2位. 00表示各子系统通用错误码) + 错误编码(3位)，共5位

    各系统需要继承此类，增加各自的业务错误码

    class ERROR(CommonStatus):
        _PASSPORT_BASE = 10000
        CUSTOM_ERROR = Status(_PASSPORT_BASE + 1, 'Some error msg.', u'Some cn error msg.')
    '''
    # ******************** Public -- 00 ********************
    _PUBLIC_BASE = 00000
    UNKNOWN = Status(_PUBLIC_BASE + 0, 'Unexpected error.')
    SUCCESS = Status(_PUBLIC_BASE + 1, 'Successful.')
    FAILURE = Status(_PUBLIC_BASE + 2, 'Failure.')
    PARAM_ERROR = Status(_PUBLIC_BASE + 3, 'Params error.')
    SIGNATURE_ERROR = Status(_PUBLIC_BASE + 4, 'Signature verification failed.')
    LICENSE_IS_EXPIRED = Status(_PUBLIC_BASE + 5, 'Sorry, your license has expired.')
    NOT_IMPLEMENTED = Status(_PUBLIC_BASE + 6, 'Not Implemented.')
    NOT_FOUND = Status(_PUBLIC_BASE + 7, 'Not found.')
    MULTI_FOUND = Status(_PUBLIC_BASE + 8, 'Multi-found.')
    HTTP_BODY_EMPTY = Status(_PUBLIC_BASE + 9, 'HTTP body empty.')
    XML_SYNTAX_ERROR = Status(_PUBLIC_BASE + 10, 'XML format error.')
    REQUEST_METHOD_ERROR = Status(_PUBLIC_BASE + 11, 'Request method not supported.')
    PERMISSION_DENIED = Status(_PUBLIC_BASE + 12, 'Sorry, Permission Denied.')
    STORAGE_IS_FULL = Status(_PUBLIC_BASE + 13, 'Sorry, Storage is full.')
    NOT_LOGIN = Status(_PUBLIC_BASE + 14, 'Not login.')
    CITY_NOT_SUPPORT = Status(_PUBLIC_BASE + 15, 'The city does not support.')
    TIMESTAMP_EXPIRED = Status(_PUBLIC_BASE + 16, 'Timestamp expired.')
    CHANNEL_EXPIRED = Status(_PUBLIC_BASE + 17, 'Channel expired.')
    SERVER_TOO_BUSY = Status(_PUBLIC_BASE + 18, 'Server is too busy.')  # 限流
    IN_BLACKLIST = Status(_PUBLIC_BASE + 19, 'Illegal IP, Denial of service.')  # 黑名单
    REQUEST_TOO_OFTEN = Status(_PUBLIC_BASE + 20, 'Request too often.')
    PARAM_NOT_ENOUGH = Status(_PUBLIC_BASE + 21, 'Params not enough.')
    ALREADY_LOGIN = Status(_PUBLIC_BASE + 22, 'already login', u'已经登录')
