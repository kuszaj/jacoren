# -*- coding: utf-8 -*-

import psutil
import jacoren.disks
from collections import OrderedDict


def test_disks_bytes():
    disks = jacoren.disks.disks()

    assert isinstance(disks, list)

    for disk in disks:
        assert 'device' in disk
        assert isinstance(disk['device'], str)
        assert 'mountpoint' in disk
        assert isinstance(disk['mountpoint'], str)
        assert 'fstype' in disk
        assert isinstance(disk['fstype'], str)
        assert 'opts' in disk
        assert isinstance(disk['opts'], str)
        assert 'total' in disk
        try:
            assert isinstance(disk['total'], (int, long))
        except NameError:
            assert isinstance(disk['total'], int)
        assert 'used' in disk
        try:
            assert isinstance(disk['used'], (int, long))
        except NameError:
            assert isinstance(disk['used'], int)
        assert 'free' in disk
        try:
            assert isinstance(disk['free'], (int, long))
        except NameError:
            assert isinstance(disk['free'], int)

def test_disks_percent():
    disks = jacoren.disks.disks(percent=True)

    assert isinstance(disks, list)

    for disk in disks:
        assert 'device' in disk
        assert isinstance(disk['device'], str)
        assert 'mountpoint' in disk
        assert isinstance(disk['mountpoint'], str)
        assert 'fstype' in disk
        assert isinstance(disk['fstype'], str)
        assert 'opts' in disk
        assert isinstance(disk['opts'], str)
        assert 'total' in disk
        try:
            assert isinstance(disk['total'], (int, long))
        except NameError:
            assert isinstance(disk['total'], int)
        assert 'used' in disk
        assert isinstance(disk['used'], float)
        assert 'free' in disk
        assert isinstance(disk['free'], float)

