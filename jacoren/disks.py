# -*- coding: utf-8 -*-

"""Utilities for disks info."""

import psutil
from collections import OrderedDict


def disks(percent=False):
    """
    Return disks metrics.

    Function returns a OrderedDict:

        {
            'device': <device name>,
            'mountpoint': <mounting point>,
            'fstype': <file system type>,
            'opts': <mounting options>,
            'used': <used space>,
            'total': <total space>,
            'free': <free space>,
        },

    If percent is true, used and free are given in
    percents. Otherwise, they are given in bytes.
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
