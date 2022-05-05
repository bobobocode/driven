#!/usr/bin/env python3

# BoBoBo

import time
import pytest
from threading import Thread
import driven.embed.sengine.sengine as wsgi_server
from driven.driven_app import driven_app
from driven.tests.base import HttpServerTests
import driven.util as util


@pytest.fixture(scope='module', autouse=True)
def start_sengine():
    app = driven_app('app_example', {'logger':
                                     util.get_logger({'name': 'app_example'})})
    t = Thread(target=wsgi_server.bootstrap,
               args=('', 8080, {'app_example': app}, {'name': 'sengine'}), daemon=True)
    t.start()
    time.sleep(3)


class TestHttpServer(HttpServerTests):
    pass
