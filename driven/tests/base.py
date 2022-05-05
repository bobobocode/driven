#!/usr/bin/env python3

# BoBoBo

import requests
import json


class HttpServerTests:

    def test_get_hello(self):
        resp = requests.get(
            'http://localhost:8080/app_example/hello?name=James')
        assert resp.text == 'Hello James!'

    def test_post_hello(self):
        resp = requests.post(
            'http://localhost:8080/app_example/hello', data=json.dumps({'name': 'James'}))
        assert resp.text == 'Hello James!'

        resp = requests.post(
            'http://localhost:8080/app_example/hello', data="abc")
        assert resp.text == 'Hello abc!'

    def test_404(self):
        resp = requests.post(
            'http://localhost:8080/app_example/hhello', data="abc")
        assert resp.status_code == 404
        resp = requests.post(
            'http://localhost:8080/aapp_example/hello', data="abc")
        assert resp.status_code == 404
        resp = requests.post(
            'http://localhost:8080', data=json.dumps({'name': 'James'}))
        assert resp.status_code == 404
