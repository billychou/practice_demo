#!/usr/bin/env python
# -*- coding: utf-8  -*-

import json
import urllib
from functools import wraps

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponseForbidden

from ..httpclient import RequestClient 
from ..logger.syslogger import SysLogger
from ..misc import build_signature
from .constant import ChannelConf


def buc_auth_required():
    def decorator(view_func):
        @wraps(view_func)
        def authenticate(request, *args, **kwargs):
            user_info = request.session.get('user')
            print "user_info:%s"%user_info
            if not user_info:
                args = {
                    'APP_NAME': settings.APP_NAME,
                    'BACK_URL': request.build_absolute_uri(),
                }

                auth_url = '%s?%s' % (settings.LOGIN_URL, urllib.urlencode(args))
                return HttpResponseRedirect(auth_url)
            user_info = json.loads(user_info)
            emp_id = user_info.get('empId', [])
            print "emp_id:%s"%emp_id
            response = view_func(request, *args, **kwargs)
            return response
        return authenticate
    return decorator


def buc_user_info(sub_system=settings.SYSTEM):
    '''
        校验登录，仅仅往session里面写入用户信息
    '''
    def decorator(view_func):
        @wraps(view_func)
        def authenticate(request, *args, **kwargs):
            user = request.session.get('user')
            print user
            if not user:
                #如果没有用户信息，去buc登陆
                args = {
                    'APP_NAME': settings.APP_NAME,
                    'BACK_URL': request.build_absolute_uri(),
                }
                auth_url = '%s?%s' % (settings.LOGIN_URL, urllib.urlencode(args))
                print auth_url
                return HttpResponseRedirect(auth_url)
            response = view_func(request, *args, **kwargs)
            return response
        return authenticate
    return decorator


class AuthorizeView(View):
    '''
        buc回调接口，登陆验证成功之后buc调此接口传入token
    '''
    def __init__(self):
        pass

    def get(self, request):
        try:
            sso_token = request.parameters.get('SSO_TOKEN')
            back_url = request.parameters.get('BACK_URL')
            print back_url
            print sso_token
            args = {
                    'SSO_TOKEN': sso_token,
                    'RETURN_USER': 'true',
            }

            url = settings.COMMUNICATE_URL
            response = RequestClient.query(url=url, method='POST', params=args, timeout=6)
            result = json.loads(response.text)
            print "Songchuan Result: %s"%result
            user_info = result['content']
            print user_info
            request.session.update({'user': user_info})
            request.session.set_expiry(60 * 15)
        except Exception as exp:
            SysLogger.exception(exp)
            return HttpResponseForbidden('访问send post处错误')
        return HttpResponseRedirect(back_url)


class LogoutView(View):
    '''
    统一登出
    '''
    def __init__(self):
        pass

    def get(self, request):
        try:
            request.session.update({'user': None})
            args = {
                'APP_NAME': settings.APP_NAME,
                'BACK_URL': settings.DOMAIN_URL,
            }
            logout_url = '%s?%s' % (settings.LOGOUT_URL, urllib.urlencode(args))
            return HttpResponseRedirect(logout_url)
        except Exception as exp:
            SysLogger.exception(exp)
        return HttpResponseRedirect(settings.DOMAIN_URL)


class BucUser:
    """适配request.user
    """
    userid = 0
    permissions = []

    def __init__(self, userid, permissions):
        self.userid = userid
        self.permissions = permissions
