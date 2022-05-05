#!/usr/bin/env python3

# BoBoBo

from driven.embed.sengine.buffer import HttpRequestBuffer


def test_append():
    bf = HttpRequestBuffer()
    bf.append(1, b'abc')
    assert bf.get_bytes(1) == b'abc'
    bf.append(1, b'123')
    assert bf.get_bytes(1) == b'abc123'
    bf.append(2, b'efg')
    assert bf.get_bytes(2) == b'efg'


def test_readline():
    bf = HttpRequestBuffer()
    bf.append(1, b'123\r\n456\r\n789')
    line = bf.read_line(1)
    assert line == '123'
    line = bf.read_line(1)
    assert line == '456'
    line = bf.read_line(1)
    assert line is None
    bf.append(1, b'10\r\n')
    line = bf.read_line(1)
    assert line == '78910'


def test_clear_read():
    bf = HttpRequestBuffer()
    bf.append(1, b'123\r\n456')
    line = bf.read_line(1)
    assert line == '123'
    assert bf.get_bytes(1) == bytearray(b'123\r\n456')
    bf.clear_read(1)
    assert bf.get_bytes(1) == bytearray(b'456')


def test_request_line():
    bf = HttpRequestBuffer()
    bf.append(1, b'123\r\n456\r\nGET /abc/efg HTTP/1.1\r\nother')
    request_line = bf.parse_http_request_line(1)
    assert request_line['REQUEST_METHOD'] == 'GET'
    assert request_line['PATH_INFO'] == '/abc/efg'
    assert request_line['QUERY_STRING'] == ''
    assert request_line['wsgi.version'] == (1, 1)


def test_headers():
    bf = HttpRequestBuffer()
    bf.append(1, b'Content-Length:10\r\nContent-')
    headers = bf.parse_http_headers(1)
    assert headers is None
    bf.append(1, b'Type:application/json\r\n')
    headers = bf.parse_http_headers(1)
    assert headers is None
    bf.append(1, b'Type:application/json\r\n\r\n')
    headers = bf.parse_http_headers(1)
    assert headers['Content-Length'] == '10'
    headers = bf.parse_http_headers(1)
    assert headers is None


def test_body():
    bf = HttpRequestBuffer()
    bf.append(1, b'Content-Length:5\r\n\r\n12345abc\r\n')
    headers = bf.parse_http_headers(1)
    body = bf.read_http_body(1, int(headers['Content-Length']))
    assert body == '12345'
    line = bf.read_line(1)
    assert line == 'abc'


def test_next_package():
    bf = HttpRequestBuffer()
    bf.append(1, b'123\r\n456\r\nGET /abc/efg HTTP/1.1\r\n')
    bf.append(1, b'Content-Length:5\r\n\r\n12345')
    bf.append(1, b'123\r\n456\r\nGET /abc/efg2 HTTP/1.1\r\n')
    bf.append(1, b'Content-Length:3\r\n\r\n12345')
    wsgi_request = bf.next_package(1)
    assert wsgi_request['PATH_INFO'] == '/abc/efg'
    assert wsgi_request['wsgi.input'].read(5) == b'12345'
    wsgi_request = bf.next_package(1)
    assert wsgi_request['PATH_INFO'] == '/abc/efg2'
    assert wsgi_request['wsgi.input'].read(3) == b'123'
