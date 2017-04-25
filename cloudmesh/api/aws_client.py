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

#Console printing packages
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
        db_client = Pymongo_client()
        images = db_client.get_images()
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
            r = db_client.delete("images")
            n =0 ;
            e = {}
            for image in images:
                # parse flavors
                data = {}
                data['id'] = str(image .id)
                data['name'] = str(image.name)
                data['driver'] = str(image.name)
                # store it in mongodb
                r = db_client.post_images(data)
                e[n] = data
                n = n + 1
                if n == 10:
                    break
                
            Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'driver'])))
            print(images)

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
        n= 1
        e = {}
        for d in data:
            e[n] = d
            n = n + 1

        Console.ok(str(Printer.dict_table(e, order=['id', 'ram', 'disk', 'bandwidth','price'])))
       
        return
        
    def flavor_refresh(self):
        print("=============SIZES/flavors============")

        #get driver
        driver = self._get_driver()

        # TODO : check local db before fetching
        # get flavor list and print
        sizes = driver.list_sizes()
        #print(sizes)
        n = 1   
        e = {}
        db_client = Pymongo_client()
        for size in sizes:
            # parse flavors
            data = {}
            data['id'] = size .id
            data['ram'] = size.ram
            data['disk'] = size.disk
            data['bandwidth'] = size.bandwidth
            data['price'] = size.price
            e[n] = data
            n = n + 1
            # store it in mongodb
            r = db_client.post_flavor(data)
            #print(data)    
        
        Console.ok(str(Printer.dict_table(e, order=['id', 'ram', 'disk', 'bandwidth','price'])))

        print("successfully stored in db", r)
        return
        

    def key_add(self):
        db_client = Pymongo_client()
        #Some test functionality
        print("======Printed added key=========")
        return

    def node_list(self):

        # get driver
        print("getting vm list")
        driver = self._get_driver()
        #List the running vm's
        nodes = driver.list_nodes()
        print("The Node is ---------------",nodes)
        return nodes

    def node_create(self):

        # get driver
        driver = self._get_driver()
        # Image with Netflix Asgard available in us-west-1 region
        # https://github.com/Answers4AWS/netflixoss-ansible/wiki/AMIs-for-NetflixOSS
        AMI_ID = 'ami-c8052d8d'
        
        # Name of the existing keypair you want to use
        KEYPAIR_NAME = 'test1'
        # A list of security groups you want this node to be added to
        SECURITY_GROUP_NAMES = ['default']
        
        print("getting image and size")
        #images = driver.list_images()
        sizes = driver.list_sizes()
        images = driver.list_images()
        
        print("now selecting the image and size")
        size = [s for s in sizes if s.id == 't2.micro'][0]
        image = images[500]
        
        print("creating the node with image :",image, " :: size:: ", size)
        # create node
        node = driver.create_node(name='test', size=size, image=image,ex_keyname=KEYPAIR_NAME,ex_securitygroup=SECURITY_GROUP_NAMES)
        print("The Node is Created --------------- :: ",node)
        #print(node)
         
        return
    
    def node_delete(self):
        # get driver
        print("getting vm list")
        driver = self._get_driver()
        #List the running vm's
        node = node_list()
        nodes = driver.destroy_node(node)
        print("Deleted Node is ---------------",nodes)

        return