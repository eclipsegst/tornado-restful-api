#!/usr/bin/env python
#--------------------------------------------------------------
# Tornado restful api
# 
# Date: 2016-04-26 
#
# Author: Zhaolong Zhong
#--------------------------------------------------------------

import json
import torndb
from torndb import IntegrityError

class UserDao(object):
    def __init__(self, db=None):
        self.db = db

    def get_user_name_by_id(self, user_id):
        sql_get = (
            "SELECT username FROM user "
            "WHERE id = %s")
        row = self.db.get(sql_get, user_id)
        if not row:
            return '{}'
        else:
            result = {'username' : row['username']}
            return json.dumps(result)

    def add_user(self, user_dict):
        if not user_dict:
            return None
        
        fields = []
        values = []
        for k, v in user_dict.items():
            if v is not None:
                fields.append(str(k))
                values.append(unicode(v))
        
        sql_insert = (
            "INSERT INTO user({}) VALUES ({})".format(
                ','.join(fields),
                ','.join(['%s'] * len(values))
            )
        )
        
        try:
            row = self.db.execute(sql_insert, *values)
            result = {'success': row}
        except IntegrityError as (_, e):
            result= {'error': e}

        return json.dumps(result)