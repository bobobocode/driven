#!/usr/bin/env python3

# BoBoBo

import time
import pytest
from threading import Thread
import driven.embed.sengine.sengine as wsgi_server
from driven.driven_app import driven_app
from driven.tests.base import HttpServerTests
import driven.util as util
import driven.driven_process as driven_process


@pytest.fixture(scope='module', autouse=True)
def start_sengine():
    driven_processes = driven_process.start(
        'driven-test-process', './driven-process-test.yaml')
    t = Thread(target=wsgi_server.bootstrap_with_driven, args=(
        '', 8080, {'name': 'sengine'}), daemon=True)
    t.start()
    time.sleep(1)
    yield t
    print('close driven-process after tests')
    for p in driven_processes:
        p['process'].terminate()


class TestHttpServer(HttpServerTests):
    pass
