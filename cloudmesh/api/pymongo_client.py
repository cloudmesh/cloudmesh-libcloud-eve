#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################

# system modules
import os

# pymongo client
from pymongo import MongoClient

# yaml modules
import yaml

#######################################################################
# Class Pymongo_client
#######################################################################
class Pymongo_client(object):
    def __init__(self):
        # get mongodb host configuration
        config_path = os.getcwd() + "/config"
        f = open(config_path + "/aws.yml")
        configd = yaml.safe_load(f)
        f.close()
        mongodb = configd["aws"]["mongodb"]
        self.host = mongodb["host"]
        self.port = (int)(mongodb["port"])
        self.db = mongodb["database"]

    def _get_db_connect(self):
        client = MongoClient(self.host, self.port)
        db = client[self.db]
        return db

    def post_one(self, collection, data):
        db = self._get_db_connect()
        conn = db[collection]
        result = conn.insert_one(data)
        return result

    def get_all(self, collection):
        db = self._get_db_connect()
        conn = db[collection]
        result = conn.find()
        return result

    def post_multiple(self, data_list):
        db = self._get_db_connect()
        posts = db.posts
        result = posts.insert_many(data_list)
        #print('One post: {0}'.format(result.inserted_id))
        return result

    def delete(self, data):
        db = self._get_db_connect()
        result = db.data.delete_many({}) 
        return result

