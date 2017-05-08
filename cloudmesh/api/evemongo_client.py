# -*- coding: utf-8 -*

"""
    This code is based on eve-demo-client available at:
    https://github.com/pyeve/eve-demo-client/blob/master/client.py
    ~~~~~~~~~~~~~~~
"""
import sys

import json
import random
import requests


ENTRY_POINT = 'localhost:5000'

#######################################################################
# Class Evemongo_client
#######################################################################
class Evemongo_client(object):
    
    @classmethod
    def post(self, resource, data):
        headers = {'Content-Type': 'application/json'}
        return requests.post(self.endpoint(resource), json.dumps(data, indent = 4).replace('\uff0e', '.'), headers=headers)

    @classmethod
    def get(self, resource):
        headers = {'Content-Type': 'application/json'}
        out = requests.get(self.endpoint(resource), headers=headers)
        data_str = out.text.replace('\uff0e', '.')
        return json.loads(data_str)['_items']
 
    @classmethod
    def delete(self, resource):
        r = requests.delete(self.endpoint(resource))
        print ("%s deleted: %d", resource, r.status_code)
        return 
    
    @classmethod
    def endpoint(self, resource):
        return 'http://%s/%s/' % (
            ENTRY_POINT, resource)

