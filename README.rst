

AWS Client
==============================================================

AWS client is a simple client to enable access to AWS cloud from a command
shell. It uses libcloud EC2 driver to connecto to the cloud, and mongodb to
store various environment related information. Pymongo is used for database
connectivity. The functionalities supported are list different images and
flavors, and create and delete vm nodes. The source code is based on 
componenets from cloudmesh.common and cloudmesh.cmd5.

Requirements
------------

* Python 2.7.13
* Ubuntu 16.04/ MAC OSX EL Capitan
* AWS account

Installation from source
------------------------

Setup a virtual environment using virtualenv.

virtualenv::

    virtualenv ~/AWSENV

Activate the virtual environment::

    source ~/AWSENV/bin/activate

Now you need to get two source directories apart from . We assume you place them in
~/github::

    mkdir ~/github
    cd ~/github
    git clone https://github.com/cloudmesh/cloudmesh.cmd5.git
    git clone https://github.com/cloudmesh/cloudmesh.rest.git
    git clone https://github.com/cloudmesh/cloudmesh.evegenie.git
    git clone https://github.com/cloudmesh/cloudmesh.aws.git


To install them simply to the following::

    cd ~/github/cloudmesh.aws
    make source

Configuration
------------------

The AWS credentials are read from configuration file config/aws.yml. It also
contains the default configuration for a creating a vm node.

You will have to do the following modifications to match you machine::

    credentials:
      EC2_ACCESS_KEY: 'ACCESS KEY'
      EC2_SECRET_KEY: 'SECRET KEY'
    default:
      image: 'IMAGE ID'
      size: 'SIZE ID'
      region: 'REGION'

The mongodb configuration and collection schema are stored in config/specification/all.settings.py.
The rest srvices can be started using that by following command::

    make rest


The AWS client setup is now ready to be used. Whether to fetch the information from the cloud over 
the network, or from the database stored locally, can be set by setting 'refresh' switch.::

    cms aws refresh on


