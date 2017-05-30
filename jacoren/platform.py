# -*- coding: utf-8 -*-

"""Basic platform information."""

import platform


#: Platform OS
OS = platform.system()

#: Platform version tuple (major, minor, release)
VERSION = tuple(platform.release().split('.', 3))


def platform():
    return {
        'os': OS,
        'version': VERSION,
    }
