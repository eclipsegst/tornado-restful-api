#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def set_default_header(self):
        self.set_header("Content-Type", "application/json")

    @property
    def db(self):
        return self.application.db

    @property
    def user_dao(self):
        return self.application.user_dao