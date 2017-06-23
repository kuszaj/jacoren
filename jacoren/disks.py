# -*- coding: utf-8 -*-

"""Utilities for disks info."""

import psutil
from collections import OrderedDict


def disks(percent=False):
    """
    Return disks metrics.

    Function returns a OrderedDict::

        {
            'device': <device name>,
            'mountpoint': <mounting point>,
            'fstype': <file system type>,
            'opts': <mounting options>,
            'used': <used space>,
            'total': <total space>,
            'free': <free space>,
        },

    >>> import jacoren
    >>> jacoren.disks.disks()
    [OrderedDict([('device', '/dev/sda2'),
                  ('mountpoint', '/'),
                  ('fstype', 'ext4'),
                  ('opts', 'rw'),
                  ('total', 103210729472),
                  ('used', 24459993088),
                  ('free', 73507856384)]),
     OrderedDict([('device', '/dev/sda1'),
                  ('mountpoint', '/boot'),
                  ('fstype', 'ext2'),
                  ('opts', 'rw'),
                  ('total', 1032085504),
                  ('used', 51761152),
                  ('free', 927895552)]),
     OrderedDict([('device', '/dev/sda5'),
                  ('mountpoint', '/home'),
                  ('fstype', 'ext4'),
                  ('opts', 'rw'),
                  ('total', 385948925952),
                  ('used', 333229932544),
                  ('free', 33113874432)])]
    >>> jacoren.disks.disks(percent=True)
    [OrderedDict([('device', '/dev/sda2'),
                  ('mountpoint', '/'),
                  ('fstype', 'ext4'),
                  ('opts', 'rw'),
                  ('total', 103210729472),
                  ('used', 25.0),
                  ('free', 75.0)]),
     OrderedDict([('device', '/dev/sda1'),
                  ('mountpoint', '/boot'),
                  ('fstype', 'ext2'),
                  ('opts', 'rw'),
                  ('total', 1032085504),
                  ('used', 5.3),
                  ('free', 94.7)]),
     OrderedDict([('device', '/dev/sda5'),
                  ('mountpoint', '/home'),
                  ('fstype', 'ext4'),
                  ('opts', 'rw'),
                  ('total', 385948925952),
                  ('used', 91.0),
                  ('free', 9.0)])]

    :param percent: If true, function will return ``used`` and ``free``
                    as percentages. Otherwise, it will return them as bytes.
    :type percent: bool

    :returns: Disks metrics
    :rtype: OrderedDict
    """
    disks = [disk._asdict()
             for disk in psutil.disk_partitions(all=False)]

    #: Mapper returning dictionary for a single disk metrics
    def _mapper(disk):
        usage = psutil.disk_usage(disk['mountpoint'])._asdict()

        _percent = usage.pop('percent')

        if percent:
            usage = OrderedDict([
                ('total', usage['total']),
                ('used', _percent),
                ('free', round(100. - _percent, 2)),
            ])

        return OrderedDict(disk, **usage)

    return [_mapper(disk) for disk in disks]
