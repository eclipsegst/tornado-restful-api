#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

from api.core.base_handler import *
from tornado.escape import json_encode

class UserHandler(BaseHandler):
    def get(self):
        #todo: handle parameter
        result = self.user_dao.get_user_name_by_id(2)
            
        self.set_default_header()
        self.write(result)

    def post(self):
        user_dict = tornado.escape.json_decode(self.request.body)
        result = self.user_dao.add_user(user_dict)
        self.set_default_header()
        self.write(result)