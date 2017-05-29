# -*- coding: utf-8 -*-

import platform


#: Platform version tuple (major, minor, release)
VERSION = tuple( platform.release().split('.', 2) )
