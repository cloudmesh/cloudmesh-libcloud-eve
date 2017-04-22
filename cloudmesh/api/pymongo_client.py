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
        self.host = configd["aws"]["mongodb"]["host"]
        self.port = (int)(configd["aws"]["mongodb"]["port"])
        self.db = configd["aws"]["mongodb"]["database"]

    def _get_db_connect(self):
        client = MongoClient(self.host, self.port)
        db = client[self.db]
        return db

    def post_images(self, data):
        db = self._get_db_connect()
        collection = db.images
        result = collection.insert_one(data)
        return result

    def get_images(self):
        db = self._get_db_connect()
        collection = db.images
        result = collection.find()
        return result

    def post_flavor(self, data):
        db = self._get_db_connect()
        collection = db.flavor
        result = collection.insert_one(data)
        return result

    def get_flavors(self):
        db = self._get_db_connect()
        collection = db.flavor
        result = collection.find()
        return result

    def post_multiple(self, data_list):
        db = self._get_db_connect()
        posts = db.posts
        result = posts.insert_many(data_list)
        #print('One post: {0}'.format(result.inserted_id))
        return result

    def post_test(self, data):
        db = self._get_db_connect()
        tdata = db.test 
        result = tdata.insert_one(data)
        return result


    def get_test(self):
        db = self._get_db_connect()
        tdata = db.test 
        result = tdata.find_one()
        return result