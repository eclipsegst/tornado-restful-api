#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-28 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

from api.core.base_handler import *

class FooHandler(BaseHandler):
    def get(self):
        self.finish(json.dumps({'msg': 'This is Foo!'}))