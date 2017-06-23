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


def _tdiff(t1, t2):
    """Return time difference t1-t2 as a rounded integer."""
    return int(round(t1 - t2))


def platform_uptime():
    """
    Return uptime in seconds.

    :Example:

    >>> import jacoren
    >>> jacoren.platform.platform_uptime()
    13881

    :return: Platform uptime
    :rtype: int
    """
    return _tdiff(time.time(), _boot_time)


def platform_users():
    """
    Return list of logged users.

    Function returns list of OrderedDict instances::

        [
            ...
            {
                'name': <user's name>,
                'logged_time': <time after logging in seconds>,
            }
            ...
        ]

    :Example:

    >>> import jacoren
    >>> jacoren.platform.platform_users()
    [OrderedDict([('name', 'some_user'),
                  ('logged_time', 19242)]),
     OrderedDict([('name', 'another_user'),
                  ('logged_time', 6176)])]

    :return: List of OrderedDict instancess with user data
    :rtype: list
    """
    now = time.time()

    _useen = set()
    _useen_add = _useen.add

    #: Avoid duplicate usernames
    users = [OrderedDict([
        ('name', u.name),
        ('logged_time', _tdiff(now, u.started)),
    ]) for u in psutil.users()
       if not (u.name in _useen or _useen_add(u.name))]

    return users


def platform():
    """
    Return basic information about platform.

    Function returns OrderedDict instance::

        {
            'os': <OS name>
            'version': [
                <major version>,
                <minor version>,
                <release>,
                <revision>
            ],
            'uptime': <uptime in seconds>,
            'users': <users currently logged in>,
        }

    On some platforms, minor version, release and revision might not be available.

    :Example:

    >>> import jacoren
    >>> jacoren.platform.platform()
    OrderedDict([
        ('os', 'Linux'),
        ('version', ('3', '7', '5', '201.fc18.x86_64')),
        ('uptime', 17411),
        ('users', [
            OrderedDict([('name', 'some_user'),
                         ('logged_time', 17411)]),
            OrderedDict([('name', 'another_user'),
                         ('logged_time', 11814)])
        ])
    ])

    :return: Basic platform information
    :rtype: OrderedDict
    """
    return OrderedDict((
        ('os', OS),
        ('version', VERSION),
        ('uptime', platform_uptime()),
        ('users', platform_users()),
    ))
