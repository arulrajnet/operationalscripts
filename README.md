operationalscripts
==================

Operationalscripts is the collection of python / shell / perl scripts. The main goal of this project to help DevOps to automate the `Application Deployment` in any flavor of *nix. 

Most of the installation scripts written using python [Fabric] module. So you have to setup the Fabric in your local machine.

### Install Fabric

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

### Applications Scripts

| Description        | Script           | Documentation  |
| ------------- |:-------------:| -----:|
| Setup Tor Anomaly Network with Privoxy      | [tor_installer.py][tor_installer.py] | [tor_installer.md][tor_installer.md] |


### Deamons

| Description        | Deamon           | Documentation  |
| ------------- |:-------------:| -----:|
| Tomcat      | [tomcat_daemon.sh][tomcat_daemon.sh] | [tomcat_daemon.md][tomcat_daemon.md] |
| Red5      | [red5_daemon.sh][red5_daemon.sh] | [red5_daemon.md][red5_daemon.md] |

### Road Map

* Create base fabric abstract scripts to get SystemInformation, Repository. It should support Redhat and Debian family.
* Each installation script should have documentation to use and blog about manual installation and auto installation. 
* Each installation script have setup defined tasks such as prequestics, installation and verify
* Getting user inputs. Then before installation ask for conformation
* Sudo handling
* Get systeminfo like platform module in python. check platform.dist()



[Fabric]: https://github.com/fabric/fabric/ "Fabric"
[tor_installer.py]: https://github.com/arulrajnet/operationalscripts/blob/master/tools/tor_installer.py "TOR installer"
[tor_installer.md]: https://github.com/arulrajnet/operationalscripts/blob/master/tools/tor_installer.md "TOR Installer Documentation"
[tomcat_daemon.sh]: https://github.com/arulrajnet/operationalscripts/blob/master/daemons/tomcat_daemon.sh "Tomcat Service Deamon"
[tomcat_daemon.md]: https://github.com/arulrajnet/operationalscripts/blob/master/daemons/tomcat_daemon.md "Tomcat Deamon Documentation"
[red5_daemon.sh]: https://github.com/arulrajnet/operationalscripts/blob/master/daemons/red5_daemon.sh "Red5 Service Deamon"
[red5_daemon.md]: https://github.com/arulrajnet/operationalscripts/blob/master/daemons/red5_daemon.md "Red5 Deamon Documentation"