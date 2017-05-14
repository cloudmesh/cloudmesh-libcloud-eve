Commands
======================================================================
refresh
----------------------------------------------------------------------
Command - refresh::

    Usage:
        refresh ON

    Arguments:
        ON  The value to set 'refresh' to. [default: off]

    Setting 'refresh' to on makes the list commands to fetch the
    information from cloud instead of local datastore.

image
----------------------------------------------------------------------
Command - image::

    Usage:
        image [refresh] [--format=FORMAT]
        image list [--format=FORMAT]

    Options:
       --format=FORMAT  The output format [default: table]

    Description:
        Prints the list of image configurations available on cloud.
        When either refresh is specified or global variable 'refresh'
        is set to on, the list is fetched from the cloud and updated
        in the database.

flavor
----------------------------------------------------------------------
Command - flavor::

    Usage:
        flavor [refresh] [--format=FORMAT]
        flavor list [--format=FORMAT]

    Commands:

          list   Fetches the information from local datastore. 

    Options:
       --format=FORMAT  The output format [default: table]


vm
----------------------------------------------------------------------
Command - vm::

    Usage:
        vm boot NODE_NAME [--image_id=IMAGE_ID] [--flavor_id=FLAVOR_ID] [--keypair_name=KEYPAIR_NAME] [--sec_grp_name=SEC_GRP_NAMES]
        vm reboot NODE_NAME
        vm delete NODE_NAME
        vm list [--format=FORMAT]
        vm refresh [--format=FORMAT]

    Commands:

        boot    Creates a node with the name specified. 
        reboot  Reboots the node identified by the name provided.
        delete  Deletes the node specified.
        list    Lists the vm along with their state.
        refresh Fetches vm information from the cloud and updates database.

    Arguments:
        NODE_NAME Name of the vm node to identify it.

    Options:
        --format=FORMAT                 The output format [default: table].
        --image_id=IMAGE_ID             Id of the image to boot.
        --flavor_id=FLAVOR_ID           Size of the image.
        --keypair_name=KEYPAIR_NAME     Keypair to use.
        --sec_grp_name=SEC_GRP_NAMES    Security group of the vm.    

keypair
----------------------------------------------------------------------
Command - keypair::

    Usage:
        keypair create NAME
        keypair delete NAME
        keypair list
        keypair refresh
        keypair get NAME

    Commands:

        create      Creates a keypair with the name specified. 
        delete      Deletes the keypair identified by the name specified.
        list        Lists available keypairs stored in the database.
        refresh     Fetches the keypair information from cloud and updates local database.
        get         TODO: 


    Arguments:
      NAME    The name of the keypair to identify it with.


location
----------------------------------------------------------------------
Command - location::

        Usage:
            location list
            location refresh

        Commands:

            list    Lists the locations available on cloud to deploy nodes.
            refresh Fetches the list of locations from cloud and updates local database.


volume
----------------------------------------------------------------------
Command - volume::

    Usage:
        volume create VOLUME_NAME
        volume list
        volume refresh
        volume delete VOLUME_NAME
        volume attach VOLUME_NAME

    Commands:

        create      Creates a new storage volume with the name specified. 
        delete      Deletes the volume identified by the name specified.
        list        Lists available volumes stored in the database.
        refresh     Fetches the volumes information from cloud and updates local database.
        attach      TODO: 

    Arguments:

        VOLUME_NAME    The name of the volume to associate it with.

