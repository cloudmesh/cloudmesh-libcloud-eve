from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.api.aws_client import Aws
import os
from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.default import Default

from cloudmesh.common.StopWatch import StopWatch

#Console printing packages
from cloudmesh.common.console import Console

class AwsCommand(PluginCommand):

    @command
    def do_aws(self, args, arguments):
        """
        ::

          Usage:
            aws refresh ON
            aws api URL
            aws default image ON
            aws image refresh [--format=FORMAT]
            aws image list [--format=FORMAT]
            aws flavor [refresh] [--format=FORMAT]
            aws flavor list [--format=FORMAT]
            aws vm boot 
            aws vm delete
            aws vm list [--format=FORMAT]
            aws keypair create NAME
            aws keypair delete NAME
            aws keypair list
            aws keypair get NAME
            aws location list
            aws add key
            aws drop collections

          Arguments:
            ON       set configuration to on/off 
            NAME     The name of the aws
            URL      URL of aws API
            FORMAT   The format in which to print the data

          Options:
            -v       verbose mode

          Description:
            Manages a virtual aws on a cloud

            to complete the command see the man page of cm boot help
        """
        v = Default()
        if v['aws', 'refresh'] != None:
            refresh = v['aws', 'refresh']
        v.close()
       
   
        if arguments.refresh and arguments.ON:
            v = Default()
            v['aws', 'refresh'] = arguments.ON
            v.close()

        """ v = Default()
        if v['aws', 'keypair'] != None:
            print("assign the name")
            NAME = v['aws', 'keypair']
        v.close()"""
        
        """if arguments.create and arguments.NAME :
           print(" create new obj :: ",arguments.NAME )
           v = Default()
           v['aws', 'keypair'] = arguments.NAME
           v.close()"""
   
        # Initialize timer and aws client 
        stopwatch = StopWatch()
        stopwatch.start('E2E')
        aws = Aws()

        if arguments.image: 
            if arguments.refresh or refresh:
                aws.images_refresh()
            else:
                aws.images_list()

            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.flavor: 
            if arguments.refresh or refresh:
                aws.flavor_refresh()
            else:
                aws.flavor_list()

            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.list :
            aws.node_list(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.boot :
            SEL_IMAGE_ID ='ami-0183d861' #ami-d85e75b0
            KEYPAIR_NAME = 'test1'
            SECURITY_GROUP_NAMES = []
            FLAVOR_ID = ''
            aws.node_create(SEL_IMAGE_ID,KEYPAIR_NAME,SECURITY_GROUP_NAMES,FLAVOR_ID)
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
 
        if arguments.vm and arguments.delete :
            NODE_UUID = '61671593de3681e7de6bd6c6e33f5a4857110864'
            aws.node_delete(NODE_UUID)
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.keypair and arguments.create and arguments.NAME:
            KEY_PAIR = arguments.NAME #"AWS3"
            aws.keypair_create(KEY_PAIR)
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.keypair and arguments.delete and arguments.NAME:
            KEY_PAIR = arguments.NAME # "AWS1"
            aws.keypair_delete(KEY_PAIR)
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.keypair and arguments.list :
            aws.keypair_list()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.keypair and arguments.get and arguments.NAME :
            KEY_PAIR =  arguments.NAME #"AWS2"
            aws.keypair_get(KEY_PAIR)
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
            

        if arguments.add and arguments.key :
            aws.key_add()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.drop and arguments.collections :
            aws.drop_collections()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.location and arguments.list :
            aws.location_list()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
          
