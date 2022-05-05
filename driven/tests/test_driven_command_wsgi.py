#!/usr/bin/env python3

# BoBoBo

import time
import pytest
from threading import Thread
from driven.tests.base import HttpServerTests


@pytest.fixture(scope='module', autouse=True)
def start_sengine():

    def shell_start():
        import os
        os.system(
            'driven.sh --command wsgi --port 8080 --driven-app app_example:./driven-process-test.yaml')

    t = Thread(target=shell_start, daemon=True)
    t.start()
    time.sleep(2)
    yield t
    print('close driven-process after tests')


class TestHttpServer(HttpServerTests):
    pass
