# -*- coding: utf-8 -*-

import jacoren.machine
from collections import OrderedDict


def test_os():
    os = jacoren.machine.OS

    assert isinstance(os, str)
    assert os != ''

def test_version():
    version = jacoren.machine.VERSION

    assert isinstance(version, tuple)
    assert len(version) > 0
    assert len(version) <= 4

def test_machine():
    machine = jacoren.machine.machine()

    assert isinstance(machine, OrderedDict)
    assert 'os' in machine
    assert isinstance(machine['os'], str)
    assert 'version' in machine
    assert isinstance(machine['version'], tuple)
    assert 'uptime' in machine
    assert isinstance(machine['uptime'], int)
    assert 'users' in machine
    assert isinstance(machine['users'], list)

def test_machine_uptime():
    uptime = jacoren.machine.machine_uptime()

    assert isinstance(uptime, int)
    assert uptime > 0

def test_machine_users():
    users = jacoren.machine.machine_users()

    assert isinstance(users, list)
    assert len(users) > 0

    for user in users:
        assert isinstance(user, OrderedDict)
        assert 'name' in user
        assert isinstance(user['name'], str)
        assert 'logged_time' in user
        assert isinstance(user['logged_time'], int)
