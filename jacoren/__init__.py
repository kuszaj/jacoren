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
import jacoren.memory

from .__version__ import (
    __version__,
    __title__,
    __description__,
    __author__,
    __author_email__,
    __license__,
    __all__,
)
