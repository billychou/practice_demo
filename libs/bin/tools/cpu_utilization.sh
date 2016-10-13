#!/usr/bin/env bash


process=`ps -eo pcpu,pid,user,args|sort -k 1 -r |head`


