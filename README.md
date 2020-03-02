Documentation
=============


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-bar.svg?branch=master)](https://travis-ci.org/TankerHQ/cloudmesn-bar)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-bar.svg)](https://pypi.org/project/cloudmesh-bar)

[![image](https://img.shields.io/pypi/v/cloudmesh-bar.svg)](https://pypi.org/project/cloudmesh-bar/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-bar.svg)](https://github.com/TankerHQ/python-cloudmesh-bar/blob/master/LICENSE)

see cloudmesh.cmd5

* https://github.com/cloudmesh/cloudmesh.cmd5

# Using Cloudmesh Key
Cloudmesh key is a command that generates public/private keys for each worker & gathers them on the master to redistribute back to each worker's authorized_keys in ssh. This will allow each worker to connect to every other worker and the master.

## Notes
This tool uses ssh to each worker a lot and wants you to input your ssh password each time you connect.

You can get around this by using the ssh-add command.
```bash
    exec ssh-agent bash
    ssh-add
```
 

## How-to
```bash
    cms key gatherkeys --ips=192.168.1.[50-55] --master=192.168.1.19
```

* The --ips option specifies the range of ips for your workers
* The --master option specifies the master's ip

