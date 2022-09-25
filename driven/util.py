#!/usr/bin/env python3

# BoBoBo

import os
import signal
import socket
import sys
from argparse import ArgumentParser


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
