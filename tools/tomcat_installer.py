# -*- coding: utf-8 -*-
from fabric.api import *

__author__ = 'arul'

"""
Installation Script of Tomcat 6 / 7 using fabric
"""

@task(default=True)
@with_settings(hide('stdout'), warn_only=True)
def install():
    pass

if __name__ == '__main__':
    pass