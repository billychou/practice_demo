#!/usr/bin/env python
# -*-coding: utf-8-*-
import  os
import sys
import re

Vipcachedir = "/home/admin/amap-aos-amaps/target/vscache/vipclient-cache"

SITES = ("ET2", "EU13", "SU18")
sites = set(SITES)
class MachineAmaps(object):
    """建立机器类,检查机器基本状态"""
    def __init__(self, ip):
        self.ip = ip

    def check_cross_site(self, site):
        """
            Return: True or False
        """
        site = self.ip.site
        #通过应用获取机房
        for root,dirs,files in os.walk(Vipcachedir):
            ROOT = root
            DIRS = dirs
            FILES = files
        filelist = []
        for file in FILES:
            filelist.append(os.path.join(ROOT, file))

        for file in filelist:
            if file != "":
                with open(file) as afile:
                    content = afile.read()













