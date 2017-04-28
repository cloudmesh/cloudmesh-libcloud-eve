#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################

# system modules
from __future__ import print_function
import os
import sys

# Yaml modules
from ruamel import yaml

# AWS connection modules
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# Cloudmesh modules

# file read modules 
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import readfile

# Console printing packages
from cloudmesh.common.console import Console
from cloudmesh.common.Printer import Printer

# Database modules
import json
from cloudmesh.api.pymongo_client import Pymongo_client

#######################################################################
# GLOBALS

# collections
IMAGE = 'images'
FLAVOR = 'flavors'
#######################################################################

NODE_NAME_DEFAULT = 'test1'
KEYPAIR_NAME_DEFAULT = 'test1'

class Aws(object):
    def __init__(self):
        filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
        content = readfile(filename)
        d = yaml.load(content, Loader=yaml.RoundTripLoader)
        self.configd = d["cloudmesh"]["clouds"]["aws"]
        return

    def _get_driver(self):

        # get driver
        cls = get_driver(Provider.EC2)

        credentials = self.configd["credentials"]
        default = self.configd["default"]
        driver = cls(credentials["EC2_ACCESS_KEY"],
            credentials["EC2_SECRET_KEY"],
            region = default["location"])

        return driver
   
    def images_list(self):
        """List of amazon images 
        from mongodb
        :returns: image list objects
        :rtype: NoneType

        """
        #Fetch the list of images from db
        db_client = Pymongo_client()
        images = db_client.get_all(IMAGE)
        """
        if len(images) == 0:
            print("No image found")
        else:"""
        #parse and print it on console
        n= 1
        e = {}
        for d in images:
            e[n] = d
            n = n + 1

        Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'driver'])))
        return

    def images_refresh(self):
        """List of amazon images
        get store it in db
        :returns: None
        :rtype: NoneType

        """
        # get driver
        driver = self._get_driver()

        # get image list and print
        images = driver.list_images()
        db_client = Pymongo_client()
       
        if len(images) == 0:
            print("Error in fetching new list ...Showing existing images")
            self.images_list()
        else:
            r = db_client.delete(IMAGE)
            n = 0 ;
            e = {}
            for image in images:
                # parse flavors
                data = {}
                data['id'] = str(image .id)
                data['name'] = str(image.name)
                data['driver'] = str(image.driver)
                #data['extra'] = str(image.extra)
                # store it in mongodb
                db_client.post_one(IMAGE, data)
                e[n] = data
                n = n + 1
                
          
            Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'driver'])))
            #print(images)

        return

    def flavor_list(self):
        
        """List of amazon images
        get store it in db
        :returns: flavor list object
        :rtype: NoneType

        """
        #fetch the list from db, parse and print
        db_client = Pymongo_client()
        data = db_client.get_all(FLAVOR)
        n= 1
        e = {}
        for d in data:
            e[n] = d
            n = n + 1

        Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'ram', 'disk', 'bandwidth','price', 'extra'])))
       
        return
        
    def flavor_refresh(self):
        #get driver
        driver = self._get_driver()

        # get flavor list and print
        sizes = driver.list_sizes()
        #print(sizes)
        n = 1   
        e = {}
        db_client = Pymongo_client()
        db_client.delete(FLAVOR)
        for size in sizes:
            # parse flavors
            data = {}
            data['id'] = size .id
            data['name'] = size.name
            data['ram'] = size.ram
            data['disk'] = size.disk
            data['bandwidth'] = size.bandwidth
            data['price'] = size.price
            #data['driver'] = size.driver
            data['extra'] = size.extra
            e[n] = data
            n = n + 1
            # store it in mongodb
            db_client.post_one(FLAVOR, data)
            #print(data)    
        
        Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'ram', 'disk', 'bandwidth','price','driver','extra'])))

        #print("successfully stored in db", r)
        return
        

    def key_add(self):
        #Some test functionality
        print("======add key=========")
        db_client = Pymongo_client()
        #Some test functionality
        print("======Delete db=========")
        db_client.delete_database(FLAVOR)
       
        return

    def drop_collections(self):
        db_client = Pymongo_client()
        #Some test functionality
        print("======Delete db=========")
        db_client.delete_database(FLAVOR)
        return

    def node_list(self,SHOW_LIST):
        # get driver
        driver = self._get_driver()
        #List the running vm's
        nodes = driver.list_nodes()
        n = 0 ;
        e = {}
        for node in nodes:
            # parse flavors
            data = {}
            data['uuid'] = str(node.uuid)
            data['name'] = str(node.name)
            data['state'] = str(node.state)
            data['public_ips'] = str(node.public_ips)
            data['private_ips'] = str(node.private_ips)
            data['provider'] = str(node.driver.name)
            e[n] = data
            n = n + 1
        
        if SHOW_LIST :
            Console.ok(str(Printer.dict_table(e, order=['uuid', 'name', 'state', 'public_ips', 'private_ips','provider'])))

        return nodes

    def node_create(self, IMAGE_ID,KEYPAIR_NAME,SECURITY_GROUP_NAMES,FLAVOR_ID):

        # get driver
        driver = self._get_driver()
        
        if IMAGE_ID == '' :
            IMAGE_ID =  self.configd["default"]['image']#'ami-0183d861'
         
        
        # Name of the existing keypair you want to use
        if KEYPAIR_NAME == '' :
            KEYPAIR_NAME = KEYPAIR_NAME_DEFAULT

        # A list of security groups you want this node to be added to
        if len(SECURITY_GROUP_NAMES) == 0 :
            SECURITY_GROUP_NAMES = ['default']
        
        if FLAVOR_ID == '':
            FLAVOR_ID = self.configd["default"]['flavor']

        sizes = driver.list_sizes()
        size = [s for s in sizes if s.id == FLAVOR_ID][0]
        
        image = driver.get_image(IMAGE_ID)
       
        # create node
        node = driver.create_node(name='test1', size=size, image=image, ex_keyname=KEYPAIR_NAME,ex_securitygroup=SECURITY_GROUP_NAMES)
        print("The Node is Created --------------- :: ",node)

        if bool(node) :
            #Push the created node in db
            print("Stored in db")
        return
    
    def node_delete(self, NODE_UUID):
        # get driver
        #print("getting vm list")
        driver = self._get_driver()
        #List the running vm's

        
        #Take the running node list
        nodes = self.node_list(False)
        node = {}
        for n in nodes:
            if n.uuid == NODE_UUID:
                node = n

        if bool(node) == False:
            print("No node found to delete")
        else:
            isNodeDelete = driver.destroy_node(node)
            n = 0 ;
            e = {}
            data = {}
            data['uuid'] = str(node.uuid)
            data['name'] = str(node.name)
            data['state'] = str(node.state)
            data['public_ips'] = str(node.public_ips)
            data['private_ips'] = str(node.private_ips)
            data['provider'] = str(node.driver.name)
            e[n] = data
            n = n + 1
            Console.ok(str(Printer.dict_table(e, order=['uuid', 'name', 'state', 'public_ips', 'private_ips','provider'])))
            print("Deleted Node is ---------------",isNodeDelete)
            if isNodeDelete :
                #Delete the node from db as well
                print("Node deleted from db")
        return        
        
    def keypair_create(self, KEY_PAIR):
        """
        Creates the key pair 
        required for node object
        """
        driver = self._get_driver()
        
        name = driver.create_key_pair(KEY_PAIR)
        print("is created !",name)
        #Store the created keypair in db 
        #is created ! <KeyPair name=AWS2 fingerprint=b6:5b:7e:f1:82:35:9c:b4:d1:fd:71:9e:aa:20:83:7b:b3:c4:10:7a driver=Amazon EC2>

        return

    def keypair_delete(self, KEY_PAIR):
        """
        deletes the created key pair 
        """
        driver = self._get_driver()
        keyPairObj = self.keypair_get(KEY_PAIR)
        name = driver.delete_key_pair(keyPairObj)
        print("is deleted !",name)
        #delete the keypair from db 
       
        return
        
    def keypair_list(self):
        """
        List all the available key pair
        associated with account
        """
        driver = self._get_driver()
        
        keyPairObjs = driver.list_key_pairs()
        n =1
        e = {}
        for kp in keyPairObjs:
            data = {}
            data['name'] = kp.name
            data['fingerprint'] = kp.fingerprint
            data['driver'] = kp.driver
            e[n] = data
            n = n + 1
            
        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint','driver'])))
       
        return

    def keypair_get(self, KEY_PAIR):
        """
        Get the keypair object 
        associated with name
        """
        driver = self._get_driver()
        
        e = {}
        getKeyPairObj = driver.get_key_pair(KEY_PAIR)
        data = {}
        data['name'] = getKeyPairObj.name
        data['fingerprint'] = getKeyPairObj.fingerprint
        data['driver'] = getKeyPairObj.driver
        e[1] = data

        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint','driver'])))
       
        return getKeyPairObj

    def location_list(self):
        """
        List all
        available locations
        """
        driver = self._get_driver()
        locations = driver.list_locations()
        n = 1
        e = {}
        #<EC2NodeLocation: id=0, name=us-west-1a, country=USA, availability_zone=<ExEC2AvailabilityZone: name=us-west-1a, 
        # zone_state=available, region_name=us-west-1> driver=Amazon EC2>,
        for location in locations:
            data = {}
            data['id'] = location.id
            data['name'] = location.name
            data['country'] = location.country
            data['availability_zone'] = location.availability_zone.name
            data['zone_state'] = location.availability_zone.zone_state
            data['region_name'] = location.availability_zone.region_name
            data['provider'] = location.driver.name    
            e[n] = data
            n = n + 1
        
        Console.ok(str(Printer.dict_table(e, order=['id','name','country', 'availability_zone', 'zone_state','region_name','provider'])))
        
        return locations
        
        