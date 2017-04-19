#!/usr/bin/env python
from __future__ import print_function
import cloudmesh
#import libcloud
import os
#import requests
#import json
import sys
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh.api.mogo_eve_client import post_people
#from cloudmesh.common.ConfigDict import ConfigDict # doesn't work
import yaml
#######################################################################


class Aws(object):
    def __init__(self):
        config_path = os.getcwd() + "/config"
        f = open(config_path + "/aws_bak.yml")
        self.configd = yaml.safe_load(f)
        f.close()
        # doesn't work
        #configd = ConfigDict("aws_bak.yml",
        #    verbose=True,load_order=[config_path])
        #cls = get_driver(Provider.EC2)
        #self.driver = cls(configd["aws"]["credentials"]["EC2_ACCESS_KEY"], \
        #    configd["aws"]["credentials"]["EC2_SECRET_KEY"], \
        #    region = configd["aws"]["default"]["region"])
       
    def images_list(self):
        """List of amazon images
        
        :returns: None
        :rtype: NoneType

        """
        #print(self.configd)

        # get driver
        cls = get_driver(Provider.EC2)
        driver = cls(self.configd["aws"]["credentials"]["EC2_ACCESS_KEY"], \
            self.configd["aws"]["credentials"]["EC2_SECRET_KEY"], \
            region = self.configd["aws"]["default"]["region"])

        # TODO : check local db

        # get image list and print
        images = driver.list_images()
        print("List of images--------------")
        print(images)

        # TODO : parse list
        #size = [s for s in sizes if s.id == 'performance1-1'][0]
        #image = [i for i in images if 'Ubuntu 12.04' in i.name][0]

        return

    def flavor_list(self):
        print("=============SIZES/flavors============")

        # get driver
        cls = get_driver(Provider.EC2)
        driver = cls(self.configd["aws"]["credentials"]["EC2_ACCESS_KEY"], \
            self.configd["aws"]["credentials"]["EC2_SECRET_KEY"], \
            region = self.configd["aws"]["default"]["region"])

        # TODO : check local db before fetching
        # get flavor list and print
        sizes = driver.list_sizes()
        print(sizes)

        # TODO : parse list and store in db

        return
        
    def key_add(self):
        print("======Adding key=========")
        post_people()
        print("======key Added=========")
        return

    def node_create(self):
        # get driver
        cls = get_driver(Provider.EC2)
        driver = cls(self.configd["aws"]["credentials"]["EC2_ACCESS_KEY"], \
            self.configd["aws"]["credentials"]["EC2_SECRET_KEY"], \
            region = self.configd["aws"]["default"]["region"])

        # create node
        #node = driver.create_node(name='libcloud', size=size, image=image)
        print("The Node is ---------------")
        #print(node)
        return

