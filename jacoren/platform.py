# -*- coding: utf-8 -*-

import platform


#: Platform version tuple (major, minor, release)
VERSION = platform.release().split('.')
if len(VERSION) > 3:
    VERSION = (VERSION[0],  # major
               VERSION[1],  # minor
               VERSION[2:]) # release
else:
    VERSION = tuple(VERSION)
