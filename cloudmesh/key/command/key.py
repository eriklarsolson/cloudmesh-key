from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.key.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
import subprocess
from cloudmesh.common.parameter import Parameter
import os

class KeyCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_key(self, args, arguments):
        """
        ::

          Usage:
                key gatherkeys --ips=192.168.1.[50-55] --master=192.168.1.19

          This command does some useful things.

          Arguments:
              --ips: IP range of workers you'd like to connect to
              --master: IP of master
        """
        ips = None if not arguments['--ips'] else Parameter.expand(arguments['--ips'])
        master = arguments['--master']
        VERBOSE(arguments)
        m = Manager()

        #TODO - Make sure they set the master parameter
        if arguments.gatherkeys:
            os.system("rm -rf /home/pi/keys")
            os.system("mkdir /home/pi/keys")
            os.system("rm /home/pi/.ssh/authorized_keys")
            for i in ips:
                ip = i

                #Generate key for worker
                command = "ssh " + ip + " sudo chown pi .ssh"
                os.system(command)
                command = "ssh " + ip + " sudo chown pi .ssh/authorized_keys"
                os.system(command)
                command = "ssh " + ip + " ssh-keygen"
                os.system(command) 

                #Copy public key back to master's authorized keys file
                command = "scp pi@" + ip + ":/home/pi/.ssh/id_rsa.pub /home/pi/keys/" + ip + "pk"
                os.system(command)
                command = "cat /home/pi/keys/" + ip + "pk >> /home/pi/.ssh/authorized_keys"
                os.system(command)

            os.system("cp /home/pi/.ssh/authorized_keys /home/pi/keys/")
            for i in ips:
                ip = i
                #Redistribute all public keys (including master) back to worker's authorized keys
                command = "scp /home/pi/keys/authorized_keys pi@" + ip + ":/home/pi/public_keys"
                os.system(command)

                #Copy over master public key
                command = "scp /home/pi/.ssh/id_rsa.pub pi@" + ip + ":/home/pi/master_pk"
                os.system(command)
                command = "ssh " + ip + " 'cat /home/pi/master_pk >> /home/pi/public_keys'"
                os.system(command) 
                command = "ssh " + ip + " cp /home/pi/public_keys /home/pi/.ssh/authorized_keys"
                os.system(command)

                #Delete public_keys & master_pk files that was transfered over after contents of it is put in authorized_keys
                os.system("ssh " + ip + " rm /home/pi/public_keys")
                os.system("ssh " + ip + " rm /home/pi/master_pk")

           #TODO - Do I need to delete the authorized_keys file I saved to /home/pi/keys on master?

        return ""
