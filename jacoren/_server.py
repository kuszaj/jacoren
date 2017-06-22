# -*- coding: utf-8 -*-

"""Utilities for running REST API."""

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
    """Decorate function so it returns JSON response."""
    @wraps(func)
    def new(inst, *args, **kwargs):
        result = func(inst, *args, **kwargs)

        if result is None:
            raise NotFound

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


class JacorenRule(Rule):
    """Extended Rule."""

    def __init__(self, *args, **kwargs):
        """Same as Rule but with description for doc rule."""
        self.doc_rule = kwargs.pop('doc_rule', None)
        self.doc_desc = kwargs.pop('doc_desc', None)

        super(JacorenRule, self).__init__(*args, **kwargs)
        self.strict_slashes = False
        if self.doc_rule is None:
            self.doc_rule = self.rule


class JacorenServer(object):
    """WSGI server class."""

    def __init__(self):
        """Init resource paths."""
        self.paths = Map((
            #: Docs
            JacorenRule('/', endpoint='api_help',
                        doc_desc='This help resource'),

            #: Plaform
            JacorenRule('/platform', endpoint='platform',
                        doc_desc='Platform info'),
            JacorenRule('/platform/uptime', endpoint='platform_uptime',
                        doc_desc='Uptime in seconds'),
            JacorenRule('/platform/users', endpoint='platform_users',
                        doc_desc='Logged users'),

            #: CPU
            JacorenRule('/cpu', endpoint='cpu',
                        doc_desc='CPU info'),
            JacorenRule('/cpu/<int:core>', endpoint='cpu',
                        doc_desc='CPU core info', doc_rule='/cpu/<core>'),
            JacorenRule('/cpu/info', endpoint='cpu_info',
                        doc_desc='CPU basic info'),
            JacorenRule('/cpu/load', endpoint='cpu_load',
                        doc_desc='CPU load'),
            JacorenRule('/cpu/load/<int:core>', endpoint='cpu_load',
                        doc_desc='CPU core load', doc_rule='/cpu/load/<core>'),
            JacorenRule('/cpu/freq', endpoint='cpu_freq',
                        doc_desc='CPU frequency'),
            JacorenRule('/cpu/freq/<int:core>', endpoint='cpu_freq',
                        doc_desc='CPU core frequency', doc_rule='/cpu/freq/<core>'),

            #: Memory
            JacorenRule('/memory', endpoint='memory',
                        doc_desc='Memory metrics'),
            JacorenRule('/memory/ram', endpoint='memory_ram',
                        doc_desc='RAM metrics'),
            JacorenRule('/memory/swap', endpoint='memory_swap',
                        doc_desc='Swap metrics'),

            #: Disks
            JacorenRule('/disks', endpoint='disks',
                        doc_desc='Disks metrics'),
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
        """Return response with HTTP error."""
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

    @json_response
    def api_help(self, request):
        """Return API help."""
        return [OrderedDict((
            ('uri', rule.doc_rule),
            ('description', rule.doc_desc)
        )) for rule in self.paths.iter_rules()]

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
    def cpu(self, request, core=None):
        """Return information about CPU."""
        cpu_time = request.args.get('cpu_time', 0, type=int)
        return cpu.cpu(cpu_time=bool(cpu_time),
                       core=core)

    @json_response
    def cpu_info(self, request):
        """Return basic information about CPU."""
        return cpu.cpu_info()

    @json_response
    def cpu_load(self, request, core=None):
        """Return CPU load for every logical core."""
        cpu_time = request.args.get('cpu_time', 0, type=int)
        return cpu.cpu_load(cpu_time=bool(cpu_time),
                            core=core)

    @json_response
    def cpu_freq(self, request, core=None):
        """Return CPU frequency for every logical core."""
        return cpu.cpu_freq(core=core)

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


def wsgi(environ, start_response):
    """WSGI interface."""
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    server = JacorenServer()
    return server.wsgi(environ, start_response)


def main():
    """
    Run single-threaded server.

    Note: This should be used only if REST API will be called by
    localhost. Otherwise, wsgi() function should be used.
    """
    import argparse
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
