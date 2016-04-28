#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

import tornado.web
import json
import time

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, controller):
        self.controller = controller

    def set_default_header(self):
        self.set_header("Content-Type", "application/json")

    def prepare(self):
        try:
            token = self.get_argument('access_token', None)
            if not token:
                auth_header = self.request.headers.get('Authorization', None)
                if not auth_header:
                    raise Exception('You need a authorization token to access to this resource.')
                token = auth_header[7:]

            key = 'oauth2_{}'.format(token)
            access = self.controller.access_token_store.rs.get(key)
            if access:
                access = json.loads(access.decode())
            else:
                raise Exception('Invalid token')
            if access['expires_at'] <= int(time.time()):
                raise Exception('Expired token')
        except Exception as err:
            self.set_status(401)
            self.finish(json.dumps({'Error': str(err)}))

    @property
    def db(self):
        return self.application.db

    @property
    def user_dao(self):
        return self.application.user_dao
        
        
    