#!/bin/bash

source /etc/profile


PID=`ps aux|grep "/opt/tomcat-hosts/apis_tomcat/"|grep -v grep|grep -v cronolog|awk '{print $2}'`

kill -9 $PID
kill -9 $PID

/opt/tomcat-hosts/apis_tomcat/bin/startup.sh
