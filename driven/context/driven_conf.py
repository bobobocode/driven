#!/usr/bin/env python3

# BoBoBo

import importlib
import sys
import os
import re
import driven.util as util


def get_conf(conf_file):
    return util.get_conf(conf_file, 'driven')


def get_mode(conf):
    return conf['mode']


def get_apps(conf):
    return conf['apps']


def get_app(conf, app_name):
    return get_apps(conf)[app_name]


def get_app_conf_file(conf, app_name):
    return get_app(conf, app_name)['conf_file']


def get_app_context_builder(conf, app_name):
    return get_app(conf, app_name)['context_builder']


def get_app_deploy(conf, app_name):
    return get_app(conf, app_name)['deploy']


def get_log(conf):
    return conf['log']


def get_log_level(conf):
    return get_log(conf)['level']


def get_log_path(conf):
    return get_log(conf)['path']
