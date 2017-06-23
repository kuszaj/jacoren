# -*- coding: utf-8 -*-

"""Utilities for CPU info."""

import platform
import psutil
from collections import OrderedDict


#: Architecture (machine type)
ARCH = platform.machine()

#: Bit architecture
BITS, _ = platform.architecture()

#: CPU name
NAME = platform.processor()

#: Number of logical cores
LOGICAL_CORES = psutil.cpu_count(logical=True)
#: Number of physical cores
PHYSICAL_CORES = psutil.cpu_count(logical=False)
#: Number of cores
CORES = LOGICAL_CORES


def cpu_info():
    """
    Return basic information about CPU.

    Function returns OrderedDict instance::

        {
            'arch': <CPU architecture>
            'bits': <bit architecture>
            'name': <CPU name>,
            'cores': <number of (logical) cores>,
            'physical_cores': <number of physical cores>
        }

    Physical cores are the number of actual physical processor cores
    available. Logical cores tells how many threads can be run in
    parallel. Both values can differ if e.g. physical cores support
    hyper-threading.

    :Example:

    >>> import jacoren
    >>> jacoren.cpu.cpu_info()
    OrderedDict([('arch', 'x86_64'),
                 ('bits', '64bit'),
                 ('name', 'x86_64'),
                 ('cores', '4'),
                 ('physical_cores', '2')])

    :return: Basic CPU information
    :rtype: OrderedDict
    """
    return OrderedDict((
        ('arch', ARCH),
        ('bits', BITS),
        ('name', NAME),
        ('cores', CORES),
        ('physical_cores', PHYSICAL_CORES),
    ))


def cpu_load(cpu_time=False, core=None):
    """
    Return CPU load.

    Function returns an OrderedDict or list of OrderedDict instances::

        [
            ...
            {
                'user': <user processes>,
                'system': <kernel processes>,
                'idle': <idle CPU>,
                'used': <used CPU (not given for cpu_time=True)>,
                ...
            },
            ...
        ]

    Above fields are available for every platform. Additionally,
    there are other, platform-specific fields:

    Linux:
        * ``nice`` - prioritized user processes
        * ``iowait`` - waiting from I/O to complete
        * ``irq`` - servicing hardware interrupts
        * ``softirq`` - servicing software interrupts
        * ``steal`` - other OS running in virtualized env (2.6.11+)
        * ``guest`` - virtual CPUs (2.6.24+)
        * ``guest_nice`` - prioritized virtual CPUs (3.2.0+)
    BSD:
        * ``nice`` - prioritized user processes
        * ``irq`` - servicing hardware interrupts
    Other POSIX platforms:
        * ``nice`` - prioritized user processes
    Windows:
        * ``interrupt`` - servicing hardware interrupts
        * ``dpc`` - servicing lower priority procedure interrupts

    :Example:

    >>> import jacoren
    >>> jacoren.cpu.cpu_load()
    [OrderedDict([('user', 10.6),
                  ('system', 1.7),
                  ('idle', 86.2),
                  ('used', 13.8),
                  ('nice', 0.0),
                  ('iowait', 1.3),
                  ('irq', 0.0),
                  ('softirq', 0.1),
                  ('steal', 0.0),
                  ('guest', 0.0),
                  ('guest_nice', 0.0)]),
     OrderedDict([('user', 8.8),
                  ('system', 2.0),
                  ('idle', 88.8),
                  ('used', 11.2),
                  ('nice', 0.0),
                  ('iowait', 0.4),
                  ('irq', 0.0),
                  ('softirq', 0.0),
                  ('steal', 0.0),
                  ('guest', 0.0),
                  ('guest_nice', 0.0)]),
     OrderedDict([('user', 11.4),
                  ('system', 1.7),
                  ('idle', 84.7),
                  ('used', 15.3),
                  ('nice', 0.0),
                  ('iowait', 2.1),
                  ('irq', 0.0),
                  ('softirq', 0.0),
                  ('steal', 0.0),
                  ('guest', 0.0),
                  ('guest_nice', 0.0)]),
     OrderedDict([('user', 12.5),
                  ('system', 2.1),
                  ('idle', 84.9),
                  ('used', 15.1),
                  ('nice', 0.0),
                  ('iowait', 0.6),
                  ('irq', 0.0),
                  ('softirq', 0.0),
                  ('steal', 0.0),
                  ('guest', 0.0),
                  ('guest_nice', 0.0)]),
    >>> jacoren.cpu.cpu_load(cpu_time=True, core=2)
    OrderedDict([('user', 17720.05),
                 ('system', 1685.29),
                 ('idle', 28722.33),
                 ('nice', 13.78),
                 ('iowait', 507.7),
                 ('irq', 0.0),
                 ('softirq', 84.44),
                 ('steal', 0.0),
                 ('guest', 0.0)
                 ('guest_nice', 0.0)]),
    >>> jacoren.cpu.cpu_load(core=4)
    None

    :param cpu_time: If true, function returns all values as CPU times.
                     Otherwise, it will return them as CPU time percentages.
    :param core: If isn't ``None``, function will return metrics only for
                 given logical core (counting from zero) as ``OrderedDict``
                 instance. Otherwise, it will return a list of ``OrderedDict``
                 instances with metrics for all cores.
    :type cpu_time: bool
    :type core: int, None

    .. note:: If **core** is beyond possible range, function will return
              ``None``.

    :returns: CPU load for all or single logical core
    :rtype: list, OrderedDict, None
    """
    if cpu_time:
        cpus = psutil.cpu_times(percpu=True)
    else:
        cpus = psutil.cpu_times_percent(percpu=True)
    cpus = [cpu._asdict() for cpu in cpus]

    # Mapper returning dictionary for a single CPU data
    def _mapper(cpu):
        if cpu_time:
            for k, v in cpu.items():
                cpu[k] = float(round(v, 2))
        else:
            cpu['used'] = float(round(100. - cpu['idle'], 2))

        return cpu

    if core is None:
        return [_mapper(cpu) for cpu in cpus]
    else:
        try:
            return _mapper(cpus[core])
        except IndexError:
            return None


