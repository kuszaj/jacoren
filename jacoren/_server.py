# -*- coding: utf-8 -*-

from __future__ import print_function
import json
from sys import version_info
from functools import wraps
from collections import Iterable, OrderedDict
from werkzeug.wrappers import Request, Response
from werkzeug.datastructures import Headers
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.serving import WSGIRequestHandler

from jacoren import (
    __version__ as _jacoren_version,
    platform,
    cpu,
    memory,
    disks,
)


_python_version = "%s.%s.%s" % (version_info.major,
                                version_info.minor,
                                version_info.micro)


def json_response(func):
    """Decorate function to it returns JSON response."""
    @wraps(func)
    def new(inst, *args, **kwargs):
        result = func(inst, *args, **kwargs)

        headers = Headers({
            'Server': 'jacoren/%s Python/%s' % (_jacoren_version,
                                                _python_version),
            'Content-Type': 'application/json; charset=UTF-8',

            #:
            #: A man is not dead while his name is still spoken.
            #:                  ~ Going Postal, Chapter 4 prologue
            #:
            #: See: gnuterrypratchett.com
            #:
            'X-Clacks-Overhead': 'GNU Terry Pratchett',
        })

        return Response(json.dumps(result) + '\r\n',
                        headers=headers)
    return new


class JacorenServer(object):
    """WSGI server class."""

    def __init__(self):
        """Init resource paths."""
        self.paths = Map((
            #: Plaform
            Rule('/platform', endpoint='platform',
                 strict_slashes=False),
            Rule('/platform/uptime', endpoint='platform_uptime',
                 strict_slashes=False),
            Rule('/platform/users', endpoint='platform_users',
                 strict_slashes=False),

            #: CPU
            Rule('/cpu', endpoint='cpu',
                 strict_slashes=False),
            Rule('/cpu/info', endpoint='cpu_info',
                 strict_slashes=False),
            Rule('/cpu/load', endpoint='cpu_load',
                 strict_slashes=False),
            Rule('/cpu/freq', endpoint='cpu_freq',
                 strict_slashes=False),

            #: Memory
            Rule('/memory', endpoint='memory',
                 strict_slashes=False),
            Rule('/memory/ram', endpoint='memory_ram',
                 strict_slashes=False),
            Rule('/memory/swap', endpoint='memory_swap',
                 strict_slashes=False),

            #: Disks
            Rule('/disks', endpoint='disks',
                 strict_slashes=False),
        ))

    def parse_request(self, request):
        """Parse HTTP request."""
        adapter = self.paths.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException as http_error:
            response = self.respond_with_error(request, http_error)
            response.status_code = http_error.code
            return response

    @json_response
    def respond_with_error(self, request, http_error):
        if isinstance(http_error, NotFound):
            response = {
                'code': http_error.code,
                'msg':  "%s not found" % (request.path)
            }
        else:
            response = {
                'code': http_error.code,
                'msg':  http_error.description
            }

        return response

    def wsgi(self, environ, start_response):
        """Main WSGI function."""
        request = Request(environ)
        response = self.parse_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """Act as WSGI function."""
        return self.wsgi(environ, start_response)

    #:
    #: Request handlers
    #:

    #: Platform
    @json_response
    def platform(self, request):
        """Return platform info."""
        return platform.platform()

    @json_response
    def platform_uptime(self, request):
        """Return platform uptime."""
        return {'uptime': platform.platform_uptime()}

    @json_response
    def platform_users(self, request):
        """Return logged users."""
        return {'users': platform.platform_users()}

    #: CPU
    @json_response
    def cpu(self, request):
        """Return information about CPU."""
        cpu_time = request.args.get('cpu_time', 0, type=int)
        return cpu.cpu(cpu_time=bool(cpu_time))

    @json_response
    def cpu_info(self, request):
        """Return basic information about CPU."""
        return cpu.cpu_info()

    @json_response
    def cpu_load(self, request):
        """Return CPU load for every logical core."""
        cpu_time = request.args.get('cpu_time', 0, type=int)
        return cpu.cpu_load(cpu_time=bool(cpu_time))

    @json_response
    def cpu_freq(self, request):
        """Return CPU frequency for every logical core."""
        return cpu.cpu_freq()

    #: Memory
    @json_response
    def memory(self, request):
        """Return memory metrics."""
        percent = request.args.get('percent', 0, type=int)
        return memory.memory(percent=bool(percent))

    @json_response
    def memory_ram(self, request):
        """Return RAM metrics."""
        percent = request.args.get('percent', 0, type=int)
        return memory.memory_ram(percent=bool(percent))

    @json_response
    def memory_swap(self, request):
        """Return swap metrics."""
        percent = request.args.get('percent', 0, type=int)
        return memory.memory_swap(percent=bool(percent))

    #: Disks
    @json_response
    def disks(self, request):
        """Return disks metrics."""
        percent = request.args.get('percent', 0, type=int)
        return disks.disks(percent=bool(percent))


def main():
    import argparse
    import time
    from werkzeug.serving import run_simple

    parser = argparse.ArgumentParser(prog='jacoren')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + _jacoren_version)
    parser.add_argument('--host',
                        type=str, default='localhost',
                        help='host IP address/name (default: localhost)')
    parser.add_argument('--port',
                        type=int, default='1313',
                        help='port (default: 1313)')
    args = parser.parse_args()

    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    server = JacorenServer()
    run_simple(args.host, args.port, server)
