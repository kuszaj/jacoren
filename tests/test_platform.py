# -*- coding: utf-8 -*-

import jacoren.platform
from collections import OrderedDict


def test_os():
    os = jacoren.platform.OS

    assert isinstance(os, str)
    assert os != ''

def test_version():
    version = jacoren.platform.VERSION

    assert isinstance(version, tuple)
    assert len(version) > 0
    assert len(version) <= 4

def test_platform():
    platform = jacoren.platform.platform()

    assert isinstance(platform, OrderedDict)
    assert 'os' in platform
    assert isinstance(platform['os'], str)
    assert 'version' in platform
    assert isinstance(platform['version'], tuple)
    assert 'uptime' in platform
    assert isinstance(platform['uptime'], int)
    assert 'users' in platform
    assert isinstance(platform['users'], list)

def test_platform_uptime():
    uptime = jacoren.platform.platform_uptime()

    assert isinstance(uptime, int)
    assert uptime > 0

def test_platform_users():
    users = jacoren.platform.platform_users()

    assert isinstance(users, list)
    assert len(users) > 0

    for user in users:
        assert isinstance(user, OrderedDict)
        assert 'name' in user
        assert isinstance(user['name'], str)
        assert 'logged_time' in user
        assert isinstance(user['logged_time'], int)