# CPU frequency is fixed for non-Linux platforms
if psutil.LINUX:
    _cpufreq = None
else:
    _cpufreq = psutil.cpu_freq(percpu=False)._asdict()


def cpu_freq(core=None):
    """
    Return CPU frequency.

    Function returns an OrderedDict or list of OrderedDict instances::

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

    :Example:

    >>> import jacoren
    >>> jacoren.cpu.cpu_freq()
    [OrderedDict([('current', 1200.0),
                  ('min', 1200.0),
                  ('max', 3400.0)]),
     OrderedDict([('current', 1200.0),
                  ('min', 1200.0),
                  ('max', 3400.0)]),
     OrderedDict([('current', 1200.0),
                  ('min', 1200.0),
                  ('max', 3400.0)]),
     OrderedDict([('current', 1200.0),
                  ('min', 1200.0),
                  ('max', 3400.0)])]
    >>> jacoren.cpu.cpu_freq(core=2)
    OrderedDict([('current', 1200.0),
                 ('min', 1200.0),
                 ('max', 3400.0)])
    >>> jacoren.cpu.cpu_freq(core=4)
    None

    :param core: If isn't ``None``, function will return metrics only for
                 given logical core (counting from zero) as ``OrderedDict``
                 instance. Otherwise, it will return a list of ``OrderedDict``
                 instances with metrics for all cores.
    :type core: int, None

    .. note:: If current platform is a Linux distribution, **core** is ignored.
              Otherwise, if **core** is beyond possible range, function will
              return ``None``.

    :returns: CPU frequency for all or single logical core
    :rtype: list, OrderedDict, None
    """
    if psutil.LINUX:
        cpus = psutil.cpu_freq(percpu=True)
        if core is None:
            return [cpu._asdict() for cpu in cpus]
        else:
            try:
                return cpus[core]._asdict()
            except IndexError:
                return None
    else:
        return _cpufreq


def cpu(cpu_time=False, core=None):
    """
    Return CPU information.

    Function amalgamates all other functions available in this module.
    It returns an OrderedDict instance::

        {
            'info': <cpu_info()>, # given only if core is None
            'load': <cpu_load(cpu_times, core)>,
            'freq': <cpu_freq(core)>,
        }

    For more specific description please refer to appropriate description
    of above functions.

    :param cpu_time: If true, function returns all values in ``load`` as CPU
                     times. Otherwise, it will return them as CPU time
                     percentages.
    :param core: If isn't ``None``, function will return metrics only for
                 given logical core (counting from zero), ommiting ``info``
                 key. Otherwise, it will return metrics for all cores.
    :type cpu_time: bool
    :type core: int, None

    .. note:: If **core** is beyond possible range, function will return
              ``None``.

    :returns: CPU load for all or single logical core
    :rtype: list, None

    .. seealso:: :func:`jacoren.cpu.cpu_info`,
                 :func:`jacoren.cpu.cpu_load`,
                 :func:`jacoren.cpu.cpu_freq`
    """
    if core is None:
        return OrderedDict((
            ('info', cpu_info()),
            ('load', cpu_load(cpu_time)),
            ('freq', cpu_freq()),
        ))
    else:
        result = OrderedDict((
            ('load', cpu_load(cpu_time, core)),
            ('freq', cpu_freq(core)),
        ))

        if result['load'] is None:
            return None
        return result
