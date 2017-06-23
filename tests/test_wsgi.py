# -*- coding: utf-8 -*-

import pytest
from werkzeug import Client
from werkzeug.wrappers import BaseResponse
from jacoren._server import JacorenServer


@pytest.fixture
def client():
    return Client(JacorenServer(), BaseResponse)

def test_root():
    response = client().get('/')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_machine():
    response = client().get('/machine')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_machine_uptime():
    response = client().get('/machine/uptime')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_machine_users():
    response = client().get('/machine/users')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu():
    response = client().get('/cpu')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_core():
    from jacoren.cpu import CORES as cores

    for core in range(cores):
        response = client().get('/cpu/%d' % (core,))

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
        assert len(response.data) > 0

def test_cpu_core_404():
    from jacoren.cpu import CORES as cores

    response = client().get('/cpu/%d' % (cores+1,))

    assert response.status_code == 404
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_info():
    response = client().get('/cpu/info')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_load():
    response = client().get('/cpu/load')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_load_core():
    from jacoren.cpu import CORES as cores

    for core in range(cores):
        response = client().get('/cpu/load/%d' % (core,))

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
        assert len(response.data) > 0

def test_cpu_load_core_404():
    from jacoren.cpu import CORES as cores

    response = client().get('/cpu/load/%d' % (cores+1,))

    assert response.status_code == 404
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_freq():
    response = client().get('/cpu/freq')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_cpu_freq_core():
    from jacoren.cpu import CORES as cores

    for core in range(cores):
        response = client().get('/cpu/freq/%d' % (core,))

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
        assert len(response.data) > 0

def test_cpu_freq_core_404():
    from jacoren.cpu import CORES as cores

    response = client().get('/cpu/freq/%d' % (cores+1,))

    assert response.status_code == 404
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_memory():
    response = client().get('/memory')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_memory_ram():
    response = client().get('/memory/ram')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_memory_swap():
    response = client().get('/memory/swap')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0

def test_disks():
    response = client().get('/disks')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert len(response.data) > 0
