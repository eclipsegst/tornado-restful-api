#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

import tornado
import tornado.web
import tornado.httpclient

from api.handlers.main_handler import *
from api.handlers.user_handler import *

from api.dal.user_dao import UserDao

class Application(tornado.web.Application):
    def __init__(self, settings, db):
        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/users/?", UserHandler),
            (r"/api/v1/users/[0-9][0-9][0-9][0-9]/?", UserHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = db
        self.async_client = tornado.httpclient.AsyncHTTPClient()
        
        self.user_dao = UserDao(db=self.db)