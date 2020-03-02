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
        if arguments.gatherkeys and master != "":
            os.system("rm -rf /home/pi/keys")
            os.system("mkdir /home/pi/keys")
            os.system("rm /home/pi/.ssh/authorized_keys")
            for i in ips:
                ip = i

                #When burning workers using cm-pi-burn, it makes .ssh owned by root instead of pi
                #This fixes permissions if it needs to be fixed
                command = "ssh " + ip + " sudo chown pi .ssh"
                os.system(command)
                command = "ssh " + ip + " sudo chown pi .ssh/authorized_keys"
                os.system(command)

                #Generate key for worker
                command = "ssh " + ip + " ssh-keygen"
                os.system(command) 

                #Copy public key back to master's authorized keys file
                command = "scp pi@" + ip + ":/home/pi/.ssh/id_rsa.pub /home/pi/keys/" + ip + "pk"
                os.system(command)
                command = "cat /home/pi/keys/" + ip + "pk >> /home/pi/.ssh/authorized_keys"
                os.system(command)

            #Once all public keys gathered, this is the redistribution step back to workers
            for i in ips:
                ip = i
                #Copy over authorized keys file from master that includes all worker's public keys
                command = "scp /home/pi/.ssh/authorized_keys pi@" + ip + ":/home/pi/public_keys"
                os.system(command)

                #Copy over master public key to worker
                command = "scp /home/pi/.ssh/id_rsa.pub pi@" + ip + ":/home/pi/master_pk"
                os.system(command)

                #Copy master public key into file with all other worker  public keys
                command = "ssh " + ip + " 'cat /home/pi/master_pk >> /home/pi/public_keys'"
                os.system(command) 

                #Write over worker's authorized_keys with file containing all worker's and master's public key
                command = "ssh " + ip + " cp /home/pi/public_keys /home/pi/.ssh/authorized_keys"
                os.system(command)

                #Delete public_keys & master_pk tmp files
                os.system("ssh " + ip + " rm /home/pi/public_keys")
                os.system("ssh " + ip + " rm /home/pi/master_pk")

        return ""
