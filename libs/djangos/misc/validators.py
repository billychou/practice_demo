#!/usr/bin/env python
# -*- coding: utf-8  -*-

import re
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from ..misc import check_tid

white_num = '[T1][34578]\d{9}'  # T开头的手机号（T替换1）用于自动化测试，校验通过，但不发短信
mobile_re = re.compile(r"^(?:\+?86[- ]?|0)?(%s)$" % white_num)
username_re = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.]{1,98}[a-zA-Z\d]$")

validate_mobile = RegexValidator(mobile_re, 'Enter a valid mobile number.', 'invalid')
validate_username = RegexValidator(username_re, 'Enter a valid username', 'invalid')


def is_valid_mobile(mobile):
    """验证手机号码 """
    if mobile is None:
        return False
    try:
        validate_mobile(mobile)
        return True
    except ValidationError:
        return False


def is_valid_email(email):
    """验证邮箱"""
    if email is None:
        return False
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def is_valid_username(username):
    """验证用户名"""
    if not username:
        return False
    try:
        validate_username(username)
        return True
    except ValidationError:
        return False


def validate_tid(tid):
    """form中用来验证tid """
    if check_tid(tid):
        return True
    raise ValidationError("Enter a valid tid.", code="invalid")
