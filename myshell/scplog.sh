#!/bin/bash
day=`date +'%Y%m%d' -d "1 day ago"`
root=/opt/data

IPADDR=`/sbin/ifconfig -a|grep "10.13"|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
Locla_file=/opt/data/$day/$IPADDR-$day.txt
Upload_file=/home/updatelog/
/opt/myshell/scplog.exp $Locla_file  $Upload_file
