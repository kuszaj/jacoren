# -*- coding: utf-8 -*-

"""Utilities for memory info."""

import psutil
from collections import OrderedDict


def memory_ram(percent=False):
    """
    Return memory metrics.

    Function returns a OrderedDict:

        {
            'total': <total memory>,
            'available': <available memory>,
            'used': <used memory>,
            'free': <free memory>,
            ...
        },

    Above fields are available for every platform.
    If percent is true, all fields (except total) and given in
    percents. Otherwise, they are given in bytes.
    Note: used and free can be calculated differently and do not
    necessarily will match with (total-free) and (total-used). It is
    recommended to use mostly total and available fields.

    Additionally, there are other, platform-specific fields:

    Linux:
        * active - currently or very recently used
        * inactive - marked as not used
        * buffers - cache for things like file system metadata
        * cached - cache for various other things
        * shared - shared among multiple processes
    BSD:
        * active - currently or very recently used
        * inactive - marked as not used
        * buffers - cache for things like file system metadata
        * cached - cache for various other things
        * shared - shared among multiple processes
        * wired - marked to always stay in RAM, never to disk
    OSX:
        * active - currently or very recently used
        * inactive - marked as not used
        * wired - marked to always stay in RAM, never to disk
    Other POSIX platforms:
        * active - currently or very recently used
        * inactive - marked as not used
    """
    metrics = psutil.virtual_memory()._asdict()
    del metrics['percent']

    if percent:
        total = metrics.pop('total')

        return OrderedDict(
            [('total', total)] +
            [(k, round(100. * v / total, 2))
             for k, v in metrics.items()]
        )
    else:
        return metrics


def memory_swap(percent=False):
    """
    Return swap metrics.

    Function returns a OrderedDict:

        {
            'total': <total memory>,
            'used': <used memory>,
            'free': <free memory>,
            ...
        },

    Above fields are available for every platform.
    If percent is true, all fields (except total) and given in
    percents. Otherwise, they are given in bytes.
    Additionally, there are other, platform-specific fields:

    POSIX platforms:
        * sin - bytes swapped in from disk
        * sout - bytes swapped out from disk

    sin and sout are always given in bytes.
    """
    metrics = psutil.swap_memory()

    if percent:
        metrics = OrderedDict([
            ('total', metrics.total),
            ('usage', metrics.percent),
            ('free', round(100. * metrics.free / metrics.total, 2)),
            ('sin', metrics.sin),
            ('sout', metrics.sout),
        ])
    else:
        metrics = metrics._asdict()
        del metrics['percent']

    if psutil.WINDOWS:
        #: sin and sout always 0 for Windows
        del metrics['sin']
        del metrics['sout']

    return metrics


def memory(percent=False):
    """
    Return memory metrics.

    Function amalgamates all other functions available in this module.
    It returns an OrderedDict instance:

        {
            'ram': <memory_ram(percent)>,
            'swap': <memory_ram(percent)>,
        }

    For more specific description please refer to appropriate description
    of above functions.
    """
    return OrderedDict((
        ('ram', memory_ram(percent)),
        ('swap', memory_swap(percent)),
    ))
