#!/usr/bin/env python3

# BoBoBo

import traceback

import driven.util as util


def get_from_yaml(conf_file, keys):
    conf = util.load_conf(conf_file)
    keys = keys.split('.')
    try:
        for k in keys:
            conf = conf[k]
        return conf
    except KeyError:
        traceback.print_exc()
        return ''


def check_conf_file(conf_file, top_key):
    conf = util.load_conf(conf_file)
    if not conf:
        return False

    if top_key not in conf:
        print('Not Found key: %s in conf file: %s.' % (top_key, conf_file))
        return False

    return True


def install_requirements(conf_file):
    conf = util.load_conf(conf_file)
    for r in conf['python']['requirements']:
        print('Deal with requiremnts: %s' % r)
        if util.install_requirements_file(r):
            raise Exception('Failed to install requiremnts: %s' % r)
