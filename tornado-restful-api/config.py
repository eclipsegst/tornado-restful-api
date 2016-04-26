#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

__version__ = "0.0.1"
__version_info__ = __version__.split('.')

CONFIG = {
    "database": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "secret",
        "db":"rest",
        "charset": "utf8",
        "max_idle_time_sec": 200,
    },
    "port": "8000",
}