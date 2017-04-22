#!/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################

# system modules
from __future__ import print_function
import os
import sys

# Yaml modules
import yaml
#from cloudmesh.common.ConfigDict import ConfigDict # doesn't work

# AWS connection modules
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# Cloudmesh modules
import cloudmesh
from cloudmesh.common.console import Console
from cloudmesh.common.Printer import Printer

# Database modules
import json
from cloudmesh.api.pymongo_client import Pymongo_client

#######################################################################


class Aws(object):
    def __init__(self):
        config_path = os.getcwd() + "/config"
        f = open(config_path + "/aws.yml")
        self.configd = yaml.safe_load(f)
        f.close()
        # doesn't work
        #self.configd = ConfigDict("aws_bak.yml",
        #    verbose=True,load_order=[config_path])

        #self.configd = ConfigDict("cloudmesh.yaml",
        #    verbose=True,load_order=[config_path])


    def _get_driver(self):

        # get driver
        cls = get_driver(Provider.EC2)

        # credentials = self.configd["aws"]["credentials"]
        # than you can use credentials["EC2_ACCESS_KEY"]
        # this would be more readable
        # i do not think you need \

        driver = cls(self.configd["aws"]["credentials"]["EC2_ACCESS_KEY"], \
            self.configd["aws"]["credentials"]["EC2_SECRET_KEY"], \
            region = self.configd["aws"]["default"]["region"])

        return driver
   
    def images_list(self):
        """List of amazon images 
        from mongodb
        :returns: image list objects
        :rtype: NoneType

        """
        #Fetch the list of images from db
        print("fetch images list")

        # TODO : parse list
       
         #print on console

        return

    def images_refresh(self):
        """List of amazon images
        get store it in db
        :returns: None
        :rtype: NoneType

        """
        # get driver
        driver = self._get_driver()

        # TODO : check local db

        # get image list and print
        images = driver.list_images()
        image = images[0]
        sizes = db_client.get_flavors()
        size = sizes[0]
        print("List of images--------------")
        print(images)

        # TODO : parse list
        #size = [s for s in sizes if s.id == 'performance1-1'][0]
        #image = [i for i in images if 'Ubuntu 12.04' in i.name][0]

        # see code in cloudmesh.openstack for similar code
        print("======Creating node ============")
        node = driver.create_node(name='libcloud', size=size, image=image)
        print(node)
        return

    def flavor_list(self):
        
        """List of amazon images
        get store it in db
        :returns: flavor list object
        :rtype: NoneType

        """
        #fetch the list from db, parse and print
        db_client = Pymongo_client()
        data = db_client.get_flavors()

        for d in data:
            print(d)
        
       
        return
        
    def flavor_refresh(self):
        print("=============SIZES/flavors============")

        #get driver
        driver = self._get_driver()

        # TODO : check local db before fetching
        # get flavor list and print
        sizes = driver.list_sizes()
        #print(sizes)

        # TODO : parse list and store in db
        db_client = Pymongo_client()
        for size in sizes:
            # parse flavors
            data = {}
            data['id'] = size .id
            data['ram'] = size.ram
            data['disk'] = size.disk
            data['bandwidth'] = size.bandwidth
            data['price'] = size.price
            # store it in mongodb
            r = db_client.post_flavor(data)
            print(data)    
        
        print("successfully stored in db", r)
        return
        

    def key_add(self):
        db_client = Pymongo_client()
        data = {}
        data['name'] = "sam"
        data['ram'] = "16gb"
        print("======Adding key=========")

        db_client.post_test(data)
        print("======key Added Now Print=========")
        db_client.get_test()
        print("======Printed=========", db_client.get_test())
        return

    def node_list(self):

        # get driver
        driver = self._get_driver()

        # create node
        #node = driver.create_node(name='libcloud', size=size, image=image)
        print("The Node is ---------------")
        #print(node)
        return

    def node_create(self):

        # get driver
        driver = self._get_driver()

        # create node
        #node = driver.create_node(name='libcloud', size=size, image=image)
        print("The Node is ---------------")
        #print(node)
        return
