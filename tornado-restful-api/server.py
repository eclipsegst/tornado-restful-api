#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import define, options
import torndb
import json

from config import CONFIG
from application import Application

define("port", default=CONFIG['port'], help="run on the given port", type=int)
define("mysql_port", default=CONFIG['database']['port'], help="db port", type=int)
define("mysql_host", default=CONFIG['database']['host'], help="db database host")
define("mysql_user", default=CONFIG['database']['user'], help="db database user")
define("mysql_password", default=CONFIG['database']['passwd'], help="db database password")
define("mysql_database", default=CONFIG['database']['db'], help="db database name")
define("mysql_idle_timeout_sec", default=CONFIG['database']['max_idle_time_sec'], help="max mysql connection idle timeout in sec")

    
def main():
    db = torndb.Connection("%s:%s" % (options.mysql_host, options.mysql_port),
        options.mysql_database, options.mysql_user, options.mysql_password,
        options.mysql_idle_timeout_sec)
        
    settings = dict(
        site_title="Tornado Rest API",
    )
    http_server = tornado.httpserver.HTTPServer(
    Application(settings, db), xheaders=True)
    
    http_server.listen(options.port)
    print("start running on port " + options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
