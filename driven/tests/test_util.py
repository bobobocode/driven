#!/usr/bin/env python3

# BoBoBo

import driven.util as util


def test_parse_http_request_line():
    header_line = 'GET /1/2/3?k1=v1&k2=v2 HTTP/1.1'
    request_line = util.parse_http_request_line(header_line)
    method = request_line['REQUEST_METHOD']
    path = request_line['PATH_INFO']
    query_string = request_line['QUERY_STRING']
    protocol = request_line['wsgi.version']
    assert method == 'GET'
    assert path == '/1/2/3'
    assert query_string == 'k1=v1&k2=v2'
    assert protocol == (1, 1)


def test_parse_http_request_line2():
    header_line = 'GET /1/2/3 HTTP/1.1'
    request_line = util.parse_http_request_line(header_line)
    method = request_line['REQUEST_METHOD']
    path = request_line['PATH_INFO']
    query_string = request_line['QUERY_STRING']
    protocol = request_line['wsgi.version']
    assert method == 'GET'
    assert path == '/1/2/3'
    assert query_string == ''
    assert protocol == (1, 1)
