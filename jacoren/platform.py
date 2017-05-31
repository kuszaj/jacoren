# -*- coding: utf-8 -*-

"""Basic platform information."""

import platform
from collections import OrderedDict


#: Platform OS
OS = platform.system()

#: Platform version tuple (major, minor, release)
VERSION = tuple(platform.release().split('.', 3))


def platform():
    """
    Return basic information about platform.

    Function returns OrderedDict instance:

        {
            'os': <OS name>
            'version': [
                <major version>,
                <minor version>,
                <release>
            ],
        }

    On some platforms, minor version and release might not be
    available.
    """
    return OrderedDict((
        ('os', OS),
        ('version', VERSION),
    ))
