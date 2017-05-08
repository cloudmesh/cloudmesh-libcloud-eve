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
from libcloud.compute.types import NodeState
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
from cloudmesh.api.evemongo_client import Evemongo_client
#######################################################################
# GLOBALS

# collections
IMAGE = 'aws_image'
FLAVOR = 'aws_flavor'
LOCATION = 'aws_location'
NODE = 'aws_node'
VOLUME = 'aws_volume'
KEYPAIR = 'aws_keypair'
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
   
    def image_list(self):
        """List of amazon images 
        from mongodb
        :returns: image list objects
        :rtype: NoneType

        """
        #Fetch the list of images from db
        db_client = Evemongo_client()
        images = db_client.get(IMAGE)

        Console.ok(str(Printer.dict_table(images, order=['id', 'name', 'driver'])))

        return

    def image_refresh(self):
        """List of amazon images
        get store it in db
        :returns: None
        :rtype: NoneType

        """
        # get driver
        driver = self._get_driver()
        print("img refresh")
        # get image list and print
        images = driver.list_images()
        db_client = Evemongo_client()
       
        if len(images) == 0:
            print("Error in fetching new list ...Showing existing images")
            self.image_list()
        else:
            print("img refresh in esles")
            #r = db_client.delete(IMAGE)
            #print(images)
            print("storing in db")
            db_client.perform_delete(IMAGE)
            n = 0 ;
            e = {}
            for image in images:
                # parse flavors
                data = {}
                data['id'] = str(image .id)
                data['name'] = str(image.name)
                data['driver'] = str(image.driver)
                # store it in mongodb
                db_client.post(IMAGE, data)
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
        db_client = Evemongo_client()
        data = db_client.get(FLAVOR)

        Console.ok(str(Printer.dict_table(d, order=['id', 'name', 'ram', 'disk', 'price']))) 

        return
        
    def flavor_refresh(self):
        #get driver
        driver = self._get_driver()

        # get flavor list and print
        sizes = driver.list_sizes()
        #print(sizes)
        n = 1   
        e = {}
        db_client = Evemongo_client()
        db_client.delete(FLAVOR)
        for size in sizes:
            # parse flavors
            data = {}
            data['id'] = size .id
            data['name'] = size.name
            data['ram'] = size.ram
            data['disk'] = size.disk
            data['price'] = size.price

            e[n] = data
            n = n + 1
            # store it in mongodb
            db_client.post(FLAVOR, data)
            #print(data)    
        
        Console.ok(str(Printer.dict_table(e, order=['id', 'name', 'ram', 'disk', 'bandwidth', 'price'])))

        #print("successfully stored in db", r)
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
            Console.ok(str(Printer.dict_table(e, order=['uuid', 'name', 'state', 'public_ips', 'private_ips', 'provider'])))

        return nodes

   # def node_create_by_profile(self, IAM_PROFILE):
   #     
   #     IMAGE_ID =  self.configd["default"]['image']#'ami-0183d861'
   #     KEYPAIR_NAME = KEYPAIR_NAME_DEFAULT
   #     FLAVOR_ID = self.configd["default"]['flavor']
   #     # get driver
   #     driver = self._get_driver()

   #     sizes = driver.list_sizes()
   #     size = [s for s in sizes if s.id == FLAVOR_ID][0]
   #     image = driver.get_image(IMAGE_ID)
   #    
   #     # create node
   #     node = driver.create_node(name='ANOTHER', size=size, image=image,ex_iamprofile=IAM_PROFILE)
   #     
   #     print(node)

   #     return""" 
    
    def node_create_by_imageId(self, image_id, keypair_name, security_group_names, flavor_id):

        # get driver
        driver = self._get_driver()
        
        if image_id == '' :
            image_id =  self.configd["default"]['image']#'ami-0183d861'
         
        
        # Name of the existing keypair you want to use
        if keypair_name == '' :
            keypair_name = KEYPAIR_NAME_DEFAULT

        # A list of security groups you want this node to be added to
        if len(security_group_names) == 0 :
            security_group_names = ['default']
        
        if flavor_id == '':
            flavor_id = self.configd["default"]['flavor']

        sizes = driver.list_sizes()
        size = [s for s in sizes if s.id == flavor_id][0]
        
        image = driver.get_image(image_id)
       
        # create node
        node = driver.create_node(name='test1', size = size, image = image, ex_keyname = keypair_name, ex_securitygroup = security_group_names)
        #print("The Node is Created --------------- :: ",node)
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

        if bool(node) :
            #Push the created node in db
            print("Stored in db")
        return
    
    def node_reboot(self, node_uuid):
        
        driver = self._get_driver()
        #Take the running node list
        nodes = self.node_list(False)
        node = {}
        for n in nodes:
            if n.uuid == node_uuid:
                node = n
                break

        if bool(node) == False:
            print("No node found to reboot")
        else:
            if node.state == NodeState.RUNNING:
                isNodeReboot = node.reboot()
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
            print("Node is NodeState.REBOOTING---------------",isNodeReboot)
            if isNodeReboot :
                #Delete the node from db as well
                print("Node deleted from db")
        return        
        return

    def node_delete(self, node_uuid):
        # get driver
        #print("getting vm list")
        driver = self._get_driver()
        #List the running vm's

        
        #Take the running node list
        nodes = self.node_list(False)
        node = {}
        for n in nodes:
            if n.uuid == node_uuid:
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
        
    def keypair_create(self, key_pair):
        """
        Creates the key pair 
        required for node object
        """
        driver = self._get_driver()
        
        keypaorObj = driver.create_key_pair(key_pair)
        #print("keypair is created !",name)
        n = 0 ;
        e = {}
        # parse flavors
        data = {}
        data['name'] = str(keypaorObj.name)
        data['fingerprint'] = str(keypaorObj.fingerprint)
        data['driver'] = str(keypaorObj.driver.name)
        e[n] = data
        n = n + 1
          
        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint', 'driver'])))

        #Store the created keypair in db 
        #is created ! <KeyPair name=AWS2 fingerprint=b6:5b:7e:f1:82:35:9c:b4:d1:fd:71:9e:aa:20:83:7b:b3:c4:10:7a driver=Amazon EC2>

        return

    def keypair_delete(self, key_pair):
        """
        deletes the created key pair 
        """
        driver = self._get_driver()
        #Get the keypair object
        keyPairObj = self.keypair_get(key_pair)
        #delete the selected obj
        kpObj = driver.delete_key_pair(keyPairObj)
        #print("is deleted !",name)
        #delete the keypair from db 
        n = 0 ;
        e = {}
        # parse flavors
        data = {}
        data['name'] = str(kpObj.name)
        data['fingerprint'] = str(kpObj.fingerprint)
        data['driver'] = str(kpObj.driver.name)
        e[n] = data
        n = n + 1
          
        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint', 'driver'])))
        print("Is deleted !!")
        return
        
    def keypair_list(self):
        """
        List all the available key pair
        associated with account
        """
        driver = self._get_driver()
        
        key_pair_objs = driver.list_key_pairs()
        n =1
        e = {}
        for kp in key_pair_objs:
            data = {}
            data['name'] = kp.name
            data['fingerprint'] = kp.fingerprint
            data['driver'] = kp.driver
            e[n] = data
            n = n + 1
            
        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint','driver'])))
       
        return

    def keypair_get(self, key_pair):
        """
        Get the keypair object 
        associated with name
        """
        driver = self._get_driver()
        
        e = {}
        key_pair_obj = driver.get_key_pair(key_pair)
        data = {}
        data['name'] = key_pair_obj.name
        data['fingerprint'] = key_pair_obj.fingerprint
        data['driver'] = key_pair_obj.driver.name
        e[1] = data

        Console.ok(str(Printer.dict_table(e, order=['name', 'fingerprint','driver'])))
       
        return key_pair_obj

    def location_list(self, print_location):
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
        
        if print_location == True:
            Console.ok(str(Printer.dict_table(e, order=['id','name','country', 'availability_zone', 'zone_state','region_name','provider'])))
        
        return locations
        
    def key_add(self):
        #Some test functionality
        print("======add key=========")
        return
        
    def volume_create(self, volume_size, volume_name):
        #Some test functionality
        #db_client = Evemongo_client()
        db_client = Pymongo_client()
        #Some test functionality
        flavor_id = self.configd["default"]['flavor']
        location = self.configd["default"]['location']
        driver = self._get_driver()
        sizes = driver.list_sizes()
        size = [s for s in sizes if s.id == flavor_id][0]
        locations = self.location_list(False)
        if len(locations) == 0:
            print("Location not found!!")
        else:
            e = {}
            for loc in locations:
                if loc.availability_zone.region_name == location:
                    locObj = loc
                    #print(locObj)
                    storageVolume = driver.create_volume(volume_size, volume_name, location=locObj, snapshot=None)
                    #<StorageVolume id=vol-0e80356132e246a7b size=1 driver=Amazon EC2>
                    data = {}
                    data['id'] = storageVolume.id
                    data['size'] = storageVolume.size
                    data['driver'] = storageVolume.driver.name
                    e[0] = data
                    # store it in mongodb
                    db_client.post(VOLUME, data)
                    Console.ok(str(Printer.dict_table(e, order=['id', 'size','driver'])))
                else:
                    print("Location list does not match with selected location:  ", location)

                break
       
        #print("======Created volume ========= :: ",storageVolume)

        return

    def volume_list(self, printObjs):
            
        #Fetch the list of images from db
        db_client = Pymongo_client()
        volumes = db_client.get(VOLUME)
        
        e = {}
        n = 1
        for vol in volumes:
            e[n] = vol
            n = n + 1

        if printObjs == True :
            Console.ok(str(Printer.dict_table(e, order=['id', 'size','driver'])))

        return volumes

    def volume_list_refresh(self, print_objs):
        driver = self._get_driver()
        volumes = driver.list_volumes()
        e = {}
        n = 1
        for vol in volumes:
            #print(vol)
            data = {}
            data['id'] = vol.id
            data['size'] = vol.size
            data['driver'] = vol.driver.name
            e[n] = data
            n = n + 1

        if print_objs == True :
            Console.ok(str(Printer.dict_table(e, order=['id', 'size','driver'])))

        return volumes

    def volume_delete(self, volume_id):
        driver = self._get_driver()
        volume_objs = self.volume_list(False)
        e = {}
        for vol in volume_objs:
            if vol.id == volume_id :
                isDeleted = driver.destroy_volume(vol)
                #print(vol)
                data = {}
                data['id'] = vol.id
                data['size'] = vol.size
                data['driver'] = vol.driver.name
                e[1] = data
                break 

        Console.ok(str(Printer.dict_table(e, order=['id', 'size', 'driver'])))
        print("Is deleted - ", isDeleted)
        return

    def volume_attache(self, node_id, volume_id):
        driver = self._get_driver()
        node = ''
        volume = ''
        nodes = self.node_list(False)
        if len(nodes) == 0:
            #No Node available to attache volume
            print("pass -No Node")
            Console.warning("No Node available to attache volume")
        else :
            if NODE_ID == '':
                #get the default 0th node from list
                node = nodes[0]
            else:
                for nd in nodes :
                    if nd.id == NODE_ID:
                        #attache the default/ 0th location node 
                        node = nd
                        break
        
        volumes = self.volume_list(False)
        if len(volumes) == 0:
            #No Node available to attache volume
            Console.warning("No Volumes available")
        else :
            for vol in volumes :
                if vol.id == volume_id:
                    #attache the default/ 0th location node 
                    volume = vol
                    break
        if node and volume :
            isVolumeAttached = driver.attach_volume(node, volume, device=None)
            Console.ok("Is volume attached - ", isVolumeAttached)
        else:
            Console.info("Unable to attached volume to node,  please verify your input")

        return 

    def drop_collections(self):
        db_client = Evemongo_client()
        #Some test functionality
        print("======Delete db=========")
        db_client.delete_database(FLAVOR)
        return
