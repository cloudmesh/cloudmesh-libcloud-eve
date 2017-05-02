
image = {
    'schema': {
        'id': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'driver': {
            'allow_unknown': True
        }
    }
}

flavor = {
    'schema': {
        'id': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'ram': {
            'type': 'integer'
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
        }
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
            'type': 'float'
        },
        'provider': {
            'type': 'dict',
            'schema': {}
        }
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
        'price': {
            'type': 'float'
        },
        'driver': {
            'allow_unknown': True
        }
    }
}



eve_settings = {
    'MONGO_HOST': 'localhost',
    'MONGO_DBNAME': 'aws',
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'BANDWIDTH_SAVER': False,
    'DOMAIN': {
        'image': image,
        'flavor': flavor,
        'location': location,
        'node': node,
    },
}
