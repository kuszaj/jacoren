# -*- coding: utf-8 -*-

"""Basic platform information."""

import platform


#: Platform version tuple (major, minor, release)
VERSION = tuple(platform.release().split('.', 3))
