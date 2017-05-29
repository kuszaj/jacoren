# -*- coding: utf-8 -*-

import platform
import psutil


#:
#: Package info
#:
__version__ = '0.0.1'
__title__ = 'jacoren'
__description__ = ''
__author__ = 'Piotr Kuszaj'
__author_email__ = 'peterkuszaj@gmail.com'
__license__ = 'MIT'

#:
#: Platform
#:

#: Platform version tuple (major, minor, release)
PLATFORM_VERSION = platform.release().split('.')
if len(PLATFORM_VERSION) > 3:
    PLATFORM_VERSION = (PLATFORM_VERSION[0],  # major
                        PLATFORM_VERSION[1],  # minor
                        PLATFORM_VERSION[2:]) # release
else:
    PLATFORM_VERSION = tuple(PLATFORM_VERSION)
