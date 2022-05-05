#!/usr/bin/env python3

# BoBoBo

import asyncio
import tornado
import tornado.wsgi as wsgi
import tornado.httpserver as httpserver
import tornado.ioloop as ioloop


def bootstrap(port, app):
    asyncio.set_event_loop(asyncio.new_event_loop())
    container = wsgi.WSGIContainer(app)
    http_server = httpserver.HTTPServer(container)
    http_server.listen(port)
    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()
    print('tornado exit')
