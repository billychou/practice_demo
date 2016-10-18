#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import AnonymousUser
from ..httpclient import RequestClient
from ..logger.syslogger import SysLogger
from ...common.misc import build_signature
from ...common.error import CommonStatus
from ..middleware.passport_user_middleware import FakeUser


class PassportClient():

    def __init__(self, base_url, channel, key):
        '''请求passport client

        base_url -- passport base_url. example: http://sns.amap.com:80
        channel -- channel to request passport
        key -- key to request passport
        '''
        self.base_url = base_url[:-1] if base_url.endswith('/') else base_url
        self.channel = channel
        self.key = key

    def get_userinfo(self, contact=None, uid=None, mode=None):
        '''按uid查询用户基本信息, 返回dict.

        调用内部接口, mode=None时不传mode参数,只查询uid
        文档http://docs.debug.amap.com/docs/v3/passport/account/userinfo_get

        uid -- 用户id
        contact -- 用户mobile or email
        '''
        PATH = '/ws/pp/account/userinfo/get/'
        url = self.base_url + PATH
        assert contact or uid
        raw_str = self.channel + str(contact or uid) + str(mode or '')
        sign = build_signature(channel=self.channel,
                               raw_str=raw_str,
                               channel_key=self.key)
        params = {
            'channel': self.channel,
            'sign': sign,
        }
        if contact:
            params['contact'] = contact
        elif uid:
            params['uid'] = uid
        if mode is not None:
            params['mode'] = mode
        response = RequestClient.query(url=url, method='GET', params=params)
        if response.status_code != 200:
            SysLogger.error('request %s error, http code: %s' % (url, response.status_code))
            return None
        result = json.loads(response.text)
        return result

    def get_mobile_by_uid(self, uid):
        '''按uid查询绑定的手机号

        返回值:  如果有绑定手机号，返回该手机号；
                 如果没绑定手机号，返回None
        '''
        mode = 2  # contact mode
        result = self.get_userinfo(uid=uid, mode=mode)
        try:
            mobile = result['profile']['mobile']
            return mobile if mobile else None
        except Exception:
            SysLogger.error('userinfo not found for uid %s' % uid)
            return None

    def get_uid_by_contact(self, contact):
        '''按绑定mobile/email查询uid

        返回值:  查到返回uid，查不到返回None
        '''
        result = self.get_userinfo(contact=contact, mode=None)
        try:
            uid = result['uid']
            return uid if uid else None
        except Exception:
            SysLogger.error('userinfo not found for contact %s' % contact)
            return None

    def checkout_code(self, type, relater, code, apply=0):
        """验证验证码:不支持绑定手机、绑定邮箱、重置密码类型的验证"""
        PATH = '/ws/pp/verifycode/check/'
        url = self.base_url + PATH
        raw_str = self.channel + str(code)
        sign = build_signature(channel=self.channel,
                               raw_str=raw_str,
                               channel_key=self.key)
        key = 'email' if '@' in relater else 'mobile'
        params = {
            'channel': self.channel,
            'sign': sign,
            key: relater,
            'code': code,
            'code_type': type,
            'apply': apply,
        }
        response = RequestClient.query(url=url, method='POST', params=params)
        if (not response) or (response.status_code != 200):
            SysLogger.error('request %s error, http code: %d' % (url, response.status_code if response else 599))
            return None
        result = response.json()
        return result

    def get_alipay_info(self, type=0, top_token='', cookie=''):
        '''获取用户支付宝实名信息，登录session用cookie透传，返回dict

        调用接口, 文档 http://docs.debug.amap.com/docs/v3/passport/account/get-alipay-info
        '''
        PATH = '/ws/pp/provider/alipay-info/'
        url = self.base_url + PATH
        raw_str = self.channel + str(type) + str(top_token)
        sign = build_signature(channel=self.channel,
                               raw_str=raw_str,
                               channel_key=self.key)
        params = {
            'channel': self.channel,
            'sign': sign,
            'type': type,
            'top_token': top_token,
            'need_auth_info': 1,
        }
        headers = {'Cookie': cookie}
        response = RequestClient.query(url=url, method='GET', params=params, headers=headers)
        if response.status_code != 200:
            SysLogger.error('request %s error, http code: %s' % (url, response.status_code))
            return None
        result = response.json()
        return result

    def check_tid_mobile(self, tid, mobile):
        """验证tid,mobile是否绑定"""
        PATH = '/ws/pp/device/if-exists/'
        url = self.base_url + PATH
        raw_str = self.channel + str(tid) + str(mobile)
        sign = build_signature(channel=self.channel,
                               raw_str=raw_str,
                               channel_key=self.key)
        params = {
            'channel': self.channel,
            'sign': sign,
            'tid': tid,
            'mobile': mobile
        }
        response = RequestClient.query(url=url, method='GET', params=params)
        if (not response) or (response.status_code != 200):
            SysLogger.error('request %s error, http code: %d' % (url, response.status_code if response else 599))
            return False
        result = response.json()
        if result['code'] == CommonStatus.SUCCESS.code:
            return True
        return False

    def get_user(self, uid):
        userinfo = self.get_userinfo(uid=uid, mode=0)
        try:
            profile = userinfo['profile']
            profile['id'] = profile.pop('uid')
            user = FakeUser(profile['id'])
            user.__dict__.update(profile)
        except Exception:
            SysLogger.error('userinfo not found for uid %s' % uid)
            user = AnonymousUser()
        return user
