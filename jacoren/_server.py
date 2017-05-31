# -*- coding: utf-8 -*-

from __future__ import print_function
import json
from functools import wraps
from collections import Iterable, OrderedDict

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    #: Python 2.7
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

try:
    from urllib.parse import parse_qs
except ImportError:
    #: Python 2.7
    from urlparse import parse_qs

from jacoren import (
    __version__ as jacoren_version,
    platform,
    cpu,
    memory,
)


def _cast_arg(arg):
    if isinstance(arg, Iterable) and not isinstance(arg, str):
        if len(arg) == 0:
            return None
        elif len(arg) == 1:
            arg = arg[0]
        else:
            return arg

    if isinstance(arg, str):
        if arg.isdigit():
            return int(arg)

    return arg
    

def _for_api(func, in_dict=False):
    @wraps(func)
    def _new_func(**kwargs):
        accepted = func.__code__.co_varnames

        if 'kwargs' not in accepted:
            kwargs = {k: _cast_arg(v) for k,v in kwargs.items()
                      if k in accepted}

        if in_dict:
            return OrderedDict([
                (func.__name__, func(**kwargs))
            ])

        return func(**kwargs)

    return _new_func


class GetHandler(BaseHTTPRequestHandler):
    request_version = 'HTTP/1.1'
    server_version = 'jacoren/' + jacoren_version

    #: Predefined paths
    _paths = {
        #: Plaform
        'platform': _for_api(platform.platform),
        'platform/uptime': _for_api(platform.platform_uptime,
                                    in_dict=True),
        'platform/users': _for_api(platform.platform_users,
                                   in_dict=True),

        #: CPU
        'cpu': _for_api(cpu.cpu),
        'cpu/info': _for_api(cpu.cpu_info),
        'cpu/load': _for_api(cpu.cpu_load, in_dict=True),
        'cpu/freq': _for_api(cpu.cpu_freq, in_dict=True),

        #: Memory
        'memory': _for_api(memory.memory),
        'memory/ram': _for_api(memory.memory_ram),
        'memory/swap': _for_api(memory.memory_swap),

    }

    def do_GET(self):
        #: Remove leading '/'
        path = self.path[1:]

        #: Split arguments
        try:
            path, kwargs = path.split('?', 1)
            kwargs = parse_qs(kwargs)
        except:
            kwargs = {}

        #: Remove '/' at the end
        if path.endswith('/'):
            path = path[:-1]

        try:
            #: Respond with jsonified dictionary
            response = GetHandler._paths[path](**kwargs)
            self._send_response(200, response)
        except KeyError:
            #: Undefined path
            response = {'message': '%s not found' % (path,)}
            self._send_response(404, response)

    def _get_message(self, d):
        message = json.dumps(d)
        try:
            message = bytes(message, 'utf8')
        except:
            #: Python 2.7
            pass

        return message

    def _set_header(self, code, message):
        self.send_response(code)

        #: Main headers
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(message))

        #:
        #: A man is not dead while his name is still spoken.
        #:                  ~ Going Postal, Chapter 4 prologue
        #:
        #: See: gnuterrypratchett.com
        #:
        self.send_header('X-Clacks-Overhead', 'GNU Terry Pratchett')

        self.end_headers()

    def _send_response(self, code, response):
        message = self._get_message(response)
        self._set_header(code, message)
        self.wfile.write(message)


class Server(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        print("Starting server on %s:%d" % (self.server_name,
                                            self.server_port))


def main():
    import argparse

    parser = argparse.ArgumentParser(prog='jacoren')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + jacoren_version)
    parser.add_argument('--host',
                        type=str, default='127.0.0.1',
                        help='host IP address/name (default: localhost)')
    parser.add_argument('--port',
                        type=int, default='1313',
                        help='port (default: 1313)')
    args = parser.parse_args()

    server = Server((args.host, args.port), GetHandler)
    server.serve_forever()
