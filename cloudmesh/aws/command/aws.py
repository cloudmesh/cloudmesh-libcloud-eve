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
            aws image list
            aws flavor list
            aws container create NAME IMAGE
            aws container start NAME
            aws container stop NAME
            aws container list
            aws container delete NAME
            aws container attach NAME
            aws container pause NAME
            aws container unpause NAME
            aws process config CNAME

  
          Arguments:
            NAME     The name of the aws
            CLOUD    The name of the cloud on which the virtual aws
                     is to be deployed
            IMAGE    Docker server images
            URL      URL of aws API
            CNAME    Config File Name

          Options:
            -v       verbose mode

          Description:
            Manages a virtual aws on a cloud

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