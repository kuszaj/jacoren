# -*- coding: utf-8 -*-

import psutil
import jacoren.memory
from collections import OrderedDict


def test_memory_bytes():
    memory = jacoren.memory.memory()

    assert isinstance(memory, OrderedDict)
    assert 'ram' in memory
    assert isinstance(memory['ram'], OrderedDict)
    assert 'swap' in memory
    assert isinstance(memory['swap'], OrderedDict)

def test_memory_percent():
    memory = jacoren.memory.memory(percent=True)

    assert isinstance(memory, OrderedDict)
    assert 'ram' in memory
    assert isinstance(memory['ram'], OrderedDict)
    assert 'swap' in memory
    assert isinstance(memory['swap'], OrderedDict)

def test_memory_ram_bytes():
    ram = jacoren.memory.memory_ram()

    assert isinstance(ram, OrderedDict)
    assert 'total' in ram
    assert isinstance(ram['total'], int)
    assert ram['total'] > 0
    assert 'available' in ram
    assert isinstance(ram['available'], int)
    assert 'used' in ram
    assert isinstance(ram['used'], int)
    assert 'free' in ram
    assert isinstance(ram['free'], int)

def test_memory_ram_percent():
    ram = jacoren.memory.memory_ram(percent=True)

    assert isinstance(ram, OrderedDict)
    assert 'total' in ram
    assert isinstance(ram['total'], int)
    assert ram['total'] > 0.
    assert 'available' in ram
    assert isinstance(ram['available'], float)
    assert 'used' in ram
    assert isinstance(ram['used'], float)
    assert 'free' in ram
    assert isinstance(ram['free'], float)

def test_memory_swap_bytes():
    swap = jacoren.memory.memory_swap()

    assert isinstance(swap, OrderedDict)
    assert 'total' in swap
    assert isinstance(swap['total'], int)
    assert swap['total'] > 0
    assert 'used' in swap
    assert isinstance(swap['used'], int)
    assert 'free' in swap
    assert isinstance(swap['free'], int)

    if not psutil.WINDOWS:
        assert 'sin' in swap
        assert isinstance(swap['sin'], int)
        assert 'sout' in swap
        assert isinstance(swap['sout'], int)

def test_memory_swap_percent():
    swap = jacoren.memory.memory_swap(percent=True)

    assert isinstance(swap, OrderedDict)
    assert 'total' in swap
    assert isinstance(swap['total'], int)
    assert swap['total'] > 0.
    assert 'used' in swap
    assert isinstance(swap['used'], float)
    assert 'free' in swap
    assert isinstance(swap['free'], float)

    if not psutil.WINDOWS:
        assert 'sin' in swap
        assert isinstance(swap['sin'], int)
        assert 'sout' in swap
        assert isinstance(swap['sout'], int)
