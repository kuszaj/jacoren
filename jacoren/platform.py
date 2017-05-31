# -*- coding: utf-8 -*-

"""Basic platform information."""

import time
import psutil
import platform
from collections import OrderedDict


#: Platform OS
OS = platform.system()

#: Platform version tuple (major, minor, release)
VERSION = tuple(platform.release().split('.', 3))

#: Boot time
_boot_time = psutil.boot_time()


def platform_uptime():
    """Return uptime in seconds."""
    return int(round(time.time() - _boot_time))


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
            'uptime': <uptime in seconds>
        }

    On some platforms, minor version and release might not be
    available.
    """
    return OrderedDict((
        ('os', OS),
        ('version', VERSION),
        ('uptime', platform_uptime()),
    ))
