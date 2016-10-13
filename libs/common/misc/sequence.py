#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
列表操作
"""
def get_sequence_index(_seq, _key, _value):
    '''
    获取sequence（形如：[{key:value,...}, ...]）的指定查询条件的下标
    
    @param _seq:    要查询的sequence实例
    @param _key:    
    @param _value:
    '''
    try:
        i = next(index for (index, d) in enumerate(_seq) if d[_key] == _value)
        return i
    except StopIteration:
        return None
    

def get_sequence_item(_seq, _key, _value):
    '''
    获取sequence（形如：[{key:value,...}, ...]）的指定查询条件的数据项
    
    
    @param _seq:    要查询的sequence实例
    @param _key:
    @param _value:

    change log:
        v1   2012-05-24: **** liaoxingang: 注释掉先得到索引再取元素的方式，直接调用next更好。
     '''
    return next((item for item in _seq if isinstance(item, dict) and item[_key] == _value), None)


def get_sequence_items(_seq, _key, _value):
    '''
    获取sequence（形如：[{key:value,...}, ...]）的指定查询条件的数据项[]
    
    
    @param _seq:    要查询的sequence实例
    @param _key:
    @param _value:

    change log:
        initial   2012-05-24: **** liaoxingang
     '''
    return filter(lambda item: _key in item and item[_key] == _value, _seq)

def has_none_param(*args):
    '''
    判断是否存在值为None的参数

    '''
    _ret = all(args)
    return not _ret