#!/bin/bash
# -*- coding: UTF8 -*-
#
# Copyright (C) 2013 Edgewall Software
#
# Intro: cut log & del old log

date_d=`/bin/date +%Y-%m-%d`
for i in `cat /opt/mytoolsh/cut_log/config.txt`
do
  days=`echo $i | awk -F '&' '{print $2}'`
  log_path=`echo $i | awk -F '&' '{print $1}'`
  #name=${log_path##*/}-${date_d}
  #save_path=${log_path%/*}
  file_name=`basename ${log_path}`
  name=`basename ${log_path}-${date_d}`
  save_path=`dirname ${log_path}`
###############variable#######################
  [ ! -f $log_path ] && exit 1
  cd $save_path
  cat $file_name >  $name.log
  tar zcf $name.tar.gz $name.log
  cat /dev/null > $log_path
  rm -fr $name.log
  find $save_path/ -type f -name "${file_name}*.tar.gz" -mtime +${days} -exec rm -fr {} \;
  sleep 2
done
