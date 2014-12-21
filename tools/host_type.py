# -*- coding: utf-8 -*-

__author__ = 'arul'

from fabric.api import *

env.use_ssh_config = True

def host_type():
    """
    How to use:
    fab -H localhost host_type -f host_type.py
    :return:
    """
    run('uname -s')