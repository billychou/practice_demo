#!/usr/bin/env python
import hashlib
from django.conf import settings
import time
from libs.djangos.httpclient import RequestClient
import md5
import json
from libs.common.error.exceptions import HTTPError


class Armory(object):
    m = md5.md5(settings.ARMORY_USERNAME +
            time.strftime('%Y%m%d', time.localtime(time.time())) +
            settings.ARMORY_KEY)
    secret_key = m.hexdigest()

    @classmethod
    def _common_device_query(cls, attr, value):
        url = settings.ARMORY_URL + '/page/api/free/opsfreeInterface/search.htm'
        params = {
            'from': 'device',
            '_username': settings.ARMORY_USERNAME,
            'q': "{0}=={1}".format(attr, value),
            'num': '0',
        }

        response = RequestClient.query(url, params=params)
        if response.status_code != 200:
            raise HTTPError("armroy api return error")
        result = json.loads(response.content)['result']
        return result

    @classmethod
    def query_nodegroups_by_appnode(cls, appnode):
        url = settings.ARMORY_URL + '/page/api/free/product/getnodeinfo.htm'
        params = {
            'appname': appnode,
            '_username': settings.ARMORY_USERNAME,
        }

        response = RequestClient.query(url, params=params)
        if response.status_code != 200:
            raise HTTPError("armroy api return error")
        result = json.loads(response.content)["nodegroup"].values()
        return result

    @classmethod
    def query_device_by_nodegroup(cls, nodegroup):
        return cls._common_device_query('nodegroup', nodegroup)