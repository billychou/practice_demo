#!-*-coding:utf-8-*-
import md5
import time
import requests


#API域名
MAC_ADDR="d4:0B:1a:69:43:c2"
Productnet="api-inc.m.alibaba-inc.com"

_username="songchuan.zhou"
_rsa="58a65fab84fff10122534de269b1c2f7"

#生成访问秘钥
m=md5.new(_username+time.strftime('%Y%m%d', time.localtime(time.time())) + _rsa)
_key=m.hexdigest()


preurl="http://api.m.alibaba-inc.com/monitor/api/monitorDataQuery.rdo"

payload = {
	"monitorType":1,
}


