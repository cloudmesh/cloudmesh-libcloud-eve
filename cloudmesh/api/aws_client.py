#!/usr/bin/env python
# Docker class to connect to docker server box and perform docker operations
from __future__ import print_function
import cloudmesh
#import libcloud
import os
#import requests
#import json
import sys
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
#import yaml

class Aws(object):
    def __init__(self):
        #self.client = docker.from_env()
        #f = open("cloudmesh/api/aws.yml");
        #self.Constants = yaml.safe_load(f)
        #f.close()
        #print(self.Constants["user_details"]["ACCESS_ID"])
        cls = get_driver(Provider.EC2)
        global driver
        driver = cls("ACCESS_ID", "SECRET_KEY", region="us-west-1")
       
        print("TODO")

    def images_list(self):
        """List of amazon images
        
        :returns: None
        :rtype: NoneType

        """
        #driver = cls(self.Constants["user_details"]["ACCESS_ID"], self.Constants["user_details"]["SECRET_KEY"], region="us-west-1")

        images = driver.list_images()
        print("List of images--------------")
        print(images)
        #size = [s for s in sizes if s.id == 'performance1-1'][0]
        #image = [i for i in images if 'Ubuntu 12.04' in i.name][0]

        #node = driver.create_node(name='libcloud', size=size, image=image)
        print("The Node is ---------------")
        #print(node)
        return

    def flavor_list(self):
        print("=============SIZES/flavors============")
        sizes = driver.list_sizes()
        print(sizes)

        return
        