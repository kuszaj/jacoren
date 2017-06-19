# jacoren

> Ah, you're here, good...
> -- <cite>Jacoren, Overseer of Vault 13, 2161</cite>

**jacoren** is a small cross-platform package for retrieving basic information about machine and its CPUs, memory and disks in a form of handy constants and dictionaries, built on top of `psutils` and `platform`. It can be used as a Python package and allows to create simple RESTful APIs if used as a WSGI application or a single-threaded server.

## Installation

#### Using pip

```shell
$ pip install jacoren
```

#### From GitHub

```shell
$ git clone git@github.com:kuszaj/jacoren.git
$ cd jacoren && python setup.py install
```

## Usage

### Platform

Constant/function | Type | Description
----------------- | ---- | -----------
`jacoren.platform.OS` | `str` | Platform operating system, e.g. `Linux`
`jacoren.platform.VERSION` | `tuple` | Platform version, e.g. `('3', '7', '5', '201.fc18.x86_64')`
`jacoren.platform.platform()` | `OrderedDict` | Basic information about platform
`jacoren.platform.platform_uptime()` | `int` | Uptime in seconds
`jacoren.platform.platform_users()` | `list(OrderedDict)` | List of logged users (names and logged time)

##### Examples

```python
>>> import jacoren
>>> jacoren.platform.OS
'Linux'
>>> jacoren.platform.VERSION
('3', '7', '5', '201.fc18.x86_64')
>>> jacoren.platform.platform_uptime()
19236
>>> jacoren.platform.platform_users()
[OrderedDict([('name', 'some_user'), ('logged_time', 19242)]), OrderedDict([('name', 'another_user'), ('logged_time', 6176)])]
>>> jacoren.platform.platform()
OrderedDict([('os', 'Linux'), ('version', ('3', '7', '5', '201.fc18.x86_64')), ('uptime', 19250), ('users', [OrderedDict([('name', 'some_user'), ('logged_time', 19242)]), OrderedDict([('name', 'another_user'), ('logged_time', 6184)])])])
```

### CPU

Constant/function | Type | Description
----------------- | ---- | -----------

##### Examples

```python
```

TODO

### Memory

Constant/function | Type | Description
----------------- | ---- | -----------

##### Examples

```python
```

TODO

### Disks

Constant/function | Type | Description
----------------- | ---- | -----------

##### Examples

```python
```

TODO


## RESTFul API

Method | Description
------ | -----------

### Stand-alone
```shell
$ jacoren --help
usage: jacoren [-h] [-v] [--host HOST] [--port PORT]

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  --host HOST    host IP address/name (default: localhost)
  --port PORT    port (default: 1313)
```

server:
```shell
$ jacoren
 * Running on http://localhost:1313/ (Press CTRL+C to quit)
```

client:
```
$ curl http://localhost:1313/cpu/load
[{"user": 0.9, "nice": 3.0, "system": 0.9, "idle": 95.3, "iowait": 0.0, "irq": 0.0, "softirq": 0.0, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0, "used": 4.7}, {"user": 1.8, "nice": 0.0, "system": 1.2, "idle": 97.0, "iowait": 0.0, "irq": 0.0, "softirq": 0.0, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0, "used": 3.0}]
```

### WSGI

```shell
$ gunicorn -w 4 jacoren:wsgi
```

## License

[MIT](LICENSE)
