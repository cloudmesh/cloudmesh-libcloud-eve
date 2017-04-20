import sys

import json
import random
import requests



def perform_post(resource, data,filter=None):
    headers = {'Content-Type': 'application/json'}
    if filter:
        scode,datao = perform_get(resource, filter)
        if len(datao) > 0:
            return perform_put(resource,data,filter)
    datastr = json.dumps(data,indent=4).replace('.','\uff0E')
    r = requests.post(endpoint(resource), datastr, headers=headers)
    return r

def perform_get(resource,filter=None):
    if filter:
        url = endpoint(resource) + "?where=" + json.dumps(filter)
    else:
        url = endpoint(resource)
    headers = {'Content-Type': 'application/json'}
    out =  requests.get(url,  headers=headers)
    datastr = out.text.replace('\uff0e','.')
    scode,datam = out.status_code, json.loads(datastr)['_items']
    return scode,datam

def perform_delete(resource,filter=None):
    if filter:
        url = endpoint(resource) + "?where=" + json.dumps(filter)
    else:
        url = endpoint(resource)
    r = requests.delete(url)
    return r

def perform_put(resource,data,filter):
    if filter:
        url = endpoint(resource) + "?where=" + json.dumps(filter)
    else:
        url = endpoint(resource)
    headers = {'Content-Type': 'application/json'}
    out =  requests.get(url,  headers=headers)
    if '_items' in json.loads(out.text).keys():
        headers['If-Match'] = json.loads(out.text)['_items'][0]['_etag']
        url = endpoint(resource)+json.loads(out.text)['_items'][0]['_id']
        datastr = json.dumps(data, indent=4).replace('.', '\uff0E')
        out = requests.put(url,datastr,headers=headers)
    return out

def endpoint(resource):
    ENTRY_POINT = 'localhost:5000'
    return 'http://%s/%s/' % (
        ENTRY_POINT , resource)


if __name__ == '__main__':
    with open('../../config/restjson/all.json') as data_file:
        data = json.load(data_file)
    for j in data:
        r = perform_delete(j)
        print ('Delete : ' + str(j) + "-" + str(r.status_code))
        r = perform_post(j,data[j])
        print ('Insert : ' + str(j) + "-" + str(r.status_code))
        status_code,data1 = perform_get(j)
        print ('Get : ' + str(j) + "-" + str(status_code))
        print (data1)
        filter ={}
        print (data[j])
        if 'ID' in data[j].keys():
            key = 'ID'
        else:
            key = 'Id'
        filter[key] = data[j][key]
        status_code, data1 = perform_get(j, filter)
        print ('Get Where : ' + str(j) + "-" + str(status_code))
        print (data1)
        r=perform_put(j,data[j],filter)
        print ('Update : ' + str(j) + "-" + str(r.status_code))
        break