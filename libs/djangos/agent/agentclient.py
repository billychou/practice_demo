#!/usr/bin/evn python
# -*- coding: utf-8 -*-

# Author: songchuan.zhou@alibaba-inc.com
# Date:   2016-07-03

import time
import hmac
from hashlib import sha1
from django.conf import settings
import re
import base64
import json

from libs.djangos.httpclient import RequestClient
from libs.common.error.exceptions import ServiceRequestError


class StarAgent(object):
    """
       StarAgent Client
    """
    def __init__(self, host, async=True):
        self.host = host
        self.async = async

    @classmethod
    def _sign(cls, params):
        sign_str = ''
        for k in sorted(params.keys()):
            sign_str += k
            sign_str += str(params[k])

        return hmac.new(settings.STARTAGENT_CODE, sign_str, sha1).digest().encode('hex')

    def invoke_cmd(self, cmd, args=None, script=False):
        command = '{0}({1})'.format(cmd, args) if args else cmd
        type_ = 'script' if script else 'cmd'
        params = {'key': settings.STARTAGETN_KEY,
                  'exeurl': type_ + '://' + command,
                  'timestamp': int(time.time())}

        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.host):
            params['ip'] = self.host
        else:
            params['hostname'] = self.host

        params['sync'] = 'true' if self.async else 'false'
        params['sign'] = self._sign(params)

        print params
        print settings.STARTAGENT_URL

        response = RequestClient.query(url=settings.STARTAGENT_URL + '/api/task',method="GET", params=params)
        if response.status_code != 200:
            raise ServiceRequestError(response.content)
        else:
            try:
                content = response.json()
            except ValueError:
                print "Error"
                content = response.content
        return content

    @classmethod
    def get_result(cls, tid):
        params = {'key': settings.STARTAGETN_KEY, 'tid': tid, 'timestamp': int(time.time())}
        params['sign'] = cls._sign(params)
        print "get_result",params
        response = RequestClient.query(url=settings.STARTAGENT_URL + '/api/query', method="GET", params=params)
        if response.status_code != 200:
            raise ServiceRequestError(response.content)
        else:
            try:
                print "content: json"
                content = response.json()
            except ValueError:
                print "content:content"
                content = response.content
        print content
        return content

    def store(self, dst_path, src_file):
        with open(src_file, 'r') as fp:
            content = base64.encodestring(fp.read())
            return True


if __name__ == "__main__":
    staragent = StarAgent(host="172.29.95.41", async=False)
    req = staragent.invoke_cmd("/home/admin/autonavi/scripts/a.sh")
    uid = req["TID"]
    exec_result = StarAgent.get_result(tid=uid)
    result = json.dumps(exec_result)
    print result