# -*- coding: utf-8 -*-

import psutil


#: Core count (physical and logical)
LOGICAL_CORES = psutil.cpu_count(logical=True)
PHYSICAL_CORES = psutil.cpu_count(logical=False)
CORES = LOGICAL_CORES

def cpu_info():
    return {
        'cores': CORES,
        'physical_cores': PHYSICAL_CORES
    }
