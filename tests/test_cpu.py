# -*- coding: utf-8 -*-

import pytest
import psutil
import jacoren.cpu
from collections import OrderedDict


def test_arch():
    arch = jacoren.cpu.ARCH

    assert isinstance(arch, str)
    assert arch != ''

def test_bits():
    bits = jacoren.cpu.BITS

    assert isinstance(bits, str)
    assert bits != ''

def test_name():
    name = jacoren.cpu.NAME

    assert isinstance(name, str)
    assert name != ''

@pytest.fixture
def cores_counts():
    return (
        jacoren.cpu.LOGICAL_CORES,
        jacoren.cpu.PHYSICAL_CORES,
        jacoren.cpu.CORES,
    )

def test_cores():
    log_cores, phys_cores, cores = cores_counts()

    assert isinstance(log_cores, int)
    assert log_cores > 0
    assert isinstance(phys_cores, int)
    assert phys_cores > 0
    assert isinstance(cores, int)
    assert cores > 0
    assert cores == log_cores

def test_cpu_percent_all():
    cpu = jacoren.cpu.cpu()
    _, __, cores = cores_counts()

    assert isinstance(cpu, OrderedDict)
    assert 'info' in cpu
    assert isinstance(cpu['info'], OrderedDict)
    assert 'load' in cpu
    assert isinstance(cpu['load'], list)
    assert 'freq' in cpu
    if psutil.LINUX:
        assert isinstance(cpu['freq'], list)
    else:
        assert isinstance(cpu['freq'], OrderedDict)

    for core in range(cores):
        assert isinstance(cpu['load'][core], OrderedDict)

        if psutil.LINUX:
            assert isinstance(cpu['freq'][core], OrderedDict)

def test_cpu_cpu_time_all():
    cpu = jacoren.cpu.cpu(cpu_time=True)
    _, __, cores = cores_counts()

    assert isinstance(cpu, OrderedDict)
    assert 'info' in cpu
    assert isinstance(cpu['info'], OrderedDict)
    assert 'load' in cpu
    assert isinstance(cpu['load'], list)
    assert 'freq' in cpu
    if psutil.LINUX:
        assert isinstance(cpu['freq'], list)
    else:
        assert isinstance(cpu['freq'], OrderedDict)

    for core in range(cores):
        assert isinstance(cpu['load'][core], OrderedDict)

        if psutil.LINUX:
            assert isinstance(cpu['freq'][core], OrderedDict)

def test_cpu_percent_single():
    _, __, cores = cores_counts()

    for core in range(cores):
        core_cpu = jacoren.cpu.cpu(core=core)

        assert isinstance(core_cpu, OrderedDict)
        assert 'info' not in core_cpu
        assert 'load' in core_cpu
        assert isinstance(core_cpu['load'], OrderedDict)
        assert 'freq' in core_cpu
        assert isinstance(core_cpu['freq'], OrderedDict)

def test_cpu_percent_single_err():
    _, __, cores = cores_counts()
    core_cpu = jacoren.cpu.cpu(core=cores+1)

    assert core_cpu is None

def test_cpu_cpu_time_single():
    _, __, cores = cores_counts()

    for core in range(cores):
        core_cpu = jacoren.cpu.cpu(cpu_time=True, core=core)

        assert isinstance(core_cpu, OrderedDict)
        assert 'info' not in core_cpu
        assert 'load' in core_cpu
        assert isinstance(core_cpu['load'], OrderedDict)
        assert 'freq' in core_cpu
        assert isinstance(core_cpu['freq'], OrderedDict)

def test_cpu_cpu_time_single_err():
    _, __, cores = cores_counts()
    core_cpu = jacoren.cpu.cpu(cpu_time=True, core=cores+1)

    assert core_cpu is None

def test_cpu_info():
    info = jacoren.cpu.cpu_info()
    keys = ('arch', 'bits', 'name', 'cores', 'physical_cores')

    assert isinstance(info, OrderedDict)
    assert set(keys) == set(info.keys())

def test_cpu_load_percent_all():
    load = jacoren.cpu.cpu_load()
    _, __, cores = cores_counts()

    assert isinstance(load, list)
    assert len(load) == cores

    for core_load in load:
        assert isinstance(core_load, OrderedDict)
        assert 'user' in core_load
        assert isinstance(core_load['user'], float)
        assert 'system' in core_load
        assert isinstance(core_load['system'], float)
        assert 'idle' in core_load
        assert isinstance(core_load['idle'], float)

def test_cpu_load_cpu_time_all():
    load = jacoren.cpu.cpu_load(cpu_time=True)
    _, __, cores = cores_counts()
    assert isinstance(load, list)
    assert len(load) == cores

    for core_load in load:
        assert isinstance(core_load, OrderedDict)
        assert 'user' in core_load
        assert isinstance(core_load['user'], float)
        assert 'system' in core_load
        assert isinstance(core_load['system'], float)
        assert 'idle' in core_load
        assert isinstance(core_load['idle'], float)

def test_cpu_load_percent_single():
    _, __, cores = cores_counts()

    for core in range(cores):
        core_load = jacoren.cpu.cpu_load(core=core)

        assert isinstance(core_load, OrderedDict)
        assert 'user' in core_load
        assert isinstance(core_load['user'], float)
        assert 'system' in core_load
        assert isinstance(core_load['system'], float)
        assert 'idle' in core_load
        assert isinstance(core_load['idle'], float)

def test_cpu_load_percent_single_err():
    _, __, cores = cores_counts()
    core_load = jacoren.cpu.cpu_load(core=cores+1)

    assert core_load is None

def test_cpu_load_cpu_time_single():
    _, __, cores = cores_counts()

    for core in range(cores):
        core_load = jacoren.cpu.cpu_load(cpu_time=True, core=core)

        assert isinstance(core_load, OrderedDict)
        assert 'user' in core_load
        assert isinstance(core_load['user'], float)
        assert 'system' in core_load
        assert isinstance(core_load['system'], float)
        assert 'idle' in core_load
        assert isinstance(core_load['idle'], float)

def test_cpu_load_cpu_time_single_err():
    _, __, cores = cores_counts()
    core_load = jacoren.cpu.cpu_load(cpu_time=True, core=cores+1)

    assert core_load is None

def test_cpu_freq_all():
    freq = jacoren.cpu.cpu_freq()

    assert isinstance(freq, list)

    if psutil.LINUX:
        _, __, cores = cores_counts()
        assert len(freq) == cores

        for core_freq in freq:
            assert isinstance(core_freq, OrderedDict)
            assert 'current' in core_freq
            assert isinstance(core_freq['current'], float)
            assert 'min' in core_freq
            assert isinstance(core_freq['min'], float)
            assert 'max' in core_freq
            assert isinstance(core_freq['max'], float)
    else:
        assert isinstance(freq, OrderedDict)
        assert 'current' in freq
        assert isinstance(freq['current'], float)
        assert 'min' in freq
        assert isinstance(freq['min'], float)
        assert 'max' in freq
        assert isinstance(freq['max'], float)

def test_cpu_freq_single():
    _, __, cores = cores_counts()

    for core in range(cores):
        core_freq = jacoren.cpu.cpu_freq(core=core)

        assert isinstance(core_freq, OrderedDict)
        assert 'current' in core_freq
        assert isinstance(core_freq['current'], float)
        assert 'min' in core_freq
        assert isinstance(core_freq['min'], float)
        assert 'max' in core_freq
        assert isinstance(core_freq['max'], float)

def test_cpu_freq_single_err():
    _, __, cores = cores_counts()
    core_freq = jacoren.cpu.cpu_freq(core=cores+1)

    assert core_freq is None
