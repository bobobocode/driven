#!/usr/bin/env python3

# BoBoBo

import pytest
import driven.embed.wsgi_server as wsgi_server
from driven.driven_app import driven_app
from driven.tests.base import HttpServerTests
from threading import Thread
import driven.util as util


@pytest.fixture(scope='module', autouse=True)
def start_sengine():
    app = driven_app(
        'app_example', {'logger': util.get_logger({'name': 'app_example'})})

    t = Thread(target=wsgi_server.bootstrap,
               args=('', 8080, app), daemon=True)
    t.start()


class TestHttpServer(HttpServerTests):
    pass
