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
    def post(cls, resource, data):
        headers = {'Content-Type': 'application/json'}
        #print(json.dumps(data, indent = 4).replace('\uff0e', '.'))
        return requests.post(cls.endpoint(resource), json.dumps(data, indent = 4).replace('\uff0e', '.'), headers=headers)

    @classmethod
    def get(cls, resource):
        headers = {'Content-Type': 'application/json'}
        out = requests.get(cls.endpoint(resource), headers=headers)
        data_str = out.text.replace('\uff0e', '.')
        return json.loads(data_str)['_items']
 
    @classmethod
    def delete(cls, resource, filter = None):
        if filter:
            url = cls.endpoint(resource) + "?where=" + json.dumps(filter).replace('\uff0e', '.')
            headers = {'Content-Type': 'application/json'}
            data = requests.get(url, headers = headers)
            if len(json.loads(out.text)['_items']) > 0:
                for item in json.loads(data.text)['_items']:
                    headers['If-Match'] = item['_etag']
                    url = cls.endpoint(resource)+item['_id']
                    r = requests.delete(url, headers = headers)

        else:
            r = requests.delete(cls.endpoint(resource))

        print ("%s deleted: %d", resource, r.status_code)
        return 
    
    @classmethod
    def endpoint(cls, resource):
        return 'http://%s/%s/' % (
            ENTRY_POINT, resource)

