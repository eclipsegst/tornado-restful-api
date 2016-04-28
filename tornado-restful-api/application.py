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

import oauth2.tokengenerator
import oauth2.grant
import oauth2.store.redisdb
import oauth2.store.mongodb
import fakeredis
import mongomock

from api.handlers.main_handler import *
from api.handlers.user_handler import *
from api.handlers.oauth2_handler import *
from api.handlers.foo_handler import *

from api.dal.user_dao import UserDao

class OAuth2Handler(tornado.web.RequestHandler):
    def initialize(self, controller):
        self.controller = controller

    def post(self):
        response = self._dispatch_request()

        self._map_response(response)

    def _dispatch_request(self):
        request = self.request
        request.post_param = lambda key: json.loads(request.body.decode())[key]

        return self.controller.dispatch(request, environ={})

    def _map_response(self, response):
        for name, value in list(response.headers.items()):
            self.set_header(name, value)

        self.set_status(response.status_code)
        self.write(response.body)
        
class Application(tornado.web.Application):
    def __init__(self, settings, db):
        auth_controller = get_auth_controller()
        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/users/?", UserHandler, dict(controller=auth_controller)),
            (r"/api/v1/users/[0-9][0-9][0-9][0-9]/?", UserHandler),
            (r'/oauth/token', OAuth2Handler, dict(controller=auth_controller)),
            (r'/foo', FooHandler, dict(controller=auth_controller)),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = db
        self.async_client = tornado.httpclient.AsyncHTTPClient()
        
        self.user_dao = UserDao(db=self.db)

def get_auth_controller():
    mongo = mongomock.MongoClient()
    mongo['db']['oauth_clients'].insert({'identifier': 'abc',
                                         'secret': 'xyz',
                                         'redirect_uris': [],
                                         'authorized_grants': [oauth2.grant.ClientCredentialsGrant.grant_type]})
    client_store = oauth2.store.mongodb.ClientStore(mongo['db']['oauth_clients'])
    token_store = oauth2.store.redisdb.TokenStore(rs=fakeredis.FakeStrictRedis())
    token_generator = oauth2.tokengenerator.Uuid4()
    token_generator.expires_in[oauth2.grant.ClientCredentialsGrant.grant_type] = 3600

    auth_controller = oauth2.Provider(
        access_token_store=token_store,
        auth_code_store=token_store,
        client_store=client_store,
       # site_adapter=None,
        token_generator=token_generator
    )
    auth_controller.token_path = '/oauth/token'
    auth_controller.add_grant(oauth2.grant.ClientCredentialsGrant())
    
    return auth_controller
