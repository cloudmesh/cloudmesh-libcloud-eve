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
            aws vm list [--format=FORMAT]
            aws add key
            aws vm boot 
            aws vm delete
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
            aws.node_list()
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.boot :
            aws.node_create()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
 
        if arguments.vm and arguments.delete :
            aws.node_delete()
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
        
          
