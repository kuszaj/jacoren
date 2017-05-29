# -*- coding: utf-8 -*-

"""
Simple cross-platform machine status retriever.

jacoren is a cross-platform package for retrieving basic information
about machine and its CPUs, memory and disks in a form of handy
constants and dictionaries.

Package can also be run as a script. This allows user to create
a simple RESTful API for receiving data through HTTP requests.
"""

import jacoren.platform
import jacoren.cpu


#:
#: Package info
#:
__version__ = '0.0.1'
__title__ = 'jacoren'
__description__ = ''
__author__ = 'Piotr Kuszaj'
__author_email__ = 'peterkuszaj@gmail.com'
__license__ = 'MIT'
