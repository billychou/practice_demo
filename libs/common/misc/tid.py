#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import binascii
import hmac
from hashlib import sha1


def b64decode(raw):
    return binascii.a2b_base64(raw)


def b64encode(raw):
    return binascii.b2a_base64(raw)


def sign(raw, key):
    hashed = hmac.new(key, raw, sha1)
    return b64encode(hashed.digest()).rstrip('\n')


def hash_code(s):
    h = 0
    for c in s:
        h = 31 * h + ord(c) & 4294967295
    return (h + 2147483648 & 4294967295) - 2147483648


def get_bytes(value):
    a = bytearray(4)
    a[3] = chr(value % 256)
    value >>= 8
    a[2] = chr(value % 256)
    value >>= 8
    a[1] = chr(value % 256)
    value >>= 8
    a[0] = chr(value % 256)
    return a


def convert_mac_style_4_byte_seq(data):
    tmp_2_1 = 0
    data[tmp_2_1] = data[tmp_2_1] ^ data[3]
    tmp_12_11 = 3
    data[tmp_12_11] = data[tmp_12_11] ^ data[0]
    tmp_22_21 = 0
    data[tmp_22_21] = data[tmp_22_21] ^ data[3]
    tmp_32_31 = 1
    data[tmp_32_31] = data[tmp_32_31] ^ data[2]
    tmp_42_41 = 2
    data[tmp_42_41] = data[tmp_42_41] ^ data[1]
    tmp_52_51 = 1
    data[tmp_52_51] = data[tmp_52_51] ^ data[2]
    return data


def is_equal(a, b):
    if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
        return True
    return False


def get_int(data):
    result = 0
    length = len(data)
    if data and length <= 4:
        for i in range(length):
            c = data[i]
            result <<= 8
            result |= (c & 0xFF)
        return result
    return 0


class M(type):
    def __new__(cls, name, bases, class_dict):
        for attr in class_dict.get('__slots__', ()):
            if attr.startswith('_'):
                def getter(self, attr=attr):
                    return getattr(self, attr)

                def setter(self, val=0, attr=attr):
                    return setattr(self, attr, val)

                class_dict['get' + attr] = getter
                class_dict['set' + attr] = setter
        return type.__new__(cls, name, bases, class_dict)


class TidObject(object):
    __metaclass__ = M
    __slots__ = ('_timestamp', '_unique_id', '_version', '_imei', "_reserve", "_is_valid", "_anti_config")

    def __init__(self, anti_config={}):
        self._timestamp = None
        self._unique_id = None
        self._version = None
        self._imei = None
        self._reserve = None
        self._is_valid = False
        self.set_anti_config(anti_config)

    def decode(self, tid):
        kwargs = self.get_anti_config() or {}
        is_need_check = kwargs.pop("is_need_check", True)
        allow_all_upper = kwargs.pop("allow_all_upper", True)
        allow_all_numbers = kwargs.pop("allow_all_numbers", False)

        if not is_need_check:
            self.set_is_valid(True)
            return None

        if tid and len(tid) == 24:
            try:
                value = b64decode(tid)
            except Exception as e:
                self.log(tid, e)
                return None

            if len(value) == 18:
                try:
                    value = bytearray(value)
                    need_check_bytes = value[:14]
                    timestamp = value[:4]
                    unique_id = value[4:8]
                    version = value[8]
                    reserve = value[9]
                    i_mei = value[10:14]
                    check_sum = value[14:18]
                    str_result = sign(need_check_bytes, "d6fc3a4a06adbde89223bvefedc24fecde188aaa9161")
                    hash1 = hash_code(str_result)
                    check_sum2 = get_bytes(hash1)
                    if version == 16:
                        check_sum = check_sum2
                        timestamp = convert_mac_style_4_byte_seq(timestamp)
                        unique_id = convert_mac_style_4_byte_seq(unique_id)
                        i_mei = convert_mac_style_4_byte_seq(i_mei)
                        version = 2
                    if is_equal(check_sum, check_sum2):
                        timestamp = get_int(timestamp)
                        unique_id = get_int(unique_id)
                        i_mei = get_int(i_mei)
                        self.set_is_valid(True)
                        self.set_timestamp(timestamp)
                        self.set_unique_id(unique_id)
                        self.set_imei(i_mei)
                        self.set_version(version)
                        self.set_reserve(reserve)
                        return True
                    elif tid.isupper() and tid.isalpha():  # 2088's bug fixed, But it has the potential risks.
                        if allow_all_upper:
                            self.set_is_valid(True)
                except Exception as e:
                    self.log(tid, e)
                return None
        elif tid is not None:
            p = re.compile("^[0-9]{20,45}$")
            m = p.match(tid)
            if m and allow_all_numbers:
                self.set_is_valid(True)
                try:
                    timestamp = int(tid[:10])
                    self.set_timestamp(timestamp)
                    self.set_version(2)
                except Exception as e:
                    self.log(tid, e)
                return None
            if tid.startswith("UTGENERATE"):
                self.set_is_valid(True)
                try:
                    timestamp = int(tid[10:20])
                    self.set_timestamp(timestamp)
                    self.set_version(2)
                except Exception as e:
                    self.log(tid, e)

    def is_valid(self, tid):
        self.decode(tid=tid)
        return self.get_is_valid()

    def log(self, tid, exception):
        """如果需要记录，请实现改log """
        pass


def check_tid(tid, **kwargs):
    tid_object = TidObject()
    return tid_object.is_valid(tid=tid)
