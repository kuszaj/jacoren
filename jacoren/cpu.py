# -*- coding: utf-8 -*-

"""Utilities for CPU info."""

import platform
import psutil
from collections import OrderedDict

from jacoren.platform import VERSION as _platform_version


#: CPU name
NAME = platform.processor()

#: Core count (physical and logical)
LOGICAL_CORES = psutil.cpu_count(logical=True)
PHYSICAL_CORES = psutil.cpu_count(logical=False)
CORES = LOGICAL_CORES


def cpu_info():
    """
    Return number of cores (logical and physical).

    Function returns OrderedDict instance:

        {
            'name': <CPU name>,
            'cores': <number of (logical) cores>,
            'physical_cores': <number of physical cores>
        }

    Physical cores are the number of actual physical processor cores
    available. Logical cores tells how many threads can be run in
    parallel. Both values can differ if e.g. physical cores support
    hyper-threading.
    """
    return OrderedDict((
        ('name', NAME),
        ('cores', CORES),
        ('physical_cores', PHYSICAL_CORES),
    ))


def cpu_load(cpu_time=False):
    """
    Return CPU load for every logical core.

    Function returns a list of OrderedDict instances:

        [
            ...
            {
                'user': <user processes>,
                'system': <kernel processes>,
                'idle': <idle CPU>,
                ...
            },
            ...
        ]

    Above fields are available for every platform. Additionally,
    there are other, platform-specific fields:

    Linux:
        * nice - prioritized user processes
        * iowait - waiting from I/O to complete
        * irq - servicing hardware interrupts
        * softirq - servicing software interrupts
        * steal - other OS running in virtualized env (2.6.11+)
        * guest - virtual CPUs (2.6.24+)
        * guest_nice - prioritized virtual CPUs (3.2.0+)
    BSD:
        * nice - prioritized user processes
        * irq - servicing hardware interrupts
    Other POSIX platforms:
        * nice - prioritized user processes
    Windows:
        * interrupt - servicing hardware interrupts
        * dpc - servicing lower priority procedure interrupts

    By default, function return all fields as CPU time percentages.
    If cpu_time is true, function will return all fields as CPU times.
    """
    if cpu_time:
        cpus = psutil.cpu_times(percpu=True)
    else:
        cpus = psutil.cpu_times_percent(percpu=True)
    cpus = [cpu._asdict() for cpu in cpus]

    #: Mapper returning dictionary for a single CPU data
    def _mapper(cpu):
        if cpu_time:
            for k,v in cpu.items():
                cpu[k] = float(round(v, 2))
        else:
            cpu['used'] = float(round(100. - cpu['idle'], 2))

        return cpu

    return [_mapper(cpu) for cpu in cpus]


#: CPU frequency is fixed for non-Linux platforms
if psutil.LINUX:
    _cpufreq = None
else:
    _cpufreq = psutil.cpu_freq(percpu=False)._asdict()


def cpu_freq():
    """
    Return CPU frequency for every logical core.

    Function returns a list of OrderedDict instances:

        [
            ...
            {
                'current': <current freq>,
                'min': <min freq>,
                'max': <max freq>
            },
            ...
        ]

    On Linux function returns real-time value of current for every
    logical core. On other platforms it returns a single element list
    with fixed current value.
    """
    if psutil.LINUX:
        cpus = psutil.cpu_freq(percpu=True)
        return [cpu._asdict() for cpu in cpus]
    else:
        return [_cpufreq]


def cpu(cpu_time=False):
    """
    Return CPU information.

    Function amalgamates all other functions available in this module.
    It returns an OrderedDict instance:

        {
            'info': <cpu_info()>,
            'load': <cpu_load(times)>,
            'freq': <cpu_freq()>,
        }

    For more specific description please refer to appropriate description
    of above functions.
    """
    return OrderedDict((
        ('info', cpu_info()),
        ('load', cpu_load(cpu_time)),
        ('freq', cpu_freq()),
    ))
