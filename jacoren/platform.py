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


def platform_users():
    """
    Return list of logged users.

    Function returns list of OrderedDict instances:

        [
            ...
            {
                'name': <user's name>,
                'logged_time': <time after logging in seconds>,
            }
            ...
        ]
    """
    now = time.time()
    users = [OrderedDict([
        ('name', u.name),
        ('logged_time', int(round(now - _boot_time))),
    ]) for u in psutil.users()]

    return users


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
            'uptime': <uptime in seconds>,
            'users': <users currently logged in>,
        }

    On some platforms, minor version and release might not be
    available.
    """
    return OrderedDict((
        ('os', OS),
        ('version', VERSION),
        ('uptime', platform_uptime()),
        ('users', platform_users()),
    ))
