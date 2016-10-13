#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from datetime import datetime


def datetime_to_timestamp(_datetime=None):
    """
        将datetime转为unix时间戳
    """
    if not isinstance(_datetime, datetime):
        _timestamp = time.time()
    else:
        _timestamp = time.mktime(_datetime.timetuple()) + _datetime.microsecond/1000000.0
    return long(_timestamp)


def timestamp_to_datetime(_timestamp):
    _value = time.localtime(float(_timestamp))
    _dt = datetime(*_value[:6])
    return _dt


def str_to_time(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def is_timestr_in_future(date_str, format="%Y-%m-%d %H:%M:%S"):
    try:
        ptime = datetime.strptime(date_str, format)
        return ptime > datetime.now()
    except:
        return False


def timestamp(_datetime=None, _type="string"):
    '''
    @param _datetime:
    @param _type: string int long float
    '''
    if (not _datetime) or (not isinstance(_datetime, datetime)):
        _timestamp = time.time()
    else:
        _timestamp = time.mktime(_datetime.timetuple()) + _datetime.microsecond / 1000000.0
    if "string" == _type.lower():
        _timestamp = str(_timestamp)
    elif "long" == _type or "int" == _type:
        _timestamp = long(float(_timestamp))
    elif "float" == _type:
        _timestamp = float(_timestamp)

    return _timestamp


def parse_date_string(s):
    """Create datetime object representing date/time
       expressed in a string
    """
    if s is None:
        return None

    s = s.strip()
    s = s.split(" ")[0]
    s = s.replace(" ", "").replace("-", "/").replace("\\", "/")
    try:
        return datetime.strptime(s, "%Y/%m/%d")
    except:
        return None
