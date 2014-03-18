#!/usr/bin/env python
#-*-coding:utf-8-*-

import requests
import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-H","--ip", help="the ip address")
parser.add_argument("-w", "--warning", help="the warning value")
parser.add_argument("-c", "--critical", help="the critical value")
parser.add_argument("-p","--port", help="the port address")
args = parser.parse_args()

def get_value1(ip, port):
    html = requests.get('http://%s:%s/metrics'%(ip, port)) 
    content = html.text
    myjson = json.loads(content)
    return myjson["CHANNEL.channel1"]["ChannelFillPercentage"]

def get_value2(ip, port):
    html = requests.get('http://%s:%s/metrics'%(ip, port)) 
    content = html.text
    myjson = json.loads(content)
    return myjson["CHANNEL.channel2"]["ChannelFillPercentage"]


Warning_value = int(args.warning)
Critical_value = int(args.critical)

if __name__=="__main__":
    try:
        value1 = float(get_value1(args.ip, args.port))
    except Exception, e:
        print e,"Unkonwn: can't get the json"
        sys.exit(3)
    try:
        value2 = float(get_value2(args.ip, args.port))
    except Exception, e:
        #print "value2 is null"
        if value1 >= Critical_value:
            print "Critical: value2 not exist, value1=%.2f|value1=%.2f;%d;%d;0;"%(value1, value1,Warning_value, Critical_value)
            sys.exit(2)
        elif  Warning_value<value1<Critical_value:
            print "Warning: value2 not exist, but value1=%.2f|value1=%.2f;%d;%d;0;"%(value1,value1,Warning_value,Critical_value)
            sys.exit(1)
        else:
            print "OK:value2 not exist, value1=%.2f|value1=%.2f;%d;%d;0;"%(value1,value1,Warning_value,Critical_value)
            sys.exit(0)
    else:
        if value1 >= Critical_value or value2 >= Critical_value:
            print "Critical: value1=%.2f, value2=%.2f|value1=%.2f;%d;%d;0; value2=%.2f;%d;%d;0;"%(value1,value2, value1,Warning_value,Critical_value, value2,Warning_value, Critical_value )
            sys.exit(2)
        elif Warning_value<value1<=Critical_value or Warning_value<value2<=Critical_value:
            print "Warning:  value1 of ChannelFillPercentage is larger than 40,is value1=%.2f, value2=%.2f|value1=%.2f;%d;%d;0; value2=%.2f;%d;%d;0;"%(value1, value2, value1, Warning_value, Critical_value, value2, Warning_value, Critical_value )
            sys.exit(1)
        else:
            print "OK:value1=%.2f,value2=%.2f|value1=%.2f;%d;%d;0; value2=%.2f;%d;%d;0;"%(value1, value2, value1,Warning_value,Critical_value, value2, Warning_value, Critical_value )
            sys.exit(0)
    finally:
        print "The program end" 
