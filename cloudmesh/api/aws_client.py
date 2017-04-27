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
# GLOBALS

# collections
IMAGE = 'images'
FLAVOR = 'flavors'

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

        credentials = self.configd["aws"]["credentials"]
        default = self.configd["aws"]["default"]

        driver = cls(credentials["EC2_ACCESS_KEY"],
            credentials["EC2_SECRET_KEY"],
            region = default["region"])

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
            r = db_client.delete("images")
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
                if n == 10:
                    break
                #Console.ok(str(Printer.dict(d, order=['id', 'name', 'driver'])))        

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
        print("=============SIZES/flavors============")

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
        
        sz = {}
        sz['id'] = size .id
        sz['name'] = size.name
        sz['ram'] = size.ram
        sz['disk'] = size.disk
        sz['bandwidth'] = size.bandwidth
        sz['price'] = size.price
        sz['driver'] = size.driver
        sz['extra'] = {}

        im = {}
        im['id'] = str(image .id)
        im['name'] = str(image.name)
        im['driver'] = image.driver
        im['extra'] = {}

        print("creating the node with image :",im, " :: size:: ", sz)
        # create node
        node = driver.create_node(name='test1', size=size, image=image, ex_keyname=KEYPAIR_NAME,ex_securitygroup=SECURITY_GROUP_NAMES)
        print("The Node is Created --------------- :: ",node)
        #print(node)
         
        return
    
    def node_delete(self):
        # get driver
        #print("getting vm list")
        driver = self._get_driver()
        #List the running vm's
        node = self.node_list()[0]
        """
        #node = "<Node: uuid=e257efd0e6763e9fdc04b79a00f5147fcc21ee7a, name=test1, state=RUNNING, public_ips=['54.153.96.91'], private_ips=['172.31.13.22'], provider=Amazon EC2 ...>";//self.node_list()
        node = {}
        node['uuid'] = "e257efd0e6763e9fdc04b79a00f5147fcc21ee7a"
        node['name'] = "test1"
        node['state'] = "RUNNING"
        node['public_ips'] = ['54.153.96.91']
        node['private_ips'] =['172.31.13.22']
        node['provider'] = "Amazon EC2"
        """
        print("Node state :: ",node.public_ips[0], "name of node ::", node.name)
        nodes = driver.destroy_node(node)
        print("Deleted Node is ---------------",nodes)

        return
