# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~
    Settings file for our little demo.
    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.
    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
#MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'user')
#MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'user')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'aws')

ALLOW_UNKNOWN = True
# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
image = {

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'schema': {
        'id': {
            'type': 'string',
            'required': True,
        },
        'name': {
            'type': 'string',
        },
        'driver': {
            'type': 'string',
        },
    }
}

flavor = {

    'schema': {
        'id': {
            'type': 'string',
            'required': True,
        },
        'name': {
            'type': 'string',
        },
        'ram': {
            'type': 'string',
        },
        'disk': {
            'type': 'integer'
        },
        'bandwidth': {
            'type': 'string'
        },
        'price': {
            'type': 'float'
        },
        'extra': {
            'type': 'dict',
            'schema': {}
        },
    }
}

location = {
    'schema': {
        'id': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'country': {
            'type': 'integer'
        },
        'availability_zone': {
            'type': 'integer'
        },
        'zone_state': {
            'type': 'string'
        },
        'region_name': {
            'type': 'string'
        },
        'provider': {
            'type': 'string',
        },
    }
}

node = {
    'schema': {
        'uuid': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'state': {
            'type': 'string'
        },
        'public_ips': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'private_ips': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'provider': {
            'type': 'string'
        },
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'image': image,
    'flavor': flavor,
    'location': location,
    'node': node,
}
