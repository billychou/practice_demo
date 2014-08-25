#!/usr/bin/env python

#*****************************#
#***Author: songchuan.zhou   *#
#***Date: 05/12/2014         *#
#*****************************#
from __future__ import with_statement
from fabric.api import run
from fabric.api import env
from fabric.api import put
from fabric.api import local
from fabric.api import cd

from datetime import datetime
import logging
import os
import sys

from fabric.api import local,settings,abort
from fabric.contrib.console import confirm
import argparse


import utils
"""
    Task:  apis.mapabc.com op program
    Usage: Managment Platfomr
"""

###Global Variables########
###########################
API_TOMCAT_PATH = "/opt/tomcat-hosts/apis_tomcat"
GSS_TOMCAT_PATH = "/opt/tomcat-hosts/gss_tomcat"
GTS_TOMCAT_PATH = "/opt/tomcat-hosts/gts_tomcat"
NGINX_PATH = "/opt/webserver"
SHELL_PATH = "/opt/myshell"
############################

###Get the Current Path######
#############################
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname("__name__"), os.path.pardir))
print "The root path is:", ROOT_PATH

env.user = 'root'
env.password = 'mapabc&2013'

#TOOL
def get_hosts(file):
    """
        Return the hosts file through the file
    """
    ip_list = []
    #print ip_list
    with open(file) as ip_file:
        for i in ip_file.readlines():
            #print i
            ip_list.append(i.strip())
    return ip_list

#env.hosts = get_hosts("ip.alist")
hosts_ip =  utils.get_hosts("ip.alist")
print "the real addresss is ",hosts_ip
env.hosts = hosts_ip
#env.hosts = ['10.16.21.41','10.16.21.50','10.16.21.60','10.16.21.70','10.16.21.80','10.16.21.90','10.16.21.100','10.16.21.110','10.16.21.140','10.16.21.130','10.16.21.120','10.16.21.150','10.16.21.165','10.16.21.170','10.16.21.175','10.16.21.155','10.16.21.180','10.16.21.185','10.16.21.160','10.16.21.190','10.16.21.195','10.16.21.45','10.16.21.55','10.16.21.65','10.16.21.75']
#env.key_filename = '/root/.ssh/keyfile.pem'
env.password='mapabc&2013'

FORMAT = '%(asctime)-15s %(clientip)s %(user)-82 %(message)s'
logging.basicConfig(filename="apis.mapabc.com_fab.log", format=FORMAT)

logging.warning("Warning information!")   #will print the loging information to the console
logging.info("The Information!") # will not print the message

###Usage ##########################
##################################

def add_key():
    """
        Add key confidton 
    """
    put("/root/.ssh/id_rsa.pub", "/tmp/id_52.pub")
    run("cat /tmp/id_52.pub >> /root/.ssh/authorized_keys")

def mkdir_myshell():
    run("mkdir -p /opt/myshell")

def delivery_content():
    put("restart_apis_tomcat.sh","/opt/myshell/restart_apis_tomcat.sh")

def restart_tomcat_apis():
    with cd(SHELL_PATH):
        run("set -m;./restart_apis_tomcat.sh")

def demo():
    run("ls -sh")
