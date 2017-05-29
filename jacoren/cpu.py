# -*- coding: utf-8 -*-

import psutil
from jacoren.platform import VERSION as _platform_version


#: Core count (physical and logical)
LOGICAL_CORES = psutil.cpu_count(logical=True)
PHYSICAL_CORES = psutil.cpu_count(logical=False)
CORES = LOGICAL_CORES

def cpu_info():
    return {
        'cores': CORES,
        'physical_cores': PHYSICAL_CORES
    }

def cpu_load(cpu_time=False):
    #: Platform-independent
    fields = ('user', 'system', 'idle')

    #: Platform-specific
    if psutil.LINUX:
        if _platform_version >= ('3', '2', '0'):
            _fields = _fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal', 'guest', 'guest_nice',
            )
        elif _platform_version >= ('2', '6', '24'):
            _fields = _fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal', 'guest',
            )
        elif _platform_version >= ('2', '6', '11'):
            _fields = _fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal',
            )
        else:
            _fields = _fields + (
                'nice', 'iowait', 'irq', 'softirq',
            )
    elif psutil.BSD:
        _fields = _fields + ('nice', 'irq')
    elif psutil.POSIX:
        _fields = _fields + ('nice')
    elif psutil.WINDOWS:
        _fields = _fields + ('interrupt', 'dpc')
    else:
        raise RuntimeError("cpuinfo not supported")
