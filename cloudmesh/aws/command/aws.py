from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.api.aws_client import Aws
import os
from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.default import Default

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
        v = Default()
        print(v['aws','refreshImage'])
        print(v['aws','refreshFlavor'])
        print(v['aws','refreshVm'])
        v.close()

        if arguments.default and arguments.image  :
            value = arguments.ON 
            v = Default()
            v['aws','refreshImage'] = value
            v.close()
            return "" 
            
        if arguments.image and arguments.list :
            aws.images_list()
            return
            
        if arguments.image and arguments.refresh :
            aws.images_refresh()
            return

        if arguments.flavor and arguments.list :
            aws.flavor_list()
            return

        if arguments.flavor and arguments.refresh :
            aws.flavor_refresh()
            return

        if arguments.vm and arguments.list :
            aws.node_list()
            return

        if arguments.vm and arguments.boot :
            aws.node_create()
            return
 
        if arguments.vm and arguments.delete :
            aws.node_delete()
            return

        if arguments.add and arguments.key :
            aws.key_add()
            return

        if arguments.drop and arguments.collections :
            aws.drop_collections()
            return
        
          