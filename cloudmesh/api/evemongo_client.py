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

    def __init__(self):
        # nothing to do
        return

    def perform_post(self, resource, data):
        headers = {'Content-Type': 'application/json'}
        print(self.endpoint(resource))
        print(json.dumps(data, indent=4).replace('\uff0E', '.'))
        #print(json.dumps(data))
        #return requests.post(self.endpoint(resource), json.dumps(data, indent=4).replace('.', '\uff0E'), headers=headers)
        return requests.post(self.endpoint(resource), json.dumps(data, indent = 4).replace('\uff0e', '.'), headers=headers)
        #return requests.post(self.endpoint(resource), json.dumps(data), headers=headers)

    def perform_get(self, resource):
        headers = {'Content-Type': 'application/json'}
        data_str = requests.get(self.endpoint(resource), headers=headers)
        print(self.endpoint(resource))
        print(data_str)
        return json.loads(data_str.text.replace('\uff0e', '.'))['_items']
 
    def perform_delete(self, resource):
        r = requests.delete(self.endpoint(resource))
        print ("'people' deleted %d", r.status_code)
        return 
    
    def endpoint(self, resource):
        return 'http://%s/%s/' % (
            ENTRY_POINT, resource)


if __name__ == '__main__':
    delete()
    ids = post_people()
    post_works(ids)
