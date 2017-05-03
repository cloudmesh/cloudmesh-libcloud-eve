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
# Database configuration
#######################################################################

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "aws"


#######################################################################
# Class Pymongo_client
#######################################################################
class Pymongo_client(object):

    def __init__(self):
        return

    def _get_db_connect(self):
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DATABASE]
        return db

    def perform_post(self, collection, data):
        db = self._get_db_connect()
        conn = db[collection]
        result = conn.insert_one(data)
        return result

    def perform_get(self, collection):
        db = self._get_db_connect()
        conn = db[collection]
        result = conn.find()
        return result

    def perform_delete(self, collection):
        db = self._get_db_connect()
        conn = db[collection]
        result = conn.delete_many({}) 
        return result

    def delete_database(self,collection):
        db = self._get_db_connect()
        print("Drop Database :: ",db)
        #db.collection.drop() 
        n  = db.runCommand( { dropAllUsersFromDatabase: 1 } )
        print("Delete user :: ",n)
        return
