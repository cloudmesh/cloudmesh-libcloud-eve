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
            aws api URL
            aws default image ON
            aws image list [--format=FORMAT]
            aws image refresh
            aws flavor list [--format=FORMAT]
            aws flavor refresh
            aws vm list [--format=FORMAT]
            aws add key
            aws vm boot 
            aws vm delete
            aws drop collections
          Arguments:
            NAME     The name of the aws
            URL      URL of aws API
            FORMAT   The format in which to print the data

          Options:
            -v       verbose mode

          Description:
            Manages a virtual aws on a cloud

            to complete the command see the man page of cm boot help
        """

        stopwatch = StopWatch()
        stopwatch.start('E2E')
        aws = Aws()
            
        if arguments.image and arguments.list :
            aws.images_list()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
            
        if arguments.image and arguments.refresh :
            aws.images_refresh()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.flavor and arguments.list :
            
            aws.flavor_list()
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.flavor and arguments.refresh :
            aws.flavor_refresh()
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
        
          