#!/usr/bin/env python3

# BoBoBo

import driven.util as util


def build_context(conf_file):
    return {'logger': util.get_logger(util.get_conf(conf_file, 'app_example')
                                      .get('log', {}))}
