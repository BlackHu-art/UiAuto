#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/9/29 15:02
"""
import socket


class Network:
    @classmethod
    def get_local_ip(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host = s.getsockname()[0]
            return host
        except:
            print('通过UDP协议获取IP出错')
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
        return host
