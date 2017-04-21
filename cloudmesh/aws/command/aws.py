from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.api.aws_client import Aws
import os
from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.StopWatch import StopWatch


class AwsCommand(PluginCommand):

    @command
    def do_aws(self, args, arguments):
        """
        ::

          Usage:
            aws api URL
            aws image list [--format=FORMAT]
            aws flavor list [--format=FORMAT]
            aws vm list [--format=FORMAT]
            aws add key
            aws vm boot 
            
  
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
            return

        if arguments.flavor and arguments.list :
            aws.flavor_list()
            return

        if arguments.vm and arguments.list :
            # aws.vm_list()
            return

        if arguments.add and arguments.key :
          aws.key_add()
          return