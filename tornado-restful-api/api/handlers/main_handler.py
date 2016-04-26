#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

from api.core.base_handler import *

class MainHandler(BaseHandler):
    def get(self):
        self.write('Hello, world')