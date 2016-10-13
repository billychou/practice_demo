#!/usr/bin/env python
# -*- coding: utf-8  -*-
import string,re

text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
_null_trans = string.maketrans('', '')


def is_text(s, text_characters=text_characters, threshold=0.30):
    """采用perl判定方法 如果字符串中包含了空值或者其中有超过30%的字符的高位被置为1
    （意味着该字符码值大于126）或是奇怪的控制码，我们就认定这段数据是二进制数据
    """
    #若s包含空值，他不是文本
    if "\0" in s:
        return False
    #一个空字符串是文本
    if not s:
        return True
    #获得s的由非文本字符构成的子串
    t = s.translate(_null_trans, text_characters)
    #如果不超过30%的字符串是非文本字符，s是字符串
    return len(t) / len(s) <= threshold


def is_textfile(filename, blocksize=512, **kwds):
    return is_text(open(filename).read(blocksize), **kwds)

def remove_htmltag(data):
    '''
    remove html tag.
    :param data:
    '''
    _req = re.compile('<[^>]*>')  # remove all HTML tags
    return _req.sub('', data)


def decode_chars_entity(data):
    '''
    decode chars entity related to html.

    :param data:
    '''
    if data and isinstance(data, basestring):
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&lt;', '<')
        data = data.replace('&gt;', '>')
        data = data.replace('&amp;', '&')
        data = data.replace('&quot;', '"')
        data = data.replace('&apos;', "'")
        data = remove_htmltag(data)
    return data
