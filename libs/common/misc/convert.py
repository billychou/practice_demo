#!/usr/bin/env python
# -*- coding: utf-8  -*-

"""提供常用的类型转换支持"""

import itertools
import socket
import struct


def unicode2utf8(_value):
    if isinstance(_value, unicode):
        _value = _value.encode("utf-8")
    if not isinstance(_value, basestring):
        _value = str(_value)
    return _value


def utf82unicode(content):
    try:
        if not isinstance(content, basestring):
            content = str(content)
        if not isinstance(content, unicode):
            content = content.decode("utf-8")
    except:
        content = u"fail_utf8_to_unicode"
    return content


def long2bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = ''
    n = long(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 0xffffffffL) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000':
            break
    else:
        # only happens when n == 0
        s = '\000'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000' + s
    return s


def dict_encode(query_dict=None, encoding='utf-8'):
    """
        把一个单维dict的各个元素给encoding
    """
    re_dict = {}
    for key in query_dict:
        var = query_dict[key]
        try:
            if not isinstance(var, basestring):
                var = str(var)
            if not isinstance(var, unicode):
                var = var.decode('utf-8')
            var = var.encode(encoding)
            re_dict[key] = var
        except:
            continue
    return re_dict


def safeunicode(obj, encoding='utf-8'):
    """
    转换任意对象为unicode编码对象

        >>> safeunicode('hello')
        u'hello'
        >>> safeunicode(2)
        u'2'
        >>> safeunicode('\xe1\x88\xb4')
        u'\u1234'
    """
    t = type(obj)
    if t is unicode:
        return obj
    elif t is str:
        return obj.decode(encoding)
    elif t in [int, float, bool]:
        return unicode(obj)
    elif hasattr(obj, '__unicode__') or isinstance(obj, unicode):
        return unicode(obj)
    else:
        return str(obj).decode(encoding)


def pretty_string(content):
    try:
        if not isinstance(content, basestring):
            content = str(content)
        if not isinstance(content, unicode):
            content = content.decode("utf-8")
        content = content.replace("\n", "").replace("\r", "")
    except:
        content = "fail_to_pretty_string"
    return content


def safestr(obj, encoding='utf-8'):
    """
    转换任意对象为str类型
    :param obj:
    :param encoding:
    :return:
    """
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next'):  # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)


def ipstr2int(ip):
    """
    把ip地址转换为整形数
    :param ip:
    :return:
    """
    return struct.unpack('!L', socket.inet_aton(ip))[0]


def ipint2str(ip_num):
    """
    整形数转换为ip地址字符串
    :param ip_num:
    :return:
    """
    return socket.inet_ntoa(struct.pack('!L', ip_num))


def convert2int(value, default=None, minv=None, maxv=None):
    '''
    将输入值转换为int

    @param value:   输入值
    @param default: 默认值
    @param minv:    最小值
    @param maxv:    最大值
    '''
    _ret = value
    try:
        _ret = int(_ret)
    except:
        _ret = default

    if _ret is not None:
        if minv is not None and _ret < minv:
            _ret = default
        if maxv is not None and _ret > maxv:
            _ret = default
    return _ret


def convert2float(value, default=None, minv=None, maxv=None):
    '''
    将输入值转换为float


    @param value:    输入值
    @param default:  默认值
    @param minv:     最小值
    @param maxv:     最大值
    '''
    _ret = value
    try:
        _ret = float(_ret)
    except:
        _ret = default

    if _ret is not None:
        _ret = float(_ret)
        if minv is not None:
            _ret = max(_ret, minv)
        if maxv is not None:
            _ret = min(_ret, float(maxv))
    return _ret
