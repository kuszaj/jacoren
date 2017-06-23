# -*- coding: utf-8 -*-

"""Utilities for memory info."""

import psutil
from collections import OrderedDict


def memory_ram(percent=False):
    """
    Return memory metrics.

    Function returns a OrderedDict::

        {
            'total': <total memory>,
            'available': <available memory>,
            'used': <used memory>,
            'free': <free memory>,
            ...
        },

    Above fields are available for every platform. Additionally, there are
    other, platform-specific fields:

    Linux:
        * ``active`` - currently or very recently used
        * ``inactive`` - marked as not used
        * ``buffers`` - cache for things like file system metadata
        * ``cached`` - cache for various other things
        * ``shared`` - shared among multiple processes
    BSD:
        * ``active`` - currently or very recently used
        * ``inactive`` - marked as not used
        * ``buffers`` - cache for things like file system metadata
        * ``cached`` - cache for various other things
        * ``shared`` - shared among multiple processes
        * ``wired`` - marked to always stay in RAM, never to disk
    OSX:
        * ``active`` - currently or very recently used
        * ``inactive`` - marked as not used
        * ``wired`` - marked to always stay in RAM, never to disk
    Other POSIX platforms:
        * ``active`` - currently or very recently used
        * ``inactive`` - marked as not used

    :Example:

    >>> import jacoren
    >>> jacoren.memory.memory_ram()
    OrderedDict([('total', 4218454016),
                 ('available', 1113473024),
                 ('used', 2908168192),
                 ('free', 138534912),
                 ('active', 2210504704),
                 ('inactive', 1627693056),
                 ('buffers', 43229184),
                 ('cached', 1128521728),
                 ('shared', 156925952)])
    >>> jacoren.memory.memory_ram(percent=True)
    OrderedDict([('total', 4218454016),
                 ('available', 26.77),
                 ('used', 68.54),
                 ('free', 4.0),
                 ('active', 51.99),
                 ('inactive', 38.25),
                 ('buffers', 1.07),
                 ('cached', 26.39),
                 ('shared', 3.74)])

    :param percent: If true, function will return all values (except for
                    ``total``) as percentages. Otherwise, it will return
                    them as bytes.
    :type percent: bool

    .. note:: ``used`` and ``free`` can be calculated differently and do not
              necessarily will match with ``total - free`` and
              ``total - used``. It is recommended to use mostly ``total`` and
              ``available`` fields.

    :returns: RAM metrics
    :rtype: OrderedDict
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

    Function returns a OrderedDict::

        {
            'total': <total memory>,
            'used': <used memory>,
            'free': <free memory>,
            ...
        },

    Above fields are available for every platform. Additionally, there are
    other, platform-specific fields:

    POSIX platforms:
        * ``sin`` - bytes swapped in from disk
        * ``sout`` - bytes swapped out from disk

    :Example:

    >>> import jacoren
    >>> jacoren.memory.memory_swap()
    OrderedDict([('total', 2097147904),
                 ('used', 615657472),
                 ('free', 1481490432),
                 ('sin', 190640128),
                 ('sout', 704741376)])
    >>> jacoren.memory.memory_swap(percent=True)
    OrderedDict([('total', 2097147904),
                 ('used', 29.4),
                 ('free', 70.64),
                 ('sin', 190640128),
                 ('sout', 704741376)])

    :param percent: If true, function will return ``used`` and ``free`` as
                    percentages. Otherwise, it will return them as bytes.
                    Other fields are always returned as bytes.
    :type percent: bool

    :returns: Swap metrics
    :rtype: OrderedDict
    """
    metrics = psutil.swap_memory()

    if percent:
        metrics = OrderedDict([
            ('total', metrics.total),
            ('used', metrics.percent),
            ('free', round(100. * metrics.free / metrics.total, 2)),
            ('sin', metrics.sin),
            ('sout', metrics.sout),
        ])
    else:
        metrics = metrics._asdict()
        del metrics['percent']

    if psutil.WINDOWS:
        # sin and sout always 0 for Windows
        del metrics['sin']
        del metrics['sout']

    return metrics


def memory(percent=False):
    """
    Return memory metrics.

    Function amalgamates all other functions available in this module.
    It returns an OrderedDict instance::

        {
            'ram': <memory_ram(percent)>,
            'swap': <memory_ram(percent)>,
        }

    For more specific description please refer to appropriate description
    of above functions.

    :param percent: If true, function will return some values as percentages.
                    Otherwise, it will return them as bytes.
    :type percent: bool

    :returns: Swap metrics
    :rtype: OrderedDict

    .. seealso:: :func:`jacoren.memory.memory_ram`,
                 :func:`jacoren.memory.memory_swap`
    """
    return OrderedDict((
        ('ram', memory_ram(percent)),
        ('swap', memory_swap(percent)),
    ))
