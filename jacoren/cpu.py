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
            fields = fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal', 'guest', 'guest_nice',
            )
        elif _platform_version >= ('2', '6', '24'):
            fields = fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal', 'guest',
            )
        elif _platform_version >= ('2', '6', '11'):
            fields = fields + (
                'nice', 'iowait', 'irq', 'softirq',
                'steal',
            )
        else:
            fields = fields + (
                'nice', 'iowait', 'irq', 'softirq',
            )
    elif psutil.BSD:
        fields = fields + ('nice', 'irq')
    elif psutil.POSIX:
        fields = fields + ('nice')
    elif psutil.WINDOWS:
        fields = fields + ('interrupt', 'dpc')
    else:
        raise RuntimeError("cpuinfo not supported")

    if cpu_time:
        cpus = psutil.cpu_times(percpu=True)
    else:
        cpus = psutil.cpu_times_percent(percpu=True)

    #: Mapper returning dictionary for a single CPU data
    def _mapper(cpu):
        if cpu_time:
            d = {field: float(round(getattr(cpu, field), 2))
                 for field in fields}
        else:
            d = {field: getattr(cpu, field)
                 for field in fields}
            d['used'] = float(round(100. - d['idle'], 2))

        return d

    return [_mapper(cpu) for cpu in cpus]


#: CPU frequency is fixed for non-Linux platforms
if psutil.LINUX:
    _cpufreq = None
else:
    _cpufreq = psutil.cpu_freq(percpu=False)
    _cpufreq = {
        'current': _cpufreq.current,
        'min': _cpufreq.min,
        'max': _cpufreq.max,
    }

def cpu_freq():
    if psutil.LINUX:
        fields = ('current', 'min', 'max')
        cpus = psutil.cpu_freq(percpu=True)
        _mapper = lambda cpu: {field: getattr(cpu, field)
                               for field in fields}
        return [_mapper(cpu) for cpu in cpus]
    else:
        return _cpufreq
