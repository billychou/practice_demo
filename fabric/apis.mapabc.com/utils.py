#!/usr/bin/env python

def get_hosts(file):                                                                                               
    """                                                                                                            
        Return the hosts file through the file                                                                     
    """                                                                                                            
    ip_list = []                                                                                                   
    with open(file) as ip_file:                                                                                    
        for i in ip_file.readlines():
            ip_list.append(i.strip())
    return ip_list
