#!/usr/bin/env python3

# BoBoBo

import json
import logging
import os
import random
import re
import signal
import socket
import sys
from argparse import ArgumentParser
from http.cookies import SimpleCookie

import yaml


def get_logger(conf={}):
    level = conf.get('level', logging.DEBUG)
    log_file = conf.get('path', 'default-log.txt')
    form = conf.get('pattern', None)
    logger_name = conf.get('name', None)
    if logger_name is None:
        logger_name = 'default-logger-' + str(random.randint(1, 100))

    return build_logger(logger_name, level, log_file, form)


def build_logger(logger_name, level, log_file, form=None):
    if not form:
        form = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(form)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConstError, 'Can not change const % s' % name)
        if not name.isupper():
            raise (self.ConstCaseError,
                   'Const name [%s] is not all uppercase' % name)
        self.__dict__[name] = value


def check_port(port, host='127.0.0.1'):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        sk.close()


def load_yaml(path):
    try:
        with open(path, mode='r') as cf:
            conf = yaml.load(cf, Loader=yaml.FullLoader)
    except Exception as ex:
        print('Failed to load conf for %s' % ex)
    else:
        return conf


def get_conf(conf_file, top_key=None):
    conf = load_yaml(conf_file)
    if not conf:
        print('Invalid configuration: %s' % conf)
        return None

    if not top_key:
        return conf

    if top_key not in conf:
        print('No %s in conf top_keys: %s' % (top_key, conf))
        return None
    return conf[top_key]


def install_requirements_file(requirements_path):
    return os.system('pip3 install -r ' + requirements_path)


def add_pythonpath(path):
    if not os.path.exists(path):
        raise Exception(
            'Cannot add %s in to module search path for not existing.' % path)

    if not (path in sys.path):
        sys.path.append(path)


def remove_pythonpath(path):
    if path in sys.path:
        sys.path.remove(path)


def parse_environ_parameters(method, environ):
    if method == 'GET':
        return parse_query_string(environ['QUERY_STRING'])
    elif method == 'POST':
        return parse_environ_body(environ)
    else:
        return {}


def parse_query_string(query):
    if not query:
        return None
    querys = query.split('&')
    querys = list(map(lambda s: s.split('='), querys))
    querys_key = list(map(lambda s: s[0], querys))
    querys_value = list(map(lambda s: s[1], querys))
    return dict(zip(querys_key, querys_value))


def parse_environ_body(environ):
    environ_body_size = int(environ.get('CONTENT_LENGTH', 0))

    if 0 != environ_body_size:
        environ_body = environ['wsgi.input'].read(environ_body_size)
        nd = environ_body.decode('utf-8')
        try:
            parameters = json.loads(nd)
        except json.JSONDecodeError:
            return nd
        else:
            return parameters
    else:
        return {}


def parse_http_request_line(line):
    ret = re.match(r'([A-Z]+) ([^( )]+) (HTTP.+)', line)
    if ret:
        method = ret.group(1)
        pathes = ret.group(2)
        protocol = tuple(map(lambda v: int(v), ret.group(3)[5:].split('.')))

        ret = re.match(r'([^( |?)]+)[?]?(.*)', pathes)
        path = ret.group(1)
        query_string = ret.group(2)
        return {
            'REQUEST_METHOD': method, 'PATH_INFO': path,
            'QUERY_STRING': query_string, 'wsgi.version': protocol
        }
    else:
        return None


def convert_wsgi_request(method, pathes, headers, body):
    request = {}
    request['PATH_INFO'] = pathes[0]
    request['REQUEST_METHOD'] = method
    request['CONTENT_LENGTH'] = headers.get('Content-Length', 0)
    request['CONTENT_TYPE'] = headers.get(
        'Content-Type', 'application/json')

    class StrFile:

        def __init__(self, s):
            if str:
                self.content = s.encode('utf-8')
            else:
                self.content = None

        def read(self, size):
            if self.content:
                return self.content[:size]
            else:
                return []

    request['wsgi.input'] = StrFile(body)

    if len(pathes) > 1:
        request['QUERY_STRING'] = pathes[1]
    else:
        request['QUERY_STRING'] = None

    cookies = SimpleCookie(headers.get('Cookie'))
    request['HTTP_COOKIE'] = cookies

    return request


def set_serv_signal():
    def sigusr1(signum, frame):
        print('Receive signal: %i' % signum)

    def sigusr2(signum, frame):
        print('Receive signal: %i' % signum)

    signal.signal(signal.SIGUSR1, sigusr1)
    signal.signal(signal.SIGUSR2, sigusr2)


def get_server_cmdargs():
    parser = ArgumentParser()
    opt = parser.add_argument
    opt('-t', '--host', dest='host',
        help='Host to listen', default='')
    opt('-p', '--port', dest='port', type=int,
        help='Port to listen', default=8080)
    opt('-c', '--conf_path', dest='conf_path',
        help='Config file path')
    opt('-m', '--mode', dest='mode',
        help='Optional param')
    return parser.parse_args()
