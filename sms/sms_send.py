#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
    Author: songchuan.zhou@autonavi.com
    Date: 11/26/2013
    Function:    
            1.Send the special information to the users through sms. 
            2.Store the sended information to the mysql dababase sms_send.
    Detail:
            1.使用高德短信平台发送信息，已经和客服部联系,账号已经开通。
              这些API接口包括name:SMSUSER、password:SMSPASSWORD、
            2.数据库保存发送的信息。MySQL数据库需要保存DBUSER、DBPASSWORD、DBNAME
    短信报警API接口：
            运维部监控中心 所需的短信测试通道已经开通，信息如下：
            通道号码：36
            完整号码：10657502096336
            测试用户名：atest36_13
            测试密码：ywjkzx
            开通的正式账号：
                账号: autonavi260
                密码: 8Eb08#c$

            servlet接口：http://www.findpath.net:82/smmp/servletsendmoremsg.do 
            接口参数：
            name——用户名
            password——密码
            mobiles——手机号码（同时发送多个，最多1000,多个号码之间用半角“,”分割）
            content——短信内容
            短信平台的部分特性说明：
            1. 短信平台可以向移动、联通、电信手机号码发送短信，仅支持移动号码向平台发送短信
            2. 每条短信最多支持60个字符，超过60个字符，系统会截取成多条，并在短信内容前加入（n/m）标示短信条数
            3. 短信平台会自动过滤部分关键字，短信内容含有关键字的，将禁止发送。（禁用关键字内容见附件）
            
"""
import requests
import argparse
import time
import MySQLdb


#CONSTANT VARIABLES
DBHOST = "180.96.71.115"
DBUSER = "root"
DBPASSWORD = "AutoNavi&2013"
DBNAME = "sms_send"

SMSUSER = "autonavi260"
SMSPASSWORD = "8Eb08#c$"
SMSURL = 'http://www.findpath.net:82/smmp/servletsendmoremsg.do'

#argument
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phone", help="The phone number")
parser.add_argument("-c", "--content", help="The content send by sms")
args = parser.parse_args()

def timestamp_datetime(value):
    """
        transfer the unix time to the localtime.
    """
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def usage():
    print """
        Usages:
        ./sms_send.py [-p|--phone] 88888888888 [-c|--content] "The sms content"
    """
    
def insertSmsRecord(phone, content):
    """
        FuncName: Insert_sms_record(phone, content)
        Usage:  add an record to the database.
        
    """
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASSWORD, port=3306, db="sms_send")
    smscursor = conn.cursor()
    params = (phone, content, timestamp_datetime(time.time()))
    #Database insert into datetime.
    
    sql = "insert into sms (phone, content, INSERT_TIME) values (%s, %s, %s)"
    try:
        smscursor.execute(sql, params)
        conn.commit()
    except:
        conn.rollback()
    smscursor.close()
    conn.close()
    
def smsSend(phone, content):
    """
        send the content to the phone
    """
    myparams = {"name":SMSUSER, "password":SMSPASSWORD, "mobiles":phone, "content":content}
    r = requests.get(SMSURL, params=myparams)
    print r
        
if __name__=="__main__":
    if args.phone and args.content:
        smsSend(args.phone, args.content)
        insertSmsRecord(args.phone, args.content)
    else:
        print "Unknown parameter, please refer --help for more detail"
        usage() 
        
        
#http://www.findpath.net:82/smmp/servletsendmoremsg.do?name=autonavi260&password=8Eb08#c$&mobiles=18638165423&content=test