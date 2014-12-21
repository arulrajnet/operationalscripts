# -*- coding: utf-8 -*-

__author__ = 'arul'

from fabric.api import *
from fabric.contrib.files import *
import sys

env.use_ssh_config = True

"""
Python Script to setup Anomaly environmental using TOR and Privoxy
"""

class SystemInfo():

    OS_ARCH = OS_NAME = OS_VERSION = None

    def __init__(self):
        self.__get_os_info__()

    def __get_os_info__(self):
        self.OS_ARCH = run(r"uname -m | sed 's/x86_//;s/i[3-6]86/32/'")

        if exists('/etc/lsb-release'):
            with prefix(". /etc/lsb-release"):
                self.OS_NAME = run("echo -n $DISTRIB_ID")
                self.OS_VERSION = run("echo -n $DISTRIB_RELEASE")
        elif exists('/etc/debian_version'):
            self.OS_NAME = "Debian"
        elif exists('/etc/redhat-release'):
            self.OS_NAME = "Redhat"
        else:
            self.OS_NAME = run("uname -s")
            self.OS_VERSION = run("uname -r")

def __install_deps_debian__():
    run("sudo apt-get update")
    run("sudo apt-get install tor -y")
    run("sudo apt-get install privoxy -y")

def __install_deps_redhat__():
    print __is_repo_present__("epel")
    if not __is_repo_present__("epel"):
        with cd("/tmp"):
            # TODO install the correct version, arch of rpm file.
            run("wget http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm")
            run("rpm -Uvh epel-release*rpm")
    run("yum install tor -y")
    run("yum install privoxy -y")
    run("yum install python-devel python-pip unzip -y")

def __is_repo_present__(reponame):
    repolist = run("yum repolist %s | grep repolist" % reponame)
    import re
    match = re.search("[0-9,]+", repolist)
    if match:
        repo_length = match.group().replace(",", "")
        if int(repo_length) > 0:
            return True
    return False

def __tor_config__():
    with cd("/etc/tor/"):
        # run("cp torrc.sample torrc")
        # Here hashed password is "Pas`sword12"
        torrc_config = """
        ControlPort 9051
        HashedControlPassword 16:79C8734C30ABD944604B839CEAF5AAC0F61AA500832A4B8BB9BC8042A5
        """
        uncomment("torrc", r"ControlPort\s\+9051")
        uncomment("torrc", r"HashedControlPassword\s\+16")
    with cd("/etc/privoxy"):
        uncomment("config", r"forward-socks5\s\+\/\s\+127.0.0.1:9050")
        uncomment("config", r"forward\s\+192")
        uncomment("config", r"forward\s\+10")
        uncomment("config", r"forward\s\+127")

def __set_system_proxy__(sysinfo):
    """
    :return:
    """

    proxy_string = """
    http_proxy="http://127.0.0.1:8118"
    https_proxy="http://127.0.0.1:8118"
    ftp_proxy="http://127.0.0.1:8118"
    HTTP_PROXY="http://127.0.0.1:8118"
    HTTPS_PROXY="http://127.0.0.1:8118"
    FTP_PROXY="http://127.0.0.1:8118"
    _JAVA_OPTIONS="-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8118"
    """

    if sysinfo.OS_NAME.lower() in ["debian", "ubuntu"]:
        run('touch /etc/environment')
        append("/etc/environment", proxy_string)
    elif sysinfo.OS_NAME.lower() in ["redhat", "centos", "fadora"]:
        run('touch /etc/profile.d/proxy.sh')
        proxy_string = proxy_string + "export http_proxy https_proxy ftp_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY _JAVA_OPTIONS"
        append("/etc/profile.d/proxy.sh", proxy_string)

def __setup_renew_ip__():
    pass

def install():
    sysinfo = SystemInfo()
    print "Name : %s, Version : %s, Arch : %s" % (sysinfo.OS_NAME, sysinfo.OS_VERSION, sysinfo.OS_ARCH)

    if sysinfo.OS_NAME.lower() in ["debian", "ubuntu"]:
        __install_deps_debian__()
    elif sysinfo.OS_NAME.lower() in ["redhat", "centos", "fadora"]:
        __install_deps_redhat__()

    __tor_config__()

    run('sudo /etc/init.d/tor restart')
    run('sudo /etc/init.d/privoxy restart')
    run('curl -v --socks5-hostname localhost:9050 http://curlmyip.com')
    __set_system_proxy__(sysinfo)
    run('curl -s http://curlmyip.com')
    __setup_renew_ip__()

if __name__ == '__main__':
    print "Usage: fab -H hostname -f %s install" % sys.argv[0]