#!/usr/bin/env python3

# BoBoBo

import driven.tests.app_example.hello as hello


def test_hello():
    assert hello.hello(None, None, 'James') == 'Hello James!'
