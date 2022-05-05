#!/usr/bin/env python3

#BoBoBo#

from wsgiref.simple_server import make_server


def bootstrap(host, port, app):
    httpd = make_server(host, port, app)
    print('Simple WSGI Server is starting on %s:%s ...' % (host, port))
    httpd.serve_forever()
