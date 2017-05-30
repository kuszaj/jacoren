# -*- coding: utf-8 -*-

from __future__ import print_function
import json
from jacoren import (
    __version__ as version,
    platform,
    cpu,
)

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    #: Python 2.7
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


def _func_to_dict(func):
    return lambda: {func.__name__: func()}


class GetHandler(BaseHTTPRequestHandler):
    request_version = 'HTTP/1.1'
    server_version = 'jacoren/' + version

    #: Predefined paths
    _paths = {
        #: Plaform
        'platform': platform.platform,
        #: CPU
        'cpu': cpu.cpu,
        'cpu/info': cpu.cpu_info,
        'cpu/load': _func_to_dict(cpu.cpu_load),
        'cpu/freq': _func_to_dict(cpu.cpu_freq),
    }

    def do_GET(self):
        #: Remove leading '/'
        path = self.path[1:]

        try:
            #: Respond with jsonified dictionary
            response = GetHandler._paths[path]()
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
    parser.add_argument('--host',
                        type=str, default='127.0.0.1',
                        help='Host IP/address')
    parser.add_argument('--port',
                        type=int, default='1313',
                        help='Port')
    args = parser.parse_args()

    server = Server((args.host, args.port), GetHandler)
    server.serve_forever()
