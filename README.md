operationalscripts
==================

Collection of scripts to automate your *nix environment.

Most of the installation scripts written using python [Fabric] module. So you have to setup the Fabric in your local machine.

__Install Fabric__

Fabric inside they are using Paramiko for remote ssh. Paramiko using pycryto. So you have to install pycryto first. 

_In Windows_

* Download the exe from http://www.voidspace.org.uk/python/modules.shtml#pycrypto
* Then install 

_In Linux_

* Ubuntu `sudo apt-get install python-dev`
* CentOS `sudo yum install python-devel`

```
pip install fabric
```













[Fabric]: https://github.com/fabric/fabric/ "Fabric"
